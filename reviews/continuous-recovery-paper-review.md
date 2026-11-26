# Independent manuscript review for continuous historical recovery

I reviewed `85978889b70c0104891efbfce111152b08b35c12` using the frozen independent paper rubric. The archived-source build reproduced PDF SHA-256 `d240e53793718d5e297d5454bca59148938d47702d8a69f5d574aa772737e233`.

| Dimension | Score | Evidence |
|---|---:|---|
| Numerical and factual accuracy | 30 / 30 | The manuscript's clean baseline width, both minimum shrinkages and both 20% coupled shrinkages match the released values. |
| Traceability | 11.25 / 15 | The detailed report links the new results. The central historical recovery registry lacks the continuous certificate and breakpoint tables. |
| Coverage and reasoning | 30 / 30 | Q1–Q4 remain represented. The paper limits the continuous optimum to historical recovery under the stipulated equal costs and distinguishes the coupled-loss evaluation of the clean winners. |
| Clarity and structure | 11.25 / 15 | A single continuation line from the recovery paragraph opens page 13. Figure 4 and its caption remain together on page 13. |
| Build and references | 10 / 10 | The anonymous PDF builds byte-for-byte. Body and references occupy pages 3–13 and appendices begin on page 14 of 74. |

**Initial score 92.5/100.** The numerical evidence and build pass. Two targeted edits address traceability and placement.

## Evidence checks

The clean baseline width is 0.457352682. The one- and two-unit plans reduce it by at least 41.4467% and 73.5055%, matching the released three-value minima. Their continuous minima exceed the largest competing three-value upper bounds by 0.042935669 and 0.072623268. Under 20% coupled loss the corresponding reductions are 41.4824% and 73.4325%. Seven of the nine discrete assignments identify the direction under both losses. [Continuous certificate](../results/recovery_continuous.csv) · [Discrete direction cases](../results/recovery_gaps.csv)

Adjacent contiguous-block mean equalities include all potential changes in the fitted isotonic blocks. Between consecutive equality values, the area score is affine in the recovered knot. The pairwise gap width adds the two call widths and independent recovered values allow separate maximization. The feasible three-value recovery configurations are a subset of the continuous domain, so their minimum shrinkage bounds the continuous minimum from above. [Frozen protocol](../docs/model-spec.md#continuous-historical-recovery-freeze) · [Numerical verification](continuous-recovery-verification.md)

I built the source from a Git archive with two passes of `pdflatex -interaction=nonstopmode -halt-on-error main.tex` and `SOURCE_DATE_EPOCH=1795731780`. I rendered pages 12–13 and checked all 74 page headers and blank author metadata. [Reviewed PDF](../paper/main.pdf)

## Targeted edits

1. Link the continuous certificate and breakpoint tables in the historical recovery portion of the central registry. [Claim registry](../claims/claim-registry.md)
2. Shorten the paragraph ending on page 12 to avoid a lone continuation line on page 13. The detailed report records the discrete identification result. [Manuscript source](../paper/results.tex) · [Results report](../docs/recovery-priority.md)

## Targeted re-review

I reproduced the PDF from the exact revised commit `ae23f49416ce775dc62fc0a2f0e443bf789cc152` using the same archived-source two-pass build. The rebuilt PDF matches SHA-256 `b3ffff73973885fe346b56add74d74968fb8bd0757ed764fc6acdc99fb42910d`. The central registry links both continuous tables. The revised paragraph fits entirely on page 12 and retains the continuous certificate and coupled-loss findings. Figure 4, its caption and all references remain together on page 13. The appendices begin on page 14 of 74. I confirmed all 74 team fields and the author field are blank. Traceability and clarity each score 15/15. **Final score 100/100, pass.** [Claim registry](../claims/claim-registry.md) · [Final PDF](../paper/main.pdf)
