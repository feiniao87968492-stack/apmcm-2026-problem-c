# Context mix and behavior priorities in Q4

The protocol froze at `a2e82e9` and ran at `094fad4`. The analysis uses the shared-exponent Q2 curve and Q3 mask probabilities at eight birds. It averages over the 20–150 m annulus under radial symmetry. The same 300 paired acoustic and whole-date draws compare clean conditions and local 6 dB acoustic loss with response held fixed.

| Outcome at empirical context mix | Clean area scores | 6 dB area scores |
|---|---|---|
| Any response | 0.259, 0.381, 0.435 | 0.167, 0.280, 0.343 |
| Head raising | 0.175, 0.243, 0.181 | 0.115, 0.182, 0.147 |
| Vocalizing | 0.234, 0.306, 0.384 | 0.150, 0.223, 0.301 |
| Approach | 0.029, 0.132, 0.097 | 0.019, 0.098, 0.079 |

Triplets follow flat, modulated and two-voice order. Every pure context and the empirical mix give the same point ordering for any response in both scenarios. Head raising and approach marginal probabilities instead yield the highest fitted scores for modulated calls under the empirical mix. These marginals include co-occurring events. The clean empirical any-response scores and their intervals agree with the released annulus. [Scores and paired changes](../results/context_priority_scores.csv) · [Call gaps and intervals](../results/context_priority_gaps.csv)

| Two-voice minus modulated | Minimum [95% interval] | Maximum [95% interval] |
|---|---|---|
| Clean | −0.077 [−0.297, −0.015] | +0.094 [−0.074, +0.259] |
| Local 6 dB | −0.047 [−0.206, −0.006] | +0.089 [−0.038, +0.211] |

Both point minima occur when head raising is prioritized in searching, and both maxima when vocalizing is prioritized after feeding. For shared unit-sum context weights and shared unit-sum behavior weights, bilinearity makes the mixed gap a convex combination of vertex gaps. The interval endpoints are recomputed over all vertices within each draw. No directional lower 95% bound for the minimum is positive in either scenario. [All directional endpoints and attaining vertices](../results/context_priority_bounds.csv)

The empirical context weights are 36/139 after feeding, 65/139 commuting and 38/139 searching. The coverage windows are intersected with the 20–150 m support. Near 150 m (125–150 m), the eight natural trials include one approach. Three call-by-context cells contain zero trials there. Predictions in those cells borrow information through the common mask model. [Trial, date and event coverage](../results/context_priority_coverage.csv)
