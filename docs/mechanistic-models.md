# Weather, vocal information and group response

The analysis rules were fixed before fitting at [311c3c4](https://github.com/feiniao87968492-stack/apmcm-2026-problem-c/commit/311c3c4a1ae7db840a19205d5d3bd30355c15118). The full choices, scoring rules and seeds are in the [model specification](model-spec.md#weather-call-dependent-distance-and-response-mechanisms).

## Q2 atmospheric variability

ERA5 provides 3,660 simultaneous temperature, humidity and surface-pressure vectors for June–July daytime conditions in False Bay across 2013–2022. Those hours span 9.8–21.5 °C, 44–100% relative humidity and 100.06–103.77 kPa. The calibration uses 142 possible calm daytime hours in December 2021 near Brandvlei Dam. Each of the 300 wide-row refits draws a possible dam weather vector. The 10,000 Monte Carlo scenarios pair a refit with a False Bay hour. The same atmospheric draw is used for all three calls. Temperature, humidity and pressure jointly change the ISO 9613-1 absorption at the observed call-type median Q50. The effective spreading term and correlation ceiling are carried from the dam fit to False Bay within each scenario. [Weather data and provenance](../sources/weather/README.md)

| 0.50 fidelity radius (m) | Fixed reference | Weather only, median [P5, P95] | Weather and fit, median [P5, P95] |
|---|---:|---:|---:|
| Flat | 85.0 | 85.6 [85.3, 85.8] | 85.7 [84.3, 87.3] |
| Modulated | 144.3 | 145.7 [145.1, 146.2] | 145.9 [143.7, 149.0] |
| Two-voice | 173.6 | 175.1 [174.4, 175.7] | 175.2 [173.3, 177.9] |

The 0.50 weather-only median changes by 0.6–1.5 m against the fixed-weather reference. The earlier 128 m truncation changed the two-voice crossing by 62.1 m. The short weather ranges reflect the effect of molecular absorption at these frequencies. The scenario draws hold the propagation form fixed and leave wind, waves, refraction and changes in ambient noise outside the atmosphere term. The lower quantile is a planning distance under the assumed simulation. All acoustic crossings are between 4 and 256 m. [All thresholds, row-only control and support counts](../results/mechanistic_q2_radii.csv) · [Earlier distance leverage check](../results/q2_256m_sensitivity.csv)

## Q3 call type and distance

We let natural call type shift the rank-one response tilt at 50 m and change its slope against log distance. Controls share the sea-wave stimulus in every model. The two orthonormal contrasts pool the three call types toward a common curve. Inner date and track-purged folds select shrinkage. The outer folds assess the model on new dates and tracks. The ordinary outer folds selected the strongest of the four interaction penalties on seven of twelve dates. [Fold settings](../results/mechanistic_q3_folds.csv)

| Rank-one model | Ordinary mask log loss | Ordinary Brier | Distant mask log loss | Distant Brier |
|---|---:|---:|---:|---:|
| Common across call types | 1.1010 | 0.1636 | 1.1504 | 0.1917 |
| Call-type main effects | 1.1150 | 0.1691 | 1.1565 | 0.2004 |
| Call type by distance | 1.1164 | 0.1697 | 1.1575 | 0.1978 |

The interaction changes ordinary mask log loss by +0.0155 [0.0044, 0.0275] versus the common curve. Against the main-effects fit the change is +0.00145 [−0.00249, 0.00659]. The distant comparison uses 33 trials with a playback arm at least 125 m away and training pairs strictly below 125 m. The adopted behavior model pools call types at matched covariates. The trial records support the pooled prediction for this specification. [Paired scores](../results/mechanistic_q3_scores.csv) · [Predictions at representative distances](../results/mechanistic_q3_probabilities.csv)

## Q4 entropy-based noise coupling

VR1–VR19 code recorded sequential group replies. Four observed codes are retained, including modflat. There is no caller identity in the sequence. Sixty natural trials supply 214 adjacent transitions, and four control trials supply 17. We weight each natural trial equally, estimate the probability of the next reply given the previous reply and the played call, then shrink each row toward pooled reply behavior. The fitted conditional mutual information is 0.0331 bit per transition under the smoothed distribution. The comparable predictive gain averages 0.0082 bits per transition after averaging within each held-out trial (95% date interval −0.0651 to +0.0709). [Transition probabilities](../results/mechanistic_vr_transitions.csv) · [Entropy decomposition](../results/mechanistic_vr_information.csv) · [Held-out scores](../results/mechanistic_vr_scores.csv)

The modeled background power rises by a factor M at the receiver. With acoustic ceiling A and current-weather fidelity F, the additive-noise model gives \(F_M=A[1+M((A/F)^2-1)]^{-1/2}\). The erasure mechanism assumes that the call-specific cue survives with probability \(r=(F_M/F)^2\), the relative explained-variance fraction. The next-reply law then mixes the call-specific transition and the pooled transition with weights r and \(1-r\). We hold the distribution of previous reply codes fixed within a played call. The KL divergence from the mixed transition to the pooled transition, averaged over previous replies, gives information \(I_c(r)\). Its retained share \(I_c(r)/I_c(1)\) multiplies the positive natural-minus-control 30 s response excess. The share lies between zero and r by convexity of KL divergence. The acoustic-only scenario sets behavioral retention to one.

The following medians [P5, P95] require 0.50 fidelity and 0.50 natural response probability by 30 s at every half-metre step from 20 m. The fit standardizes to eight birds and the recorded context proportions. Q2 weather and refit draws are propagated jointly while the behavior and transition fits are held at their point estimates.

| Call | Clean | +3 dB, acoustic only | +3 dB, entropy transfer | +6 dB, acoustic only | +6 dB, entropy transfer |
|---|---:|---:|---:|---:|---:|
| Flat | 85.5 [84.0, 87.0] | 63.0 [62.0, 64.0] | 38.5 [37.5, 39.0] | 46.5 [45.5, 47.5] | 24.5 [24.0, 25.0] |
| Modulated | 145.5 [143.5, 149.0] | 115.5 [113.5, 118.0] | 68.0 [66.5, 69.0] | 91.5 [90.0, 93.5] | 49.5 [48.5, 50.5] |
| Two-voice | ≥150 across all draws | 146.0 [144.5, 148.0] | 93.0 [92.0, 94.0] | 122.0 [120.5, 123.0] | 73.5 [72.5, 74.5] |

For two-voice calls at +3 dB the same draws give a median reduction of 53.0 m [52.0, 54.5] from the acoustic-only model to the entropy-transfer model. The difference quantifies the imposed behavioral mechanism. Data02 supplies sequences from the natural playback protocol. It has no paired observations under measured receiver noise to estimate the erasure or information-to-response transfer. The two scenarios therefore have conditional weather ranges and their difference measures structural sensitivity. The gross effectiveness index applies the same retention to the 60 s response excess and uses the released cutoff 0.287598. For two-voice, the +3 dB gross radius medians are 137.3 m with acoustic loss alone and 106.6 m with entropy transfer. The original 20% coupled case remains available in the earlier comparison. [Radius and retention tables](../results/mechanistic_q4_radii.csv) · [Radius plot](../results/mechanistic_ranges.png) · [Earlier scenarios](core-q4.md)

## First response in groups

The first observed response is the minimum of the birds' onset times. We fit group onset bins through 60 s, including zero-time events and a separate no-event bin. We compare conditional independence at given covariates with a shared Gamma trial frailty of variance one. In both models the conditional group cumulative hazard is proportional to \(n^\kappa\). A fixed \(\kappa=1\) gives equal per-bird response rates across group sizes at matched covariates. A free \(\kappa\) allows the recorded rate per bird to vary with group size.

| Timing model | Held-date bin log loss | 30 s Brier | Singleton bin log loss |
|---|---:|---:|---:|
| Stimulus timing | 0.856 | 0.174 | 0.870 |
| Factorized 60 s risk and response-time distribution | 1.131 | 0.161 | 0.777 |
| Independence, fixed size exponent | 1.028 | 0.225 | 1.064 |
| Independence, fitted size exponent | 0.838 | 0.162 | 0.837 |
| Gamma frailty, fixed size exponent | 0.963 | 0.206 | 0.999 |
| Gamma frailty, fitted size exponent | 0.849 | 0.164 | 0.874 |

For independence, freeing the size exponent changes group bin log loss by −0.191 [−0.247, −0.124]. With shared frailty the change is −0.113 [−0.155, −0.065]. The fitted exponents are −0.31 and −0.35. The independence fit with a free exponent improves the stimulus timing benchmark by −0.018 in point bin log loss [−0.070, +0.038]. The factorization has the lowest 30 s Brier point score. Singleton results come from 30 held-out trials on eight dates. The group-size association may reflect group composition and behavior at matching recorded covariates. [Held-out scores and intervals](../results/mechanistic_latency_scores.csv)

At 100 m the Q4 30 s group probability of 0.577 is compatible with 0.82 expected distinct responders under conditional independence and 1.18 with shared Gamma frailty. For this comparison we invert the group risk at the same covariates within each context before averaging. The group-risk bound is [0.577, 4.617]. The timing data give the first response and lack onset times and identities for the other birds. The example quantifies how the projected individual count depends on an assumed correlation mechanism. [Same-risk individual projections](../results/mechanistic_latency_fixed_risk.csv) · [Projections from the four fitted models](../results/mechanistic_latency_responders.csv)

## Reproduce

The command reads the contest Data01–Data11 and the weather snapshot tracked in the repository. It also runs as part of the default entry point.

~~~sh
python main.py --mechanistic --data "/path/to/C-attachments" --output generated
~~~
