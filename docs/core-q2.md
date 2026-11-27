# Q2 core propagation comparison

The target is equal-weight available-case correlation across the spectrogram, amplitude spectrum and envelope at the seven measured distances. The frequency-informed curve takes the form $A_c[1+(d/D_c)^{g_c}10^{\alpha_c(d-1)/10}]^{-1/2}$. The call-specific ceiling, scale and effective spreading exponent are fitted. The atmospheric term uses the pure-tone equations in ISO 9613-1:1993 at assumed 20 ?C, 70% relative humidity and 101.325 kPa. We use the Data01 type-specific medians of peak frequency (Fpeak) and spectral median (Q50) as proxies for a broadband signal. The Fpeak medians are 916, 831 and 829.5 Hz for flat, modulated and two-voice calls. The Q50 medians are 908, 864.5 and 844.5 Hz and imply 1.182, 1.140 and 1.120 dB of modeled atmospheric attenuation between 1 and 256 m. The measurements provide correlations and lack calibrated received levels, verified acquisition groups and links to the individual Data01 recordings. [Frozen specification](model-spec.md#antigravity-3-q2-freeze) ? [Atmospheric inputs](../results/core_q2_absorption.csv)

| Model | Pooled interior RMSE | Pooled forward RMSE at 128/256 m |
|---|---:|---:|
| Isotonic | 0.06816 | 0.24843 |
| Fixed exponent | 0.06034 | 0.11583 |
| Shared exponent | 0.05526 | 0.11236 |
| Separate exponents | 0.04677 | 0.10859 |
| Log-exponent penalty 0.0025 | 0.04547 | 0.10703 |
| Log-exponent penalty 0.01 | 0.04956 | 0.11067 |
| Log-exponent penalty 0.04 | 0.05330 | 0.11190 |
| Penalty 0.01 with Fpeak absorption | 0.04899 | 0.10564 |
| Penalty 0.0025 with Fpeak absorption | 0.045322 | 0.102622 |
| **Penalty 0.0025 with Q50 absorption** | **0.045319** | **0.102486** |

Interior validation holds out one of five interior distances at a time. Forward fits use only shorter distances, with isotonic carrying its last fitted knot forward. Both new absorption candidates qualify under the frozen rule. Q50 gives the smallest point interior RMSE, closely followed by Fpeak. The selected fit changes paired RMSE versus isotonic by ?0.02284 [?0.02376, ?0.02200] for interior validation and ?0.14595 [?0.15121, ?0.14142] for forward validation. Against the matched no-absorption 0.0025 fit, the corresponding changes are ?0.00015 [?0.00024, ?0.00004] and ?0.00455 [?0.00482, ?0.00422]. The Fpeak counterpart changes RMSE against that same ablation by ?0.00014 [?0.00024, ?0.00004] and ?0.00441 [?0.00468, ?0.00409]. These intervals use the same 300 paired wide-row resamples as the prior comparison and condition on available rows and unknown acquisition groups. The selected fit still overpredicts two-voice fidelity at 256 m by 0.196 when fitted on shorter distances. At 128 m each two-voice representation has 190 of 300 rows. [Validation scores](../results/core_q2_scores.csv) ? [Paired differences](../results/core_q2_comparisons.csv) ? [Signed errors](../results/core_q2_holdouts.csv) ? [Held-out row counts](../results/core_q2_support.csv)

The selected curve gives the radii below in flat, modulated and two-voice order, with 95% percentile intervals from the 300 existing wide-row refits.

| Fidelity threshold | Flat (m) | Modulated (m) | Two-voice (m) |
|---|---:|---:|---:|
| Potential 0.40 | 112.2 [111.1, 113.5] | 178.8 [177.0, 181.0] | 207.8 [206.3, 209.2] |
| Standard 0.50 | 85.0 [83.9, 86.2] | 144.3 [142.4, 146.5] | 173.6 [172.5, 174.7] |
| Reliable 0.60 | 63.2 [62.0, 64.6] | 114.7 [112.9, 117.0] | 141.0 [140.0, 142.0] |
| Sensitivity 0.70 | 42.8 [41.6, 44.4] | 84.4 [82.7, 86.5] | 98.6 [97.2, 100.0] |

All 12 point crossings and all 3,600 draw crossings fall within 4?256 m. The export records boundary flags and counts for the selected curve. The archived isotonic values are 84.7, 144.6 and 169.7 m at 0.50 and 35.4, 77.7 and 79.3 m at 0.70. [Frozen reporting rule](model-spec.md#core-contest-reporting-thresholds-and-respondent-timing-freeze) ? [Decision table](../results/core_q2_decision.csv) ? [Threshold crossings](../results/core_q2_radii.csv) ? [Figure 2 data](../results/core_q2_propagation.csv)

The Q2 entry point writes the scores, decision, curves, radii and figure to the selected output directory.

    python main.py --data "<attachment directory>/date" --output generated --core
