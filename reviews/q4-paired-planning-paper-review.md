# Independent manuscript review of Q4 paired planning

I reviewed `025f318f7ad298f70313e8ad2abc0b379f2c4e1d` against the frozen manuscript rubric and paired allocation protocol. The prior paper review covers the unchanged Q1–Q4 sections. I checked the new paragraph, the protection and monitoring guidance around it, the claim map and the extended source appendix. [Rubric](../docs/model-spec.md#frozen-independent-paper-rubric) · [Protocol](../docs/model-spec.md#paired-dependence-allocation-sensitivity-freeze) · [Previous review](q4-fisher-paper-review.md)

| Dimension | Initial score | Basis |
|---|---:|---|
| Numerical and factual accuracy | 22.5 / 30 | All four maximum ratios round correctly. The midpoint claim needs to identify the maximum across margins as the improving quantity. |
| Traceability | 15 / 15 | The claim registry identifies all three planning exports. All 37 tracked Python modules have full-file listings, exactly once each. |
| Coverage and reasoning | 30 / 30 | The planning comparison preserves fitted mask marginals and evaluates four scenarios on three margins. The constrained Fisher conclusion is limited to the four evaluated allocations. The guidance retains the measurement and randomized validation requirements for field use. |
| Clarity and structure | 15 / 15 | The new paragraph and references remain on page 14. Listing 37 begins on page 103 and finishes on page 105. The inspected pages are legible. |
| Build and references | 10 / 10 | The deterministic build matches the delivered PDF. All 105 team fields and the PDF author are blank. The body and references occupy 12 pages. |

**Initial score 92.5/100.** On page 14 the sentence about midpoint greedy should specify that it lowers the maximum relative variance compared with the constrained Fisher plan. At the midpoint and upper log odds ratios, the maximum falls from 0.427727 to 0.423741 and from 0.428582 to 0.422293, respectively. Both two-voice margin ratios rise in each of those scenarios. The modulated margin ratio falls. The ratios use the current-data variance for the corresponding scenario and margin. [Scenario and margin scores](../results/q4_paired_planning_precision.csv) · [Manuscript](../paper/main.tex)

## Archived build

I extracted a fresh Git archive and ran `pdflatex -interaction=nonstopmode -halt-on-error main.tex` twice from `paper/` with `SOURCE_DATE_EPOCH=1795731780`. The rebuilt PDF matches SHA-256 `898399e61a8fe978a51dadee0762567fbbe5902cccc310f977fcba3abe1af378`. I rendered pages 14–15 and 103–105 to inspect the changed planning paragraph, the appendix boundary and the full new listing. The body and references occupy pages 3–14, and the appendices begin on page 15. [PDF](../paper/main.pdf) · [Claim registry](../claims/claim-registry.md)

## Targeted re-review

Revision `7b0bc1543489fc77183dd9b8c55e3e28d65705ba` specifies that midpoint greedy lowers the largest ratio at the two positive log odds scenarios relative to constrained Fisher. This agrees with the paired planning precision table. I rebuilt a separate Git archive using the same two-pass command and confirmed a byte-for-byte match with the delivered PDF at SHA-256 `f6a3f138598510c75ac8a84a7460d06a8632bfb1d423cfac0105b9cdd11b884c`. The rendered revision on page 14 fits above the limitations and references. The extracted text differs only on page 14. The body and references occupy 12 pages, and all 105 team fields and the PDF author are blank. Numerical and factual accuracy earns 30/30 after correction. **Final score 100/100, pass.** [Final PDF](../paper/main.pdf) · [Precision table](../results/q4_paired_planning_precision.csv)
