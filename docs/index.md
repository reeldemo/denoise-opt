# DenoiseOpt

Manuscript sources, figure data and statistics scripts for *Unsupervised Wrap-Discontinuity Repair in Wavetable Synthesis via Hybrid GA-PPO Meta-Search* (v14).

A looped wavetable period has a discontinuity where its end meets its start. The manuscript searches for a small repair operator at that seam without paired training data, using a hybrid genetic-algorithm and PPO meta-search. Every method is scored with one locked metric, R_blend. No listening study was run (N_listeners = 0), so the evidence is objective.

- [Install](install.md) the tools.
- Find your way around in the [repository layout](layout.md).
- [Reproduce](reproduce.md) the paired statistics, rebuild the PDF, or see how the full GPU runs are launched.
- Read the [API reference](api.md) for the experiment scripts.
- See [data and licence](data-and-licence.md).
