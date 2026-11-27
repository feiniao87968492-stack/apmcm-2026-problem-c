# Independent verification of the Q4 monitoring review budget

**Pass.** I read the committed input CSVs from `eb9c942` using Python's standard library and recomputed both orders and all budget cells independently of the production module. I joined the archived logistic predictions and probabilities by source row and checked the fold, recording group, true label and original hard prediction. The joined sample contains 105 FalseBay recordings from 15 recording groups. [Frozen specification](../docs/model-spec.md#q4-monitoring-review-budget-freeze)

At 100 m with 20% coupled loss, the archived gross scores are 0.162173 for flat, 0.243645 for modulated and 0.297058 for two-voice. The cutoff is 0.287598. Only two-voice passes. The original decisions leave six false passes among 84 truly nonpassing rows and 19 missed passes among 21 truly passing rows. [Curve archive](../results/q4_comparison_curves.csv)

I computed each ordering from the archived two-voice probability and hard decision, with the source row number as the final key. Counting residual errors used only the unreviewed suffix of each resulting order. For the uniform random rule, each row has probability `(105 - budget) / 105` of remaining unreviewed. I used exact rational arithmetic for the probabilities, rates and random differences. Both rank vectors match all 105 rows in `33e6eb4` exactly. Counts, rates, random expectations and differences match across all 30 budget rows to absolute tolerance of 1e-13. [Rank audit](../results/q4_review_budget_ranks.csv) · [Budget results](../results/q4_review_budget_results.csv)

| Reviews | Uniform random expected false / missed passes | Descending error probability | Nonpasses first |
|---:|---:|---:|---:|
| 0 | 6 / 19 | 6 / 19 | 6 / 19 |
| 10 | 5.429 / 17.190 | 1 / 18 | 6 / 18 |
| 25 | 4.571 / 14.476 | 0 / 18 | 6 / 14 |
| 50 | 3.143 / 9.952 | 0 / 8 | 6 / 5 |
| 105 | 0 / 0 | 0 / 0 | 0 / 0 |

At budget 50, descending error probability leaves fewer errors of both kinds than random expectation. Prioritizing nonpasses recovers three more missed passes than descending error probability and retains six false passes. Both rankings pool model scores across the five held-out fits. The calculation treats the review of any selected recording as a perfect and equally costly correction.

I ran the independent scratch verifier from the repository root with `python "$env:TEMP/apmcm-q4-budget-independent.py" 33e6eb4`.
