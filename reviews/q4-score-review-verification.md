# Independent verification of Q4 score-guided manual review

**Pass.** I read archived prediction, location and fold-prevalence tables from 05f4bab. All 105 holdout identifiers, folds, date-location groups and labels match the FalseBay subset of the 108-row location archive. I recomputed the ten fold prevalences as exact fractions from each full training complement, including other-site rows in the training complement. [Frozen specification](../docs/model-spec.md#q4-score-guided-manual-review-freeze) · [Archived forecasts](../results/q1_q4_cost_predictions.csv) · [Fold prevalences](../results/q1_q4_prevalence_folds.csv)

I independently sorted the score blocks in descending order and used rational arithmetic to count reviewed positives. For each block of size t with y positives and k slots available to that block, I added k*y/t to the complete higher blocks. Random review used the exact fraction of positives times the integer review budget. I generated 300 common date draws with seed 20261126 in sorted date-group order. In each draw I multiplied row weights by the sampled date multiplicities, ranked using the weighted blocks, and applied the integer budget floor((2*b*n+105)/210). The realized budget ranges were 5–19 for 10 nominal reviews, 12–47 for 25 and 25–95 for 50. I took 2.5th and 97.5th percentiles of the paired excess counts. All 30 yield rows and 42 contrast rows match production commit 51b3eb6 within absolute tolerance 1e-13, with exact denominators and draw counts. [Yields](../results/q4_score_review_yield.csv) · [Paired contrasts](../results/q4_score_review_contrasts.csv)

| Rule at 25 reviews, two-voice only | Expected positives confirmed | Share of the 21 positives |
|---|---:|---:|
| Random | 5 | 23.81% |
| Training prevalence | 48/11 | 20.78% |
| Multinomial | 3 | 14.29% |
| Binary | 4 | 19.05% |
| Proportional odds | 5 | 23.81% |

The primary multinomial excess is −2 relative to random (paired 95% interval −3.03 to 3.22) and −15/11 relative to prevalence (−4.79 to 5.66). Both lower limits are negative, so the frozen primary ranking-advantage criterion is unmet. In the broader passing set at 25 reviews, binary confirms 19 of 61 positives and has an excess of 135/19 over prevalence (0.49 to 14.76). Its excess over random has an interval of −0.60 to 8.56. These batch comparisons condition on the archived scores, modeled Q4 labels and perfect review of selected recordings.
