# Independent numerical recomputation

**PASS.** The frozen specification is 195a5af. I used separate calculations to verify the outputs at 4130bdd. I reconstructed recording groups and the three feature designs, refit the logistic models and recomputed both classification metrics and paired recording-group intervals. The original predictions match the archived benchmark.

I rebuilt both playback holdouts and confirmed that every experiment pair was intact. A direct ridge normal-equation solve and explicit fold-training time medians reproduced all 18 conditional latency rows, including the unavailable control approach rows. A separately scored four-class prediction reproduced all four timing score rows. I reconstructed all 300 date draws and reproduced the 54 cumulative probability estimates, percentile endpoints and local support counts. [Results](../docs/acoustic-onset.md)
