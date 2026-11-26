"""Audit Monte Carlo precision of three distance-deletion decisions."""
from argparse import ArgumentParser
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binomtest

import physical_attenuation as attenuation
import q2
import q3
from control_subtraction import reference, score_curves
from distance_deletion import pair_filters, refit

ACOUSTIC_SEED = 20261130
DATE_SEED = 20261201
PREFIXES = (300, 1200, 4800)
CASES = (("tv", 150, "clean", "net_own"),
         ("tv", 100, "coupled", "net_own"),
         ("mod", 100, "clean", "gross"))


def acoustics(data, distances):
    tables = q2.load_tables(data)
    rng = np.random.default_rng(ACOUSTIC_SEED)
    means = [q2.bootstrap_means(tables[call], PREFIXES[-1], rng) for call in q2.CALLS]
    reference_fidelity, score_fidelity = [], []
    for sample in zip(*means):
        knots = [q2.fit_knots(m, q2.WEIGHTS["equal"]) for m in sample]
        reference_fidelity.append([q2.interpolated(distances[:1], k) for k in knots])
        parameters = attenuation.fit(q2.KNOTS, np.stack([attenuation.equal_means(m) for m in sample]),
                                     shared=True)
        score_fidelity.append(attenuation.curve(distances, parameters))
    return np.stack(reference_fidelity), np.stack(score_fidelity)


def summary(count, valid, requested, source):
    interval = binomtest(count, valid).proportion_ci(confidence_level=.95, method="exact")
    status = "above" if interval.low > .80 else "below" if interval.high < .80 else "unresolved"
    return dict(source=source, requested_draws=requested, valid_draws=valid, count=count,
                support=count/valid, low95=interval.low, high95=interval.high,
                point_passes_80=5*count >= 4*valid, mc_status=status)


def run(data, archived, output):
    distances = np.array([20, 100, 150])
    frame = q3.load_playbacks(data)
    weights = frame.loc[frame.Type.eq("call"), "Context"].value_counts(normalize=True).sort_index()
    dates = frame.Date.nunique()
    sampled = np.random.default_rng(DATE_SEED).integers(dates, size=(PREFIXES[-1], dates))
    filters, _ = pair_filters(frame)
    iso, fidelity = acoustics(data, distances)
    baseline = pd.read_csv(archived).set_index(["model", "call", "distance_m", "link", "definition"])
    rows = []
    for model, eligible in filters.items():
        _, draws = refit(frame, eligible, sampled, weights, distances=distances)
        valid_draws = np.isfinite(draws).all(axis=(1, 2, 3))
        if model == "full":
            cutoffs = {
                "gross": reference(iso, draws[:, 0]),
                "net_own": reference(iso, draws[:, 0] - draws[:, 1]),
            }
        for call, distance, link, definition in CASES:
            loss = .20 if link == "coupled" else 0.
            i, j = q2.CALLS.index(call), np.searchsorted(distances, distance)
            gross, net = score_curves(fidelity[:, i, j], draws[:, 0, i, j],
                                      draws[:, 1, i, j], loss, link == "coupled")
            score = gross if definition == "gross" else net
            cutoff = cutoffs[definition]
            valid = valid_draws & np.isfinite(cutoff)
            qualifies = (score >= cutoff) & valid
            key = (model, call, distance, link, definition)
            labels = dict(zip(baseline.index.names, key))
            old = baseline.loc[key]
            rows.append(dict(labels, **summary(int(old["count"]), int(old["draws"]), 300, "archived")))
            for prefix in PREFIXES:
                rows.append(dict(labels, **summary(int(qualifies[:prefix].sum()),
                                                   int(valid[:prefix].sum()), prefix, "fresh")))
    output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output, index=False)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True, help="Contest attachment CSV directory")
    parser.add_argument("--archived", type=Path, default=Path("results/distance_deletion_points.csv"))
    parser.add_argument("--output", type=Path, default=Path("results/distance_deletion_mc.csv"))
    args = parser.parse_args()
    run(args.data, args.archived, args.output)


if __name__ == "__main__":
    main()
