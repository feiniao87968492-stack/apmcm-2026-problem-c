# Independent manuscript review of Q2 spectral allocation

I reviewed `222569c573f0427c02c3ae2155b1b86bb35099a7` against the frozen paper rubric, with the earlier analyses covered by the previous reviews. I checked the five envelope paths, the continuous fixed-envelope slice and the resampling condition. [Rubric](../docs/model-spec.md#frozen-independent-paper-rubric) · [Frozen specification](../docs/model-spec.md#q2-spectral-allocation-sensitivity-freeze) · [Previous review](q2-envelope-rank-paper-review.md)

| Dimension | Initial score | Basis |
|---|---:|---|
| Numerical and factual accuracy | 30 / 30 | The reversal range 0.339651–0.347216, equal spectral split value 0.342706 and endpoint leads of 2.91 and 0.87 m all match the exports. |
| Traceability | 15 / 15 | The claim registry points to the three spectral allocation tables. The appendix lists all 44 tracked Python files once each. All seven exported figures have CSV and metadata companions. |
| Coverage and reasoning | 22.5 / 30 | The paragraph should name the two fidelity thresholds on the fixed-envelope slice and state the condition for applying the resampling analysis on that slice. |
| Clarity and structure | 15 / 15 | The new paragraph and Figure 2 fit on rendered page 6. Listing 44 is complete and legible across pages 124–126. |
| Build and references | 10 / 10 | The separate archive rebuild matches the delivered PDF. All 126 team fields and the PDF author field are blank. Body and references occupy pages 3–16. |

**Initial score 92.5/100.** Replace “at both thresholds” with “at fidelity 0.40 and 0.70.” State that the frozen protocol called for fixed-envelope resampling only if the point leader changed on the slice. This explains the scope of the current analysis alongside the prior 300-draw result for increasing the envelope weight. [Manuscript](../paper/results.tex) · [Events](../results/q2_spectral_allocation_events.csv) · [Radii](../results/q2_spectral_allocation_radii.csv) · [Fixed-envelope results](../results/q2_spectral_allocation_slice.csv)

## Separate archive rebuild

Two passes of `pdflatex -interaction=nonstopmode -halt-on-error main.tex` from the archived `paper/` directory with `SOURCE_DATE_EPOCH=1795731780` reproduce SHA-256 `fb9f6086156770b5fc9df355bc9a1c73a7ddb63e001e599ea41c9a9b2006ba72`. I rendered and inspected page 6, the transition to Q3 and the three pages with Listing 44. Body and references occupy 14 pages, and the appendices start on page 17. [PDF](../paper/main.pdf) · [Claim registry](../claims/claim-registry.md)

## Targeted re-review

Revision `0519946cbbe4c31fa353b84a6737855b1a059c14` names fidelity 0.40 and 0.70 explicitly and states that the fixed-envelope resampling applied only if the point leader changed. Two-voice leads throughout the fixed-envelope slice at both thresholds, so that condition does not trigger. The revised paragraph and Figure 2 fit together on rendered page 6. [Revised manuscript](../paper/results.tex) · [Fixed-envelope results](../results/q2_spectral_allocation_slice.csv)

The separate two-pass archive rebuild matches final PDF SHA-256 `180664b498d3567d96e9888e173791b1724211590c9a2341963e058802a6b49a`. All 126 team fields and the PDF author field are blank. Body and references occupy 14 pages, with 44 source listings in the appendix. Coverage and reasoning earns 30/30. **Final score 100/100, pass.** [Final PDF](../paper/main.pdf)
