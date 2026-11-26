# Q4 distance deletion

The protocol froze at `ddb3e30` and ran at `61b8151`. A pair was flagged if either arm was 125–175 m inclusive or farther than 175 m, according to the selected band. Both flags selected 14 pairs each, with two pairs in common. The union removed 26 pairs. All four fits use the same full-data context weights, acoustic draws and clean gross and own-net cutoffs. [Pair overlap](../results/distance_deletion_overlap.csv)

| Fit | Retained pairs | Natural responses | Control responses | Clean gross support | Clean own-net support | Coupled gross support | Coupled own-net support |
|---|---:|---:|---:|---:|---:|---:|---:|
| Full | 139 | 90 | 18 | 73.3% | 90.7% | 17.3% | 49.7% |
| Drop 125–175 m | 125 | 81 | 17 | 64.7% | 88.7% | 14.7% | 38.3% |
| Drop above 175 m | 125 | 78 | 15 | 55.0% | 86.3% | 12.7% | 35.7% |
| Drop both bands | 113 | 71 | 14 | 46.0% | 79.7% | 8.7% | 30.0% |

Support in the last four columns is for two-voice at 150 m. The clean own-net decision passes with either band deleted on its own. Deleting both gives 239 of 300 draws at or above the cutoff, one draw short of the 80% rule. At 150 m the clean predicted natural/control probabilities move from 0.647/0.081 to 0.504/0.045 under union deletion. The paired margin differences are −0.078 [−0.115, 0.012] for gross and −0.058 [−0.089, 0.022] for own-net, with 95% date-acoustic percentile intervals. [Probabilities, margins and decisions](../results/distance_deletion_points.csv)

The three deletion comparisons change five decisions relative to the full fit. In addition to the union result at 150 m, near deletion changes the clean gross decision for modulated at 100 m (244 to 234 draws). Under coupling all three deletions change the two-voice own-net decision at 100 m (245 to 231, 223 and 214 draws). Every change is from passing to below the 80% rule. [Fixed-distance comparisons](../results/distance_deletion_points.csv)

Near deletion leaves no local trials within 25 m of 150 m. Far deletion leaves one local two-voice trial in each arm. Union deletion leaves observations only through 120 m overall, with two-voice natural and control maxima of 100 m and 120 m respectively. The 150 m prediction thus uses extrapolation under union deletion. The changes describe sensitivity to which pairs support the fit. [Training counts by arm and call](../results/distance_deletion_training.csv) · [Local coverage and retained ranges](../results/distance_deletion_coverage.csv)
