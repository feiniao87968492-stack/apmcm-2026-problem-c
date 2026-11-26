"""Follow Q2 radius ranks along the common envelope-weight path."""
from itertools import combinations

import numpy as np
import pandas as pd
from scipy.optimize import isotonic_regression

import q2
from continuous_recovery import adjacent_blocks

TOL = 1e-10
START = 1 / 3
WEIGHTS = (0., .10, START, .50, 1.)
LOG_KNOTS = np.log2(q2.KNOTS)


def block_contrasts(size):
    rows = []
    for start, split, stop in adjacent_blocks(size):
        contrast = np.zeros(size)
        contrast[start:split] = 1 / (split - start)
        contrast[split:stop] = -1 / (stop - split)
        rows.append(contrast)
    return np.asarray(rows)


ADJACENT = block_contrasts(len(LOG_KNOTS))


def partitions(values, low, high):
    edges = np.sort(np.r_[low, np.asarray(values).ravel(), high])
    return np.r_[low, edges[1:-1][(np.diff(edges)[:-1] > TOL) & (edges[1:-1] < high - TOL)], high]


def affine_roots(affine, low, high):
    affine = affine.reshape(-1, 2)
    offset, slope = affine[affine[:, 1] != 0].T
    roots = -offset / slope
    return roots[(roots > low + TOL) & (roots < high - TOL)]


def lines(means):
    spectral = means[:2].mean(axis=0)
    return np.column_stack((spectral, means[2] - spectral))


def at(affine, e):
    return affine[:, 0] + e * affine[:, 1]


def structure(affine, low, high):
    clips = partitions(np.r_[affine_roots(affine, low, high),
                             affine_roots(affine - [1, 0], low, high)], low, high)
    for lo, hi in zip(clips[:-1], clips[1:]):
        y = at(affine, (lo + hi) / 2)
        clipped = affine.copy()
        clipped[y <= 0] = (0, 0)
        clipped[y >= 1] = (1, 0)
        edges = partitions(affine_roots(ADJACENT @ clipped, lo, hi), lo, hi)
        for a, b in zip(edges[:-1], edges[1:]):
            blocks = isotonic_regression(at(clipped, (a + b) / 2), increasing=False).blocks
            fitted = clipped.copy()
            for start, stop in zip(blocks[:-1], blocks[1:]):
                fitted[start:stop] = clipped[start:stop].mean(axis=0)
            yield a, b, fitted


def radius_functions(pieces, threshold):
    for low, high, fitted in pieces:
        edges = partitions(affine_roots(fitted - [threshold, 0], low, high), low, high)
        for a, b in zip(edges[:-1], edges[1:]):
            good = np.flatnonzero(at(fitted, (a + b) / 2) >= threshold)
            if not len(good) or good[-1] == len(LOG_KNOTS) - 1:
                bound = LOG_KNOTS[-1] if len(good) else LOG_KNOTS[0]
                yield a, b, np.array([bound, 0.]), np.array([1., 0.])
                continue
            j = good[-1]
            denominator = fitted[j] - fitted[j+1]
            numerator = LOG_KNOTS[j] * denominator + fitted[j] - [threshold, 0]
            yield a, b, numerator, denominator


def direct(means, e, threshold, snap=False):
    knots = q2.fit_knots(means, ((1-e)/2, (1-e)/2, e))
    if snap:
        knots[np.abs(knots-threshold) <= 1e-13] = threshold
    return q2.radius(knots, threshold)


def state(left, right, e, threshold, snap=False):
    left_radius, _ = direct(left, e, threshold, snap)
    right_radius, _ = direct(right, e, threshold, snap)
    gap = np.log2(left_radius / right_radius)
    return int(np.sign(gap)) if abs(gap) > TOL else 0


def pair_path(left, right, left_pieces, right_pieces, threshold):
    low, high = left_pieces[0][0], left_pieces[-1][1]
    left_edges = [p[0] for p in left_pieces]
    right_edges = [p[0] for p in right_pieces]
    edges = partitions(left_edges[1:] + right_edges[1:], low, high)
    roots = []
    for a, b in zip(edges[:-1], edges[1:]):
        mid = (a + b) / 2
        _, _, ln, ld = left_pieces[np.searchsorted(left_edges, mid, side="right") - 1]
        _, _, rn, rd = right_pieces[np.searchsorted(right_edges, mid, side="right") - 1]
        # Change variables to the local interval u in [0,1].
        ln, ld, rn, rd = [np.array([v[0] + a*v[1], (b-a)*v[1]]) for v in (ln, ld, rn, rd)]
        coefficients = np.convolve(ln, rd) - np.convolve(rn, ld)
        scale = max(np.max(np.abs(np.convolve(ln, rd))), np.max(np.abs(np.convolve(rn, ld))))
        if np.max(np.abs(coefficients)) <= 1e-13 * scale:
            continue
        for root in np.polynomial.polynomial.polyroots(coefficients):
            if abs(root.imag) <= TOL and 0 < root.real < 1:
                roots.append(a + (b-a) * root.real)
    edges = partitions(np.r_[edges[1:-1], roots], low, high)
    on_edges = [state(left, right, e, threshold, snap=True) for e in edges]
    interiors = [state(left, right, (a+b)/2, threshold) for a, b in zip(edges[:-1], edges[1:])]
    return edges, on_edges, interiors


def rank_events(left, right, path, threshold):
    edges, on, interior = path
    for i, (e, at_e) in enumerate(zip(edges, on)):
        before = interior[i-1] if i else None
        after = interior[i] if i < len(interior) else None
        if before is None or after is None:
            if at_e and at_e == (after if before is None else before):
                continue
        elif before == at_e == after:
            continue
        l_radius, l_status = direct(left, e, threshold, snap=True)
        r_radius, r_status = direct(right, e, threshold, snap=True)
        yield dict(weight=e, before=before, at=at_e, after=after, radius_left=l_radius,
                   radius_right=r_radius, status_left=l_status, status_right=r_status)


def first_lead(left, right):
    cutoff = .70
    pieces = [list(radius_functions(list(structure(lines(m), START, 1.)), cutoff))
              for m in (left, right)]
    edges, on, interior = pair_path(left, right, *pieces, cutoff)
    if on[0] > 0:
        return "already_reversed", START
    for i, e in enumerate(edges):
        if on[i] > 0 or (i < len(interior) and interior[i] > 0):
            return "observed", e
    return "right_censored", np.nan


def run(metrics, output):
    means = {call: metrics[call][0] for call in q2.CALLS}
    structures = {call: list(structure(lines(values), 0., 1.)) for call, values in means.items()}
    comparisons, events = [], []
    for threshold in q2.THRESHOLDS:
        curves = {call: list(radius_functions(pieces, threshold)) for call, pieces in structures.items()}
        for e in WEIGHTS:
            for call in q2.CALLS:
                radius, status = direct(means[call], e, threshold, snap=True)
                comparisons.append(dict(threshold=threshold, weight=e, call=call, radius_m=radius, status=status))
        for left, right in combinations(q2.CALLS, 2):
            path = pair_path(means[left], means[right], curves[left], curves[right], threshold)
            events.extend(dict(threshold=threshold, left=left, right=right, **event)
                          for event in rank_events(means[left], means[right], path, threshold))
    draws = pd.DataFrame((dict(draw=i, status=status, first_weight=weight)
                          for i, (status, weight) in enumerate(
                              (first_lead(l, r) for l, r in zip(metrics["mod"][1], metrics["tv"][1])), 1)))
    observed = draws.loc[draws.status.eq("observed"), "first_weight"]
    low, median, high = np.quantile(observed, [.025, .50, .975]) if len(observed) else [np.nan]*3
    summary = pd.DataFrame([dict(draws=len(draws), already_reversed=draws.status.eq("already_reversed").sum(),
                                 observed=len(observed), right_censored=draws.status.eq("right_censored").sum(),
                                 low95=low, median=median, high95=high)])
    for name, table in (("radii", pd.DataFrame(comparisons)), ("events", pd.DataFrame(events)),
                        ("draws", draws), ("bootstrap", summary)):
        table.to_csv(output / f"q2_envelope_rank_{name}.csv", index=False, lineterminator="\n")
