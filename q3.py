"""Paired playback responses, behavioral combinations, and conditional latency."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.special import ndtr
from scipy.stats import binomtest
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler


CALLS = ("flat", "mod", "tv")
STIMULI = ("call", "control")
BEHAVIORS = ("HeadsUp", "Vocal", "Approach")
INTENSITY = ("HeadsUpDuration", "VocalNcalls", "ApproachDuration")
MASKS = np.arange(8)
BITS = ((MASKS[:, None] >> np.arange(3)) & 1)
MASK_LABELS = ("None", "Head", "Vocal", "Head + vocal", "Approach",
               "Head + approach", "Vocal + approach", "All three")
COLORS = ("#285478", "#BA572C", "#3C785E")
REPRESENTATIVE = (50, 100, 150)


def load_playbacks(data: Path) -> pd.DataFrame:
    """Attach the natural call assigned to each experiment to both stimulus rows."""
    path, = sorted(data.glob("Data02*.csv"))
    frame = pd.read_csv(path).sort_values(["expID", "Type"]).reset_index(drop=True)
    pairs = frame.groupby(["expID", "Type"]).size().unstack(fill_value=0)
    if set(pairs.columns) != set(STIMULI) or not pairs.eq(1).all().all():
        raise ValueError("Each experiment must contain one call and one control stimulus.")
    calls = frame.loc[frame["Type"].eq("call")].set_index("expID")["CallType"]
    frame["assigned_call"] = frame["expID"].map(calls)
    if not set(frame["assigned_call"]).issubset(CALLS):
        raise ValueError("Unexpected natural call type.")
    values = frame[[name + "YesNo" for name in BEHAVIORS]].to_numpy()
    if not np.isin(values, [0, 1]).all():
        raise ValueError("Behavior indicators must be binary.")
    frame["mask"] = values @ np.array([1, 2, 4])
    if not np.array_equal(frame["mask"].ne(0), frame["ResponseYesNo"].eq(1)):
        raise ValueError("Overall response differs from the union of the behavior flags.")
    return frame


def features(frame: pd.DataFrame, contexts: tuple[str, ...]) -> np.ndarray:
    natural = frame["Type"].eq("call").to_numpy()
    call_terms = [frame["assigned_call"].eq(call).to_numpy() for call in CALLS[1:]]
    context_terms = [frame["Context"].eq(context).to_numpy() for context in contexts[1:]]
    return np.column_stack([
        natural, *call_terms, *(natural & term for term in call_terms), *context_terms,
        np.log1p(frame["Distance"]), np.log1p(frame["Npenguins"]),
    ])


def fit_masks(x: np.ndarray, y: np.ndarray, evaluation: np.ndarray) -> np.ndarray:
    """Fit multinomial ridge logistic regression and align the eight mask columns."""
    labels = np.unique(y)
    predictions = np.zeros((len(evaluation), len(MASKS)))
    if len(labels) == 1:
        predictions[:, labels[0]] = 1
        return predictions
    scale = StandardScaler().fit(x)
    model = LogisticRegression(C=1, max_iter=1000).fit(scale.transform(x), y)
    predictions[:, model.classes_] = model.predict_proba(scale.transform(evaluation))
    return predictions


def paired_summary(frame: pd.DataFrame, samples: np.ndarray, output: Path) -> None:
    natural = frame.iloc[::2]["mask"].ne(0).to_numpy()
    control = frame.iloc[1::2]["mask"].ne(0).to_numpy()
    differences = natural.astype(int) - control
    natural_only = int(np.sum(differences == 1))
    control_only = int(np.sum(differences == -1))
    low, high = np.quantile(differences[samples].mean(axis=1), [0.025, 0.975])
    pd.DataFrame([{
        "pairs": len(natural), "natural_responses": natural.sum(),
        "control_responses": control.sum(), "both_responses": np.sum(natural & control),
        "neither_response": np.sum(~natural & ~control), "natural_only": natural_only,
        "control_only": control_only, "natural_rate": natural.mean(),
        "control_rate": control.mean(), "raw_paired_difference": differences.mean(),
        "bootstrap_lower": low, "bootstrap_upper": high,
        "mcnemar_exact_p": binomtest(natural_only, natural_only + control_only).pvalue
        if natural_only + control_only else 1.0,
    }]).to_csv(output / "q3_paired_response.csv", index=False)


def grouped_validation(x: np.ndarray, frame: pd.DataFrame, output: Path) -> None:
    y = frame["mask"].to_numpy()
    stimuli = frame["Type"].to_numpy()
    folds = GroupKFold(n_splits=5)
    records, oof_scores = [], []
    for fold, (train, test) in enumerate(folds.split(x, y, frame["expID"]), start=1):
        pooled = np.bincount(y[train], minlength=len(MASKS))[None, :] / len(train)
        stratified = np.zeros((len(test), len(MASKS)))
        for stimulus in STIMULI:
            training_masks = y[train[stimuli[train] == stimulus]]
            frequencies = np.bincount(training_masks, minlength=len(MASKS))
            stratified[stimuli[test] == stimulus] = frequencies / len(training_masks)
        variants = {
            "multinomial": fit_masks(x[train], y[train], x[test]),
            "pooled_frequency": np.broadcast_to(pooled, (len(test), len(MASKS))),
            "stimulus_frequency": stratified,
        }
        pair_numbers, test_experiments = pd.factorize(frame.iloc[test]["expID"])
        scores = {}
        for name, probabilities in variants.items():
            observed_probability = probabilities[np.arange(len(test)), y[test]]
            row_scores = pd.DataFrame({
                "pair_in_fold": pair_numbers + 1,
                "mask_log_loss": -np.log(observed_probability.clip(1e-12)),
                "any_response_brier": (1 - probabilities[:, 0] - (y[test] != 0)) ** 2,
            })
            pair_scores = row_scores.groupby("pair_in_fold", as_index=False).mean()
            oof_scores.append(pair_scores.assign(fold=fold, model=name))
            scores[name] = row_scores[["mask_log_loss", "any_response_brier"]].mean()
        for name, score in scores.items():
            difference = score - scores["stimulus_frequency"]
            records.append({
                "fold": fold, "model": name, "test_experiments": len(test_experiments),
                "mask_log_loss": score["mask_log_loss"],
                "any_response_brier": score["any_response_brier"],
                "mask_log_loss_minus_stimulus": difference["mask_log_loss"],
                "any_response_brier_minus_stimulus": difference["any_response_brier"],
            })
    pd.DataFrame(records).to_csv(output / "q3_grouped_validation.csv", index=False)
    columns = ["fold", "pair_in_fold", "model", "mask_log_loss", "any_response_brier"]
    pd.concat(oof_scores, ignore_index=True)[columns].to_csv(
        output / "q3_validation_oof_scores.csv", index=False,
    )


def probability_grid(distances: np.ndarray, contexts: tuple[str, ...], size: float) -> pd.DataFrame:
    grid = pd.MultiIndex.from_product(
        [STIMULI, CALLS, distances, contexts],
        names=["Type", "assigned_call", "Distance", "Context"],
    ).to_frame(index=False)
    return grid.assign(Npenguins=size)


def response_figures(
    summary: pd.DataFrame, mask_summary: pd.DataFrame, output: Path, draws: int,
) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(9, 3.1), sharey=True, layout="constrained")
    for axis, call, color in zip(axes, CALLS, COLORS):
        for stimulus, name, style in zip(STIMULI, ("Natural", "Control"), ("-", "--")):
            part = summary.loc[summary["call_type"].eq(call) & summary["stimulus"].eq(stimulus)]
            axis.plot(part["distance_m"], part["probability"], color=color, ls=style, label=name)
            if stimulus == "call":
                axis.fill_between(part["distance_m"], part["lower"], part["upper"], color=color, alpha=.18)
        axis.set(title=call, xlabel="Distance (m)", ylim=(0, 1))
        axis.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("Probability of any response")
    axes[-1].legend(loc="upper right", frameon=False)
    save_figure(fig, summary, output, "q3_response_curve", {
        "source": "Data02", "group_size": 8, "interval": "pointwise 95% paired bootstrap",
        "draws": draws, "context": "empirical experiment distribution",
    })

    at_100 = mask_summary.loc[mask_summary["distance_m"].eq(100)].copy()
    fig, axis = plt.subplots(figsize=(8.1, 3.5), layout="constrained")
    values = at_100["probability"].to_numpy().reshape(6, 8)
    image = axis.imshow(values, vmin=0, vmax=1, cmap="Blues", aspect="auto")
    for row, col in np.ndindex(values.shape):
        axis.text(col, row, f"{values[row, col]:.2f}", ha="center", va="center",
                  color="white" if values[row, col] > .5 else "#192d3d", fontsize=8)
    axis.set_xticks(MASKS, MASK_LABELS, rotation=30, ha="right")
    axis.set_yticks(range(6), [f"{call} | {stimulus}" for stimulus in STIMULI for call in CALLS])
    fig.colorbar(image, ax=axis, label="Predicted probability")
    save_figure(fig, at_100, output, "q3_behavior_masks", {
        "source": "Data02", "distance_m": 100, "group_size": 8,
        "context": "empirical experiment distribution",
        "mask_bit_order": list(BEHAVIORS),
    })


def save_figure(
    figure: plt.Figure, values: pd.DataFrame, output: Path, stem: str, metadata: dict,
) -> None:
    values.to_csv(output / f"{stem}.csv", index=False)
    (output / f"{stem}.meta.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    figure.savefig(output / f"{stem}.png", dpi=300)
    plt.close(figure)


def latency_predictions(
    frame: pd.DataFrame, x: np.ndarray, grid: pd.DataFrame, grid_x: np.ndarray,
    probabilities: np.ndarray, context_weights: np.ndarray, output: Path,
) -> None:
    # Each vector indexes the fixed eight-mask prediction in a common orientation.
    event_probabilities = probabilities @ BITS
    records, intensities = [], []
    for index, (behavior, intensity) in enumerate(zip(BEHAVIORS, INTENSITY)):
        onset = behavior + "Latency"
        events = frame[behavior + "YesNo"].eq(1)
        valid = events & frame[onset].notna()
        observed = frame.loc[valid, onset].to_numpy()
        if np.any(observed < 0):
            raise ValueError(f"Negative observed latency in {onset}.")
        scaler = StandardScaler().fit(x[valid])
        observed_x = scaler.transform(x[valid])
        log_onset = np.log1p(observed)
        model = Ridge(alpha=5.0).fit(observed_x, log_onset)
        log_center = model.predict(scaler.transform(grid_x))
        sigma = max(float(np.std(log_onset - model.predict(observed_x), ddof=1)), 1e-8)
        for stimulus in STIMULI:
            for call in CALLS:
                stratum = frame["Type"].eq(stimulus) & frame["assigned_call"].eq(call)
                latency_count = int((stratum & valid).sum())
                intensities.append({
                    "behavior": behavior, "intensity": intensity, "stimulus": stimulus,
                    "call_type": call, "stimuli": int(stratum.sum()), "response_events": latency_count,
                    "mean_over_stimuli": frame.loc[stratum, intensity].mean(),
                    "median_among_responses": frame.loc[stratum & valid, intensity].median()
                    if latency_count else np.nan,
                })
                for distance in REPRESENTATIVE:
                    positions = grid["Type"].eq(stimulus) & grid["assigned_call"].eq(call) & grid["Distance"].eq(distance)
                    probability = event_probabilities[positions, index]
                    event_weights = context_weights * probability
                    conditional_median = np.nan
                    if latency_count and event_weights.sum() > 0:
                        centers = log_center[positions]
                        weights = event_weights / event_weights.sum()

                        def median_equation(value: float) -> float:
                            return float(weights @ ndtr((value - centers) / sigma) - 0.5)

                        root = brentq(median_equation, centers.min() - 8 * sigma, centers.max() + 8 * sigma)
                        conditional_median = max(0.0, float(np.expm1(root)))
                    in_window = stratum & frame["Distance"].sub(distance).abs().le(25)
                    records.append({
                        "behavior": behavior, "stimulus": stimulus, "call_type": call,
                        "distance_m": distance, "predicted_response_probability": event_weights.sum(),
                        "conditional_latency_median_s": conditional_median,
                        "response_events": int((stratum & events).sum()),
                        "observed_latency_count": latency_count,
                        "stimuli_within_25m": int(in_window.sum()),
                        "response_events_within_25m": int((in_window & events).sum()),
                        "observed_latencies_within_25m": int((in_window & valid).sum()),
                        "latency_support": "unavailable" if not latency_count else
                        "sparse" if (in_window & valid).sum() < 5 else "supported",
                    })
    pd.DataFrame(records).to_csv(output / "q3_representative_latency.csv", index=False)
    pd.DataFrame(intensities).to_csv(output / "q3_observed_intensity.csv", index=False)


def any_response_support(frame: pd.DataFrame, curve: pd.DataFrame, output: Path) -> None:
    records = []
    responses = frame["mask"].ne(0)
    for row in curve.loc[curve["distance_m"].isin(REPRESENTATIVE)].itertuples(index=False):
        stratum = frame["Type"].eq(row.stimulus) & frame["assigned_call"].eq(row.call_type)
        in_window = stratum & frame["Distance"].sub(row.distance_m).abs().le(25)
        records.append({
            "stimulus": row.stimulus, "call_type": row.call_type,
            "distance_m": row.distance_m, "predicted_any_response_probability": row.probability,
            "stimuli": int(stratum.sum()), "responses": int((stratum & responses).sum()),
            "stimuli_within_25m": int(in_window.sum()),
            "responses_within_25m": int((in_window & responses).sum()),
        })
    pd.DataFrame(records).to_csv(output / "q3_representative_response_support.csv", index=False)


def run(data: Path, output: Path, seed: int, n_boot: int) -> dict:
    """Run the behavioral analysis and return aligned Q4 probabilities and draws."""
    if n_boot < 1:
        raise ValueError("At least one paired bootstrap draw is required.")
    output.mkdir(parents=True, exist_ok=True)
    frame = load_playbacks(data)
    counts = frame.iloc[::2]["Context"].value_counts(normalize=True).sort_index()
    contexts = tuple(counts.index)
    context_weights = counts.to_numpy()
    distances = np.arange(20, 150.5, .5)
    grid = probability_grid(distances, contexts, 8)
    x, grid_x = features(frame, contexts), features(grid, contexts)
    y = frame["mask"].to_numpy()

    def average_context(probabilities: np.ndarray) -> np.ndarray:
        shaped = probabilities.reshape(len(STIMULI), len(CALLS), len(distances), len(contexts), len(MASKS))
        return np.einsum("scdjm,j->scdm", shaped, context_weights)

    point = fit_masks(x, y, grid_x)
    mask_point = average_context(point)
    rng = np.random.default_rng(seed)
    pairs = len(frame) // 2
    samples = rng.integers(0, pairs, size=(n_boot, pairs))
    representative_positions = np.searchsorted(distances, REPRESENTATIVE)
    draw_arrays = np.empty((n_boot, 2, len(CALLS), len(distances)))
    natural_mask_draws = np.empty((n_boot, len(CALLS), len(distances), len(MASKS)))
    mask_draws = np.empty((n_boot, 2, len(CALLS), len(REPRESENTATIVE), len(MASKS)))
    for i, pair_draw in enumerate(samples):
        rows = (2 * pair_draw[:, None] + np.arange(2)).ravel()
        fitted = average_context(fit_masks(x[rows], y[rows], grid_x))
        draw_arrays[i] = 1 - fitted[..., 0]
        natural_mask_draws[i] = fitted[0]
        mask_draws[i] = fitted[:, :, representative_positions, :]
    if not np.allclose(mask_point.sum(axis=-1), 1) or not np.allclose(mask_draws.sum(axis=-1), 1):
        raise RuntimeError("Predicted behavior probabilities do not sum to one.")

    axes = ["stimulus", "call_type", "distance_m"]
    curve = pd.MultiIndex.from_product([STIMULI, CALLS, distances], names=axes).to_frame(index=False)
    curve["probability"] = (1 - mask_point[..., 0]).ravel()
    curve["lower"], curve["upper"] = np.quantile(
        draw_arrays.reshape(n_boot, -1), [.025, .975], axis=0,
    )
    masks = pd.MultiIndex.from_product(
        [STIMULI, CALLS, REPRESENTATIVE, MASKS], names=axes + ["mask"],
    ).to_frame(index=False)
    masks["probability"] = mask_point[:, :, representative_positions, :].ravel()
    masks["lower"], masks["upper"] = np.quantile(
        mask_draws.reshape(n_boot, -1), [.025, .975], axis=0,
    )
    observed = frame.groupby(["Type", "assigned_call", "mask"]).size().reindex(
        pd.MultiIndex.from_product([STIMULI, CALLS, MASKS]), fill_value=0,
    ).rename("events").reset_index()
    observed.columns = ["stimulus", "call_type", "mask", "events"]
    observed["stimuli"] = observed.groupby(["stimulus", "call_type"])["events"].transform("sum")
    observed["empirical_probability"] = observed["events"] / observed["stimuli"]
    observed.to_csv(output / "q3_observed_masks.csv", index=False)
    masks.to_csv(output / "q3_predicted_masks.csv", index=False)
    contrast = masks.loc[masks["stimulus"].eq("call"), axes[1:] + ["mask"]].reset_index(drop=True)
    representative_masks = mask_point.take(representative_positions, axis=2)
    contrast["natural_minus_control"] = (representative_masks[0] - representative_masks[1]).ravel()
    contrast["lower"], contrast["upper"] = np.quantile(
        (mask_draws[:, 0] - mask_draws[:, 1]).reshape(n_boot, -1), [.025, .975], axis=0,
    )
    contrast.to_csv(output / "q3_predicted_mask_contrasts.csv", index=False)
    response_figures(curve, masks, output, n_boot)
    paired_summary(frame, samples, output)
    grouped_validation(x, frame, output)
    any_response_support(frame, curve, output)
    latency_predictions(frame, x, grid, grid_x, point, context_weights, output)
    # The same adjusted model predicts changes in context, distance, and group size.
    group_sizes = np.unique(np.quantile(frame["Npenguins"], [.25, .5, .75]))
    conditions = pd.concat([
        probability_grid(np.asarray(REPRESENTATIVE), contexts, size)
        for size in group_sizes
    ], ignore_index=True)
    conditional = fit_masks(x, y, features(conditions, contexts))
    conditions["any_response_probability"] = 1 - conditional[:, 0]
    for behavior, probability in zip(BEHAVIORS, (conditional @ BITS).T):
        conditions[behavior + "Probability"] = probability
    conditions.to_csv(output / "q3_adjusted_conditions.csv", index=False)
    return {
        "distance": distances, "calls": CALLS, "natural": 1 - mask_point[0, ..., 0],
        "control": 1 - mask_point[1, ..., 0], "natural_draws": draw_arrays[:, 0],
        "control_draws": draw_arrays[:, 1],
        "natural_masks": mask_point[0], "natural_mask_draws": natural_mask_draws,
    }

