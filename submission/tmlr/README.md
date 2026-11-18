# TMLR submission package (DenoiseOpt / seam-local wavetable repair)

**Status: prepared, NOT submitted.** No OpenReview account was created, nothing was uploaded.

Built from `main.tex` + `subsections/` of this repository at the commit this branch is based on (`3da6d38`, "unified denoise-opt" version, title "Seam-Local Repair of Wavetable Wrap Discontinuities with a Self-Supervised Blended Residual").
Note: the older aiXiv package (aixiv.260719.000003, PR #2 of the archived `denoiseopt-paper`) has a different title and different headline numbers; this package follows `main`.

| File | Purpose |
|------|---------|
| `main.tex`, `subsections/`, `figures/` | Anonymous double-blind manuscript sources in the TMLR style (generated) |
| `denoiseopt_tmlr_anonymous_review.pdf` | Compiled review PDF (tectonic 0.15.0, 54 pages: main text to p. 28, references from p. 29, appendices after) |
| `tmlr.sty` | Official TMLR style file, unmodified (https://github.com/JmlrOrg/tmlr-style-file, last commit 7bf90ef, 2023-06-30) |
| `make_tmlr.py` | Reproducible converter; `python3 submission/tmlr/make_tmlr.py [--accepted]` |
| `cover_letter.md` | Draft text for the OpenReview form fields / comments to the Action Editor |

Build: `cd submission/tmlr && tectonic -X compile main.tex`.

Converter changes: preamble, title/author block, abstract placement, `\cite` -> `\citep` with generated author-year bibliography labels, starred floats -> plain floats, `\keywords` dropped (TMLR has none), a first-page footnote on LLM use (TMLR FAQ, wording pending Julian's OK), and `\tabcolsep` 2 pt for Table `tab:transfer-summary-main` so it fits the single-column block (no overfull boxes left). In the review variant only: links into the author's repositories are plain text, the named author and acknowledgment text are replaced, ReelSynth becomes "the host synthesizer", the review-service name becomes a neutral description, and the CRediT block and the repository sentence in the competing-interests paragraph are dropped. Numbers, tables and figures are untouched.

CI: `.github/workflows/paper-build.yml` regenerates this package, fails if the committed files differ, builds the review PDF with tectonic, fails on overfull boxes or undefined references, and greps the PDF text and metadata for author, repository and project names.

Other files: `AUTHOR_INFO.md` (form data), `VENUES.md` (verified venue shortlist), `TMLR_STYLE_LICENSE_APACHE2.txt` (licence of the TMLR style files).

## Honest status of the paper (read before submitting)

- No klaut or paper-review score for the current head was found in the repo. The older documented numbers are klaut 4.78/10 with 13 majors (Nov 2) and about 6/10 afterwards (`PAPER_SHIP_STATUS.md`). The commit log since then mentions fixing "Klaut v224 findings" without a score.
- No listening study (N_listeners = 0). The abstract says so.
- Length: 54 pages in TMLR format (main text about 28). TMLR gives longer review timescales above 12 pages of main content.
- The method name DenoiseOpt matches the repository name `denoise-opt`. Julian decides whether to rename it for review.
- The repository has no code licence file (GitHub reports NOASSERTION). The manuscript text is CC BY 4.0.

## Open before submission (Julian)

- Venue choice and the submit step. Julian creates the OpenReview profile.
- Wording of the LLM footnote, the cover-letter paragraphs marked [Pending Julian's OK], and a code licence.
