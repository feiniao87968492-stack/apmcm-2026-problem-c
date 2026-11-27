# Independent review of the Q4 context Monte Carlo manuscript update

I reviewed manuscript source `1e8ab6a5657bbc1adebe793a4e779a135f571d1f` against the frozen specification and evidence at `15c508b1aebdb6501bbdd6abb59a1919477fa149`. At 50% overall noisy-opportunity exposure with each context constrained to 30–70%, the 4,800-draw full-fit minimum is 80.343945%. Its projected 95% simultaneous Monte Carlo interval is 79.707497%–80.980393%, leaving the all-pass decision unresolved under the inclusive 80% rule. The union-deleted maximum interval is 76.124544%–77.433699%, preserving the all-fail decision. The revised paragraph identifies the 4,800-draw point comparison and conditions the simulation precision on the data and model. [Frozen design](../docs/model-spec.md#q4-bounded-context-monte-carlo-precision-freeze) · [Projected bounds](../results/q4_context_mc_bounds.csv) · [Frozen rubric](../docs/model-spec.md#frozen-independent-paper-rubric)

| Frozen rubric dimension | Score | Verification |
|---|---:|---|
| Numerical and factual accuracy | 30/30 | The projected intervals, rounding and threshold decisions match the frozen rule and evidence table. |
| Traceability | 15/15 | The compiled link on page 17 resolves to the pinned evidence commit. All seven figure sets include PNG, CSV and metadata. |
| Coverage and reasoning | 30/30 | The amendment reports the relevant extremum for each fit, explains the decision consequence and retains the hypothetical exposure scope. |
| Clarity and structure | 15/15 | The revised sentence before the interval explicitly limits the point comparison to the 4,800 draws. The entire paragraph is legible on rendered page 17. |
| Build and references | 10/10 | The archive built in two passes. Pages 3–20 cover the body and references, with appendices starting on page 21 of 177. Team number and author metadata are blank. |

**Pass, 100/100.** I ran `pdflatex -interaction=nonstopmode -halt-on-error main.tex` twice from `paper/` in a fresh Git archive with `SOURCE_DATE_EPOCH=1795731780`. The independently rebuilt PDF SHA-256 is `4eaa49fc414a57397ec99a3d4577d919dd4f3d42acd380a47a3ecae0cc33b3f8`. [Anonymous PDF](../paper/main.pdf)
