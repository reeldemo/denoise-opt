#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1]
PAPER = ENGINE.parents[1]
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))


def _has_torch_and_reelsynth() -> bool:
    try:
        import torch  # noqa: F401
    except ImportError:
        return False
    root = os.environ.get("REELSYNTH_ROOT")
    if not root:
        return False
    baselines = Path(root) / "scripts" / "baselines"
    n2n = Path(root) / "brand/artifacts/n2n_seam_baselines/n2n_corrupt_corrupt.pt"
    return baselines.is_dir() and n2n.is_file()


@unittest.skipUnless(_has_torch_and_reelsynth(), "needs torch + REELSYNTH_ROOT")
class TestRefitAsIs(unittest.TestCase):
    def test_as_is_matches_holdout_subset(self) -> None:
        os.environ.setdefault("PAPER_PYTHON", sys.executable)
        from common import bootstrap_reelsynth  # noqa: E402
        from holdout_eval import eval_holdout  # noqa: E402
        from refit_holdout import run_refit  # noqa: E402

        root = bootstrap_reelsynth()
        champ = PAPER / "legacy_meta/artifacts/models/paper-e4-hybrid_ppo_only-dry-1902771841/fitted/final_champion_fitted.pt"
        if not champ.is_file():
            self.skipTest("legacy champion artifact missing")
        seeds = (20260719, 20260720)
        with tempfile.TemporaryDirectory() as td:
            hout = Path(td) / "holdout.json"
            rout = Path(td) / "refit.json"
            ref_payload = run_refit(
                champ=champ,
                mode="as_is",
                init="fresh",
                eval_seeds=seeds,
                batch=8,
                refit_seed=424242,
                device="cpu",
                dry_run=True,
            )
            hold = eval_holdout(
                champ_path=champ,
                eval_seeds=seeds,
                batch=8,
                device="cpu",
                dry_run=True,
            )
            for seed in seeds:
                rs = ref_payload["per_seed"][str(seed)]["hybrid"]
                hs = hold["per_seed"][str(seed)]["hybrid"]
                self.assertAlmostEqual(rs, hs, places=6)
            rout.write_text(json.dumps(ref_payload), encoding="utf-8")
            hout.write_text(json.dumps(hold), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()