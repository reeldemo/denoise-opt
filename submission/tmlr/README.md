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

Converter changes: preamble, title/author block, abstract placement, `\cite` -> `\citep` with generated author-year bibliography labels, starred floats -> plain floats, `\keywords` dropped (TMLR has none), and, in the review variant only, links into the author's repositories are shown as plain text and the named author/acknowledgment text is replaced. The scientific text, numbers, tables, and figures are untouched.

Known leftovers: one paragraph is 35 pt too wide (`main.log` line 875, an overfull hbox); main text is 28 single-column pages (TMLR accepts any length; reviews are requested within 4 weeks instead of 2 above 12 pages of main content).
