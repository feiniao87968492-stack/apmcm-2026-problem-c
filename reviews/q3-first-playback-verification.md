# Independent verification of Q3 first-playback response bounds

**Pass.** I read raw Data02 with Python's CSV reader and paired the call and control rows by `expID`. Matching the two observed playback distances and penguin counts gives 49 pairs. The four observed response cells (00, 01, 10, 11), ordered natural then control, contain 14, 2, 27 and 6 pairs in the matched sample and 47, 2, 74 and 16 in all 139 pairs. [Frozen protocol](../docs/model-spec.md#q3-first-playback-order-bounds-freeze)

I enumerated every feasible four-cell allocation of natural-first assignments. For allocation `(x00,x01,x10,x11)` with sum `m`, the natural-first response numerator is `x10+x11` and the control-first numerator is `count01+count11-x01-x11`. I computed the two extrema for each `m` with integer numerators over the common denominator `m(n−m)`. This calculation is independent of the production sorting method. I separately verified the allocation witnesses against the frozen tie rule by grouping equal weights and consuming ascending experiment IDs within each group.

At production commit `ab2b923`, all 186 per-`m` rows and all eight summary rows match the independently enumerated rational endpoints. Witness feasibility, displayed response numerators, share endpoints, tie handling, percentage-point conversions and strict positivity flags agree. The lower bound is strictly positive at `m=21–35` for the matched sample and `m=62–106` for all pairs. Neither sample has an exact zero lower bound at an interior `m`. [Per-m bounds and witnesses](../results/q3_first_playback_bounds.csv) · [Assumption summaries](../results/q3_first_playback_summary.csv)

| Assumed natural-first share | Matched exact bounds | All-pair exact bounds |
|---|---:|---:|
| Unrestricted interior shares | [−16/43, 41/43] | [−49/123, 121/123] |
| Nearest half | [7/75, 23/25] | [148/2415, 34/35] |
| 45%–55% | [22/299, 12/13] | [2/171, 37/38] |
| 40%–60% | [−1/145, 27/29] | [−45/664, 81/83] |

For example, at the matched 45%–55% lower endpoint, `m=23` and the allocation `(14,2,7,0)` gives 7/23 natural responses versus 6/26 control responses. The share bands are assumptions about the missing presentation sequence. The extrema describe contrasts among observed outcomes retained under such assignments. [Playback-order data audit](../docs/data-audit.md#playback-design-and-order-recoverability)
