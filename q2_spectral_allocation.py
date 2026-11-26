"""Test Q2 radius ranks when spectral weight is reallocated."""
from itertools import combinations

import numpy as np
import pandas as pd

import q2
from q2_envelope_rank import START, TOL, direct, pair_path, radius_functions, rank_events, structure

SHARES = (0., .25, .50, .75, 1.)
THRESHOLDS = (.40, .70)
PAIRS = tuple(combinations(range(len(q2.CALLS)), 2))


def envelope_path(s):
    return lambda e: ((1-e)*s, (1-e)*(1-s), e)


def fixed_envelope(s):
    return envelope_path(s)(START)


def evaluate(means, threshold, weights):
    endpoints = np.array([weights(0), weights(1)]) @ means
    paths = [list(radius_functions(structure(np.column_stack((a, b-a)), 0., 1.), threshold))
             for a, b in endpoints]
    return {(i, j): pair_path(means[i], means[j], paths[i], paths[j], threshold, weights)
            for i, j in PAIRS}


def leading_calls(means, weights, x, threshold, snap=True):
    radii = np.array([direct(m, x, threshold, snap, weights)[0] for m in means])
    return tuple(name for name, radius in zip(q2.CALLS, radii)
                 if abs(np.log2(radius / radii.max())) <= TOL)


def nearest_switch(means, threshold, paths):
    weights = fixed_envelope
    start = leading_calls(means, weights, .50, threshold)
    if len(start) != 1:
        return dict(start="=".join(start), status="tied_start"), []
    edges = np.unique(np.concatenate(([.50], *(path[0] for path in paths.values()))))
    candidates = []
    for a, b in zip(edges[:-1], edges[1:]):
        boundary = b if b <= .50 else a
        leader = leading_calls(means, weights, (a+b)/2, threshold, snap=False)
        if len(leader) == 1 and leader != start:
            candidates.append((boundary, leader[0]))
    for edge in edges:
        leader = leading_calls(means, weights, edge, threshold)
        if len(leader) == 1 and leader != start:
            candidates.append((edge, leader[0]))
    if not candidates:
        return dict(start=start[0], status="no_switch"), []
    distance = min(abs(edge-.50) for edge, _ in candidates)
    nearest = sorted({(edge, replacement) for edge, replacement in candidates
                      if abs(abs(edge-.50)-distance) <= TOL})
    rows = [dict(s=edge, direction="decrease" if edge < .50 else "increase",
                 replacement=replacement, delta_s=abs(edge-.50),
                 weight_transferred=(1-START)*abs(edge-.50),
                 strict_at_boundary=leading_calls(means, weights, edge, threshold) == (replacement,))
            for edge, replacement in nearest]
    return dict(start=start[0], status="switch"), rows


def run(metrics, output):
    means = np.stack([metrics[call][0] for call in q2.CALLS])
    points, events, switches, draws, summaries = [], [], [], [], []
    paths = [("envelope", s, envelope_path(s), (0., START, 1.)) for s in SHARES]
    paths.append(("spectral", START, fixed_envelope, SHARES))
    for threshold in THRESHOLDS:
        for axis, fixed, weights, checkpoints in paths:
            label = dict(threshold=threshold, axis=axis, fixed=fixed)
            fitted = evaluate(means, threshold, weights)
            for x in checkpoints:
                leader = "=".join(leading_calls(means, weights, x, threshold))
                for call, data in zip(q2.CALLS, means):
                    radius, status = direct(data, x, threshold, True, weights)
                    points.append(dict(label, coordinate=x, call=call, radius_m=radius,
                                       status=status, leader=leader))
            for (i, j), path in fitted.items():
                events.extend(dict(label, left=q2.CALLS[i], right=q2.CALLS[j], **row)
                              for row in rank_events(means[i], means[j], path, threshold, weights))
            if axis != "spectral":
                continue
            point, nearest = nearest_switch(means, threshold, fitted)
            switches.extend(dict(threshold=threshold, **point, **row) for row in nearest or [{}])
            if point["status"] != "switch":
                continue
            bootstrap = zip(*(metrics[call][1] for call in q2.CALLS))
            for index, data in enumerate(bootstrap, 1):
                data = np.stack(data)
                fit = evaluate(data, threshold, weights)
                info, nearest = nearest_switch(data, threshold, fit)
                leaders = {"leader_" + label: "=".join(leading_calls(data, weights, x, threshold))
                           for label, x in (("zero", 0.), ("equal", .50), ("one", 1.))}
                draws.extend(dict(threshold=threshold, draw=index, **info, **leaders, **row)
                             for row in nearest or [{}])

    draw_table = pd.DataFrame(draws)
    if len(draw_table):
        for threshold, subset in draw_table.groupby("threshold"):
            unique_draws = subset.drop_duplicates("draw")
            for column in ("leader_zero", "leader_equal", "leader_one", "status"):
                for value, count in unique_draws[column].value_counts().items():
                    summaries.append(dict(threshold=threshold, quantity=column, value=value, count=count))
            switched = subset.query("status == 'switch'")
            for (direction, replacement), group in switched.groupby(["direction", "replacement"]):
                summaries.append(dict(threshold=threshold, quantity="switch_direction",
                                      value=f"{direction}:{replacement}", count=group.draw.nunique()))
            for column in ("s", "delta_s", "weight_transferred"):
                values = switched.drop_duplicates("draw")[column] if column != "s" else switched[column]
                low, median, high = values.quantile([.025, .50, .975])
                summaries.append(dict(threshold=threshold, quantity=column, count=len(values),
                                      low95=low, median=median, high95=high))

    tables = dict(radii=pd.DataFrame(points), events=pd.DataFrame(events), slice=pd.DataFrame(switches))
    if len(draw_table):
        tables.update(draws=draw_table, bootstrap=pd.DataFrame(summaries))
    for name, table in tables.items():
        table.to_csv(output / f"q2_spectral_allocation_{name}.csv", index=False, lineterminator="\n")
