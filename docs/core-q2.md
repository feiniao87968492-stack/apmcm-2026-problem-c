# Q2 core propagation comparison

The target is equal-weight available-case correlation across the spectrogram, amplitude spectrum and envelope at the seven measured distances. The frequency-informed curve takes the form $A_c[1+(d/D_c)^{g_c}10^{\alpha_c(d-1)/10}]^{-1/2}$. The call-specific ceiling, scale and effective spreading exponent are fitted. The fixed atmospheric term uses the pure-tone equations in ISO 9613-1:1993, with 20 °C, 70% relative humidity, 101.325 kPa and Data01 median peak frequency by call type. Frequencies are 916 Hz for flat, 831 Hz for modulated and 829.5 Hz for two-voice, corresponding to 1.190, 1.107 and 1.105 dB of modeled atmospheric attenuation between 1 and 256 m. The peak frequency is a type-level proxy for a broadband sound. The measurements provide correlations and lack calibrated received levels, verified acquisition groups and links to the individual Data01 recordings. The environmental values and absorption law enter as physical assumptions. [Frozen specification](model-spec.md#q2-frequency-informed-core-propagation-freeze) · [Atmospheric inputs](../results/core_q2_absorption.csv)

| Model | Pooled interior RMSE | Pooled forward RMSE at 128/256 m |
|---|---:|---:|
| Isotonic | 0.06816 | 0.24843 |
| Fixed exponent | 0.06034 | 0.11583 |
| Shared exponent | 0.05526 | 0.11236 |
| Separate exponents | 0.04677 | 0.10859 |
| Log-exponent penalty 0.0025 | **0.04547** | 0.10703 |
| Log-exponent penalty 0.01 | 0.04956 | 0.11067 |
| Log-exponent penalty 0.04 | 0.05330 | 0.11190 |
| Penalty 0.01 with frequency-informed absorption | 0.04899 | **0.10564** |

Interior folds hold out one of the five interior distances at a time. Forward folds use only shorter distances, with isotonic extrapolation at its last fitted knot. The selected 0.0025 penalty has the smallest interior point RMSE among models meeting the frozen rule. Its paired RMSE changes versus isotonic are −0.02269 [−0.02368, −0.02179] interior and −0.14140 [−0.14681, −0.13674] forward. The frequency-informed fit improves on its matched 0.01 ablation by −0.00057 [−0.00070, −0.00043] interior and −0.00503 [−0.00528, −0.00471] forward. The latter fit has the lowest forward RMSE, while the frozen rule selects using interior RMSE among qualifying fits. Residual forward errors are material. For instance, the selected fit overpredicts two-voice fidelity at 256 m by 0.203 when fitted on shorter distances. At 128 m the two-voice target uses 190 of 300 rows per representation. Intervals are 95% percentiles over the same 300 wide-row resamples as the published forward comparison, conditional on available rows and unknown acquisition groups. The candidate penalties and the distance holdouts have been used in earlier work on these data. [Validation scores](../results/core_q2_scores.csv) · [Paired differences](../results/core_q2_comparisons.csv) · [Signed errors](../results/core_q2_holdouts.csv) · [Held-out row counts](../results/core_q2_support.csv)

The selected full-data curve crosses 0.50 at **84.5, 143.9 and 173.2 m** and 0.70 at **43.2, 85.0 and 99.4 m** for flat, modulated and two-voice calls. The isotonic values are 84.7, 144.6 and 169.7 m at 0.50 and 35.4, 77.7 and 79.3 m at 0.70. All twelve crossings occur inside the measured range. [Decision table](../results/core_q2_decision.csv) · [Full fitted curves](../results/core_q2_curves.csv) · [Threshold crossings](../results/core_q2_radii.csv) · [Figure 2 data](../results/core_q2_propagation.csv)

The Q2 entry point writes the scores, decision, curves, radii and figure to the selected output directory.

    python main.py --data "<attachment directory>/date" --output generated --core
