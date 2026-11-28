"""Plot archived noise experiments and field-design evidence for the core paper."""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


TEAL = "#17686a"
ORANGE = "#ae542b"
PURPLE = "#634892"
INK = "#29323c"
CALLS = ("flat", "mod", "tv")
CALL_LABELS = ("Flat", "Modulated", "Two-voice")


def save_figure(figure, rows, output, name, **metadata):
    rows.to_csv(output / f"{name}.csv", index=False, lineterminator="\n")
    (output / f"{name}.meta.json").write_text(
        json.dumps(dict(data=f"{name}.csv", **metadata), indent=2) + "\n",
        encoding="utf-8", newline="\n",
    )
    figure.savefig(output / f"{name}.png", dpi=300)
    plt.close(figure)


def plot_noise(archive, output):
    """Show band-minus-broadband contrasts for the three measured call examples."""
    rows = pd.read_csv(archive / "appendix5_noise_contrasts.csv").query("metric == 'composite'")
    figure, panels = plt.subplots(1, 3, figsize=(7.2, 2.9), sharex=True, sharey=True,
                                  layout="constrained")
    bands = (("100_500", TEAL, "-", "100-500 Hz"),
             ("500_3000", ORANGE, "--", ">500-3,000 Hz"))
    clip_names = ("flat", "modulated", "two-voice")
    for ax, clip, name, letter in zip(panels, clip_names, CALL_LABELS, "ABC"):
        ax.axhline(0, color="#9a9fa5", lw=.8)
        ax.axvline(0, color="#d4d8dc", lw=.7, zorder=0)
        for band, color, linestyle, label in bands:
            part = rows.loc[rows["clip"].eq(clip) & rows.band.eq(band)].sort_values("snr_db")
            ax.fill_between(part.snr_db, part.low95, part.high95, color=color, alpha=.14, linewidth=0)
            ax.plot(part.snr_db, part["mean"], color=color, linestyle=linestyle, marker="o",
                    markersize=3.0, linewidth=1.4, label=label)
        ax.set(title=f"{letter}  {name}", xlabel="Input SNR (dB)", xticks=(-10, 0, 10, 20))
    panels[0].set_ylabel("Composite correlation change")
    handles, labels = panels[0].get_legend_handles_labels()
    figure.legend(handles, labels, loc="outside upper center", ncol=2, frameon=False)
    save_figure(
        figure, rows, output, "core_figure5", source="appendix5_noise_contrasts.csv",
        contrast="Band minus broadband, same noise RMS at the same clip and input SNR",
        uncertainty="Central 95% of 200 paired simulated noise realizations per clip and SNR",
        sample="One archival WAV per call type",
    )


def loss_curves(archive):
    """Evaluate the archived inclusive retention boundary over its loss domain."""
    targets = pd.read_csv(archive / "q4_target_loss_boundaries.csv").query(
        "rule == 'all_four_prefix' and kind == 'diagonal' and distance_m in [100, 150]"
    )
    tables = []
    for row in targets.itertuples():
        acoustic = np.linspace(0, min(.20, 1 - row.requirement), 201)
        response = np.clip(1 - row.requirement / (1 - acoustic), 0, .20)
        tables.append(pd.DataFrame(dict(
            model=row.model, distance_m=row.distance_m, requirement=row.requirement,
            acoustic_loss_pct=100 * acoustic, response_loss_limit_pct=100 * response,
            target_outside_retained_range=(
                row.target_outside_natural_range or row.target_outside_control_range
            ),
        )))
    return pd.concat(tables, ignore_index=True)


def plot_field_design(archive, output):
    """Compare where to sample and which losses and participation matter."""
    allocations = pd.read_csv(archive / "q4_paired_planning_allocations.csv").query(
        "plan in ['uniform', 'fisher_constrained']"
    )
    responders = pd.read_csv(output / "core_q4_responders.csv").query("call == 'flat'")
    limits = loss_curves(archive)
    figure, panels = plt.subplot_mosaic(
        [["allocation", "allocation"], ["responders", "loss"]],
        figsize=(7.25, 5.45), height_ratios=(.86, 1), layout="constrained",
    )
    allocation = panels["allocation"]
    groups = ((np.arange(4), "uniform", "Uniform"), (np.arange(4) + 5, "fisher_constrained", "Constrained Fisher"))
    distances = (20, 50, 100, 150)
    for x, plan, label in groups:
        table = allocations.loc[allocations.plan.eq(plan)].pivot(index="distance_m", columns="call", values="pairs")
        bottom = np.zeros(len(distances))
        for call, name, color in zip(CALLS, CALL_LABELS, (TEAL, ORANGE, PURPLE)):
            count = table.loc[list(distances), call].to_numpy()
            allocation.bar(x, count, bottom=bottom, width=.71, color=color,
                           label=name if plan == "uniform" else None)
            bottom += count
        allocation.text(x.mean(), 76, label, ha="center", va="bottom")
    allocation.set(title="A  Location of 120 new pairs", ylabel="Playback pairs",
                   ylim=(0, 94), xticks=np.r_[groups[0][0], groups[1][0]],
                   xticklabels=distances * 2, xlabel="Matched playback distance (m)")
    allocation.legend(loc="upper left", ncol=3, frameon=False)

    counts = panels["responders"]
    for y, row in enumerate(responders.itertuples()):
        counts.hlines(y, row.lower, row.upper, color="#a8adb4", linewidth=2.0,
                      label="Sharp range" if y == 0 else None)
        counts.scatter([row.share_25, row.share_50, row.share_75], [y]*3, marker="o", s=32,
                       facecolor="white", edgecolor=TEAL, zorder=3,
                       label="25%, 50%, 75% participation" if y == 0 else None)
        counts.scatter(row.independent, y, marker="D", s=30, color=INK, zorder=3,
                       label="Independent birds" if y == 0 else None)
    counts.set(title="B  Responders at 100 m", xlabel="Expected birds in a group of eight",
               yticks=(0, 1), yticklabels=("Clean", "20% loss"), ylim=(1.6, -.65), xlim=(0, 5))
    counts.legend(loc="upper center", bbox_to_anchor=(.5, -.24), frameon=False, fontsize=8)

    boundary = panels["loss"]
    for (distance, model), part in limits.groupby(["distance_m", "model"], sort=True):
        style = "-" if model == "full" else "--"
        color = TEAL if distance == 100 else PURPLE
        label = f"{distance:g} m, " + ("full fit" if model == "full" else "deletion fit")
        if part.target_outside_retained_range.iloc[0]:
            label += "*"
        boundary.plot(part.acoustic_loss_pct, part.response_loss_limit_pct,
                      color=color, linestyle=style, linewidth=1.5, label=label)
    boundary.set(title="C  Two-voice loss limits", xlabel="Acoustic fidelity loss (%)",
                 ylabel="Allowed response loss (%)", xlim=(0, 20.5), ylim=(0, 21.4),
                 xticks=(0, 5, 10, 15, 20), yticks=(0, 5, 10, 15, 20))
    boundary.legend(loc="upper center", bbox_to_anchor=(.5, -.24), ncol=2, frameon=False, fontsize=8)

    plotted = pd.concat([
        allocations.assign(panel="allocation"), responders.assign(panel="responders"),
        limits.assign(panel="loss_boundary"),
    ], ignore_index=True)
    save_figure(
        figure, plotted, output, "core_figure6",
        sources=["q4_paired_planning_allocations.csv", "core_q4_responders.csv", "q4_target_loss_boundaries.csv"],
        loss_rule="Archive two-voice all-four-curve prefix and inclusive 80% across 4,800 draws",
        loss_boundary="(1-acoustic_loss)*(1-response_loss) >= requirement, both losses at most 20%",
        participation="One row per scenario at 100 m because the adopted group response pools calls",
    )


def run(archive, output):
    with plt.rc_context({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                         "axes.linewidth": .7, "pdf.fonttype": 42, "ps.fonttype": 42}):
        plot_noise(archive, output)
        plot_field_design(archive, output)

