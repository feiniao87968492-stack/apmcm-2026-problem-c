# Data audit

- Data01 contains 108 recordings in 16 date-by-location groups. There are 44 flat, 40 modulated, and 24 two-voice calls. The second fundamental is missing in 84 recordings. The primary classifier uses the seven complete numeric predictors.
- Data02 contains 278 stimuli in 139 experiment pairs. The natural stimuli comprise 48 flat, 33 modulated, and 58 two-voice calls. Any response is recorded for 90 natural stimuli and 18 controls. Observed playback distances span 5–200 m and median group size is 8.
- Data03–Data11 each contain 300 rows and seven columns for distances from 4 to 256 m. The supplementary method and R code determine the actual resampling unit. Missingness varies with distance and call type, so retain available-case counts beside distance summaries.
- The reported behavior is at the observed-group level. The supplied intensity variables and the latency variables represent different measurements.
- The analyses use the original contest CSV files as inputs. [Archive and supplementary material](https://zenodo.org/records/21376649).

