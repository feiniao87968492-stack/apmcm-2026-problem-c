"""Compute fixed-distance Q4 decisions along the common envelope-weight path."""
from argparse import ArgumentParser
from pathlib import Path

import numpy as np
import pandas as pd

import q2
import q3
from distance_deletion import pair_filters, refit
from distance_deletion_mc import ACOUSTIC_SEED, CASES, DATE_SEED, PREFIXES
from q2_envelope_rank import START, WEIGHTS, lines, structure

DISTANCES = np.array([20, 100, 150])
DRAWS = PREFIXES[-1]
REQUIRED = 3840
TOL = 1e-12
REFERENCES = ("equal_weight", "weight_specific")
MODELS = ("full", "drop_union")


def fidelity_path(means):
    """Return common segment edges and continuous fidelity at those edges."""
    pieces = [list(structure(lines(m), 0., 1.)) for m in means]
    edges = np.unique(np.concatenate([[0., 1.], *[[p[1] for p in call] for call in pieces]]))
    fidelity = []
    for call in pieces:
        ends = np.array([p[1] for p in call])
        coefficients = np.stack([p[2] for p in call])[np.searchsorted(ends, edges)]
        knots = coefficients[..., 0] + edges[:, None] * coefficients[..., 1]
        fidelity.append([q2.interpolated(DISTANCES, values) for values in knots])
    return edges, np.stack(fidelity, axis=1)


def regions(edges, selected_edges, selected_gaps):
    """Merge selected points and adjacent open intervals into closed components."""
    indices = np.flatnonzero(selected_edges)
    if not len(indices):
        return []
    cut = np.flatnonzero((np.diff(indices) != 1) | ~selected_gaps[indices[:-1]]) + 1
    return [(edges[group[0]], edges[group[-1]]) for group in np.split(indices, cut)]


def margin_regions(edges, values, zero=False):
    values = np.where(np.abs(values) <= TOL, 0., values)
    changes = np.flatnonzero(values[1:] * values[:-1] < 0)
    roots = edges[changes] - values[changes] * np.diff(edges)[changes] / np.diff(values)[changes]
    coordinates = np.r_[edges, roots]
    values = np.r_[values, np.zeros(len(roots))]
    order = np.argsort(coordinates)
    coordinates, values = coordinates[order], values[order]
    chosen = values == 0 if zero else values >= 0
    return regions(coordinates, chosen, chosen[1:] & chosen[:-1])


def attainment(intervals):
    """Count closed-interval membership at endpoints and in open gaps."""
    bounds = np.asarray([(0., 0.), (1., 1.), *intervals])
    values, inverse = np.unique(bounds.ravel(), return_inverse=True)
    groups = np.cumsum(np.r_[True, np.diff(values) > TOL]) - 1
    edges = values[np.r_[True, np.diff(groups) != 0]]
    edges[-1] = 1.
    starts, ends = groups[inverse].reshape(-1, 2)[2:].T
    starts = np.bincount(starts, minlength=len(edges))
    ends = np.bincount(ends, minlength=len(edges))
    after = np.cumsum(starts - ends)
    at = after + ends
    above = regions(edges, at >= REQUIRED, after[:-1] >= REQUIRED)
    index = {value: i for i, value in enumerate(edges)}
    for lo, hi in above:
        i, j = index[lo], index[hi]
        yield dict(weight_low=lo, weight_high=hi, count_low=at[i], count_high=at[j],
                   count_before=after[i-1] if i else None,
                   count_after=after[j] if j < len(edges)-1 else None)


def evidence(data, baseline):
    tables = q2.load_tables(data)
    rng = np.random.default_rng(ACOUSTIC_SEED)
    acoustics = np.stack([
        np.concatenate((np.nanmean(table, axis=1)[None], q2.bootstrap_means(table, DRAWS, rng)))
        for table in tables.values()
    ], axis=1)
    frame = q3.load_playbacks(data)
    weights = frame.loc[frame.Type.eq("call"), "Context"].value_counts(normalize=True).sort_index()
    n_dates = frame.Date.nunique()
    sampled = np.random.default_rng(DATE_SEED).integers(n_dates, size=(DRAWS, n_dates))
    filters, _ = pair_filters(frame)
    behavior = []
    for model in MODELS:
        point, draws = refit(frame, filters[model], sampled, weights, distances=DISTANCES)
        behavior.append(np.concatenate((point[None], draws)))
    natural, control = np.stack(behavior, axis=1).transpose(2, 0, 1, 3, 4)
    excess = natural - control
    coefficients = np.empty((DRAWS+1, len(MODELS), len(CASES)))
    reference = np.empty((DRAWS+1, len(CASES), len(q2.CALLS)))
    targets = []
    for k, (call, distance, link, definition) in enumerate(CASES):
        i, j = q2.CALLS.index(call), np.searchsorted(DISTANCES, distance)
        targets.append((i, j))
        response = natural if definition == "gross" else excess
        reference[:, k] = response[:, 0, :, 0] / 6
        factor = np.where(excess[:, :, i, j] > 0, .8**2, .8) if link == "coupled" else 1.
        coefficients[:, :, k] = response[:, :, i, j] * factor
    assert np.isfinite(coefficients).all() and np.isfinite(reference).all()

    labels = [dict(model=model, call=call, distance_m=distance, link=link,
                   definition=definition, reference=rule)
              for model in MODELS for call, distance, link, definition in CASES for rule in REFERENCES]
    values = np.empty((DRAWS + 1, len(labels), len(WEIGHTS)))
    point_regions, draw_intervals = [], [[] for _ in labels]
    for index, means in enumerate(acoustics):
        edges, fidelity = fidelity_path(means)
        target_fidelity = np.column_stack([fidelity[:, i, j] for i, j in targets])
        scores = coefficients[index][None] * target_fidelity[:, None, :]
        cutoff = fidelity[:, :, 0] @ reference[index].T
        fixed = np.array([np.interp(START, edges, c) for c in cutoff.T])
        margins = np.stack((scores-fixed, scores-cutoff[:, None, :]), axis=-1)
        for k, (margin, label) in enumerate(zip(margins.reshape(len(edges), -1).T, labels)):
            values[index, k] = np.interp(WEIGHTS, edges, margin)
            parts = margin_regions(edges, margin, zero=index == 0)
            if index:
                draw_intervals[k].extend(parts)
            else:
                point_regions.extend(dict(label, weight_low=a, weight_high=b) for a, b in parts)

    archived_points = pd.read_csv(baseline / "distance_deletion_points.csv")
    archived_counts = pd.read_csv(baseline / "distance_deletion_mc.csv").query(
        "source == 'fresh' and requested_draws == @DRAWS"
    )
    keys = ["model", "call", "distance_m", "link", "definition"]
    archived_points = archived_points.set_index(keys).margin
    archived_counts = archived_counts.set_index(keys)["count"]
    checkpoints, boundaries = [], []
    for label, case, intervals in zip(labels, values.transpose(1, 0, 2), draw_intervals):
        key = tuple(label[name] for name in keys)
        old_margin, old_count = archived_points.loc[key], archived_counts.loc[key]
        rows = list(attainment(intervals))
        boundaries.extend(dict(label, status="qualifying", **row) for row in rows)
        if not rows:
            boundaries.append(dict(label, status="empty"))
        for weight, column in zip(WEIGHTS, case.T):
            lower, upper = np.quantile(column[1:], [.025, .975])
            count = int(np.count_nonzero(column[1:] >= -TOL))
            assert (count >= REQUIRED) == any(row["weight_low"]-TOL <= weight <= row["weight_high"]+TOL
                                              for row in rows)
            checkpoints.append(dict(label, weight=weight, margin=column[0], low95=lower,
                                    high95=upper, count=count, draws=DRAWS, support=count/DRAWS,
                                    archived_margin=old_margin, archived_count=old_count,
                                    delta_margin=column[0]-old_margin, delta_count=count-old_count))
    return {"points": pd.DataFrame(checkpoints), "zeros": pd.DataFrame(point_regions),
            "intervals": pd.DataFrame(boundaries)}


def write(data, output, baseline):
    tables = evidence(data, baseline)
    output.mkdir(parents=True, exist_ok=True)
    for name, table in tables.items():
        table.to_csv(output / f"q4_envelope_attainment_{name}.csv", index=False, lineterminator="\n")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True, type=Path)
    parser.add_argument("--output", default=Path("results"), type=Path)
    parser.add_argument("--baseline", default=Path("results"), type=Path)
    args = parser.parse_args()
    write(args.data, args.output, args.baseline)
