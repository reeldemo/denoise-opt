# Reproduce the paper results

## 1. Tests

<!-- ci:run -->
```bash
RESEARCH_BACKUP_OPTIONAL=1 bash scripts/tests/run_all_tests.sh
```

Expected last line: `All scripts/tests passed`. This checks the launcher scripts and the N2N compatibility shim. It does not check paper numbers.

## 2. Paired statistics from stored results

Both scripts read `figures/multiseed_summary.json` and rewrite their output with identical content, so `git diff` shows no change.

<!-- ci:run -->
```bash
python scripts/stats_paired_holdout.py
python scripts/stats_meta_approach_5k.py
git diff --exit-code figures/stats_paired_holdout.json figures/stats_meta_approach_5k.json
```

The expected output lines are listed in the README. In summary:

| Comparison (R_blend, hybrid minus other) | Difference | Bootstrap 95% interval | Wins |
| --- | --- | --- | --- |
| Five-seed holdout, vs Noise2Noise | -0.0059 | [-0.0068, -0.0053] | 0/5 |
| Five-seed holdout, vs DualCosine | +0.4288 | [0.4023, 0.4621] | 5/5 |
| 20 multifamily boards, vs Noise2Noise | +0.0069 | [-0.0039, 0.0186] | 13/20 |
| Matched 5k bake-off, vs aging evolution | +0.0114 | [0.0064, 0.0144] | 3/3 |

Exact sign-flip p values are bounded below by 0.0625 for n = 5 and 0.25 for n = 3. The tests are exploratory.

## 3. Build the PDF

<!-- ci:run -->
```bash
latexmk -outdir=build main.tex
test -f build/Unsupervised_Wrap-Discontinuity_Repair_in_Wavetable_Synthesis_via_Hybrid_GA-PPO_Meta-Search_v14.pdf
```

## 4. Full runs

The searches and holdout evaluations that produce `multiseed_summary.json` and the other result files need a GPU and the ReelSynth repository. `REPRO.md` lists the launchers for the bake-off, the v14 FitCell run, the signal-heal transfer table and the hear pack, and the search and holdout seeds. Launchers read `REELSYNTH_ROOT`, which has no default:

```bash
export REELSYNTH_ROOT=/path/to/reelsynth
```

CI does not run the full runs.

## What each level checks

| Level | Checks |
| --- | --- |
| Tests | The launcher scripts. No numbers. |
| Paired statistics | The paired statistics in the table above from stored per-seed values. |
| PDF build | That the manuscript compiles. |
| Full run | The searches and holdout scores themselves. |
