# Q1 recording-location sensitivity

Data01 has 105 FalseBay recordings from 15 dates (44 flat, 40 modulated, 21 two-voice) and three Seapoint recordings from one date (all two-voice). Both original models reproduced their archived predictions on all 108 rows. The comparison below holds the 105 FalseBay test rows fixed and uses the original five folds. The refits drop Seapoint group 11 wherever it would enter training. Fold 4 already held out group 11 and yields identical predictions under both training conditions. [Frozen specification](model-spec.md#q1-recording-location-sensitivity-freeze)

| Training | Model | Macro F1 | Two-voice correct (of 21) | Two-voice false positives |
|---|---|---:|---:|---:|
| All training locations | Logistic | 0.3229 | 2 | 6 |
| All training locations | XGBoost | 0.3756 | 3 | 10 |
| FalseBay only | Logistic | 0.3604 | 3 | 8 |
| FalseBay only | XGBoost | 0.3919 | 3 | 7 |

| Paired contrast | Macro F1 change [95% interval] | Correct count change [95% interval] | False-positive count change [95% interval] |
|---|---:|---:|---:|
| XGBoost minus logistic, original | +0.05267 [−0.02975, 0.11186] | +1 [−2, 5] | +4 [0, 9] |
| XGBoost minus logistic, FalseBay-only fit | +0.03142 [−0.03887, 0.08096] | 0 [−3, 3] | −1 [−4.525, 2] |
| FalseBay-only minus original, logistic | +0.03751 [0.00017, 0.07460] | +1 [0, 3] | +2 [0, 5] |
| FalseBay-only minus original, XGBoost | +0.01626 [−0.01606, 0.04593] | 0 [0, 0] | −3 [−6, 0] |

All 300 paired resamples of the 15 FalseBay dates retained all three classes. The count intervals describe paired differences in resampled counts. The logistic refit's lower F1 bound is close to zero, and the two XGBoost-versus-logistic intervals span zero. The results describe sensitivity to this particular group in the fixed training and scoring design. With two-voice as the only class observed at Seapoint on one date, the data confound location, date and class composition.

With archived decisions fixed, scoring all 108 rows ranks XGBoost (0.3834) above random forest (0.3698) and logistic (0.3144). Restricting scoring to FalseBay ranks random forest (0.3786) above XGBoost (0.3756) and logistic (0.3229). In source rows 25–27, all of which are two-voice, the archived predictions are modulated/modulated/modulated for logistic, flat/modulated/modulated for random forest, and flat/two-voice/modulated for XGBoost. [Predictions](../results/q1_location_predictions.csv) · [Scoring-only comparison](../results/q1_location_scoring_only.csv) · [Full-precision paired contrasts](../results/q1_location_contrasts.csv)

```sh
python main.py --data "<attachment directory>/date" --output generated --q1-location
```

[Independent verification](../reviews/q1-location-verification.md)
