# Independent review of contest source appendix

**Pass.** I reviewed commit `8c979da315614889380ba32774ca82d0efd4c3ef` against the supplied *2026 APMCM Essay format and submission specifications*. The document requires the software names and source code in the appendix and sets a 25-page limit on the main body.

## Source and software coverage

I compared the Python paths in the reviewed Git tree with the full-file LaTeX listing inputs. All 33 tracked Python modules appear exactly once. Listings 24–33 add `group_size.py`, `vocal_counts.py`, `first_reply.py`, `behavior_gap.py`, `spatial_annulus.py`, `context_priority.py`, `recovery.py`, `continuous_recovery.py`, `control_subtraction.py` and `behavior_ablation.py`. The software section includes Python, the seven packages in the requirements file, the MiKTeX build tool and Poppler. All seven package versions match both the requirements and installed distribution metadata. [LaTeX source](../paper/main.tex) · [Requirements](../requirements.txt)

## Approved content and pagination

The diff from `a8268bd` contains only `paper/main.tex` and `paper/main.pdf`. The LaTeX source preceding the appendices matches the approved version. Extracted text on pages 1 and 3–14 matches after excluding the running page totals. Page 2 includes the new appendix subsections. The body and references occupy pages 3–14 (12 pages). The appendices occupy pages 15–97 (83 pages), with Analysis source and Software on page 16. I rendered page 16 and pages 75–97 and checked the software section, the ten new listings and the page transitions. All 97 sequential team headers and the PDF author field are blank. [Reviewed PDF](../paper/main.pdf)

## Deterministic rebuild

I unpacked a fresh Git archive of the reviewed commit, set `SOURCE_DATE_EPOCH=1795731780`, and ran `pdflatex -interaction=nonstopmode -halt-on-error main.tex` twice from its `paper/` directory. The rebuilt PDF matches the published binary byte-for-byte with SHA-256 `fd6e50a634c2159bcdf6b349a97f1d9aa989f09a547524066534273629b403c1`. [Reviewed PDF](../paper/main.pdf)
