"""Align production propagation, observed behavior and Q4 planning figures."""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import q3
from q4 import environment, radius


def plot(frame, output, name, x, y, series, xlabel, ylabel, thresholds=(), bounds=None):
    frame.to_csv(output / f"{name}.csv", index=False, lineterminator="\n")
    fig, axes = plt.subplots(1, 3, figsize=(9, 2.95), sharey=True, layout="constrained")
    colors = ("#17686a", "#ae542b", "#634892", "#4d6680")
    for ax, call, label in zip(axes, q3.CALLS, ("Flat", "Modulated", "Two-voice")):
        part = frame.loc[frame.call.eq(call)]
        for color, (key, group) in zip(colors, part.groupby(series, sort=False)):
            ax.plot(group[x], group[y], label=key, color=color)
            if bounds:
                ax.fill_between(group[x], group[bounds[0]], group[bounds[1]], color=color, alpha=.16)
            if "observed" in group:
                ax.scatter(group[x], group.observed, color="#263535", s=13, zorder=3)
        for threshold in thresholds:
            ax.axhline(threshold, color="#888888", lw=.8, ls=":")
        if x == "window_s":
            ax.set_xticks((0, 15, 30, 60))
        ax.set(title=label, xlabel=xlabel, ylim=(0, 1.03))
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel(ylabel)
    axes[0].legend(fontsize=7, loc="best")
    fig.savefig(output / f"{name}.png", dpi=240)
    plt.close(fig)
    (output / f"{name}.meta.json").write_text(json.dumps(
        dict(data=f"{name}.csv", x=x, y=y, groups=["call", series], thresholds=list(thresholds),
             pointwise_interval=list(bounds) if bounds else None), indent=2) + "\n", encoding="utf-8", newline="\n")


def run(output):
    acoustic = pd.read_csv(output / "core_q2_curves.csv")
    behavior = pd.read_csv(output / "core_q3_predictions.csv")
    selected_acoustic = acoustic.loc[acoustic.selected].copy()
    selected_model, = selected_acoustic.model.unique()
    selected_mask, = behavior.query("family == 'mask' and selected").model.unique()
    timing = behavior.query("family == 'timing' and endpoint == 'Any' and selected and distance_m == 100")
    timing_plot = behavior.query("family == 'timing' and selected and distance_m == 100 and call == 'tv'")
    timing_plot.to_csv(output / "core_figure3.csv", index=False, lineterminator="\n")
    fig, axes = plt.subplots(1, 4, figsize=(9, 2.8), sharey=True, layout="constrained")
    for ax, endpoint, label in zip(axes, ("Any", "HeadsUp", "Vocal", "Approach"),
                                   ("Any response", "Head raising", "Vocalizing", "Approach")):
        data = timing_plot.loc[timing_plot.endpoint.eq(endpoint)]
        for stimulus, style, color, name in (("call", "-", "#17686a", "Natural"),
                                              ("control", "--", "#ae542b", "Control")):
            group = data.loc[data.stimulus.eq(stimulus)].sort_values("window_s")
            ax.step(group.window_s, group.probability, where="post", color=color, ls=style, label=name)
            ax.scatter(group.window_s, group.probability, color=color, s=12)
        ax.set(title=label, xlabel="Window (s)", xticks=(0, 15, 30, 60), ylim=(0, .72))
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("Cumulative response probability")
    axes[0].legend(fontsize=7)
    fig.suptitle("Stimulus timing pooled across calls and distances", fontsize=11)
    fig.savefig(output / "core_figure3.png", dpi=240)
    plt.close(fig)
    (output / "core_figure3.meta.json").write_text(json.dumps(
        dict(data="core_figure3.csv", x="window_s", y="probability",
             display_rows={"distance_m": 100, "call": "tv"},
             estimand="Stimulus-level timing pooled across calls and distances",
             groups=["endpoint", "stimulus"]), indent=2) + "\n", encoding="utf-8", newline="\n")

    distance = np.arange(20., 150.5, .5)
    acoustic = acoustic.loc[acoustic.distance_m.isin(distance)].set_index(["model", "call", "distance_m"]).sort_index()
    behavior = behavior.loc[behavior.endpoint.eq("Any")].set_index(["family", "model", "call", "stimulus", "window_s", "distance_m"]).sort_index()
    timing_model, = timing.model.unique()

    def fidelity(model, call):
        return acoustic.loc[(model, call), "fidelity"].reindex(distance).to_numpy()

    def response(family, model, call, stimulus, window):
        return behavior.loc[(family, model, call, stimulus, window), "probability"].reindex(distance).to_numpy()

    cutoff = .5 * np.mean([fidelity("isotonic", c)[0] *
                           response("mask", "full_multinomial", c, "call", 60)[0] for c in q3.CALLS])
    support = pd.read_csv(output / "core_q3_support.csv").groupby(["call", "stimulus"]).first()
    rows, limits = [], []
    for c in q3.CALLS:
        natural_support = support.loc[(c, "call")]
        control_support = support.loc[(c, "control")]
        for a, acoustic_model in (("archived", "isotonic"), ("selected", selected_model)):
            f = fidelity(acoustic_model, c)
            for b, mask_model in (("archived", "full_multinomial"), ("selected", selected_mask)):
                p = response("mask", mask_model, c, "call", 60)
                control = response("mask", mask_model, c, "control", 60)
                for loss in (0., .20):
                    gross, _ = environment(f, p, control, loss, 0)
                    value, status = radius(distance, gross, cutoff)
                    limits.append(dict(call=c, acoustic=a, behavior=b, loss=loss, criterion="gross",
                                       radius_m=value, status=status, cutoff=cutoff))
                    for w in (15, 30):
                        early = response("timing", timing_model, c, "call", w)
                        # Apply the same coupled link to the early cumulative risk.
                        early_control = response("timing", timing_model, c, "control", w)
                        _, adjusted = environment(f, early, early_control, loss, 0)
                        planning = np.minimum((1-loss)*f, adjusted)
                        passed = np.logical_and.accumulate(planning >= .5)
                        value = float(distance[passed][-1]) if passed.any() else 20.
                        status = ("above_support" if passed.all() else
                                  "below_support" if not passed.any() else "last_passing_node")
                        limits.append(dict(call=c, acoustic=a, behavior=b, loss=loss,
                                           criterion=f"joint_{w}s", radius_m=value,
                                           status=status, cutoff=.5))
                        for j, d in enumerate(distance):
                            rows.append(dict(call=c, distance_m=d, acoustic=a, behavior=b,
                                             acoustic_model=acoustic_model, mask_model=mask_model,
                                             timing_model=timing_model, loss=loss, window_s=w,
                                             fidelity=(1-loss)*f[j], early_response=adjusted[j],
                                             gross=gross[j], planning_score=planning[j],
                                             prefix_pass=passed[j],
                                             natural_support=natural_support.min_observed_m <= d <= natural_support.max_observed_m,
                                             control_support=control_support.min_observed_m <= d <= control_support.max_observed_m))
    curves = pd.DataFrame(rows)
    curves.to_csv(output / "core_q4_curves.csv", index=False, lineterminator="\n")
    pd.DataFrame(limits).to_csv(output / "core_q4_radii.csv", index=False, lineterminator="\n")
    fig = curves.query("acoustic == 'selected' and behavior == 'selected' and window_s == 30")
    gross = fig.assign(scenario=fig.loss.map({0.: "Clean product", .20: "Coupled-loss product"}),
                       score=fig.gross)
    joint = fig.assign(scenario=fig.loss.map({0.: "Clean joint minimum", .20: "Coupled-loss joint minimum"}),
                       score=fig.planning_score)
    plot(pd.concat((gross, joint)), output, "core_figure4", "distance_m", "score",
         "scenario", "Distance (m)", "Planning score", (cutoff, .5))
