#!/usr/bin/env python3
"""Run domain-specific DenoiseOpt search for Table 10 boards (Multi-family, Factory+FX, AKWF OA).

Compares zero-shot E2 (2026072701), zero-shot SeamN2N, DualCosine, and domain-searched
DenoiseOpt on disjoint held-out splits for each board.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import torch

PAPER_ROOT = Path(__file__).resolve().parents[1]
REEL_ARTIFACTS = Path("/home/s4il0r/reel_runs/src/reeldemo-reelsynth-0a8567b")
sys.path.insert(0, str(PAPER_ROOT / "scripts" / "engine"))
sys.path.insert(0, "/home/s4il0r/reelsynth/scripts")

from holdout_eval import load_hybrid_champ, load_n2n  # noqa: E402
import gpu_rl_arch as og  # noqa: E402
import bench_sota_matrix as bsm  # noqa: E402
import real_wt_wrap_protocol as rw  # noqa: E402
import bench_signal_heal_transfer as bsht  # noqa: E402


class MultiFamilyBatcher:
    """Drop-in og.make_batch for multi-family training (seeds disjoint from 20260719..20260723)."""

    def __init__(self, device: torch.device, seed: int = 1337):
        self.device = device
        self.step = 0
        self.n = 64 * len(bsm.FAMILIES)
        self.l = og.N
        self.rng = np.random.default_rng(seed)
        # Pre-generate held-out batch for internal holdout() check
        torch.manual_seed(20260719)
        if device.type == "cuda":
            torch.cuda.manual_seed_all(20260719)
        self.hold_i, self.hold_e = bsm.make_family_batch("harmonic_fft", 64, og.N, device, seed=20260719)

    def __call__(self, batch: int, n: int, device: torch.device) -> tuple[torch.Tensor, torch.Tensor]:
        self.step += 1
        fam = bsm.FAMILIES[int(self.rng.integers(0, len(bsm.FAMILIES)))]
        s = int(self.rng.integers(1000, 999999))
        return bsm.make_family_batch(fam, batch, n, device, seed=s)

    def holdout(self, n: int = 64, seed: int = 20260719) -> tuple[torch.Tensor, torch.Tensor]:
        return self.hold_i[:n], self.hold_e[:n]


class TensorSplitBatcher:
    """Drop-in og.make_batch over a disjoint training slice of (ideal, engine)."""

    def __init__(self, train_i: torch.Tensor, train_e: torch.Tensor, test_i: torch.Tensor, test_e: torch.Tensor):
        self.train_i = train_i
        self.train_e = train_e
        self.test_i = test_i
        self.test_e = test_e
        self.n = int(train_i.shape[0])
        self.l = int(train_i.shape[1])

    def __call__(self, batch: int, n: int, device: torch.device) -> tuple[torch.Tensor, torch.Tensor]:
        idx = torch.randint(0, self.n, (batch,), device=device)
        return self.train_i[idx], self.train_e[idx]

    def holdout(self, n: int = 64, seed: int = 20260719) -> tuple[torch.Tensor, torch.Tensor]:
        return self.test_i[:n], self.test_e[:n]


def load_domain_champ(out_dir: Path, dev: torch.device):
    summ = json.loads((out_dir / "summary.json").read_text(encoding="utf-8"))
    cfg = og.ArchConfig.from_dict(summ["champ_arch"])
    cell = og.SeamCell(cfg).to(dev)
    sd = torch.load(out_dir / "champ_cell.pt", map_location=dev, weights_only=False)
    cell.load_state_dict(sd)
    cell.eval()

    def fn(eng: torch.Tensor) -> torch.Tensor:
        return og.apply_ops(eng, cell, cfg.ops)

    return fn, cfg, cell, summ


def run_and_score_board(
    name: str,
    batcher,
    eval_fn,
    *,
    dev: torch.device,
    out_root: Path,
    iters: int = 80,
    fit_steps: int = 100,
    seed: int = 2026072701,
) -> dict:
    t0 = time.time()
    out_dir = out_root / name
    if (out_dir / "champ_cell.pt").is_file() and (out_dir / "summary.json").is_file():
        print(f"[{name}] reusing existing {out_dir}", flush=True)
    else:
        bsht.run_hybrid_lstm_domain(
            batcher,
            iters=iters,
            seed=seed,
            device=dev,
            out_dir=out_dir,
            fit_steps=fit_steps,
            batch=64,
            pop_size=12,
        )
    champ_fn, cfg, cell, summ = load_domain_champ(out_dir, dev)
    scores = eval_fn(champ_fn)
    dt = time.time() - t0
    n_params = sum(p.numel() for p in cell.parameters())
    print(f"[{name}] done in {dt:.1f}s | params={n_params} | scores={scores}", flush=True)
    return {
        "board": name,
        "wall_s": round(dt, 2),
        "champ_ops": list(cfg.ops),
        "champ_blocks": list(cfg.blocks),
        "champ_params": int(n_params),
        "scores": scores,
    }


def main() -> int:
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    n2n_fn, _ = load_n2n(REEL_ARTIFACTS, dev)
    e2_root = REEL_ARTIFACTS / "brand/artifacts/meta_approach_compare_v14_converge"
    zs_fn, _, _ = load_hybrid_champ(e2_root / "2026072701/hybrid_lstm/champ_cell.pt", dev)

    out_root = PAPER_ROOT / "results" / "domain_search_table10"
    out_root.mkdir(parents=True, exist_ok=True)
    eval_seeds = [20260719, 20260720, 20260721, 20260722, 20260723]

    results = {}

    # 1. Multi-family
    wave_specs = [(fam, wseed) for wseed in bsm.WAVEFORM_SEEDS for fam in bsm.FAMILIES]

    def eval_multifamily(fn) -> dict:
        seed_means = []
        with torch.no_grad():
            for s in eval_seeds:
                w_vals = []
                for fam, wseed in wave_specs:
                    ideal, eng = bsm.make_family_batch(fam, 64, og.N, dev, seed=s + wseed)
                    w_vals.append(float(og.residual_score_blend(ideal, eng, fn(eng)).mean().item()))
                seed_means.append(float(np.mean(w_vals)))
        return {"mean": float(np.mean(seed_means)), "std": float(np.std(seed_means, ddof=1))}

    mf_res = run_and_score_board("multi_family", MultiFamilyBatcher(dev), eval_multifamily, dev=dev, out_root=out_root)
    mf_res["baselines"] = {
        "e2_zeroshot": eval_multifamily(zs_fn),
        "n2n_zeroshot": eval_multifamily(n2n_fn),
        "dual_cosine": eval_multifamily(og.dual_cosine_blend),
    }
    results["multi_family"] = mf_res

    # 2. Factory+FX (80/20 split of 1280 cycles)
    cyc_f = rw.load_reelsynth_export(rw.ART / "reelsynth_export_cycles.json", dev)
    closed_f = rw.close_seam_ideal(cyc_f)
    ideal_f, eng_f = rw.apply_open_wrap_cliff(closed_f, seed=rw.PROTOCOL_SEED)
    g = torch.Generator(device="cpu").manual_seed(20260719)
    perm_f = torch.randperm(ideal_f.shape[0], generator=g).to(dev)
    n_tr_f = int(0.8 * ideal_f.shape[0])
    tr_idx_f, te_idx_f = perm_f[:n_tr_f], perm_f[n_tr_f:]

    def eval_split(fn, ii, ee) -> dict:
        with torch.no_grad():
            r = og.residual_score_blend(ii, ee, fn(ee))
            return {"mean": float(r.mean().item()), "n": int(ii.shape[0])}

    f_batcher = TensorSplitBatcher(ideal_f[tr_idx_f], eng_f[tr_idx_f], ideal_f[te_idx_f], eng_f[te_idx_f])
    f_res = run_and_score_board(
        "factory_fx", f_batcher, lambda fn: eval_split(fn, ideal_f[te_idx_f], eng_f[te_idx_f]), dev=dev, out_root=out_root
    )
    f_res["baselines"] = {
        "e2_zeroshot": eval_split(zs_fn, ideal_f[te_idx_f], eng_f[te_idx_f]),
        "n2n_zeroshot": eval_split(n2n_fn, ideal_f[te_idx_f], eng_f[te_idx_f]),
        "dual_cosine": eval_split(og.dual_cosine_blend, ideal_f[te_idx_f], eng_f[te_idx_f]),
    }
    results["factory_fx"] = f_res

    # 3. AKWF OA (80/20 split of 1280 wavs)
    cyc_a = rw.load_oa_wav_cycles(rw.ART / "oa_akwf", dev, n_max=1280)
    closed_a = rw.close_seam_ideal(cyc_a)
    ideal_a, eng_a = rw.apply_open_wrap_cliff(closed_a, seed=rw.PROTOCOL_SEED)
    g2 = torch.Generator(device="cpu").manual_seed(20260719)
    perm_a = torch.randperm(ideal_a.shape[0], generator=g2).to(dev)
    n_tr_a = int(0.8 * ideal_a.shape[0])
    tr_idx_a, te_idx_a = perm_a[:n_tr_a], perm_a[n_tr_a:]

    a_batcher = TensorSplitBatcher(ideal_a[tr_idx_a], eng_a[tr_idx_a], ideal_a[te_idx_a], eng_a[te_idx_a])
    a_res = run_and_score_board(
        "akwf_oa", a_batcher, lambda fn: eval_split(fn, ideal_a[te_idx_a], eng_a[te_idx_a]), dev=dev, out_root=out_root
    )
    a_res["baselines"] = {
        "e2_zeroshot": eval_split(zs_fn, ideal_a[te_idx_a], eng_a[te_idx_a]),
        "n2n_zeroshot": eval_split(n2n_fn, ideal_a[te_idx_a], eng_a[te_idx_a]),
        "dual_cosine": eval_split(og.dual_cosine_blend, ideal_a[te_idx_a], eng_a[te_idx_a]),
    }
    results["akwf_oa"] = a_res

    out_json = PAPER_ROOT / "results" / "table10_domain_search.json"
    out_json.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("WROTE", out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
