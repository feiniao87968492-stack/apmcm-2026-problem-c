# Final figure and noise agreement

Figure 2 uses the adopted shared-exponent attenuation fit, seven observed equal-weight correlations per call, and pointwise 95% intervals from the original 300 whole-row acoustic draws. Dashed lines show the archived isotonic curves. Horizontal guides at 0.40, 0.50 and 0.60 correspond to the thresholds in Table 2. [Figure](../results/physical_q2_curves.png) · [Plotted data](../results/physical_q2_curves.csv) · [Metadata](../results/physical_q2_curves.meta.json)

For each noisy setting, the intersection requires at least 80% attainment in all eight combinations of attenuation shape, response link and resampling scheme.

| Noise | All variants pass | All variants fail | Mixed |
|---|---:|---:|---:|
| 3 dB | 2 | 5 | 2 |
| 6 dB | 0 | 5 | 4 |
| Total | 2 | 10 | 6 |

Only modulated and two-voice calls at 50 m under 3 dB pass throughout. In clean conditions, five settings pass both sampling schemes, three fail both, and two-voice at 150 m passes only under experiment-pair resampling. The eight-variant intersection applies to the noisy settings. [Setting-level counts](../results/noise_q4_agreement.csv)

| Factor compared, other factors fixed | Both pass | Both fail | First variant only | Second variant only |
|---|---:|---:|---:|---:|
| Local noise-power / matched uniform | 15 | 47 | 10 | 0 |
| Acoustic-only / coupled | 15 | 47 | 10 | 0 |
| Experiment-pair / date-block | 18 | 50 | 4 | 0 |

The agreement summarizes the tested scenario assumptions. The mixed settings identify where measuring noise and playback response can clarify a protection decision. The two intersection passes support monitoring the relevant 50 m conditions, with site-specific limits requiring field evidence. [Matched comparisons by factor and noise level](../results/noise_q4_agreement_by_factor.csv)
