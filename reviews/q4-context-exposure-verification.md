# Independent verification of Q4 context-dependent intermittent exposure

**Pass.** I rebuilt the eight-bird context prediction grid and date-block resamples, with each model fitted once per sampled date draw and predictions reused across all allocations. I used the published Q3 fitter and acoustic draw generator, independently calculated the whole-pair far-distance exclusions, and formed the full-data clean 20 m isotonic cutoff from the weighted context responses. Running each acoustic shape explicitly on all 161 grid nodes reproduced the archived standardized clean/noisy counts of 4,776/3,230 for the full fit and 4,753/2,430 for union deletion. [Frozen specification](../docs/model-spec.md#q4-context-dependent-intermittent-exposure-freeze) · [Archived endpoints](../results/q4_intermittent_noise_checks.csv)

| Fit | After feeding clean/noisy | Commuting clean/noisy | Searching clean/noisy |
|---|---:|---:|---:|
| Full | 4,707 / 2,884 | 4,592 / 2,702 | 4,785 / 4,369 |
| Union deletion | 4,494 / 1,309 | 4,439 / 2,224 | 4,765 / 4,253 |

I computed the context weights from distinct observed experiment IDs. The resulting counts were 36, 65 and 38 out of 139. At each checkpoint the independent three-variable HiGHS linear program optimized the change in attainment over weighted exposure amounts. The equality constraint fixed their sum to the overall share, and each amount lay between zero and its context's weight. I evaluated the uniform allocation directly and inverted each curve by bisection. The six maximum qualifying fractions are interior and their attained shares equal 80%. [Context counts](../results/q4_context_exposure_counts.csv) · [Limits and allocations](../results/q4_context_exposure_limits.csv)

| Fit | At 50% exposure, pass share min / uniform / max | Limits at 80%, min / uniform / max |
|---|---:|---:|
| Full | 77.74% / 82.08% / 86.41% | 44.16% / 56.78% / 66.39% |
| Union deletion | 66.33% / 73.79% / 81.26% | 22.05% / 35.11% / 52.73% |

All eight count records, 30 checkpoint records, six limits and 24 support records agree with production commit 2105296. The LP shares, allocations and boundary locations agree with the exact-rational exports within an absolute tolerance of 1e-11. The extrema straddle 80% at 50% exposure in both fits. The context-specific result thresholds each context before averaging and uses a common cutoff from the full-data standardized response. [Checkpoints and allocations](../results/q4_context_exposure_checks.csv)

Within 25 m of 100 m, the full and deleted fits each have seven after-feeding natural trials with two responses, and six after-feeding control trials with one response. In searching, the earliest retained distance is 40 m for both arms, so the 20–39.5 m prefix nodes lie outside their observed context-specific distances. These are trial support counts across recorded group sizes. Context-linked receiver exposure and behavioral noise response remain unmeasured. [Support by context and arm](../results/q4_context_exposure_support.csv)
