# Independent creative-modeling manuscript review

I reviewed manuscript commit `14db7439f200c1bbd2d5e7f9de910f499356f23f`, with outputs from `5a00f56` and specification `b47de34`. The reviewed PDF SHA-256 is `8b0fd88b0b0850f6e72ac65caedee6f7826b13a3d6ee7072163c4a3429cb17d3`. [Frozen rubric](../docs/model-spec.md#frozen-independent-paper-rubric) · [Creative protocol](../docs/model-spec.md#creative-modeling-freeze)

| Dimension | Score | Review evidence |
|---|---:|---|
| Numerical and factual accuracy | 30 / 30 | The reported blocked contrasts, co-occurrence estimates, held-out scores and inverse-loss limits agree with the output precision and rounding. |
| Traceability | 11.25 / 15 | The matching CSVs and source appendix are available. The initial claim registry predates the four new analyses. |
| Coverage and reasoning | 30 / 30 | The manuscript explains the retained models, the grouped comparisons and the scenario interpretation of the gate and inverse limits. |
| Clarity and structure | 11.25 / 15 | Main figures and the new table fit on individual pages. The summary omits the new headline findings and the excess fit needs a more precise likelihood description. |
| Build and references | 10 / 10 | Two successful LaTeX passes reproduced the PDF text and pagination. All 45 visible team identifiers and author metadata are blank. The body and references occupy pages 3–10 and the appendix begins on page 11. |

Initial score **92.5/100**. The review found no hard failure.

## Results cross-checked

- **Q1.** The 11 informative blocks, pair sample sizes, Holm p values and intervals match the blocked analyses. The two positive flat-call contrasts are 206.9 and 297.9 Hz. The contribution attributed to group 14 is its normalized weighted contribution to each estimate. The paper describes feature selection from earlier results as exploratory. [Blocked tests](../results/creative_q1_fpeak_tests.csv) · [Group contributions](../results/creative_q1_fpeak_groups.csv)
- **Q3.** The mask equation gives a softmax model with three constant pairwise coefficients and reproduces the conditional log-odds interpretation. Against the ablation, mask loss decreases by 0.0401 and Brier by 0.0089, with both paired intervals below zero. Under the full-model comparison, the mask-loss improvement is 0.1502 and the Brier interval includes zero. The empirical-frequency mask-loss interval also includes zero. The manuscript's retained full model follows the frozen rule. [Paired comparisons](../results/creative_q3_comparison.csv) · [Interaction estimates](../results/creative_q3_interactions.csv)
- **Q4 gate.** The center and width in the equation agree with the frozen sensitivity. The gate, ungated excess, and released binary logit score pairs match the CSVs. The positive gate-minus-ungated Brier interval rules out the specified joint adoption. The paper treats attenuation as a scenario assumption. [Released-binary comparison](../results/creative_gate_vs_binary_comparison.csv) · [Ungated comparison](../results/creative_gate_vs_ungated_comparison.csv)
- **Q4 inverse.** All 18 cells after separating the two links agree with the loss inversion rows. The six clean failures and the capped values are distinguishable. The 150 m two-voice acoustic-only point margin at 20% is 0.0062, with 58.7% draw support. Under coupling the point cutoff is 12.2% and the 80% support limit is 5.2%. The paper ties these limits to the original scenarios. [Inverse grid results](../results/creative_q4_inverse_loss.csv)

## Targeted edits

1. Add the four creative analyses to the claim registry so that the new manuscript numbers can be traced directly to the supporting CSVs. [Claim registry](../claims/claim-registry.md)
2. Clarify that the control background is fit on control trials, then the excess predictor is fit on natural trials with the background held fixed in the Bernoulli mean. This states how the constrained response probability enters the likelihood. [Gate methods](../paper/main.tex)
3. Include the pairwise model's main held-out trade-off and the 150 m inverse loss limits in the summary to surface the new results. [Results and summary](../paper/results.tex)

## Targeted re-review

Revised manuscript commit `6f859dc`. The released PDF SHA-256 is `5222a9ca1834357edf7c76d536772812087ae40b1c3026c8cdacb3a4d49cdaa6`.

All three edits are closed. The new claim-registry rows point directly to each analysis. The methods describe fitting the background on control trials and the natural-trial likelihood conditional on that background. The summary states the blocked peak-frequency finding, the pairwise mask-loss improvement with similar Brier scores, and the 150 m two-voice loss limits of 9.7% and 5.2% under the respective scenarios. I inspected the rendered summary and confirmed blank author metadata and anonymous headers across all 45 pages. [Claim registry](../claims/claim-registry.md) · [Revised methods](../paper/main.tex) · [Revised summary](../paper/results.tex)

| Dimension | Revised score |
|---|---:|
| Numerical and factual accuracy | 30 / 30 |
| Traceability | 15 / 15 |
| Coverage and reasoning | 30 / 30 |
| Clarity and structure | 15 / 15 |
| Build and references | 10 / 10 |

**PASS, 100/100.** The revised manuscript meets the frozen acceptance threshold and closes all review items.
