# Independent verification of Q2 envelope-weight ordering

**Pass.** I reconstructed the available-value means from Data03–Data11 and evaluated the shared envelope-weight path on 16,385 equally spaced weights by the min–max formula for decreasing isotonic fits. I refined each located transition with direct calls to the released Q2 fit and last-qualifying radius functions. The 60 reported checkpoint radii differed by at most 8.53e-14 m and their support statuses matched exactly. [Frozen specification](../docs/model-spec.md#q2-rank-changes-along-a-common-envelope-weight-path) · [Checkpoint radii](../results/q2_envelope_rank_radii.csv)

The direct sweep found six interior transitions. I checked each archived event at its weight and on both available sides. At exact events I snapped fitted knots within 1e-10 of the threshold before selecting the last qualifying knot. The sweep and direct event evaluations agree with the production table, including the endpoint tie. [Event table](../results/q2_envelope_rank_events.csv)

| Fidelity threshold | Compared against two-voice | Envelope weight | Event |
|---:|---|---:|---|
| 0.50 | Modulated | 0.995106 | Interior tie and reversal |
| 0.60 | Modulated | 0.669765 | Interior tie and reversal |
| 0.60 | Flat | 0.749981 | Order reverses just above weight |
| 0.70 | Modulated | 0.342706 | Interior tie and reversal |
| 0.70 | Flat | 0.404520 | Order reverses just above weight |
| 0.70 | Flat | 0.812056 | Both reported radii reach 4 m |
| 0.70 | Flat | 1.000000 | Endpoint still tied at 4 m |

At the two flat-versus-two-voice jumps, both curves have crossing status. The flat and two-voice radii at the exact weights are 32.004 and 64 m at fidelity 0.60 and 31.393 and 64 m at fidelity 0.70. The last-qualifying convention puts the two-voice radius at the end of its threshold plateau. The 4 m tie at fidelity 0.70 is at the reporting boundary. At its entry flat has crossing status and two-voice is below support. At envelope-only weighting both calls are below support. The order is constant across the swept weights at fidelity 0.40.

I regenerated the 300 independent-metric wide-row draws with seed 20261127 and consumed each aligned-draw stream wherever the released Q2 procedure does. Starting at equal weights, 28 draws already favor modulated calls over two-voice at fidelity 0.70, 272 first show a strict lead at a higher weight, and none are right-censored. I refined all observed first leads independently and checked both sides at offsets of 1e-8. All 300 statuses matched exactly. The largest root difference was 2.11e-15. The conditional median and 95% percentile endpoints are 0.343444 [0.334375, 0.355039], with a maximum numerical discrepancy of 1.12e-15. These draws measure sensitivity under representation-wise wide-row resampling. Acquisition-unit identifiers remain unavailable. [Draw results](../results/q2_envelope_rank_draws.csv) · [Bootstrap summary](../results/q2_envelope_rank_bootstrap.csv)

I ran both independent calculations from the repository root. Their scripts and scratch tables are in the local temporary directory.

```powershell
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-verify-q2-envelope.py" "<attachment directory>/date" "$env:TEMP/apmcm-verify-q2-envelope"
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-compare-q2-envelope.py" "<attachment directory>/date" "$env:TEMP/apmcm-verify-q2-envelope"
```
