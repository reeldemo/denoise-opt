#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import torch

ENGINE = Path(__file__).resolve().parents[1]
PAPER = ENGINE.parents[1]
REELSYNTH = Path("/agent/repos/reelsynth")
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))
if REELSYNTH.is_dir():
    os.environ.setdefault("REELSYNTH_ROOT", str(REELSYNTH))


def _legacy_champ() -> Path | None:
    champ = (
        PAPER
        / "legacy_meta/artifacts/models/paper-e4-hybrid_ppo_only-dry-1902771841/fitted/final_champion_fitted.pt"
    )
    return champ if champ.is_file() else None


def _has_torch_and_reelsynth() -> bool:
    root = os.environ.get("REELSYNTH_ROOT")
    if not root:
        return False
    baselines = Path(root) / "scripts" / "baselines"
    n2n = Path(root) / "brand/artifacts/n2n_seam_baselines/n2n_corrupt_corrupt.pt"
    return baselines.is_dir() and n2n.is_file()


class TestInitModes(unittest.TestCase):
    def test_fresh_vs_search_weights_differ(self) -> None:
        champ = _legacy_champ()
        if champ is None:
            self.skipTest("legacy champion artifact missing")
        from refit_holdout import build_cell_from_champion, load_champion_blob  # noqa: E402

        dev = torch.device("cpu")
        cfg, state, _lr, _blob = load_champion_blob(champ, dev)
        search_cell = build_cell_from_champion(cfg, state, device=dev, init="search", refit_seed=1)
        fresh_cell = build_cell_from_champion(cfg, state, device=dev, init="fresh", refit_seed=424242)
        s0 = next(p for p in search_cell.parameters() if p.numel() > 0).detach().clone()
        f0 = next(p for p in fresh_cell.parameters() if p.numel() > 0).detach().clone()
        self.assertFalse(torch.allclose(s0, f0))

    def test_fresh_init_is_reproducible(self) -> None:
        champ = _legacy_champ()
        if champ is None:
            self.skipTest("legacy champion artifact missing")
        from refit_holdout import build_cell_from_champion, load_champion_blob  # noqa: E402

        dev = torch.device("cpu")
        cfg, state, _lr, _blob = load_champion_blob(champ, dev)
        a = build_cell_from_champion(cfg, state, device=dev, init="fresh", refit_seed=99)
        b = build_cell_from_champion(cfg, state, device=dev, init="fresh", refit_seed=99)
        pa = next(p for p in a.parameters() if p.numel() > 0).detach()
        pb = next(p for p in b.parameters() if p.numel() > 0).detach()
        self.assertTrue(torch.allclose(pa, pb))


class TestPlateauValidationBatch(unittest.TestCase):
    def test_training_batch_differs_from_fixed_validation(self) -> None:
        champ = _legacy_champ()
        if champ is None:
            self.skipTest("legacy champion artifact missing")
        from refit_holdout import (  # noqa: E402
            _import_gpu_rl_arch,
            REFIT_VAL_SEED,
            build_cell_from_champion,
            load_champion_blob,
            make_batch_with_generator,
        )

        og = _import_gpu_rl_arch()
        dev = torch.device("cpu")
        cfg, state, _lr, _blob = load_champion_blob(champ, dev)
        cell = build_cell_from_champion(cfg, state, device=dev, init="search", refit_seed=0)
        ops = list(cfg.ops)
        batch = 8
        val_gen = torch.Generator(device=dev)
        val_gen.manual_seed(REFIT_VAL_SEED)
        val_ideal, val_eng = make_batch_with_generator(batch, og.N, dev, val_gen)
        # Simulate post-validation training step without re-seeding global RNG.
        torch.manual_seed(123456789)
        train_ideal, train_eng = og.make_batch(batch, og.N, dev)
        self.assertFalse(torch.allclose(val_eng, train_eng))
        self.assertFalse(torch.allclose(val_ideal, train_ideal))
        with torch.no_grad():
            vout = og.apply_ops(val_eng, cell, ops)
            tout = og.apply_ops(train_eng, cell, ops)
        self.assertFalse(torch.allclose(vout, tout))


class TestRefitAsIs(unittest.TestCase):
    @patch("refit_holdout.bootstrap_reelsynth")
    @patch("holdout_eval.load_n2n")
    def test_as_is_matches_holdout_subset(self, mock_load_n2n, mock_boot) -> None:
        mock_boot.return_value = REELSYNTH
        from holdout_eval import eval_holdout, score_seed  # noqa: E402
        from refit_holdout import (  # noqa: E402
            _import_gpu_rl_arch,
            build_cell_from_champion,
            load_champion_blob,
            run_refit,
        )

        mock_load_n2n.return_value = (lambda x: x, "stub-n2n.pt")

        champ = _legacy_champ()
        if champ is None:
            self.skipTest("legacy champion artifact missing")
        seeds = (20260719, 20260720)
        ref_payload = run_refit(
            champ=champ,
            mode="as_is",
            init="search",
            eval_seeds=seeds,
            batch=8,
            refit_seed=424242,
            device="cpu",
            dry_run=True,
        )
        eval_seeds = tuple(ref_payload["eval_seeds"])
        dev = torch.device("cpu")
        og = _import_gpu_rl_arch()
        cfg, state, _, _ = load_champion_blob(champ, dev)
        cell = build_cell_from_champion(cfg, state, device=dev, init="search", refit_seed=0)
        ops = list(cfg.ops)

        def hybrid_fn(eng: torch.Tensor) -> torch.Tensor:
            return og.apply_ops(eng, cell, ops)

        for seed in eval_seeds:
            rs = ref_payload["per_seed"][str(seed)]["hybrid"]
            hs = score_seed(seed, device=dev, batch=8, methods={"hybrid": hybrid_fn})["hybrid"]
            self.assertAlmostEqual(rs, hs, places=6)

        if _has_torch_and_reelsynth():
            hold = eval_holdout(
                champ_path=champ,
                eval_seeds=eval_seeds,
                batch=8,
                device="cpu",
                dry_run=True,
            )
            for seed in eval_seeds:
                rs = ref_payload["per_seed"][str(seed)]["hybrid"]
                hs = hold["per_seed"][str(seed)]["hybrid"]
                self.assertAlmostEqual(rs, hs, places=6)


if __name__ == "__main__":
    unittest.main()