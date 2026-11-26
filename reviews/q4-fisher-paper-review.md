# Independent manuscript review of Q4 Fisher planning

I reviewed `2a7e971dd55e630d086c7361e0be5ffcd0282e49` against the frozen manuscript rubric and the frozen Fisher planning protocol. [Rubric](../docs/model-spec.md#frozen-independent-paper-rubric) · [Planning protocol](../docs/model-spec.md#fisher-planning-for-three-q4-margins)

| Dimension | Initial score | Basis |
|---|---:|---|
| Numerical and factual accuracy | 22.5 / 30 | The variance ratios and the direction of each standard-error change agree with the exports. The first constrained-greedy gain needs a rounding correction. |
| Traceability | 15 / 15 | The claim registry identifies the allocation and precision tables. All 36 tracked Python modules appear exactly once in full-file listings. |
| Coverage and reasoning | 30 / 30 | The paper retains Q1–Q4 and specifies the planning model, common distances, conditional independence, fitted cutoff gradients, fixed acoustics and hypothetical coupling. |
| Clarity and structure | 15 / 15 | The planning paragraph, limitations and references fit on page 14. The source listing is legible throughout. |
| Build and references | 10 / 10 | The deterministic rebuild matches the PDF. All 103 team fields and the author field are blank. Body and references occupy 12 pages. |

**Initial score 92.5/100, pass.** Round the first constrained-greedy standard-error reduction directly from 8.1481879% to 8.1%, or display 8.15% at two decimal places. The initial manuscript displays 8.2%. [Precision table](../results/q4_fisher_precision.csv) · [Manuscript](../paper/main.tex)

## Evidence and archived build

All four new allocations sum to 120 pairs. The constrained greedy plan assigns 10, 10 and 18 pairs to the three focal cells. Uniform, focal-only, unconstrained and constrained allocations have largest relative variances of 0.500059, 0.563346, 0.415599 and 0.419388. The constrained plan's reductions against uniform are 8.1482% and 8.4207% for the clean 150 m and coupled 100 m two-voice margins. Its clean 100 m modulated standard error increases by 0.4617%. [Allocations](../results/q4_fisher_allocations.csv) · [Precision](../results/q4_fisher_precision.csv) · [Claim registry](../claims/claim-registry.md)

I extracted a fresh Git archive and ran `pdflatex -interaction=nonstopmode -halt-on-error main.tex` twice from `paper/` with `SOURCE_DATE_EPOCH=1795731780`. The rebuilt PDF matches SHA-256 `67a412c102f0a6477b69770d802d341b35e2e3ff1eccb68cde73cda7bf3fe2e8`. I rendered page 14 and pages 101–103 to inspect the new planning paragraph and Listing 36. The body and references occupy pages 3–14. The appendices begin on page 15. [Reviewed PDF](../paper/main.pdf)

## Targeted re-review

I independently rebuilt `dddc5415dea856cb9bd1d126904d78c91b32816a` from a separate Git archive using the same two-pass command. The rebuilt PDF matches SHA-256 `fc872aad7a9b3cf241ffb5315cd43e0e9f631f5ddda020f26e6f3de4b2efe055`. Rendered page 14 shows the corrected 8.15% and 8.42% without disrupting the layout. The extracted text matches on every other page, including all 36 full-file listings. The body and references occupy pages 3–14, the appendices start on page 15, and all 103 team fields and the PDF author field are blank. Numerical and factual accuracy earns 30/30 after correction. **Final score 100/100, pass.** [Final PDF](../paper/main.pdf)
