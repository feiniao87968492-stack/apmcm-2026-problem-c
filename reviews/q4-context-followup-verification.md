# Independent verification of the full-fit Q4 Monte Carlo follow-up

**Pass.** The fixed follow-up generated 38,400 paired draws in eight blocks of 4,800. I reconciled the per-block counts to 26 distinct, lexicographically ordered joint clean and +6 dB profiles. Every noisy pass is paired with a clean pass in the same context. The pooled clean/noisy counts are 37,645/23,399 after feeding, 36,737/21,347 commuting, and 38,288/35,041 searching. The three published CSVs match the clean-archive run byte for byte. [Frozen protocol](../docs/model-spec.md#q4-independent-full-fit-monte-carlo-follow-up-freeze) · [Joint profiles](../results/q4_context_followup_profiles.csv)

I checked that the seed arithmetic implements 20261300–20261307 for acoustic draws and 20261400–20261407 for playback draws, separated from the archived 20261130 and 20261201 streams. The existing acoustic and playback draws are paired in row order within each block. The default path retains 4,800 draws and both fits with the original seeds. The lead's default-seed replay matched all 4,800 indexed rows per fit, including the context and standardized clean/noisy indicators. Separately, I recovered the archived full-fit margins and exact vertex means from the indexed indicators. Resampling those indices at the archived seed 20261205 also reproduced its half-width of 70,773/11,120,000 in probability units. [Archived indicators](../results/q4_context_mc_indicators.csv) · [Archived bounds](../results/q4_context_mc_bounds.csv)

I reconstructed the six allocation vertices by fixing two context shares on opposite box faces, solving the weighted half-exposure constraint and reflecting around uniform exposure. For each vertex I calculated the integer score at each profile in units of 1/1,390. With integer profile score vectors \(x_p\), counts \(n_p\), and sum \(T=\sum_p n_p x_p\), I used the exact covariance of sample means
\[
\frac{N\sum_p n_p x_p x_p^\mathsf{T} - T T^\mathsf{T}}
     {N^2 (N-1) 1390^2},
\qquad N=38{,}400.
\]
All six exact means, six Monte Carlo standard errors and 36 covariance entries agree with the implementation. The vertex standard errors range from 0.099400 to 0.110280 percentage points. [Vertex statistics](../results/q4_context_followup_vertices.csv)

I independently generated the 10,000 multinomial count vectors one at a time using PCG64 at seed 20261500. I weighted the integer profile scores by each resampled count vector, subtracted the original score sums, and sorted the largest absolute deviations across the six vertices. The two integer deviations surrounding the linear 95th percentile are 122,488 and 122,574. Linear interpolation and division by \(38{,}400 \times 1390\) give the exact common half-width \(1224923/533760000\), or 0.229489471 percentage points. The independently projected intervals agree with the published extrema. [Follow-up bounds](../results/q4_context_followup_bounds.csv)

| Sample | Minimum (95% simultaneous projection) | Maximum (95% simultaneous projection) |
|---|---:|---:|
| Archived 4,800 pairs | 80.343945% (79.707497%–80.980393%) | 83.810432% (83.173984%–84.446879%) |
| Independent 38,400 pairs | 80.210368% (79.980878%–80.439857%) | 83.899831% (83.670342%–84.129321%) |

The minimum occurs at the same allocation in both samples, with 35% after feeding, 70% commuting and 30% searching. The follow-up minimum interval crosses the inclusive 80% threshold, falling 0.019122 percentage points below it at the lower endpoint. Conditional all-pass remains unresolved. The fixed-model simulation intervals describe Monte Carlo error with the data, fit procedure and exposure scenario held fixed. Field exposure and model uncertainty are outside this calculation.
