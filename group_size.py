"""Paired group-size contrasts, strict prediction, and size-specific Q4 scenarios."""
from itertools import combinations

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sklearn.preprocessing import StandardScaler

import q3
from q4 import environment
from sea_state import probability

STRATA = ("at_most_4", "5_to_12", "at_least_13")
SIZES = (2, 8, 20)


def size_stratum(size):
    return np.digitize(size, [5, 13])


def paired_contrasts(natural, control, samples, output):
    n = natural.ResponseYesNo.to_numpy(dtype=bool)
    c = control.ResponseYesNo.to_numpy(dtype=bool)
    date = natural.Date.to_numpy()
    sizes = size_stratum(natural.Npenguins)
    matched = ((natural.Distance.to_numpy() == control.Distance.to_numpy())
               & (natural.Npenguins.to_numpy() == control.Npenguins.to_numpy()))
    difference = n.astype(int) - c
    rows = []
    for subset, eligible in (("all", np.ones(len(n), dtype=bool)), ("same_distance_size", matched)):
        for size, stratum in enumerate(STRATA):
            selected = eligible & (sizes == size)
            by_date = [selected & (date == d) for d in sorted(set(date))]
            totals = np.array([difference[block].sum() for block in by_date])
            counts = np.array([block.sum() for block in by_date])
            denominators = counts[samples].sum(axis=1)
            valid = denominators > 0
            draws = totals[samples[valid]].sum(axis=1) / denominators[valid]
            low, high = np.quantile(draws, [.025, .975]) if valid.any() else (np.nan, np.nan)
            rows.append({
                "subset": subset, "stratum": stratum, "pairs": selected.sum(),
                "dates": np.count_nonzero(counts), "natural_responses": (selected & n).sum(),
                "control_responses": (selected & c).sum(), "natural_only": (selected & n & ~c).sum(),
                "control_only": (selected & c & ~n).sum(),
                "difference": difference[selected].mean() if selected.any() else np.nan,
                "low95": low, "high95": high, "draws": valid.sum(),
            })
    pd.DataFrame(rows).to_csv(output / "group_size_pair_contrasts.csv", index=False)


def cloglog(train, y, test, train_offset, test_offset):
    scale = StandardScaler().fit(train)
    x = np.column_stack((np.ones(len(train)), scale.transform(train)))
    target = np.column_stack((np.ones(len(test)), scale.transform(test)))

    def objective(beta):
        eta = x @ beta + train_offset
        hazard = np.exp(eta)
        positive_hazard = hazard[y]
        # For very small hazards, log(1-exp(-hazard)) approaches eta.
        tiny = eta[y] < -30
        log_response = eta[y].copy()
        log_response[~tiny] = np.log(-np.expm1(-positive_hazard[~tiny]))
        slope = hazard.copy()
        # Above 50 the positive-row derivative is negligible at optimizer tolerance.
        interior = (~tiny) & (positive_hazard < 50)
        positive_slope = np.zeros_like(positive_hazard)
        positive_slope[tiny] = -1
        positive_slope[interior] = -positive_hazard[interior] / np.expm1(positive_hazard[interior])
        slope[y] = positive_slope
        penalty = np.r_[0., beta[1:]]
        value = hazard[~y].sum() - log_response.sum() + (penalty @ penalty) / 2
        return value, x.T @ slope + penalty

    solution = minimize(objective, np.zeros(x.shape[1]), jac=True, method="L-BFGS-B",
                        options={"maxiter": 1000, "ftol": 1e-12, "gtol": 1e-8})
    if not solution.success:
        raise RuntimeError(solution.message)
    estimates = -np.expm1(-np.exp(target @ solution.x + test_offset))
    return estimates, solution.x[-1] / scale.scale_[-1]


def validate(frame, natural, design, samples, output):
    date = natural.Date.to_numpy()
    track = natural.PlaybackTrack.to_numpy()
    y = frame.ResponseYesNo.to_numpy(dtype=bool)
    log_size = np.log(frame.Npenguins.to_numpy())
    other = design[:, :-1]
    relaxed = np.column_stack((other, log_size))
    names = ("logit", "cloglog_offset", "cloglog_free")
    fold_rows, score_totals, sizes = [], [], []
    for held in sorted(set(date)):
        test = date == held
        train = ~test & ~np.isin(track, track[test])
        tr, te = np.repeat(train, 2), np.repeat(test, 2)
        fixed, _ = cloglog(other[tr], y[tr], other[te], log_size[tr], log_size[te])
        free, coefficient = cloglog(relaxed[tr], y[tr], relaxed[te], 0., 0.)
        estimates = np.column_stack((probability(design[tr], y[tr], design[te]), fixed, free))
        outcome = y[te, None]
        loss = -np.log(np.maximum(np.where(outcome, estimates, 1 - estimates), 1e-12))
        brier = (estimates - outcome)**2
        totals = np.stack([loss.sum(axis=0), brier.sum(axis=0)], axis=1)
        score_totals.append(totals)
        sizes.append(te.sum())
        for name, (ll, bs), beta_size in zip(names, totals / te.sum(), (np.nan, 1., coefficient)):
            fold_rows.append({
                "date": held, "model": name, "train_pairs": train.sum(), "test_pairs": test.sum(),
                "purged_pairs": (~test & ~train).sum(), "log_n_coefficient": beta_size,
                "log_loss": ll, "brier": bs,
            })
    sizes, totals = np.asarray(sizes), np.asarray(score_totals)
    point = totals.sum(axis=0) / sizes.sum()
    draws = totals[samples].sum(axis=1) / sizes[samples].sum(axis=1)[:, None, None]
    rows = []
    for reference, candidate in combinations(range(len(names)), 2):
        delta = draws[:, candidate] - draws[:, reference]
        delta_low, delta_high = np.quantile(delta, [.025, .975], axis=0)
        for j, metric in enumerate(("log_loss", "brier")):
            reference_low, reference_high = np.quantile(draws[:, reference, j], [.025, .975])
            score_low, score_high = np.quantile(draws[:, candidate, j], [.025, .975])
            rows.append({
                "reference": names[reference], "model": names[candidate], "metric": metric,
                "reference_score": point[reference, j], "reference_low95": reference_low,
                "reference_high95": reference_high, "score": point[candidate, j], "low95": score_low,
                "high95": score_high, "delta": point[candidate, j] - point[reference, j],
                "delta_low95": delta_low[j], "delta_high95": delta_high[j],
                "joint_gain": (delta_high < 0).all(),
            })
    pd.DataFrame(fold_rows).to_csv(output / "group_size_strict_folds.csv", index=False)
    pd.DataFrame(rows).to_csv(output / "group_size_strict_scores.csv", index=False)


def scenarios(frame, design, contexts, weights, samples, propagation, behavior, date_predictions, output):
    distances = np.array(q3.REPRESENTATIVE)
    locations = np.searchsorted(propagation["distance"], distances)
    f = propagation["fidelity"][:, locations]
    fd = propagation["draws"][:, :, locations]
    point_cutoff = (propagation["fidelity"][:, 0] * behavior["natural"][:, 0]).mean() / 2
    cutoffs = (propagation["draws"][:, :, 0] * date_predictions[:, 0, :, 0]).mean(axis=1) / 2
    points = {8: np.stack((behavior["natural"][:, locations], behavior["control"][:, locations]))}
    draws = {8: date_predictions[..., locations]}
    target = pd.concat([q3.probability_grid(distances, contexts, size) for size in (2, 20)])
    target_x = q3.features(target, contexts)
    shape = (2, len(q3.STIMULI), len(q3.CALLS), len(distances), len(contexts))
    masks = frame["mask"].to_numpy()
    groups = [np.flatnonzero(frame.Date.eq(d)) for d in sorted(frame.Date.unique())]

    def predict(rows):
        any_probability = 1 - q3.fit_masks(design[rows], masks[rows], target_x)[:, 0]
        return any_probability.reshape(shape) @ weights

    point_new = predict(np.arange(len(frame)))
    draw_new = np.stack([predict(np.concatenate([groups[i] for i in dates])) for dates in samples])
    for i, size in enumerate((2, 20)):
        points[size], draws[size] = point_new[i], draw_new[:, i]

    rows, coverage = [], []
    for loss in (0., .20):
        point_base, _ = environment(f, *points[8], loss, 0)
        draw_base, _ = environment(fd, draws[8][:, 0], draws[8][:, 1], loss, 0)
        for size in SIZES:
            index, p = environment(f, *points[size], loss, 0)
            draw_index, draw_p = environment(fd, draws[size][:, 0], draws[size][:, 1], loss, 0)
            for i, call in enumerate(q3.CALLS):
                for j, distance in enumerate(distances):
                    margin = draw_index[:, i, j] - cutoffs
                    margin_low, margin_high = np.quantile(margin, [.025, .975])
                    diff = draw_index[:, i, j] - draw_base[:, i, j]
                    diff_low, diff_high = np.quantile(diff, [.025, .975])
                    p_low, p_high = np.quantile(draw_p[:, i, j], [.025, .975])
                    count = np.count_nonzero(margin >= 0)
                    rows.append({
                        "n": size, "call": call, "distance_m": distance, "loss": loss,
                        "point_cutoff": point_cutoff, "response_probability": p[i, j],
                        "count_lower": p[i, j], "count_upper": size * p[i, j],
                        "count_lower_low95": p_low, "count_lower_high95": p_high,
                        "count_upper_low95": size * p_low, "count_upper_high95": size * p_high,
                        "point_margin": index[i, j] - point_cutoff,
                        "margin_low95": margin_low, "margin_high95": margin_high,
                        "delta_margin_vs_8": index[i, j] - point_base[i, j],
                        "delta_margin_low95": diff_low, "delta_margin_high95": diff_high,
                        "draws_attaining": count, "draws": len(samples), "attainment": count / len(samples),
                        "passes_80": 5 * count >= 4 * len(samples),
                    })
    strata = size_stratum(frame.Npenguins)
    for size in SIZES:
        for call in q3.CALLS:
            for distance in distances:
                local = frame.assigned_call.eq(call) & frame.Distance.sub(distance).abs().le(25)
                for stimulus in q3.STIMULI:
                    eligible = local & frame.Type.eq(stimulus)
                    for scope, selection in (("exact", frame.Npenguins.eq(size)),
                                             ("stratum", strata == size_stratum(size))):
                        part = frame.loc[eligible & selection]
                        coverage.append({
                            "n": size, "call": call, "distance_m": distance, "stimulus": stimulus,
                            "coverage": scope, "trials": len(part), "responses": part.ResponseYesNo.sum(),
                            "dates": part.Date.nunique(),
                        })
    pd.DataFrame(rows).to_csv(output / "group_size_q4.csv", index=False)
    pd.DataFrame(coverage).to_csv(output / "group_size_q4_coverage.csv", index=False)


def run(frame, samples, propagation, behavior, date_predictions, output):
    natural, control = frame.iloc[::2], frame.iloc[1::2]
    counts = natural.Context.value_counts(normalize=True).sort_index()
    contexts = tuple(counts.index)
    design = q3.features(frame, contexts)
    paired_contrasts(natural, control, samples, output)
    validate(frame, natural, design, samples, output)
    scenarios(frame, design, contexts, counts.to_numpy(), samples,
              propagation, behavior, date_predictions, output)
