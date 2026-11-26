# Q1 candidate sets for new recording groups

The split schedule and calibration rules froze at `bfb37d7`. Each test group has a separate fit on six other date-by-location groups and calibration on another nine. All methods share the same fold-specific six-feature logistic probabilities. The five-fold hard-label benchmark remains macro F1 0.314 and two-voice recall 2/24. The top-1 and top-2 results below use the new split schedule. [Frozen specification](model-spec.md#q1-candidate-sets-for-a-held-out-recording-group)

| Rule | Trial coverage | Equal-group coverage | Whole groups | Mean size | Three-label sets | Singleton errors | Two-voice coverage |
|---|---:|---:|---:|---:|---:|---:|---:|
| Top-1 | 42/108 | 40.6% | 2/16 | 1.00 | 0 | 66/108 | 1/24 |
| Top-2 | 78/108 | 66.4% | 3/16 | 2.00 | 0 | Undefined | 8/24 |
| Pooled row 80% | 82/108 | 75.8% | 6/16 | 2.20 | 40 | 10/18 | 12/24 |
| Equal-group 80% | 100/108 | 86.9% | 9/16 | 2.62 | 73 | 2/6 | 20/24 |
| Group maximum 80% | 106/108 | 97.7% | 14/16 | 2.83 | 93 | 1/3 | 24/24 |
| Pooled row 90% | 102/108 | 88.3% | 10/16 | 2.69 | 80 | 2/6 | 21/24 |
| Equal-group 90% | 107/108 | 99.8% | 15/16 | 2.94 | 103 | 1/1 | 24/24 |
| Group maximum 90% | 107/108 | 99.8% | 15/16 | 2.94 | 103 | 1/1 | 24/24 |

Against top-2, group-maximum 80% adds 68.75 percentage points in whole-group coverage (paired 95% interval 43.75 to 87.50), 66.67 points in two-voice coverage (52.17 to 85.20), and 0.83 labels per set (0.69 to 0.96). Resampling the held-out groups preserves the pairing of rules. These intervals condition on the fixed out-of-fold sets. The singleton error denominator can be zero in some resamples, especially when singletons are rare. [Scores and intervals](../results/q1_candidate_sets_summary.csv) · [Paired changes](../results/q1_candidate_sets_paired.csv) · [Group counts](../results/q1_candidate_sets_folds.csv)

The pooled row rule assumes exchangeable rows for its nominal coverage. Within-group dependence can invalidate that assumption. The equal-group rule targets a uniform recording within a new exchangeable group. Each calibration group contributes one tenth of the quantile mass, with the test group's entire tenth at infinity. Under group exchangeability, symmetry gives the marginal guarantee for a uniformly selected recording from the test group. Replacing that group's score distribution with infinity can only increase the threshold relative to a quantile computed with all ten empirical group distributions. The group-maximum rule targets all recordings in a new exchangeable group. With nine calibration groups the 80% and 90% ranks are 8 and 9. At 90% both group rules select the largest calibration score because calibration scores carry exactly 90% of total mass. The pooled row ranks vary from 32 to 68 at 80% and 36 to 76 at 90%. The group guarantees are marginal under label-blind splitting and group exchangeability conditional on fitting. Shared dates or sites can limit exchangeability. Observed two-voice coverage describes these held-out groups. [Split assignments, ranks and thresholds](../results/q1_candidate_sets_thresholds.csv)

```sh
python q1_candidate_sets.py --data "/path/to/C-attachments/date"
```

The default `python main.py --data` workflow also generates the four tables.
