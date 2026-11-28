# Core Q1 classification

The five released date-location folds hold out all 108 recordings. Inside each outer training fold, three recording-group folds select model settings by pooled log loss. The physical representation uses duration, first fundamental, peak-to-fundamental ratio, interquartile bandwidth, normalized peak location and quartile skewness. [Frozen design](model-spec.md#core-upgrade-q1-and-integrated-q4-freeze)

| Model | Macro F1 | Flat / modulated / two-voice recall | Log loss | Summed Brier |
|---|---:|---:|---:|---:|
| Fixed original logistic | 0.314 | 0.523 / 0.375 / 0.083 | 1.223 | 0.738 |
| Training prevalence | 0.229 | 0.523 / 0.275 / 0.000 | 1.090 | 0.664 |
| Tuned original logistic | 0.326 | 0.591 / 0.425 / 0.042 | 1.127 | 0.690 |
| Tuned original forest | 0.350 | 0.636 / 0.550 / 0.000 | 1.067 | 0.648 |
| Tuned physical logistic | 0.337 | 0.659 / 0.400 / 0.042 | 1.126 | 0.684 |
| Tuned physical forest | 0.392 | 0.659 / 0.675 / 0.000 | 0.974 | 0.582 |

The physical forest gains 0.077 macro F1 (paired 95% interval 0.022–0.151) and improves both probability scores against prevalence. Its two-voice recall is 0/24 compared with 2/24 for the fixed logistic. The unweighted forest fails the two-voice recall requirement. [Scores and selection](../results/core_q1_scores.csv) · [Held-out probabilities](../results/core_q1_oof.csv) · [Training-only settings](../results/core_q1_settings.csv)

The follow-up selected the balanced physical forest. It scored 0.5032 macro F1, a gain of 0.1888 [0.0683, 0.3103] against fixed logistic. It recovered 13/24 two-voice calls at precision 13/34 and scored 0.9778 for log loss and 0.5875 for summed Brier. Balanced-subsample weighting scored 0.5000 with 12/24 recovered. The train-only decision multiplier scored 0.4765 with 8/24 recovered. Its proper scores use the original physical forest probabilities. [Follow-up freeze](model-spec.md#antigravity-3-q1-and-q4-freeze) ? [Scores](../results/core_q1_scores.csv) ? [Figure 1 confusion matrix](../results/core_figure1.csv)

F02 is recorded for all 24 two-voice recordings and for none of the other 84. Pulse rate appears in 34/40 modulated and 20/24 two-voice recordings, with none in 44 flat recordings. These availability patterns can encode how calls were annotated. The physical representation uses neither field. The three supplementary clips have Hann-window spectral peaks of 978, 792 and 845 Hz in flat, modulated and two-voice order, with interquartile bandwidths of 331, 317 and 325 Hz. Their different peak locations and overlapping bandwidths illustrate the spectral coordinates used here. Each type contributes one clip. [Availability audit](../results/core_q1_availability.csv) · [Example spectra summaries](../results/core_q1_wav.csv)

## What drives held-out classifications

We shuffled each physical predictor 40 times within the held-out recording folds, keeping the selected forest and its fold settings fixed. Normalized peak position, log first fundamental and log peak-to-fundamental ratio give mean pooled macro F1 decreases of 0.069, 0.048 and 0.042, respectively. The figure reports the standard deviation across shuffles. These summaries depend on the fitted ensemble and on the observed relationships among the predictors. [Frozen design](model-spec.md#antigravity-4-manuscript-figures-and-archive-checks) ? [Figure](../results/core_figure1.png) ? [Plotted data](../results/core_figure1.csv)
