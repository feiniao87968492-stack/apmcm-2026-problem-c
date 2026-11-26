"""Propagate the four equal-weight attenuation fits into the focal Q4 margins."""
from pathlib import Path

import numpy as np
import pandas as pd

import physical_attenuation as physical
import q2
import q3
from control_subtraction import reference, score_curves
from distance_deletion import pair_filters, refit
from distance_deletion_mc import ACOUSTIC_SEED, CASES, DATE_SEED
from q2_shape_rank import fit_all
from q4_envelope_attainment import DISTANCES, DRAWS, MODELS, REQUIRED


def acoustic_fidelities(data, distances=DISTANCES, *, include_shared=False):
    tables = q2.load_tables(data)
    rng = np.random.default_rng(ACOUSTIC_SEED)
    samples = []
    for call in q2.CALLS:
        values = tables[call]
        samples.append(np.concatenate((np.nanmean(values, axis=1)[None],
                                       q2.bootstrap_means(values, DRAWS, rng))))
    rows, shared_parameters = [], []
    for draw in zip(*samples):
        fits = fit_all(q2.KNOTS, np.stack([physical.equal_means(m) for m in draw]))
        if include_shared:
            shared_parameters.append(fits["shared_g"])
        rows.append({shape: (np.stack([q2.interpolated(distances, row) for row in fitted])
                             if shape == "isotonic" else physical.curve(distances, fitted))
                     for shape, fitted in fits.items()})
    curves = {shape: np.stack([row[shape] for row in rows]) for shape in rows[0]}
    return (curves, np.stack(shared_parameters)) if include_shared else curves


def behavior_probabilities(data, distances=DISTANCES):
    frame = q3.load_playbacks(data)
    weights = frame.loc[frame.Type.eq("call"), "Context"].value_counts(normalize=True).sort_index()
    n_dates = frame.Date.nunique()
    dates = np.random.default_rng(DATE_SEED).integers(n_dates, size=(DRAWS, n_dates))
    filters, _ = pair_filters(frame)
    for model in MODELS:
        point, draws = refit(frame, filters[model], dates, weights, distances=distances)
        yield model, np.concatenate((point[None], draws))


def summarize(model, probabilities, fidelities, cutoffs):
    for call, distance, link, definition in CASES:
        i, j = q2.CALLS.index(call), np.searchsorted(DISTANCES, distance)
        natural, control = probabilities[:, :, i, j].T
        cutoff = cutoffs[definition]
        coupled = link == "coupled"
        margins = {}
        for shape, values in fidelities.items():
            gross, net = score_curves(values[:, i, j], natural, control, .20 if coupled else 0., coupled)
            margins[shape] = (gross if definition == "gross" else net) - cutoff
        shared_fidelity = fidelities["shared_g"][:, i, j]
        shared_margin = margins["shared_g"]
        shared_attains = shared_margin[1:] >= 0
        shared_count = int(shared_attains.sum())
        for shape, margin in margins.items():
            fidelity = fidelities[shape][:, i, j]
            df = fidelity - shared_fidelity
            dm = margin - shared_margin
            assert np.isfinite(margin).all() and np.isfinite(fidelity).all()
            df_low, df_high = np.quantile(df[1:], [.025, .975])
            dm_low, dm_high = np.quantile(dm[1:], [.025, .975])
            low, high = np.quantile(margin[1:], [.025, .975])
            attains = margin[1:] >= 0
            count = int(attains.sum())
            passes = count >= REQUIRED
            yield dict(model=model, call=call, distance_m=distance, link=link, definition=definition,
                       shape=shape, fidelity=fidelity[0], delta_fidelity=df[0],
                       delta_fidelity_low95=df_low, delta_fidelity_high95=df_high, cutoff=cutoff[0],
                       margin=margin[0], margin_low95=low, margin_high95=high, delta_margin=dm[0],
                       delta_margin_low95=dm_low, delta_margin_high95=dm_high,
                       count=count, draws=DRAWS, support=count/DRAWS, passes_80=passes,
                       delta_count=count-shared_count, gains=int((attains & ~shared_attains).sum()),
                       losses=int((~attains & shared_attains).sum()),
                       decision_changed=passes != (shared_count >= REQUIRED))


def check_archives(result, baseline):
    keys = ["model", "call", "distance_m", "link", "definition"]
    point = pd.read_csv(baseline / "distance_deletion_points.csv").set_index(keys)
    counts = pd.read_csv(baseline / "distance_deletion_mc.csv").query(
        "source == 'fresh' and requested_draws == @DRAWS"
    ).set_index(keys)
    iso = pd.read_csv(baseline / "q4_envelope_attainment_points.csv").query(
        "reference == 'equal_weight' and abs(weight - 1/3) < 1e-12"
    ).set_index(keys)
    shared = result.query("shape == 'shared_g'").set_index(keys)
    isotonic = result.query("shape == 'isotonic'").set_index(keys)
    for actual, archived_points, archived_counts in ((shared, point, counts), (isotonic, iso, iso)):
        np.testing.assert_allclose(actual.margin, archived_points.loc[actual.index, "margin"],
                                   atol=1e-6, rtol=0)
        np.testing.assert_array_equal(actual["count"], archived_counts.loc[actual.index, "count"])


def write(data: Path, output: Path, baseline: Path):
    fidelities = acoustic_fidelities(data)
    rows = []
    for model, probabilities in behavior_probabilities(data):
        if model == "full":
            natural, control = probabilities.transpose(1, 0, 2, 3)
            cutoffs = {"gross": reference(fidelities["isotonic"], natural),
                       "net_own": reference(fidelities["isotonic"], natural-control)}
        rows.extend(summarize(model, probabilities, fidelities, cutoffs))
    result = pd.DataFrame(rows)
    check_archives(result, baseline)
    output.mkdir(parents=True, exist_ok=True)
    result.to_csv(output / "q4_shape_propagation.csv", index=False, lineterminator="\n")
