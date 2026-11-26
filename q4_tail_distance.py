"""Audit released tail predictions by actual trial distance."""
from argparse import ArgumentParser
from pathlib import Path

import numpy as np
import pandas as pd

import q3
from distance_deletion_mc import DATE_SEED, PREFIXES
from q4_tail_models import Design, METRICS, validation_folds
from round2 import mask_scores

MODELS = ("A", "B", "C", "E")
BANDS = ("at_least_125", "below_125", "pooled")


def audit(data, archived):
    frame = q3.load_playbacks(data)
    contexts = tuple(sorted(frame.loc[frame.Type.eq("call"), "Context"].unique()))
    design = Design(frame, contexts)
    n_dates = len(np.unique(design.dates))
    draws = np.random.default_rng(DATE_SEED).integers(n_dates, size=(PREFIXES[-1], n_dates))
    counts = np.zeros((len(BANDS), n_dates), dtype=int)
    losses = np.zeros((len(MODELS), len(BANDS), n_dates, len(METRICS[:2])))
    for fold, (_, _, _, _, train, test) in enumerate(validation_folds(design, tail_only=True)):
        training = np.flatnonzero(np.repeat(train, 2))
        testing = np.flatnonzero(np.repeat(test, 2))
        if not len(testing):
            continue
        actual_long = design.distance[testing] >= 125
        bands = (actual_long, ~actual_long, np.ones(len(testing), dtype=bool))
        counts[:, fold] = [band.sum() for band in bands]
        for model_index, model in enumerate(MODELS):
            probabilities, _ = design.predict(model, training, frame.iloc[testing])
            scores = mask_scores(probabilities, design.y[testing])
            losses[model_index, :, fold] = [scores[band].sum(axis=0) for band in bands]

    released = pd.read_csv(archived).query("assessment == 'tail'").set_index("model")
    totals = counts.sum(axis=1)
    means = losses.sum(axis=2) / totals[None, :, None]
    deltas = means - means[:1]
    np.testing.assert_allclose(np.average(deltas[:, :2], axis=1, weights=totals[:2]),
                               deltas[:, 2], atol=1e-12, rtol=0)
    rows = []
    for model_index, model in enumerate(MODELS):
        metrics = list(METRICS[:2])
        delta_columns = [f"{metric}_delta" for metric in metrics]
        np.testing.assert_allclose(means[model_index, 2], released.loc[model, metrics].to_numpy(float),
                                   atol=1e-12, rtol=0)
        np.testing.assert_allclose(deltas[model_index, 2],
                                   released.loc[model, delta_columns].to_numpy(float), atol=1e-12, rtol=0)
        for band_index, band in enumerate(BANDS):
            boot_counts = counts[band_index, draws].sum(axis=1)
            valid = boot_counts > 0
            daily_deltas = losses[model_index, band_index] - losses[0, band_index]
            boot_delta = daily_deltas[draws[valid]].sum(axis=1) / boot_counts[valid, None]
            low, high = np.quantile(boot_delta, [.025, .975], axis=0)
            if band == "pooled":
                for label, limit in (("low95", low), ("high95", high)):
                    columns = [f"{metric}_delta_{label}" for metric in metrics]
                    np.testing.assert_allclose(limit, released.loc[model, columns].to_numpy(float),
                                               atol=1e-12, rtol=0)
            row = dict(model=model, band=band, trials=totals[band_index],
                       dates=np.count_nonzero(counts[band_index]), valid_draws=int(valid.sum()))
            for index, metric in enumerate(metrics):
                row.update({metric: means[model_index, band_index, index],
                            f"{metric}_delta": deltas[model_index, band_index, index],
                            f"{metric}_delta_low95": low[index], f"{metric}_delta_high95": high[index]})
            rows.append(row)

    pair_date = np.repeat(design.dates, 2)
    cover = []
    for arm in q3.STIMULI:
        cell = frame.assigned_call.eq("tv") & frame.Type.eq(arm) & frame.Distance.between(125, 175)
        cover.append(dict(stimulus=arm, trials=int(cell.sum()), dates=len(np.unique(pair_date[cell])),
                          responses=int((cell & frame["mask"].ne(0)).sum()),
                          trials_at_150=int((cell & frame.Distance.eq(150)).sum())))
    return pd.DataFrame(rows), pd.DataFrame(cover)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("results"))
    parser.add_argument("--archived", type=Path, default=Path("results/q4_tail_ablation_validation.csv"))
    args = parser.parse_args()
    scores, coverage = audit(args.data, args.archived)
    args.output.mkdir(parents=True, exist_ok=True)
    for name, table in (("scores", scores), ("coverage", coverage)):
        table.to_csv(args.output / f"q4_tail_distance_{name}.csv", index=False, lineterminator="\n")
