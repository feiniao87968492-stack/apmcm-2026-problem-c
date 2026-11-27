"""Predict each held-out propagation distance from shorter measurements."""
from itertools import combinations

import numpy as np
import pandas as pd

import physical_attenuation as physical
import q2
from q2_shape_rank import MODELS, fit_all


TARGETS = (64, 128, 256)
DRAWS = 300
SEED = 20261127


def predict(targets):
    """Return model predictions with axes model, call and held-out distance."""
    predictions = np.empty((len(MODELS), len(q2.CALLS), len(TARGETS)))
    for index, distance in enumerate(TARGETS):
        train = q2.KNOTS < distance
        fits = fit_all(q2.KNOTS[train], targets[:, train])
        for model_index, model in enumerate(MODELS):
            fit = fits[model]
            predictions[model_index, :, index] = (
                fit[:, -1] if model == "isotonic" else physical.curve(np.array([distance]), fit)[:, 0]
            )
    return predictions


def summarize(observed, predictions):
    residual = predictions - observed[:, :, -3:][:, None]
    rows, contrasts = [], []
    selections = [(call, [i]) for i, call in enumerate(q2.CALLS)] + [
        ("pooled", list(range(len(q2.CALLS))))
    ]
    targets = [(str(distance), [i]) for i, distance in enumerate(TARGETS)] + [("128_256", [1, 2])]
    for call, call_indices in selections:
        for target, target_indices in targets:
            selected = residual[:, :, call_indices, :][:, :, :, target_indices]
            means = selected.mean(axis=(2, 3))
            rmses = np.sqrt((selected**2).mean(axis=(2, 3)))
            scope = {"call": call, "target_m": target, "cells": len(call_indices) * len(target_indices)}
            for i, model in enumerate(MODELS):
                rows.append({**scope, "model": model, "mean_error": means[0, i], "rmse": rmses[0, i]})
            for i, j in combinations(range(len(MODELS)), 2):
                for metric, values in (("rmse", rmses), ("mean_error", means)):
                    delta = values[:, j] - values[:, i]
                    lo, hi = np.quantile(delta[1:], [.025, .975])
                    contrasts.append({**scope, "model": MODELS[j], "reference": MODELS[i],
                                      "metric": metric, "difference": delta[0],
                                      "low95": lo, "high95": hi, "draws": len(delta) - 1})
    return pd.DataFrame(rows), pd.DataFrame(contrasts)


def write(data, output):
    tables = q2.load_tables(data)
    rng = np.random.default_rng(SEED)
    observed, support = [], []
    for call, arrays in tables.items():
        means = np.concatenate((np.nanmean(arrays, axis=1)[None], q2.bootstrap_means(arrays, DRAWS, rng)))
        # Match the published stream before advancing to the next call.
        if np.all(np.isnan(arrays) == np.isnan(arrays[:1])):
            q2.bootstrap_means(arrays, DRAWS, rng, aligned=True)
        observed.append(np.stack([physical.equal_means(draw) for draw in means]))
        for metric, values in zip(q2.METRICS, arrays):
            for distance in TARGETS:
                column = values[:, q2.KNOTS == distance]
                support.append({"call": call, "representation": metric, "distance_m": distance,
                                "available": np.isfinite(column).sum(), "rows": len(column)})
    observed = np.stack(observed, axis=1)
    predictions = np.stack([predict(draw) for draw in observed])
    cells = []
    for i, model in enumerate(MODELS):
        for j, call in enumerate(q2.CALLS):
            for k, distance in enumerate(TARGETS):
                actual = observed[0, j, np.searchsorted(q2.KNOTS, distance)]
                prediction = predictions[0, i, j, k]
                cells.append({"model": model, "call": call, "distance_m": distance,
                              "last_training_m": distance / 2, "observed": actual,
                              "predicted": prediction, "error": prediction - actual})
    scores, contrasts = summarize(observed, predictions)
    output.mkdir(parents=True, exist_ok=True)
    for name, table in (("holdouts", pd.DataFrame(cells)), ("support", pd.DataFrame(support)),
                        ("scores", scores), ("contrasts", contrasts)):
        table.to_csv(output / f"q2_forward_{name}.csv", index=False, lineterminator="\n")
