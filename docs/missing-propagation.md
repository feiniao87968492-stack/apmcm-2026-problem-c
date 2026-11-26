# Missing propagation comparisons

The protocol froze at `87748d6` and the analysis ran at `7150087`. Twenty-seven of the 63 representation-by-call-by-distance cells have fewer than 300 scores. Two-voice has 190 available at 128 m in each representation. [Cell counts and means](../results/missing_q2_cells.csv)

| Call | Available-value isotonic radius at 0.50 (m) | Sharp completed range (m) | Change from available radius (m) |
|---|---:|---:|---:|
| Flat | 84.7 | 44.8–130.5 | −39.9 to +45.7 |
| Modulated | 144.6 | 89.2–167.3 | −55.4 to +22.8 |
| Two-voice | 169.7 | 73.8–251.2 | −95.9 to +81.5 |

The bounds concern the isotonic estimator after filling each missing correlation with a value in [−1, 1], with both endpoints attainable. Modulated leads under the all-low completion at every threshold. Under the all-high completion two-voice leads, reaching the 256 m support boundary at 0.40. The bounds describe uncertainty about missing comparisons. [All threshold radii and flags](../results/missing_q2_radius_bounds.csv)

On the 0.01-spaced relative quality grid, at threshold 0.70 the isotonic leader changes from modulated at 0.97 to two-voice at 0.98. The shared-exponent leader is modulated throughout. At thresholds 0.40, 0.50 and 0.60 the first grid points at which two-voice leads are 0.22, 0.21 and 0.46 under isotonic fitting and 0.30, 0.39 and 0.56 under the shared-exponent fit. The grid describes stipulated values for the missing scores. [Both curves across the grid](../results/missing_q2_quality_grid.csv)

| Q4 scenario | Pass all completions | Depend on completion | Fail all completions |
|---|---|---|---|
| Clean | Modulated and two-voice at 50 m | Flat at 50 m, modulated at 100 m, two-voice at 100 and 150 m | Flat at 100 and 150 m, modulated at 150 m |
| 20% coupled loss | Modulated at 50 m | Two-voice at 50 m | All six settings at 100 and 150 m, flat at 50 m |

Under coupled loss, two-voice at 50 m has 85.3% available-value attainment versus 51.0–90.3% across completions. Clean two-voice at 150 m has 78.7% versus 0–89.0%. The cutoff is shared across completions within each of the original 300 paired acoustic/date draws. Each curve is held fixed, and the percentile intervals describe conditional resampling variation. At 150 m the comparison is at the Q4 support boundary. [All baseline and endpoint margins, intervals and decisions](../results/missing_q4_attainment.csv)

We adopt the bounds and the quality grid as sensitivity evidence. We retain the available-value shared-exponent curve as the primary Q2 fit and interpret Q4 attainment as conditional on the stated scenario and reference. The observed data supply neither the missing scores nor their relative quality.
