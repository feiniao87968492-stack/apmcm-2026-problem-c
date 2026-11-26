# Q2 spectral allocation sensitivity

Let e be the envelope weight and s the spectrogram share of the remaining weight. The two spectral weights are (1−e)s for spectrogram and (1−e)(1−s) for amplitude spectrum. All call types use the same weights. The fits use available-value means, clipping, decreasing PAVA and the last qualifying log-distance radius. [Frozen protocol](model-spec.md#q2-spectral-allocation-sensitivity-freeze)

| Spectrogram share s | 0.70 modulated ties two-voice at e | Flat moves ahead of two-voice just above e | Flat and two-voice enter reported 4 m tie at e |
|---:|---:|---:|---:|
| 0.00 | 0.347216 | 0.408724 | 0.817159 |
| 0.25 | 0.344771 | 0.406630 | 0.814643 |
| 0.50 | 0.342706 | 0.404520 | 0.812056 |
| 0.75 | 0.341005 | 0.402395 | 0.809397 |
| 1.00 | 0.339651 | 0.400255 | 0.806661 |

At fidelity 0.70, modulated takes the lead after the first crossover on each path. The five crossover weights span 0.339651–0.347216, all above equal envelope weight. At the flat–two-voice switch, two-voice still has a last qualifying radius of 64 m at the exact weight. The flat lead starts immediately beyond it. The reported 4 m tie persists to the envelope-only endpoint. At fidelity 0.40, every path keeps two-voice > modulated > flat. [Pair events and one-sided states](../results/q2_spectral_allocation_events.csv) · [Checkpoint radii and support flags](../results/q2_spectral_allocation_radii.csv)

On the continuous slice at e = 1/3, the same strict order holds throughout at both thresholds. At fidelity 0.70 the two-voice lead over modulated is 2.91 m at s = 0, 1.57 m at s = 0.50 and 0.87 m at s = 1. The slice has no strict change of leader, so no spectral weight transfer within it produces a reversal. The frozen condition for reusing the 300 draws on this slice was a point leader change. These results describe the available-value isotonic common-weight sensitivity. [Fixed-envelope decision](../results/q2_spectral_allocation_slice.csv)

Run `python main.py --data "<attachment directory>/date"` to generate the three tables.
