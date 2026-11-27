# Independent verification of Q1 label errors in Q4 monitoring

**Pass.** I read the frozen input CSVs with `git show 1e12e3a:results/<name>.csv` and reconciled the 108 archived rows on source row, fold, recording group, true label and original logistic decision. The FalseBay subset contains 105 recordings on 15 dates, of which 44 are flat, 40 modulated and 21 two-voice. I independently counted assigned classes within each true class. [Specification](../docs/model-spec.md#q1-labels-in-q4-monitoring-freeze) · [Location predictions](../results/q1_location_predictions.csv) · [Prior correction predictions](../results/q1_class_prior_predictions.csv)

Half of the equally weighted clean 20 m point scores gives the common cutoff 0.28759819888730354. All 18 selected gross point scores and their cutoff flags matched both archived curve exports. The true-label rule has exactly zero bias, false passes and missed passes throughout. [Q4 curves](../results/q4_comparison_curves.csv) · [Figure data](../results/q4_loss_comparison.csv)

| True-label pass sets | 50 m | 100 m | 150 m |
|---|---|---|---|
| Clean | Flat, modulated, two-voice | Modulated, two-voice | Two-voice |
| 20% coupled loss | Modulated, two-voice | Two-voice | None |

I assigned each recording its predicted-class point score and calculated the signed deviation and threshold error indicators directly. For each of the 300 draws, I sampled 15 dates with replacement using seed 20261126 and reused their recording indices across all rules and settings. Every draw retained all three true classes. The 36 confusion rows and 72 monitoring rows in computation commit `29b952b88b4ec48ef45629817e122ada5bdb97fd` match on keys, counts and decisions. All proportions, point estimates and interval endpoints match at absolute tolerance `1e-14`. [Confusion proportions](../results/q1_q4_label_confusion.csv) · [Monitoring estimates and paired intervals](../results/q1_q4_label_monitoring.csv)

At 100 m with coupled loss, the true two-voice score is 0.29706, just above the cutoff. Logistic, full prior correction and XGBoost miss 19/21, 15/21 and 18/21 such passes, respectively. The full correction reduces this missed-pass rate relative to logistic from 90.5% to 71.4%, while increasing false passes from 3/44 to 15/44 for flat and from 3/40 to 9/40 for modulated. Clean 150 m has the same true-label pass set and threshold error rates. All automatic rules raise mean flat scores and lower mean modulated and two-voice scores at each of the six settings.

The calculations transfer FalseBay recording-group confusion to every monitoring setting. The paired intervals condition on the archived predictions, Q4 curves and cutoff. The 150 m result sits at the shared support boundary.
