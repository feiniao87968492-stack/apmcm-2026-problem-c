"""Integrate Q4 indices and supported attainment intervals over the annulus."""
from itertools import combinations

import numpy as np
import pandas as pd

import noise_scenarios
import q2
from q4 import environment, radius


def limits(draws, name):
    low, high = np.quantile(draws, [.025, .975])
    return {f"{name}_low95": low, f"{name}_high95": high}


def average(index, distance, area):
    weights = 2 * np.pi * distance if area else np.ones_like(distance)
    return np.trapezoid(index * weights, distance, axis=-1) / np.trapezoid(weights, distance)


def integrated_scores(scenarios, distance, calls, output):
    scores, gaps = [], []
    clean_point, clean_draws = scenarios[0, "clean", "clean"]
    for key, (point, draws) in scenarios.items():
        db, shape, link = key
        for weight in ("distance", "area"):
            area = weight == "area"
            p, b = average(point, distance, area), average(draws, distance, area)
            p0 = average(clean_point, distance, area)
            b0 = average(clean_draws, distance, area)
            ranks = 1 + (p[None, :] > p[:, None]).sum(axis=1)
            draw_ranks = 1 + (b[:, None, :] > b[:, :, None]).sum(axis=2)
            for i, call in enumerate(calls):
                delta = b0[:, i] - b[:, i]
                scores.append(dict(db=db, shape=shape, link=link, weight=weight, call=call,
                                   score=p[i], **limits(b[:, i], "score"),
                                   loss=p0[i]-p[i], **limits(delta, "loss"),
                                   relative_loss=(p0[i]-p[i])/p0[i],
                                   **limits(delta / b0[:, i], "relative_loss"),
                                   rank=ranks[i], rank_min=draw_ranks[:, i].min(),
                                   rank_max=draw_ranks[:, i].max(),
                                   **limits(draw_ranks[:, i], "rank")))
            for i, j in combinations(range(len(calls)), 2):
                diff = b[:, i] - b[:, j]
                gaps.append(dict(db=db, shape=shape, link=link, weight=weight,
                                 first=calls[i], second=calls[j], gap=p[i]-p[j],
                                 **limits(diff, "gap"), share_first_larger=(diff > 0).mean()))
    pd.DataFrame(scores).to_csv(output / "annulus_scores.csv", index=False)
    pd.DataFrame(gaps).to_csv(output / "annulus_score_gaps.csv", index=False)


def connected_intervals(distance, nodes):
    if not nodes.any():
        return []
    indices = np.flatnonzero(nodes)
    runs = np.split(indices, np.flatnonzero(np.diff(indices) > 1) + 1)
    return [(distance[run[0]], distance[run[-1]]) for run in runs]


def attainment(scenarios, distance, calls, cutoff, draw_cutoffs, output):
    rows, intervals, grid = [], [], []
    denominator = distance[-1]**2 - distance[0]**2

    def record(key, call, passes, outer, status):
        db, shape, link = key
        fields = dict(db=db, shape=shape, link=link, call=call)
        segments = connected_intervals(distance, passes)
        area = sum(hi**2 - lo**2 for lo, hi in segments) / denominator
        radius_area = (outer**2 - distance[0]**2) / denominator
        rows.append(dict(fields, area_share=area, radius_m=outer, status=status,
                         radius_area_share=radius_area, area_minus_radius=area-radius_area,
                         qualifying_nodes=passes.sum(), connected_intervals=len(segments)))
        intervals.extend(dict(fields, start_m=lo, end_m=hi,
                              area_share=(hi**2-lo**2)/denominator) for lo, hi in segments)

    for i, call in enumerate(calls):
        noisy = []
        for key, (point, draws) in scenarios.items():
            counts = (draws[:, i] >= draw_cutoffs[:, None]).sum(axis=0)
            passes = 5 * counts >= 4 * len(draw_cutoffs)
            outer, status = radius(distance, point[i], cutoff)
            record(key, call, passes, outer, status)
            db, shape, link = key
            grid.extend(dict(db=db, shape=shape, link=link, call=call, distance_m=d,
                             draws_attaining=n, draws=len(draw_cutoffs), passes_80=ok)
                        for d, n, ok in zip(distance, counts, passes))
            if db:
                noisy.append((passes, outer, status))
        common = np.logical_and.reduce([passes for passes, _, _ in noisy])
        outer, status = min(((outer, status) for _, outer, status in noisy),
                            key=lambda item: item[0])
        record(("3_and_6", "intersection", "intersection"), call, common, outer, status)
    pd.DataFrame(rows).to_csv(output / "annulus_attainment.csv", index=False)
    pd.DataFrame(intervals).to_csv(output / "annulus_intervals.csv", index=False)
    pd.DataFrame(grid).to_csv(output / "annulus_attainment_grid.csv", index=False)


def completion_bounds(curves, distance, calls, natural, control, date_predictions, output):
    rows, gaps = [], []
    for loss in (0., .20):
        point, draws = {}, {}
        for name, knots in curves.items():
            fidelity = np.stack([q2.interpolated(distance, values) for values in knots])
            index, _ = environment(fidelity, natural, control, loss, 0)
            boot, _ = environment(fidelity, date_predictions[:, 0], date_predictions[:, 1], loss, 0)
            point[name] = average(index, distance, True)
            draws[name] = average(boot, distance, True)
            for i, call in enumerate(calls):
                rows.append(dict(loss=loss, completion=name, call=call, score=point[name][i],
                                 **limits(draws[name][:, i], "score")))
        for i, j in combinations(range(len(calls)), 2):
            lower = point["lower"][i] - point["upper"][j]
            upper = point["upper"][i] - point["lower"][j]
            draw_lower = draws["lower"][:, i] - draws["upper"][:, j]
            draw_upper = draws["upper"][:, i] - draws["lower"][:, j]
            gaps.append(dict(loss=loss, first=calls[i], second=calls[j],
                             available_gap=point["available"][i] - point["available"][j],
                             gap_lower=lower, gap_upper=upper,
                             identified=calls[i] if lower > 0 else calls[j] if upper < 0 else "none",
                             **limits(draw_lower, "lower_endpoint"), **limits(draw_upper, "upper_endpoint"),
                             share_first_identified=(draw_lower > 0).mean(),
                             share_second_identified=(draw_upper < 0).mean()))
    pd.DataFrame(rows).to_csv(output / "annulus_completion_scores.csv", index=False)
    pd.DataFrame(gaps).to_csv(output / "annulus_completion_gaps.csv", index=False)


def run(propagation, behavior, date_predictions, parameters, sampled_parameters, curves, output):
    distance, calls = propagation["distance"], propagation["calls"]
    natural, control = behavior["natural"], behavior["control"]
    pn, pc = date_predictions[:, 0], date_predictions[:, 1]
    cutoff = (propagation["fidelity"][:, 0] * natural[:, 0]).mean() / 2
    draw_cutoffs = (propagation["draws"][:, :, 0] * pn[:, :, 0]).mean(axis=1) / 2
    settings = [(0, "clean", "clean")] + [
        (db, shape, link) for db in (3, 6) for shape in ("noise_power", "matched_uniform")
        for link in ("acoustic_only", "coupled")
    ]
    scenarios = {}
    for db, shape, link in settings:
        matched, coupled = shape == "matched_uniform", link == "coupled"
        f, loss, _ = noise_scenarios.scenario(distance, parameters, db, matched)
        fd, loss_draws, _ = noise_scenarios.scenario(distance, sampled_parameters, db, matched)
        scenarios[db, shape, link] = (f * noise_scenarios.response(natural, control, loss, coupled),
                                      fd * noise_scenarios.response(pn, pc, loss_draws, coupled))

    integrated_scores(scenarios, distance, calls, output)
    attainment(scenarios, distance, calls, cutoff, draw_cutoffs, output)
    completion_bounds(curves, distance, calls, natural, control, date_predictions, output)
