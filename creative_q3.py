"""Grouped evaluation of structured eight-mask playback models."""
from itertools import combinations

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import logsumexp, softmax
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler

import q3
from post_hoc import smoothed_masks
from final_analysis import two_stage
from round2 import interval, mask_scores, playback_matrices, score_frame


BEHAVIOR_PAIRS = tuple(combinations(range(len(q3.BEHAVIORS)), 2))
PAIR_BITS = np.column_stack([q3.BITS[:, i] * q3.BITS[:, j] for i, j in BEHAVIOR_PAIRS])
BASELINES = ("stimulus_frequency", "full_multinomial", "two_stage")
CANDIDATES = ("interaction_free", "pairwise")
METRICS = ("mask_log_loss", "any_response_brier")


def fit_structured(train_x, train_y, evaluation_x, interactions):
    """Fit an L2 mask softmax with shared pairwise terms."""
    scale = StandardScaler().fit(train_x)
    x = np.column_stack((np.ones(len(train_x)), scale.transform(train_x)))
    n_behavior_terms = x.shape[1] * q3.BITS.shape[1]
    pair_bits = PAIR_BITS if interactions else PAIR_BITS[:, :0]
    observed = (np.arange(len(train_y)), train_y)

    def unpack(parameters):
        return parameters[:n_behavior_terms].reshape(x.shape[1], -1), parameters[n_behavior_terms:]

    def loss_gradient(parameters):
        beta, pair = unpack(parameters)
        logits = (x @ beta) @ q3.BITS.T + pair_bits @ pair
        normalizer = logsumexp(logits, axis=1)
        loss = (normalizer - logits[observed]).sum() + .5 * (parameters @ parameters)
        residual = np.exp(logits - normalizer[:, None])
        residual[observed] -= 1
        gradient = np.r_[(x.T @ (residual @ q3.BITS)).ravel(),
                         residual.sum(axis=0) @ pair_bits]
        return loss, gradient + parameters

    initial = np.zeros(n_behavior_terms + pair_bits.shape[1])
    fitted = minimize(loss_gradient, initial, method="L-BFGS-B", jac=True,
                      options={"maxiter": 1000, "gtol": 1e-7, "ftol": 1e-12})
    if not fitted.success:
        raise RuntimeError(f"Structured mask fit failed: {fitted.message}")
    beta, pair = unpack(fitted.x)
    if evaluation_x is None:
        return pair
    evaluation = np.column_stack((np.ones(len(evaluation_x)), scale.transform(evaluation_x)))
    return softmax((evaluation @ beta) @ q3.BITS.T + pair_bits @ pair, axis=1)


def evaluate(frame, design, seed, n_boot, output):
    names = (*BASELINES, *CANDIDATES)
    y = frame["mask"].to_numpy()
    stimulus = frame.Type.to_numpy()
    folds = list(GroupKFold(5).split(frame, groups=frame.expID))
    oof = np.empty((len(y), len(q3.MASKS), len(names)))
    for train, test in folds:
        train_x, train_y, test_x = design[train], y[train], design[test]
        frequency = np.empty((len(test), len(q3.MASKS)))
        for label in q3.STIMULI:
            observed = train_y[stimulus[train] == label]
            frequency[stimulus[test] == label] = (
                np.bincount(observed, minlength=len(q3.MASKS)) / len(observed)
            )
        oof[test] = np.stack((
            frequency,
            q3.fit_masks(train_x, train_y, test_x),
            two_stage(train_x, train_y, test_x),
            fit_structured(train_x, train_y, test_x, interactions=False),
            fit_structured(train_x, train_y, test_x, interactions=True),
        ), axis=-1)

    smoothed_masks(frame, folds, oof, names, output, seed, n_boot)
    scores = np.stack([mask_scores(oof[:, :, i], y) for i in range(len(names))], axis=-1)
    scores = score_frame(frame, folds, scores, METRICS, names)
    fold_scores = scores.groupby(level="fold").mean()
    fold_scores.stack(level="model", future_stack=True).reset_index().to_csv(
        output / "creative_q3_fold_scores.csv", index=False,
    )
    probability_rows = []
    for i, name in enumerate(names):
        block = pd.DataFrame(oof[:, :, i], columns=[f"p{mask}" for mask in q3.MASKS])
        block.index = scores.index
        probability_rows.append(block.assign(model=name, stimulus=stimulus, observed_mask=y))
    pd.concat(probability_rows).reset_index().to_csv(output / "creative_q3_oof.csv", index=False)

    resampler = np.random.default_rng(seed)
    draws = []
    pair_scores = scores.groupby(level=["fold", "pair"]).mean()
    for _, fold in pair_scores.groupby(level="fold"):
        indices = resampler.integers(len(fold), size=(n_boot, len(fold)))
        draws.append(fold.to_numpy()[indices].mean(axis=1))
    draw_scores = pd.DataFrame(np.mean(draws, axis=0), columns=scores.columns)
    mean_scores = fold_scores.mean()
    contrasts = [(baseline, candidate) for candidate in CANDIDATES for baseline in BASELINES]
    contrasts.append(("interaction_free", "pairwise"))
    records = []
    for baseline, candidate in contrasts:
        rows = []
        for metric in METRICS:
            old, new = (metric, baseline), (metric, candidate)
            low, high = interval(draw_scores[new] - draw_scores[old])
            rows.append({
                "baseline": baseline, "candidate": candidate, "metric": metric,
                "baseline_score": mean_scores[old], "candidate_score": mean_scores[new],
                "difference": mean_scores[new] - mean_scores[old],
                "difference_low": low, "difference_high": high,
            })
        joint_gain = all(row["difference_high"] < 0 for row in rows)
        records.extend({**row, "joint_gain": joint_gain} for row in rows)

    comparison = pd.DataFrame(records)
    required = comparison.candidate.eq("pairwise") & comparison.baseline.ne("two_stage")
    comparison["adopt_pairwise"] = bool(comparison.loc[required, "joint_gain"].all())
    comparison.to_csv(output / "creative_q3_comparison.csv", index=False)


def report_interactions(frame, design, seed, n_boot, output):
    y = frame["mask"].to_numpy()
    point = fit_structured(design, y, None, interactions=True)
    resampler = np.random.default_rng(seed)
    n_pairs = frame.expID.nunique()
    pairs = np.arange(len(frame)).reshape(n_pairs, 2)
    drawn_pairs = resampler.integers(n_pairs, size=(n_boot, n_pairs))
    draws = []
    for pair_indices in drawn_pairs:
        rows = pairs[pair_indices].ravel()
        draws.append(fit_structured(design[rows], y[rows], None, interactions=True))
    low, high = interval(draws)
    pd.DataFrame({
        "behavior_1": [q3.BEHAVIORS[i] for i, _ in BEHAVIOR_PAIRS],
        "behavior_2": [q3.BEHAVIORS[j] for _, j in BEHAVIOR_PAIRS],
        "log_odds_ratio": point, "log_odds_ratio_low": low, "log_odds_ratio_high": high,
    }).to_csv(output / "creative_q3_interactions.csv", index=False)


def run(data, output, seed, n_boot):
    frame = q3.load_playbacks(data)
    design = playback_matrices(frame)["add_context_group"]
    evaluate(frame, design, seed + 2, n_boot, output)
    report_interactions(frame, design, seed + 2, n_boot, output)
