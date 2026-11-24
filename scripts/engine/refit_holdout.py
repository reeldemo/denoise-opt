#!/usr/bin/env python3
"""Refit a frozen champion on holdout seeds (modes: as_is, plateau, n2n_matched)."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any, Callable

import torch
import torch.nn as nn

from common import EXTENDED_HOLDOUT_SEEDS, bootstrap_reelsynth, save_json, utc_now
from holdout_eval import load_hybrid_champ, score_seed


REFIT_VAL_SEED = 777_001


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def plateau_refit(
    cell,
    ops: list[str],
    *,
    device: torch.device,
    lr: float,
    batch: int,
    max_steps: int = 2048,
    check_every: int = 32,
    rel_eps: float = 1e-3,
    patience: int = 5,
    val_seed: int = REFIT_VAL_SEED,
) -> tuple[dict[str, torch.Tensor], int, str]:
    import gpu_rl_arch as og  # noqa: E402

    opt = torch.optim.Adam(cell.parameters(), lr=lr)
    flat_bad = 0
    steps_used = 0
    stop_reason = "max_steps"

    def val_score() -> float:
        torch.manual_seed(val_seed)
        if device.type == "cuda":
            torch.cuda.manual_seed_all(val_seed)
        ideal, eng = og.make_batch(batch, og.N, device)
        with torch.no_grad():
            out = og.apply_ops(eng, cell, ops)
            return float(og.residual_score_blend(ideal, eng, out).mean().item())

    prev_val: float | None = None
    for step in range(1, max_steps + 1):
        ideal, eng = og.make_batch(batch, og.N, device)
        out = og.apply_ops(eng, cell, ops)
        r = og.residual_score_blend(ideal, eng, out).mean()
        loss = 1.0 - r
        if loss.requires_grad:
            opt.zero_grad(set_to_none=True)
            loss.backward()
            nn.utils.clip_grad_norm_(cell.parameters(), 1.0)
            opt.step()
        steps_used = step
        if step % check_every == 0:
            v = val_score()
            if prev_val is not None:
                rel = abs(prev_val - v) / max(abs(prev_val), 1e-9)
                if rel < rel_eps:
                    flat_bad += 1
                    if flat_bad >= patience:
                        stop_reason = "plateau"
                        break
                else:
                    flat_bad = 0
            prev_val = v
    return cell.state_dict(), steps_used, stop_reason


def fixed_steps_refit(
    cell,
    ops: list[str],
    *,
    device: torch.device,
    lr: float,
    batch: int,
    steps: int,
) -> tuple[dict[str, torch.Tensor], int, str]:
    import gpu_rl_arch as og  # noqa: E402

    opt = torch.optim.Adam(cell.parameters(), lr=lr)
    for step in range(1, steps + 1):
        ideal, eng = og.make_batch(batch, og.N, device)
        out = og.apply_ops(eng, cell, ops)
        r = og.residual_score_blend(ideal, eng, out).mean()
        loss = 1.0 - r
        if loss.requires_grad:
            opt.zero_grad(set_to_none=True)
            loss.backward()
            nn.utils.clip_grad_norm_(cell.parameters(), 1.0)
            opt.step()
    return cell.state_dict(), steps, "fixed_steps"


def load_champion_blob(champ: Path, device: torch.device):
    bootstrap_reelsynth()
    import gpu_rl_arch as og  # noqa: E402

    blob = torch.load(champ, map_location=device, weights_only=False)
    if "cell_state_dict" in blob and "architecture" in blob:
        cfg = og.ArchConfig.from_dict(blob["architecture"])
        hp_raw = blob.get("hyperparams") or {}
        cell = og.SeamCell(cfg).to(device)
        cell.load_state_dict(blob["cell_state_dict"], strict=False)
        cell.eval()
        lr = float(hp_raw.get("lr", 3e-3))
        return cfg, cell, lr, blob
    raise ValueError(f"Unrecognized champion blob keys in {champ}")


def eval_methods_on_holdout(
    *,
    hybrid_fn: Callable[[torch.Tensor], torch.Tensor],
    eval_seeds: tuple[int, ...],
    batch: int,
    device: torch.device,
) -> dict[str, Any]:
    from holdout_eval import load_n2n

    root = bootstrap_reelsynth()
    import gpu_rl_arch as og  # noqa: E402

    methods: dict[str, Callable[[torch.Tensor], torch.Tensor]] = {
        "hybrid": hybrid_fn,
        "n2n": load_n2n(root, device)[0],
        "dual_cosine": og.dual_cosine_blend,
        "no_bake": lambda x: x,
    }
    per_seed: dict[str, dict[str, float]] = {}
    for seed in eval_seeds:
        per_seed[str(seed)] = score_seed(seed, device=device, batch=batch, methods=methods)

    summary: dict[str, Any] = {}
    for name in methods:
        vals = [per_seed[str(s)][name] for s in eval_seeds]
        mean = sum(vals) / len(vals)
        std = (sum((v - mean) ** 2 for v in vals) / max(len(vals) - 1, 1)) ** 0.5
        summary[name] = {"mean": mean, "std": std, "values": vals}
    return {"per_seed": per_seed, "summary": summary}


def run_refit(
    *,
    champ: Path,
    mode: str,
    init: str,
    eval_seeds: tuple[int, ...],
    batch: int,
    refit_seed: int,
    device: str,
    dry_run: bool,
) -> dict[str, Any]:
    if dry_run:
        eval_seeds = (eval_seeds[0],)
        batch = min(batch, 8)
    dev = torch.device(device if device != "cuda" or torch.cuda.is_available() else "cpu")
    cfg, cell, lr, _blob = load_champion_blob(champ, dev)
    import gpu_rl_arch as og  # noqa: E402

    ops = list(cfg.ops)
    steps_used = 0
    stop_reason = "as_is"
    torch.manual_seed(refit_seed)
    if dev.type == "cuda":
        torch.cuda.manual_seed_all(refit_seed)

    if mode == "plateau":
        max_s = 64 if dry_run else 2048
        state, steps_used, stop_reason = plateau_refit(
            cell, ops, device=dev, lr=lr, batch=batch, max_steps=max_s
        )
        cell.load_state_dict(state)
    elif mode == "n2n_matched":
        n_steps = 32 if dry_run else 20_000
        state, steps_used, stop_reason = fixed_steps_refit(
            cell, ops, device=dev, lr=lr, batch=batch, steps=n_steps
        )
        cell.load_state_dict(state)
    elif mode != "as_is":
        raise ValueError(f"Unknown mode {mode!r}")

    cell.eval()

    def hybrid_fn(eng: torch.Tensor) -> torch.Tensor:
        return og.apply_ops(eng, cell, ops)

    t0 = time.time()
    scored = eval_methods_on_holdout(
        hybrid_fn=hybrid_fn, eval_seeds=eval_seeds, batch=batch, device=dev
    )
    return {
        "schema": "denoiseopt.refit_holdout.v1",
        "created_at": utc_now(),
        "mode": mode,
        "init": init,
        "champ_sha256": sha256_file(champ),
        "champ_path": str(champ),
        "device": str(dev),
        "batch": batch,
        "refit_seed": refit_seed,
        "eval_seeds": list(eval_seeds),
        "steps_used": steps_used,
        "stop_reason": stop_reason,
        "dry_run": dry_run,
        "wall_s": time.time() - t0,
        **scored,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--champ", type=Path, required=True)
    ap.add_argument("--mode", choices=("as_is", "plateau", "n2n_matched"), default="as_is")
    ap.add_argument("--init", choices=("fresh", "search"), default="fresh")
    ap.add_argument(
        "--holdout-seeds",
        default=",".join(map(str, EXTENDED_HOLDOUT_SEEDS)),
    )
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--refit-seed", type=int, default=424_242)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    seeds = tuple(int(s.strip()) for s in args.holdout_seeds.split(",") if s.strip())
    try:
        payload = run_refit(
            champ=args.champ,
            mode=args.mode,
            init=args.init,
            eval_seeds=seeds,
            batch=args.batch,
            refit_seed=args.refit_seed,
            device=args.device,
            dry_run=args.dry_run,
        )
    except Exception as exc:
        print(f"refit_holdout failed: {exc}", file=sys.stderr)
        return 1
    save_json(args.out, payload)
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())