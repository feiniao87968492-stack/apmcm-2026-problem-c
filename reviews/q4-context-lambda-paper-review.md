# Independent review of the Q4 behavioral-loss manuscript update

I reviewed manuscript source 252c1042c8c1f09ab78915547dd2c4a45cc7b4e3 against specification 3192ea6 and evidence 5a67dcc. At 100 m, 50% overall exposure and 30–70% exposure within each context, the acoustic-only minima are 93.02% for the full fit and 86.53% after union deletion. With the acoustic retention factor also applied to positive response excess, the union-deleted maximum drops to 76.78%. This switch meets the frozen manuscript trigger. The surrounding paragraph retains the full-fit Monte Carlo qualification and identifies the hypothetical exposure and uncalibrated response loss. [Frozen design](../docs/model-spec.md#q4-bounded-context-behavioral-noise-sensitivity-freeze) · [Checkpoint evidence](../results/q4_context_lambda_checks.csv)

| Frozen rubric dimension | Score | Verification |
|---|---:|---|
| Numerical and factual accuracy | 30/30 | The fixed-draw all-pass and all-fail decisions match the inclusive 80% rule and the checkpoint table. |
| Traceability | 15/15 | The page 17 PDF hyperlink targets the context evidence at commit 5a67dcc. The linked file contains the checkpoint and crossing tables. |
| Coverage and reasoning | 30/30 | The added sentence attributes the decision switch to behavioral retention at the same acoustic loss. The paragraph retains the simulation precision and field-calibration limits. |
| Clarity and structure | 15/15 | I rendered page 17 and confirmed that the amended paragraph is legible within the page margins. |
| Build and references | 10/10 | The archive built in two passes. Pages 3–20 cover the body and references. Appendices start on page 21 of 177. Team number and PDF author metadata are blank. |

**Pass, 100/100.** I ran two pdflatex passes with halt-on-error in a fresh Git archive using SOURCE_DATE_EPOCH=1795731780. The independent PDF SHA-256 is 3dd232a0a98f01b42b748dce57c4e8d0a7f6c2ef3db7ad21bc4ceac404ef1722. [Frozen rubric](../docs/model-spec.md#frozen-independent-paper-rubric) · [Anonymous PDF](../paper/main.pdf)
