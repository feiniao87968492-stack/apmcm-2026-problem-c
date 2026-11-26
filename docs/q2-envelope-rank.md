# Q2 radius ranking along the envelope-weight path

For a shared envelope weight (e), each spectral representation receives ((1-e)/2). The point analysis combines available-value means, clips pooled similarities to [0,1], fits decreasing PAVA and interpolates the last qualifying distance in log distance. The protocol froze at `c19d712`. [Specification](model-spec.md#q2-rank-changes-along-a-common-envelope-weight-path)

| Fidelity | e = 0 | e = 0.10 | e = 1/3 | e = 0.50 | e = 1 |
|---|---|---|---|---|---|
| 0.40 | 139.89 / 200.31 / 233.08 | 132.02 / 195.46 / 224.44 | 113.47 / 181.74 / 203.89 | 99.02 / 169.19 / 188.91 | 51.77 / 113.39 / 142.94 |
| 0.50 | 108.93 / 167.31 / 196.97 | 102.05 / 161.26 / 188.86 | 84.72 / 144.56 / 169.73 | 71.27 / 129.83 / 155.91 | 35.70 / 82.46 / 81.75 |
| 0.60 | 85.77 / 139.75 / 166.46 | 79.25 / 133.04 / 158.93 | 62.56 / 109.16 / 141.29 | 45.63 / 93.28 / 128.68 | 19.28 / 26.58 / 9.81 |
| 0.70 | 67.54 / 106.79 / 140.67 | 57.44 / 96.92 / 133.74 | 35.38 / 77.70 / 79.27 | 25.53 / 66.77 / 12.11 | <4 / 9.50 / <4 |

Radii are in metres, ordered flat, modulated and two-voice. A value below 4 m is recorded as the 4 m lower support bound in the CSV. [Point radii and support flags](../results/q2_envelope_rank_radii.csv)

| Fidelity | Pair | Envelope weight | Order as weight increases |
|---|---|---:|---|
| 0.50 | Modulated and two-voice | 0.995106 | Two-voice lead, equality, modulated lead |
| 0.60 | Modulated and two-voice | 0.669765 | Two-voice lead, equality, modulated lead |
| 0.60 | Flat and two-voice | 0.749981 | Two-voice leads at this weight, then flat leads |
| 0.70 | Modulated and two-voice | 0.342706 | Two-voice lead, equality, modulated lead |
| 0.70 | Flat and two-voice | 0.404520 | Two-voice leads at this weight, then flat leads |
| 0.70 | Flat and two-voice | 0.812056 | Flat lead becomes a 4 m reported tie that persists through e = 1 |

At fidelity 0.40 the point order is two-voice, modulated, flat throughout. Modulated stays ahead of flat at all four thresholds. Both switches involving flat at 0.60 and 0.70 occur when the two-voice fitted plateau over 32–64 m equals the threshold. The last-qualifying convention gives 64 m at the switch itself, then the radius drops on its right. The final tie compares support bounds. [Exact event weights, point radii and side order](../results/q2_envelope_rank_events.csv)

Of 300 released wide-row draws at fidelity 0.70, 28 already put modulated ahead of two-voice at e = 1/3. The other 272 first show a modulated lead above that starting weight, with a conditional median of 0.343444 and a central 95% range of 0.334375–0.355039. Zero draws are right-censored at e = 1. These are sensitivity results under a common representation-weight path and the released within-representation wide-row resampling assumption. Independent acquisition units are unavailable. [First reversal by draw](../results/q2_envelope_rank_draws.csv) · [Bootstrap summary](../results/q2_envelope_rank_bootstrap.csv)

Run `python main.py --data "<attachment directory>/date"` to reproduce all four tables. The default run carries forward the 300 released independent-metric draws from Q2.
