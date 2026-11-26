# Q3 decomposition of behavior probability gaps

The protocol froze at `9795561` and ran at `49929bc`. Let (p) be the probability of any response and (q) the share of responders showing a given event or exact behavior combination. Averaging the two reference-arm decompositions gives the response-frequency term ((p_N-p_C)(q_N+q_C)/2) and the responder-composition term ((p_N+p_C)(q_N-q_C)/2). The terms describe the observed and modeled group responses.

| Pairs | Event | Natural minus control | Response frequency | Responder composition [95% date interval] |
|---|---|---:|---:|---:|
| All 139 | Head raising | 30.2 | 34.5 | −4.3 [−12.1, 2.0] |
| All 139 | Vocalizing | 51.1 | 29.1 | 22.0 [14.5, 30.8] |
| All 139 | Approach | 16.5 | 6.6 | 9.9 [7.4, 13.1] |
| 49 same-distance and same-size | Head raising | 20.4 | 31.5 | −11.1 [−24.4, 2.2] |
| 49 same-distance and same-size | Vocalizing | 55.1 | 28.8 | 26.3 [11.6, 40.0] |
| 49 same-distance and same-size | Approach | 18.4 | 7.0 | 11.4 [6.6, 17.5] |

Values are percentage points. The all-pair natural and control responder denominators are 90 and 18, and the matched denominators are 33 and eight. All 300 date draws have positive response counts in both arms for both subsets. The tables provide intervals for both terms and the marginal gap, together with the three events and seven exact positive masks. [Raw estimates and counts](../results/behavior_gap_raw.csv)

For standardization, mix the eight mask probabilities using the empirical context weights at eight birds before conditioning on any response. Across all nine call and distance settings, the marginal point estimates for composition are negative for head raising and positive for vocalizing and approach. For two-voice at 150 m, the modeled vocalizing gap is 55.2 points, made up of 44.4 points of frequency and 10.8 points of composition. The respective date intervals are [21.8, 59.6] and [0.6, 25.3] points. Within 25 m of that distance, both natural trials responded and the sole control trial gave no response. The local counts show where the standardized predictions draw heavily on the broader fit. [Standardized estimates, intervals and coverage](../results/behavior_gap_standardized.csv)
