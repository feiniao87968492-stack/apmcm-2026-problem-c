# Q2 forward-distance validation

For each target, all three calls are held out at that distance. The fits use only shorter measured distances and the same equal-weight available-case fidelity. Isotonic prediction carries forward the final fitted knot. Errors are prediction minus observation. [Frozen design](model-spec.md#q2-forward-distance-validation-freeze)

| Model | RMSE at 64 m | RMSE at 128 m | RMSE at 256 m | Pooled RMSE at 128 and 256 m |
|---|---:|---:|---:|---:|
| Isotonic carry-forward | 0.07619 | 0.18467 | 0.29889 | 0.24843 |
| Fixed exponent two | 0.14537 | 0.06889 | 0.14862 | 0.11583 |
| Shared exponent | 0.12492 | 0.08434 | 0.13467 | 0.11236 |
| Separate exponents | 0.30479 | 0.10586 | 0.11126 | 0.10859 |

The primary pool weights the six call-distance cells equally. Separate minus shared RMSE is -0.00376 (paired 95% interval -0.00883 to 0.00355), so the forward comparison does not establish the advantage seen in interior interpolation. Separate exponents have higher RMSE at 128 m and lower RMSE at 256 m than shared exponents. Fixed exponent two has the lowest point RMSE at 128 m. Isotonic carry-forward has the lowest point RMSE in the 64 m sensitivity. The primary pooled signed errors are +0.22859, +0.09143, +0.09302 and +0.01730 in table order. [Signed errors by cell](../results/q2_forward_holdouts.csv) | [Grouped errors and RMSE](../results/q2_forward_scores.csv) | [Paired contrasts](../results/q2_forward_contrasts.csv)

At 128 m, each of the spectrogram, amplitude-spectrum and envelope files has 190 of 300 available rows for two-voice, compared with 230 for each other call. Their equal-weight two-voice observation is 0.65385. The 300 common draws independently resample whole wide rows by file and recompute training and held-out observations together. Intervals condition on the available rows and the row-resampling convention. Acquisition groups are unknown. The interior result still describes prediction with measurements on both sides. The forward results cover only the tested steps within the measured distance series. [Support by representation](../results/q2_forward_support.csv)

Run from the repository root with the contest CSV directory.

    python main.py --data "<attachment directory>/date" --output generated --q2-forward

[Independent numerical review](../reviews/q2-forward-verification.md)
