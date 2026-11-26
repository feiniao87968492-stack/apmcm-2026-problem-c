"""Compare five consecutive-distance Q4 radii for two-voice calls."""
from itertools import combinations

import numpy as np
import pandas as pd

import q2
import q3
from control_subtraction import reference
from distance_deletion import pair_filters
from q4_envelope_attainment import DRAWS, REQUIRED
from q4_shape_propagation import acoustic_fidelities, behavior_probabilities

GRID = np.arange(20., 150.5, .5)
SCENARIOS = (("clean", 0.), ("loss_20_20", .20))


def evaluate(model, probabilities, curves, cutoff, retained):
    tv = q2.CALLS.index("tv")
    excess = probabilities[:, 0, tv] - probabilities[:, 1, tv]
    outside = {}
    for arm in q3.STIMULI:
        distances = retained.loc[retained.Type.eq(arm), "Distance"]
        outside[arm] = (GRID < distances.min()) | (GRID > distances.max())
    for scenario, loss in SCENARIOS:
        response = (1-loss) * (excess - loss*np.maximum(excess, 0.))
        margins = {shape: fidelity[:, tv]*response-cutoff[:, None]
                   for shape, fidelity in curves.items()}
        margins["all_four"] = np.minimum.reduce(list(margins.values()))
        marginal, prefix = {}, {}
        label = dict(model=model, scenario=scenario)
        counts = []
        for shape, margin in margins.items():
            assert np.isfinite(margin).all()
            marginal[shape] = (margin[1:] >= 0).sum(axis=0)
            prefix[shape] = (np.minimum.accumulate(margin[1:], axis=1) >= 0).sum(axis=0)
            counts.extend(dict(label, shape=shape, distance_m=distance, point_margin=margin[0, j],
                               marginal_count=marginal[shape][j], prefix_count=prefix[shape][j], draws=DRAWS,
                               outside_natural_range=outside["call"][j], outside_control_range=outside["control"][j])
                          for j, distance in enumerate(GRID))

        shared = marginal["shared_g"]
        rules = {
            "shared_point_last": (margins["shared_g"][0] >= 0, False, None),
            "shared_marginal_last": (shared >= REQUIRED, False, shared),
            "shared_marginal_prefix": (shared >= REQUIRED, True, shared),
            "shared_same_draw_prefix": (prefix["shared_g"] >= REQUIRED, True, prefix["shared_g"]),
            "all_four_same_draw_prefix": (prefix["all_four"] >= REQUIRED, True, prefix["all_four"]),
        }
        radii = []
        for rule, (passes, contiguous, node_counts) in rules.items():
            passing = np.flatnonzero(np.logical_and.accumulate(passes) if contiguous else passes)
            index = passing[-1] if len(passing) else None
            if index is None:
                status = "empty_at_20" if contiguous else "no_passing_node"
            else:
                status = "grid_cap" if index == len(GRID)-1 else "interior"
            radii.append(dict(label, rule=rule, radius_m=None if index is None else GRID[index], status=status,
                              count_at_20=None if node_counts is None else node_counts[0],
                              count_at_radius=None if node_counts is None or index is None else node_counts[index],
                              count_next=None if node_counts is None or index is None or index == len(GRID)-1
                              else node_counts[index+1],
                              radius_outside_natural_range=None if index is None else outside["call"][index],
                              radius_outside_control_range=None if index is None else outside["control"][index]))
        differences = [dict(label, rule=right["rule"], comparator=left["rule"],
                            delta_m=right["radius_m"]-left["radius_m"])
                       for left, right in combinations(radii, 2)
                       if left["radius_m"] is not None and right["radius_m"] is not None]
        yield counts, radii, differences


def write(data, output, baseline):
    frame = q3.load_playbacks(data)
    filters, _ = pair_filters(frame)
    curves = acoustic_fidelities(data, distances=GRID)
    counts, radii, differences, ranges = [], [], [], []
    for model, probabilities in behavior_probabilities(data, distances=GRID):
        if model == "full":
            cutoff = reference(curves["isotonic"], probabilities[:, 0]-probabilities[:, 1])
            assert np.all(np.isfinite(cutoff) & (cutoff > 0))
        retained = frame.loc[filters[model] & frame.assigned_call.eq("tv")]
        for arm, part in retained.groupby("Type"):
            ranges.append(dict(model=model, arm=arm, trials=len(part), min_m=part.Distance.min(),
                               max_m=part.Distance.max()))
        for nodes, summary, delta in evaluate(model, probabilities, curves, cutoff, retained):
            counts.extend(nodes)
            radii.extend(summary)
            differences.extend(delta)

    counts = pd.DataFrame(counts)
    keys = ["model", "distance_m", "shape"]
    old = pd.read_csv(baseline / "q4_net_loss_counts.csv")
    for scenario, distance, loss in (("clean", 150, 0.), ("loss_20_20", 100, .20)):
        published = old.loc[old.acoustic_loss.eq(loss) & old.response_loss.eq(loss)].set_index(keys)
        actual = counts.loc[counts.scenario.eq(scenario) & counts.distance_m.eq(distance)].set_index(keys)
        np.testing.assert_array_equal(actual.marginal_count, published.loc[actual.index, "count"])
    output.mkdir(parents=True, exist_ok=True)
    for name, table in (("counts", counts), ("radii", pd.DataFrame(radii)),
                         ("differences", pd.DataFrame(differences)), ("ranges", pd.DataFrame(ranges))):
        table.to_csv(output / f"q4_consecutive_{name}.csv", index=False, lineterminator="\n")
