# Q3/Q4 playback observation duration

The field protocol records group behavior and vocal activity for one minute from playback onset. Methods and Table 1 define latency from playback start to the first bird in the group showing the scored response. We take the earliest flagged head raise, vocalization or approach, retain zero, and count events on each window boundary. All 172 flagged latencies are finite and span 0–47.8 s. The 60 s counts match the recorded response flags. [Field study, Methods and Table 1](https://doi.org/10.12688/openreseurope.24618.1) · [Frozen design](model-spec.md#q3q4-shortened-observation-freeze)

Risk differences are natural minus control. Changes subtract the 60 s contrast. Brackets give 95% whole-date bootstrap intervals in percentage points. Both samples cover 12 dates.

| Sample | Window (s) | Natural / control events | Risk difference (pp) | Change from 60 s (pp) |
|---|---:|---:|---:|---:|
| 49 matched pairs | 5 | 23 / 7 | 32.65 [19.30, 47.83] | −18.37 [−34.69, −4.76] |
| | 15 | 32 / 8 | 48.98 [36.36, 60.78] | −2.04 [−5.77, 0.00] |
| | 30 | 33 / 8 | 51.02 [36.66, 64.18] | 0.00 [0.00, 0.00] |
| | 60 | 33 / 8 | 51.02 [36.66, 64.18] | Reference |
| 139 pairs | 5 | 74 / 16 | 41.73 [33.77, 50.38] | −10.07 [−18.40, −3.50] |
| | 15 | 89 / 17 | 51.80 [45.33, 59.12] | 0.00 [−2.19, 1.97] |
| | 30 | 90 / 17 | 52.52 [45.61, 60.56] | +0.72 [0.00, 2.29] |
| | 60 | 90 / 18 | 51.80 [45.12, 59.83] | Reference |

At 30 s the primary sample retains every recorded event. This equality holds under every date omission. Across all pairs, 30 s misses one control event and raises the contrast by 0.72 points. At 5 s, omitting any one date leaves the contrast below its 60 s value by 9.76–21.95 points in the matched pairs and by 6.92–12.00 points across all pairs. At 15 s the matched sample misses one natural event, and the sensitivity sample misses one event per arm. These comparisons retrospectively truncate the recorded playbacks. [Counts, paired contrasts and intervals](../results/observation_window_summary.csv) · [Leave-one-date-out estimates](../results/observation_window_leave_date_out.csv)

At 60 s the restricted waiting times average 22.43 s for natural playbacks and 50.49 s for controls in the matched sample. The paired contrast is −28.06 s [−35.10, −20.37], with date-omission estimates from −29.88 to −25.92 s. Across all pairs, the corresponding means are 23.14 and 52.82 s, with a contrast of −29.68 s [−34.05, −25.91] and date-omission estimates from −30.88 to −28.88 s. The restricted mean includes 60 s for each trial without a recorded event and reflects both event occurrence and timing. [Predictive onset comparison](acoustic-onset.md#q3-earliest-recorded-onset)

    python main.py --data "<attachment directory>/date" --output generated --observation-window
