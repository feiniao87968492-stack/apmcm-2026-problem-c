# Independent verification of Q1 recording-location sensitivity

**Pass.** I reconstructed the five folds from the raw Data01 rows and the frozen group lists. The regenerated logistic and XGBoost predictions match the archive on all 108 rows, along with row identifiers, fold, group and true class. The 105 FalseBay rows cover 15 dates and contain 44 flat, 40 modulated and 21 two-voice calls. Seapoint contributes three two-voice calls on one date in group 11. Both training conditions produce identical predictions in fold 4, which already holds out group 11. [Frozen specification](../docs/model-spec.md#q1-recording-location-sensitivity-freeze) · [Archived predictions](../results/round2_q1_predictions.csv)

I independently fitted logistic regression with an unweighted scaler and XGBoost on raw features. For each prediction variant I built a confusion matrix for each FalseBay date, summed the selected date matrices for each paired draw, and computed the three metrics from those totals. All 300 seed-20261126 draws contained all three true classes. All four CSVs in computation commit `3d7927bef8c1da8801c86fdcd283f59f7503f1e1` reconcile with these calculations. The 426 defined decisions, six blank deletion fields and row metadata match exactly. The 12 point metrics, 12 paired contrasts and six scoring-only scores agree at absolute tolerance `1e-14`. [Predictions](../results/q1_location_predictions.csv) · [Point metrics](../results/q1_location_metrics.csv) · [Paired contrasts](../results/q1_location_contrasts.csv) · [Scoring-only audit](../results/q1_location_scoring_only.csv)

| FalseBay holdouts | Macro F1 | Two-voice correct | Two-voice false positives |
|---|---:|---:|---:|
| Original logistic | 0.322922 | 2 | 6 |
| Original XGBoost | 0.375594 | 3 | 10 |
| Logistic refit without group 11 | 0.360434 | 3 | 8 |
| XGBoost refit without group 11 | 0.391855 | 3 | 7 |

| Paired contrast | Macro F1 change and 95% interval | Two-voice correct change and interval | Two-voice false positives change and interval |
|---|---:|---:|---:|
| Original XGBoost minus original logistic | +0.05267 [−0.02975, 0.11186] | +1 [−2, 5] | +4 [0, 9] |
| Deletion XGBoost minus deletion logistic | +0.03142 [−0.03887, 0.08096] | 0 [−3, 3] | −1 [−4.525, 2] |
| Logistic deletion minus original | +0.03751 [0.00017, 0.07460] | +1 [0, 3] | +2 [0, 5] |
| XGBoost deletion minus original | +0.01626 [−0.01606, 0.04593] | 0 [0, 0] | −3 [−6, 0] |

In archived row order 25–27, logistic predicts modulated for all three Seapoint calls. The random forest predicts flat, modulated and modulated. XGBoost predicts flat, two-voice and modulated. With those three rows included, XGBoost leads the random forest in macro F1 (0.38339 versus 0.36980). Scoring only FalseBay keeps the archived decisions and reverses that order (random forest 0.37857, XGBoost 0.37559). Logistic ranks third under both scoring scopes. The two XGBoost–logistic intervals include zero. The logistic refit interval has a lower endpoint only 0.00017 above zero and is conditional on these held-out dates and fitted predictions. Seapoint's single date and class confound location with date and class coverage. [Scoring-only audit](../results/q1_location_scoring_only.csv)

I ran a local scratch verifier with Python 3.10.11, NumPy 2.2.6, pandas 2.3.3, scikit-learn 1.7.2 and XGBoost 3.2.0. It read the archive through `git show` and did not import production code.

```powershell
$data01 = Get-ChildItem -LiteralPath "<attachment directory>/date" -Filter "Data01*.csv"
python "$env:TEMP/apmcm-q1-location-independent.py" $data01.FullName
```
