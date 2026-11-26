# Attenuation curves and acquisition-batch sensitivity

The protocol was frozen at 92e3265. Outputs are at 1284ba2. The shared-exponent curve is adopted for Q2 distance prediction under the frozen interior-distance test. The archived isotonic scenarios remain the Q4 reference for the fixed-cutoff comparison.

| Fit | Pooled RMSE | Pooled MAE | Flat RMSE | Modulated RMSE | Two-voice RMSE |
|---|---:|---:|---:|---:|---:|
| Isotonic with log-distance interpolation | 0.06816 | 0.05675 | 0.04851 | 0.06569 | 0.08525 |
| Fixed exponent 2 | 0.06034 | 0.05243 | 0.03131 | 0.05647 | 0.08219 |
| Shared fitted exponent | 0.05526 | 0.04891 | 0.04755 | 0.04735 | 0.06824 |

The pooled RMSE falls 18.9% relative to isotonic with all call-specific RMSEs lower. The fitted exponent 2.8585 describes the shape of the equal-weight correlation curves. At fidelity 0.50 the ranges are 88.3, 142.9 and 167.2 m for flat, modulated and two-voice, respectively. The 0.70 point ordering changes to modulated > two-voice > flat, with overlapping modulated and two-voice intervals. [Validation](../results/physical_q2_validation.csv) · [Fits](../results/physical_q2_parameters.csv) · [Fitted radius intervals](../results/physical_q2_radii.csv)

Hypothetical batches of ten adjacent rows widen all twelve isotonic 95% radius intervals. At 0.50, the modulated interval goes from [142.27, 147.05] to [138.78, 150.21] m. The strict point order is retained in all draws at thresholds 0.40, 0.50 and 0.60 under both schemes. At 0.70 it is retained in 272/300 row draws and 197/300 block draws. These results are conditional on file order and the imposed batch structure. [Full resampling comparison](../results/physical_q2_blocks.csv)

## Q4 fixed-reference comparison

Both propagation fits use the same behavior predictions and the isotonic common cutoff of 0.28760, with its original draw-specific values. The three changes in the 27 settings are:

| Setting at 20% loss | Isotonic margin | Shared-exponent margin | Paired difference, 95% interval | Attainment share |
|---|---:|---:|---|---:|
| Flat at 50 m, acoustic-only | +0.0242 | +0.0526 | +0.0284 [0.0218, 0.0340] | 72.7% to 91.7% |
| Two-voice at 150 m, acoustic-only | +0.0062 | −0.0068 | −0.0130 [−0.0162, −0.0095] | 58.7% to 44.7% |
| Flat at 50 m, coupled | −0.0230 | +0.0012 | +0.0241 [0.0184, 0.0290] | 16.0% to 43.3% |

The first setting gains 80% attainment. The other two change point attainment, with draw shares below 80% under both fits. All clean decisions agree. [All Q4 margins and decisions](../results/physical_q4_margins.csv)
