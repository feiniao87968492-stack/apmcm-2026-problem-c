# Independent verification of monitoring baselines without acoustic features

**Pass.** I read the original Data01 rows with Python's CSV reader and enumerated the 16 date-by-location groups in sorted order. I reconstructed the five frozen folds and checked the source row, group, fold and call label of every archived forecast. The scored rows are exactly the 105 FalseBay recordings from 15 dates. Training counts used all 108 source rows before removing the corresponding test groups. [Frozen specification](../docs/model-spec.md#q1-to-q4-monitoring-without-acoustic-features-freeze) · [Archived forecasts](../results/q1_q4_cost_predictions.csv)

| Passing set | Fold 1 | Fold 2 | Fold 3 | Fold 4 | Fold 5 |
|---|---:|---:|---:|---:|---:|
| Two-voice | 20/89 | 20/94 | 20/87 | 19/83 | 17/79 |
| Modulated or two-voice | 55/89 | 56/94 | 54/87 | 49/83 | 42/79 |

Using the cutoff formula, the fold-specific prevalence rule predicts nonpass at every cost ratio for the two-voice set. For the broader set it predicts pass at 1:1 and 1:3 and nonpass at 3:1. These decisions follow from the training proportions. [Fold counts](../results/q1_q4_prevalence_folds.csv)

I independently calculated decisions and scores from the archived labels and probabilities. For each paired interval I summed the per-date cost differences with the bootstrap date multiplicities and divided by the sampled recording count. At computation commit 8ba6707, all 10 fold rows, 48 decision rows, 30 paired cost contrasts and eight probability scores agree within 1e-14, with exact agreement for counts and flags. The archived rules reproduce all 30 prior decision rows exactly. [Decision counts](../results/q1_q4_prevalence_decisions.csv) · [Paired contrasts](../results/q1_q4_prevalence_contrasts.csv) · [Probability scores](../results/q1_q4_prevalence_scores.csv)

At equal costs in the primary setting, the training prevalence rule gives zero false passes and 21 missed passes. The best acoustic point rules make 25 errors. The multinomial and binary probability rules have paired mean-cost differences of +0.03810 [0.01063, 0.07305] and +0.04762 [0.01249, 0.08064], respectively. No acoustic rule has a strictly negative upper 95% cost-difference bound in any evaluated setting. Prevalence has lower Brier and log loss point scores than every acoustic probability model for the two-voice set (0.16125, 0.50406) and the broader set (0.25285, 0.69926). These comparisons describe the fixed modeled scenarios and held-out recordings.
