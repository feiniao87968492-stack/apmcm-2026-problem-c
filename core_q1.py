"""Recording-group comparison of physical acoustic features and estimators."""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from appendix5_noise import load_clips
from q1 import CALLS, FEATURES, FROZEN_TEST_GROUPS, comparison_scores, macro_f1


def model(kind, setting, class_weight=None):
    if kind == "logistic":
        return make_pipeline(StandardScaler(), LogisticRegression(C=setting, max_iter=1000))
    return RandomForestClassifier(n_estimators=400, max_depth=setting, min_samples_leaf=5,
                                  max_features="sqrt", random_state=20261209, class_weight=class_weight)


def logloss(p, labels):
    return -np.log(p[np.arange(len(labels)), labels].clip(1e-15))


def examples(data):
    if not list(data.glob("Supplementary5*.wav")):
        return []
    rows = []
    for call, values in load_clips(data).items():
        frequency = np.fft.rfftfreq(len(values), 1/12000)
        energy = abs(np.fft.rfft(values * np.hanning(len(values))))**2
        cumulative = np.cumsum(energy) / energy.sum()
        q25, q50, q75 = np.interp([.25, .5, .75], cumulative, frequency)
        rows.append(dict(call=call, duration_s=len(values)/12000, peak_hz=frequency[energy.argmax()],
                         q25_hz=q25, q50_hz=q50, q75_hz=q75, bandwidth_hz=q75-q25))
    return rows


def run(data, output):
    frame = pd.read_csv(next(data.glob("Data01*.csv")))
    classes = np.array(sorted(CALLS))
    labels = np.searchsorted(classes, frame.CallType)
    _, groups = np.unique(frame.Date.astype(str) + " | " + frame.Location, return_inverse=True)
    raw = frame[list(FEATURES)].to_numpy()
    duration, fundamental, peak, q25, q50, q75 = raw.T
    iqr = q75 - q25
    physical = np.column_stack((np.log(duration), np.log(fundamental), np.log(peak/fundamental),
                               np.log(iqr), (peak-q25)/iqr, (q75+q25-2*q50)/iqr))
    candidates = {f"{rep}_{kind}": (x, kind, settings)
                  for rep, x in (("original", raw), ("physical", physical))
                  for kind, settings in (("logistic", (.1, 1., 10.)), ("forest", (2, 4)))}
    weighting = {"physical_balanced": "balanced", "physical_balanced_subsample": "balanced_subsample"}
    candidates.update({name: (physical, "forest", (2, 4)) for name in weighting})
    probabilities = {m: np.empty((len(labels), len(classes)))
                     for m in ("fixed_logistic", "prevalence", *candidates)}
    multiplier_name = "physical_forest_tv_multiplier"
    multipliers = (1., 1.25, 1.5, 2., 3., 4.)
    tv = int(np.flatnonzero(classes == "tv")[0])
    decision_weights = np.ones(len(labels))
    settings_rows = []
    for fold, held in enumerate(FROZEN_TEST_GROUPS, 1):
        test = np.flatnonzero(np.isin(groups, held))
        train = np.flatnonzero(~np.isin(groups, held))
        fit = model("logistic", 1).fit(raw[train], labels[train])
        probabilities["fixed_logistic"][test] = fit.predict_proba(raw[test])
        probabilities["prevalence"][test] = np.bincount(labels[train], minlength=3) / len(train)
        folds = list(StratifiedGroupKFold(3, shuffle=True, random_state=20261209).split(
            raw[train], labels[train], groups[train]))
        for name, (x, kind, settings) in candidates.items():
            losses, inner_predictions = [], []
            for setting in settings:
                predictions = np.zeros((len(train), len(classes)))
                for a, b in folds:
                    fit = model(kind, setting, weighting.get(name)).fit(x[train[a]], labels[train[a]])
                    predictions[np.ix_(b, fit.classes_)] = fit.predict_proba(x[train[b]])
                losses.append(logloss(predictions, labels[train]).mean())
                inner_predictions.append(predictions)
            best = settings[int(np.argmin(losses))]
            probabilities[name][test] = model(kind, best, weighting.get(name)).fit(x[train], labels[train]).predict_proba(x[test])
            settings_rows.append(dict(fold=fold, model=name, setting=best, inner_log_loss=min(losses)))
            if name == "physical_forest":
                inner = inner_predictions[int(np.argmin(losses))]
                weighted = np.repeat(inner[None], len(multipliers), axis=0)
                weighted[:, :, tv] *= np.array(multipliers)[:, None]
                scores = [macro_f1(classes[labels[train]], classes[p.argmax(axis=1)]) for p in weighted]
                selected = int(np.argmax(scores))
                decision_weights[test] = multipliers[selected]
                settings_rows.append(dict(fold=fold, model=multiplier_name, setting=best,
                                          inner_log_loss=min(losses), tv_multiplier=multipliers[selected],
                                          inner_macro_f1=scores[selected]))

    rows = [np.flatnonzero(groups == g) for g in np.unique(groups)]
    sampled = np.random.default_rng(20261210).integers(len(rows), size=(1000, len(rows)))
    draws = [np.concatenate([rows[i] for i in draw]) for draw in sampled]
    draws = [draw for draw in draws if len(np.unique(labels[draw])) == len(classes)]
    actual = classes[labels]
    hard = {name: classes[p.argmax(axis=1)] for name, p in probabilities.items()}
    decision = probabilities["physical_forest"].copy()
    decision[:, tv] *= decision_weights
    hard[multiplier_name] = classes[decision.argmax(axis=1)]
    probabilities[multiplier_name] = probabilities["physical_forest"]
    baseline = np.array([macro_f1(actual[d], hard["fixed_logistic"][d]) for d in draws])
    records = []
    for name, p in probabilities.items():
        f1, *recall = comparison_scores(actual, hard[name])
        resampled = [macro_f1(actual[d], hard[name][d]) for d in draws]
        lo, hi = np.quantile(resampled-baseline, [.025, .975])
        pred_tv = hard[name] == "tv"
        true_tv = int(np.sum(pred_tv & (actual == "tv")))
        records.append(dict(tv_true_positive=true_tv, tv_predicted=int(pred_tv.sum()),
                            tv_precision=true_tv/pred_tv.sum() if pred_tv.any() else np.nan,model=name, macro_f1=f1, lower_f1_gain=lo, upper_f1_gain=hi,
                            **dict(zip((f"recall_{c}" for c in CALLS), recall)),
                            log_loss=logloss(p, labels).mean(),
                            brier=((p-np.eye(3)[labels])**2).sum(axis=1).mean()))
    scores = pd.DataFrame(records).set_index("model")
    base, prior = scores.loc["fixed_logistic"], scores.loc["prevalence"]
    qualified = scores.loc[[*candidates, multiplier_name]].query(
        "lower_f1_gain > 0 and recall_tv >= @base.recall_tv and log_loss < @prior.log_loss and brier < @prior.brier"
    )
    selected = "fixed_logistic" if qualified.empty else qualified.macro_f1.idxmax()
    scores["selected"] = scores.index == selected
    oof = pd.DataFrame(dict(row=np.arange(1, len(labels)+1), group=groups, actual=actual))
    for name, p in probabilities.items():
        oof[f"{name}_decision"] = hard[name]
        for j, call in enumerate(classes):
            oof[f"{name}_{call}"] = p[:, j]
    oof["tv_decision_multiplier"] = decision_weights
    audit = frame.groupby("CallType")[["F02", "PulseRate"]].count().join(frame.groupby("CallType").size().rename("n"))
    output.mkdir(parents=True, exist_ok=True)
    plot_decisions(frame, actual, hard[selected], classes, selected, output)
    for suffix, table in (("scores", scores.reset_index()), ("settings", pd.DataFrame(settings_rows)),
                          ("oof", oof), ("availability", audit.reset_index()),
                          ("wav", pd.DataFrame(examples(data)))):
        if not table.empty:
            table.to_csv(output / f"core_q1_{suffix}.csv", index=False, lineterminator="\n")

def plot_decisions(frame, actual, hard, classes, selected, output):
    import json
    import matplotlib.pyplot as plt
    from sklearn.metrics import confusion_matrix

    counts = confusion_matrix(actual, hard, labels=classes)
    features = (*FEATURES, "F02", "PulseRate")
    labels = ("Duration", "First fundamental", "Peak frequency", "Spectral Q25",
              "Spectral Q50", "Spectral Q75", "Second fundamental", "Pulse rate")
    colors = ("#17686a", "#ae542b", "#634892")
    names = ("Flat", "Modulated", "Two-voice")
    fig, (dist, ax) = plt.subplots(1, 2, figsize=(8.3, 3.7), layout="constrained",
                                   gridspec_kw={"width_ratios": (1.5, 1)})
    rows = []
    for i, feature in enumerate(features):
        quartiles = frame.groupby("CallType")[feature].quantile([.25, .5, .75]).unstack()
        start = quartiles[.25].min()
        width = quartiles[.75].max() - start
        for j, (call, color, name) in enumerate(zip(classes, colors, names)):
            low, middle, high = quartiles.loc[call]
            if not np.isfinite(middle):
                continue
            dist.errorbar((middle-start)/width, i+.22*(j-1),
                          xerr=[[(middle-low)/width], [(high-middle)/width]],
                          color=color, fmt="o", markersize=3, capsize=2,
                          label=name if i == 0 else None)
            rows.append(dict(panel="distribution", feature=feature, call=call, count=frame.loc[
                frame.CallType.eq(call), feature].count(), q25=low, median=middle, q75=high,
                scale_origin=start, scale_width=width))
    dist.set(yticks=range(len(labels)), yticklabels=labels, xlabel="Scaled median and IQR",
             title="A  Acoustic features")
    dist.invert_yaxis()
    dist.legend(fontsize=7, loc="lower center", bbox_to_anchor=(.5, -.24), ncol=3, frameon=False)
    for i, j in np.ndindex(counts.shape):
        rows.append(dict(panel="confusion", call=classes[i], predicted=classes[j], count=counts[i, j]))
    pd.DataFrame(rows).to_csv(output / "core_figure1.csv", index=False, lineterminator="\n")
    (output / "core_figure1.meta.json").write_text(json.dumps(
        dict(data="core_figure1.csv", model=selected,
             distribution="Observed medians and quartiles on a common scale within each feature",
             confusion="Counts of held-out recordings by recorded and predicted class"),
        indent=2) + "\n", encoding="utf-8", newline="\n")
    ax.imshow(counts, cmap="Blues", vmin=0)
    ax.set(title="B  Grouped holdout", xticks=range(3), yticks=range(3), xticklabels=names, yticklabels=names,
           xlabel="Predicted call", ylabel="Recorded call")
    for i, j in np.ndindex(counts.shape):
        ax.text(j, i, str(counts[i, j]), ha="center", va="center",
                color="white" if counts[i, j] > .58*counts.max() else "#172332")
    fig.savefig(output / "core_figure1.png", dpi=240)
    plt.close(fig)
