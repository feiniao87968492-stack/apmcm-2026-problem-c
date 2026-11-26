"""Prioritize equal-cost historical recovery units using completion bounds."""
from itertools import combinations, product

import numpy as np
import pandas as pd

import q2
from missing_propagation import NOMINAL_COUNT, isotonic_curves
from q4 import environment
from spatial_annulus import average, limits

VALUES = (-1, 0, 1)
PAIR = (2, 1)
TOL = 1e-12


def label(unit):
    call, distance = unit
    return f"{q2.CALLS[call]}_{q2.KNOTS[distance]:g}m"


def fitted_bounds(completions, missing, plan, values):
    curves = []
    for name, endpoint in (("lower", -1), ("upper", 1)):
        means = completions[name].copy()
        for (i, j), value in zip(plan, values):
            means[i, :, j] += (value - endpoint) * missing[i, :, j] / NOMINAL_COUNT
        curves.append(isotonic_curves(means))
    return np.array(curves)


def area_bounds(knots, distance, natural, control, loss):
    fidelity = np.stack([
        [q2.interpolated(distance, row) for row in endpoint] for endpoint in knots
    ])
    return np.stack([
        average(environment(endpoint, natural, control, loss, 0)[0], distance, area=True)
        for endpoint in fidelity
    ])


def pair_gap(bounds, first, second):
    lower, upper = bounds
    return lower[..., first] - upper[..., second], upper[..., first] - lower[..., second]


def audit(missing, output):
    rows = []
    eligible = []
    for i, call in enumerate(q2.CALLS):
        for j, distance in enumerate(q2.KNOTS):
            counts = missing[i, :, j]
            if counts.sum():
                eligible.append((i, j))
            rows.append(dict(unit=label((i, j)), call=call, distance_m=distance,
                             total_missing=counts.sum(), **dict(zip(q2.METRICS, counts))))
    pd.DataFrame(rows).to_csv(output / "recovery_units.csv", index=False)
    return eligible


def detail(knots, case, distance, natural, control, draws, radii, gaps):
    for threshold in (.50, .60):
        for i, call in enumerate(q2.CALLS):
            lower, upper = [q2.radius(endpoint[i], threshold) for endpoint in knots]
            radii.append(dict(case, threshold=threshold, call=call,
                              lower_m=lower[0], lower_status=lower[1],
                              upper_m=upper[0], upper_status=upper[1]))

    for loss in (0., .20):
        point = area_bounds(knots, distance, natural, control, loss)
        boot = area_bounds(knots, distance, draws[:, 0], draws[:, 1], loss)
        for i, j in combinations(range(len(q2.CALLS)), 2):
            low, high = pair_gap(point, i, j)
            draw_low, draw_high = pair_gap(boot, i, j)
            first, second = q2.CALLS[i], q2.CALLS[j]
            gaps.append(dict(case, loss=loss, first=first, second=second,
                             gap_lower=low, gap_upper=high,
                             identified=first if low > 0 else second if high < 0 else "none",
                             **limits(draw_low, "lower_endpoint"), **limits(draw_high, "upper_endpoint"),
                             share_first_identified=(draw_low > 0).mean(),
                             share_second_identified=(draw_high < 0).mean()))


def run(completions, missing, distance, behavior, draws, output):
    units = audit(missing, output)
    natural, control = behavior["natural"], behavior["control"]
    baseline_knots = fitted_bounds(completions, missing, (), ())
    baseline = area_bounds(baseline_knots, distance, natural, control, 0.)
    baseline_low, baseline_high = pair_gap(baseline, *PAIR)
    width = baseline_high - baseline_low
    case_rows, plan_rows, radii, gaps = [], [], [], []
    detail(baseline_knots, dict(plan="none", values="none"), distance, natural, control,
           draws, radii, gaps)
    for budget in (1, 2):
        plans = {}
        for plan in combinations(units, budget):
            name = "|".join(map(label, plan))
            count = sum(missing[i, :, j].sum() for i, j in plan)
            reductions = []
            for values in product(VALUES, repeat=budget):
                knots = fitted_bounds(completions, missing, plan, values)
                low, high = pair_gap(area_bounds(knots, distance, natural, control, 0.), *PAIR)
                residual = high - low
                reduction = width - residual
                reductions.append(reduction)
                case_rows.append(dict(budget=budget, plan=name, values="|".join(map(str, values)),
                                      gap_lower=low, gap_upper=high, width=residual,
                                      baseline_width=width, reduction=reduction,
                                      relative_reduction=reduction/width))
            plans[plan] = (name, count, min(reductions), max(reductions))
        best = max(result[2] for result in plans.values())
        optimum = next(plan for plan, result in plans.items() if result[2] >= best - TOL)
        highest_count = max(plans, key=lambda plan: plans[plan][1])
        for plan, (name, count, worst, best_case) in plans.items():
            plan_rows.append(dict(budget=budget, plan=name, total_missing=count,
                                  minimum_reduction=worst, maximum_reduction=best_case,
                                  minimum_relative_reduction=worst/width,
                                  maximum_relative_reduction=best_case/width,
                                  selected_minimax=plan == optimum, selected_count=plan == highest_count))
        for plan in dict.fromkeys((optimum, highest_count)):
            for values in product(VALUES, repeat=budget):
                case = dict(plan=plans[plan][0], values="|".join(map(str, values)))
                detail(fitted_bounds(completions, missing, plan, values), case,
                       distance, natural, control, draws, radii, gaps)
    for name, rows in (("plans", plan_rows), ("cases", case_rows), ("radii", radii), ("gaps", gaps)):
        pd.DataFrame(rows).to_csv(output / f"recovery_{name}.csv", index=False)
