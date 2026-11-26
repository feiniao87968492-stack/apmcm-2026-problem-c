# First vocal replies and group event order

The protocol froze at `19ae12e` and ran at `2221807`. We use the first reply among scored vocal responses, following the field study. All 76 natural and five control responses have a recognized first reply. [Field study](https://doi.org/10.12688/openreseurope.24618.1)

| Stimulus | Context | Flat | Modulated | Two-voice | Responses | All trials |
|---|---|---:|---:|---:|---:|---:|
| Natural | Resting after feeding | 5 | 9 | 3 | 17 | 36 |
| Natural | Commuting | 11 | 13 | 3 | 27 | 65 |
| Natural | Searching | 12 | 18 | 2 | 32 | 38 |
| Control | Resting after feeding | 1 | 0 | 1 | 2 | 36 |
| Control | Commuting | 0 | 1 | 0 | 1 | 65 |
| Control | Searching | 0 | 2 | 0 | 2 | 38 |

For example, modulated first replies while searching account for 56.3% of natural vocal responses (95% date interval 36.0–72.7%) and occur in 47.4% of all corresponding natural trials (29.0–64.5%). The control cells describe five responses across four dates. Conditional shares use 212–263 draws with nonzero response denominators in the control cells. [Full matrix with both denominators and intervals](../results/first_reply_matrix.csv)

| Strict natural-responder prediction | Cross-entropy | Summed Brier |
|---|---:|---:|
| Pooled half-count | 0.953 | 0.585 |
| Context shrinkage | 1.000 | 0.606 |
| Context and played call shrinkage | 1.023 | 0.625 |

Context and played call versus pooled changes cross-entropy by +0.070 (95% paired date interval [−0.028, 0.183]) and Brier by +0.041 [−0.001, 0.073]. Keep the pooled distribution under the joint rule. Date-and-context permutation gives 24 observed matches versus 25.98 expected among 76 natural responders (31.6% versus 34.2%, one-sided p=0.8859). Eleven of 27 blocks, containing 40 responders, have variation in both labels. This checks enrichment among observed natural vocal responses. [Fold coverage](../results/first_reply_folds.csv) · [Paired intervals](../results/first_reply_scores.csv) · [Permutation](../results/first_reply_matching.csv)

Of 19 natural trials with scored vocalizing and approach across 11 dates, 18 had vocal onset first, one had approach first, and none tied. The vocal-first share was 94.7% (95% date interval 87.5–100%). The mean approach-minus-vocal lag was 6.68 s [3.61, 11.60], and the median was 3.60 s [2.20, 11.60]. These are first observed events within groups and can involve different birds. [Order and lag estimates](../results/first_reply_event_order.csv)
