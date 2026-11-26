"""Invert consecutive-distance Q4 attainment for hypothetical losses."""
import numpy as np
import pandas as pd

import q2
from control_subtraction import reference
from q4_consecutive import GRID
from q4_envelope_attainment import DRAWS, REQUIRED
from q4_net_loss import CAP, PROBE, TOL, limits
from q4_shape_propagation import acoustic_fidelities, behavior_probabilities

RULES = {
    "all_four_endpoint": ("all_four", "marginal_count"),
    "shared_prefix": ("shared_g", "prefix_count"),
    "all_four_prefix": ("all_four", "prefix_count"),
}


def requirements(score, cutoff):
    result = np.full_like(score, np.inf)
    np.divide(cutoff[:, None], score, out=result, where=score > 0)
    return result


def direct_count(score, cutoff, a, b, boundary=False):
    adjusted = (1-a) * (score - b*np.maximum(score, 0.))
    return int(np.count_nonzero(adjusted >= cutoff * (1-TOL if boundary else 1.)))


def boundary_rows(label, required, score, cutoff):
    for kind, fixed, limit, status in limits(required):
        row = dict(label, kind=kind, fixed_loss=fixed, status=status, max_loss=limit)
        if limit is None:
            a = fixed if kind == "max_b" else 0.
            b = fixed if kind == "max_a_at_full_b" else 0.
            row["count_if_zero"] = direct_count(score, cutoff, a, b)
            assert row["count_if_zero"] < REQUIRED
        else:
            if kind == "max_b":
                a, b, da, db = fixed, limit, 0., PROBE
            elif kind == "diagonal":
                a, b, da, db = limit, limit, PROBE, PROBE
            else:
                a, b, da, db = limit, fixed, PROBE, 0.
            count = direct_count(score, cutoff, a, b, boundary=status == "boundary")
            assert count >= REQUIRED
            row.update(acoustic_loss=a, response_loss=b, count=count)
            if status == "boundary" and max(a+da, b+db) <= CAP:
                row["count_beyond"] = direct_count(score, cutoff, a+da, b+db)
                assert row["count_beyond"] < REQUIRED
        yield row


def write(data, output, baseline):
    curves = acoustic_fidelities(data, distances=GRID)
    old = pd.read_csv(baseline / "q4_consecutive_counts.csv").set_index(
        ["model", "scenario", "shape", "distance_m"]
    ).sort_index()
    tv = q2.CALLS.index("tv")
    grid_rows, boundaries, radii = [], [], []
    for model, probabilities in behavior_probabilities(data, distances=GRID):
        excess = probabilities[:, 0] - probabilities[:, 1]
        if model == "full":
            cutoff = reference(curves["isotonic"], excess)
            assert np.all(np.isfinite(cutoff) & (cutoff > 0))
        scores = {shape: curve[:, tv] * excess[:, tv] for shape, curve in curves.items()}
        joint = np.minimum.reduce(list(scores.values()))
        by_rule = (joint, np.minimum.accumulate(scores["shared_g"], axis=1),
                   np.minimum.accumulate(joint, axis=1))
        for (rule, (shape, count_field)), score in zip(RULES.items(), by_rule):
            assert np.isfinite(score).all()
            required = requirements(score, cutoff)
            draw_requirements = required[1:]
            order_statistic = np.partition(draw_requirements, REQUIRED-1, axis=0)[REQUIRED-1]
            matches = {}
            for scenario, loss in (("clean", 0.), ("loss_20_20", CAP)):
                retention = (1-loss)**2
                count = (draw_requirements <= retention).sum(axis=0)
                old_count = old.loc[(model, scenario, shape)]
                np.testing.assert_array_equal(count, old_count[count_field].to_numpy())
                passes = np.flatnonzero(order_statistic <= retention)
                radii.append(dict(model=model, rule=rule, scenario=scenario,
                                  radius_m=GRID[passes[-1]] if len(passes) else None,
                                  status=("no_passing_node" if rule == "all_four_endpoint" else "empty_at_20")
                                  if not len(passes) else "grid_cap" if passes[-1] == len(GRID)-1 else "interior",
                                  count_at_radius=count[passes[-1]] if len(passes) else None))
                matches[scenario] = count
            flags = old.loc[(model, "clean", shape)]
            for j, distance in enumerate(GRID):
                label = dict(model=model, rule=rule, distance_m=distance,
                             requirement=order_statistic[j], point_requirement=required[0, j],
                             clean_count=matches["clean"][j], loss_20_20_count=matches["loss_20_20"][j],
                             draws=DRAWS)
                for arm in ("natural", "control"):
                    outside = flags[f"outside_{arm}_range"].to_numpy()
                    label[f"target_outside_{arm}_range"] = outside[j]
                    label[f"prefix_outside_{arm}_range"] = outside[:j+1].any()
                grid_rows.append(label)
                if distance in (50, 100, 150):
                    boundaries.extend(boundary_rows(label, order_statistic[j], score[1:, j], cutoff[1:]))

    output.mkdir(parents=True, exist_ok=True)
    for suffix, rows in (("grid", grid_rows), ("boundaries", boundaries), ("radii", radii)):
        pd.DataFrame(rows).to_csv(output / f"q4_target_loss_{suffix}.csv", index=False, lineterminator="\n")
