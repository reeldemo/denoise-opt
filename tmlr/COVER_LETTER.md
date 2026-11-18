# Cover letter draft (TMLR, via OpenReview; "comment to editors" / cover note)

DRAFT. Not sent. Julian reads and edits before anything is submitted.

---

To the Editors-in-Chief and the Action Editor,

I submit "Seam-Local Repair of Wavetable Wrap Discontinuities with a Self-Supervised Blended Residual" for review at TMLR.

**What the paper does.** Wavetable oscillators click when the stored period does not join cleanly at the wrap. The paper frames the click as a cycle-local seam-restoration problem, scores repairs self-supervised with a procedural cliff-withheld sibling and a blended residual R_blend, and searches compact repair operators with genetic search, PPO and population-based training used as an engineering outer loop. It does not propose a new NAS or RL algorithm.

**What it claims, and what it does not.** Confirmatory comparisons are against neural and classical baselines only (matched Noise2Noise, two circular Residual U-Nets, a sawtooth/pulse generator, a dual-cosine fade), with Holm-Bonferroni correction: for example 0.9903 vs 0.9764 on a 10-seed holdout (adjusted p = 0.0039) and 0.9108 vs 0.8772 on Factory+FX exports. Primary evidence is objective; there is no listening study (zero listeners), which the abstract states, and click-splatter and log-spectral-distortion proxies are reported with their correlation to R_blend. The non-audio periodic-boundary (TDSE) replications and the exploratory pilots are separated from the confirmatory results.

**Why TMLR.** TMLR asks whether the claims are supported by accurate and clear evidence, and accepts accounts of applications of existing techniques. The claims here are limited to what the evidence supports.

**Prior versions and originality.** Earlier versions are public on the aiXiv preprint server (an archive, not an archival peer-reviewed venue; TMLR's policy accepts overlap with preprint servers). Those versions used a different title and different headline claims; the submitted manuscript is the revised paper. To keep the review double-blind I do not link the preprint here and will add it, with the code links, in the camera-ready version. The work is not under review and has not been published elsewhere.

**AI tools.** The manuscript's "Tooling and AI use" section lists the AI tools that assisted software development, literature triage, citation checks and manuscript review. I checked claims, numbers and citations against the code and frozen result files and I am responsible for the content.

**Code and data.** The repository (manuscript, results, search and evaluation code) is public; the link is withheld in the anonymous build and added at camera-ready.

**Length.** The main text runs to about 28 pages in the TMLR single-column format before the references; appendices follow. I understand TMLR describes longer timescales for long submissions.

Sole author: Julian M. Kleber, ORCID 0000-0001-5518-0932, julian.m.kleber@gmail.com.

Suggested action editor: [to be chosen by Julian from the OpenReview list]

Sincerely,
Julian M. Kleber
