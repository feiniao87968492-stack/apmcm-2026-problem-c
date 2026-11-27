# Q2 partial pooling of attenuation exponents

Partial pooling retains call-specific ceilings and scales and penalizes the variance of log exponents. The three penalties were fixed before fitting. The comparison reuses the strictly shorter training distances and 300 paired wide-row draws from the forward study. The 128 and 256 m pool contains six equally weighted call-distance cells. [Frozen design](model-spec.md#q2-partial-pooling-of-attenuation-exponents-freeze)

| Fit | RMSE at 64 m | RMSE at 128 m | RMSE at 256 m | Pooled RMSE at 128 and 256 m |
|---|---:|---:|---:|---:|
| Shared | 0.12492 | 0.08434 | 0.13467 | 0.11236 |
| Separate | 0.30479 | 0.10586 | 0.11126 | 0.10859 |
| Lambda 0.0025 | 0.12497 | 0.08787 | 0.12326 | 0.10703 |
| Lambda 0.01 (primary) | 0.12490 | 0.08535 | 0.13119 | 0.11067 |
| Lambda 0.04 | 0.12491 | 0.08460 | 0.13374 | 0.11190 |

| Penalty | Pooled RMSE difference vs shared [paired 95% interval] | Pooled RMSE difference vs separate [paired 95% interval] |
|---|---:|---:|
| 0.0025 | -0.00532 [-0.00726, -0.00333] | -0.00156 [-0.00849, 0.00323] |
| 0.01 (primary) | -0.00169 [-0.00233, -0.00102] | +0.00208 [-0.00509, 0.00712] |
| 0.04 | -0.00045 [-0.00063, -0.00027] | +0.00331 [-0.00400, 0.00837] |

The primary setting meets the comparison criterion against the shared exponent only. The three penalties reduce the large separate-exponent error at 64 m to levels close to the shared fit. For flat calls at 64 m, the signed errors are -0.50113 for separate exponents, -0.00537 at the primary penalty and -0.00150 for the shared exponent. The primary penalty's pooled signed errors at 64, 128 and 256 m are -0.10373, +0.08324 and +0.10013. [All signed errors](../results/q2_partial_pooling_holdouts.csv) · [Scores](../results/q2_partial_pooling_scores.csv) · [Paired comparisons](../results/q2_partial_pooling_contrasts.csv)

| Full fit | Exponents (flat / modulated / two-voice) | Radii at 0.50 (m) | Radii at 0.70 (m) |
|---|---|---|---|
| Shared | 2.858 / 2.858 / 2.858 | 88.31 / 142.86 / 167.22 | 49.49 / 81.95 / 81.27 |
| Separate | 2.175 / 3.056 / 4.437 | 83.33 / 143.89 / 176.71 | 41.08 / 85.12 / 106.93 |
| Lambda 0.0025 | 2.334 / 3.049 / 3.918 | 84.52 / 143.85 / 173.24 | 43.16 / 85.02 / 99.42 |
| Lambda 0.01 (primary) | 2.555 / 2.995 / 3.386 | 86.15 / 143.58 / 170.08 | 45.93 / 84.17 / 90.89 |
| Lambda 0.04 | 2.747 / 2.915 / 3.029 | 87.53 / 143.16 / 168.11 | 48.22 / 82.89 / 84.52 |

All full-fit radii in the table cross within the measured distance domain. At 0.70 the primary penalty gives a two-voice radius between the two endpoint estimates. These are point radii from the full data. The paired prediction intervals condition on available rows and the wide-row resampling convention with unknown acquisition groups. The distances already motivated this follow-up. The frozen two-comparator rule leaves the existing interpretation of forward prediction in place. [Full and fold-specific fits](../results/q2_partial_pooling_fits.csv)

```sh
python main.py --data "<attachment directory>/date" --output generated --q2-partial-pooling
```

[Independent numerical review](../reviews/q2-partial-pooling-verification.md)
