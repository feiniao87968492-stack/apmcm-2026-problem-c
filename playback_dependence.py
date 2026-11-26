"""Sensitivity to playback grouping and planning precision."""
import numpy as np
import pandas as pd

from creative_q3 import fit_structured
import q3
from round2 import mask_scores


def grouped_scores(frame, design, output):
    natural = frame.loc[frame.Type.eq("call")].set_index("expID")
    track = frame.expID.map(natural.PlaybackTrack)
    if frame.Date.isna().any() or track.isna().any() or frame.groupby("expID").Date.nunique().ne(1).any():
        raise ValueError("Each playback pair requires one date and a natural track")
    y, stimulus = frame["mask"].to_numpy(), frame.Type.to_numpy()
    records = []
    for scheme, group, other in (("date", frame.Date, track), ("track", track, frame.Date)):
        for group_id, value in enumerate(sorted(group.unique()), 1):
            test = group.eq(value).to_numpy()
            train = ~test
            frequencies = np.empty((test.sum(), len(q3.MASKS)))
            unseen_stimulus_masks = 0
            for label in q3.STIMULI:
                counts = np.bincount(y[train & (stimulus == label)], minlength=len(q3.MASKS))
                in_test = stimulus[test] == label
                frequencies[in_test] = (counts + .5) / (counts.sum() + 4)
                unseen_stimulus_masks += np.count_nonzero(counts[y[test][in_test]] == 0)
            models = {
                "smoothed_stimulus": frequencies,
                "full_multinomial": q3.fit_masks(design[train], y[train], design[test]),
                "pairwise": fit_structured(design[train], y[train], design[test], interactions=True),
            }
            for model, probabilities in models.items():
                loss, brier = mask_scores(probabilities, y[test]).mean(axis=0)
                records.append({
                    "scheme": scheme, "fold": group_id, "model": model,
                    "test_rows": test.sum(), "test_pairs": frame.expID[test].nunique(),
                    "test_rows_other_group_seen": other[test].isin(other[train]).sum(),
                    "test_rows_mask_unseen": (~np.isin(y[test], y[train])).sum(),
                    "test_rows_stimulus_mask_unseen": unseen_stimulus_masks,
                    "test_rows_call_unseen": (~frame.assigned_call[test].isin(frame.assigned_call[train])).sum(),
                    "mask_log_loss": loss, "any_response_brier": brier,
                })
    folds = pd.DataFrame(records)
    folds.to_csv(output / "dependence_q3_folds.csv", index=False)
    totals = []
    for (scheme, model), rows in folds.groupby(["scheme", "model"], sort=False):
        total = {"scheme": scheme, "model": model, "folds": len(rows),
                 "min_test_pairs": rows.test_pairs.min(), "max_test_pairs": rows.test_pairs.max()}
        total.update(rows.filter(regex="^test_").sum().to_dict())
        for metric in ("mask_log_loss", "any_response_brier"):
            total[metric] = np.average(rows[metric], weights=rows.test_rows)
        totals.append(total)
    pd.DataFrame(totals).to_csv(output / "dependence_q3_pooled.csv", index=False)


def date_draws(frame, design, contexts, weights, distances, sampled_dates):
    group_rows = [np.flatnonzero(frame.Date.eq(date)) for date in sorted(frame.Date.unique())]
    grid = q3.probability_grid(distances, contexts, 8)
    grid_x = q3.features(grid, contexts)
    y = frame["mask"].to_numpy()
    shape = (len(q3.STIMULI), len(q3.CALLS), len(distances), len(contexts))
    predictions = []
    natural_masks = []
    representative = np.searchsorted(distances, q3.REPRESENTATIVE)
    point_masks = q3.fit_masks(design, y, grid_x).reshape(*shape, len(q3.MASKS))
    point_mixed = np.einsum("scdjm,j->scdm", point_masks[:, :, representative], weights)
    date_mixed = []
    for dates in sampled_dates:
        rows = np.concatenate([group_rows[i] for i in dates])
        masks = q3.fit_masks(design[rows], y[rows], grid_x).reshape(*shape, len(q3.MASKS))
        p = 1 - masks[..., 0]
        predictions.append(p.reshape(shape) @ weights)
        natural_masks.append(masks[0])
        date_mixed.append(np.einsum("scdjm,j->scdm", masks[:, :, representative], weights))
    return np.asarray(predictions), point_masks[0], np.stack(natural_masks), point_mixed, np.stack(date_mixed)


def margin_table(propagation, behavior, date_predictions, crossed_predictions=None):
    fidelity, draws = propagation["fidelity"], propagation["draws"]
    natural, control = behavior["natural"], behavior["control"]
    point_cutoff = (fidelity[:, 0] * natural[:, 0]).mean() / 2
    records = []
    schemes = (("expID", behavior["natural_draws"], behavior["control_draws"]),
               ("date", date_predictions[:, 0], date_predictions[:, 1]))
    if crossed_predictions is not None:
        schemes += (("crossed", crossed_predictions[:, 0], crossed_predictions[:, 1]),)
    for scheme, p, q in schemes:
        cutoff = (draws[:, :, 0] * p[:, :, 0]).mean(axis=1) / 2
        for loss in (0, .20):
            point = fidelity * (1 - loss) * (natural - loss * np.maximum(natural - control, 0))
            index = draws * (1 - loss) * (p - loss * np.maximum(p - q, 0))
            for i, call in enumerate(propagation["calls"]):
                for j in np.flatnonzero(np.isin(propagation["distance"], (50, 100, 150))):
                    margin = index[:, i, j] - cutoff
                    low, high = np.quantile(margin, [.025, .975])
                    n_pass = int(np.count_nonzero(margin >= 0))
                    records.append({
                        "resampling": scheme, "call": call, "distance_m": propagation["distance"][j],
                        "coupled_loss": loss, "point_cutoff": point_cutoff,
                        "point_margin": point[i, j] - point_cutoff,
                        "point_attains": point[i, j] >= point_cutoff,
                        "margin_low": low, "margin_high": high, "draws_attaining": n_pass,
                        "draws": len(margin), "attainment_share": n_pass / len(margin),
                        "passes_80": n_pass * 5 >= len(margin) * 4,
                    })
    return pd.DataFrame(records)


def trial_precision(output):
    cells = pd.read_csv(output / "decision_q4_trial.csv").query("allocation == 'equal'").copy()
    target = .20
    cells["target_half_width"] = target
    cells["required_pairs_per_arm"] = np.maximum(
        5, np.ceil(2 * cells.within_pair_difference_variance * (1.96 / target)**2).astype(int),
    )
    columns = ["call", "distance_m", "assumed_rho", "applied_rho", "paired_covariance",
               "within_pair_difference_variance", "half_width_95", "target_half_width",
               "required_pairs_per_arm"]
    cells[columns].to_csv(output / "dependence_q4_trial_cells.csv", index=False)
    records = []
    for rho, group in cells.groupby("assumed_rho"):
        se = np.sqrt(group.contrast_variance.sum()) / len(group)
        records.append({
            "assumed_rho": rho, "planning_pairs": 120, "mean_contrast_standard_error": se,
            "mean_contrast_half_width_95": 1.96 * se, "worst_cell_half_width_95": group.half_width_95.max(),
            "cell_half_width_target": target, "minimum_total_pairs": 2 * group.required_pairs_per_arm.sum(),
            "equal_allocation_total_pairs": 2 * len(group) * group.required_pairs_per_arm.max(),
        })
    pd.DataFrame(records).to_csv(output / "dependence_q4_trial_summary.csv", index=False)


def run(data, output, seed, n_boot, propagation, behavior):
    frame = q3.load_playbacks(data)
    counts = frame.loc[frame.Type.eq("call"), "Context"].value_counts(normalize=True).sort_index()
    contexts = tuple(counts.index)
    design = q3.features(frame, contexts)
    grouped_scores(frame, design, output)
    n_dates = frame.Date.nunique()
    sampled_dates = np.random.default_rng(seed + 2).integers(n_dates, size=(n_boot, n_dates))
    draws, point_masks, natural_masks, point_mixed, date_mixed = date_draws(
        frame, design, contexts, counts.to_numpy(), propagation["distance"], sampled_dates,
    )
    margin_table(propagation, behavior, draws).to_csv(output / "dependence_q4_margins.csv", index=False)
    trial_precision(output)
    return frame, sampled_dates, draws, point_masks, natural_masks, point_mixed, date_mixed
