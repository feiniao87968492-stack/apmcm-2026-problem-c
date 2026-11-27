# Q3 playback carryover sensitivity

Use the two observed responses in each pair at their recorded distances and group sizes. The uncorrected natural-minus-control difference is 25/49 for matched pairs and 72/139 for all pairs. For each hypothetical sequence, retain the first response and allow the second to change to the binary response it could have had without the preceding playback. Suppressive carryover allows only 0-to-1 corrections. Enhancing carryover allows only 1-to-0 corrections. Two-sided carryover allows both. [Frozen specification](model-spec.md#q3-playback-carryover-sensitivity-freeze)

Each eligible correction changes the natural-minus-control numerator by exactly one in a known direction. For a given direction and order restriction, let L and U be the largest feasible counts of corrections that lower and raise that numerator, respectively. For an at-most budget b and observed numerator D, the sharp bounds are (D − min(b,L))/n and (D + min(b,U))/n. Four-cell integer allocations find the capacities and witness orders. The unrestricted case includes m=0 and m=n. Nearest-half allows m=24 or 25 for 49 pairs, and m=69 or 70 for 139. [All budgets and endpoint witnesses](../results/q3_carryover_bounds.csv)

| Sample | Natural-first order | Allowed carryover | Full-budget bounds (pp) | Fewest changed pairs for a nonpositive contrast |
|---|---|---|---:|---:|
| Matched | Unrestricted | Two-sided | [−44.90, 95.92] | 25 |
| Matched | Unrestricted | Suppressive | [−32.65, 83.67] | 25 |
| Matched | Unrestricted | Enhancing | [−16.33, 67.35] | 25 |
| Matched | Nearest half | Two-sided | [−44.90, 95.92] | 25 |
| Matched | Nearest half | Suppressive | [0.00, 83.67] | 25 |
| Matched | Nearest half | Enhancing | [0.00, 67.35] | 25 |
| All | Unrestricted | Two-sided | [−46.76, 98.56] | 72 |
| All | Unrestricted | Suppressive | [−35.25, 87.05] | 72 |
| All | Unrestricted | Enhancing | [−12.95, 64.75] | 72 |
| All | Nearest half | Two-sided | [−46.76, 98.56] | 72 |
| All | Nearest half | Suppressive | [1.44, 87.05] | Unreachable |
| All | Nearest half | Enhancing | [1.44, 64.75] | Unreachable |

For example, with nearest-half order and suppression in the 49 matched pairs, place 25 of the 27 natural-only responders in the natural-first arm and put all other pairs in the control-first arm. In the cell order (00, 01, 10, 11) this gives natural-first allocation (0, 0, 25, 0). Correct their second, control responses from 0 to 1 to reach zero. Under enhancement the allocation (14, 2, 2, 6) gives 24 natural-first pairs. Correct the second, natural responses of the 25 control-first natural-only pairs from 1 to 0 to reach zero. The remaining budget cannot make either nearest-half one-direction contrast negative in the matched sample. [Summary CSV](../results/q3_carryover_summary.csv)

Actual playback order and carryover remain unknown. The bounds condition on observed distances and hypothetical order, direction and budget restrictions. The [first-playback analysis](q3-first-playback.md) instead describes the difference among the hypothetical first-playback subsets using uncorrected observations.

```sh
python main.py --data "<attachment directory>/date" --output generated --q3-carryover
```
