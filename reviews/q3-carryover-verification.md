# Independent verification of Q3 playback carryover bounds

**Pass.** I read Data02 with Python's CSV reader and paired the two stimulus records by `expID`. The 49 equal-distance and equal-group-size pairs have counts (14, 2, 27, 6) in observed (natural, control) cell order 00, 01, 10, 11. The 139-pair sensitivity has counts (47, 2, 74, 16). The corresponding original response differences are 25/49 and 72/139. [Frozen protocol](../docs/model-spec.md#q3-playback-carryover-sensitivity-freeze)

I used an integer dynamic program over individual pairs to track minimum and maximum achievable numerators by exact natural-first count and exact number of corrected second responses. Each transition retains the observed first response and considers the observed or permitted corrected second response. For each budget I took the extrema over all admissible orders and correction counts up to that budget. A separate dynamic program over the four cells recovered the greatest correction capacity and lexicographically earliest order allocation for each endpoint. I checked the exported corrections against the frozen cell and order tie rules and reconstructed the endpoint from each allocation.

All 1,140 budget rows, 2,280 endpoint allocations and 12 summaries agree with production commit `67cfb74`. Exact rational endpoints, capacities, order counts, correction counts and minimum budgets agree exactly. Percentage-point values agree within `1e-12`. [Budget bounds and witnesses](../results/q3_carryover_bounds.csv) · [Summary](../results/q3_carryover_summary.csv)

| Sample | Carryover | Full-budget numerator bounds, unrestricted | Full-budget numerator bounds, nearest half | First nonpositive budget, unrestricted / nearest half |
|---|---|---:|---:|---:|
| 49 matched | Two-sided | [−22, 47] | [−22, 47] | 25 / 25 |
| 49 matched | Suppressive | [−16, 41] | [0, 41] | 25 / 25 |
| 49 matched | Enhancing | [−8, 33] | [0, 33] | 25 / 25 |
| All 139 | Two-sided | [−65, 137] | [−65, 137] | 72 / 72 |
| All 139 | Suppressive | [−49, 121] | [2, 121] | 72 / unreachable |
| All 139 | Enhancing | [−18, 90] | [2, 90] | 72 / unreachable |

Divide the numerators by the sample size to obtain rate differences. In the all-pair one-direction cases with nearest-half order, at most 70 second responses can reduce the contrast, leaving a lower bound of 2/139. The budget and direction describe hypothetical corrections at the recorded distances. Actual presentation order and carryover remain unknown. [Order recoverability audit](../docs/data-audit.md#playback-design-and-order-recoverability)
