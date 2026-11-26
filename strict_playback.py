"""Validate playback on unseen dates and tracks and resample both clusters."""
import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar

import q3
from creative_q3 import fit_structured
from playback_dependence import margin_table
from round2 import mask_scores


def joint_table(p, q, log_odds):
    """Four cells in 00, 01, 10, 11 order, preserving the two margins."""
    lower, upper = np.maximum(0., p + q - 1), np.minimum(p, q)
    odds = np.exp(log_odds)
    # Solve the monotone odds-ratio equation over the feasible interval.
    for _ in range(52):
        middle = (lower + upper) / 2
        residual = middle * (1 - p - q + middle) - odds * (p - middle) * (q - middle)
        lower, upper = np.where(residual < 0, middle, lower), np.where(residual >= 0, middle, upper)
    both = (lower + upper) / 2
    return np.maximum(0, np.column_stack((1 - p - q + both, q - both, p - both, both)))


def pair_loss(probabilities, y):
    return -np.log(np.maximum(probabilities[np.arange(len(y)), y], 1e-12))


def validate(frame, date, track, design, output, seed, n_boot):
    y = frame["mask"].to_numpy().reshape(-1, 2)
    x = design.reshape(len(y), 2, -1)
    states = (y > 0) @ np.array([2, 1])
    masks, pairs, coverage, losses = [], [], [], []
    for fold, held_date in enumerate(sorted(set(date)), 1):
        test = date == held_date
        excluded_tracks = np.unique(track[test])
        train = ~test & ~np.isin(track, excluded_tracks)
        train_y, test_y = y[train], y[test]
        train_x, test_x = x[train].reshape(-1, x.shape[-1]), x[test].reshape(-1, x.shape[-1])
        frequencies = np.stack([(np.bincount(train_y[:, i], minlength=8) + .5) / (len(train_y) + 4)
                                for i in range(2)])
        full = q3.fit_masks(train_x, train_y.ravel(), test_x)
        candidates = {
            "smoothed_stimulus": np.tile(frequencies, (len(test_y), 1)),
            "full_multinomial": full,
            "pairwise_mask": fit_structured(train_x, train_y.ravel(), test_x, interactions=True),
        }
        coverage.append({
            "fold": fold, "date": held_date, "train_pairs": train.sum(), "test_pairs": test.sum(),
            "purged_pairs": (~test & ~train).sum(), "held_tracks": len(excluded_tracks),
            "unseen_mask_trials": (~np.isin(test_y, train_y)).sum(),
            "unseen_stimulus_mask_trials": sum((~np.isin(test_y[:, i], train_y[:, i])).sum() for i in range(2)),
        })
        for name, probabilities in candidates.items():
            loss, brier = mask_scores(probabilities, test_y.ravel()).mean(axis=0)
            masks.append({"fold": fold, "model": name, "test_trials": test_y.size,
                          "mask_log_loss": loss, "any_response_brier": brier})

        train_p = (1 - q3.fit_masks(train_x, train_y.ravel(), train_x)[:, 0]).reshape(-1, 2)
        fitted = minimize_scalar(
            lambda eta: pair_loss(joint_table(*train_p.T, eta), states[train]).sum() + eta**2 / 2,
            bounds=(-8, 8), method="bounded", options={"xatol": 1e-9},
        )
        if not fitted.success:
            raise RuntimeError(f"Pair odds-ratio fit failed on fold {fold}")
        test_p = (1 - full[:, 0]).reshape(-1, 2)
        brier = np.mean((test_p - (test_y > 0))**2)
        independent = pair_loss(joint_table(*test_p.T, 0), states[test])
        dependent = pair_loss(joint_table(*test_p.T, fitted.x), states[test])
        losses.append(dependent - independent)
        for name, score, eta in (("independent", independent, 0.), ("shared_odds_ratio", dependent, fitted.x)):
            pairs.append({"fold": fold, "model": name, "test_pairs": test.sum(), "log_odds_ratio": eta,
                          "pair_log_loss": score.mean(), "marginal_brier": brier})
    tables = {"coverage": coverage, "mask_folds": masks, "pair_folds": pairs}
    for name, rows in tables.items():
        pd.DataFrame(rows).to_csv(output / f"strict_q3_{name}.csv", index=False)

    records = []
    for name, rows, count, metrics in (
        ("mask", masks, "test_trials", ("mask_log_loss", "any_response_brier")),
        ("pair", pairs, "test_pairs", ("pair_log_loss", "marginal_brier")),
    ):
        for model, group in pd.DataFrame(rows).groupby("model", sort=False):
            records.append({"comparison": name, "model": model, "n": group[count].sum(),
                            **{k: np.average(group[k], weights=group[count]) for k in metrics}})
    sizes = np.array([len(v) for v in losses])
    indices = np.random.default_rng(seed).integers(len(losses), size=(n_boot, len(losses)))
    differences = np.array([v.sum() for v in losses])[indices].sum(axis=1) / sizes[indices].sum(axis=1)
    low, high = np.quantile(differences, [.025, .975])
    pd.DataFrame(records).to_csv(output / "strict_q3_scores.csv", index=False)
    pd.DataFrame([{"difference": np.concatenate(losses).mean(), "low": low, "high": high,
                   "adopt_dependency": high < 0}]).to_csv(output / "strict_q3_pair_contrast.csv", index=False)


def crossed(frame, date, track, design, contexts, weights, propagation, seed, n_boot, output):
    n_dates, n_tracks = date.max() + 1, track.max() + 1
    date_rng, track_rng = np.random.default_rng(seed), np.random.default_rng(seed + 1)
    distance = propagation["distance"]
    grid_x = q3.features(q3.probability_grid(distance, contexts, 8), contexts)
    y = frame["mask"].to_numpy()
    shape = (2, 3, len(distance), len(contexts))
    estimates, coverage = [], []
    redraws = 0
    while len(estimates) < n_boot:
        n_date = date_rng.multinomial(n_dates, np.full(n_dates, 1 / n_dates))
        n_track = track_rng.multinomial(n_tracks, np.full(n_tracks, 1 / n_tracks))
        multiplicity = n_date[date] * n_track[track]
        if not multiplicity.any():
            redraws += 1
            continue
        rows = np.repeat(np.arange(len(frame)), np.repeat(multiplicity, 2))
        p = 1 - q3.fit_masks(design[rows], y[rows], grid_x)[:, 0]
        estimates.append(p.reshape(shape) @ weights)
        included = multiplicity > 0
        coverage.append({"draw": len(estimates), "weighted_pairs": multiplicity.sum(),
                         "unique_pairs": included.sum(), "unique_dates": len(np.unique(date[included])),
                         "unique_tracks": len(np.unique(track[included])), "empty_attempts_so_far": redraws})
    pd.DataFrame(coverage).to_csv(output / "strict_q4_crossed_coverage.csv", index=False)
    return np.asarray(estimates)


def run(frame, propagation, behavior, date_predictions, output, seed, n_boot):
    natural = frame.loc[frame.Type.eq("call")]
    dates = natural.Date.to_numpy()
    tracks = natural.PlaybackTrack.to_numpy()
    counts = natural.Context.value_counts(normalize=True).sort_index()
    contexts = tuple(counts.index)
    design = q3.features(frame, contexts)
    validate(frame, dates, tracks, design, output, seed + 2, n_boot)
    _, dates = np.unique(dates, return_inverse=True)
    _, tracks = np.unique(tracks, return_inverse=True)
    draws = crossed(frame, dates, tracks, design, contexts, counts.to_numpy(), propagation,
                    seed + 2, n_boot, output)
    margin_table(propagation, behavior, date_predictions, draws).to_csv(
        output / "strict_q4_margins.csv", index=False,
    )
