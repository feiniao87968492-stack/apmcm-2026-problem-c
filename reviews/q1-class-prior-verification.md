# Independent verification of Q1 class-prior decisions

**Pass.** I independently reconstructed the five folds from Data01 and the group IDs specified in the freeze. The 108 rows match the archived row numbers, class labels, group IDs, folds and baseline decisions exactly. The unweighted training-fold scaler serves all four comparisons. The inverse-frequency weights average one in each training fold. [Baseline predictions](../results/q1_oof_predictions.csv) · [Frozen protocol](../docs/model-spec.md#q1-class-prior-decision-comparison-freeze)

I fitted both multinomial regressions with scikit-learn 1.7.2. The scratch verifier used log-scale prior corrections, per-group confusion matrices for paired resampling, and direct average precision from the ranked held-out probabilities. All 300 seed-20261126 resamples retained all three classes. Against production commit `2628c4c4dcd083f4481c15513942d16b06170588`, all 432 hard predictions match exactly. Fold priors, baseline probabilities and the numerical metrics agree to absolute tolerance of 1e-14. [Prediction rows](../results/q1_class_prior_predictions.csv) · [Metrics](../results/q1_class_prior_metrics.csv)

| Decision rule | Macro F1 | Paired F1 change (95% interval) | Recall flat / modulated / two-voice | Two-voice precision | Two-voice true / false positives |
|---|---:|---:|---:|---:|---:|
| Original logistic | 0.314408 | Reference | 0.523 / 0.375 / 0.083 | 0.250 | 2 / 6 |
| Divide by square root of prior | 0.290810 | −0.023598 [−0.078072, 0.025427] | 0.477 / 0.325 / 0.083 | 0.100 | 2 / 18 |
| Divide by prior | 0.335185 | +0.020777 [−0.071496, 0.174686] | 0.432 / 0.325 / 0.250 | 0.200 | 6 / 24 |
| Inverse-frequency weighted refit | 0.326783 | +0.012375 [−0.073870, 0.168806] | 0.432 / 0.300 / 0.250 | 0.182 | 6 / 27 |

The original model's pooled two-voice average precision is 0.254730, with 24/108 = 0.222222 as the constant-score reference. The full correction keeps both originally correct two-voice labels and adds four correct and 18 incorrect ones. The half correction adds 12 incorrect labels. The weighted refit adds four correct and 21 incorrect labels. The full correction meets the recall condition, and its lower paired F1 bound is negative. Retain the original logistic decision. The other two intervals also span zero. These uncertainty intervals condition on fixed held-out predictions, and the equal target priors express a decision assumption. [Published metrics](../results/q1_class_prior_metrics.csv)

I ran the scratch verification from the repository root with Python 3.10.11, NumPy 2.2.6, pandas 2.3.3 and scikit-learn 1.7.2.

```powershell
$source = Get-ChildItem -LiteralPath "<attachment directory>/date" -Filter "Data01*.csv"
python "$env:TEMP/apmcm-q1-prior-independent.py" $source.FullName 2628c4c4dcd083f4481c15513942d16b06170588
```
