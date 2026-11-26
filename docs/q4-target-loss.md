# Q4 loss limits by target distance

For a two-voice target, each of the 4,800 paired draws supplies the retention needed to reach its clean full-data 20 m net cutoff. The endpoint rule takes the maximum across four curves at the target. The shared-curve prefix takes the maximum over grid nodes from 20 m to the target. The four-curve prefix takes both maxima. For the resulting 3,840th order statistic R, the inclusive loss region satisfies (1−a)(1−b) ≥ R with each loss capped at 20%. [Frozen protocol](model-spec.md#q4-loss-boundaries-at-target-radii-freeze) · [Full grid requirements](../results/q4_target_loss_grid.csv)

| Fit | Target | Equal losses, four-curve endpoint | Equal losses, shared prefix | Equal losses, four-curve prefix |
|---|---:|---:|---:|---:|
| Full | 50 m | 20% cap | 20% cap | 20% cap |
| Full | 100 m | 19.560% | 20% cap | 19.397% |
| Full | 150 m | 9.788% | 11.226% | 9.786% |
| Union deletion | 50 m | 20% cap | 20% cap | 20% cap |
| Union deletion | 100 m | 15.969% | 18.122% | 15.696% |
| Union deletion | 150 m | 0.215% | 1.721% | 0.113% |

The boundary table also gives the maximum response-excess loss at acoustic losses of 0%, 10% and 20%. At 100 m under the four-curve prefix, 20% acoustic loss allows up to 18.789% response-excess loss with the full fit and 11.160% after deletion. At the union-deleted 150 m target, one loss alone can reach 0.226% and each equal loss can reach 0.113%. The clean four-curve prefix passes in 3,850/4,800 draws in this batch, with an exact 95% Monte Carlo interval of 79.05%–81.33%. [Loss boundaries and counts](../results/q4_target_loss_boundaries.csv)

Applying 20% to both losses yields radii of 97, 109.5 and 96 m with the full fit and 85.5, 92.5 and 84 m after union deletion, in rule order. Retained natural and control ranges are 20–200 and 5–200 m in the full fit and 20–100 and 5–120 m after deletion. The 50 and 100 m prefixes are within both retained ranges for both fits. The 150 m target extrapolates for both arms after deletion. The losses describe hypothetical scenarios on the 0.5 m grid. [Recovered radii](../results/q4_target_loss_radii.csv) · [Observed ranges](../results/q4_consecutive_ranges.csv)

Run `python main.py --data "<attachment directory>/date" --q4-target-loss`.
