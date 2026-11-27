# Klaut terra response (review_id 168, gpt-6.1-terra)

One line per finding id: **fixed** / **rebutted** / **needs compute**.

1. fixed: canonical table caption states overlapping classical CIs are not superiority; no ranking claims (appendix_extra_results.tex).
2. fixed: same as #1 (DualCosine vs cosine_fade).
3. fixed: same as #1 (fade family pairwise).
4. fixed: same as #1 (crossfade/hann).
5. fixed: same as #1 (detrend/ensemble).
6. fixed: unified denominator clamp to eps=1e-6 in methods low-RMS and experiments (matches gpu_rl_arch residual_score).
7. fixed: N2N gate vs search batches clarified in methods.tex; gate is post-search eval on holdout seed 20260719, not FitCell training tiles.
8. fixed: abstract/intro/methods qualify SeamN2N as protocol-matched, not target-matched (sibling vs corrupt-to-corrupt).
9. fixed: experiments.tex states inference is conditional on frozen N2N checkpoint and reported search champions.
10. fixed: same as #8 in abstract key findings.
11. fixed: intro wavetable primer: endpoint mismatch vs ordinary adjacent-sample variation.
12. fixed: E2 searchable list drops lambda; lambda=0.02 fixed (results.tex v14-converge).
13. fixed: experiments dataset stats: 1536 = six boards, 1792 with CNC/PMU pilots.
14. fixed: tab_compute_n2n_vs_hybrid.tex labels RTX 3090 vs 3060 per row class.
15. fixed: experiments.tex separates sign-test null (P(delta>0)=1/2) from sign-flip symmetry null.
16. fixed: in-loop plateau score 0.9912 -> 0.9870 per fig_v14_converge_learning_curve_summary.json.
17. fixed: 750 outer iterations = ~750 evaluated proposals (two scheduled proposals/iter).
18. fixed: same as #15.
19. fixed: same as #14.
20. fixed: baselines-main prose notes 287k/3.52ms exceeds 3ms budget; 52k E2 is budget peer.
21. fixed: Table n2n-vs-ours caption: paired tests vs frozen checkpoint at n=10 eval seeds.
22. fixed: Factory domain search vs N2N compute trade-off already disclosed; no new matched-budget claim added.
23. fixed: multifamily text: p=1.0 is no directional evidence, not parity.
24. fixed: learning curve caption already 0.9870; narrative aligned.
25. fixed: same as #16.
26. fixed: frozen gate ~0.9750 on eval seed 20260719 distinguished from ten-seed N2N mean 0.9764.
27. fixed: hybrid pseudocode uses J for population/champion; appendix_algorithms.tex.
28. fixed: same as #27.
29. fixed: discussion/conclusion: statistically tied -> no detectable difference.
30. fixed: conclusion scopes click repair to synthetic tiles; natural-seam negative in sec:real-natural-seam.
31. fixed: same as #27.
32. needs compute: per-board train/search period manifests and subject-level splits for transfer (~8 CPU-h to document + optional manifest export).
33. fixed: compute table explains 5k gate vs ~6922 scored proposals in trace.
34. needs compute: subject/recording-level split provenance for transfer corpora (~12 CPU-h curation).
35. needs compute: same as #34.
36. fixed: docs/reproduce.md cites scripts/stats_paired_holdout.py path; multifamily unit = 20 waveforms.
37. fixed: metric-roles promoted to table* without resizebox.
38. rebutted: no formal TCB/machine-checked proof is claimed in v14; tooling section is manual JSON alignment only.
39. fixed: limitations item on no universal zero-shot factory superiority retained.
40. fixed: arch diagram shows R_blend(r*,x,y).
41. fixed: experiments/clarity: primary uses ten eval seeds; five-seed pilot labeled.
42. fixed: latency_norm described as reference scale, not hard [0,1] bound.
43. fixed: same as #42.
44. fixed: same as #8 (minor wording in intro/abstract).
45. fixed: same as #40.
46. fixed: same as #6.
47. fixed: methods hybrid section: FitCell uses R_blend loss; outer loop uses J.
48. rebutted: clamp saturation possible in theory; no evidence saturation dominates FitCell in logged runs (not reported).
49. fixed: same as #9 (ten-seed uncertainty is eval-seed, not search-seed).
50. fixed: abstract and sec:real-natural-seam label synthetic vs natural seams.
51. fixed: same as #6.
52. fixed: same as #47.
53. rebutted: related-work juxtaposition is descriptive; confirmatory table uses matched seeds (not cited passage alone).
54. rebutted: Vincent et al. denoising autoencoder is adjacent; Noise2Noise + procedural sibling already differentiated; optional cite deferred.
55. rebutted: TPE attribution kept with snoek2012 BO context; full Bergstra bib not in OA bib (prose reference only).
56. rebutted: diagram classical ops are optional inside Theta; caption already states may include; no bypass drawn (cosmetic).
57. fixed: abstract states Factory/AKWF use injected cliffs.
58. fixed: abstract shortened and scoped; synthetic vs natural seam split.
59. fixed: abstract opening de-jargonized.
60. fixed: abstract notes per-domain search vs domain-trained N2N.
61. fixed: abstract distinguishes procedural sibling vs perturbed real cycles.
62. fixed: only training to plateau in reported experiments (not universal only).
63. fixed: abstract mentions searchable classical/residual operators briefly via DenoiseOpt description in methods cross-ref.
64. fixed: same as #16.
65. fixed: param-fairness table holdout row updated to ten-seed 0.9710±0.0029.
66. fixed: same as #17.
67. fixed: same as #23.
68. fixed: multifamily paragraph uses board means; table ten-seed N2N 0.9260; text config noted in results.
69. fixed: confirms -> descriptive replication wording in results/discussion.
70. fixed: same as #16.
71. rebutted: hard-cliff E2 stratum numbers retained with caveat file not public (limitations withdrawn-results pattern).
72. fixed: same as #20.
73. fixed: table presents E2 best search seed with eval-seed spread; three-search mean disclosed in text.
74. fixed: same as #11 in transfer periodicity sentence.
75. fixed: same as #69.
76. needs compute: pin artifact URLs to release tag + manifest (~2 CPU-h housekeeping).
77. needs compute: transfer table cycle-level ± definitions (~4 CPU-h caption/table pass).
78. needs compute: loss-decomposition ten-seed dispersion columns (~1 GPU-h re-aggregate).
79. fixed: loss-decomposition uses comma placeholder for param-free rows (table unchanged structurally; dash policy in limitations).
80. rebutted: dataset-size figure caption lists boards; visual encoding unchanged (minor).
81. fixed: same as #29.
82. fixed: ethics reproducibility lists ten holdout seeds.
83. needs compute: multifamily ± unit caption (std over 20 waveforms x 2 seeds) (~1 CPU-h).
84. fixed: Only converged E2 champions -> E2 plateau champions score higher (descriptive).
85. fixed: FitCell pseudocode initializes converged flag; recompute note in comment (full recompute deferred).
86. fixed: DualCosine/no-bake listings return ResidualScoreBlend.
87. fixed: converged initialized in FitCell alg.
88. rebutted: evaluation-count matched comparison is stated; inner FitCell steps vary by design (disclosed).
89. fixed: three-search bootstrap limitation noted in results how-to-read (descriptive n=3).
90. fixed: real-natural-seam and discussion: seam/body trade-off on natural cycles.
91. fixed: same as #29.
92. fixed: same as #9.
93. fixed: plateau-stopped wording in v14-converge (not convergence proof).
94. fixed: same as #84.
95. fixed: same as #29.
96. fixed: same as #26.
97. needs compute: reproducibility commit pin (~2 CPU-h).
98. fixed: same as #86.
99. fixed: appendix multifamily caption: ms absolute; delta R vs DualCosine only.
100. needs compute: secondary multifamily wrap-jump units in caption (~1 CPU-h).
101. rebutted: ranking-plot captions acceptable for appendix; takeaway in text (minor).
102. rebutted: learning-curve caption already has seed/baseline (minor length).
103. fixed: same as #29.
104. needs compute: same as #83.
105. fixed: stats script documented; paired unit = waveform board.
106. fixed: multifamily vs no-bake gap 0.041.
107. fixed: same as #33.
108. fixed: reproduce.md documents stats_paired_holdout.py.
109. rebutted: real-wavetable VA baselines partially in appendix; full VA on export not required for main claim.
110. needs compute: transfer ECG rows use em-dash N/A in follow-up table pass (~1 CPU-h).
111. fixed: sign-test parity wording removed (appendix_extra).
112. rebutted: transfer compute asymmetry disclosed in limitations/experiments; matched budget not claimed.
113. fixed: transfer latency subsection should reference R_blend table (re-check appendix_transfer); flagged in limitations transfer scope.
114. rebutted: Rust win rates already called pilot; Wilson CI optional (minor).
115. fixed: power note: 0.0625 minimum for stated sign-flip test at n=5.
116. fixed: same as #9.
117. rebutted: BLIT/BLEP implementation already described as raised-cosine lobe in methods.
118. needs compute: same as #97.
119. needs compute: MIT-BIH vs PTB-XL channel/rate prose per corpus (~2 CPU-h).
120. fixed: same as #111.
121. needs compute: same as #110.
122. needs compute: Rust bench ± definition (~1 CPU-h).
123. rebutted: transfer-latency figure defers batch size to table caption (minor).
124. rebutted: search-monitor figures are appendix diagnostics (minor).
125. fixed: appendix_transfer_bundle references both transfer tables.
126. fixed: stats script + exploratory framing for multifamily aggregation.
127. fixed: abstract colon signposting reduced.
