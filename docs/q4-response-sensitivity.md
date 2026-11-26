# Q4 response sensitivity at 6 dB

At 100 m, the four acoustic curves use the same 4,800 paired draws, full-data clean cutoff and shared-exponent acoustic retention ratio r. Positive response excess retains r raised to lambda. The local ratio varies by distance, and the matched uniform ratio uses its value at 100 m in the same draw. [Frozen protocol](model-spec.md#q4-response-sensitivity-at-6-db-freeze)

| Behavior fit | Loss shape | Prefix counts at lambda 0 / .25 / .50 / .75 / 1 | Prefix limit | Endpoint limit | Endpoint minus prefix |
|---|---|---|---:|---:|---:|
| Full | Local | 4,538 / 4,367 / 4,108 / 3,721 / 3,230 | 0.683627 | 0.683627 | 0 |
| Full | Uniform | 4,530 / 4,360 / 4,097 / 3,692 / 3,168 | 0.667481 | 0.683627 | 0.016146 |
| Union deletion | Local | 4,288 / 3,983 / 3,547 / 2,986 / 2,430 | 0.339062 | 0.344207 | 0.005145 |
| Union deletion | Uniform | 4,278 / 3,956 / 3,500 / 2,920 / 2,330 | 0.319405 | 0.344207 | 0.024802 |

All eight fitted boundaries qualify in exactly 3,840 draws. Increasing lambda by 1e-7 gives 3,839 draws in each case. The endpoint limits match between spatial scenarios because their retention ratios match at 100 m. The prefix adds every evaluated node from 20 m. For the union-deleted fit, the 100 m target is at the natural arm's retained maximum and within the control range. Lambda describes hypothetical response sensitivity and requires field evidence. [Full-precision estimates and counts](../results/q4_response_sensitivity.csv)

Run `python main.py --data "<attachment directory>/date" --q4-response-sensitivity`.
