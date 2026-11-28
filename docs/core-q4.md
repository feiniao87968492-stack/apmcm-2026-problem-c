# Core Q4 aligned propagation and playback scenarios

The default pipeline passes the selected Q50 absorption curve and distance-penalized rank-one mask model into Q4. Substitutions share eight birds, empirical context weights and the archived clean gross cutoff of 0.287598. [Frozen design](model-spec.md#antigravity-3-q1-and-q4-freeze) ? [Dense component comparisons](../results/core_q4_curves.csv)

| Call | Archived gross clean / loss (m) | Selected gross clean / loss (m) | Joint clean (m) | Joint loss 15 s / 30 s (m) | Pooled-timing joint loss (m) |
|---|---:|---:|---:|---:|---:|
| Flat | 82.4 / 41.8 | 88.3 / 51.6 | 84.5 | 58.0 / 58.0 | 58.0 |
| Modulated | 139.3 / 77.2 | 134.9 / 79.7 | 144.0 | 77.0 / 81.5 | 107.0 |
| Two-voice | ?150 / 116.2 | ?150 / 83.8 | ?150 | 77.0 / 81.5 | 132.0 |

Loss is the hypothetical 20% coupled scenario. The selected timing benchmark remains stimulus-only. The planning model instead factors each arm's timely risk into the selected distance-varying 60 s risk times the fraction of its observed responders by the chosen window. The loss-adjusted natural 30 s probability declines from 0.635 at 20 m to 0.440 at 150 m. At 20% loss, fidelity binds for flat and timely response binds for the other two calls. The first failing nodes for modulated and two-voice are 77.5 and 82.0 m at 15 and 30 s, respectively. [Timely rates](../results/core_q3_conditional_rates.csv) ? [Radii and status](../results/core_q4_radii.csv) ? [Local support](../results/core_q3_support.csv)

At 100 m the selected natural group risks are 0.577 clean and 0.481 under loss for all three calls. The sharp expected counts among eight birds are bounded by [0.577, 4.617] and [0.481, 3.847], respectively. Identical independent bird responses imply 0.816 and 0.630. Conditional shares of 25%, 50% and 75% give the scenarios in the export. [Responder counts and assumed shares](../results/core_q4_responders.csv)

Archived comparisons provide the [waveform noise evidence](appendix5-noise.md), [Fisher allocation](q4-fisher.md), [paired sandwich sensitivity](q4-paired-planning.md) and [manual-review illustration](q4-review-budget.md). At 50 recordings reviewed, uniform random review has fixed-sample marginal central 95% ranges of 1?5 residual false passes and 6?14 missed passes. These are hypergeometric quantiles for the remaining 55 of 105 recordings, starting with six and 19 errors, respectively.

Run the current production comparisons and figures with `python main.py --data "<attachment directory>/date" --output generated`. Use `--archived` for the previous full pipeline and `--help` to list the historical named analyses. The paired uncertainty analyses in the archive remain available as conditional sensitivity evidence.

## Conservation figures

Figure 5 compares matched-power band-limited and broadband noise across six input SNRs. Its intervals describe the paired noise realizations within each of three archived example recordings. Figure 6 presents the archived 120-pair constrained allocation, the production eight-bird count sensitivity and the archived full-prefix two-voice loss boundaries at 100 and 150 m. The 150 m deletion fit uses extrapolated playback risks. [Figure 5 data](../results/core_figure5.csv) ? [Figure 6 data](../results/core_figure6.csv)
