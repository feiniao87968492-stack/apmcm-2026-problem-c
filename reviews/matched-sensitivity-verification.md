# Independent recomputation of matched-distance and Q4 sensitivities

**PASS.** I recomputed the three analyses separately from the new implementation at f6e5984 under the specification at c4bf42f. The audit reused the published Q2 and Q3 estimators and rebuilt their input samples.

- I joined paired trials on experiment ID, assigned strata from the two distances and recomputed discordance and all three date-block percentile intervals directly from the paired binary outcomes. [Strata](../results/matching_q3_strata.csv)
- I reconstructed experiment and date bootstrap predictions and used a reverse scalar search over the 201 loss steps with an independently evaluated coupled response. All 18 rows matched, including endpoint support, the archived experiment-pair limits, the date limits, and intersection status. [Loss limits](../results/matching_q4_loss_limits.csv)
- I summed mask probabilities containing each behavior and then multiplied those marginals by their weights. This independently reproduced all 54 fixed-distance rows and 18 radius rows, including support flags and interval endpoints. [Fixed distances](../results/matching_q4_weighted_points.csv) · [Radii](../results/matching_q4_weighted_radii.csv)
