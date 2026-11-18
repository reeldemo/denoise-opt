# Crowdsourced listening test for DenoiseOpt: plan

Prepared 2026-11-18 (Europe/Berlin) for Julian M. Kleber. **Status: plan, code and templates only. No requester account was created, no money was funded, no HIT/study was launched, and no listener data exists.** Every number marked "assumed" is a placeholder until a pilot replaces it.

## 1. TL;DR

* **Amazon Mechanical Turk is not available.** MTurk closed to requesters on 2026-09-30 (https://www.mturk.com/help ; press: https://www.cnbc.com/2026/08/25/amazon-service-that-jeff-bezos-called-artificial-ai-is-shutting-down.html). The same answer applies to "can we find listeners on Mechanical Turk": no. **Prolific** is the recommended replacement and is what everything here targets.
* Design: ITU-T P.808-style crowdsourced **DCR** (degradation category rating with a hidden clean reference) on 5 systems, plus a short forced-choice **A/B** block (Ours vs SeamN2N). Two stages on Prolific: a 4-minute headphone screener, then a ~17-minute main study.
* Recommended size: **60 analysable listeners** (about 71 recruited, 102 screened), 8 tiles each from a pool of 24 (48 if the audio exports are cheap). Planning cost **GBP 478.86 (about EUR 575)** with the corporate fee, GBP 506.15 with an assumed 19% VAT on the fee. A **pilot of 10 analysable listeners costs about GBP 82 (EUR 98)** and should come first.
* Honest power statement: with assumed variance components, 60 listeners x 24 tiles detect a 0.5-point DCR difference with power 0.97 but a 0.3-point difference only with power 0.64 (0.38 if the pessimistic variances are right). The forced-choice block is the more sensitive test for Ours vs SeamN2N (power 0.92 at 60% preference for Ours, assumed ICC 0.1).
* This does not change what the paper may claim until data exist. Today the paper states `N_listeners = 0`, and that stays true.

## 2. Mechanical Turk versus Prolific

| | Amazon MTurk | Prolific |
|---|---|---|
| Availability (2026-11-18) | closed to requesters since 2026-09-30; unused balances refunded by 2026-11-30 (https://www.mturk.com/help) | open |
| Fee (historical / current) | 20% commission, +20% for HITs with 10+ assignments (40% for this study), +5% Masters (https://requester.mturk.com/pricing, historical) | 42.857% of reward (corporate) or 33.33% (academic, needs an institutional e-mail and the academic account type); VAT charged on the fee only (https://researcher-help.prolific.com/en/articles/445239-what-is-your-pricing) |
| Minimum pay | none | GBP 6.00/h minimum, GBP 9.00/h recommended (same page family) |
| P.808 tooling | Microsoft P.808 toolkit targets MTurk and also supports Prolific (https://github.com/microsoft/P.808) | same toolkit; this repo uses a static page instead |
| Participant quality | known bot/low-effort issues, needs heavy screening | pseudonymous IDs, pre-screening, attention-check policy; headphone use cannot be enforced by a Prolific filter, so we screen in the page |
| GDPR | worker IDs are personal data | Prolific ID is pseudonymous personal data; privacy notice required (`consent/consent_and_privacy_en.md`) |

## 3. Systems, stimuli, conditions

Read from the paper (`subsections/experiments_eval_listening.tex`, `LISTENING_PROTOCOL_MAIN.md`) and `reelsynth` hear-pack notes.

| ID | System | Role |
|---|---|---|
| IDEAL | clean sibling cycle (no seam) | reference; also hidden reference in the test list |
| OURS | seam-local blended residual (the paper's method) | focus |
| N2N | SeamN2N baseline | confirmatory contrast and A/B partner |
| DUALCOSINE | classical dual cosine blend | confirmatory contrast |
| NOBAKE | unrepaired wrap | confirmatory contrast (expected worst) |
| CRIPPLED | deliberately degraded clip | gold item, never analysed as a system |

* Clips: 3.0 s, A4 (440 Hz), 5 Hz vibrato at 3% depth, 44.1 kHz mono PCM16 (as the released hear samples), equal integrated loudness, fixed level.
* **Audio availability:** `hear_vibrato_methods` already has no-bake, DualCosine and ours_hybrid (and several search arms) for 5 tiles (46, 21, 4, 49, 48). **IDEAL siblings, SeamN2N clips and a pool of 24 (or 48) tiles still have to be exported.** The 5 existing tiles can serve as training clips.
* Tile pool: 24 tiles stratified over the objective R_blend range (include top-quartile "wrap cliff" tiles as in `limitations.tex`). This is a design decision (section 12).
* Difference from the paper's earlier protocol sketch (MUSHRA/ABX, n>=24 listeners, 12 tiles, 48 kHz): DCR is used because P.808 standardises ACR/DCR/CCR for crowdsourcing and the reference-based DCR scale directly asks about click audibility; 44.1 kHz matches the released clips. MUSHRA remains possible on a later, in-lab or crowd extension (crowdsourced MUSHRA was reported to correlate with lab results, r about 0.78 to 0.96, by Cartwright et al., ICASSP 2016; that figure is from my literature notes and should be re-checked before it is quoted in the paper).

## 4. Task structure (per listener, main study)

1. Consent, volume setting (no loudspeakers).
2. 5 practice trials spanning the scale (feedback-free).
3. 45 DCR trials = 8 tiles x 5 systems (IDEAL shown as the hidden reference, expected 5) + 2 gold (CRIPPLED, expected 1) + 3 trapping clips (expected values stored in the session file). Order randomised; same tile not back to back where possible.
4. 8 A/B trials (Ours vs SeamN2N, same tile, left/right counterbalanced) with a "no audible difference" option.
5. Four setup questions + optional comment.

DCR scale (ITU-T P.800 DCR labels): 5 degradation inaudible, 4 audible but not annoying, 3 slightly annoying, 2 annoying, 1 very annoying. Time per item (assumed, to be replaced by pilot medians): DCR 12 s, A/B 14 s, practice 12 s, 120 s for consent/instructions, 20% slack, total 16.6 min.

Session files: `scripts/session_builder.py` (balanced tile rotation, fixed seed, manifest check). The page is `hit/index.html` + `hit/hit.js`: no external libraries, no cookies, no analytics, WebAudio headphone test, answers kept in memory and POSTed once at the end to a placeholder endpoint (`CONFIG.resultEndpoint`) or offered as a JSON download.

## 5. Quality control (frozen before launch)

* **Screener (stage 1, ~4 min, GBP 0.85):** headphone check of Woods et al. (2017): 6 trials, 200 Hz tones, one tone 6 dB quieter, one tone in antiphase, answer the quietest; pass = at least 5 of 6 correct (antiphase tones cancel on loudspeakers, so loudspeaker users fail). Passers go onto a Prolific custom allowlist for the main study.
* **In the main study:** gold clips (CRIPPLED rated 1 +- 1), trapping clips (expected value +- 1), hidden reference IDEAL (mean rating at least 4).
* **Analysis exclusion (not the same as non-payment):** exclude a listener with 2 or more failed gold/trapping items or mean hidden-reference rating below 4. Implemented in `scripts/analyze_ratings.py` and tested on synthetic data.
* **Payment/rejection:** follow Prolific's attention-check policy, as read on its help pages: for studies of 5 minutes or more reject only after at least 2 failed checks, and give clear instructions. Never reject for low ratings or disagreement. Re-read the policy before launch.
* Limit one submission per participant; do not mix pilot and main participants.

## 6. Power analysis

`scripts/power_analysis.py` (seed 20261118, 1000 simulations per cell, K = 8 tiles per listener, crossed random effects listener x system and tile x system, two-way cluster-robust t test with df = min(L, T) - 1). **Variance components are assumptions** (assumed: sigma_listener x system 0.30, sigma_tile x system 0.35, residual 0.80; pessimistic: 0.40, 0.50, 1.00), to be replaced by pilot estimates. Full table: `results/power_table.md`.

Power for a single pairwise DCR contrast (alpha 0.05, two-sided, no multiplicity correction):

| listeners x tiles | Delta 0.3, assumed | Delta 0.3, pessimistic | Delta 0.5, assumed | Delta 0.5, pessimistic |
|---|---|---|---|---|
| 40 x 24 | 0.54 | 0.34 | 0.94 | 0.75 |
| 60 x 24 | 0.64 | 0.38 | 0.97 | 0.77 |
| 60 x 48 | 0.80 | 0.53 | 0.99 | 0.94 |
| 100 x 24 | 0.70 | 0.43 | 0.99 | 0.85 |
| 100 x 48 | 0.88 | 0.63 | 1.00 | 0.97 |

Reading: more tiles buy more power than more listeners once listeners exceed about 60 (tile variance dominates). Type-I error at Delta = 0 was 0.04 to 0.07 across cells (0.057 to 0.070 at 20 listeners), so the cluster t test is slightly liberal for small L; use 60 or more and report this. Large contrasts (Ours vs NOBAKE or DualCosine, expected well above 1 point if the objective gap is audible) are powered everywhere; **the close contrast Ours vs SeamN2N is the weak point** (it may also be genuinely tiny, which is a finding).

Forced choice (exact binomial, effective n = trials x (1 - no-difference share), design effect 1 + (m - 1) x ICC with ICC 0.1 assumed): power at p(prefer Ours) = 0.60 is 0.49 / 0.79 / 0.92 / 0.99 for 20 / 40 / 60 / 100 listeners; at 0.55 only 0.16 / 0.27 / 0.39 / 0.56. The effective n shrinks if many answer "no audible difference" (the table assumes none are dropped beyond the 8 trials per listener, check `results/power_table.md` for the stated convention).

**Recommendation:** pilot 10, then 60 analysable listeners with a 48-tile pool if exports allow (power 0.80 at Delta 0.3 under the assumed variances), otherwise 24 tiles and a claim limited to Delta of at least 0.5 or to the A/B result.

## 7. Pay and cost

* Floor: German statutory minimum wage EUR 13.90/h in 2026 (https://www.bmas.de/DE/Service/Presse/Pressemitteilungen/2025/anhebung-gesetzlicher-mindestlohn-zum-1-1-2026.html), EUR 14.60 from 2027-01-01. With the ECB reference rate of 2026-11-17 (1 EUR = 0.83305 GBP) the floor is GBP 11.58/h; Prolific's own minimum is GBP 6.00/h.
* Plan: **GBP 12.50/h (= EUR 15.01/h)**: GBP 3.50 for the 16.6-minute main study (GBP 12.65/h at the planned duration), GBP 0.85 for the 4-minute screener. If the 2027 minimum applies when the study runs, raise the reward (GBP 3.50 still clears EUR 14.60 = GBP 12.16/h at 16.6 min). If pilot durations are longer than planned, raise the reward, do not cut the rate.
* Fee: corporate 42.857% (planning case: Julian has a personal e-mail, no institution); academic 33.33% would need an institutional e-mail. VAT on the fee only, assumed 19%.

| analysable listeners | recruited main | screened | rewards | total corporate | corporate + VAT | total academic | EUR corporate |
|---|---|---|---|---|---|---|---|
| 10 (pilot) | 12 | 18 | GBP 57.30 | GBP 81.86 | GBP 86.52 | GBP 76.40 | EUR 98.26 |
| 40 | 48 | 69 | GBP 226.65 | GBP 323.79 | GBP 342.24 | GBP 302.20 | EUR 388.67 |
| **60** | 71 | 102 | GBP 335.20 | **GBP 478.86** | GBP 506.15 | GBP 446.93 | EUR 574.82 |
| 100 | 118 | 169 | GBP 556.65 | GBP 795.21 | GBP 840.54 | GBP 742.20 | EUR 954.58 |

Assumptions: screener pass rate 70%, exclusion rate 15%. Reproduce with `python scripts/cost_model.py`. Prolific fee page date: 2026-10-09; re-check at launch.

## 8. Analysis (pre-specified, `scripts/analyze_ratings.py`)

1. Exclusions as in section 5. Report counts per rule.
2. DCR means per system with two-way (listeners and tiles) cluster-bootstrap 95% intervals; report DMOS-style differences relative to IDEAL.
3. **Confirmatory:** Ours - SeamN2N, Ours - DualCosine, Ours - NoBake, two-way cluster-robust t test (Cameron, Gelbach and Miller), Holm over the three p values at alpha 0.05, 95% intervals for the differences.
4. **Forced choice:** per-listener share of decisive answers for Ours, one-sample t test against 0.5, "no audible difference" rate reported.
5. **Exploratory:** Spearman correlation between tile-by-system mean DCR and objective `R_blend` (does the paper's objective metric track listeners?).
6. Everything else (breakdown by device, experience, hearing answer) is exploratory and labelled so. Optionally register the plan beforehand on OSF or AsPredicted (free) *(optional; not done)*.

`tests/test_listening_pipeline.py` exercises session building, exclusions, contrasts (detects an injected effect, does not reject under the null), Holm, the pay floor and cost model, and the simulation's type-I rate on synthetic data. Run: `pip install -r requirements.txt && pytest -q listening_test/tests`.

## 9. GDPR and ethics

See `consent/consent_and_privacy_en.md`. Summary: Julian is the controller; Prolific IDs are pseudonymous personal data kept only until payment is approved (then replaced by a random code); no name, e-mail, location, IP, cookies or analytics; hearing-difficulty answer is optional and special-category-adjacent, so it has its own consent basis; free-text comments are reviewed and deleted if personal; the collector must not log IP addresses or user agents; anonymous ratings and the analysis code are published. No IRB exists for an independent researcher. TMLR's OpenReview form asks for IRB/human-subjects information, and Acta Acustica or JCMS may ask for an ethics statement, so Julian should decide on an ethics route (section 12).

## 10. How the results enter the paper

Edit points in `main`, none made in this PR (the claims would be false today):
* `subsections/experiments_eval_listening.tex` line 16 (`N_listeners = 0` and "none are invented") and the sentence about a protocol "if run later": replace with a Listening-study subsection (design, N, exclusions, Table of DMOS with intervals, contrast table, A/B result, R_blend correlation).
* `subsections/experiments.tex` lines 21 and 41, `introduction.tex` lines 75 and 84, `limitations.tex` item 1 and the "why deferred" paragraph, `conclusion.tex` line 14: change "no listening study" wording to the study's actual result and state its limits (crowdsourced, headphone-screened, synthetic A4 vibrato tones, 8 tiles per listener).
* Release the anonymised ratings, the session files and the clip manifest with the paper; keep the objective claims as they are.
* If Ours vs SeamN2N is not significant, say so: the paper's objective result is a claim about residual-based metrics, and an honest "no audible difference to SeamN2N, audible gain over NoBake/DualCosine" is a publishable and consistent outcome.

## 11. What each shortlisted venue gains

Venue facts are in `docs/venues/FREE_JOURNALS_DENOISEOPT.md` on branch `venue/tmlr-submission-package` (PR #1).
* **TMLR (current pick):** no listening test required (judged on claims versus evidence). A study would remove the paper's biggest stated limitation and answer the "no perceptual claim" reviewer question, but it is optional; submitting first and running the study during review is possible, with changes then covered by TMLR's revision process. The OpenReview form asks about human-subjects review, which is the ethics question above.
* **Acta Acustica (best topical fit, diamond OA, no APC):** a listening study is, in my judgment, close to a prerequisite for an acoustics audience; Audio Articles allow embedded clips. Also needs a cut to about 12 pages and an answer to EDP's AI policy (language improvement only).
* **JCMS (no APC, double-blind):** evaluation frameworks are encouraged and MP3/MP4 supplements are accepted, so the study and clips help; scope fit remains uncertain.
* **JAIR / Computo:** the study adds little to their criteria.

## 12. Open decisions for Julian

1. Run the pilot (about GBP 82 / EUR 98) at all, and from whose payment method? Prolific needs a funded workspace; nothing has been created.
2. Tile pool 24 or 48 (48 gives power 0.80 at Delta 0.3 under assumed variances but needs more exports).
3. Corporate fee (planning case) or an institutional/academic account (33.33% fee) if one is available.
4. Ethics route and where the collector is hosted (EU server, processing agreement if a third party hosts it). Address for the privacy notice.
5. Order: TMLR submission now, study in parallel, or study first and Acta Acustica.
6. DCR plus A/B (this plan) or MUSHRA as in the older protocol sketch.

## 13. Timeline (estimates, not commitments)

1. Export clips (IDEAL, SeamN2N, pool of 24 or 48 tiles, CRIPPLED, training, trapping clips) and host them on a static EU host: 1 to 2 days of work plus Julian's decision on hosting.
2. Deploy the collector, dry-run with 2 or 3 friends: 1 day.
3. Pilot on Prolific (10 analysable): about 1 day of fieldwork; re-estimate variances and timing, then re-run `power_analysis.py` with the pilot components.
4. Main study: Prolific studies of this size typically finish within days (my expectation, not a measured value); analysis the same day with `analyze_ratings.py`.

## 14. Not done

No clips were exported, no hosting set up, no collector deployed, no Prolific/MTurk account touched, no pilot run. The HIT page was syntax-checked with `node --check` but not tested in a browser against real audio. Prolific policy statements were read from help pages on 2026-11-18 and must be re-read at launch.
