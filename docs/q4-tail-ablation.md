# Five-model Q4 tail ablation

The specification froze at `09c0aca` before the candidate fits. The comparison uses the same recorded paired playbacks, acoustic fidelity, full-model cutoffs and 4,800 paired draws as the released distance-deletion audit. [Frozen model and acceptance rule](model-spec.md#q4-monotone-and-bounded-extrapolation-ablation-freeze)

| Model | Ordinary mask loss | Ordinary Brier | Ordinary pair loss | Tail mask loss | Tail Brier | Tail pair loss |
|---|---:|---:|---:|---:|---:|---:|
| A. Released multinomial | 1.29934 | 0.16978 | 1.05868 | 1.14866 | 0.21475 | 1.33270 |
| B. Shared monotone distance slope | 1.14080 | 0.17891 | 1.10547 | 1.29355 | 0.22987 | 1.40674 |
| C. Call-specific monotone slopes | 1.15643 | 0.18373 | 1.13671 | 1.29347 | 0.23285 | 1.40656 |
| D. Multinomial with joint odds ratio | 1.29934 | 0.16978 | 1.04314 | 1.14866 | 0.21475 | 1.30268 |
| E. Restricted training and bounded plateau | 1.14702 | 0.17391 | 1.09034 | 1.19512 | 0.19847 | 1.21434 |

Each date is held out in turn and training additionally excludes all pairs whose natural track occurs on that date. Ordinary validation covers all 139 pairs across 12 dates. The tail check scores 26 pairs across eight of those dates and removes all such distant pairs from training. A tail test pair has at least one playback at 125 m or farther, and the scores include both arms. There are zero fit failures and zero held-date or held-track training overlaps. The four other dates have no tail tests. [Fold audit](../results/q4_tail_ablation_folds.csv) · [Pooled metrics and paired intervals](../results/q4_tail_ablation_validation.csv)

**Model decision.** Retain A. B, C and E have lower ordinary mask loss and higher ordinary Brier point estimates. B and C both worsen the two tail scores. E lowers tail Brier by 0.01628 (paired 95% interval −0.04211 to +0.01980) and increases tail mask loss by 0.04646 (−0.08221 to +0.19058). D preserves A's marginals, with joint pair log-loss changes of −0.01554 (−0.03434 to +0.00364) in ordinary validation and −0.03003 (−0.04725 to +0.00497) in the tail check. B and C share stimulus-specific composition among responders, so comparisons with A reflect both response-incidence and mask-composition choices. [Adoption decision](../results/q4_tail_ablation_adoption.csv)

The archived experiments supply tail tests after artificial deletion. They provide limited overlap with the exact standardized prediction at 150 m. Call-by-arm combinations at 150 m after union deletion still require interpretation as model-based extrapolations.

## Q4 under union deletion

Cells show the point margin and the percentage of draws attaining the same frozen cutoff. All 4,800 draws were valid for each model and fit.

| Model | Clean two-voice net at 150 m | Coupled two-voice net at 100 m | Clean modulated gross at 100 m |
|---|---:|---:|---:|
| A and D | +0.05479 / 83.38% | +0.02422 / 74.48% | +0.08995 / 84.35% |
| B | +0.03142 / 69.92% | +0.01690 / 68.25% | +0.07701 / 83.52% |
| C | +0.06365 / 87.50% | +0.02683 / 80.69% | +0.06867 / 79.79% |
| E | +0.12161 / 99.25% | +0.05224 / 90.33% | +0.13800 / 94.79% |

The full-data fits, paired differences from A and 95% intervals are in the same evidence table. E uses the same eligible pairs in the full and union-deletion analyses by construction. [Q4 margins and decisions](../results/q4_tail_ablation_margins.csv)

| Model | Natural change from 100 to 150 m (pp) | Control change from 120 to 150 m (pp) | Natural-only maximum lambda | Control-only maximum lambda | Both-arm maximum lambda |
|---|---:|---:|---:|---:|---:|
| A and D | −7.434 | −0.961 | 0.098582 | 1.109350 | 0.093046 |
| B | −10.108 | −1.005 | infeasible | infeasible | infeasible |
| C | −6.175 | −0.871 | 0.277370 | 2.067469 | 0.252397 |
| E | 0 | 0 | 1.096569 | 4.368128 | 0.960482 |

Each feasible drift maximum is approximate and set by the 80% draw rule. The exact reported boundary has 3,840 qualifying draws, decreasing to 3,839 immediately above it. B starts below the rule even though its zero-drift point margin is positive. E holds each arm at its last fitted probability by construction. Its greater tolerance quantifies the effect of that assumption on the decision. [Nominal tail changes and intervals](../results/q4_tail_ablation_tail.csv) · [Drift limits, odds factors and boundary counts](../results/q4_tail_ablation_drift.csv)

## Scoring by actual playback distance

The 26 tail-test pairs contain 33 trials at 125 m or farther across eight dates and 19 shorter partners across seven dates. Each band has 4,800 valid whole-date draws. The table gives trial-weighted changes from A with paired 95% percentile intervals.

| Actual distance | Model | Mask log-loss change | Brier change |
|---|---|---:|---:|
| At least 125 m | B | +0.11733 [−0.10797, +0.36759] | +0.02028 [−0.01101, +0.04272] |
| At least 125 m | C | +0.09431 [−0.10837, +0.31972] | +0.01453 [−0.00886, +0.03834] |
| At least 125 m | E | −0.06243 [−0.28364, +0.20914] | −0.03427 [−0.06729, +0.00871] |
| Below 125 m | B | +0.19276 [+0.05114, +0.42157] | +0.00616 [−0.00939, +0.02935] |
| Below 125 m | C | +0.23250 [+0.05364, +0.43670] | +0.02431 [+0.00415, +0.04272] |
| Below 125 m | E | +0.23558 [+0.05785, +0.36194] | +0.01497 [−0.00698, +0.04078] |

E's Brier point gain is larger on actual long trials, and its paired interval includes zero. Its mask log loss also improves in point estimate there, while the shorter partners drive the increase in pooled mask loss. Weighting the split deltas by 33/52 and 19/52 reproduces the released pooled deltas to 1e-12. D shares A's marginal predictions. The original adoption rule retains A. [Absolute scores, deltas and reconciliation](../results/q4_tail_distance_scores.csv)

From 125 to 175 m inclusive, two-voice natural playback contributes two trials across two dates with two responses. Control contributes one trial with zero responses. All three trials were at 150 m. This limits what the pooled long-trial scores establish about two-voice playback at that distance. [Coverage by arm](../results/q4_tail_distance_coverage.csv)

## Reproduction

Run from a clean checkout with the pinned dependencies and the supplied attachment CSVs.

```sh
python main.py --data "/path/to/C-attachments/date" --q4-tail-ablation
python q4_tail_distance.py --data "/path/to/C-attachments/date"
```

The ablation uses the archived point summaries in the checkout and regenerates the acoustic and date streams from the attachments.
