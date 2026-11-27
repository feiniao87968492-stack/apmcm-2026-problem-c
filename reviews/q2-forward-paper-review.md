# Independent manuscript review of Q2 forward-distance validation

**Pass, 100/100.** The final source is `217fe02bfd4e25641aa96bdefe7d976ddfb9f8d8` under the frozen paper rubric. The initial source `ebaf366` included the forward-validation listing. The final revision adds the score-guided manual-review listing, closing the gap between the archived Python sources and the appendix. [Frozen paper rubric](../docs/model-spec.md#frozen-independent-paper-rubric)

The paragraph on pages 6-7 reports pooled 128 and 256 m RMSE of 0.10859 for separate exponents and 0.11236 for a shared exponent. The difference of -0.00376 and paired 95% interval [-0.00883, 0.00355] match the six-cell forward comparison. The fixed exponent gives the lowest point RMSE at 128 m, and the separate fit gives the lowest at 256 m. All three two-voice representations have 190 of 300 available rows at 128 m. The paper distinguishes this shorter-distance design from interior interpolation and limits the interval to the available correlations and whole-row resampling with unknown acquisition groups. [Forward results](../docs/q2-forward.md) | [Fit scores](../results/q2_forward_scores.csv) | [Paired intervals](../results/q2_forward_contrasts.csv) | [Measured support](../results/q2_forward_support.csv)

| Frozen rubric dimension | Score | Evidence |
|---|---:|---|
| Numerical and factual accuracy | 30/30 | The model definitions, target scope, RMSEs, paired interval, target-specific ranking and row counts match the exports. |
| Traceability | 15/15 | The compiled page 7 evidence link points to the results note pinned at `3575c47e7f75e638bdfaeec0530e739625e11ea9`. All seven repository figures have CSV and metadata companions. |
| Coverage and reasoning | 30/30 | The text describes strictly shorter training distances and the isotonic baseline. The paired interval includes zero, supporting the qualification on carrying the interior preference into forward prediction. |
| Clarity and structure | 15/15 | The paragraph and its one-line continuation above Figure 2 are legible on pages 6-7. The forward validation and score-guided review code listings are legible. |
| Build and references | 10/10 | The archived source compiled in two passes. The body and references occupy pages 3-20 of 170, and the appendices start on page 21. All 66 tracked Python modules appear once. The team and author fields are blank. |

I ran two passes of `pdflatex -interaction=nonstopmode -halt-on-error main.tex` with `SOURCE_DATE_EPOCH=1795731780` from the `paper/` directory of a fresh Git archive. The final PDF SHA-256 is `3a56fddff2307a56f78f5f9282df8ca2c6a279cd7ad095c9137f8d79e68dd812`. [Anonymous PDF](../paper/main.pdf)
