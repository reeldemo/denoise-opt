# Repository layout

| Path | Contents |
| --- | --- |
| `main.tex`, `subsections/` | Manuscript source. `main.tex` includes one file per section from `subsections/`. |
| `arxiv-twocolumn.sty`, `.latexmkrc`, `build.ps1` | Class file and build configuration. `.latexmkrc` sets the PDF name. |
| `Unsupervised_Wrap-Discontinuity_..._v14.pdf` | The built v14 manuscript. |
| `figures/` | Figure files (`fig_*.png`, `fig_*.pdf`) and the result JSON files behind the tables, for example `multiseed_summary.json`, `meta_approach_compare.json`, `stats_paired_holdout.json`. |
| `results/` | Experiment outputs: Table 10 domain search, FX suite, loss decomposition, N2N baseline reruns, queue status. |
| `scripts/` | Experiment drivers and statistics. `stats_*.py` run on CPU. `engine/` holds the holdout and search helpers that need ReelSynth. `compat/` holds the N2N checkpoint shim. `tests/` holds the launcher tests. |
| `legacy_meta/` | Frozen artifacts from earlier versions (v7). |
| `docs/` | This documentation site. `docs/audits/` holds an internal audit note. |
| `REPRO.md` | Full reproduction commands for every table, including the GPU runs. |
| `EVAL_PROTOCOL.md`, `LISTENING_PROTOCOL_MAIN.md`, `EXPERIMENT_PLAN.md`, `EXPERIMENTS_NEXT.md` | Evaluation and experiment planning notes. |
| `NOMENCLATURE.md` | Names used in the manuscript and the matching code keys. |
| `PAPER_SHIP_STATUS.md`, `REVIEW_RESPONSE_v2.1.md` | Status and review-response notes. |
| `SAMPLE_LICENSES.md` | Licences of third-party audio samples. |

The three files in `figures/` named `REPRO_meta_compare.md`, `LISTENING_PROTOCOL_MAIN.md` and `PENDING_RBLEND.md` are notes that sit next to the data they describe.
