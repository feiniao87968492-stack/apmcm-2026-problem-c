# Q4 summaries over the supported annulus

The protocol froze at `a844b4d` and ran at `05bd6e8`. Both averages use the 20–150 m grid and the adopted shared-exponent propagation curve with the existing eight-bird response model. The area average weights a uniform surface location under radial symmetry. [Integrated scores and intervals](../results/annulus_scores.csv)

| Call | Clean distance mean | Clean area mean | 6 dB local coupled area loss [95%] | 6 dB matched uniform coupled area loss |
|---|---:|---:|---:|---:|
| Flat | 0.312 | 0.259 | 53.3% [49.2%, 55.9%] | 49.7% |
| Modulated | 0.426 | 0.381 | 42.0% [36.4%, 45.9%] | 50.9% |
| Two-voice | 0.464 | 0.435 | 34.5% [31.8%, 36.3%] | 50.7% |

Both weighting schemes give the point order two-voice, modulated, flat in every scenario. The clean two-voice minus modulated area gap is 0.055 with a paired interval of [−0.113, 0.178]. [Pairwise gaps](../results/annulus_score_gaps.csv)

| Call | Clean qualifying area | Clean point-radius area | Eight-scenario interval | Eight-scenario area | Smallest noisy point-radius area |
|---|---:|---:|---|---:|---:|
| Flat | 15.03% | 31.52% | Empty | 0% | 0.99% |
| Modulated | 44.35% | 84.28% | 20–29 m | 2.00% | 3.87% |
| Two-voice | 84.99% | 100% | 20–20.5 m | 0.09% | 2.14% |

No scenario produces multiple qualifying runs. A segment qualifies when each endpoint passes the 80% rule with the original common cutoff, using the archived paired acoustic and date draws. Filling to a point radius uses a different criterion. Clean two-voice has a qualifying interval of 20–138.5 m, and its point radius reaches the 150 m support boundary. These areas describe the radial scenario. [Area comparison](../results/annulus_attainment.csv) · [Connected intervals](../results/annulus_intervals.csv) · [Grid attainment](../results/annulus_attainment_grid.csv)

| Call | Clean available → completion range | 20% coupled available → completion range |
|---|---|---|
| Flat | 0.257 → [0.122, 0.316] | 0.172 → [0.082, 0.212] |
| Modulated | 0.376 → [0.264, 0.411] | 0.249 → [0.175, 0.272] |
| Two-voice | 0.446 → [0.182, 0.492] | 0.296 → [0.121, 0.327] |

These bounds use the isotonic completion curves. All six point difference ranges span zero, so no pair has an identified strict ordering under the permitted completions. The tables give separate date-draw uncertainty for the fixed completion endpoints and the share of draws identifying each direction. [Completion scores](../results/annulus_completion_scores.csv) · [Pairwise completion gaps](../results/annulus_completion_gaps.csv)
