# Independent numerical verification of Q4 extrapolation sensitivity

**Pass.** The sampled support is the binding constraint in all three scenarios. The production counts and binding labels matched exactly. Across the point and joint limits, odds factors, probability shifts and boundary margins, the largest absolute difference was 8.89e-15. [Production table](../results/q4_extrapolation_drift.csv)

I reconstructed union deletion directly by discarding every expID with at least one recorded distance of 125 m or more. The 113 retained pairs have two rows each. The retained two-voice maxima are 100 m for natural and 120 m for control. I generated the 4,800 whole-date draws from seed 20261201 in sorted date order and fitted the released multinomial to both intact-pair sets on every draw. I reused the released seed-20261130 acoustic generator and calculated the common own-net cutoff directly as the sum of the three full-data 20 m isotonic fidelity-weighted response differences divided by six. The fit weights use the original empirical natural contexts at eight birds. [Frozen specification](../docs/model-spec.md#q4-extrapolation-drift-freeze)

The clean two-voice union-deletion baseline at 150 m reproduced **4,002/4,800** qualifying draws with zero drift. The point fidelity is 0.5422657768710943, cutoff is 0.1943707143010796, and the point probabilities are 0.5042629441858850 for natural and 0.0447885761706546 for control. The baseline point margin is +0.0547865108230545. The cutoff, probabilities and margin match the archived point to absolute tolerance 1e-12. [Archived point comparison](../results/distance_deletion_points.csv) · [Archived Monte Carlo count](../results/distance_deletion_mc.csv)

| Adverse drift | Point limit | Support limit and joint maximum | Odds factor per doubling | Natural shift at 150 m (pp) | Control shift at 150 m (pp) | Point margin at joint maximum | Count at boundary | Count immediately above |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Natural only | 0.699318912541 | 0.098581825940 | 1.103604704192 | −1.441516906 | 0 | 0.046969657974 | 3,840 | 3,839 |
| Control only | 4.014001695604 | 1.109349739417 | 3.032385912160 | 0 | +1.801689119 | 0.045016567324 | 3,840 | 3,839 |
| Both arms | 0.631711854263 | 0.093045640287 | 1.097511824880 | −1.360586169 | +0.129912601 | 0.046704046089 | 3,840 | 3,839 |

I multiplied natural odds by \(\exp[-\lambda\log_2(1.5)]\) and control odds by \(\exp[+\lambda\log_2(1.25)]\) when each arm was perturbed. I converted these odds back to probabilities and bisected directly on whether the inclusive count reached 3,840. The final passing and failing bounds were within 2e-15 in lambda for all cases. Checking 1e-10 on either side gave the same count transitions. I used a separate scalar Brent solve on the point margin and checked the natural-only and control-only point roots by inverting the odds formulas. Every joint limit is set by the support condition.

The registered interpretation is sensitivity of this fitted decision beyond both arms' retained support. The odds factor is the multiplier on control odds per doubling, with its reciprocal on natural odds in scenarios where each arm is perturbed. Counts and probability changes use the original paired-draw ensemble and the fixed 150 m target.

## Reproduction

I ran the independent calculation from the repository root using the project Python environment. The review script is in the local temporary directory.

```powershell
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-verify-drift.py" "<attachment directory>/date"
```
