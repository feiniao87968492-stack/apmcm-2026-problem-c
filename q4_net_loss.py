"""Compute exact paired-draw boundaries for two hypothetical Q4 losses."""
from pathlib import Path

import numpy as np
import pandas as pd

import q2
from control_subtraction import reference
from q4_envelope_attainment import DISTANCES, DRAWS, REQUIRED
from q4_shape_propagation import acoustic_fidelities, behavior_probabilities

CAP = .20
TOL = 1e-12
PROBE = 1e-8


def count_pass(product, excess, cutoff, a, b, boundary=False):
    score = (1-a) * product * (excess-b*np.maximum(excess, 0.))
    threshold = cutoff * (1-TOL) if boundary else cutoff
    return int(np.count_nonzero(np.all(score >= threshold, axis=1)))


def limits(required):
    """Return allowance by slice and diagonal, capped at the scenario limit."""
    slices = [("max_b", a, 1-required/(1-a)) for a in (0., .10, CAP)]
    slices.extend((("acoustic_extent", 0., 1-required),
                   ("max_a_at_full_b", CAP, 1-required/(1-CAP)),
                   ("diagonal", None, 1-np.sqrt(required))))
    for kind, fixed, value in slices:
        status = "infeasible" if value < 0 else "capped" if value > CAP else "boundary"
        yield kind, fixed, min(value, CAP) if value >= 0 else None, status


def boundaries(label, names, fidelity, excess, cutoff):
    net = fidelity * excess
    needs = np.full_like(net, np.inf)
    np.divide(cutoff, net, out=needs, where=(fidelity > 0) & (excess > 0))
    for name, columns in [(name, [i]) for i, name in enumerate(names)] + [
        ("all_four", list(range(len(names)))),
    ]:
        worst = needs[:, columns].max(axis=1)
        draw_needs = worst[1:]
        required = np.sort(draw_needs)[REQUIRED-1]
        binding = []
        if np.isfinite(required):
            tied_rows = np.isclose(draw_needs, required, atol=0, rtol=TOL)
            binding = [names[col] for col in columns
                       if np.any(np.isclose(needs[1:, col][tied_rows], required, atol=0, rtol=TOL))]
        finite = np.isfinite(draw_needs)
        dominates = [names[col] for col in columns if finite.any()
                     and np.all(needs[1:, col][finite] == draw_needs[finite])]
        selected = fidelity[1:, columns]
        draw_excess, draw_cutoff = excess[1:], cutoff[1:]
        base = dict(label, shape=name, requirement=required, point_requirement=worst[0],
                    binding_shapes=" ".join(binding), dominates_on_finite_draws=" ".join(dominates),
                    infinite_requirements=int((~finite).sum()), draws=DRAWS,
                    point_cutoff=cutoff[0, 0], min_draw_cutoff=draw_cutoff.min(), max_draw_cutoff=draw_cutoff.max())
        checkpoint = {(a, b): count_pass(selected, draw_excess, draw_cutoff, a, b)
                      for a in (0., .10, CAP) for b in (0., .10, CAP)}
        for (a, b), count in checkpoint.items():
            assert count == np.count_nonzero(draw_needs <= (1-a)*(1-b))
        summary = dict(base, clean_count=checkpoint[0., 0.], loss_20_20_count=checkpoint[CAP, CAP])
        rows = []
        for kind, fixed, limit, status in limits(required):
            if limit is None:
                rejected = checkpoint[fixed, 0.] if kind == "max_b" else (
                    checkpoint[0., CAP] if kind == "max_a_at_full_b" else checkpoint[0., 0.])
                assert rejected < REQUIRED
                rows.append(dict(label, shape=name, kind=kind, fixed_loss=fixed,
                                 status=status, count_if_zero=rejected))
                continue
            if kind == "max_b":
                a, b, da, db = fixed, limit, 0., PROBE
            elif kind == "diagonal":
                a, b, da, db = limit, limit, PROBE, PROBE
            else:
                a, b, da, db = limit, fixed, PROBE, 0.
            exact = status == "boundary"
            count = count_pass(selected, draw_excess, draw_cutoff, a, b, boundary=exact)
            assert count >= REQUIRED
            after = None
            if exact and max(a+da, b+db) <= CAP:
                after = count_pass(selected, draw_excess, draw_cutoff, a+da, b+db)
                assert after < REQUIRED
            rows.append(dict(label, shape=name, kind=kind, fixed_loss=fixed, status=status,
                             max_loss=limit, acoustic_loss=a, response_loss=b, count=count,
                             count_beyond=after))
        yield summary, rows, [dict(label, shape=name, acoustic_loss=a, response_loss=b, count=count)
                              for (a, b), count in checkpoint.items()]


def write(data: Path, output: Path, baseline: Path):
    curves = acoustic_fidelities(data)
    names = list(curves)
    tv = q2.CALLS.index("tv")
    summary, frontier, counts = [], [], []
    for model, probabilities in behavior_probabilities(data):
        if model == "full":
            cutoff = reference(curves["isotonic"], probabilities[:, 0]-probabilities[:, 1])[:, None]
            assert np.isfinite(cutoff).all() and np.all(cutoff > 0)
        for distance in (100, 150):
            j = np.searchsorted(DISTANCES, distance)
            fidelity = np.column_stack([curve[:, tv, j] for curve in curves.values()])
            excess = (probabilities[:, 0, tv, j] - probabilities[:, 1, tv, j])[:, None]
            assert np.isfinite(fidelity).all() and np.isfinite(excess).all()
            for row, limits_at_loss, grid in boundaries(dict(model=model, distance_m=distance),
                                                        names, fidelity, excess, cutoff):
                summary.append(row)
                frontier.extend(limits_at_loss)
                counts.extend(grid)
    summary = pd.DataFrame(summary)
    keys = ["model", "distance_m", "shape"]
    archived = pd.read_csv(baseline / "q4_shape_propagation.csv").query("call == 'tv'").set_index(keys)
    for distance, column in ((100, "loss_20_20_count"), (150, "clean_count")):
        check = summary.loc[summary.distance_m.eq(distance) & summary["shape"].ne("all_four")].set_index(keys)
        np.testing.assert_array_equal(check[column], archived.loc[check.index, "count"])
    output.mkdir(parents=True, exist_ok=True)
    for suffix, table in (("requirements", summary), ("boundaries", pd.DataFrame(frontier)),
                          ("counts", pd.DataFrame(counts))):
        table.to_csv(output / f"q4_net_loss_{suffix}.csv", index=False, lineterminator="\n")
