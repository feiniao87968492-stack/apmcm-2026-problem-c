# Q4 allocation under paired response dependence

The protocol froze at `2bdbc6f` and the calculations ran at `b47db32`. All four plans allocate 120 equal-cost pairs and place at least 10 in each focal cell. Both arms contribute marginal information to the sandwich bread, with the original ridge curvature added once. The meat sums expected whole-pair score covariances, using fitted marginal mask probabilities and four fixed any-response log odds ratios. The positive values 0.4644, 1.0307 and 1.5971 are the strict-fold minimum, midpoint and maximum. They define planning scenarios. [Frozen protocol](model-spec.md#paired-dependence-allocation-sensitivity-freeze)

| Allocation | Independence | Fold minimum | Midpoint | Fold maximum | Overall maximum | Pairs at 20 m | Pairs at 150 m | Independence cost vs Fisher |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Uniform | 0.5134 | 0.5097 | 0.5059 | 0.5032 | 0.5134 | 30 | 30 | +0.08146 |
| Released constrained Fisher | 0.4320 | 0.4271 | 0.4277 | 0.4286 | 0.4320 | 66 | 22 | 0 |
| Midpoint greedy | 0.4336 | 0.4287 | 0.4237 | 0.4223 | 0.4336 | 66 | 23 | +0.00161 |
| Greedy across all scenarios | 0.4412 | 0.4376 | 0.4366 | 0.4372 | 0.4412 | 71 | 18 | +0.00920 |

Each scenario column gives the largest variance ratio over the three Q4 margins, normalized by the corresponding margin's current-data sandwich variance in that scenario. Independence contributes the highest ratio for each plan. The released Fisher allocation has the smallest overall observed maximum among the four plans. Midpoint greedy improves the ratios at the midpoint and maximum log odds. The all-scenario greedy rule optimizes each addition, and its final allocation has the largest overall maximum among the three nonuniform plans. The independent sandwich estimate can differ from the original inverse penalized Fisher estimate because the ridge contributes only to bread. [Cell allocations](../results/q4_paired_planning_allocations.csv) · [Margin variances and standard errors](../results/q4_paired_planning_precision.csv) · [Plan summary](../results/q4_paired_planning_summary.csv)

Run `python q4_paired_planning.py --data "<attachment directory>/date"` from the repository root. The command uses the archived Q2 and strict-playback results.
