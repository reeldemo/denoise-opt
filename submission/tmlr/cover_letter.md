# Draft cover note for the TMLR submission (not sent)

TMLR has no separate cover-letter upload; this text is for the OpenReview submission fields. Julian reviews and edits it first.

---

**Title:** Seam-Local Repair of Wavetable Wrap Discontinuities with a Self-Supervised Blended Residual

**Author:** Julian M. Kleber (ORCID 0000-0001-5518-0932), Independent Researcher, julian.m.kleber@gmail.com (identity withheld in the anonymous PDF)

**Dear Action Editor,**

Please consider the attached manuscript for TMLR.

**Contribution.** The paper treats the click at the wrap point of a wavetable oscillator as a cycle-local seam-restoration problem and scores repairs self-supervised with a blended residual R_blend against a procedurally withheld ideal sibling. DenoiseOpt searches compact repair operators with an outer loop of genetic search, PPO and population-based training. The paper states plainly that these search tools are reused and that no new NAS or RL algorithm is proposed.

**Evidence and its limits.** Confirmatory comparisons against matched neural and classical baselines (SeamN2N, SeamResUNet, DualCosine) use Holm-Bonferroni correction; the 10-seed holdout result is 0.9903 vs 0.9764 for matched SeamN2N (adjusted p = 0.0039). The evidence is objective: N_listeners = 0, no MOS/MUSHRA was collected, and the manuscript says so in the abstract and limitations; proxies for click splatter and log-spectral distortion are reported alongside. Perceptual superiority is not claimed. [If the crowdsourced listening test planned in the listening-test PR is run before submission, replace this paragraph with its results.]

**Fit with TMLR.** The submission is an empirical study with sound validation and claims limited to the evidence, which is what TMLR's first acceptance criterion asks for; it makes no state-of-the-art or novelty claim beyond that.

**Related versions.** An earlier version of this work is listed on aiXiv (aixiv.260719.000003) and received its automated review there. It is not published or accepted at an archival venue and is not under review elsewhere. The anonymous TMLR PDF does not link to the named version.

**Code and data.** MIT-licensed code and CC BY 4.0 manuscript sources are public (links withheld in the anonymous PDF; an anonymized mirror will be added to the supplementary ZIP). Audio comparison clips are in the ReelSynth repository.

**Human subjects / IRB:** none so far (a listening study is planned, see the separate listening-test PR). **Funding:** none. **Competing interests:** none.

**LLM use:** the manuscript's "Tooling and AI use" section lists the AI-assisted tools (Cursor, SciSpace, NotebookLM, aiXiv review); the author checked all claims, numbers and citations against code and frozen result files and takes full responsibility. [Julian to confirm wording.]

Sincerely,
Julian M. Kleber
