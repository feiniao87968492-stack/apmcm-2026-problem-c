"""Compare Q2 attenuation shape and weight sensitivity on common targets."""
import numpy as np
import pandas as pd
from scipy.optimize import isotonic_regression, least_squares

import physical_attenuation as physical
import q2
from q2_envelope_rank import START, WEIGHTS, equal_spectral

THRESHOLDS = (.50, .70)
MODELS = ("isotonic", "fixed_g", "shared_g", "separate_g")
TIE = 1e-9


def separate_fit(distance, observed):
    def fit_call(values):
        def residual(x):
            ceiling, log_scale, exponent = x
            return ceiling / np.sqrt(1 + (distance / np.exp(log_scale))**exponent) - values

        fit = least_squares(residual, [.9, np.log(100), 2.],
                            bounds=([0., 0., .25], [1., np.log(2048), 8.]),
                            ftol=1e-11, xtol=1e-11, gtol=1e-11)
        if not fit.success:
            raise RuntimeError(fit.message)
        return fit.x[0], np.exp(fit.x[1]), fit.x[2]

    return np.array([fit_call(row) for row in observed])


def fit_all(distance, observed):
    return {
        "isotonic": np.stack([isotonic_regression(row, increasing=False).x for row in observed]),
        "fixed_g": physical.fit(distance, observed, False),
        "shared_g": physical.fit(distance, observed, True),
        "separate_g": separate_fit(distance, observed),
    }


def targets(metric_means, weight):
    return np.clip(np.asarray(equal_spectral(weight)) @ metric_means, 0., 1.)


def rank(radii):
    order = sorted(range(len(radii)), key=lambda i: -radii[i])
    groups = [[order[0]]]
    for i in order[1:]:
        if radii[groups[-1][0]] - radii[i] <= TIE:
            groups[-1].append(i)
        else:
            groups.append([i])
    return ">".join("=".join(q2.CALLS[i] for i in sorted(group)) for group in groups)


def radius_rows(fits, weight):
    for model, values in fits.items():
        radius = q2.radius if model == "isotonic" else physical.fitted_radius
        for threshold in THRESHOLDS:
            distances, statuses = zip(*(radius(row, threshold) for row in values))
            row = dict(model=model, weight=weight, threshold=threshold,
                       mod_minus_tv_m=distances[1] - distances[2], rank=rank(distances))
            for call, value, status in zip(q2.CALLS, distances, statuses):
                row.update({f"{call}_m": value, f"{call}_status": status})
            yield row


def holdouts(observed, weight):
    for i in range(1, len(q2.KNOTS) - 1):
        keep = np.arange(len(q2.KNOTS)) != i
        train = q2.KNOTS[keep]
        distance = q2.KNOTS[i:i+1]
        for model, fit in fit_all(train, observed[:, keep]).items():
            if model == "isotonic":
                predictions = [np.interp(np.log(distance[0]), np.log(train), row) for row in fit]
            else:
                predictions = physical.curve(distance, fit)[:, 0]
            for call, actual, prediction in zip(q2.CALLS, observed[:, i], predictions):
                yield dict(model=model, weight=weight, call=call, distance_m=distance[0],
                           observed=actual, predicted=prediction, error=prediction-actual)


def run(metrics, output):
    means, draws = zip(*(metrics[call] for call in q2.CALLS))
    folds, radii = [], []
    for weight in WEIGHTS:
        observed = targets(np.stack(means), weight)
        folds.extend(holdouts(observed, weight))
        radii.extend(radius_rows(fit_all(q2.KNOTS, observed), weight))
    folds = pd.DataFrame(folds)
    scores = (pd.concat([folds, folds.assign(call="pooled")])
              .groupby(["weight", "model", "call"], as_index=False)
              .error.agg(rmse=lambda error: np.sqrt(np.mean(error**2))))

    equal = scores.loc[scores.weight.eq(START)].pivot(index="model", columns="call", values="rmse")
    gain = 1 - equal.loc["separate_g", "pooled"] / equal.loc["shared_g", "pooled"]
    all_calls = (equal.loc["separate_g", list(q2.CALLS)] <= equal.loc["shared_g", list(q2.CALLS)]).all()
    decision = pd.DataFrame([dict(weight=START, pooled_relative_gain=gain, no_worse_call=all_calls,
                                 prefer_separate=bool(gain >= .05 and all_calls))])
    samples = pd.DataFrame([dict(draw=index, **row)
                            for index, sample in enumerate(zip(*draws), 1)
                            for row in radius_rows(fit_all(q2.KNOTS, targets(np.stack(sample), START)), START)])
    gaps = []
    for (model, threshold), group in samples.groupby(["model", "threshold"]):
        gap = group.mod_minus_tv_m
        low, median, high = gap.quantile([.025, .5, .975])
        gaps.append(dict(model=model, threshold=threshold, draws=len(gap), low95_m=low, median_m=median,
                         high95_m=high, mod_ahead=(gap > TIE).sum(), tv_ahead=(gap < -TIE).sum(),
                         tied=(gap.abs() <= TIE).sum()))
    ranks = samples.groupby(["model", "threshold", "rank"], as_index=False).size().rename(columns={"size": "count"})
    for name, result in (("holdouts", folds), ("rmse", scores), ("radii", pd.DataFrame(radii)),
                         ("draws", samples), ("gaps", pd.DataFrame(gaps)), ("ranks", ranks),
                         ("decision", decision)):
        result.to_csv(output / f"q2_shape_rank_{name}.csv", index=False, lineterminator="\n")
