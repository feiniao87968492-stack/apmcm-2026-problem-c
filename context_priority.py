"""Compare supported-area ranks across context mixes and behavior priorities."""
from itertools import combinations, permutations

import numpy as np
import pandas as pd

import noise_scenarios
import q3
from spatial_annulus import average, limits


def area_scores(masks, fidelity, distance):
    marginals = np.concatenate(((1 - masks[..., :1]), masks @ q3.BITS), axis=-1)
    weighted = marginals * fidelity[..., None, None]
    return average(np.moveaxis(weighted, -3, -1), distance, area=True)


def comparison(rows, gaps, db, context, event, point, draws, baseline, base_draws):
    fields = dict(db=db, context=context, event=event)
    for i, call in enumerate(q3.CALLS):
        rows.append(dict(fields, call=call, score=point[i], **limits(draws[:, i], "score"),
                         rank=1 + (point > point[i]).sum(),
                         delta_vs_empirical_any=point[i]-baseline[i],
                         **limits(draws[:, i]-base_draws[:, i], "delta")))
    for i, j in combinations(range(len(q3.CALLS)), 2):
        gap = draws[:, i] - draws[:, j]
        gaps.append(dict(fields, first=q3.CALLS[i], second=q3.CALLS[j],
                         gap=point[i]-point[j], **limits(gap, "gap")))


def vertex_bounds(db, point, draws, contexts):
    vertices = [(context, event) for context in contexts for event in q3.BEHAVIORS]
    rows = []
    for i, j in permutations(range(len(q3.CALLS)), 2):
        gaps = (point[i, :, 1:] - point[j, :, 1:]).ravel()
        paired = (draws[:, i, :, 1:] - draws[:, j, :, 1:]).reshape(len(draws), -1)
        minimum, maximum = gaps.min(), gaps.max()
        row = dict(db=db, first=q3.CALLS[i], second=q3.CALLS[j])
        for name, endpoint, samples in (
            ("minimum", minimum, paired.min(axis=1)), ("maximum", maximum, paired.max(axis=1)),
        ):
            attained = [f"{context}/{event}" for gap, (context, event) in zip(gaps, vertices)
                        if gap == endpoint]
            row.update({name: endpoint, f"{name}_vertices": "|".join(attained),
                        **limits(samples, name)})
        row["robust"] = row["minimum_low95"] > 0
        rows.append(row)
    return rows


def coverage(natural, contexts, weights):
    rows = []
    supported = natural.Distance.between(20, 150)
    for call in q3.CALLS:
        for context, weight in zip(contexts, weights):
            cell = natural.loc[natural.assigned_call.eq(call) & natural.Context.eq(context) & supported]
            for distance in (None, *q3.REPRESENTATIVE):
                part = cell if distance is None else cell.loc[cell.Distance.sub(distance).abs().le(25)]
                rows.append(dict(call=call, context=context, distance_m=distance,
                                 empirical_weight=weight, trials=len(part), dates=part.Date.nunique(),
                                 any_response=part.ResponseYesNo.sum(),
                                 **{event: part[f"{event}YesNo"].sum() for event in q3.BEHAVIORS}))
    return rows


def run(frame, distance, parameters, sampled_parameters, point_masks, date_masks, output):
    natural = frame.loc[frame.Type.eq("call")]
    proportions = natural.Context.value_counts(normalize=True).sort_index()
    contexts, weights = tuple(proportions.index), proportions.to_numpy()
    rows, gaps, bounds = [], [], []
    for db in (0, 6):
        fidelity = noise_scenarios.fidelity(distance, parameters, db)
        sampled = noise_scenarios.fidelity(distance, sampled_parameters, db)
        point = area_scores(point_masks, fidelity, distance)
        draws = area_scores(date_masks, sampled, distance)
        pooled = np.einsum("cje,j->ce", point, weights)
        pooled_draws = np.einsum("bcje,j->bce", draws, weights)
        for i, context in enumerate((*contexts, "empirical")):
            scores = pooled if context == "empirical" else point[:, i]
            samples = pooled_draws if context == "empirical" else draws[:, :, i]
            for j, event in enumerate(("any", *q3.BEHAVIORS)):
                comparison(rows, gaps, db, context, event, scores[:, j], samples[:, :, j],
                           pooled[:, 0], pooled_draws[:, :, 0])
        bounds.extend(vertex_bounds(db, point, draws, contexts))
    for name, records in (("scores", rows), ("gaps", gaps), ("bounds", bounds),
                          ("coverage", coverage(natural, contexts, weights))):
        pd.DataFrame(records).to_csv(output / f"context_priority_{name}.csv", index=False)
