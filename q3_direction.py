"""Predict the response direction in equal-size discordant playback pairs."""
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import expit
from sklearn.preprocessing import StandardScaler

import q3
from q4_tail_models import Design, fit_pair_eta, validation_folds
from strict_playback import joint_table

MODELS = ("half_count", "independent", "shared_or", "firth_distance", "firth_call")
CONTRASTS = [(model, MODELS[0]) for model in MODELS[1:]] + [
    ("firth_call", "firth_distance"), ("shared_or", "independent"),
]


def design_matrix(natural_distance, control_distance, calls):
    ratio = np.log2(natural_distance / control_distance)
    return np.column_stack((ratio, *(np.asarray(calls) == call for call in q3.CALLS[1:])))


def firth(x, y, target):
    scale = StandardScaler().fit(x) if len(y) else None
    if scale is None or len(np.unique(y)) < 2:
        return np.full(len(target), (y.sum()+.5)/(len(y)+1)), True
    design = np.column_stack((np.ones(len(x)), scale.transform(x)))
    if np.linalg.matrix_rank(design) < design.shape[1]:
        return np.full(len(target), (y.sum()+.5)/(len(y)+1)), True

    def objective(beta):
        eta = design @ beta
        p = expit(eta)
        variance = expit(-eta) * p
        info = design.T @ (variance[:, None] * design)
        sign, determinant = np.linalg.slogdet(info)
        if sign <= 0:
            return np.inf, np.zeros_like(beta)
        leverage = variance * np.sum(design * np.linalg.solve(info, design.T).T, axis=1)
        gradient = design.T @ (y - p + leverage * (.5 - p))
        return np.sum(np.logaddexp(0, eta) - y*eta) - .5*determinant, -gradient

    fit = minimize(objective, np.zeros(design.shape[1]), jac=True, method="BFGS",
                   options={"gtol": 1e-9, "maxiter": 500})
    if not np.isfinite(fit.fun) or np.linalg.norm(fit.jac, ord=np.inf) > 1e-7:
        raise RuntimeError(f"Firth optimization failed: {fit.message}")
    return expit(fit.x[0] + scale.transform(target) @ fit.x[1:]), False


def models(frame, contexts, training, evaluation, pair_x, labels, target):
    """Return conditional direction predictions and unconditional joint cells."""
    frequency = (labels.sum() + .5) / (len(labels) + 1)
    x = q3.features(frame, contexts)
    target_x = q3.features(evaluation, contexts)
    rows = np.flatnonzero(np.repeat(training, 2))
    y = frame["mask"].to_numpy()[rows]
    masks = q3.fit_masks(x[rows], y, np.vstack((x[rows], target_x)))
    eta = fit_pair_eta(masks[:len(rows)], y)
    natural, control = (1 - masks[len(rows):, 0]).reshape(-1, 2).T
    independent = np.column_stack(((1-natural)*(1-control), (1-natural)*control,
                                   natural*(1-control), natural*control))
    joint = {"independent": independent, "shared_or": joint_table(natural, control, eta)}
    probabilities = {MODELS[0]: np.full(len(target), frequency)}
    fallback = {}
    for name, cells in joint.items():
        probabilities[name] = direction(cells)
    for name, n in (("firth_distance", 1), ("firth_call", 3)):
        probabilities[name], fallback[name] = firth(pair_x[:, :n], labels, target[:, :n])
    return probabilities, fallback, joint, eta


def direction(cells):
    return cells[:, 2] / cells[:, 1:3].sum(axis=1)


def counts(mask, outcomes):
    part = outcomes[mask]
    natural, control = part.T
    return dict(pairs=len(part), natural_only=int((natural & ~control).sum()),
                control_only=int((control & ~natural).sum()),
                both=int((natural & control).sum()), neither=int((~natural & ~control).sum()))


def run(frame, output):
    natural, control = frame.iloc[::2], frame.iloc[1::2]
    weights = natural.Context.value_counts(normalize=True).sort_index()
    contexts = tuple(weights.index)
    design = Design(frame, contexts)
    outcomes = frame["mask"].ne(0).to_numpy().reshape(-1, 2)
    discordant = outcomes[:, 0] != outcomes[:, 1]
    labels = outcomes[:, 0]
    equal_size = natural.Npenguins.to_numpy() == control.Npenguins.to_numpy()
    equal_distance = natural.Distance.to_numpy() == control.Distance.to_numpy()
    features = design_matrix(natural.Distance.to_numpy(), control.Distance.to_numpy(), natural.assigned_call)
    fold_rows, score_sums, fold_counts = [], [], []
    for fold, (_, held, tracks, _, train, _) in enumerate(validation_folds(design, tail_only=False), 1):
        training, testing = train & equal_size, held & equal_size
        eligible, test = training & discordant, testing & discordant
        evaluation = frame.iloc[np.flatnonzero(np.repeat(test, 2))]
        predicted, fallback, _, eta = models(frame, contexts, training, evaluation,
                                             features[eligible], labels[eligible], features[test])
        scored = []
        for name in MODELS:
            p = predicted[name]
            observed = np.where(labels[test], p, 1-p)
            scores = np.column_stack((-np.log(observed.clip(1e-12)), (p-labels[test])**2))
            scored.append(scores.sum(axis=0))
            fold_rows.append(dict(fold=fold, model=name,
                                  **{f"train_{k}": v for k, v in counts(training, outcomes).items()},
                                  **{f"test_{k}": v for k, v in counts(testing, outcomes).items()},
                                  train_held_date=int((training & held).sum()),
                                  train_held_track=int((training & np.isin(design.tracks, tracks)).sum()),
                                  fallback=fallback.get(name, False), log_odds_ratio=eta if name=="shared_or" else None,
                                  log_loss=scores[:, 0].mean() if len(p) else np.nan,
                                  brier=scores[:, 1].mean() if len(p) else np.nan))
        score_sums.append(scored)
        fold_counts.append(int(test.sum()))

    totals, fold_counts = np.asarray(score_sums), np.asarray(fold_counts)
    sample = np.random.default_rng(20261201).integers(len(fold_counts), size=(4800, len(fold_counts)))
    denominators = fold_counts[sample].sum(axis=1)
    valid = denominators > 0
    draws = totals[sample[valid]].sum(axis=1) / denominators[valid, None, None]
    point = totals.sum(axis=0) / fold_counts.sum()
    score_rows = []
    for i, name in enumerate(MODELS):
        for j, metric in enumerate(("log_loss", "brier")):
            low, high = np.quantile(draws[:, i, j], [.025, .975])
            score_rows.append(dict(model=name, metric=metric, value=point[i, j], low95=low, high95=high,
                                   pairs=fold_counts.sum(), dates=np.count_nonzero(fold_counts),
                                   valid_draws=valid.sum(),
                                   fallbacks=sum(row["fallback"] for row in fold_rows if row["model"] == name)))
    differences = []
    for lhs, rhs in CONTRASTS:
        i, k = MODELS.index(lhs), MODELS.index(rhs)
        low, high = np.quantile(draws[:, i] - draws[:, k], [.025, .975], axis=0)
        for j, metric in enumerate(("log_loss", "brier")):
            differences.append(dict(model=lhs, comparator=rhs, metric=metric,
                                    delta=point[i, j]-point[k, j], low95=low[j], high95=high[j],
                                    valid_draws=valid.sum()))

    # Order each synthetic pair as natural then control at an identical condition.
    grid = q3.probability_grid(np.asarray(q3.REPRESENTATIVE), contexts, 8)
    grid = grid.assign(arm=grid.Type.map({"call": 0, "control": 1})).sort_values(
        ["assigned_call", "Distance", "Context", "arm"], kind="stable",
    )
    active = equal_size & discordant
    grid_natural = grid.iloc[::2]
    grid_x = design_matrix(grid_natural.Distance.to_numpy(), grid_natural.Distance.to_numpy(),
                           grid_natural.assigned_call)
    predicted, fallback, joint, eta = models(frame, contexts, equal_size, grid, features[active],
                                             labels[active], grid_x)
    standardized = []
    for (call, distance), positions in grid_natural.groupby(["assigned_call", "Distance"]).indices.items():
        for name in MODELS:
            if name in joint:
                cells = weights.to_numpy() @ joint[name][positions]
                p = direction(cells[None])[0]
            else:
                p = weights.to_numpy() @ predicted[name][positions]
            standardized.append(dict(model=name, call=call, distance_m=distance, birds=8,
                                     probability=p, fallback=fallback.get(name, False),
                                     log_odds_ratio=eta if name=="shared_or" else None))

    raw = []
    for sample_name, selected in (("equal_size", equal_size), ("matched", equal_size & equal_distance)):
        for call in ("all", *q3.CALLS):
            selection = selected if call == "all" else selected & natural.assigned_call.eq(call).to_numpy()
            result = counts(selection, outcomes)
            n = result["natural_only"] + result["control_only"]
            raw.append(dict(sample=sample_name, call=call, **result,
                            dates=len(np.unique(design.dates[selection])),
                            discordant_dates=len(np.unique(design.dates[selection & discordant])),
                            direction=result["natural_only"]/n if n else np.nan))

    for name, rows in (("folds", fold_rows), ("scores", score_rows), ("contrasts", differences),
                       ("standardized", standardized), ("counts", raw)):
        pd.DataFrame(rows).to_csv(output / f"q3_direction_{name}.csv", index=False, lineterminator="\n")
