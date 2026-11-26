"""Final grouped playback comparisons and fixed-prediction influence analysis."""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import q1
import q3
import q4
from round2 import mask_scores, playback_matrices, report_playback_scores, score_frame


def recording_influence(output):
    oof = pd.read_csv(output / "round2_q1_predictions.csv")
    pairs = (("random_forest", "shared_features"), ("xgboost", "shared_features"),
             ("xgboost", "random_forest"))
    actual = oof.actual.to_numpy()
    names = ("shared_features", "random_forest", "xgboost")
    predictions = {name: oof[name].to_numpy() for name in names}
    all_scores = {name: q1.comparison_scores(actual, prediction)[[0, 3]]
                  for name, prediction in predictions.items()}
    rows = []
    for group in sorted(oof.recording_group.unique()):
        removed = oof.recording_group.eq(group).to_numpy()
        keep = ~removed
        scores = {name: q1.comparison_scores(actual[keep], prediction[keep])[[0, 3]]
                  for name, prediction in predictions.items()}
        for candidate, baseline in pairs:
            for i, metric in enumerate(("macro_f1", "two_voice_recall")):
                full = all_scores[candidate][i] - all_scores[baseline][i]
                deleted = scores[candidate][i] - scores[baseline][i]
                rows.append({
                    "recording_group": group,
                    **{f"removed_{call}": int(np.sum(removed & (actual == call))) for call in q1.CALLS},
                    "candidate": candidate, "baseline": baseline, "metric": metric,
                    "logistic_full": all_scores["shared_features"][i],
                    "logistic_after_deletion": scores["shared_features"][i],
                    "full_difference": full, "deleted_difference": deleted,
                    "influence": deleted - full, "sign_reversal": full * deleted < 0,
                })
    pd.DataFrame(rows).to_csv(output / "final_q1_group_influence.csv", index=False)


def two_stage(train_x, train_y, test_x):
    responded = train_y != 0
    binary = make_pipeline(StandardScaler(), LogisticRegression(C=1, max_iter=1000))
    binary.fit(train_x, responded)
    probability = binary.predict_proba(test_x)[:, 1]
    masks = q3.fit_masks(train_x[responded], train_y[responded], test_x)
    masks[:, 1:] *= probability[:, None]
    masks[:, 0] = 1 - probability
    if not np.allclose(masks.sum(axis=1), 1):
        raise ValueError("Two-stage mask probabilities must sum to one")
    return masks


def binary_scores(masks, y):
    p = 1 - masks[:, 0]
    event = y != 0
    return np.column_stack((-np.log(np.where(event, p, 1 - p).clip(1e-12)), (p - event) ** 2))


def validate_playback(frame, full, reduced, output, seed, n_boot):
    folds = list(GroupKFold(5).split(frame, groups=frame.expID))
    y = frame["mask"].to_numpy()
    stimulus = frame.Type.to_numpy()
    behavior_names = ("stimulus_frequency", "full_multinomial", "two_stage")
    curve_names = ("full_multinomial", "stimulus_distance")
    behavior_scores = np.empty((len(y), 2, len(behavior_names)))
    curve_scores = np.empty((len(y), 2, len(curve_names)))
    for train, test in folds:
        full_prediction = q3.fit_masks(full[train], y[train], full[test])
        reduced_prediction = q3.fit_masks(reduced[train], y[train], reduced[test])
        two_stage_prediction = two_stage(full[train], y[train], full[test])
        frequency = np.empty_like(full_prediction)
        for label in q3.STIMULI:
            observed = y[train[stimulus[train] == label]]
            frequency[stimulus[test] == label] = (
                np.bincount(observed, minlength=len(q3.MASKS)) / len(observed)
            )
        for i, p in enumerate((frequency, full_prediction, two_stage_prediction)):
            behavior_scores[test, :, i] = mask_scores(p, y[test])
        for i, p in enumerate((full_prediction, reduced_prediction)):
            curve_scores[test, :, i] = binary_scores(p, y[test])

    metrics = ("mask_log_loss", "any_response_brier")
    scores = score_frame(frame, folds, behavior_scores, metrics, behavior_names)
    report_playback_scores(scores, metrics, output, "q3", seed + 2, n_boot, prefix="final")
    metrics = ("binary_log_loss", "any_response_brier")
    scores = score_frame(frame, folds, curve_scores, metrics, curve_names)
    report_playback_scores(scores, metrics, output, "q4", seed + 3, n_boot, prefix="final")


def reduced_behavior(frame, reduced, distance, seed, n_boot):
    context = (sorted(frame.Context.unique())[0],)
    grid = q3.probability_grid(distance, context, 8)
    grid_x = np.column_stack((grid.Type.eq("call"), np.log1p(grid.Distance)))
    y = frame["mask"].to_numpy()
    shape = (len(q3.STIMULI), len(q3.CALLS), len(distance))
    point = (1 - q3.fit_masks(reduced, y, grid_x)[:, 0]).reshape(shape)
    rng = np.random.default_rng(seed)
    pairs = len(frame) // 2
    draws = []
    for groups in rng.integers(pairs, size=(n_boot, pairs)):
        rows = (2 * groups[:, None] + np.arange(2)).ravel()
        probabilities = q3.fit_masks(reduced[rows], y[rows], grid_x)
        draws.append((1 - probabilities[:, 0]).reshape(shape))
    return point, np.asarray(draws)


def effectiveness(fidelity, curve, scenario):
    natural, control = curve[..., 0, :, :], curve[..., 1, :, :]
    loss, gate, coupled = scenario
    if coupled:
        return q4.environment(fidelity, natural, control, loss, gate)[0]
    return (1 - loss) * fidelity * natural


def radius_sensitivity(propagation, behavior, reduced_point, reduced_draws, output):
    distance = propagation["distance"]
    fidelity, draws = propagation["fidelity"], propagation["draws"]
    full = np.stack([behavior["natural"], behavior["control"]])
    full_draws = np.stack([behavior["natural_draws"], behavior["control_draws"]], axis=1)
    references = .5 * fidelity[:, 0] * full[0, :, 0]
    draw_references = .5 * draws[:, :, 0] * full_draws[:, 0, :, 0]
    scenarios = {
        "clean": (0, 0, False), "gate_060": (0, .6, True), "gate_070": (0, .7, True),
        "loss_20_acoustic_only": (.2, 0, False), "loss_20_coupled": (.2, 0, True),
    }
    radii, attainment = [], []
    for name, scenario in scenarios.items():
        full_index = effectiveness(fidelity, full, scenario)
        reduced_index = effectiveness(fidelity, reduced_point, scenario)
        full_boot = effectiveness(draws, full_draws, scenario)
        reduced_boot = effectiveness(draws, reduced_draws, scenario)
        for i, call in enumerate(propagation["calls"]):
            for policy, cutoff, sampled in (
                ("call_specific", references[i], draw_references[:, i]),
                ("common", references.mean(), draw_references.mean(axis=1)),
            ):
                common = {"scenario": name, "call": call, "threshold_policy": policy, "cutoff": cutoff}
                baseline, full_status = q4.radius(distance, full_index[i], cutoff)
                candidate, reduced_status = q4.radius(distance, reduced_index[i], cutoff)
                base_draws, base_flags = zip(*(q4.radius(distance, v, c)
                                               for v, c in zip(full_boot[:, i], sampled)))
                test_draws, test_flags = zip(*(q4.radius(distance, v, c)
                                               for v, c in zip(reduced_boot[:, i], sampled)))
                low, high = np.quantile(np.asarray(test_draws) - base_draws, [.025, .975])
                full_low, full_high = np.quantile(base_draws, [.025, .975])
                reduced_low, reduced_high = np.quantile(test_draws, [.025, .975])
                radii.append({
                    **common, "full_radius_m": baseline, "reduced_radius_m": candidate,
                    "full_status": full_status, "reduced_status": reduced_status,
                    "bounded_difference_m": candidate - baseline, "difference_low_m": low,
                    "difference_high_m": high, "full_low_m": full_low, "full_high_m": full_high,
                    "reduced_low_m": reduced_low, "reduced_high_m": reduced_high,
                    "full_draws_below_support": base_flags.count("below_support"),
                    "reduced_draws_below_support": test_flags.count("below_support"),
                    "full_draws_above_support": base_flags.count("above_support"),
                    "reduced_draws_above_support": test_flags.count("above_support"),
                })
                for j in np.flatnonzero(np.isin(distance, (50, 100, 150))):
                    attainment.append({
                        **common, "distance_m": distance[j], "full_index": full_index[i, j],
                        "reduced_index": reduced_index[i, j], "full_meets": full_index[i, j] >= cutoff,
                        "reduced_meets": reduced_index[i, j] >= cutoff,
                    })
    pd.DataFrame(radii).to_csv(output / "final_q4_radii.csv", index=False)
    pd.DataFrame(attainment).to_csv(output / "final_q4_cutoff_attainment.csv", index=False)


def run(data, output, seed, n_boot, propagation, behavior):
    recording_influence(output)
    frame = q3.load_playbacks(data)
    matrices = playback_matrices(frame)
    full, reduced = matrices["add_context_group"], matrices["add_distance"]
    validate_playback(frame, full, reduced, output, seed, n_boot)
    point, draws = reduced_behavior(frame, reduced, propagation["distance"], seed + 2, n_boot)
    radius_sensitivity(propagation, behavior, point, draws, output)
    return point, draws
