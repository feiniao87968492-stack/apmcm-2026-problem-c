# Independent verification of first replies and event order

**Pass.** I used the specification frozen at `19ae12e` and independently reconstructed the five outputs from Data02 before inspecting the implementation. The comparison covers the released analysis at `2221807`.

## First-reply matrix

I selected only trials marked `VocalYesNo=1` and rebuilt each stimulus-by-context matrix using the recorded context of that trial. All 76 natural and five control responders have a recognized, nonmissing VR1. For natural trials, the flat, modulated and two-voice counts are 5, 9 and 3 in the after context, 11, 13 and 3 while commuting, and 12, 18 and 2 while searching. The denominators are respectively 17, 27 and 32 vocal responses, or 36, 65 and 38 total trials. The control counts are 1, 0 and 1 in after, 0, 1 and 0 in commuting, and 0, 2 and 0 in searching. For those control cells, the date bootstrap retained 263, 212 and 256 of 300 draws for the conditional shares. All 18 rows agree for counts, date coverage, both sets of denominators, shares and interval limits. [Matrix](../results/first_reply_matrix.csv)

## Strict validation and matching

I formed the held-out tracks on all natural trials for each date and independently removed those tracks before selecting labeled responders. All date, train-pair, test-pair and purged-pair counts match the archived strict coverage. Across the 36 fold rows and six pooled comparison rows, scores, paired intervals and adoption flags agree within 2.02e-16. Cross-entropy and summed Brier were 0.953044 and 0.584543 for pooled proportions, 0.999596 and 0.605943 for context, and 1.023371 and 0.625144 for context and played call. Each paired interval includes zero, supporting retention of the pooled comparison. [Archived strict coverage](../results/strict_q3_coverage.csv) · [Folds](../results/first_reply_folds.csv) · [Comparisons](../results/first_reply_scores.csv)

Among 76 natural responders, 24 first replies matched the played call type, compared with an expected 25.983 under the date-and-context block margins. I reproduced the 19,999 draws, null percentile endpoints of 22 and 30 matches, and one-sided plus-one p-value of 0.8859. Eleven of the 27 occupied blocks contain variation in both labels, covering 40 responders. As a check on simulation precision, I enumerated unique label allocations for the blocks with variation and convolved their match-count distributions, giving a one-sided exact probability of 0.885344 under the same exchangeability assumption. The observed match proportion is 31.6% and the block-marginal expectation is 34.2%. [Matching statistics](../results/first_reply_matching.csv)

## Vocalizing and approach

Of 19 natural trials with both events, all have finite latencies and occur on 11 dates. Eighteen were vocal-first, one was approach-first and none tied. The vocal-first fraction was 94.7% (95% date interval 87.5%–100%), with a mean signed lag of 6.679 seconds (3.607–11.600) and a median lag of 3.6 seconds (2.2–11.6). All date draws had eligible cases. Each released statistic and its interval matches the independent reconstruction. The lags describe first events at group level. [Event order](../results/first_reply_event_order.csv)

## Natural playback detail

I rebuilt all 27 played-call, context and reply cells from Data02 under `8de62a4` and compared them with the export at `abce327`. Counts, both denominators, date coverage, retained bootstrap draws, shares and all percentile endpoints match exactly. Summing the counts over played calls reproduces all nine natural-arm counts. Summing each denominator once per played-call and context cell reproduces the original 17, 27 and 32 responses and 36, 65 and 38 trials across after, commuting and searching. The replies to flat playback number 12 flat, 12 modulated and two two-voice. The counts are 6, 8 and 2 for modulated playback and 10, 20 and 4 for two-voice playback. These recover the known response totals of 26, 16 and 34 and the same-type counts of 12, 8 and 4. The narrowest response support is three responses to modulated playback while commuting. The fewest bootstrap draws with a nonzero response denominator is 268 for modulated playback in the after context. [Played-call detail](../results/first_reply_by_played_call.csv) · [Arm matrix](../results/first_reply_matrix.csv)

## Reproduction

The independent verifier imports no project modules. I ran the temporary verifier and comparison scripts from the repository root.

```powershell
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-reply-verify.py" "<attachment directory>/date" "$env:TEMP/apmcm-reply-independent"
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-reply-compare.py" "$env:TEMP/apmcm-reply-independent" results results
& "$env:TEMP/apmcm-2026-c-round2-venv/Scripts/python.exe" "$env:TEMP/apmcm-reply-detail-verify.py" "<attachment directory>/date" "$env:TEMP/apmcm-reply-independent"
```
