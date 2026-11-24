"""Resume / promotion helpers for bench_meta_approaches_5k (Bug 2)."""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def beats_n2n_gate(r_raw: float, n2n_gate_r: float | None) -> bool:
    return n2n_gate_r is None or r_raw > float(n2n_gate_r)


def should_promote_champion(
    *,
    r_raw: float,
    r: float,
    champ_r: float,
    champ_beats_n2n: bool,
    n2n_gate_r: float | None,
) -> bool:
    beats = beats_n2n_gate(r_raw, n2n_gate_r)
    if beats and (not champ_beats_n2n or r > champ_r):
        return True
    if (not champ_beats_n2n) and (not beats) and r > champ_r:
        return True
    return False


def build_protocol_fingerprint(
    *,
    iters_target: int,
    batch: int,
    fit_steps: int,
    pop_size: int,
    plateau_every: int,
    lambda_latency: float,
    hp_reward_sweep: bool = True,
) -> dict[str, Any]:
    return {
        "iters_target": int(iters_target),
        "batch": int(batch),
        "fit_steps_default": int(fit_steps),
        "pop_size": int(pop_size),
        "plateau_every": int(plateau_every),
        "lambda_latency": float(lambda_latency),
        "hp_reward_sweep": bool(hp_reward_sweep),
    }


def _gate_equal(a: float | None, b: float | None) -> bool:
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=1e-9)


def fingerprints_match(a: dict[str, Any] | None, b: dict[str, Any] | None) -> bool:
    if not a and not b:
        return True
    if not a or not b:
        return False
    keys = (
        "iters_target",
        "batch",
        "fit_steps_default",
        "pop_size",
        "plateau_every",
        "lambda_latency",
        "hp_reward_sweep",
    )
    for k in keys:
        if k not in a or k not in b:
            return False
        if a[k] != b[k]:
            return False
    return True


@dataclass(frozen=True)
class ResumeCheck:
    ok: bool
    gate_ok: bool
    fingerprint_ok: bool
    gate_ckpt: float | None
    gate_now: float | None
    message: str
    resumed_from_iter: int | None = None


def validate_resume(
    ckpt: dict[str, Any],
    *,
    iters: int,
    fingerprint_now: dict[str, Any],
    n2n_gate_now: float | None,
    force_fresh: bool,
) -> ResumeCheck:
    if force_fresh or not ckpt:
        return ResumeCheck(
            ok=True,
            gate_ok=True,
            fingerprint_ok=True,
            gate_ckpt=None,
            gate_now=n2n_gate_now,
            message="fresh_start",
        )
    gate_ckpt = ckpt.get("n2n_gate_r")
    if gate_ckpt is not None:
        try:
            gate_ckpt = float(gate_ckpt)
        except (TypeError, ValueError):
            gate_ckpt = None
    fp_ckpt = ckpt.get("protocol_fingerprint") or build_protocol_fingerprint(
        iters_target=int(ckpt.get("iters_target") or ckpt.get("iters_done") or 0),
        batch=int(fingerprint_now["batch"]),
        fit_steps=int(fingerprint_now["fit_steps_default"]),
        pop_size=int(fingerprint_now["pop_size"]),
        plateau_every=int(fingerprint_now["plateau_every"]),
        lambda_latency=float(fingerprint_now["lambda_latency"]),
        hp_reward_sweep=bool(fingerprint_now.get("hp_reward_sweep", True)),
    )
    gate_ok = _gate_equal(gate_ckpt, n2n_gate_now)
    fingerprint_ok = fingerprints_match(fp_ckpt, fingerprint_now)
    resumed = int(ckpt.get("iters_done") or 0)
    if gate_ok and fingerprint_ok:
        msg = f"RESUME_CHECK gate_ckpt={gate_ckpt} gate_now={n2n_gate_now} fingerprint_ok=True"
        return ResumeCheck(
            ok=True,
            gate_ok=True,
            fingerprint_ok=True,
            gate_ckpt=gate_ckpt,
            gate_now=n2n_gate_now,
            message=msg,
            resumed_from_iter=resumed if resumed > 0 else None,
        )
    msg = (
        f"RESUME protocol mismatch: gate_ok={gate_ok} fingerprint_ok={fingerprint_ok} "
        f"gate_ckpt={gate_ckpt} gate_now={n2n_gate_now}. "
        "Pass --force-fresh to restart."
    )
    return ResumeCheck(
        ok=False,
        gate_ok=gate_ok,
        fingerprint_ok=fingerprint_ok,
        gate_ckpt=gate_ckpt,
        gate_now=n2n_gate_now,
        message=msg,
        resumed_from_iter=resumed if resumed > 0 else None,
    )


def recompute_champ_beats_n2n(champ_raw: float, n2n_gate_r: float | None) -> bool:
    return beats_n2n_gate(champ_raw, n2n_gate_r)


def load_checkpoint(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def is_dry_run_checkpoint(ckpt: dict[str, Any], requested_iters: int) -> bool:
    if ckpt.get("dry_run"):
        return True
    done = int(ckpt.get("iters_done") or 0)
    target = ckpt.get("iters_target")
    if target is not None and int(target) < requested_iters and done <= 5:
        return True
    if done <= 5 and requested_iters > 10:
        status_dry = ckpt.get("run_phase") == "dry"
        if status_dry:
            return True
    return False