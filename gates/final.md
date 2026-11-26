# Final evidence and reproduction

The results reproduced byte-for-byte from a clean public checkout with the original C attachments. Independent reviews cover model design, implementation readiness, numeric results, figures, and paper claims.

The propagation intervals are conditional on row resampling. The Q3 matched-covariate predictions are group-level model estimates. The two-voice clean integrated radius reaches the upper end of the 20–150 m shared domain. Environmental probabilities and radii quantify the specified scenarios.

Use the [claim registry](../claims/claim-registry.md) for sources and the [figure index](../figures/figure-index.md) for plotted data.

## Round 1 evidence and reproduction

The frozen comparisons and paper rubric are at 3a7b195, with models and derived outputs at 5e7c49d. The final manuscript source and PDF reviewed after revision are at 22529a9. See the [comparison and decision table](../docs/round1-results.md), [independent numeric review](../reviews/round1-numeric-review.md) and [independent paper review with follow-up](../reviews/round1-paper-review.md).

A clean clone of 22529a9 ran the default 300-draw analysis with Python 3.10.11 in an isolated environment created from requirements.txt. Dependency checks passed. The reproduction command was:

```sh
python main.py --data "/path/to/C-attachments/date" --output regenerated
```

The regenerated directory contained the same 46 files as results/. The 40 CSV and JSON files matched byte-for-byte. All six PNGs matched by decoded pixels. With the original production environment the entire result directory also matched byte-for-byte.

Two passes of pdflatex from paper/ in the clean checkout reproduced the released PDF's extracted text and all 28 rendered pages. Page 1 is the summary, page 2 the contents, pages 3–8 the body and references, and appendices start on page 9. The public build left the team number blank. The released PDF SHA-256 is a1ec58529561ae98f6b4ab7f9e091d650e1e88da06c4549ee7ecd659b245483b.

The recording-group comparison, the incremental playback validation and the operational scenario checks support the stated adoption decisions. Acquisition identifiers, local playback events at the far end of the range and measured ambient-noise effects remain evidence limits.

## Final follow-up evidence and reproduction

The experimental specification was frozen at 634bd20. A clean clone of 13c5be8 reproduced all 62 result files using the original attachments and the isolated Python 3.10.11 environment installed from requirements.txt. All 56 CSV/JSON files matched byte-for-byte and all six PNGs matched by decoded pixels. The default 300-draw entry point is `python main.py --data <attachment-dir>`.

The [independent numerical review](../reviews/final-followup-numeric-review.md) verifies the recording-group deletion impacts, grouped behavior scores, paired intervals and all radius and cutoff comparisons. The [independent manuscript review](../reviews/final-followup-paper-review.md) verifies the manuscript claims, figures and format against the frozen rubric.

A two-pass clean-checkout pdflatex build of the revised manuscript reproduced the published PDF's extracted text and all 37 rendered pages. The summary and contents occupy pages 1–2, the body and references occupy pages 3–9, and the appendices begin on page 10. The public team fields are blank.

## Creative modeling evidence

The [frozen specification](../docs/model-spec.md#creative-modeling-freeze) is at b47de34 and the results at 5a00f56. A clean checkout reproduced 68 CSV/JSON files byte-for-byte and six PNGs by decoded pixels. The anonymous manuscript is 45 pages including appendices, with body and references on pages 3–10. See the [numeric review](../reviews/creative-numeric-review.md) and [paper review](../reviews/creative-paper-review.md).

## Post hoc verification

The post hoc checks froze at 43c39e6 and ran at 1ac4bbd. A clean checkout of the revised manuscript and source at c873d45 reproduced 74 CSV/JSON files byte-for-byte and six PNGs by decoded pixels. Two pdflatex passes reproduced the released extracted text and all 47 rendered pages. The team field is blank and the body and references occupy pages 3–10. [Results](../docs/posthoc-results.md) · [Independent numerical verification](../reviews/posthoc-numeric-review.md)

## Q4 decision verification

The decision analyses were frozen at d18ff9a and computed at c1e1ee8. Independent calculations reproduced the decision counts, crossed variance shares and exact integer optimum. A clean checkout of 2e8fe9b reproduced 77 CSV/JSON files byte-for-byte, six PNGs by decoded pixels, and the English PDF's text and all 50 rendered pages. The public team fields are blank. Body and references occupy pages 3–11. [Decision results](../docs/q4-decision-results.md) · [Independent recomputation](../reviews/q4-decision-verification.md)

## Playback dependence verification

The analysis was frozen at fa1b026 and computed at 4c1b3a3. Independent refits verified both holdout schemes, 36 margin rows and the trial precision results. A clean checkout of 1b20cd6 reproduced 82 CSV/JSON files byte-for-byte, six PNGs by decoded pixels and all 51 rendered PDF pages. The public team fields are blank. Body and references occupy pages 3–10, one page shorter than the previous release. [Results](../docs/playback-dependence.md) · [Independent recomputation](../reviews/playback-dependence-verification.md)
