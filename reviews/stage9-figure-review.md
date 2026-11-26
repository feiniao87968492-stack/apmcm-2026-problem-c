# Stage 9 independent figure review

All five result PNGs decoded successfully and were inspected visually. At source resolution, axes, symbols, legend entries and panel labels remain readable without clipping or collisions. The corresponding CSVs contained plotted rows and each metadata sidecar parsed as JSON. The manuscript references all five assets.

| Manuscript figure | Result stem | PNG size | Plot rows | Visual and content check |
|---|---|---|---|---|
| 1 | q1_acoustics | 3660 × 1200 | 36 | Scaled quartile ranges and medians, grouped confusion counts and held-out permutation importance agree with the caption. |
| 2 | q2_propagation | 1875 × 1095 | 1,515 | Colors and line styles distinguish the call types. Discrete means, fitted curves and narrow pointwise bands are present. |
| 3 | q3_response_curve | 2700 × 930 | 1,566 | Three call panels show solid natural and dashed control probability curves. Shading shows the 95% paired bootstrap interval for natural stimuli. |
| 4 | q4_scenarios | 3000 × 1050 | 2,349 | All three scenarios and the dotted clean reference appear in each panel. The threshold curve coincides with the clean curve above the gate and drops to zero below it, as confirmed from the CSV. |
| 5 | q3_behavior_masks | 2430 × 1050 | 48 | The eight response categories and six trial strata are readable. Predictions use 100 m, eight birds and empirical context frequencies. |

Pass for the source figure artifacts. The Figure 3 caption can identify the shaded interval as natural-stimulus uncertainty, and the Figure 5 caption can give its exact prediction conditions. PDF page layout is checked on the compiled manuscript.
