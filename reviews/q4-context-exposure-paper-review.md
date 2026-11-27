# Independent manuscript review of Q4 context-dependent opportunity exposure

**Pass, 100/100.** I reviewed manuscript source `9681ef2dc877cd26349cd675fb80b49287188f4d` under the frozen rubric. The review covers the new context-specific result, its evidence link and the source listing. [Frozen paper rubric](../docs/model-spec.md#frozen-independent-paper-rubric)

With half of all playback opportunities in the noisy state, the modeled pass fraction ranges from 77.74% to 86.41% in the full fit and from 66.33% to 81.26% after union deletion. Both ranges straddle the 80% criterion. The largest share meeting that criterion across all allocations is 44.16% in the full fit and 22.05% after deletion. The respective uniform-exposure limits are 56.78% and 35.11%. The manuscript gives the original weights of 36/139, 65/139 and 38/139 in after-feeding, commuting and searching order. [Frozen specification](../docs/model-spec.md#q4-context-dependent-intermittent-exposure-freeze) | [Checkpoints and allocations](../results/q4_context_exposure_checks.csv) | [Boundary limits](../results/q4_context_exposure_limits.csv)

The preceding paragraph defines the 100 m prefix and hypothetical noisy-opportunity share. The addition explains that context-specific thresholding precedes aggregation using the same context-standardized clean reference. The recommendation to measure exposure by behavioral context stays within the scenario evidence. Both searching arms have observed ranges beginning at 40 m, and the text flags extrapolation below that distance. Context-linked receiver exposure and behavioral noise response require calibration. [Support by context and arm](../results/q4_context_exposure_support.csv) | [Independent numerical verification](q4-context-exposure-verification.md)

| Frozen rubric dimension | Score | Verification |
|---|---:|---|
| Numerical and factual accuracy | 30/30 | The empirical weights, rounded shares, 80% decision changes and searching support agree with the exports. |
| Traceability | 15/15 | The page 17 PDF annotation points to the tracked results note pinned at commit 287e65d. Each of the seven figures has its CSV and metadata companions. |
| Coverage and reasoning | 30/30 | The new paragraph identifies the aggregation order, interprets the limits under the fixed model and identifies the measurement gap. |
| Clarity and structure | 15/15 | The paragraph fits together near the top of page 17. Listing 61 starts legibly on page 162. |
| Build and references | 10/10 | A fresh Git archive compiled in two passes. The body and references occupy pages 3 through 20 of 176. The appendices begin on page 21. All 69 Python modules appear once, and every team header and the PDF author field are anonymous. |

I ran `pdflatex -interaction=nonstopmode -halt-on-error main.tex` twice from the `paper/` directory of a fresh Git archive with `SOURCE_DATE_EPOCH=1795731780`. The rebuilt PDF SHA-256 is `4c10c1de385459aa77b65b322e50c85bcc7cd000c7dbac2a8254832f581e9bc9`. [Anonymous PDF](../paper/main.pdf)
