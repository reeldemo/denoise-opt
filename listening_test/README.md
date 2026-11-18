# DenoiseOpt crowdsourced listening test (plan and tooling)

**Amazon Mechanical Turk closed on 2026-09-30, so this targets Prolific.** Read `PLAN.md` first (design, power, pay, cost, GDPR, how results enter the paper, open decisions).
Nothing here has been run on real participants; no accounts exist and nothing was funded.

| Path | What it is |
|---|---|
| `PLAN.md` | the plan |
| `config/design.json` | all design constants and assumptions (variance components are placeholders) |
| `scripts/power_analysis.py` | simulation-based power for DCR contrasts + exact binomial for A/B -> `results/power_table.md` |
| `scripts/cost_model.py` | reward and fee model -> `results/cost_table.md` |
| `scripts/session_builder.py` | balanced per-listener session JSON from a clip manifest (`manifest.example.csv`) |
| `hit/index.html`, `hit/hit.js` | static listening page (consent, headphone screener, practice, DCR, A/B, questionnaire); no cookies, no analytics |
| `scripts/analyze_ratings.py` | pre-specified analysis: exclusions, DCR means with bootstrap CIs, Holm-corrected contrasts, A/B, R_blend correlation |
| `consent/consent_and_privacy_en.md` | consent and privacy notice draft |
| `collector/schema.sql` | PostgreSQL schema for the collector (not deployed) |
| `tests/` | pytest suite on synthetic data |

```bash
cd listening_test
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
pytest -q tests
python scripts/power_analysis.py --nrep 1000        # about 1 minute
python scripts/cost_model.py
python scripts/session_builder.py --manifest manifest.csv --extra clips_extra.csv --n-sessions 60 --out hit/sessions --base-url https://HOST/clips
```
To try the page locally put the sessions and clips under `hit/` and run `python3 -m http.server` there, then open `index.html?stage=main`. Before any real launch set `CONFIG.resultEndpoint` and the three Prolific completion URLs in `hit/hit.js`.
