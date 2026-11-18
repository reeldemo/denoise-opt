# DenoiseOpt

Manuscript sources, figure data and statistics scripts for *Unsupervised Wrap-Discontinuity Repair in Wavetable Synthesis via Hybrid GA-PPO Meta-Search* (version v14), by Julian M. Kleber.

[![CI](https://github.com/reeldemo/denoise-opt/actions/workflows/ci.yml/badge.svg)](https://github.com/reeldemo/denoise-opt/actions/workflows/ci.yml)

## What this is

A looped wavetable period has a discontinuity where its end meets its start. The manuscript searches for a small repair operator at that seam without paired training data, using a hybrid genetic-algorithm and PPO meta-search, and scores every method with one locked metric, R_blend. No listening study was run (N_listeners = 0). The evidence is objective and the manuscript says so.

This repository holds the LaTeX sources, the figure and result JSON files behind the tables, the statistics scripts that can be rerun on CPU, and the experiment drivers. The engine that produced the raw searches is the separate ReelSynth repository (`reeldemo/reelsynth`) and is not needed for the steps below.

Sole author: Julian M. Kleber. The tools that assisted the work are described in the Tooling section of the PDF. Ship status and the aiXiv listing notes are in [PAPER_SHIP_STATUS.md](PAPER_SHIP_STATUS.md).

The built PDF is in the repository root. A map of the repository is in [docs/layout.md](docs/layout.md), and the documentation site is built with MkDocs Material from `docs/` and `mkdocs.yml`.

## Quickstart

Python 3 with no third-party packages (CI uses 3.12). This runs the unit and shell tests of the experiment launchers.

<!-- ci:run -->
```bash
python3 -m venv .venv
. .venv/bin/activate
RESEARCH_BACKUP_OPTIONAL=1 bash scripts/tests/run_all_tests.sh
```

Expected last line: `All scripts/tests passed`.

## Reproducing the paper numbers

Two statistics tables are recomputed from `figures/multiseed_summary.json`. Both scripts are deterministic and rewrite their output file with identical content.

<!-- ci:run -->
```bash
python scripts/stats_paired_holdout.py
python scripts/stats_meta_approach_5k.py
git diff --exit-code figures/stats_paired_holdout.json figures/stats_meta_approach_5k.json
```

Expected output of the first script (R_blend difference of the hybrid method minus the comparison, bootstrap 95% interval, exact sign-flip p value, wins over seeds or boards):

```text
hybrid_vs_n2n_holdout_5seed d=-0.0059 CI95boot=[-0.0068, -0.0053] p=0.0625 gz=-4.75 wins=0/5
hybrid_vs_dualcosine_holdout_5seed d=+0.4288 CI95boot=[0.4023, 0.4621] p=0.0625 gz=9.26 wins=5/5
hybrid_minus_n2n_multifamily_20boards d=+0.0069 CI95boot=[-0.0039, 0.0186] p=0.2685 gz=0.25 wins=13/20
```

Expected output of the second script (matched 5k-iteration bake-off, three search seeds):

```text
hybrid_vs_aging_evo d=+0.0114 CIboot=[0.0064, 0.0144] p=0.25 wins=3/3
hybrid_vs_cmaes d=+0.0184 CIboot=[0.0166, 0.0211] p=0.25 wins=3/3
hybrid_vs_random d=+0.0381 CIboot=[0.0363, 0.0403] p=0.25 wins=3/3
hybrid_vs_reinforce d=+0.0149 CIboot=[-0.0003, 0.023] p=0.5 wins=2/3
hybrid_vs_tpe d=+0.0297 CIboot=[0.0267, 0.0319] p=0.25 wins=3/3
hybrid_vs_runner_up_aging_evo d=+0.0114 CIboot=[0.0064, 0.0144] p=0.25 wins=3/3
```

With n = 5 the smallest attainable exact p value is 0.0625, and with n = 3 it is 0.25. The scripts and the `note` field of the output JSON say these tests are exploratory. In the five-seed holdout the Noise2Noise baseline scores slightly higher than the hybrid champion (difference -0.0059).

The PDF is rebuilt with LaTeX. `latexmk` reads `.latexmkrc`, which sets the output name to the titled v14 PDF.

<!-- ci:run -->
```bash
latexmk -outdir=build main.tex
test -f build/Unsupervised_Wrap-Discontinuity_Repair_in_Wavetable_Synthesis_via_Hybrid_GA-PPO_Meta-Search_v14.pdf
```

On Windows, `.\build.ps1` builds the same PDF with two `pdflatex` passes.

### Smoke run and full run

| Level | What it checks | Needs |
| --- | --- | --- |
| Quickstart tests | Launcher scripts and the N2N checkpoint compatibility shim. No paper numbers. | Python, bash |
| Statistics scripts | The paired statistics in the table above, recomputed from stored per-seed values. | Python |
| PDF build | That the manuscript compiles. | TeX Live |
| Full run | The searches and holdout evaluations that produce `multiseed_summary.json` and the other result files: bake-off, FitCell to convergence, holdout, transfer. Commands are in [REPRO.md](REPRO.md). | GPU, the ReelSynth repository, many hours |

CI runs the first three levels. The full run is not run in CI.

## Related repositories

| Repository | Role |
| --- | --- |
| [reeldemo/denoise-opt](https://github.com/reeldemo/denoise-opt) | This repository: manuscript and result files |
| [reeldemo/denoise-opt-meta](https://github.com/reeldemo/denoise-opt-meta) | Meta-search and paper pipeline artifacts |
| [reeldemo/reelsynth](https://github.com/reeldemo/reelsynth) | ReelSynth engine and the DenoiseOpt search runners |

## Citation

Cite with the metadata in [CITATION.cff](CITATION.cff). Author: Julian M. Kleber, ORCID [0000-0001-5518-0932](https://orcid.org/0000-0001-5518-0932). Contact: julian.m.kleber@gmail.com. The preprint is on aiXiv as [aixiv.260719.000003](https://aixiv.science/abs/aixiv.260719.000003).

## Licence

The manuscript text, figures and LaTeX sources are licensed under CC BY 4.0, see [LICENSE](LICENSE). The scripts have no licence yet, so no code licence is granted. Third-party audio samples keep their own licences, see [SAMPLE_LICENSES.md](SAMPLE_LICENSES.md).
