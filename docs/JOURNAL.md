# Research journal (sanitized snapshot)

This is a sanitized research-journal snapshot dated **2026-11-27 07:46 Europe/Berlin**. It records scientific status, publication status and named git heads for DenoiseOpt / Seam (code and manuscript). The same note is intended for both [reeldemo/denoise-opt](https://github.com/reeldemo/denoise-opt) and [reeldemo/denoiseopt-paper](https://github.com/reeldemo/denoiseopt-paper). Operational hostnames, machine paths and process identifiers are omitted on purpose. This file is not permission to merge a pull request or to submit or upload a paper.

Canonical operational handover notes live outside these repositories.

## Goal

DenoiseOpt / Seam paper: *Seam-Local Repair of Wavetable Wrap Discontinuities with a Self-Supervised Blended Residual* (paper-db id `denoiseopt`). Raise the work to paper-review and klaut.pro ≥8.5 with findings fixed, then show Julian M. Kleber the Zenodo draft (metadata + PDF) before any Zenodo publish (permanent DOI, under his name and ORCID 0000-0001-5518-0932). TMLR rejected the paper (Julian, 2026-11-24). Code licence MIT; preprint text CC BY 4.0. Experiment scripts used for the engine runs live in `reeldemo/reelsynth`.

aiXiv id: **aixiv.260719.000003** (v2.1 submitted 2026-11-02 via web UI by Julian; further submits hold until his Go).

## Publication status

- **Stage:** drafting / evidence refresh. Path is Zenodo after paper-review and klaut.pro ≥8.5 with findings fixed, draft shown to Julian first.
- **paper-review:** **6.9 / 10**, 0 blockers, 2026-11-24, PR #7 (base `main` `e56fd7d`) — below 8.5. A deterministic klaut row exists (2026-11-24); the Azure klaut panel was blocked (403); Julian forbade further Azure spend.
- **Preprint / aiXiv:** **aixiv.260719.000003** (v2.1 submitted 2026-11-02; v1.0 / v2.1 / v3.2 appear in the 2026-11-24 paper-db export). No Zenodo DOI.
- **Venue target:** diamond open access, no APC, Scopus/WoS or similar (Julian, 2026-11-24 17:29 Europe/Berlin).
- **Open PRs (2026-11-27):** [denoise-opt #7](https://github.com/reeldemo/denoise-opt/pull/7) `6a1c1a037852795bce61c0bffd9a63321e554457` (Zenodo review pass 1 — draft, do not merge); also drafts #3 and #2 (superseded). [denoiseopt-paper](https://github.com/reeldemo/denoiseopt-paper) drafts #3, #2 and #1 (all in blocked merge state). Default `denoise-opt` `main` is `f9f33f091a352fab0954f98e34c47bf31c69f754`; `denoiseopt-paper` `master` is `264d936cc3644910328ff1e3d9a9ec174ad4a2b5`.
- **Ready to submit / Zenodo upload?** No. Review 6.9 < 8.5; holdout for the new full-set seed is missing; invalid earlier champions must be replaced honestly; Julian's yes is required on a named head.

## Current step

**Live 2026-11-27 07:43 Europe/Berlin.** Full-set seed **d_e3_2026072704** is **finished**. Status `phase=all_complete`, 6/6 approaches, updated 2026-11-26 21:57:55 Europe/Berlin. All six approaches completed at 5000 iterations (champ_r):

| approach | champ_r | wall_h |
|---|---|---|
| random | 0.9375548660755157 | 2.31 |
| cmaes | 0.9579188525676727 | 0.79 |
| reinforce | 0.9509831070899963 | 2.63 |
| aging_evo | 0.9481123983860016 | 5.68 |
| tpe | 0.9457070231437683 | 5.03 |
| hybrid_lstm | **0.9742968380451202** | 5.16 |

Baseline dual-cosine 0.5144028663635254. The compare artefact is marked `publishable: true`. **No holdout file** is present for this seed; the queue moved on to variants anyway.

Variants (projection cap still 1000 GPU-h): V1 seed 2026072701 done 1.832 GPU-h (2026-11-26 23:48:33); V1 seed 2026072702 done 1.507 GPU-h (2026-11-27 01:22:44); V2 seed 2026072701 done 3.858 GPU-h (2026-11-27 05:14:51); **V2 seed 2026072702 running** since 05:15:11 (projection before start 73.668 GPU-h; 5000 iters, branches ppo/nas/pbt/ga/combo, cell kind `n2n_unet`, max 200 h). Do not kill that job.

## Decision log

- **2026-11-27 07:39–07:40 Europe/Berlin — Julian via Grok Bot:** keep this journal in the four-paper set (with Publication status) and open a sanitized journal PR on `reeldemo/denoise-opt` and on `reeldemo/denoiseopt-paper`. Do not merge until his yes.
- **2026-11-25 07:36 Europe/Berlin — Julian:** all yes on the DenoiseOpt questions then posed (20k refit + real-seam eval; queue adoption).
- **2026-11-24 — Julian:** TMLR rejection; Zenodo path after ≥8.5; show drafts first. Also approved the full re-run set after a dry-run/resume bug froze 3 of 14 E3/E4 champions (those numbers are invalid). The N2N baseline was trained for 20k steps, not the 4k the paper states.
- **2026-11-02 — Julian:** submitted Seam aixiv.260719.000003 → v2.1 via the web UI. Further submits hold until his Go.

## Blockers

- paper-review 6.9 < 8.5; withdrawn/invalid champion numbers must be replaced by this full-set run, with honest holdout if the manuscript needs it.
- Local klaut panel not yet trusted as a substitute for the blocked Azure panel.
- Listening-test plan PR #3 still draft (N_listeners = 0 remains the honest statement until a study is run).
- Zenodo publish and any merge need Julian's yes. Further aiXiv submits need his Go.

## Next steps

1. Let V2 seed 2026072702 finish; do not kill the running job. After the queue is idle, decide whether to run the missing holdout for `d_e3_2026072704` before rebuilding paper numbers.
2. Rebuild paper numbers from the new result files in draft denoise-opt PR #7 once the measurements the manuscript needs are in; re-review to ≥8.5; show Julian a Zenodo draft before any upload.

## Last updated

2026-11-27 07:46 Europe/Berlin.
