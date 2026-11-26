# False Bay sea-state sensitivity

The protocol was frozen at e86dfe1 and run at 7bffe2b. The field study reports 12 playback days in June 2022, between 07:48 and 13:15 and under 10 knots of wind. The date join uses unweighted means of six local hours from 08:00 to 13:00. Across the 12 dates, the reanalysis means range from 1.557 to 6.202 m/s at the atmospheric cell and from 1.433 to 2.810 m at the offshore wave cell. The regional hourly means and field conditions measure different locations and time scales. [Archived sources and grid points](../sources/false-bay/README.md)

## Observed paired outcomes by date

Slopes are percentage-point change in the daily mean of natural minus control per m/s of wind or metre of total significant wave height. Intervals are 95% percentiles over 300 date resamples.

| Eligible pairs | Wind slope [interval] | Wave slope [interval] |
|---|---:|---:|
| All 139 | +3.23 [−5.06, +8.06] | −7.34 [−29.20, +10.89] |
| 49 same-distance | +11.86 [−1.16, +22.36] | +13.41 [−23.60, +64.38] |

All 12 dates contribute to each analysis. The estimated wave slope changes sign in the matched subset, and all intervals span zero. The slopes are exploratory date-level comparisons. [Daily inputs](../results/sea_state_daily.csv) · [Slopes](../results/sea_state_slopes.csv)

## Strict validation

The 12 folds hold out the target date and remove pairs sharing its natural tracks from training. All 278 trials are evaluated. Each augmented fit includes one weather variable and its natural-stimulus interaction. Inputs are standardized on the training fold.

| Model | Binary log loss | Brier | Log loss change [95%] | Brier change [95%] |
|---|---:|---:|---:|---:|
| Baseline | 0.5530 | 0.1789 | Reference | Reference |
| Wind | 0.6130 | 0.1964 | +0.0600 [+0.0140, +0.1229] | +0.0174 [+0.0043, +0.0375] |
| Offshore wave | 0.5434 | 0.1784 | −0.0096 [−0.0542, +0.0464] | −0.0005 [−0.0170, +0.0197] |

Wind worsens both scores. Wave-height intervals span zero. The archived model remains the reference under the joint adoption rule. [Coverage](../results/sea_state_coverage.csv) · [Scores](../results/sea_state_validation.csv)

## Standardized contrasts

Using eight birds and the original context weights, the wind comparison goes from 2.100 to 4.048 m/s and the wave comparison goes from 1.721 to 2.338 m. At 100 m the standardized natural-minus-control gap for two-voice changes by +5.65 percentage points for wind [−9.24, +23.44] and −9.89 for offshore wave height [−26.94, +3.53]. All 18 high-minus-low gap intervals across call, distance and variable span zero. These are associations over the sampled dates and use regional weather proxies. The separate +3 and +6 dB calculations retain their hypothetical interpretation. [Natural and control probabilities and contrasts](../results/sea_state_standardized.csv)
