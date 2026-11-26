# Q4 envelope-weight attainment

The same 4,800 paired acoustic and whole-date draws supply each comparison. The PAVA score uses envelope weight e and gives each spectral representation weight (1−e)/2. The fixed reference uses full-data clean equal-weight PAVA at 20 m. The weight-specific reference uses the same full-data clean calculation at the evaluated weight. Both keep the clean reference across loss settings. [Frozen specification](model-spec.md#q4-envelope-weight-attainment-freeze)

| Behavior fit | Margin | Fixed reference | Weight-specific reference |
|---|---|---:|---:|
| Full | Clean two-voice net, 150 m | [0, 0.831124] | [0, 1] |
| Full | Coupled two-voice net, 100 m | [0, 0.483958] | [0, 0.857858] |
| Full | Clean modulated gross, 100 m | [0, 0.386488] | [0, 0.546884] |
| Union deletion | Clean two-voice net, 150 m | [0, 0.490312] | [0, 0.751721] |
| Union deletion | Coupled two-voice net, 100 m | [0, 0.293838] | [0, 0.154242] |
| Union deletion | Clean modulated gross, 100 m | [0, 0.372357] | [0, 0.489427] |

The table gives rounded weight intervals with at least 3,840 qualifying draws. Each range is closed. At each interior upper endpoint exactly 3,840 draws qualify, with 3,839 immediately beyond. The five point-margin zeros all occur under the fixed reference, at weights from 0.625021 to 0.842573. All point margins with weight-specific references stay positive. [Full-precision intervals and counts](../results/q4_envelope_attainment_intervals.csv) · [Point zeros](../results/q4_envelope_attainment_zeros.csv)

At e = 0.50 after union deletion, the clean 150 m two-voice margin is positive under either reference. The draw decision depends on the reference, with 3,813 qualifying draws under the fixed reference and 4,048 under the weight-specific reference. For coupled two-voice at 100 m, recalibration narrows the qualifying range after union deletion from 0.293838 to 0.154242. All three focal decisions agree with the released shared-exponent analysis at equal weight under each behavior fit, although attainment counts differ. In particular, clean two-voice at 150 m after union deletion increases from 4,002 to 4,142 qualifying draws when the equal-weight score uses PAVA. The 150 m playback prediction after deletion still extrapolates beyond both arms' retained support. [Five checkpoint weights, point margins, intervals and archived comparisons](../results/q4_envelope_attainment_points.csv)

```sh
python main.py --data "<attachment directory>/date" --q4-envelope-attainment
```
