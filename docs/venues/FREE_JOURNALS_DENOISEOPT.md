# Free (diamond open-access) journal options for DenoiseOpt / seam-local wavetable repair

Prepared 2026-11-18 (Europe/Berlin) for Julian M. Kleber. **Nothing was submitted, no journal account was created.**
Facts were read from each venue's official pages on 2026-11-18 (URL next to the fact). Items I could not confirm on an official page are marked *(unverified)*.

**Where the paper lives.** `reeldemo/denoiseopt-paper` is archived (read-only, so no PR can be added there; its PR #2/#3 are frozen). The living sources are in this repository (`reeldemo/denoise-opt`, `main` at `3da6d38`, title "Seam-Local Repair of Wavetable Wrap Discontinuities with a Self-Supervised Blended Residual"). The aiXiv package in `/workspace/aixiv-packages/seam` is the older PR #2 text with a different title and different headline numbers; the packages here follow `main`.

**Claim profile the venue must tolerate:** objective evidence only (R_blend, click-splatter and LSD proxies, Holm-Bonferroni confirmatory tests vs SeamN2N/SeamResUNet/DualCosine), `N_listeners = 0`, "no new NAS/RL algorithm", no perceptual-superiority claim.

## Ranking

| # | Venue | APC (author) | Review time (official) | Fit | Effort |
|---|-------|--------------|------------------------|-----|--------|
| **1 (pick)** | **TMLR** | **0** | decision aimed ~9 weeks after submission | good: judged on evidence vs claims, no listening test required | low (package in this PR) |
| 2 | Acta Acustica | **0** (diamond OA since 2025-01-01) | not stated officially; a third-party listing says about 12 weeks *(unverified)* | very good topical fit (audio signal processing, auditory quality, musical acoustics); acousticians will likely expect a listening test | high (LaTeX re-cut to 8-12 pages, abstract <=200 words, AI-policy question) |
| 3 | Journal of Creative Music Systems (JCMS) | **0** | feedback within 2 months of submission | medium (music systems; creativity not central) | medium |
| 4 | JAIR | 0 | decision in about 8-12 weeks | medium-low (AI journal; significance bar) | medium |
| 5 | Computo | 0 | not stated *(unverified)* | medium-low (stats/ML reproducibility notebook) | high |

### 1. TMLR (recommended now)
* Official: https://jmlr.org/tmlr/ , https://jmlr.org/tmlr/editorial-policies.html , https://jmlr.org/tmlr/author-guide.html , https://jmlr.org/tmlr/faq.html , https://jmlr.org/tmlr/acceptance-criteria.html
* APC: none; "TMLR imposes no fees or payments to authors"; CC BY 4.0, authors keep copyright.
* Review: double-blind, open reviews on OpenReview, at least 3 reviewers; 2-week review deadline for up to 12 main pages, 4 weeks above; FAQ: decision aimed ~9 weeks after submission.
* Criteria: (1) claims supported by accurate and convincing evidence; (2) interest to some of the audience. Not novelty/significance. A claim-evidence gap can be closed by reducing the claim. This matches a paper that explicitly says "objective evidence only, `N_listeners = 0`".
* Scope: includes "accounts of applications of existing techniques that shed light on the strengths and weaknesses of the methods" and new algorithms with sound empirical validation.
* Format: TMLR LaTeX style, any length (long main text delays review), appendix after references, supplementary <=100 MB anonymized.
* Preprints: arXiv or other servers allowed at any time; no link from the anonymous PDF to a named version. aiXiv listing is compatible.
* LLM policy: assistive use allowed, authors responsible. The paper's own "Tooling and AI use" section is therefore compatible.
* Human subjects: the OpenReview form asks for IRB/human-subjects information (author guide) - relevant if the listening test is run first.
* Indexing/reputation: Scopus and DBLP per a secondary source *(unverified)*; official site shows the NeurIPS/ICML/ICLR Journal-to-Conference track membership (news 2025-10-21).
* Audience caveat: ML audience, not acoustics/music-technology.

### 2. Acta Acustica (best topical fit; recommended second, after a listening test)
* Official: https://acta-acustica.edpsciences.org/author-information/instructions-for-authors , https://acta-acustica.edpsciences.org/about-the-journal/open-access , https://acta-acustica.edpsciences.org/about-the-journal/indexed-in , https://www.edpsciences.org/en/publication-charges
* APC: "No APC" for 2026 in the EDP price list; diamond OA since 2025-01-01 as a pilot financed by EAA, CNRS, TIB and others through 2027 (funding gap for 2027 is stated on the open-access page, so continuity is not guaranteed).
* Reputation: indexed in Science Citation Index Expanded and Scopus, among others; 2025 Journal Impact Factor 1.4 (journal's own indexed-in page).
* Scope list includes "Audio Signal Processing and Transducers", "Auditory Quality of Systems", "Musical Acoustics". Article types include Scientific Articles (typically up to 12 pages), Short Communications (<=4 typeset pages) and **Audio Articles** (playable MP3 clips embedded; clips must also be in a public repository).
* Requirements: LaTeX source only, English, any internally consistent style, numbered pages and **line numbers**, figure legends on a separate page, structured (IMRAD) abstract of at most 200 words, at most 80 references, mandatory Data Availability Statement, Conflict-of-Interest statement, authenticated ORCID, suggest three reviewers from different countries. Typical final length 8-12 pages; the current paper is about 19 two-column pages of main text.
* Preprints: "Submissions of manuscripts previously published on Preprint servers such as arXiv are accepted."
* **AI policy risk:** EDP policy (linked from the instructions) allows AI "only for language improvement", forbids AI creation or modification of figures, and requires disclosure in the cover letter and manuscript. The paper's tooling section says Cursor assisted the figure scripts and code, SciSpace/NotebookLM assisted literature and citation checks. Julian must decide whether that is compatible before choosing this venue.
* Needed changes: cut to about 12 pages (move the TDSE/transfer material to supplement or a second paper), 200-word IMRAD abstract, line numbers, Data Availability statement, COI statement, MP3 audio files for an Audio Article, listening-test results strongly advisable *(my judgment, not an official requirement)*.

### 3. JCMS - Journal of Creative Music Systems
* Official: https://www.jcms.org.uk/submissions/ , https://www.jcms.org.uk/site/submission-requirements/ ; DOAJ entry reports no APCs.
* APC: "JCMS does not charge a publication fee. Funding is provided by the University of Huddersfield Press." CC BY 4.0 or CC BY-ND 4.0.
* Review: double-blind; feedback within two months; publication within one month of acceptance.
* Scope: "computer systems which generate, perform or analyse music" that show creativity or shed light on creativity; empirical articles on design and implementation of new techniques are welcome. A wavetable seam-repair operator is music technology but not obviously creative; a scope-fit risk.
* Format: LaTeX-generated PDF or Word with the journal templates, APA7, numbered sections (max two nesting levels), MP3/MP4 as a ZIP, evaluation framework encouraged (e.g. SPECS). Preprint and AI-use policies not found on the pages I read *(unverified)*.

### 4. JAIR
* Official: https://www.jair.org/index.php/jair/about/submissions , https://www.jair.org/index.php/jair/about
* APC: none ("we do not charge any publication fees to authors, nor do we charge readers"); indexed in INSPEC, Science Citation Index, MathSciNet.
* Review: 8-12 weeks. Mandatory JAIR LaTeX format and reproducibility checklist; papers outside the format are rejected without review. arXiv posting allowed. Bar: originality and significance for the AI community; an engineering study with `N_listeners = 0` is a weak fit.

### 5. Computo
* Official: https://computo-journal.org/site/about.html , https://computo-journal.org/site/guidelines-authors.html
* APC: none (Diamond OA, CC-BY 4.0). Requires a Quarto notebook in a GitHub repo with frozen environment and CI, data on Zenodo/OSF; reviewers run the code. New AI-use declaration since 2026-11-04. Scope: stats/ML numerical studies, software/tutorial papers.

### Excluded (with evidence)
* **JMLR** (https://jmlr.org/author-info.html): no fees, but "does not publish applications of machine learning to other domains" and may reject for narrow audience.
* **TISMIR** (https://transactions.ismir.net/about/submissions): research article APC GBP 530, waiver on request only, so not APC-free.
* **Applied Sciences (MDPI)**: APC 2400 CHF on its Audio Signal Processing special-issue page (https://www.mdpi.com/journal/applsci/special_issues/audio_signal_processing).
* **JOSS** (https://joss.readthedocs.io/en/latest/submitting.html): free, but publishes software, needs six months of public history. `reelsynth` (public since 2026-07-11, MIT) could qualify for a software paper later; `denoise-opt` was created 2026-11-15 and does not. Not a venue for this manuscript.

## Manuscript changes needed for TMLR
1. Anonymize (done in `submission/tmlr/`); Julian still has to provide an anonymized code mirror for the supplementary ZIP.
2. Update stale repository references: `subsections/conclusion.tex` and `subsections/ethics.tex` still name the archived `reeldemo/denoiseopt-paper` as the paper repository.
3. If the listening study is run, add its results and drop the `N_listeners = 0` statements; if not, keep wording as is (no change needed for TMLR).
4. Length: main text is 28 single-column pages; trimming to about 12 would halve the review turnaround requested by TMLR (4 weeks to 2).
5. The released audio clips cover no-bake, DualCosine, Ours and meta-search arms, but not SeamN2N/SeamResUNet. Add those exports before any audio-based claim (needed for the listening test anyway).
6. Fix one overfull paragraph (`main.log` line 875).

## Recommendation
Submit to TMLR first if Julian wants speed and no listening dependency. If Julian prefers the acoustics audience and is willing to run the listening study and cut to about 12 pages, go to Acta Acustica after clearing the AI-policy question. Do not dual-submit: both venues forbid parallel submission.

## Open decisions for Julian
1. TMLR now, or listening study first and Acta Acustica?
2. Is the paper's AI-assisted workflow acceptable under EDP's "language improvement only" rule (only matters for Acta Acustica)?
3. Ethics approval route for the listening study (no institution; TMLR asks for IRB info; Prolific does not itself require approval unless an institution/policy does, https://researcher-help.prolific.com/en/articles/449628-irb-applications-and-ethics-approval).
4. Trim to about 12 main pages or keep the long version.
