# Score-guided manual review for Q4

The review queues use archived scores for 105 FalseBay holdouts. A selected recording is assumed to receive perfect, equally costly human review. Only reviewed positives are confirmed. Unreviewed recordings remain unresolved. The labels are defined by the archived Q4 gross-score scenarios. The primary comparison uses multinomial ranking for 25 reviews at 100 m under 20% coupled loss, when only two-voice passes. [Frozen specification](model-spec.md#q4-score-guided-manual-review-freeze)

| Passing set | Reviews | Random | Training prevalence | Multinomial | Binary | Proportional odds |
|---|---:|---:|---:|---:|---:|---:|
| Two-voice | 10 | 2.00 | 1.90 | 3 | 2 | 1 |
| Two-voice | 25 | 5.00 | 4.36 | 3 | 4 | 5 |
| Two-voice | 50 | 10.00 | 7.47 | 13 | 13 | 11 |
| Modulated or two-voice | 10 | 5.81 | 4.76 | 8 | 8 | 5 |
| Modulated or two-voice | 25 | 14.52 | 11.89 | 19 | 19 | 17 |
| Modulated or two-voice | 50 | 29.05 | 24.71 | 31 | 30 | 32 |

The entries are expected confirmed positives. Random review has yield equal to the review fraction times the positive count. When a score tie straddles the budget, each tied row gets the same chance of occupying a remaining slot. The primary multinomial rule finds 3 of 21 positives (14.3%). Its excess yield is −2.00 versus random (paired 95% interval −3.03 to 3.22) and −1.36 versus training prevalence (−4.79 to 5.66). Neither lower endpoint exceeds zero, so the frozen criterion for a primary ranking advantage is unmet. [All yields and shares](../results/q4_score_review_yield.csv) · [Paired intervals](../results/q4_score_review_contrasts.csv)

At 50 reviews on the primary passing set, multinomial ranking finds 13 positives versus a random expectation of 10. Its paired excess interval includes zero. On the wider set at 25 reviews, binary ranking finds 19 positives, with an excess of 7.11 over prevalence (95% interval 0.49 to 14.76) and 4.48 over random (−0.60 to 8.56). These are sensitivity comparisons.

The paired intervals use 300 date-block resamples with fixed forecasts. Each resampled budget is the original review fraction times the resampled size, rounded to the nearest integer with halves rounded up. The analysis conditions on scenario-defined labels and ideal review, with field performance still to be validated.

```sh
python main.py --data . --output generated --q4-score-review
```

The command uses the committed probabilities and training prevalences. [Independent verification](../reviews/q4-score-review-verification.md)
