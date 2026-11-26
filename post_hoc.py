"""Post hoc sensitivities using the original held-out predictions and scenario draws."""
import numpy as np
import pandas as pd

from creative_inverse import limit, status
from q3 import MASKS, STIMULI
from q4 import environment
from round2 import mask_scores, report_playback_scores, score_frame


def smoothed_masks(frame, folds, oof, names, output, seed, n_boot):
    actual = frame["mask"].to_numpy()
    stimulus = frame.Type.to_numpy()
    smoothed = np.empty(oof.shape[:2])
    for train, test in folds:
        for label in STIMULI:
            training = actual[train[stimulus[train] == label]]
            counts = np.bincount(training, minlength=len(MASKS))
            smoothed[test[stimulus[test] == label]] = (counts + .5) / (len(training) + 4)
    pairwise = oof[:, :, names.index("pairwise")]
    metrics = ("mask_log_loss", "any_response_brier")
    candidate_scores = mask_scores(pairwise, actual)
    comparator_scores = mask_scores(smoothed, actual)
    scores = np.stack((comparator_scores, candidate_scores), axis=-1)
    grouped = score_frame(frame, folds, scores, metrics, ("smoothed_stimulus", "pairwise"))
    report_playback_scores(grouped, metrics, output, "q3_smoothed", seed, n_boot, prefix="posthoc")

    index = grouped.index
    focal_rows = np.flatnonzero((index.get_level_values("fold") == 1)
                                & (index.get_level_values("pair") == 138)
                                & (stimulus == "call") & (actual == 4))
    records = []
    if len(focal_rows) == 1:
        focal = focal_rows[0]
        divisor = len(folds) * len(folds[0][1])
        for reference in ("stimulus_frequency", "full_multinomial", "two_stage", "smoothed_stimulus"):
            probabilities = smoothed if reference == "smoothed_stimulus" else oof[:, :, names.index(reference)]
            baseline_scores = mask_scores(probabilities, actual)
            difference = candidate_scores - baseline_scores
            aggregate = np.mean([difference[test].mean(axis=0) for _, test in folds], axis=0)
            for i, metric in enumerate(metrics):
                contribution = difference[focal, i] / divisor
                records.append({
                    "fold": 1, "pair": 138, "stimulus": "call", "observed_mask": 4,
                    "baseline": reference, "candidate": "pairwise", "metric": metric,
                    "baseline_observed_probability": probabilities[focal, 4],
                    "candidate_observed_probability": pairwise[focal, 4],
                    "baseline_row_score": baseline_scores[focal, i],
                    "candidate_row_score": candidate_scores[focal, i],
                    "all_rows_difference": aggregate[i], "focal_row_contribution": contribution,
                    "remaining_rows_contribution": aggregate[i] - contribution,
                })
    pd.DataFrame(records).to_csv(output / "posthoc_q3_focal_contribution.csv", index=False)


def inverse_sensitivity(propagation, behavior, reduced, reduced_draws, output):
    f, f_draws = propagation["fidelity"], propagation["draws"]
    full = np.stack((behavior["natural"], behavior["control"]))
    full_draws = np.stack((behavior["natural_draws"], behavior["control_draws"]), axis=1)
    cutoff = .5 * (f[:, 0] * full[0, :, 0]).mean()
    cutoffs = .5 * (f_draws[:, :, 0] * full_draws[:, 0, :, 0]).mean(axis=1)
    losses = np.arange(201) / 1000
    distance = propagation["distance"]
    records = []
    for name, point, draws in (("full", full, full_draws), ("reduced", reduced, reduced_draws)):
        for i, call in enumerate(propagation["calls"]):
            for j in np.flatnonzero(np.isin(distance, (50, 100, 150))):
                for link, control_index in (("acoustic_only", 0), ("coupled", 1)):
                    index, _ = environment(f[i, j], point[0, i, j], point[control_index, i, j], losses, 0)
                    boot, _ = environment(f_draws[:, i, j, None], draws[:, 0, i, j, None],
                                          draws[:, control_index, i, j, None], losses, 0)
                    point_margin = index - cutoff
                    counts = (boot >= cutoffs[:, None]).sum(axis=0)
                    for required in (70, 80, 90):
                        passed = counts * 100 >= required * len(cutoffs)
                        records.append({
                            "behavior_model": name, "call": call, "distance_m": distance[j],
                            "response_link": link, "required_support_percent": required, "cutoff": cutoff,
                            "clean_margin": point_margin[0], "loss_20_margin": point_margin[-1],
                            "point_limit_loss": limit(losses, point_margin >= 0),
                            "point_status": status(point_margin >= 0),
                            "support_limit_loss": limit(losses, passed), "support_status": status(passed),
                            "clean_support": counts[0] / len(cutoffs), "loss_20_support": counts[-1] / len(cutoffs),
                        })
    pd.DataFrame(records).to_csv(output / "posthoc_q4_inverse_sensitivity.csv", index=False)
