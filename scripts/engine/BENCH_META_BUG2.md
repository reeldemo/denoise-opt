# bench_meta Bug 2 (N2N gate on resume)

Primary fix: **reeldemo/reelsynth** `scripts/bench_meta_approaches_5k.py` (see paired PR).

This repo ships `bench_meta_resume.py` with the same promotion and resume-validation rules for unit tests and launcher guards. Launchers still invoke the reelsynth script via `REELSYNTH_ROOT`.