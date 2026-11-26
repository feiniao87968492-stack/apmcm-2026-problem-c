"""Frozen playback models and whole-date, track-purged validation."""
import warnings

import numpy as np
import pandas as pd
from scipy.optimize import minimize, minimize_scalar
from scipy.special import expit
from sklearn.exceptions import ConvergenceWarning
from sklearn.preprocessing import StandardScaler

import q3
from round2 import mask_scores
from strict_playback import joint_table, pair_loss


MODELS = ("A", "B", "C", "D", "E")
METRICS = ("mask_log_loss", "any_response_brier", "pair_log_loss")


def fit_pair_eta(train_probabilities, train_masks):
    arms = (1 - train_probabilities[:, 0]).reshape(-1, 2)
    states = (np.asarray(train_masks).reshape(-1, 2) > 0) @ np.array([2, 1])
    fit = minimize_scalar(
        lambda eta: pair_loss(joint_table(*arms.T, eta), states).sum() + eta**2 / 2,
        method="bounded", bounds=(-8, 8), options={"xatol": 1e-9},
    )
    if not fit.success or not np.isfinite(fit.fun):
        raise RuntimeError(f"Joint odds-ratio optimization failed: {fit.message}")
    return fit.x


class Design:
    """Cache the released covariates and intact pair identifiers."""

    def __init__(self, frame, contexts):
        self.frame = frame.reset_index(drop=True)
        self.contexts = tuple(contexts)
        self.x = q3.features(self.frame, self.contexts)
        # The final two released columns are distance and group size.
        self.nondistance = np.r_[np.arange(self.x.shape[1] - 2), self.x.shape[1] - 1]
        self.y = self.frame["mask"].to_numpy()
        self.distance = self.frame.Distance.to_numpy(dtype=float)
        self.call = pd.Categorical(self.frame.assigned_call, categories=q3.CALLS).codes
        self.arm = pd.Categorical(self.frame.Type, categories=q3.STIMULI).codes
        pair_ids = self.frame.expID.to_numpy().reshape(-1, 2)
        if not (np.all(pair_ids[:, 0] == pair_ids[:, 1])
                and np.all(self.arm.reshape(-1, 2) == [0, 1])):
            raise ValueError("Expected adjacent natural/control rows per playback pair.")
        natural = self.frame.iloc[::2]
        self.dates = natural.Date.to_numpy()
        self.tracks = natural.PlaybackTrack.to_numpy()
        self.tail = np.any(self.distance.reshape(-1, 2) >= 125, axis=1)
        self.support_pairs = np.all(
            ((self.distance >= 20) & (self.distance < 125)).reshape(-1, 2), axis=1,
        )

    def fit_rows(self, model, rows):
        if model == "E":
            rows = rows[np.repeat(self.support_pairs[rows[::2] // 2], 2)]
        return rows

    def bounded_distances(self, rows, distance, call, arm):
        evaluated = distance.copy()
        train_distance = self.distance[rows]
        train_arm = self.arm[rows]
        train_call = self.call[rows]
        for stimulus in range(len(q3.STIMULI)):
            observed_arm = train_distance[train_arm == stimulus]
            arm_support = observed_arm if len(observed_arm) else train_distance
            for assigned_call in range(len(q3.CALLS)):
                cell = (arm == stimulus) & (call == assigned_call)
                observed_cell = train_distance[(train_arm == stimulus) & (train_call == assigned_call)]
                support = observed_cell if len(observed_cell) else arm_support
                evaluated[cell] = np.clip(distance[cell], support.min(), support.max())
        return evaluated

    def predict(self, model, rows, evaluation, joint=False):
        rows = self.fit_rows(model, np.asarray(rows))
        if not len(rows):
            raise RuntimeError("No eligible training pairs.")
        y = self.y[rows]
        evaluation_x = q3.features(evaluation, self.contexts)
        if model in ("A", "D"):
            train_x = self.x[rows]
            targets = np.vstack((evaluation_x, train_x)) if model == "D" and joint else evaluation_x
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("error", ConvergenceWarning)
                    probabilities = q3.fit_masks(train_x, y, targets)
            except ConvergenceWarning as exc:
                raise RuntimeError("Multinomial fit did not converge.") from exc
            stop = len(evaluation)
            eta = fit_pair_eta(probabilities[stop:], y) if model == "D" and joint else 0.
            return probabilities[:stop], eta

        distance = evaluation.Distance.to_numpy(dtype=float)
        call = pd.Categorical(evaluation.assigned_call, categories=q3.CALLS).codes
        arm = pd.Categorical(evaluation.Type, categories=q3.STIMULI).codes
        if model == "E":
            distance = self.bounded_distances(rows, distance, call, arm)

        response = y != 0
        if response.all() or not response.any():
            p = np.full(len(evaluation), (response.sum() + .5) / (len(y) + 1))
        else:
            scale = StandardScaler().fit(self.x[rows][:, self.nondistance])
            train = self.hurdle_design(self.x[rows], self.distance[rows], self.call[rows], model, scale)
            target = self.hurdle_design(evaluation_x, distance, call, model, scale)
            slopes = len(q3.CALLS) if model == "C" else 1

            def objective(beta):
                logit = train @ beta
                error = expit(logit) - response
                penalty = np.r_[0., beta[1:]]
                value = (np.logaddexp(0, logit) - response * logit).sum() + .5 * (penalty @ penalty)
                return value, train.T @ error + penalty

            fit = minimize(
                objective, np.zeros(train.shape[1]), jac=True, method="L-BFGS-B",
                bounds=[(None, None)] * (train.shape[1] - slopes) + [(None, 0.)] * slopes,
                options={"maxiter": 500, "ftol": 1e-12, "gtol": 1e-7},
            )
            if not fit.success or not np.isfinite(fit.fun):
                raise RuntimeError(f"Hurdle fit failed: {fit.message}")
            p = expit(target @ fit.x)

        counts = np.stack([
            np.bincount(y[self.arm[rows] == stimulus], minlength=8)[1:] + .5
            for stimulus in range(len(q3.STIMULI))
        ])
        composition = counts / counts.sum(axis=1, keepdims=True)
        return np.column_stack((1 - p, p[:, None] * composition[arm])), 0.

    def hurdle_design(self, x, distance, call, model, scale):
        t = np.log2((1 + distance) / 21)
        slopes = t[:, None]
        if model == "C":
            slopes = slopes * (call[:, None] == np.arange(len(q3.CALLS)))
        return np.column_stack((np.ones(len(x)), scale.transform(x[:, self.nondistance]), slopes))


def validation_folds(design, tail_only):
    for date in np.unique(design.dates):
        held = design.dates == date
        tracks = np.unique(design.tracks[held])
        purged = ~held & np.isin(design.tracks, tracks)
        train = ~held & ~purged
        if tail_only:
            train &= ~design.tail
        test = held & design.tail if tail_only else held
        yield date, held, tracks, purged, train, test


def validate(design, sampled_dates):
    """Compute pooled held-out scores and paired whole-date intervals."""
    dates = np.unique(design.dates)
    folds, summaries = [], []
    for assessment in ("ordinary", "tail"):
        totals = np.zeros((len(MODELS), len(dates), len(METRICS)))
        counts = np.zeros((len(MODELS), len(dates)), dtype=int)
        failed = np.zeros_like(counts, dtype=bool)
        empty = np.zeros(len(dates), dtype=bool)
        folds_for_assessment = validation_folds(design, tail_only=assessment == "tail")
        for fold, (date, held, tracks, purged, train, test) in enumerate(folds_for_assessment):
            rows = np.flatnonzero(np.repeat(train, 2))
            test_rows = np.flatnonzero(np.repeat(test, 2))
            test_y = design.y[test_rows]
            states = (test_y.reshape(-1, 2) > 0) @ np.array([2, 1])
            empty[fold] = not test.any()
            test_frame = design.frame.iloc[test_rows]
            for i, model in enumerate(MODELS):
                used = design.fit_rows(model, rows)
                used_pairs = used[::2] // 2
                means, eta, error = np.full(len(METRICS), np.nan), np.nan, ""
                if not empty[fold]:
                    try:
                        masks, eta = design.predict(model, rows, test_frame, joint=True)
                    except RuntimeError as exc:
                        failed[i, fold] = True
                        error = str(exc)
                    else:
                        p = (1 - masks[:, 0]).reshape(-1, 2)
                        joint = joint_table(*p.T, eta)
                        scores = np.column_stack((
                            mask_scores(masks, test_y).reshape(-1, 2, 2).mean(axis=1),
                            pair_loss(joint, states),
                        ))
                        totals[i, fold] = scores.sum(axis=0)
                        counts[i, fold] = len(scores)
                        means = scores.mean(axis=0)
                overlap_date = int(np.count_nonzero(held[used_pairs]))
                overlap_track = int(np.count_nonzero(np.isin(design.tracks[used_pairs], tracks)))
                assert overlap_date == overlap_track == 0
                folds.append(dict(
                    model=model, assessment=assessment, fold=fold + 1, date=date,
                    train_pairs=len(used_pairs), test_pairs=int(test.sum()), test_trials=len(test_rows),
                    purged_pairs=int(purged.sum()), held_tracks=len(tracks),
                    train_held_date_pairs=overlap_date, train_held_track_pairs=overlap_track,
                    failed=failed[i, fold], empty_test=empty[fold], fit_error=error, eta=eta,
                    **dict(zip(METRICS, means)),
                ))

        for i, model in enumerate(MODELS):
            n = int(counts[i].sum())
            common = (counts[i] > 0) & (counts[0] > 0)
            denominator = np.where(common, counts[i], 0)
            differences = np.where(common[:, None], totals[i] - totals[0], 0.)
            sampled_count = denominator[sampled_dates].sum(axis=1)
            valid = sampled_count > 0
            means = totals[i].sum(axis=0) / n if n else np.full(len(METRICS), np.nan)
            paired = differences.sum(axis=0) / denominator.sum() if common.any() else np.full(len(METRICS), np.nan)
            bounds = np.full((2, len(METRICS)), np.nan)
            if valid.any():
                sampled_difference = differences[sampled_dates[valid]].sum(axis=1)
                bounds = np.quantile(sampled_difference / sampled_count[valid, None], [.025, .975], axis=0)
            summary = dict(
                model=model, assessment=assessment, scored_pairs=n, scored_trials=2 * n,
                common_scored_pairs=int(denominator.sum()), failed_folds=int(failed[i].sum()),
                empty_test_folds=int(empty.sum()),
                worse_marginal_folds=int(np.count_nonzero(common & (differences[:, :2] > 0).any(axis=1))),
                valid_bootstrap_draws=int(valid.sum()),
            )
            for j, metric in enumerate(METRICS):
                summary.update({
                    metric: means[j], f"{metric}_delta": paired[j],
                    f"{metric}_delta_low95": bounds[0, j], f"{metric}_delta_high95": bounds[1, j],
                })
            summaries.append(summary)

    summary = pd.DataFrame(summaries)
    summary["validation_eligible"] = False
    for model in MODELS:
        scores = summary.loc[summary.model.eq(model)].set_index("assessment")
        ordinary, tail = scores.loc["ordinary"], scores.loc["tail"]
        eligible = (
            model != "A" and scores.failed_folds.sum() == 0
            and ordinary.mask_log_loss_delta_high95 < 0 and ordinary.any_response_brier_delta_high95 < 0
            and tail.mask_log_loss_delta < 0 and tail.any_response_brier_delta < 0
            and tail.mask_log_loss_delta_high95 < 0
        )
        summary.loc[summary.model.eq(model), "validation_eligible"] = bool(eligible)
    return {"folds": pd.DataFrame(folds), "validation": summary}
