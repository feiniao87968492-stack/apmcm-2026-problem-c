# Fisher planning for the Q4 margins

The design froze at `2fc20af` and was evaluated at `bfd73f9`. Each cell is one call type and one common natural/control distance. The 120 pairs have equal cost. Fisher information uses conditional independence of the two arms, with the released multinomial ridge curvature counted once. The fitted gross and own-net cutoffs enter the margin gradients. Acoustics are fixed and the 20% coupling is hypothetical. [Frozen protocol](model-spec.md#fisher-planning-for-three-q4-margins)

The vectors below give pair counts at 20, 50, 100 and 150 m, in order.

| Plan | Flat | Modulated | Two-voice |
|---|---|---|---|
| Uniform | 10, 10, 10, 10 | 10, 10, 10, 10 | 10, 10, 10, 10 |
| Focal only | 0, 0, 0, 0 | 0, 0, 40, 0 | 0, 0, 40, 40 |
| Greedy | 29, 0, 0, 0 | 21, 14, 0, 10 | 23, 0, 0, 23 |
| Greedy with at least 10 per focal cell | 31, 0, 0, 0 | 14, 12, 10, 4 | 21, 0, 10, 18 |

| Plan | Clean two-voice own-net, 150 m | Coupled two-voice own-net, 100 m | Clean modulated gross, 100 m | Largest relative variance |
|---|---:|---:|---:|---:|
| Current data | 0.05354 | 0.04004 | 0.06590 | 1.0000 |
| Uniform | 0.03767 | 0.02831 | 0.04242 | 0.5001 |
| Focal only | 0.03747 (+0.54%) | 0.03005 (−6.14%) | 0.04376 (−3.14%) | 0.5633 |
| Greedy | 0.03450 (+8.42%) | 0.02581 (+8.84%) | 0.04248 (−0.13%) | 0.4156 |
| Greedy with at least 10 per focal cell | 0.03460 (+8.15%) | 0.02593 (+8.42%) | 0.04262 (−0.46%) | 0.4194 |

Parentheses give percentage SE reduction versus uniform. The greedy rule targets the largest variance relative to its current-data value, so the modulated margin can have a slightly higher SE even as the largest relative variance falls. The greedy plans assign 73 and 66 pairs to 20 m, respectively, where new measurements also inform the clean cutoffs. These are local planning SEs under the stipulated information model. [Allocation counts](../results/q4_fisher_allocations.csv) · [Precision and gains](../results/q4_fisher_precision.csv)

From the repository root, use `python q4_fisher.py --data "<attachment directory>/date"` with the released result tables under `results/`. Use `--output` to write to a separate directory.
