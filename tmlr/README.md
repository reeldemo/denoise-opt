# TMLR submission package (draft, NOT submitted)

Source: `main.tex` and `subsections/` at head `3da6d38` of `main` (the current manuscript; aiXiv shows v3.2 from 2026-11-16 and this head has two later commits). This branch only adds the TMLR packaging.

| File | What |
|---|---|
| `main_tmlr.tex` / `main_tmlr.pdf` | anonymous review build in TMLR style (54 pages; main text 28) |
| `main_tmlr_preprint.tex` | same text, non-anonymous (`[preprint]` option); PDF not committed, rebuild it |
| `tmlr/make_tmlr.py` | regenerates the `.tex` files and `tmlr/subsections/` |
| `tmlr/subsections/` | copies of `subsections/` with code links and the author name behind macros |
| `tmlr/tmlr.sty`, `fancyhdr.sty`, `tmlr.bst` | TMLR style files (Apache-2.0) from <https://github.com/JmlrOrg/tmlr-style-file> |
| `tmlr/COVER_LETTER.md`, `AUTHOR_INFO.md`, `VENUES.md` | cover letter draft, form data, verified shortlist |

Build (repo root): `python3 tmlr/make_tmlr.py && tectonic -X compile -Z search-path=tmlr main_tmlr.tex`

## Honest status of the paper (read before submitting)

- No klaut or paper-review score for the current head was found in the repo. The older documented numbers are klaut 4.78/10 with 13 majors (Nov 2) and about 6/10 afterwards (`PAPER_SHIP_STATUS.md`); the commit log since then mentions fixing "Klaut v224 findings" without a score. I did not re-run any review.
- No listening study (N_listeners = 0). The abstract says so.
- Length: 54 pages in TMLR format; TMLR warns that long submissions get longer review timescales.
- Anonymity leaks that remain: project names (ReelSynth, denoise-opt). See `VENUES.md`.

## Changes against `main.tex`

Only preamble/title block (TMLR style, numeric citations kept), plus macros so that GitHub links and the author name are neutral in the anonymous build. Body text, tables and numbers are unchanged.

## Open before submission

- Julian's own yes to the venue and the submit step; Julian creates the OpenReview profile.
- A standard code-licence file in the repo (GitHub reports the licence as NOASSERTION).
- Build has no undefined references; remaining warnings are over/underfull boxes.
