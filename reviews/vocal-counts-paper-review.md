# Independent manuscript review of vocal counts and contact scenarios

Reviewed manuscript `567e3a52a75349184f536bd5b4ba6cd81d0f33d2` and PDF SHA-256 `15687593de225e879aacefa7dbfe88cbdde0f98227cdaeb69e96045871cd23a3` using the frozen rubric. [Rubric](../docs/model-spec.md#frozen-independent-paper-rubric)

| Dimension | Score | Finding |
|---|---:|---|
| Numerical and factual accuracy | 30 / 30 | The paired contrasts, intervals, count and flag comparison, held-out scores, and joint threshold results agree with the evidence. |
| Traceability | 15 / 15 | The field study supports the observation windows. The claim registry links all three comparisons to six new tables. Existing figures have CSV and metadata companions. |
| Coverage and reasoning | 30 / 30 | Q1–Q4 retain coverage. The count comparison uses the strict holdout and the prespecified two-metric adoption rule. The contact results stay within the modeled scenarios and shared support. |
| Clarity and structure | 11.25 / 15 | Figure and caption placement works. The count contrast says “differ by” and leaves the direction implicit. |
| Build and references | 10 / 10 | The detached two-pass build matches the distributed PDF byte-for-byte. The 73 team fields and author metadata are blank. Body and references occupy pages 3–12, and appendices begin on page 13. |

**96.25/100.** The numerical review supports acceptance. The signed contrast merits a targeted wording fix.

## Cross-checks

- The original study methods give two 60-second windows, one before playback and one from onset. The signed natural-minus-control contrast in changes is 1.978 calls per minute across 139 pairs and 1.673 across the 49 same-distance and same-size pairs. The 95% date-block intervals are [1.682, 2.351] and [1.308, 2.168]. A strict post-onset increase and the scored vocal response coincide in all rows. Positive post-onset counts yield two additional positives per arm. [Field study](https://doi.org/10.12688/openreseurope.24618.1) · [Paired counts](../results/vocal_count_pairs.csv) · [Audit](../results/vocal_count_audit.csv)
- The stimulus means, full Poisson and baseline-augmented Poisson score 2.520, 2.370 and 2.194 in mean deviance and 1.269, 1.145 and 1.181 calls in MAE. The full Poisson improves MAE over stimulus means with its date interval below zero. Its deviance interval includes zero, so the joint rule retains stimulus means. [Scores](../results/vocal_count_scores.csv) · [Independent numerical review](vocal-counts-verification.md)
- The eight-bird comparisons apply the fidelity and excess thresholds of 0.50 and 0.20 to paired acoustic and date draws. The 80% decisions match for all 18 settings, with six passing clean and four under 20% coupling. For modulated calls at 50 m under coupling, attainment changes from 100% to 95%. The manuscript retains 150 m as the support boundary and keeps the protection guidance as field evaluation. [Q4 results](../results/vocal_contact_q4.csv) · [Local coverage](../results/vocal_contact_coverage.csv)
- The clean build used two passes of `pdflatex -interaction=nonstopmode -halt-on-error main.tex` with `SOURCE_DATE_EPOCH=1795731780`. I rendered body pages 7–12, including the two new results paragraphs. Figure 4 and its caption fit together on page 12 above the conservation conclusion and references. [Reviewed PDF](../paper/main.pdf)

## Targeted wording fix

Name the signed natural-minus-control change explicitly and state that the same bird can contribute multiple calls. [Q3 results source](../paper/results.tex)

## Targeted re-review and acceptance

I reviewed revised manuscript commit `e898182d926e28f8d6c28dd232ec1dac227420ee` and PDF SHA-256 `db70b1404c9266ba9b05c1ab53f280f03e6c8405dd8b02c7bd371e733080d37b`. Page 7 states that the mean post-minus-pre change is 1.98 calls per minute higher for natural playback than for control and explains that one bird can contribute multiple calls. The edited paragraph fits on page 7. The clean two-pass build again reproduced the committed PDF byte-for-byte. All 73 team fields and the author field remain blank. Body and references occupy pages 3–12 and the appendices begin on page 13. [Revised PDF](../paper/main.pdf)

| Frozen dimension | Revised score |
|---|---:|
| Numerical and factual accuracy | 30 / 30 |
| Traceability | 15 / 15 |
| Coverage and reasoning | 30 / 30 |
| Clarity and structure | 15 / 15 |
| Build and references | 10 / 10 |

**Pass, 100/100.** The targeted wording change is verified.
