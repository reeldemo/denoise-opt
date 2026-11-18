# Draft cover note for the TMLR submission (not sent)

TMLR has no separate cover-letter upload; this text is for the OpenReview submission fields. Julian reviews and edits it first.

---

**Title:** Seam-Local Repair of Wavetable Wrap Discontinuities with a Self-Supervised Blended Residual

**Author:** Julian M. Kleber (ORCID 0000-0001-5518-0932), Independent Researcher, julian.m.kleber@gmail.com (identity withheld in the anonymous PDF)

**Dear Action Editor,**

Please consider the attached manuscript for TMLR.

**Contribution.** The paper treats the click at the wrap point of a wavetable oscillator as a cycle-local seam-restoration problem and scores repairs self-supervised with a blended residual R_blend against a procedurally withheld ideal sibling. HybridSeam (called DenoiseOpt in the public repository) searches compact repair operators with an outer loop of genetic search, PPO and population-based training. The paper states plainly that these search tools are reused and that no new NAS or RL algorithm is proposed.

**Evidence and its limits.** Confirmatory comparisons against matched neural and classical baselines (SeamN2N, SeamResUNet, DualCosine) use Holm-Bonferroni correction; the 10-seed holdout result is 0.9903 vs 0.9764 for matched SeamN2N (adjusted p = 0.0039). The evidence is objective: N_listeners = 0, no MOS/MUSHRA was collected, and the manuscript says so in the abstract and limitations; proxies for click splatter and log-spectral distortion are reported alongside. Perceptual superiority is not claimed. [If the crowdsourced listening test planned in the listening-test PR is run before submission, replace this paragraph with its results.]

**Fit with TMLR.** The submission is an empirical study with sound validation and claims limited to the evidence, which is what TMLR's first acceptance criterion asks for; it makes no state-of-the-art or novelty claim beyond that.

**Prior versions and originality.** Earlier versions are public on the aiXiv preprint server (an archive, not an archival peer-reviewed venue. TMLR's policy accepts overlap with preprint servers). Those versions used a different title and different headline claims, and the submitted manuscript is the revised paper. To keep the review double-blind I do not link the preprint here and will add it, with the code links, in the camera-ready version. The work is not under review and has not been published elsewhere. [Pending Julian's OK]

**Code and data.** Code, frozen result files and CC BY 4.0 manuscript sources are in a public repository (links withheld in the anonymous PDF; an anonymized mirror will be added to the supplementary ZIP). Code is under the MIT licence (Julian's decision of 2026-11-18); the manuscript text and figures are CC BY 4.0.

**Human subjects / IRB:** none so far (a listening study is planned) [Pending Julian's OK]. **Funding:** none. **Competing interests:** none.

**LLM use:** AI assistants (Cursor, Grok Bot, Hermes Agent, Antigravity and SciSpace) were used for code, literature search and text, as disclosed in a first-page footnote. I checked all numbers and citations and I am responsible for the content.

Sincerely,
Julian M. Kleber
