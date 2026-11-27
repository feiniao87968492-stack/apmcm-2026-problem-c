# Q3 first-playback response bounds

Data02 identifies natural and sea-wave control responses within each group but leaves presentation order unresolved. The primary sample contains 49 pairs with identical recorded playback distance and group size. The sensitivity uses all 139 pairs. In cell order (neither, control only, natural only, both), their observed counts are (14, 2, 27, 6) and (47, 2, 74, 16). [Data audit](data-audit.md#playback-design-and-order-recoverability) · [Frozen specification](model-spec.md#q3-first-playback-order-bounds-freeze)

Assign exactly m pairs to natural first and retain their observed natural response N. Retain the observed control response C in the complementary n−m pairs. The natural-minus-control difference equals the sum of N/m + C/(n−m) over the m selected pairs, less the total number of observed control responses divided by n−m. Selecting the smallest or largest m weights attains the corresponding endpoint. Equal weights use ascending experiment ID. [Exact bounds and allocations for each m](../results/q3_first_playback_bounds.csv)

| Assumed natural-first share | Allowed m, matched | Matched bounds (pp) | Allowed m, all | All-pair bounds (pp) |
|---|---:|---:|---:|---:|
| Unrestricted, both stimuli represented | 1–48 | [−37.21, 95.35] | 1–138 | [−39.84, 98.37] |
| Nearest half | 24–25 | [9.33, 92.00] | 69–70 | [6.13, 97.14] |
| 45%–55%, inclusive | 23–26 | [7.36, 92.31] | 63–76 | [1.17, 97.37] |
| 40%–60%, inclusive | 20–29 | [−0.69, 93.10] | 56–83 | [−6.78, 97.59] |

The lower endpoint is strictly positive for exactly m = 21–35 in the matched sample and m = 62–106 in all pairs. At m = 24 in the matched sample, the natural-first allocation (14, 2, 8, 0) gives the lower endpoint of 8/24 − 6/25. The allocation (0, 0, 18, 6) gives the upper endpoint of 24/24 − 2/25. Under the broader 40%–60% assumption, (14, 2, 4, 0) at m = 20 attains the matched lower endpoint of 4/20 − 6/29. The summary export gives an attainable allocation for each endpoint. [Exact summary and allocations](../results/q3_first_playback_summary.csv)

The share ranges are assumptions about the unobserved order. The bounds describe the observed first-playback sample contrast under those assumptions. Each endpoint is attainable, and the possible contrasts form a discrete set. The bounds provide no estimate of population effects or carryover.

```sh
python main.py --data "<attachment directory>/date" --output generated --q3-first-playback
```

[Independent integer-allocation verification](../reviews/q3-first-playback-verification.md)
