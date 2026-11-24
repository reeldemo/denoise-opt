#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1]
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from bench_meta_resume import (  # noqa: E402
    build_protocol_fingerprint,
    should_promote_champion,
    validate_resume,
)


class TestPromotion(unittest.TestCase):
    def test_provisional_below_gate(self) -> None:
        gate = 0.9748
        seq = [0.90, 0.92, 0.91, 0.93]
        champ_r = -1.0
        champ_beats = False
        for r_raw in seq:
            r = r_raw - 0.01
            if should_promote_champion(
                r_raw=r_raw,
                r=r,
                champ_r=champ_r,
                champ_beats_n2n=champ_beats,
                n2n_gate_r=gate,
            ):
                champ_r = r
                champ_beats = r_raw > gate
        self.assertAlmostEqual(champ_r, 0.92)

    def test_frozen_champ_when_beats_n2n(self) -> None:
        gate = 0.9748
        self.assertFalse(
            should_promote_champion(
                r_raw=0.90,
                r=0.89,
                champ_r=0.97,
                champ_beats_n2n=True,
                n2n_gate_r=gate,
            )
        )

    def test_promote_when_beats_and_better_j(self) -> None:
        gate = 0.9748
        self.assertTrue(
            should_promote_champion(
                r_raw=0.98,
                r=0.985,
                champ_r=0.975,
                champ_beats_n2n=True,
                n2n_gate_r=gate,
            )
        )


class TestResumeProtocol(unittest.TestCase):
    def test_gate_mismatch_aborts(self) -> None:
        fp = build_protocol_fingerprint(
            iters_target=5000,
            batch=48,
            fit_steps=24,
            pop_size=12,
            plateau_every=500,
            lambda_latency=0.05,
        )
        ckpt = {
            "iters_done": 2,
            "n2n_gate_r": None,
            "protocol_fingerprint": fp,
            "champ_raw": 0.9,
        }
        check = validate_resume(
            ckpt,
            iters=5000,
            fingerprint_now=fp,
            n2n_gate_now=0.9748,
            force_fresh=False,
        )
        self.assertFalse(check.ok)

    def test_matching_gate_resumes(self) -> None:
        fp = build_protocol_fingerprint(
            iters_target=5000,
            batch=48,
            fit_steps=24,
            pop_size=12,
            plateau_every=500,
            lambda_latency=0.05,
        )
        ckpt = {
            "iters_done": 2,
            "n2n_gate_r": 0.9748,
            "protocol_fingerprint": fp,
            "champ_raw": 0.9,
            "champ_beats_n2n": True,
        }
        check = validate_resume(
            ckpt,
            iters=5000,
            fingerprint_now=fp,
            n2n_gate_now=0.9748,
            force_fresh=False,
        )
        self.assertTrue(check.ok)
        self.assertEqual(check.resumed_from_iter, 2)


if __name__ == "__main__":
    unittest.main()