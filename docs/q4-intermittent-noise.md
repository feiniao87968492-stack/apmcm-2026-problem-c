# Q4 intermittent noise through 100 m

The clean and +6 dB local coupled states use the same 4,800 paired draws, four curves and clean 20 m reference. The table gives the prefix count or expected count for a noisy playback-opportunity fraction f. The rule requires at least 3,840. [Frozen specification](model-spec.md#q4-intermittent-noise-at-100-m-freeze)

| Fit | Rule | f=0 | .25 | .50 | .75 | 1 | Maximum f |
|---|---|---:|---:|---:|---:|---:|---:|
| Full | Opportunity-mean score | 4,776 | 4,728 | 4,607 | 4,233 | 3,230 | 87.38% |
| Full | Continuous, equal mean excess power | 4,776 | 4,691 | 4,462 | 3,971 | 3,230 | 80.55% |
| Full | Opportunity-weighted state indicators | 4,776 | 4,389.5 | 4,003 | 3,616.5 | 3,230 | 60.54% |
| Union deletion | Opportunity-mean score | 4,753 | 4,663 | 4,410 | 3,747 | 2,430 | 72.52% |
| Union deletion | Continuous, equal mean excess power | 4,753 | 4,601 | 4,153 | 3,325 | 2,430 | 61.05% |
| Union deletion | Opportunity-weighted state indicators | 4,753 | 4,172.25 | 3,591.5 | 3,010.75 | 2,430 | 39.30% |

Thresholding the opportunity-mean score lets the clean score offset a noisy deficit within the same draw and node. Averaging indicators gives each opportunity a single state across the prefix and weights the corresponding pass decisions. The resulting expected counts may be fractional. For positive excess the score is proportional to (1+u)/(1+ku), which is convex in the power multiplier k. The opportunity-mean score therefore passes every draw passed by continuous noise at equal mean excess power. Nonpositive excess fails the positive reference under either rule. The four score-rule boundaries have 3,840 passing draws and the next numerical brackets have 3,839. The indicator limits solve the expected count equation directly. [Checkpoint counts](../results/q4_intermittent_noise_checks.csv) · [Boundary brackets](../results/q4_intermittent_noise_limits.csv)

Under the modeled coupling, limiting noisy exposure for individual playback opportunities gives a more restrictive criterion here than either score summary. The results use hypothetical receiver noise and response loss. Interpreting the opportunity share as a time share requires uniform opportunity timing. [Independent numerical review](../reviews/q4-intermittent-noise-verification.md)

    python main.py --data "<attachment directory>/date" --output generated --q4-intermittent-noise
