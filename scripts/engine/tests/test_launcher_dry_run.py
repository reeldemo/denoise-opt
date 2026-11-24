#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1]
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from common import guard_real_meta_run, meta_seed_dir  # noqa: E402


class TestDryRunDirs(unittest.TestCase):
    def test_meta_seed_dir_splits_dry(self) -> None:
        root = Path("/tmp/out")
        self.assertEqual(meta_seed_dir(root, 1902771841, True), root / "1902771841-dry")
        self.assertEqual(meta_seed_dir(root, 1902771841, False), root / "1902771841")

    def test_real_run_refuses_legacy_dry_ckpt(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            seed_dir = Path(td) / "1902771841" / "hybrid_lstm"
            seed_dir.mkdir(parents=True)
            ckpt = {
                "iters_done": 2,
                "iters_target": 3,
                "dry_run": True,
                "champ_raw": 0.5,
            }
            (seed_dir / "checkpoint.json").write_text(json.dumps(ckpt), encoding="utf-8")
            with self.assertRaises(SystemExit):
                guard_real_meta_run(Path(td) / "1902771841", 5000)
            guard_real_meta_run(Path(td) / "1902771841", 5000, resume_from_dry=True)

    def test_dry_dir_does_not_block_guard(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            dry = meta_seed_dir(Path(td), 1, True)
            app = dry / "hybrid_lstm"
            app.mkdir(parents=True)
            (app / "checkpoint.json").write_text(
                json.dumps({"iters_done": 2, "dry_run": True}), encoding="utf-8"
            )
            guard_real_meta_run(Path(td) / "1", 5000)


if __name__ == "__main__":
    unittest.main()