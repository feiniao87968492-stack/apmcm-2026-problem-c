# Independent manuscript review of the Q4 behavior-model ablation

I reviewed `184d9327fab157933f68d64ba36eb55411e9ce15` under the frozen manuscript rubric. The independent rebuild matches PDF SHA-256 `c57c0fc6e6290610ce119a415d3febd079e1c99a1d063ac6f568b6883594dc15`. [Frozen rubric](../docs/model-spec.md#frozen-independent-paper-rubric)

| Dimension | Score | Evidence |
|---|---:|---|
| Numerical and factual accuracy | 30 / 30 | The published ranks, cutoff decision counts and example at 150 m match the result tables. |
| Traceability | 15 / 15 | The evidence registry links the area means, paired gaps, point decisions and sparse-cell flags. |
| Coverage and reasoning | 30 / 30 | The comparison follows strict holdout evidence and keeps the multinomial model primary. The added results describe Q4 sensitivity under both loss settings. |
| Clarity and structure | 11.25 / 15 | The new paragraph sits together on page 13. The three cutoff definitions and the convention for transferring references across models could be stated directly. |
| Build and references | 10 / 10 | The archive rebuild is byte-identical. All 75 team fields and the PDF author are blank. Body and references occupy pages 3–14, and Appendix A starts on page 15. |

**Initial score 96.25/100, pass.** State explicitly that gross and shared-threshold net use model A's clean cutoff, while each net score also uses its own model-specific clean reference. These definitions make the denominator of 54 decisions clear. [Manuscript source](../paper/results.tex)

## Evidence checks

- Strict date and track holdout gives multinomial, pairwise and smoothed stimulus mask log losses of 1.299, 1.142 and 1.125 respectively. Any-response Brier scores are 0.1698, 0.1681 and 0.1778. These scores motivate the two sensitivity fits. [Strict validation](../results/strict_q3_scores.csv)
- Both scores rank two-voice, modulated, flat in all models under clean and coupled conditions. The pairwise fit changes two decisions and smoothed stimulus frequencies change seven, each out of 54 relative to the multinomial. At the 150 m support boundary the clean gross two-voice attainment is 73.3%, 80.7% and 89.7%. All six local call-by-stimulus cells at that boundary have less than five trials or less than five responses. The stimulus frequency estimates depend only on stimulus type, leaving fidelity to determine the point area ordering. [Area means](../results/behavior_ablation_area.csv) · [Point decisions](../results/behavior_ablation_points.csv) · [Coverage](../results/behavior_ablation_coverage.csv)
- I built twice with `pdflatex -interaction=nonstopmode -halt-on-error main.tex` and `SOURCE_DATE_EPOCH=1795731780`. I rendered pages 12–14 and checked all sequential extracted page headers. Figure 4 and its caption fit on page 13. Limitations and the reference list fit on page 14. [Reviewed PDF](../paper/main.pdf)

## Targeted re-review

The revised paragraph in `5d58a82` explicitly states that the gross score and shared-reference net score use the primary multinomial's gross cutoff, and that the own net cutoff is recomputed for each model. The paragraph links the 54 decisions to those three conventions. I rebuilt this commit from a separate Git archive. The two-pass result matches SHA-256 `4a46e23b571f145376b431481ba79f7f3a447cfd4b5b2e6ed5454a5d41065839`. The rendered paragraph, Figure 4 and its caption remain together on page 13. Page 14 contains the limitations and references, and Appendix A begins on page 15. All 75 team fields and the author field remain blank. Clarity and structure is now 15/15. **Final score 100/100, pass.** [Final PDF](../paper/main.pdf)
