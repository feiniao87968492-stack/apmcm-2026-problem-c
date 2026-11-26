# Independent review of the Q4 distance deletion manuscript

**Pass, 100/100.** I reviewed commit `ec785cf4523c61b50cac542eb935b514bcfcfd62` under the frozen manuscript rubric. The separate archive build reproduced PDF SHA-256 `71484041597849721f34b67d5a45af3e29c93ee046bcfa4e6236ced917031e09`. [Frozen rubric](../docs/model-spec.md#frozen-independent-paper-rubric) · [Reviewed PDF](../paper/main.pdf)

| Dimension | Score | Basis |
|---|---:|---|
| Numerical and factual accuracy | 30 / 30 | The deletion overlap, model support, cutoff counts and paired margin interval agree with the published outputs. |
| Traceability | 15 / 15 | The claim registry links all four output tables. The 34 tracked Python files each have one complete listing. |
| Coverage and reasoning | 30 / 30 | The paper keeps the four questions and explains distance support and extrapolation for the deletion diagnosis. The language describes sensitivity to the retained observations. |
| Clarity and structure | 15 / 15 | Page 13 keeps the new paragraph and Figure 4 with its caption. Page 14 contains the limitations and full reference list. |
| Build and references | 10 / 10 | The PDF builds byte-for-byte, all team fields and author metadata are blank, and the body with references occupies 12 pages. |

## Evidence checks

The two distance bands select 14 pairs each, with two in both bands and 113 pairs remaining under union deletion. At 150 m, the clean two-voice own-net draw counts are 272, 266, 259 and 239 of 300 for the full, near, far and union fits. The stated percentages round correctly and the final count is one short of 240. Union deletion leaves a maximum observed training distance of 120 m. The paired union-minus-full interval for the margin rounds to [−0.089, 0.022]. The paper explicitly holds the full-data cutoffs and context weights fixed. [Pair overlap](../results/distance_deletion_overlap.csv) · [Retained distances](../results/distance_deletion_training.csv) · [Draw results](../results/distance_deletion_points.csv) · [Claim registry](../claims/claim-registry.md)

## Clean build and source appendix

I extracted a fresh Git archive of the reviewed commit and ran `pdflatex -interaction=nonstopmode -halt-on-error main.tex` twice from `paper/` with `SOURCE_DATE_EPOCH=1795731780`. I checked all 99 sequential PDF headers and blank author metadata, and rendered the affected body and appendix pages. The body and references occupy pages 3–14. Appendices start on page 15 and Listing 34, for the intact-pair distance deletion, spans pages 97–99. A set-and-count comparison of the LaTeX listing paths against the Git tree confirms complete, single coverage. [LaTeX source](../paper/main.tex) · [Reviewed PDF](../paper/main.pdf)
