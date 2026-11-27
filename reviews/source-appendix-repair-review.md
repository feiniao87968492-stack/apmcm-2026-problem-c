# Independent review of the anonymous source appendix repair

I reviewed source commit `b26bd5d` against release `7b0b621`. Comparing the Git tree with the LaTeX listing paths as multisets gave 72 tracked Python files and 72 unique listings, with each path occurring exactly once. Removing the three new listing lines restored the baseline `paper/main.tex` byte for byte. Poppler text extraction also matched across pages 1–20 after normalizing the total-page number in each header and the shifted appendix entry in the table of contents. [Appendix source](../paper/main.tex)

I built a clean Git archive of `b26bd5d` using two runs of `pdflatex -halt-on-error -interaction=nonstopmode main.tex` with `SOURCE_DATE_EPOCH=1795731780`. The result has 182 pages, with body and references on pages 3–20 and the appendices starting at page 21. The cover's team number and the PDF author metadata are blank. The extracted PDF has sequential captions for listings 1–72. [Anonymous PDF](../paper/main.pdf)

I rendered the cover, page 17 and pages 164–169 using Poppler's `pdftoppm` and inspected each image. The analysis text on page 17 and the code in all three listings are legible within the page margins.

| Source | Listing | PDF pages |
|---|---:|---|
| `q4_context_mc.py` | 62 | 164–166 |
| `q4_context_followup.py` | 63 | 166–168 |
| `q4_context_lambda.py` | 64 | 168–169 |

**Pass.** The independently rebuilt PDF SHA-256 is `93a74ff2c7133088d791d8ad17b0b39a3780e9a32064eeafad33d8f5626aad0e`.
