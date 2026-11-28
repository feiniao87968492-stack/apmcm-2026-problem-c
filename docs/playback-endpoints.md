# Head raising, timely response and external noise

The analysis specification froze at c9e0034. The comparison uses the released folds and planning thresholds. [Estimands, assumptions and validation](model-spec.md#head-raising-timely-response-and-external-noise-evidence)

## Head raising at matched playback distance and group size

The source study measured the recorded group span from the first bird raising its head to the last bird stopping, up to the observation limit of 60 s. The span includes any intervals between individual responses. A trial with zero seconds contributes zero to the group mean. The analysis compares every trial in the paired sample and reports positive spans separately. [Field protocol, Methods and Table 1](https://doi.org/10.12688/openreseurope.24618.1)

| Outcome, 49 matched pairs | Natural | Sea-wave control | Natural minus control [95% date interval] |
|---|---:|---:|---:|
| Trials with a positive span | 16/49 | 6/49 | +20.4 percentage points [12.2, 28.8] |
| Mean seconds per trial | 7.06 | 2.22 | +4.84 s [2.10, 7.80] |
| Mean seconds among responders | 21.63 | 18.17 | +3.46 s [−6.68, 15.76] |

The symmetric decomposition assigns 4.06 s [2.51, 5.39] to the difference in response frequency and 0.78 s [−1.44, 3.48] to the difference in positive spans. The conditional contrasts and decomposition use the 9,980 of 10,000 resamples with a responder in each arm. Across all 139 pairs the mean recorded contrast is 8.96 s [7.02, 11.08], with playback distances or group sizes differing within the other 90 pairs. Call-specific matched support is 16 flat, four modulated and 29 two-voice pairs. [Paired estimates](../results/q3_head_duration.csv) · [Sample support](../results/q3_head_duration_support.csv)

The hurdle predicts expected seconds as the product of the probability of head raising and the expected positive duration. The pooled version uses stimulus, distance, group size and context. The call-specific version adds two natural-arm call-type coefficients to each part. Across 278 held-out trials on 12 dates with shared tracks purged, MSE is 129.36 s² for the pooled hurdle, 129.03 s² for the call-specific hurdle and 144.71 s² for stimulus-arm means. The pooled difference is −15.35 s² [−26.36, −2.63]. The added call terms change the point score by only 0.32 s². The paired result supports a difference in recorded seconds per exposure and attributes most of it to occurrence. The conditional difference remains uncertain among the observed responders. [Prediction scores](../results/q3_head_duration_scores.csv) · [Held-out predictions](../results/q3_head_duration_oof.csv)

## Q2 influence of the 256 m observation

A refit of the same selected curve using 4–128 m predicts 0.472 for two-voice fidelity at 256 m, where the observed mean is 0.276. The 0.50 crossing moves from 173.6 to 235.7 m and the 0.60 crossing from 141.0 to 168.5 m. Both shorter-fit crossings extrapolate beyond 128 m. The shorter fit still exceeds 0.40 at 256 m. The flat 0.50 crossing moves by −0.9 m and the modulated crossing by +7.4 m. The shortened fit isolates the contribution of the far-distance knot. The dam measurements come from one calm campaign. [Crossings and forward errors](../results/q2_256m_sensitivity.csv) · [Propagation model and validation](core-q2.md)

## Q4 response by 30 seconds

The event is any of the three flagged responses by 30 s. The ordinary evaluation holds out 12 dates and purges shared natural tracks. The distant evaluation scores 33 arms at or beyond 125 m after additionally excluding from training any pair with an arm at those distances. [All scores and paired intervals](../results/q4_timely30_scores.csv) · [Held-out predictions](../results/q4_timely30_oof.csv)

| Timing used for the 30 s event | Ordinary Brier | Ordinary log loss | Distant Brier | Distant log loss |
|---|---:|---:|---:|---:|
| Direct stimulus-only frequency | 0.1742 | 0.5272 | 0.1531 | 0.4879 |
| Released stimulus-only timing | 0.1742 | 0.5273 | 0.1523 | 0.4849 |
| Released distance-dependent factorization | 0.1606 | 0.4972 | 0.1919 | 0.5775 |
| Direct covariate logistic | 0.1642 | 0.5066 | 0.2152 | 0.6413 |

Against direct stimulus-only frequencies, the factorized model's ordinary Brier difference is −0.0135 [−0.0294, +0.0041]. The direct covariate model's difference is −0.0099 [−0.0270, +0.0088]. Both intervals cross zero. For the distant trials the direct model's Brier difference is +0.0621 [+0.0025, +0.1050]. These results quantify the effect of the behavioral-model choice on the 30 s planning criterion.

The joint rule requires fidelity and natural response probability of at least 0.50 at every half-metre step from 20 m. At eight birds and the released context mix, the four response predictions give the following endpoints with the selected acoustic fit and hypothetical 20% coupled loss.

| Call | Last distance meeting the rule under all four models (m) | Largest single-model endpoint (m) |
|---|---:|---:|
| Flat | 58.0 | 58.0 |
| Modulated | 81.5 | 107.0 |
| Two-voice | 81.5 | 132.0 |

The direct covariate model gives 87.0 m for both modulated and two-voice calls. Using the 4–128 m acoustic refit with factorized timing alone leaves both noisy endpoints at 81.5 m. It moves the flat endpoint from 58.0 to 56.0 m. The loss remains hypothetical and the ranges describe the tested model choices. [All radii and binding constraints](../results/q4_timely30_radii.csv) · [Model ranges](../results/q4_timely30_model_range.csv)

## Stony Point boat-noise experiment

The public dataset covers a separate onshore playback experiment. At each exposure stratum, we compare the same visible birds' share of scans in vigilance before and during motor-boat noise. Each video receives equal weight and the intervals resample videos within exposure stratum. The complete before/during records cover 67 birds in 18 videos. [Source study](https://doi.org/10.1016/j.scitotenv.2026.182372) · [Data and attribution](../sources/stony-point/README.md)

| Received exposure (dB re 20 µPa) | Videos | Birds | Increase in vigilance share [95% video interval] |
|---|---:|---:|---:|
| 61–64 | 7 | 24 | +44.5 percentage points [33.2, 58.0] |
| 67–70 | 5 | 22 | +43.3 percentage points [28.3, 55.4] |
| 73–76 | 6 | 21 | +48.4 percentage points [41.7, 56.9] |

The experiment documents vigilance during a boat-noise stimulus on land. Q4 needs the effects of measured receiver noise on call fidelity at sea and on the within-pair natural-minus-control response. Those quantities require paired call and control playbacks with receiver noise measured at the trial level. [Video-weighted estimates](../results/q4_stony_point_vigilance.csv) · [Availability of at-sea inputs](data-audit.md)

## Reproduce

Run the default pipeline or use the named analysis with the released core tables.

~~~sh
python main.py --playback-endpoints --data "/path/to/C-attachments" --output generated
~~~
