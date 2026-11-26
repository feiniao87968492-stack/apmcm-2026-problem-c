# Vocal counts and contact scenarios

The protocol froze at `4652deb` and ran at `6212e85`. The field study recorded group calls for 60 seconds before playback and 60 seconds from onset. Counts were available in both windows and arms for all 139 pairs, including 49 at equal recorded distance and group size. [Field study](https://doi.org/10.12688/openreseurope.24618.1)

| Pairs | Natural post minus pre | Control post minus pre | Difference in changes [95% date interval] |
|---|---:|---:|---:|
| All 139 | 1.914 | −0.065 | 1.978 [1.682, 2.351] |
| 49 matched | 1.776 | 0.102 | 1.673 [1.308, 2.168] |

The unit is group calls per minute. Counts can include repeated calls from the same bird. The count increase and the scored `VocalYesNo` coincide in every trial, with 76 natural and five control positives. Positive post-onset counts give 78 natural and seven control positives, including two cases per stimulus without an increase. [Pair contrasts](../results/vocal_count_pairs.csv) · [Count audit](../results/vocal_count_audit.csv)

| Strictly held-out model | Mean Poisson deviance | MAE (calls) |
|---|---:|---:|
| Stimulus means | 2.520 | 1.269 |
| Full Poisson | 2.370 | 1.145 |
| Full Poisson plus pre-playback count | 2.194 | 1.181 |

Full Poisson versus stimulus means lowers MAE by 0.124 calls (95% paired date interval [−0.223, −0.023]), while the deviance change of −0.150 spans zero [−0.458, 0.189]. Adding pre-playback count changes deviance by −0.176 [−0.709, 0.197] and MAE by +0.035 [−0.067, 0.132] relative to full Poisson. The frozen joint rule retains stimulus means. [Fold scores](../results/vocal_count_folds.csv) · [Score comparisons](../results/vocal_count_scores.csv)

With the same eight-bird standardization and paired acoustic and date draws, replacing any response with a strict call-count increase preserves the 80% decision in all 18 settings under the joint fidelity and response-excess rule. Six pass in clean conditions and four under 20% linked loss. The largest change in joint attainment is at 50 m for modulated calls under linked loss, from 100% to 95%. There the fitted natural-minus-control gap changes from 0.442 to 0.366. The comparisons depend on the fitted behavioral probabilities and the scenario. The grid ends at the 150 m support boundary. [Probabilities, intervals and decisions](../results/vocal_contact_q4.csv) · [Local coverage](../results/vocal_contact_coverage.csv)
