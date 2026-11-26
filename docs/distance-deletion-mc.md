# Monte Carlo precision of Q4 distance-deletion decisions

The protocol froze at `0e2899e` and ran at `8429d3e`. The archived 300 draws and the first 300, 1,200 and 4,800 fresh draws are reported with exact pointwise 95% Clopper–Pearson intervals. The fresh prefixes are nested. All draws were valid. An interval containing 80% is computationally unresolved. [All counts, intervals and decisions](../results/distance_deletion_mc.csv)

| Target | Full fit | Drop 125–175 m | Drop above 175 m | Drop both bands |
|---|---:|---:|---:|---:|
| Clean two-voice own-net, 150 m | 94.31% | 91.54% | 87.02% | 83.38% |
| Coupled two-voice own-net, 100 m | 85.75% | 80.90% | 78.92% | 74.48% |
| Clean modulated gross, 100 m | 84.88% | 82.94% | 86.40% | 84.35% |

At 4,800 draws all intervals in the first and third rows lie above 80%. For the coupled 100 m target, the full fit lies above and union deletion lies below. The intervals for near and far deletion contain 80%, at [79.75%, 82.00%] and [77.73%, 80.06%]. For the clean 150 m union result, the archived count is 239/300 with interval [74.66%, 84.07%]. The fresh counts are 259/300, 1,006/1,200 and 4,002/4,800. The final interval is [82.29%, 84.42%]. The 150 m union estimate still extrapolates from training distances no greater than 120 m. The intervals quantify simulation precision conditional on the data and model. [Original deletion analysis](distance-deletion.md)

From the repository root, run `python distance_deletion_mc.py --data "<attachment directory>/date"`. The command reads the archived baseline CSV and regenerates only the Monte Carlo audit table.
