# Independent manuscript review of Q3 discordant response direction

I reviewed `1edc7923e76c150defd5353cc2368f4856499d39` against the frozen paper rubric. This review covers the new Q3 direction comparison, its relation to the existing conditional and absolute predictions, and the additional source listing. [Rubric](../docs/model-spec.md#frozen-independent-paper-rubric) · [Frozen direction protocol](../docs/model-spec.md#q3-discordant-pair-direction-freeze) · [Previous review](q4-envelope-attainment-paper-review.md)

| Dimension | Initial score | Basis |
|---|---:|---|
| Numerical and factual accuracy | 30 / 30 | All counts, reported scores, paired date intervals and fallback statements match the independent results. |
| Traceability | 15 / 15 | The evidence map links all five direction tables. The appendix includes all 46 tracked Python files once each. All seven exported figures have CSV and metadata companions. |
| Coverage and reasoning | 22.5 / 30 | The conditional intercept distinction and standardized predictions are correctly described. State explicitly that the purged direction scores use all 76 equal-size discordant pairs and that Firth trains on eligible discordant pairs, including those at unequal distances. |
| Clarity and structure | 11.25 / 15 | The two new paragraphs fit on page 8, but the next paragraph leaves a single opening line at the foot of that page. |
| Build and references | 10 / 10 | The independent archive rebuild reproduces the PDF. Body and references occupy 15 pages and the team and author fields are blank. |

**Initial score 88.75/100.** The 49 equal-distance pairs are the descriptive subset of the 137 equal-size pairs. The predictive comparison scores the 76 discordant pairs from the full equal-size sample. The standardized predictions additionally match playback distance and set eight birds. Name the score sample alongside the paired Firth fit so the reader can distinguish all three. Keep the opening line of the vocal-count paragraph with the rest of that paragraph. The counts 74 natural-only and two control-only, direction intercept and determinant penalty, larger scores after adding call, and one half-count fallback per Firth model match the frozen specification and tables. [Manuscript](../paper/results.tex) · [Counts](../results/q3_direction_counts.csv) · [Scores](../results/q3_direction_scores.csv) · [Contrasts](../results/q3_direction_contrasts.csv) · [Numerical review](q3-direction-verification.md)

## Independent archive rebuild

Two passes of `pdflatex -interaction=nonstopmode -halt-on-error main.tex` from the archived `paper/` directory with `SOURCE_DATE_EPOCH=1795731780` reproduce SHA-256 `d05b62431a080872b0d8c5504b8a560821f5dbef1017ac656da344542ba9468a`. I rendered the new Q3 paragraphs, the page turn to the vocal-count paragraph, Figure 3 and the additional source listing. All 133 page headers have empty team fields and the PDF author is blank. Body and references occupy pages 3–17, and the appendices begin on page 18. Listing 46 spans pages 130–133. [PDF](../paper/main.pdf) · [Claim registry](../claims/claim-registry.md)

## Targeted re-review

Revision `8affc5a87fe239c2d960b801a4b2acd9f3fda5aa` explicitly includes unequal playback distances in the eligible equal-size discordant training and scoring samples. The scope is distinct from the equal-distance raw counts and the matched-distance standardized predictions. The two new Q3 paragraphs fit on rendered page 8, and the full vocal-count paragraph opens page 9. [Revised manuscript](../paper/results.tex)

The independent two-pass build reproduces final SHA-256 `ad426f83bbb3aae643eeadccdb3c2a87eb33aa81c2a8fe01d23871cf0ce4347d`. All 133 team fields and the PDF author field are blank. Body and references occupy 15 pages, with 46 source listings in the appendices starting at page 18. Coverage and reasoning earns 30/30, and clarity and structure earns 15/15. **Final score 100/100, pass.** [Final PDF](../paper/main.pdf)
