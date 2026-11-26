# Creative modeling independent numerical review

**Verdict PASS.** I independently reconstructed the calculations at commit `5a00f56` from the frozen rules at `b47de34` and the original Data01–Data11 attachments. The verification used standalone Python and library routines without importing the production modeling modules. The checks support the prespecified model dispositions.

## Q1 blocked Fpeak association

I rebuilt the 16 date-by-site group IDs and verified all 64 group-by-test rows against the attachment. Eleven groups contribute to the rank omnibus. Its statistic is 8808.5, with Monte Carlo p=0.0017 and Holm p=0.0052. All four 9,999-permutation p values, the three 300-draw group-bootstrap intervals and the Holm adjustments reproduced.

| Contrast | Contributing groups | Difference in Hz | 95% group interval in Hz | Holm p |
|---|---:|---:|---:|---:|
| Flat minus modulated | 8 | 206.92 | [61.09, 292.29] | 0.0100 |
| Flat minus two-voice | 5 | 297.85 | [150.54, 453.98] | 0.0052 |
| Modulated minus two-voice | 6 | 32.15 | [−201.99, 203.60] | 0.7562 |

Keep the association exploratory because Fpeak was chosen after the earlier analysis. [Tests](../results/creative_q1_fpeak_tests.csv) · [Group evidence](../results/creative_q1_fpeak_groups.csv)

## Q3 structured mask models

I rebuilt all five held-out folds from expID with the 139 pairs intact, refit the three released comparators, and fit both structured variants using a dense mask design and BFGS. The maximum absolute difference across 1,390 exported probability rows was 2.68e-6. The 300 paired scoring draws reproduced the comparison intervals within 2e-6, and 300 intact-pair interaction refits reproduced the coefficient interval endpoints within 2e-5.

The pairwise model gives mask log loss 1.09471 and Brier 0.15486. Its differences versus the interaction-free model are −0.04010 [−0.06863, −0.01298] and −0.00885 [−0.01416, −0.00376]. Against the full multinomial, the differences are −0.15024 [−0.40896, −0.02790] and +0.00071 [−0.00640, +0.00704]. The mask-loss difference against empirical stimulus frequencies also has an interval containing zero. The pairwise model misses the joint adoption rule. Head–vocal and head–approach conditional log-odds-ratio intervals lie above zero. Vocal–approach spans zero. [Paired scores](../results/creative_q3_comparison.csv) · [Probabilities](../results/creative_q3_oof.csv) · [Conditional associations](../results/creative_q3_interactions.csv)

## Q4 fitted smooth gate

I reconstructed the three propagation curves from available-case means, verified 252 eligible held-out rows across 135 experiments, and refit the two background/excess versions using numerical-gradient BFGS. All fold scores and 300 paired-draw intervals reproduced within 2e-6, as did the 18 standardized representative rows. The published binary baseline, ungated excess and gated versions give binary loss/Brier of 0.49059/0.15567, 0.47325/0.14780 and 0.50747/0.16335. The smooth gate's Brier difference against the ungated excess is +0.01555 [0.00211, 0.02621]. The smooth gate misses the frozen joint rule. Its center and slope are specified scenario inputs. [Published binary comparison](../results/creative_gate_vs_binary_comparison.csv) · [Ungated comparison](../results/creative_gate_vs_ungated_comparison.csv) · [Representative predictions](../results/creative_gate_representative.csv)

## Q4 loss inversion

I reconstructed all 300 propagation bootstrap draws with independent adjacent-block pooling and all 300 behavior draws with independent intact-pair refits. Scalar root finding at the draw-specific common cutoff independently reproduced all 18 output rows after rounding down to the loss grid. I checked both margins, both support fractions, point and 80% support limits, clean failures, ceiling statuses, and bounded percentile endpoints.

At 50 m the 80% limits for flat are 18.0% acoustic-only and 10.4% coupled. Modulated and two-voice reach the 20% search ceiling under both links at 50 m. At 100 m, the modulated limits are 9.0% and 5.0%. Two-voice reaches the ceiling under acoustic-only loss and has a 16.4% coupled limit. At 150 m, the two-voice limits are 9.7% and 5.2%. Flat at 100 and 150 m and modulated at 150 m fail the 80% criterion in clean conditions. The limits express conditional support under each specified loss link and the finite search domain. [Inverse scenarios](../results/creative_q4_inverse_loss.csv)
