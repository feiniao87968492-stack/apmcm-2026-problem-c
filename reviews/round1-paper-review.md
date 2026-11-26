# Round 1 independent manuscript review

## Frozen submission

Reviewed source commit `fdd3a2b`, experiment commit `5e7c49d` and rubric commit `3a7b195`. The reviewed PDF SHA-256 is `a79ad63f5c6e879ac4ef2184647afb09e10791d5e0c56a1553e342aa1c42187d`. Review used a detached checkout. The reviewer did not implement or draft the manuscript. The official Problem C and 2026 essay format PDFs were read from the contest directory.

## Score

| Frozen dimension | Score | Evidence and basis |
|---|---:|---|
| Numerical and factual accuracy | 30 / 30 | Grouped classifier results, propagation estimates, playback performance and latency, integrated bounds and loss comparisons agree with source results. |
| Traceability | 11.25 / 15 | References and companions are present. Figures 4 and 6 are transposed in the index and the last row is outside the table. |
| Coverage and reasoning | 22.5 / 30 | Four questions and adoption decisions are addressed. Representative distance checks and timing model details need completion, as below. |
| Clarity and structure | 11.25 / 15 | Summary and result organization are effective. Onset table introduction is separated from its tables by a page break. |
| Build and references | 10 / 10 | Clean two-pass build, English text, correct front matter, anonymous page headers and compliant body length. |
| **Total** | **85 / 100** | **Targeted revision and re-review.** No hard failure. Close the coverage and traceability items before delivery. |

## Evidence and actionable findings

1. **Keep Q1 conclusions and model decision.** Macro F1 0.314/0.370, paired improvement 0.055 with interval −0.010 to 0.100, recalls and instability for two-voice agree with `results/q1_model_comparison.csv`. The historical comparison uses different folds as stated in `paper/results.tex:3`. The paper preserves the measurement availability limits and the feature-test evidence.
2. **Repair the figure index.** Figure 4 in `paper/results.tex:79` is `q4_loss_comparison` and Figure 6 in `paper/main.tex:103` is `q4_scenarios`. Reverse the corresponding labels in `figures/figure-index.md` and remove the blank line before its final row so all six PNG, CSV and metadata bundles are reached through the same Markdown table.
3. **Complete the Q3 effect and latency reporting.** At `paper/main.tex:59` quantify the distance mismatch as 90/139 and keep the descriptive interpretation of the raw paired comparison. Restore its 51.8 percentage-point difference and paired 95% interval 43.9–60.1 in `paper/results.tex:40`, sourced to `results/q3_paired_response.csv`. In the onset method at `paper/main.tex:65` describe the Gaussian residual model on the transformed scale and the way the median averages contexts via empirical frequency times event probability, matching `q3.py:206` onward. Numeric cross-checks reproduced all three grouped performance mean pairs and all 54 behavior-by-stimulus-by-type-by-distance cells from `results/q3_grouped_validation.csv` and `results/q3_representative_latency.csv`. The no-control-approach and local support limitations are represented correctly.
4. **Complete Q4 common threshold and protection comparisons.** Specify the common 20–150 m domain and dimensionless common cutoff 0.2876 in `paper/main.tex:74` or `paper/results.tex`. Include 20 and 150 m indices alongside 50/100 m to complete the four fixed-distance comparisons. At 20 m the indices by call are 0.550, 0.608 and 0.567 and at 150 m they are 0.165, 0.266 and 0.367. At 50 m modulated and two-voice round to the same displayed value, 0.507. At 20% loss and 50 m, flat meets both cutoffs with acoustic loss alone and falls below both with coupling, while modulated and two-voice meet both cutoffs in both scenarios. This completes the short-distance counterpart to the correctly reported 100 and 150 m cases. The clean 40% and 60% reference sensitivity mentioned in the methods can be summarized in one sentence. At 40% modulated and two-voice both reach the 150 m support bound. At 60% the radii are 69.1, 101.8 and at least 150 m. These numbers trace to `results/q4_comparison_curves.csv`, `results/q4_comparison_radii.csv` and `results/q4_radii.csv`. The paper appropriately reserves site-specific vessel limits for future measurements.
5. **Keep the onset introduction with its first table.** In the compiled review copy, Appendix A starts on page 8 and its first table starts on page 9. A page break before Appendix A or keeping its short introduction with the first table would preserve reading order. The body fits on pages 3–8 including references. Summary and contents are on pages 1 and 2. The 28-page total includes the unrestricted appendices with the code listings.

The reviewed LaTeX rebuilt with two `pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error` passes in the detached checkout, with the local team include absent. `pdftotext -layout` produced identical bytes for the reviewed PDF and clean build (SHA-256 `2b52bb4f57c119fac6c98a9f1e781ae051401eb92bc2ac60b26bb0b6054f5b5a`). All 28 pages rasterized at 54 DPI and the corresponding PNG page files matched byte-for-byte. The non-fatal epstopdf shell-escape warning under the explicit no-shell mode has no effect on the PNG figures.

## Targeted re-review

The revised manuscript is fixed at commit `22529a9`. The detached copy's PDF SHA-256 is `a1ec58529561ae98f6b4ab7f9e091d650e1e88da06c4549ee7ecd659b245483b`. Its model and result files agree with the first reviewed version.

- Figure 4 now identifies `q4_loss_comparison` and Figure 6 identifies `q4_scenarios`. The six-row figure index renders as one Markdown table. Every indexed bundle has a PNG, CSV and parseable metadata JSON.
- The Q3 methods report the 90/139 unequal-distance pairs and the Gaussian log-onset mixture with response-weighted empirical contexts. The results restore 51.8 percentage points and the paired 95% interval of 43.9–60.1 points. The additions match the data audit, paired result and implementation.
- The Q4 methods specify the 20–150 m grid and the 0.2876 common threshold. The four same-distance comparison triplets, the 50 m cutoff judgments, and the 40% and 60% clean reference checks agree with the exported comparisons. The monitoring advice preserves the conditional interpretation.
- The rendered PDF has the three onset tables together with their introduction on page 9. Summary and contents remain on pages 1 and 2, the body and references occupy pages 3–8, and team fields are blank across all 28 pages.

| Frozen dimension | Revised score |
|---|---:|
| Numerical and factual accuracy | 30 / 30 |
| Traceability | 15 / 15 |
| Coverage and reasoning | 30 / 30 |
| Clarity and structure | 15 / 15 |
| Build and references | 10 / 10 |
| **Total** | **100 / 100** |

**Pass.** The targeted findings are closed under the frozen rubric.
