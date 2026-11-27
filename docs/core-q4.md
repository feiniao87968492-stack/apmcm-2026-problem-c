# Core Q4 aligned propagation and playback scenarios

The default pipeline passes the selected partially pooled Q2 curve to Q4. The point scenarios cross selected and archived acoustic curves with selected and archived mask models. The Q3 mask comparison retained the full multinomial, so the behavior substitution gives identical curves. Each comparison at a fixed distance uses the same covariate standardization, loss assumptions and archived clean gross cutoff of 0.287598. [Frozen design](model-spec.md#core-upgrade-q1-and-integrated-q4-freeze) · [Dense component comparisons](../results/core_q4_curves.csv)

| Call | Archived gross, clean / 20% coupled loss (m) | Aligned gross, clean / 20% coupled loss (m) | Aligned joint 30 s, clean / 20% coupled loss (m) |
|---|---:|---:|---:|
| Flat | 82.4 / 41.8 | 82.4 / 46.3 | 84.5 / 58.0 |
| Modulated | 139.3 / 77.2 | 139.0 / 81.6 | 143.5 / 107.5 |
| Two-voice | ≥150 / 116.2 | ≥150 / 117.4 | ≥150 / 132.0 |

The conjunctive rule requires fidelity and the probability of a recorded natural response by 30 s to each reach 0.50 at every half-metre node from 20 m. The selected timing distribution pools calls and distances within stimulus. Its clean natural risks are 0.6373 at 15 s and 0.6479 at 30 s. The coupled-loss risks are 0.5359 and 0.5451, respectively. Both remain above 0.50 throughout the grid, so the joint results for 15 s and 30 s coincide and the fidelity threshold sets the reported limits. The gross rule uses the distance-dependent multinomial. These point scenarios use 150 m as the common upper evaluation boundary. Local playback evidence is sparse for some calls near that boundary. [Radii and status](../results/core_q4_radii.csv) · [Local support](../results/core_q3_support.csv)

Run the current production comparisons and figures with `python main.py --data "<attachment directory>/date" --output generated`. Use `--archived` for the previous full pipeline and `--help` to list the historical named analyses. The paired uncertainty analyses in the archive remain available as conditional sensitivity evidence.
