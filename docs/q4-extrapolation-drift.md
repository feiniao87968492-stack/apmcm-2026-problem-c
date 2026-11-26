# Q4 drift beyond retained playback distances

The protocol froze at `4e5fac1`. For the union deletion, the retained two-voice maxima are 100 m for natural and 120 m for control. The target is the clean net score at 150 m minus the full-data clean cutoff of 0.194371 in the point fit. This cutoff is half the equal-call mean of the isotonic net score at 20 m. Fidelity, context weights and the draw-specific cutoffs follow the published Monte Carlo analysis.

| Adverse drift | Maximum lambda | Point-only limit | Odds factor per doubling | Natural shift (pp) | Control shift (pp) | Point margin | Attainment |
|---|---:|---:|---:|---:|---:|---:|---:|
| Zero | 0 | — | 1 | 0 | 0 | 0.054787 | 4,002 / 4,800 |
| Natural only | 0.098582 | 0.699319 | 1.103605 | −1.442 | 0 | 0.046970 | 3,840 / 4,800 |
| Control only | 1.109350 | 4.014002 | 3.032386 | 0 | +1.802 | 0.045017 | 3,840 / 4,800 |
| Both arms | 0.093046 | 0.631712 | 1.097512 | −1.361 | +0.130 | 0.046704 | 3,840 / 4,800 |

The 80% draw criterion binds in all three drift scenarios. Immediately above each limit, attainment drops to 3,839 draws. The odds factor multiplies control odds and its reciprocal multiplies natural odds per doubling beyond the respective anchors. At 150 m the zero-drift probabilities are 50.426% for natural and 4.479% for control. The shifts in the table are changes to those point probabilities. The specified drift is a sensitivity of the retained multinomial extrapolation and the draw decision. Field validation at 150 m would require observations beyond both retained ranges.

Run from the repository root after installing the pinned dependencies. The targeted command reuses archived point acoustic summaries under `results/` and regenerates the paired draws from the contest attachments.

```sh
python q4_extrapolation_drift.py --data "/path/to/C-attachments/date"
```

[Result CSV](../results/q4_extrapolation_drift.csv) · [Frozen specification](model-spec.md#q4-extrapolation-drift-freeze)
