# Free (no author fee) peer-reviewed venues for the DenoiseOpt / seam-repair paper

Facts were read from the journals' own pages on 2026-11-18 (Europe/Berlin) unless marked **(3rd party)** (aggregator or search result, not the journal) or **not verified**. Nothing has been submitted; no journal account was created.

## Shortlist

| # | Venue | Author fee | Access / licence | Review | Index | Format | Preprint / AI policy |
|---|---|---|---|---|---|---|---|
| 1 | **TMLR** <https://jmlr.org/tmlr/> | none: "imposes no fees or payments to authors" ([policies](https://jmlr.org/tmlr/editorial-policies.html)) | free; CC BY 4.0 from submission, author keeps copyright ([author guide](https://jmlr.org/tmlr/author-guide.html)) | open + double-blind on OpenReview; >=3 reviewers; aims at a decision about 9 weeks after submission ([FAQ](https://jmlr.org/tmlr/faq.html)); main text over 12 pages gets longer timescales | DBLP records exist **(3rd party search result)**; Scopus and DOAJ **(3rd party, PubScope)**; no Web of Science JIF **(3rd party)**; own pages list no index | TMLR LaTeX style ([repo](https://github.com/JmlrOrg/tmlr-style-file)); any length; anonymous | preprints on arXiv-like servers allowed at any time; LLMs allowed as assistive tools, author fully responsible |
| 2 | **Acta Acustica** (EAA) <https://acta-acustica.edpsciences.org/> | none: "Diamond Open Access ... authors do not have to pay any article processing charges" since 2025-01-01 ([aims](https://acta-acustica.edpsciences.org/about-the-journal/aims-and-scope), [instructions](https://acta-acustica.edpsciences.org/author-information/instructions-for-authors)); one sentence on short communications still mentions invoicing, so confirm with the editorial office | free; CC BY 4.0, authors keep copyright | not stated on the pages read | Scopus Q1 and Web of Science SCIE, DOAJ **(3rd party, journalindexes.com)**; own pages list none | LaTeX source only, any internally consistent style, line numbers, structured abstract <= 200 words, <= 80 references (some from acoustics journals), typically 8-12 pages, mandatory data-availability statement, 3 suggested reviewers | preprints "are considered as original"; **AI use limited to language improvement and must be disclosed in the cover letter** (see risk below) |
| 3 | **Journal of Creative Music Systems** <https://www.jcms.org.uk/> | none: "does not charge a publication fee" ([submissions](https://www.jcms.org.uk/submissions/)) | free; CC BY 4.0 or CC BY-ND 4.0, authors keep copyright | double-blind; feedback intended within 2 months, publication within 1 month of acceptance (own page, a target not a guarantee) | own page only says the article section is "Indexed"; DOAJ and Scopus **not verified on the journal's page** (a search result lists DOAJ) | LaTeX or Word template; APA7 citations ([requirements](https://www.jcms.org.uk/site/submission-requirements/)); anonymised | not stated on the pages read |
| 4 | **JAIR** <https://www.jair.org/> | none ([about](https://www.jair.org/index.php/jair/about)) | free; CC BY (since 2023-05-01) | decision in about 8-12 weeks ([submissions](https://www.jair.org/index.php/jair/about/submissions)) | own page: INSPEC, Science Citation Index, MathSciNet | JAIR template (Overleaf link on [author instructions](https://www.jair.org/index.php/jair/authorinstrs)); mandatory reproducibility checklist | not under review/published elsewhere; arXiv posting allowed; AI policy: core contributions must come from the authors |

## Scope fit

1. **TMLR (recommended).** Scope includes "accounts of applications of existing techniques that shed light on the strengths and weaknesses of the methods", which is how the paper describes its use of GA, PPO and PBT. The acceptance test is evidence for the claims, not novelty. Weak points: audio is outside most TMLR reviewers' home field, there is no listening study, and the paper is very long (about 28 pages of main text in this format, 54 with appendices).
2. **Acta Acustica.** "Audio Signal Processing and Transducers", "Musical Acoustics" and "Computational and Numerical Acoustics" are in scope, so the topic fits best here. Weak points: reviewers from acoustics will want perceptual evidence and the paper has none; the journal wants the reference list to include acoustics journals; the paper must be cut to roughly 8-12 pages and 80 references; and its AI policy ("AI tools only for language improvement") conflicts with how this paper says Cursor, SciSpace and NotebookLM were used. That conflict could make a submission non-compliant, so do not choose this venue before asking the editorial office.
3. **JCMS.** Scope is music-creative systems (systems that generate, perform or analyse music). A seam-repair operator is audio DSP rather than a creative system, so the fit is weak. Listed because it is verifiably free and its template is simple.
4. **JAIR.** Covers all AI including search and reinforcement learning, SCI-indexed per its own page. The application is audio, the paper would need the JAIR template and checklist, and the AI-tools policy needs the same care as above.

## Checked and excluded (not free)

| Venue | Why excluded | Source |
|---|---|---|
| TISMIR | APC GBP 530 per research article; waiver on request, not guaranteed | [submissions page](https://transactions.ismir.net/about/submissions/) |
| EURASIP Journal on Audio, Speech, and Music Processing | APC (about USD 1,890 / EUR 1,490 in third-party summaries); not read on the journal's own page | search results (**3rd party**) |
| JMLR | scope excludes applications of ML to other domains; no fee, so not excluded for cost, just poor fit | [author info](https://www.jmlr.org/author-info.html) |
| JOSS | would publish the software only, "Your paper must not focus on new research results" | [JOSS docs](https://joss.readthedocs.io/en/latest/submitting.html) |

## Prior publication on aiXiv

`aixiv.260719.000003` is listed on aiXiv (fetched 2026-11-18) as "v3.2, 2026-11-16", titled "Seam-Local Repair of Wavetable Wrap Discontinuities with a Self-Supervised Blended Residual", author Julian M. Kleber. aiXiv describes itself as "a free, AI- or human-peer-reviewed preprint archive" ([about](https://aixiv.science/about)). TMLR says preprint servers do not count as overlap; Acta Acustica says preprint submissions are considered original; JAIR says authors may post to arXiv and similar. JCMS does not say, so ask or state it in the cover letter. The repo head is newer than aiXiv v3.2 (two commits after it on 2026-11-17/18), so the preprint is slightly behind the manuscript.

## What changes if Julian picks another venue

| Venue | Still to do |
|---|---|
| Acta Acustica | ask about AI-use compliance first; new LaTeX layout with line numbers; structured abstract <= 200 words; cut to about 12 pages and <= 80 references (the paper has 39); data-availability statement; 3 suggested reviewers; AI-use disclosure in cover letter; ORCID is authenticated through the submission system |
| JCMS | LaTeX/Word template; APA7 references; anonymise; ask about preprint policy |
| JAIR | JAIR template; reproducibility checklist; account registration by Julian |

## TMLR-specific cautions

- Julian creates the OpenReview profile himself; this package created no account.
- Quota: TMLR limits submissions per author per year ("Generalized Harmonic Quota Rule, N_1 = 2 and N_9 = 9"). If the NCA paper goes to TMLR too, check the remaining budget with the tool linked on [the policies page](https://jmlr.org/tmlr/editorial-policies.html).
- Anonymity: in the review build `make_tmlr.py` replaces the project name ReelSynth with "the host synthesizer", the review-service name with a neutral description, and drops the CRediT block and the repository sentence in the competing-interests paragraph. The method name DenoiseOpt is close to the repository name `denoise-opt` and stays in the text. Julian decides whether to rename it for review.
