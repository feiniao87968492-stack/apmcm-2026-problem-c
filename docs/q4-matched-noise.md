# Q4 local and matched uniform noise

The earlier gross-score comparison at 6 dB gave two-voice radii of 95.6 and 29.5 m under local and uniform loss. Here the criterion uses the signed net score and requires all four curves at every node of the same draw. The shared-exponent noise-to-clean fidelity ratio multiplies each clean curve. The uniform ratio is the local two-voice ratio at 100 m in that draw. Coupling applies the same ratio to positive natural-minus-control response excess. Both use the common clean 20 m cutoff. [Frozen specification](model-spec.md#q4-local-versus-matched-uniform-noise-freeze)

| Behavior fit | Loss link | 100 m limit, local / uniform (dB) | 3 dB radii, local / uniform (m) | 6 dB radii, local / uniform (m) |
|---|---|---:|---:|---:|
| Full | Acoustic only | 6 cap / 6 cap | 150 cap / 150 cap | 119.5 / 137.5 |
| Full | Coupled | 5.316405 / 5.279167 | 126.5 / 150 cap | 93.5 / 79 |
| Union deletion | Acoustic only | 6 cap / 6 cap | 127.5 / 135 | 107.5 / 112 |
| Union deletion | Coupled | 4.502439 / 4.456254 | 112.5 / 120.5 | 89 / 72.5 |

All 50 m comparisons reach the 6 dB search cap. At 100 m under 6 dB coupled loss, local and uniform counts are 3,230 and 3,168 with the full fit and 2,430 and 2,330 after deletion, all below 3,840. The curves agree at the target because they match there. Their prefix counts still differ because the shorter nodes use different losses. The four solved limits are reported as passing lower brackets, with 3,840 draws at the passing end and 3,839 at the failing end, less than 1e-9 dB apart. [Target counts and limits](../results/q4_matched_noise_targets.csv) · [Grid radii and boundary counts](../results/q4_matched_noise_radii.csv)

Under 6 dB coupled loss the local radius exceeds the matched uniform radius by 14.5 m with full training and 16.5 m after deletion. Under 6 dB acoustic-only loss, the matched uniform radii extend farther. The 50 and 100 m targets lie within both retained arms' ranges. After deletion the natural and control ranges are 20–100 and 5–120 m. Radii that exceed those maxima use extrapolated behavior in the respective arms. The dB mapping comes from the hypothetical noise-power model. [Retained distances](../results/q4_consecutive_ranges.csv)

Run `python main.py --data "<attachment directory>/date" --q4-matched-noise` to reproduce the tables.
