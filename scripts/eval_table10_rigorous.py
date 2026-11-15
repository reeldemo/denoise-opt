#!/usr/bin/env python3
"""Rigorous 10-seed + domain-trained N2N evaluation for Table 10 with Holm-Bonferroni correction."""
from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from scipy.stats import wilcoxon

PAPER_ROOT = Path(__file__).resolve().parents[1]
REEL_ARTIFACTS = Path("/home/s4il0r/reel_runs/src/reeldemo-reelsynth-0a8567b")
sys.path.insert(0, str(PAPER_ROOT / "scripts" / "engine"))
sys.path.insert(0, "/home/s4il0r/reelsynth/scripts")

from holdout_eval import load_hybrid_champ, load_n2n  # noqa: E402
from baselines.n2n_seam import SeamN2N  # noqa: E402
import overnight_gpu_rl_arch as og  # noqa: E402
import bench_sota_matrix as bsm  # noqa: E402
import real_wt_wrap_protocol as rw  # noqa: E402
import train_n2n_transfer_domains as tnt  # noqa: E402


def load_domain_champ(out_dir: Path, dev: torch.device):
    summ = json.loads((out_dir / "summary.json").read_text(encoding="utf-8"))
    cfg = og.ArchConfig.from_dict(summ["champ_arch"])
    cell = og.SeamCell(cfg).to(dev)
    sd = torch.load(out_dir / "champ_cell.pt", map_location=dev, weights_only=False)
    cell.load_state_dict(sd)
    cell.eval()
    return (lambda eng: og.apply_ops(eng, cell, cfg.ops)), cfg


def exact_sign_flip_p(deltas: np.ndarray) -> float:
    n = len(deltas)
    obs = abs(float(np.mean(deltas)))
    cnt = 0
    total = 1 << n
    for signs in itertools.product((-1.0, 1.0), repeat=n):
        m = abs(float(np.mean(deltas * np.array(signs))))
        if m >= obs - 1e-12:
            cnt += 1
    return cnt / total


def bootstrap_ci(deltas: np.ndarray, n_boot: int = 10000, seed: int = 42) -> list[float]:
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(deltas), size=(n_boot, len(deltas)))
    means = deltas[idx].mean(axis=1)
    return [float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))]


def train_domain_n2n(train_ideal: torch.Tensor, dev: torch.device, steps: int = 4000, batch: int = 64, lr: float = 1e-3):
    model = SeamN2N().to(dev)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    rng = np.random.default_rng(424242)
    torch.manual_seed(424242)
    if dev.type == "cuda":
        torch.cuda.manual_seed_all(424242)
    n_train = int(train_ideal.shape[0])
    for _ in range(steps):
        idx = torch.randint(0, n_train, (min(batch, n_train),), device=dev)
        bi = train_ideal[idx]
        a, b = tnt.cliff_pair(bi, rng)
        loss = 0.5 * (F.mse_loss(model(a), b) + F.mse_loss(model(b), a))
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
    model.eval()
    return model


def holm_bonferroni(pvals: dict[str, float]) -> dict[str, float]:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    adj = {}
    prev = 0.0
    for rank, (k, p) in enumerate(items):
        val = min(1.0, max(prev, p * (m - rank)))
        adj[k] = val
        prev = val
    return adj


def main() -> int:
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    n2n_fn, _ = load_n2n(REEL_ARTIFACTS, dev)
    e2_root = REEL_ARTIFACTS / "brand/artifacts/meta_approach_compare_v14_converge"
    c_2702, _, _ = load_hybrid_champ(e2_root / "2026072702/hybrid_lstm/champ_cell.pt", dev)
    c_2701, _, _ = load_hybrid_champ(e2_root / "2026072701/hybrid_lstm/champ_cell.pt", dev)

    eval_seeds_10 = list(range(20260719, 20260729))
    out: dict = {"eval_seeds_10": eval_seeds_10}

    # 1. Holdout 10-seed
    hold_scores = {k: [] for k in ("e2_2702", "e2_2701", "n2n", "dual_cos")}
    with torch.no_grad():
        for s in eval_seeds_10:
            torch.manual_seed(s)
            if dev.type == "cuda":
                torch.cuda.manual_seed_all(s)
            ideal, eng = og.make_batch(64, og.N, dev)
            for k, fn in (("e2_2702", c_2702), ("e2_2701", c_2701), ("n2n", n2n_fn), ("dual_cos", og.dual_cosine_blend)):
                hold_scores[k].append(float(og.residual_score_blend(ideal, eng, fn(eng)).mean().item()))

    d_hold = np.array(hold_scores["e2_2702"]) - np.array(hold_scores["n2n"])
    out["holdout_10seed"] = {
        k: {"mean": float(np.mean(v)), "std": float(np.std(v, ddof=1))} for k, v in hold_scores.items()
    }
    out["holdout_10seed"]["paired_2702_vs_n2n"] = {
        "delta_mean": float(np.mean(d_hold)),
        "ci95": bootstrap_ci(d_hold),
        "wins": int(np.sum(d_hold > 0)),
        "n": 10,
        "p_exact": exact_sign_flip_p(d_hold),
    }

    # 2. Multi-family 10-seed
    wave_specs = [(fam, wseed) for wseed in bsm.WAVEFORM_SEEDS for fam in bsm.FAMILIES]
    mf_scores = {k: [] for k in ("e2_2702", "e2_2701", "n2n", "dual_cos")}
    with torch.no_grad():
        for s in eval_seeds_10:
            per_fn = {k: [] for k in mf_scores}
            for fam, wseed in wave_specs:
                ideal, eng = bsm.make_family_batch(fam, 64, og.N, dev, seed=s + wseed)
                for k, fn in (("e2_2702", c_2702), ("e2_2701", c_2701), ("n2n", n2n_fn), ("dual_cos", og.dual_cosine_blend)):
                    per_fn[k].append(float(og.residual_score_blend(ideal, eng, fn(eng)).mean().item()))
            for k in mf_scores:
                mf_scores[k].append(float(np.mean(per_fn[k])))

    d_mf = np.array(mf_scores["e2_2702"]) - np.array(mf_scores["n2n"])
    out["multifamily_10seed"] = {
        k: {"mean": float(np.mean(v)), "std": float(np.std(v, ddof=1))} for k, v in mf_scores.items()
    }
    out["multifamily_10seed"]["paired_2702_vs_n2n"] = {
        "delta_mean": float(np.mean(d_mf)),
        "ci95": bootstrap_ci(d_mf),
        "wins": int(np.sum(d_mf > 0)),
        "n": 10,
        "p_exact": exact_sign_flip_p(d_mf),
    }

    # 3 & 4. Factory+FX & AKWF OA (domain-trained N2N vs domain-searched Ours on identical 256-cycle held-out splits)
    ds_root = PAPER_ROOT / "results" / "domain_search_table10"
    for bname, loader in (
        ("factory_fx", lambda: rw.load_reelsynth_export(rw.ART / "reelsynth_export_cycles.json", dev)),
        ("akwf_oa", lambda: rw.load_oa_wav_cycles(rw.ART / "oa_akwf", dev, n_max=1280)),
    ):
        cyc = loader()
        closed = rw.close_seam_ideal(cyc)
        ideal, eng = rw.apply_open_wrap_cliff(closed, seed=rw.PROTOCOL_SEED)
        g = torch.Generator(device="cpu").manual_seed(20260719)
        perm = torch.randperm(ideal.shape[0], generator=g).to(dev)
        n_tr = int(0.8 * ideal.shape[0])
        tr_idx, te_idx = perm[:n_tr], perm[n_tr:]

        n2n_dom = train_domain_n2n(ideal[tr_idx], dev, steps=4000)
        ours_dom, _ = load_domain_champ(ds_root / bname, dev)

        ii, ee = ideal[te_idx], eng[te_idx]
        with torch.no_grad():
            r_ours = og.residual_score_blend(ii, ee, ours_dom(ee)).cpu().numpy()
            r_n2n_dom = og.residual_score_blend(ii, ee, n2n_dom(ee)).cpu().numpy()
            r_n2n_zs = og.residual_score_blend(ii, ee, n2n_fn(ee)).cpu().numpy()
            r_e2_zs = og.residual_score_blend(ii, ee, c_2701(ee)).cpu().numpy()
            r_dc = og.residual_score_blend(ii, ee, og.dual_cosine_blend(ee)).cpu().numpy()

        d_dom = r_ours - r_n2n_dom
        w_stat = wilcoxon(d_dom)
        out[bname] = {
            "n_train": int(n_tr),
            "n_test": int(len(te_idx)),
            "ours_domain": {"mean": float(np.mean(r_ours)), "std": float(np.std(r_ours, ddof=1))},
            "n2n_domain": {"mean": float(np.mean(r_n2n_dom)), "std": float(np.std(r_n2n_dom, ddof=1))},
            "n2n_zeroshot": {"mean": float(np.mean(r_n2n_zs))},
            "e2_zeroshot": {"mean": float(np.mean(r_e2_zs))},
            "dual_cos": {"mean": float(np.mean(r_dc))},
            "paired_ours_vs_n2n_domain": {
                "delta_mean": float(np.mean(d_dom)),
                "ci95": bootstrap_ci(d_dom),
                "wins": int(np.sum(d_dom > 0)),
                "n": int(len(d_dom)),
                "p_wilcoxon": float(w_stat.pvalue),
            },
        }
        print(
            f"[{bname}] ours_dom={np.mean(r_ours):.4f} vs n2n_dom={np.mean(r_n2n_dom):.4f} "
            f"(delta={np.mean(d_dom):+.4f}, wins={int(np.sum(d_dom>0))}/{len(d_dom)}, p={w_stat.pvalue:.2e})",
            flush=True,
        )

    raw_p = {
        "holdout_10seed": out["holdout_10seed"]["paired_2702_vs_n2n"]["p_exact"],
        "multifamily_10seed": out["multifamily_10seed"]["paired_2702_vs_n2n"]["p_exact"],
        "factory_fx_256": out["factory_fx"]["paired_ours_vs_n2n_domain"]["p_wilcoxon"],
        "akwf_oa_256": out["akwf_oa"]["paired_ours_vs_n2n_domain"]["p_wilcoxon"],
    }
    out["holm_bonferroni_p"] = holm_bonferroni(raw_p)

    out_path = PAPER_ROOT / "results" / "table10_rigorous_stats.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("WROTE", out_path)
    print("Holm-Bonferroni p:", out["holm_bonferroni_p"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
