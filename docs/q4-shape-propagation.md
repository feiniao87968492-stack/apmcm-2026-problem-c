# Q4 attenuation-shape propagation

All four equal-weight acoustic fits use the same 4,800 paired acoustic and whole-date draws. Every point or draw uses the full-data clean 20 m isotonic reference, shared across score shapes and behavior fits. Behavior predictions and the positive-excess coupling rule are common across shapes. [Frozen specification](model-spec.md#q4-attenuation-shape-propagation-freeze)

| Behavior fit | Focal case | Isotonic | Fixed exponent 2 | Shared exponent | Separate exponents |
|---|---|---:|---:|---:|---:|
| Full | Clean two-voice net, 150 m | 4,593 | 4,468 | 4,527 | 4,638 |
| Full | Coupled two-voice net, 100 m | 4,215 | 3,773 | 4,116 | 4,381 |
| Full | Clean modulated gross, 100 m | 3,949 | 3,747 | 4,074 | 4,129 |
| Union deletion | Clean two-voice net, 150 m | 4,142 | 3,858 | 4,002 | 4,261 |
| Union deletion | Coupled two-voice net, 100 m | 3,722 | 3,039 | 3,575 | 4,034 |
| Union deletion | Clean modulated gross, 100 m | 3,927 | 3,708 | 4,049 | 4,119 |

Counts at or above 3,840 satisfy the 80% rule. Relative to shared exponents, separate exponents change one decision. For coupled two-voice net at 100 m after union deletion, fidelity rises from 0.66347 to 0.71066 (paired difference 0.04719, 95% percentile interval 0.04517 to 0.04918). The margin rises from 0.02422 to 0.03977 (paired difference 0.01555, interval 0.01111 to 0.02032). Attainment rises from 74.48% to 84.04%, with 459 draws gaining attainment and zero losing it. The fixed exponent changes three decisions from passing to failing. Isotonic gives the same six decisions as the shared exponent. All four shapes pass the clean two-voice decision at 150 m for both behavior fits. These results condition on the score model and paired resampling. Union-deleted behavior predictions at 150 m extrapolate beyond both arms' retained distances. [Fidelities, point margins, paired deltas and decisions](../results/q4_shape_propagation.csv)

```sh
python main.py --data "<attachment directory>/date" --q4-shape-propagation
```
