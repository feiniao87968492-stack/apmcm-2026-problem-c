# Q1 class-prior decision comparison

The original logistic fit and three prior-based variants use the same five held-out recording-group folds. All 108 original decisions and their fold, group and observed-label fields match the archive. The training-fold scaler and six complete acoustic predictors are shared across comparisons. [Frozen specification](model-spec.md#q1-class-prior-decision-comparison-freeze)

| Decision rule | Macro F1 | Paired change (95% interval) | Recall, flat / modulated / two-voice | Two-voice precision | Two-voice correct / false labels | Change in correct / false labels |
|---|---:|---:|---:|---:|---:|---:|
| Original logistic | 0.3144 | Reference | 52.3% / 37.5% / 8.3% | 25.0% | 2 / 6 | Reference |
| Half correction | 0.2908 | −0.0236 [−0.0781, 0.0254] | 47.7% / 32.5% / 8.3% | 10.0% | 2 / 18 | 0 / +12 |
| Full correction | 0.3352 | +0.0208 [−0.0715, 0.1747] | 43.2% / 32.5% / 25.0% | 20.0% | 6 / 24 | +4 / +18 |
| Inverse-frequency weighted refit | 0.3268 | +0.0124 [−0.0739, 0.1688] | 43.2% / 30.0% / 25.0% | 18.2% | 6 / 27 | +4 / +21 |

All 300 paired recording-group bootstrap draws contained all three classes. The full correction retained both original correct two-voice labels and added four correct labels, together with 12 new false labels among flat calls and six among modulated calls. The original held-out two-voice probability ranks recordings with average precision 0.2547, versus 0.2222 for a constant score at the observed two-voice fraction. The point estimate suggests limited separation in this sample, alongside the low original two-voice recall.

Retain the original logistic decision. The full correction meets the recall condition and its paired F1 interval spans zero. The half correction adds false labels without recovering any additional two-voice calls. The weighted refit recovers the same number as full correction with more false labels, and its interval also spans zero. The equal-prior rule describes a decision objective under a prior-shift assumption. The sample provides no estimate of deployment class proportions.

```sh
python main.py --data "<attachment directory>/date" --output generated --q1-class-prior
```

[Per-recording probabilities, folds and predictions](../results/q1_class_prior_predictions.csv) · [Full-precision metrics and decisions](../results/q1_class_prior_metrics.csv) · [Independent recomputation](../reviews/q1-class-prior-verification.md)
