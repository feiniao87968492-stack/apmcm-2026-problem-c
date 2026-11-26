# Independent verification of Q2 spectral allocation sensitivity

**Pass.** I reconstructed the available-value means from Data03–Data11. At each of the six frozen paths I evaluated the decreasing isotonic fit by its min–max formula at 16,385 equally spaced coordinates, then refined changes with the released direct Q2 fits. I verified all 120 reported checkpoint radii, support statuses and leaders. The largest radius difference was 8.53e-14 m. [Frozen specification](../docs/model-spec.md#q2-spectral-allocation-sensitivity-freeze) · [Checkpoint radii](../results/q2_spectral_allocation_radii.csv)

At fidelity 0.70 the two-voice-to-modulated crossover weights on the five fixed-spectral-share paths are as follows. At the crossing the reported radii are equal and modulated leads immediately above it. [Pair events](../results/q2_spectral_allocation_events.csv)

| Spectrogram share of spectral weight | Envelope crossover weight |
|---:|---:|
| 0 | 0.347216 |
| 0.25 | 0.344771 |
| 0.50 | 0.342706 |
| 0.75 | 0.341005 |
| 1 | 0.339651 |

All 20 reported events match direct ranks at the event and on each available side, including 15 interior changes and five endpoint ties. Interior event locations differ by at most 9.00e-15. On each path, the flat versus two-voice order also changes immediately above a two-voice threshold plateau, then both reported radii reach the 4 m boundary at a larger envelope weight. A direct table comparison at equal spectral share reproduced all 18 overlapping checkpoint rows and all four earlier event rows to 1e-12. [Pair events](../results/q2_spectral_allocation_events.csv) · [Equal-spectral reference](../results/q2_envelope_rank_events.csv)

At envelope weight one third, two-voice leads across the full spectral slice at both fidelity thresholds. Its smallest sampled lead over the next call was 21.970 m at 0.40 and 0.872 m at 0.70, matching the absence of a pair event on either exact slice. The frozen conditional resampling criterion is unmet, so the spectral slice reports the two no-switch cases. The results describe sensitivity to common representation weights. [Fixed-envelope slice](../results/q2_spectral_allocation_slice.csv)

I ran the independent calculations from the repository root. Both scripts and scratch tables are in the local temporary directory.

```powershell
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-verify-q2-spectral.py" "<attachment directory>/date" "$env:TEMP/apmcm-verify-q2-spectral"
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-compare-q2-spectral.py" "<attachment directory>/date" "$env:TEMP/apmcm-verify-q2-spectral"
```
