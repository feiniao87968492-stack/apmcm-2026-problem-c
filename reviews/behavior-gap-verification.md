# Independent verification of Q3 response-gap decomposition

I used the specification frozen at 9795561. I reconstructed the masks from the three behavior indicators in Data02, indexed both stimuli by experiment ID, and verified that the paired rows shared dates. I reconstructed the 12-date draws using seed 20261128. I rebuilt the recorded and target designs and refitted the same regularized multinomial model independently on the full dataset and every date resample. I averaged eight-mask probabilities over the observed natural-context distribution before conditioning on any positive mask. The verifier imports no project modules.

The full-data predictions match the archived eight mask probabilities, marginal natural-minus-control mask contrasts, any-response probabilities and all three event marginals at the representative distances within \(10^{-12}\). The reconstructed local trial and responder denominators match the Q3 support table. [Archived masks](../results/q3_predicted_masks.csv) · [Archived contrasts](../results/q3_predicted_mask_contrasts.csv) · [Archived local support](../results/q3_representative_response_support.csv) · [Archived event marginals](../results/q3_representative_latency.csv)

I computed each component independently as the mean of its changes in the two possible reference-arm orders, then verified the sum against every defined marginal gap. I compared all 20 raw and 90 standardized rows, including point probabilities, component estimates, percentile endpoints, valid draw counts and observed counts. The maximum absolute differences were \(2.22\times10^{-16}\) for the raw rows and \(1.83\times10^{-14}\) for the standardized rows. All counts agreed exactly. All 300 draws were valid for both the marginal gaps and the decompositions in each reported comparison. [Raw results](../results/behavior_gap_raw.csv) · [Standardized results](../results/behavior_gap_standardized.csv)

| Sample | Natural/control responders | Behavior | Gap | Response frequency | Responder composition [95% date interval] |
|---|---:|---|---:|---:|---:|
| 139 pairs | 90/18 | Head raising | 0.302 | 0.345 | −0.043 [−0.121, 0.020] |
| 139 pairs | 90/18 | Vocalizing | 0.511 | 0.291 | 0.220 [0.145, 0.308] |
| 139 pairs | 90/18 | Approach | 0.165 | 0.066 | 0.099 [0.074, 0.131] |
| 49 matched pairs | 33/8 | Head raising | 0.204 | 0.315 | −0.111 [−0.244, 0.022] |
| 49 matched pairs | 33/8 | Vocalizing | 0.551 | 0.288 | 0.263 [0.116, 0.400] |
| 49 matched pairs | 33/8 | Approach | 0.184 | 0.070 | 0.114 [0.066, 0.175] |

At the nine standardized settings, the head-raising composition term is negative in every point estimate, while vocalizing and approach composition are positive. Within 25 m of 150 m the eight natural and eight control trials contain only one approach, for modulated natural playback. The components are descriptive measures of group responses.

## Reproduction

I ran the following commands from the repository root with temporary verifier and comparator scripts. One reconstructs the output independently and the other checks the released tables by explicit export keys.

~~~powershell
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-gap-independent.py" . "<attachment directory>/date" "$env:TEMP/apmcm-gap-independent"
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-gap-compare.py" "$env:TEMP/apmcm-gap-independent" results
~~~
