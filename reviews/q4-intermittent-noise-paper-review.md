# Independent manuscript review of Q4 intermittent noise

**Pass, 100/100.** I reviewed manuscript source `7e4dfb287bf641ce0906ba440d74793711ca8d7a` under the frozen paper rubric. The review covers the new opportunity-exposure paragraph, its linked evidence and the source appendix. [Frozen paper rubric](../docs/model-spec.md#frozen-independent-paper-rubric)

The maximum noisy-opportunity shares on pages 16 and 17 agree with the six boundary records. In manuscript order the limits round to 87.4%, 80.6% and 60.5% for the full fit, and 72.5%, 61.1% and 39.3% after union deletion. The checkpoint decisions support adding the paragraph. At 75% noisy opportunities, the full fit gives 4,233 and 3,971 passes under the two score rules, and 3,616.5 expected passes under the indicator rule. At 50% noisy opportunities, the deletion fit gives 4,410, 4,153 and 3,591.5, respectively. [Frozen specification](../docs/model-spec.md#q4-intermittent-noise-at-100-m-freeze) | [Checkpoints](../results/q4_intermittent_noise_checks.csv) | [Boundary counts](../results/q4_intermittent_noise_limits.csv)

The new text describes the modeled prefix for one state per opportunity and explains the offset possible when averaging scores before applying the cutoff. The implication concerns measuring exposure at playback opportunities alongside average power. It keeps receiver noise and behavioral loss hypothetical and conditions the time-share interpretation on uniform opportunity timing. [Pinned results](https://github.com/feiniao87968492-stack/apmcm-2026-problem-c/blob/965d20b2a8d4517f78e59c21fd9ef7d52bdd6b1b/docs/q4-intermittent-noise.md)

| Frozen rubric dimension | Score | Verification |
|---|---:|---|
| Numerical and factual accuracy | 30/30 | The three criteria, six rounded limits and interpretation of the opportunity fraction agree with the frozen specification and exports. |
| Traceability | 15/15 | The compiled link on page 17 points to the tracked results note at the pinned commit. Each of the seven figures has its CSV and metadata companions. |
| Coverage and reasoning | 30/30 | The text distinguishes within-draw score averaging, continuous mean-power exposure and mixed state indicators. The conservation implication stays within the modeled scenarios. |
| Clarity and structure | 15/15 | The paragraph starts at the foot of page 16 and continues legibly at the top of page 17. The two new source listings start on pages 144 and 160. |
| Build and references | 10/10 | A clean archive compiled in two passes. The body and references occupy pages 3 through 20 of 174. The appendices begin on page 21. All 68 tracked Python modules appear exactly once. Every team header and the PDF author field are anonymous. |

I ran `pdflatex -interaction=nonstopmode -halt-on-error main.tex` twice from the `paper/` directory of a fresh Git archive with `SOURCE_DATE_EPOCH=1795731780`. The rebuilt PDF SHA-256 is `e46cb528c291fcc546d4a3fa1bdbd813c06972a59f0b0883bd219f0f33229b13`. [Anonymous PDF](../paper/main.pdf)
