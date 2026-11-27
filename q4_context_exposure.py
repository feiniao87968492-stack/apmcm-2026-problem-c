"""Compare uniform and extremal context allocations of noisy opportunities."""
from fractions import Fraction

import numpy as np
import pandas as pd

import q2
import q3
from control_subtraction import reference
from distance_deletion import pair_filters
from q4_envelope_attainment import DRAWS, REQUIRED
from q4_intermittent_noise import EXCESS_POWER, DISTANCES, LEVELS
from q4_shape_propagation import acoustic_fidelities, behavior_probabilities


CONTEXTS = ("after", "commuting", "searching")
WEIGHTS = tuple(Fraction(n, 139) for n in (36, 65, 38))
RULES = ("uniform", "minimum", "maximum")


def pass_counts(score, cutoff, squared_ratio):
    noisy = score * np.where(score > 0, squared_ratio, np.sqrt(squared_ratio))
    return tuple(int((state >= cutoff).all(axis=1).sum()) for state in (score, noisy))


def allocate(fraction, rule, losses):
    if rule == "uniform":
        return tuple(fraction * weight for weight in WEIGHTS)
    order = sorted(range(len(WEIGHTS)), key=lambda i: -losses[i] if rule == "minimum" else losses[i])
    allocation = [Fraction(0)] * len(WEIGHTS)
    for i in order:
        allocation[i] = min(fraction, WEIGHTS[i])
        fraction -= allocation[i]
    return allocation


def compare(model, counts):
    clean = sum(weight * pair[0] for weight, pair in zip(WEIGHTS, counts))
    losses = [a - b for a, b in counts]
    assert all(loss >= 0 for loss in losses)

    def result(fraction, rule):
        allocation = allocate(fraction, rule, losses)
        value = clean - sum(x * loss for x, loss in zip(allocation, losses))
        return value, {f"f_{context}": float(x / weight)
                       for context, x, weight in zip(CONTEXTS, allocation, WEIGHTS)}

    for rule in RULES:
        checks = []
        for f in LEVELS:
            value, shares = result(Fraction(f), rule)
            checks.append(dict(model=model, rule=rule, f=f, expected_count=float(value),
                               share=float(value / DRAWS), passes_80=value >= REQUIRED, **shares))

        if clean < REQUIRED:
            yield checks, dict(model=model, rule=rule, status="infeasible")
            continue
        if result(Fraction(1), rule)[0] >= REQUIRED:
            maximum, status = Fraction(1), "cap"
        else:
            order = sorted(range(len(WEIGHTS)),
                           key=lambda i: -losses[i] if rule == "minimum" else losses[i])
            breaks = [Fraction(0), Fraction(1)]
            if rule != "uniform":
                breaks[1:1] = [WEIGHTS[order[0]], WEIGHTS[order[0]] + WEIGHTS[order[1]]]
            for left, right in zip(breaks, breaks[1:]):
                low, high = result(left, rule)[0], result(right, rule)[0]
                if high < REQUIRED:
                    maximum = left + (right-left) * (low-REQUIRED) / (low-high)
                    break
            status = "boundary"
        value, shares = result(maximum, rule)
        yield checks, dict(model=model, rule=rule, status=status, max_f=float(maximum),
                           max_f_exact=str(maximum), expected_count=float(value),
                           share=float(value/DRAWS), **shares)


def coverage(frame, eligible, model):
    selected = frame.loc[eligible & frame.assigned_call.eq("tv")]
    for context in CONTEXTS:
        for arm in q3.STIMULI:
            part = selected.loc[selected.Context.eq(context) & selected.Type.eq(arm)]
            for window, lower, upper in (("prefix", 20, 100), ("near_100", 75, 125)):
                local = part.loc[part.Distance.between(lower, upper)]
                yield dict(model=model, context=context, arm=arm, window=window,
                           trials=len(local), responses=int(local.ResponseYesNo.sum()),
                           observed_min_m=part.Distance.min(), observed_max_m=part.Distance.max())


def write(data, output, archive):
    frame = q3.load_playbacks(data)
    counts_by_context = frame.loc[frame.Type.eq("call"), "Context"].value_counts().reindex(CONTEXTS)
    assert tuple(counts_by_context) == (36, 65, 38)
    weights = np.array(WEIGHTS, dtype=float)
    filters, _ = pair_filters(frame)
    curves, shared = acoustic_fidelities(data, distances=DISTANCES, include_shared=True)
    tv = q2.CALLS.index("tv")
    _, scale, exponent = shared[1:, tv].T
    u = (DISTANCES / scale[:, None])**exponent[:, None]
    squared_ratio = (1 + u) / (1 + (1 + EXCESS_POWER)*u)
    weakest = np.minimum.reduce([curve[1:, tv] for curve in curves.values()])
    prior = pd.read_csv(archive / "q4_intermittent_noise_checks.csv").query(
        "rule == 'state_indicators' and f in [0, 1]"
    ).set_index(["model", "f"]).count_or_expected
    counts, checks, limits, support = [], [], [], []
    for model, probabilities in behavior_probabilities(data, distances=DISTANCES, context_specific=True):
        standardized = probabilities @ weights
        if model == "full":
            cutoff = reference(curves["isotonic"], standardized[:, 0] - standardized[:, 1])[1:, None]
            assert np.all(np.isfinite(cutoff) & (cutoff > 0))
        excess = probabilities[1:, 0, tv] - probabilities[1:, 1, tv]
        old = pass_counts(weakest * (standardized[1:, 0, tv] - standardized[1:, 1, tv]),
                          cutoff, squared_ratio)
        assert old == tuple(prior.loc[model, f] for f in (0., 1.))
        state = [pass_counts(weakest * excess[:, :, i], cutoff, squared_ratio)
                 for i in range(len(CONTEXTS))]
        for context, weight, (clean, noisy) in zip(CONTEXTS, WEIGHTS, state):
            counts.append(dict(model=model, context=context, weight=float(weight),
                               clean_count=clean, noisy_count=noisy, A0=clean/DRAWS, A6=noisy/DRAWS))
        counts.append(dict(model=model, context="standardized_archive_check", weight=1.,
                           clean_count=old[0], noisy_count=old[1], A0=old[0]/DRAWS, A6=old[1]/DRAWS))
        for rows, limit in compare(model, state):
            checks.extend(rows)
            limits.append(limit)
        support.extend(coverage(frame, filters[model], model))
    output.mkdir(parents=True, exist_ok=True)
    for name, rows in (("counts", counts), ("checks", checks), ("limits", limits), ("support", support)):
        pd.DataFrame(rows).to_csv(output / f"q4_context_exposure_{name}.csv",
                                  index=False, lineterminator="\n")
