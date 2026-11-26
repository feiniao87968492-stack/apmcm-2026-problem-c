"""Certify continuous recovery priorities with isotonic block breakpoints."""
from itertools import combinations

import numpy as np
import pandas as pd
from scipy.optimize import isotonic_regression

import q2
from missing_propagation import NOMINAL_COUNT
from recovery import PAIR, TOL, label
from spatial_annulus import average


def breakpoints(endpoints, knot):
    """Find adjacent-block equalities in either isotonic fit along one axis."""
    low, high = endpoints[:, knot]
    candidates = [low, high]
    for data in endpoints:
        offsets = data.copy()
        offsets[knot] = 0
        slopes = np.zeros_like(data)
        slopes[knot] = 1
        for start, split, stop in combinations(range(len(data) + 1), 3):
            slope = slopes[start:split].mean() - slopes[split:stop].mean()
            if slope:
                offset = offsets[start:split].mean() - offsets[split:stop].mean()
                value = -offset / slope
                if low < value < high:
                    candidates.append(value)
    return np.unique(candidates)


def residual_width(endpoints, distance, response):
    fitted = [isotonic_regression(row, increasing=False).x for row in endpoints]
    difference = q2.interpolated(distance, fitted[1] - fitted[0])
    return average(difference * response, distance, area=True)


def evaluate_unit(endpoints, knots, call, knot, distance, response):
    bounds = endpoints[:, call, :].copy()
    widths = []
    for value in knots:
        bounds[:, knot] = value
        widths.append(residual_width(bounds, distance, response[call]))
    return np.asarray(widths)


def run(completions, missing, distance, behavior, plans, output):
    weights = np.asarray(q2.WEIGHTS["equal"])
    endpoints = np.clip(np.stack([weights @ completions[k] for k in ("lower", "upper")]), 0, 1)
    # Average the completed representations before clipping, as in the archived fit.
    midpoint = np.clip(weights @ (completions["available"] * (1 - missing / NOMINAL_COUNT)), 0, 1)
    units = {label((i, j)): (i, j) for i in range(len(q2.CALLS)) for j in range(len(q2.KNOTS))}
    winners = plans.loc[plans.selected_minimax]
    natural, control = behavior["natural"], behavior["control"]
    rows, candidates = [], []
    for loss in (0., .20):
        response = (1 - loss) * (natural - loss * np.maximum(natural - control, 0))
        base = [residual_width(endpoints[:, i], distance, response[i]) for i in range(len(q2.CALLS))]
        baseline = sum(base[i] for i in PAIR)
        for winner in winners.itertuples(index=False):
            residual = baseline
            discrete_residual = baseline
            attaining = []
            for name in winner.plan.split("|"):
                i, j = units[name]
                knots = breakpoints(endpoints[:, i], j)
                widths = evaluate_unit(endpoints, knots, i, j, distance, response)
                index = widths.argmax()
                discrete_knots = (endpoints[0, i, j], midpoint[i, j], endpoints[1, i, j])
                discrete_widths = evaluate_unit(endpoints, discrete_knots, i, j, distance, response)
                residual += widths[index] - base[i]
                discrete_residual += discrete_widths.max() - base[i]
                attaining.append(f"{knots[index]:.16g}")
                candidates.extend(dict(loss=loss, budget=winner.budget, plan=winner.plan,
                                       unit=name, knot=value, call_width=width)
                                  for value, width in zip(knots, widths))
            minimum = baseline - residual
            discrete = baseline - discrete_residual
            row = dict(loss=loss, budget=winner.budget, plan=winner.plan,
                       baseline_width=baseline, maximum_residual_width=residual,
                       minimum_shrinkage=minimum, minimum_fraction=minimum / baseline,
                       discrete_minimum=discrete, discrete_minus_continuous=discrete-minimum,
                       worst_knots="|".join(attaining))
            if loss == 0:
                rivals = plans.loc[plans.budget.eq(winner.budget) & plans.plan.ne(winner.plan)]
                rival = rivals.loc[rivals.minimum_reduction.idxmax()]
                if abs(discrete - winner.minimum_reduction) > TOL:
                    raise ValueError("Clean three-value minimum differs from the archived calculation")
                margin = minimum - rival.minimum_reduction
                if margin <= TOL:
                    raise ValueError("Discrete bounds leave a competing recovery plan unresolved")
                row.update(competitor=rival.plan, competitor_upper_bound=rival.minimum_reduction,
                           certificate_margin=margin, competitors_excluded=len(rivals))
            rows.append(row)
    pd.DataFrame(rows).to_csv(output / "recovery_continuous.csv", index=False)
    pd.DataFrame(candidates).to_csv(output / "recovery_breakpoints.csv", index=False)
