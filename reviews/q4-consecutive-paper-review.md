# Independent manuscript review of Q4 consecutive-distance attainment

I reviewed `fd5e1ed85311a508427ed6fcd994e85d579f2fee` against the frozen rubric. The review covers the five grid rules, exact Monte Carlo interval and retained arm ranges. Prior reviews cover the earlier analyses. [Rubric](../docs/model-spec.md#frozen-independent-paper-rubric) · [Frozen specification](../docs/model-spec.md#q4-consecutive-distance-attainment-freeze) · [Numerical review](q4-consecutive-verification.md)

| Dimension | Initial score | Basis |
|---|---:|---|
| Numerical and factual accuracy | 30 / 30 | The radii, 3,858 and 3,850 clean counts, two 3,847 loss counts, and pairwise arm ranges match the exports. An independent exact calculation gives 79.05255%–81.32726% for 3,850 of 4,800. |
| Traceability | 15 / 15 | The claim registry links the four exports through the analysis note. The 50 tracked Python files each have one full listing. All seven figures have CSV and metadata companions. |
| Coverage and reasoning | 30 / 30 | The manuscript distinguishes marginal grids from simultaneous passage by the same draws, and identifies the clean 150 m cap after union deletion as extrapolation for both arms. The exact interval describes Monte Carlo precision. |
| Clarity and structure | 11.25 / 15 | The new paragraph fits on page 15. A manual page break leaves page 16 with the drift paragraph alone. |
| Build and references | 10 / 10 | The independent archive rebuild matches the PDF. All 142 team fields and the author field are blank. Body and references occupy 16 pages. |

**Initial score 96.25/100.** The observed count is ten above the rule's 3,840 cutoff. Its exact 95% interval contains 80%. The natural and control fits extrapolate beyond 100 and 120 m, respectively, after union deletion. Remove the manual break before the hurdle-model paragraph and inspect the resulting Q4 page turns. [Manuscript](../paper/results.tex) · [Radii](../results/q4_consecutive_radii.csv) · [Node counts](../results/q4_consecutive_counts.csv) · [Retained distances](../results/q4_consecutive_ranges.csv)

## Independent archive rebuild

Two passes of `pdflatex -interaction=nonstopmode -halt-on-error main.tex` from the archived `paper/` directory with `SOURCE_DATE_EPOCH=1795731780` reproduce SHA-256 `3469bc55f4e870b46028b0e4be63be1ff85f8c78b11aeeef8dd5bb26cf2307b1`. Body and references occupy pages 3–18, with appendices beginning on page 19. I inspected the new paragraph, its surrounding page breaks, Figure 4 and Listing 50 on pages 140–142. [PDF](../paper/main.pdf) · [Claim registry](../claims/claim-registry.md)

## Targeted re-review

Revision `b368940785432fe2eb389b11cc87a59bf727508a` removed the break before the hurdle-model comparison. The remaining break before Fisher planning left page 17 with eight lines. Revision `ecf2567b516ed5e212a7a24c582835c5e1dae8e7` removed that break. Rendered pages 16 and 17 show readable text and Figure 4, with the monitoring paragraph continuing from three lines at the foot of page 16. The results paragraph remains intact on page 15. [Revised manuscript](../paper/results.tex)

The independent two-pass archive build matches the final PDF at SHA-256 `ce8822fba6fa0377376303f7bb2d3bdaa09cdc088bb0ade6a6890924c4da4c55`. Body and references occupy pages 3–17, and the appendices begin on page 18. All 141 team fields and the PDF author field are blank. Clarity and structure earns 15/15. **Final score 100/100, pass.** [Final PDF](../paper/main.pdf)
