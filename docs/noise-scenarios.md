# Hypothetical noise power and responder counts

The [frozen protocol](model-spec.md#noise-power-and-responder-count-freeze) is at 5a0c8c0. Outputs are at c5fd3fd. A hypothetical 3 or 6 dB increase multiplies the additive noise variance by 2.00 or 3.98, with the signal and fitted ceiling held fixed. The uniform comparator matches the mean relative fidelity loss across calls at 100 m in each acoustic draw. The point matched losses are 15.7% and 32.1%, with conditional 95% intervals of [15.4%, 15.9%] and [31.8%, 32.4%]. [Local and matched losses](../results/noise_q4_losses.csv)

## Radii and attainment

Both loss shapes and response links use the same clean isotonic cutoff and the 20–150 m support range. With 6 dB coupled loss, the two-voice radius is 95.6 m under local attenuation and 29.5 m under matched uniform loss. With date-block draws their respective bounded intervals are 67.0–134.5 m and 20.0–138.8 m. The second interval reaches the lower support boundary.

Among the 72 comparisons matched on noise level, link, resampling scheme, call and distance, 62 agree on the 80% decision. The ten disagreements all favor the local attenuation scenario. At 6 dB coupled loss, modulated and two-voice at 50 m reach the cutoff in every local-attenuation draw, versus 10.7–30.0% under matched uniform loss. Both also change point attainment. Under local attenuation, date draws remove three positive 80% decisions from the experiment-pair results:

| Noise and link | Call and distance | Experiment-pair | Date |
|---|---|---:|---:|
| 3 dB, coupled | Flat at 50 m | 96.3% | 75.3% |
| 6 dB, acoustic-only | Flat at 50 m | 84.7% | 67.7% |
| 6 dB, acoustic-only | Two-voice at 100 m | 89.3% | 74.7% |

The other 33 noisy local-attenuation settings give the same 80% decision under both schemes. [Point margins and support](../results/noise_q4_points.csv) · [Radii, intervals and boundary counts](../results/noise_q4_radii.csv)

## Expected individual responders

For eight birds and probability p of any recorded response, the sharp expected-count bounds are [p, 8p]. A response always involving one bird attains the lower bound and a response always involving all eight attains the upper bound. The independent scenario assumes identical independent individual events. The share scenario assumes a conditional mean of 2, 4 or 6 responders given a positive group response.

| Two-voice at 100 m | Group probability | Sharp bounds | Independent expectation | 25–75% share range |
|---|---:|---:|---:|---:|
| Clean | 0.662 | [0.66, 5.29] | 1.01 | 1.32–3.97 |
| 3 dB coupled | 0.607 | [0.61, 4.85] | 0.88 | 1.21–3.64 |
| 6 dB coupled | 0.532 | [0.53, 4.26] | 0.72 | 1.06–3.19 |

The independent expectation at 6 dB has a date-block interval of 0.43–1.03. These intervals capture fitted group-response variation under the resampling scheme. The sharp interval describes uncertainty about how individual responses combine at any particular group probability. [All assumptions and intervals at 50/100/150 m](../results/noise_q4_responders.csv)
