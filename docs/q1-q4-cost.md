# Cost-sensitive Q1-to-Q4 monitoring

The same 105 FalseBay holdouts are scored under each of two passing sets from the archived common gross cutoff. The primary set is two-voice alone, as at 100 m under 20% coupled loss. The other set is modulated or two-voice, as at clean 100 m or coupled 50 m. The three probability rules use summed multinomial probabilities, separate binary logistic fits, or a proportional-odds fit with flat, modulated and two-voice in that order. All five ordinal fits converged and their probabilities are nested on every holdout. [Frozen protocol](model-spec.md#q1-to-q4-cost-sensitive-monitoring-freeze)

| Equal costs | Two-voice only false / missed passes | Modulated or two-voice false / missed passes |
|---|---:|---:|
| Archived hard logistic | 6 / 19 | 21 / 31 |
| Archived hard XGBoost | 10 / 18 | 20 / 24 |
| Multinomial | 4 / 21 | 29 / 21 |
| Binary logistic | 5 / 21 | 30 / 20 |
| Proportional odds | 5 / 20 | 28 / 20 |

At equal costs in the primary scenario, multinomial and proportional odds both tie hard logistic at 25 errors. Binary logistic makes 26. Every paired date-bootstrap cost contrast with either hard rule includes zero. The frozen improvement criterion is a strictly negative upper 95% cost-difference bound against both hard rules. No candidate meets it, so the published monitoring conclusion and six-feature classification benchmark are retained. [All decision counts and costs](../results/q1_q4_cost_decisions.csv) · [All paired cost contrasts](../results/q1_q4_cost_contrasts.csv)

When a false pass costs three times a missed pass, primary multinomial and binary rules both reduce mean cost from 0.352 to 0.200 relative to hard logistic by declaring every recording a nonpass. They miss all 21 passes. When a missed pass costs three times a false pass and the broader passing set applies, both rules give 43 false and four missed passes, lowering mean cost to 0.524 from 1.086 for hard logistic and 0.876 for hard XGBoost. Their paired intervals against each baseline lie below zero in that sensitivity. At the same cost ratio with the narrower passing set, proportional odds gives 24 false and 11 missed passes. Its interval against each hard rule includes zero.

| Probability model | Two-voice Brier / log loss | Broader set Brier / log loss |
|---|---:|---:|
| Multinomial | 0.16981 / 0.51638 | 0.28877 / 0.82684 |
| Binary logistic | 0.17028 / 0.51641 | 0.28243 / 0.80430 |
| Proportional odds | 0.17779 / 0.54608 | 0.28199 / 0.80854 |

Multinomial has the lowest point scores on the primary task. For the wider set, proportional odds has the lowest Brier score and binary logistic the lowest log loss. These are held-out point scores. The cost intervals resample dates with fixed forecasts and Q4 pass sets. Results apply to those modeled settings and stipulated costs. [Probability scores](../results/q1_q4_cost_scores.csv) · [Held-out predictions](../results/q1_q4_cost_predictions.csv)

```sh
python main.py --data "<attachment directory>/date" --output generated --q1-q4-cost
```

[Independent verification](../reviews/q1-q4-cost-verification.md)
