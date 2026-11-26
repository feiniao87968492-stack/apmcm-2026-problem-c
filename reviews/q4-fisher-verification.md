# Independent verification of Q4 pair allocation

**Pass.** I used the protocol frozen at `2fc20af` and constructed the verification before opening the production implementation. I compared against the two released tables at `bfd73f9`. [Frozen protocol](../docs/model-spec.md#fisher-planning-for-three-q4-margins)

## Point margins, gradients and information

I reconstructed the eight behavior masks and standardized predictor matrix from Data02. The released multinomial specification fitted all eight mask classes. At the fitted model I expressed each of the seven nonzero-mask logits relative to mask zero. For each trial I computed expected information as the probability-weighted outer product of the score for each possible outcome. For each proposed pair I added both arms' information for each context and averaged over the fixed natural-context proportions. I added the unit standardized-slope ridge once in the current information. In baseline-mask coordinates its class factor is \(I_7-\mathbf 1\mathbf 1^\top/8\), obtained by centering the augmented eight-class coefficients. The intercepts carry zero ridge.

I used five-point central differences of each full margin, including the fitted clean reference, and checked the gradients using smaller-step two-point differences. The reference uses the archived isotonic 20 m fidelities. The focal scores use the archived shared-exponent fidelity. The three point margins agree with the archived full fit within \(1.67\times10^{-16}\). Their values are 0.112472954 for clean two-voice own-net at 150 m, 0.047423554 for coupled two-voice own-net at 100 m, and 0.091183655 for clean modulated gross at 100 m. After transforming my independent calculation to the production Helmert coordinates, the maximum gradient difference was \(2.59\times10^{-12}\), the maximum current-information difference was \(6.40\times10^{-14}\), and the maximum difference over all 12 pair-information matrices was \(8.89\times10^{-16}\). [Archived margins](../results/distance_deletion_points.csv)

## Allocations and precision

I re-evaluated all 12 candidate increments at each greedy step using the largest ratio to current-data margin variance. The scores below follow the focal order above. Maximum relative variance refers to the largest of the three ratios.

| Plan | SE for clean two-voice own-net, 150 m | SE for coupled two-voice own-net, 100 m | SE for clean modulated gross, 100 m | Maximum relative variance |
|---|---:|---:|---:|---:|
| Current data | 0.053536 | 0.040035 | 0.065900 | 1.000000 |
| Uniform | 0.037674 | 0.028311 | 0.042423 | 0.500059 |
| Focal only | 0.037471 | 0.030049 | 0.043755 | 0.563346 |
| Unconstrained greedy | 0.034504 | 0.025809 | 0.042478 | 0.415599 |
| Greedy with 10 focal pairs per cell | 0.034604 | 0.025927 | 0.042619 | 0.419388 |

The unconstrained and constrained plans allocate 73 and 66 pairs at 20 m. The focal first and second SEs decrease by 8.42% and 8.84% versus uniform in the unconstrained plan, and by 8.15% and 8.42% in the constrained plan. The third SE increases by 0.13% and 0.46% respectively. All 60 allocation rows match exactly, including focal flags. Across the 15 precision rows the maximum SE difference is \(2.56\times10^{-13}\), and the maximum difference in relative variance or relative gain is \(1.66\times10^{-12}\). These results use fixed acoustics, conditional independence and hypothetical coupling. [Allocations](../results/q4_fisher_allocations.csv) · [Precision](../results/q4_fisher_precision.csv)

## Reproduction

I ran both temporary scripts from the repository root with the contest CSV directory and wrote the independently computed results to the temporary directory.

```powershell
$env:OPENBLAS_NUM_THREADS = '1'
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-q4-fisher-independent.py" "<attachment directory>/date" "$env:TEMP/apmcm-q4-fisher-independent"
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-q4-fisher-compare.py" "<attachment directory>/date" "$env:TEMP/apmcm-q4-fisher-independent"
```
