# Q4 context-dependent opportunity exposure through 100 m

The context weights for after feeding, commuting and searching are 36, 65 and 38 of 139 observed pairs. For each context and state, the analysis counts draws that pass all four curves at every half-metre node from 20 to 100 m with eight birds. Each draw retains the full-data, context-standardized, clean isotonic net reference at 20 m. Thresholding each context before combining its indicators gives a different estimand from thresholding after standardizing responses. [Frozen design](model-spec.md#q4-context-dependent-intermittent-exposure-freeze)

| Fit | After feeding clean / noisy | Commuting clean / noisy | Searching clean / noisy | Responses aggregated before scoring |
|---|---:|---:|---:|---:|
| Full | 4,707 / 2,884 | 4,592 / 2,702 | 4,785 / 4,369 | 4,776 / 3,230 |
| Union deletion | 4,494 / 1,309 | 4,439 / 2,224 | 4,765 / 4,253 | 4,753 / 2,430 |

Each count uses 4,800 draws. The last column reproduces the archive. For each fit, the allocation uses the same predicted responses throughout. Assigning noisy opportunities first to contexts with the largest clean-to-noisy pass reduction attains the minimum. Assigning them first to contexts with the smallest reduction attains the maximum. Uniform exposure uses the same noisy share in every context. [Counts and pass fractions](../results/q4_context_exposure_counts.csv)

| Fit | Pass fraction at 50% (minimum / uniform / maximum) | Largest noisy share meeting 80% (minimum / uniform / maximum) |
|---|---:|---:|
| Full | 77.74% / 82.08% / 86.41% | 44.16% / 56.78% / 66.39% |
| Union deletion | 66.33% / 73.79% / 81.26% | 22.05% / 35.11% / 52.73% |

All six limits are interior crossings. At a 50% overall noisy share, the full-fit minimum uses 12.5% after feeding, 100% commuting and 0% searching. Its maximum uses 87.5%, 0% and 100%. After deletion, the corresponding allocations are (100%, 51.54%, 0%) and (0%, 48.46%, 100%). The exports report allocations at all five checkpoints and all six limits. [Checkpoints and allocations](../results/q4_context_exposure_checks.csv) · [Exact limits and allocations](../results/q4_context_exposure_limits.csv)

Within 75–125 m, the full fit has 7/6, 12/11 and 6/7 natural/control trials in context order. After deletion those counts are 7/6, 11/11 and 5/6. Searching has no retained trials below 40 m in either arm, so its prefix uses predictions below observed context-specific support. These opportunity shares are hypothetical. Receiver noise and behavioral response to noise have no measured exposure link, and interpreting the shares as time shares requires uniform opportunity timing. [Trial support and response counts](../results/q4_context_exposure_support.csv)

Run the analysis with the contest CSV directory.

    python main.py --data "<attachment directory>/date" --output generated --q4-context-exposure

[Independent verification](../reviews/q4-context-exposure-verification.md)
