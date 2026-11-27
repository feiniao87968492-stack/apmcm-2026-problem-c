"""Diagnose supported-distance Q4 decisions by deleting intact playback pairs."""
import numpy as np
import pandas as pd

import noise_scenarios
import q3
from behavior_ablation import coverage
from control_subtraction import reference, score_curves
from spatial_annulus import limits


def pair_filters(frame):
    near = frame.Distance.between(125, 175).groupby(frame.expID).transform("any")
    far = frame.Distance.gt(175).groupby(frame.expID).transform("any")
    filters = {
        "full": np.ones(len(frame), dtype=bool),
        "drop_near": ~near.to_numpy(),
        "drop_far": ~far.to_numpy(),
        "drop_union": ~(near | far).to_numpy(),
    }
    membership = np.select([near & far, near, far], ["both", "near_only", "far_only"], default="neither")
    pairs = frame.loc[frame.Type.eq("call"), ["assigned_call"]].assign(
        band=membership[frame.Type.eq("call")],
    )
    overlap = pd.crosstab(pairs.assigned_call, pairs.band).reindex(
        index=q3.CALLS, columns=["neither", "near_only", "far_only", "both"], fill_value=0,
    )
    overlap.loc["all"] = overlap.sum()
    return filters, overlap


def training_counts(frame, eligible, model):
    for (call, stimulus), cell in frame.assign(kept=eligible).groupby(["assigned_call", "Type"]):
        for kept in (True, False):
            part = cell.loc[cell.kept.eq(kept)]
            yield dict(model=model, call=call, stimulus=stimulus, kept=kept, trials=len(part),
                       responses=part["mask"].ne(0).sum(), dates=part.Date.nunique(),
                       min_m=part.Distance.min(), max_m=part.Distance.max())


def refit(frame, eligible, sampled_dates, weights, distances=q3.REPRESENTATIVE, *, context_specific=False):
    contexts = tuple(weights.index)
    design = q3.features(frame, contexts)
    target = q3.features(q3.probability_grid(np.asarray(distances), contexts, 8), contexts)
    masks = frame["mask"].to_numpy()
    shape = (len(q3.STIMULI), len(q3.CALLS), len(distances), len(contexts))

    def predict(rows):
        zero = q3.fit_masks(design[rows], masks[rows], target)[:, 0].reshape(shape)
        response = 1 - zero
        return response if context_specific else response @ weights.to_numpy()

    blocks = [np.flatnonzero(eligible & frame.Date.eq(d)) for d in sorted(frame.Date.unique())]
    draws = np.full((len(sampled_dates), *(shape if context_specific else shape[:-1])), np.nan)
    for i, dates in enumerate(sampled_dates):
        rows = np.concatenate([blocks[j] for j in dates])
        if len(rows):
            draws[i] = predict(rows)
    return predict(np.flatnonzero(eligible)), draws


def row_change(name, point, draws, base_point, base_draws):
    delta = draws - base_draws
    return {name: point, **limits(draws, name), f"{name}_delta": point-base_point,
            **limits(delta, f"{name}_delta")}


def run(frame, sampled_dates, propagation, behavior, date_predictions,
        parameters, sampled_parameters, output):
    distance, calls = propagation["distance"], propagation["calls"]
    positions = np.searchsorted(distance, q3.REPRESENTATIVE)
    iso, iso_draws = propagation["fidelity"], propagation["draws"]
    full_point = np.stack((behavior["natural"], behavior["control"]))
    references = {
        "gross": (reference(iso, full_point[0]), reference(iso_draws, date_predictions[:, 0])),
        "net_own": (reference(iso, full_point[0]-full_point[1]),
                    reference(iso_draws, date_predictions[:, 0]-date_predictions[:, 1])),
    }
    fidelity = noise_scenarios.fidelity(distance, parameters, 0)[..., positions]
    sampled = noise_scenarios.fidelity(distance, sampled_parameters, 0)[..., positions]
    base_point, base_draws = full_point[..., positions], date_predictions[..., positions]
    weights = frame.loc[frame.Type.eq("call"), "Context"].value_counts(normalize=True).sort_index()
    filters, overlap = pair_filters(frame)
    overlap.to_csv(output / "distance_deletion_overlap.csv")

    counts, support, records = [], [], []
    for model, eligible in filters.items():
        assert frame.loc[eligible].groupby("expID").size().eq(2).all()
        counts.extend(training_counts(frame, eligible, model))
        retained = frame.loc[eligible]
        for row in coverage(retained):
            distances = retained.loc[retained.assigned_call.eq(row["call"])
                                     & retained.Type.eq(row["stimulus"]), "Distance"]
            support.append(dict(row, model=model, retained_min_m=distances.min(),
                                retained_max_m=distances.max(),
                                beyond_range=not distances.min() <= row["distance_m"] <= distances.max()))
        point, draws = ((base_point, base_draws) if model == "full"
                        else refit(frame, eligible, sampled_dates, weights))
        valid = np.isfinite(draws).all(axis=(1, 2, 3))
        n = valid.sum()
        for loss, link in ((0., "clean"), (.20, "coupled")):
            coupled = loss > 0
            scores = score_curves(fidelity, *point, loss, coupled)
            draw_scores = score_curves(sampled[valid], draws[valid, 0], draws[valid, 1], loss, coupled)
            base_scores = score_curves(fidelity, *base_point, loss, coupled)
            base_samples = score_curves(sampled[valid], base_draws[valid, 0], base_draws[valid, 1], loss, coupled)
            point_n = noise_scenarios.response(*point, loss, coupled)
            draw_n = noise_scenarios.response(draws[valid, 0], draws[valid, 1], loss, coupled)
            base_n = noise_scenarios.response(*base_point, loss, coupled)
            base_draw_n = noise_scenarios.response(base_draws[valid, 0], base_draws[valid, 1], loss, coupled)
            for k, (definition, (cutoff, cutoffs)) in enumerate(references.items()):
                for i, call in enumerate(calls):
                    for j, d in enumerate(q3.REPRESENTATIVE):
                        margin = scores[k][i, j] - cutoff
                        sampled_margin = draw_scores[k][:, i, j] - cutoffs[valid]
                        baseline_margin = base_samples[k][:, i, j] - cutoffs[valid]
                        count = np.count_nonzero(sampled_margin >= 0)
                        base_count = np.count_nonzero(baseline_margin >= 0)
                        passes = 5 * count >= 4 * n
                        records.append(dict(
                            model=model, loss=loss, link=link, definition=definition, call=call,
                            distance_m=d, cutoff=cutoff, point_attains=margin >= 0,
                            **row_change("p_n", point_n[i, j], draw_n[:, i, j],
                                         base_n[i, j], base_draw_n[:, i, j]),
                            **row_change("p_c", point[1, i, j], draws[valid, 1, i, j],
                                         base_point[1, i, j], base_draws[valid, 1, i, j]),
                            **row_change("margin", margin, sampled_margin,
                                         base_scores[k][i, j]-cutoff, baseline_margin),
                            draws=n, count=count, support=count/n, passes_80=passes,
                            support_delta=(count-base_count)/n,
                            decision_changed=passes != (5 * base_count >= 4 * n),
                        ))
    for name, rows in (("training", counts), ("coverage", support), ("points", records)):
        pd.DataFrame(rows).to_csv(output / f"distance_deletion_{name}.csv", index=False)
