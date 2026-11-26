# Q4 decision analyses

The [frozen specification](model-spec.md#q4-decision-analysis-freeze) is at d18ff9a. The implementation and all three tables are at c1e1ee8. All scenario estimates use the full playback model standardized to eight birds and empirical context frequencies.

## Dual criterion

The criterion requires fidelity of at least 0.50 and a natural-minus-control response probability of at least 0.20 in the same draw. At 80% support, it passes 26 of 45 settings, compared with 19 under the product rule. All seven disagreements pass only the dual criterion. The same seven disagreements occur at excess thresholds of 0.10 and 0.30.

| Call and distance | Loss and response link | Dual support | Product support |
|---|---|---:|---:|
| Modulated, 100 m | 10%, acoustic-only | 100.0% | 78.0% |
| Two-voice, 150 m | 10%, acoustic-only | 100.0% | 79.7% |
| Modulated, 100 m | 10%, coupled | 99.3% | 61.7% |
| Two-voice, 150 m | 10%, coupled | 100.0% | 65.3% |
| Flat, 50 m | 20%, acoustic-only | 100.0% | 72.7% |
| Flat, 50 m | 20%, coupled | 100.0% | 16.0% |
| Two-voice, 100 m | 20%, coupled | 100.0% | 61.3% |

The dual thresholds are exploratory and the product remains the operational reference. The differences show how the decision changes when separate minimums are required for fidelity and response advantage. [All results and marginal counts](../results/decision_q4_dual.csv)

## Crossed variance of the product margin

Crossing 300 propagation draws with 300 playback draws gives 90,000 margins per setting, each with its recomputed common cutoff. Across the 18 call, distance and loss settings, the behavior share is 99.79–99.97%. The interaction share is at most 0.0038%. These are shares of variation in the fitted product-minus-cutoff margin under the existing resampling assumptions. The predominance of behavior variation supports collecting more matched playback data, especially near the far edge of the sampled domain. Record acquisition identifiers and paired fidelity measurements to assess how much propagation variation the current files capture. [Absolute variances and shares](../results/decision_q4_variance.csv)

## Matched-playback allocation and precision

The trial has six call-by-distance cells and two equally sized noise arms per cell. An independently sampled group receives both natural and control stimuli in counterbalanced order. The noise contrast is estimated separately in each cell as the elevated-minus-reference difference in the natural-minus-control response gap. Planning uses the clean fitted probabilities in both arms. The two arms are independent and outcomes within a pair may be correlated.

The exact minimax allocation under zero within-pair covariance is ten pairs per noise arm in every cell, identical to the equal allocation. All 120 pairs are assigned and the five-per-arm minimum is met. Flat calls at 100 m give the largest variance under all three planning correlations.

| Planning within-pair correlation | Worst standard error | Worst normal 95% half-width | Reduction versus equal |
|---|---:|---:|---:|
| −0.25 | 0.283 | 0.554 | 0.000 |
| 0 | 0.256 | 0.502 | 0.000 |
| +0.25 | 0.227 | 0.445 | 0.000 |

Correlations are clipped to the feasible Bernoulli covariance range for each cell. The half-widths use the normal approximation under the working probabilities. The 120-pair budget provides coarse precision for noise contrasts estimated within individual cells. [Cell counts, covariance and precision](../results/decision_q4_trial.csv)
