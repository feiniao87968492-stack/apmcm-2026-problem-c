"""Propagate jointly sampled ERA5 weather through the fitted Q50 attenuation."""
from pathlib import Path

import numpy as np
import pandas as pd

import core_q2
import physical_attenuation
import q2
from q2_forward import observed_and_support


SEED = 20261212
DRAWS = 10_000
PERCENTILES = [.05, .50, .95]
WEATHER = Path(__file__).resolve().parent / "sources/weather/era5-calm-dam-and-false-bay.csv"


def absorption(frequency, hours):
    return core_q2.iso9613_absorption(
        frequency, hours.temperature_c.to_numpy()[:, None],
        hours.relative_humidity_pct.to_numpy()[:, None],
        hours.surface_pressure_hpa.to_numpy()[:, None] / 10,
    )


def radius_crossings(parameters, alpha, threshold):
    """Vectorized roots for the monotone fidelity curves, with support bounds."""
    lo = np.full_like(alpha, q2.KNOTS[0])
    hi = np.full_like(alpha, q2.KNOTS[-1])

    def fidelity(distance):
        return core_q2.absorption_curve(distance[..., None], parameters, alpha)[..., 0]

    below = fidelity(lo) < threshold
    above = fidelity(hi) >= threshold
    for _ in range(42):
        midpoint = (lo + hi) / 2
        passes = fidelity(midpoint) >= threshold
        lo = np.where(passes, midpoint, lo)
        hi = np.where(passes, hi, midpoint)
    radius = np.where(below, q2.KNOTS[0], np.where(above, q2.KNOTS[-1], (lo + hi) / 2))
    return radius, below, above


def summarize(regimes, fixed_parameters, fixed_alpha):
    rows = []
    for threshold, label in core_q2.THRESHOLDS.items():
        reference, _, _ = radius_crossings(fixed_parameters, fixed_alpha, threshold)
        for name, (parameters, coefficients) in regimes.items():
            radius, below, above = radius_crossings(parameters, coefficients, threshold)
            quantiles = np.quantile(radius, PERCENTILES, axis=0)
            delta = np.quantile(radius-reference, PERCENTILES, axis=0)
            for c, call in enumerate(q2.CALLS):
                rows.append(dict(
                    regime=name, call=call, threshold=threshold, level=label,
                    reference_m=reference[c], p05_m=quantiles[0, c], median_m=quantiles[1, c],
                    p95_m=quantiles[2, c], paired_change_p05_m=delta[0, c],
                    paired_change_median_m=delta[1, c], paired_change_p95_m=delta[2, c],
                    below_support=below[:, c].sum(), above_support=above[:, c].sum(),
                    draws=len(radius),
                ))
    return pd.DataFrame(rows)


def scenarios(data):
    weather = pd.read_csv(WEATHER)
    target = weather[weather.site.eq("false_bay")].reset_index(drop=True)
    dam = weather[weather.site.eq("brandvlei")].reset_index(drop=True)
    coefficients, table = core_q2.absorption_from_recordings(data)
    fixed_alpha = coefficients["Q50"]
    frequency = table[table.frequency_measure.eq("Q50")].median_frequency_hz.to_numpy()
    dam_alpha, bay_alpha = absorption(frequency, dam), absorption(frequency, target)

    observed, _ = observed_and_support(data)
    num_refits = len(observed) - 1
    dam_stream, target_stream, fit_stream = map(np.random.default_rng, np.random.SeedSequence(SEED).spawn(3))
    dam_indices = dam_stream.integers(len(dam), size=num_refits)
    bay_indices = target_stream.integers(len(target), size=DRAWS)
    fit_indices = fit_stream.integers(num_refits, size=DRAWS)

    def fit(values, shared, coefficients):
        return core_q2.fit_absorption(q2.KNOTS, values, shared, coefficients, penalty=.0025)

    initials = [physical_attenuation.fit(q2.KNOTS, values, True) for values in observed]
    anchor = fit(observed[0], initials[0], fixed_alpha)
    fixed_fits = np.stack([fit(values, shared, fixed_alpha)
                           for values, shared in zip(observed[1:], initials[1:])])
    joint_fits = np.stack([fit(values, shared, dam_alpha[row])
                           for values, shared, row in zip(observed[1:], initials[1:], dam_indices)])

    bay_draws = bay_alpha[bay_indices]
    joint = joint_fits[fit_indices], bay_draws
    regimes = {
        "weather_only": (np.broadcast_to(anchor, joint[0].shape), bay_draws),
        "rows_only": (fixed_fits[fit_indices], np.broadcast_to(fixed_alpha, bay_draws.shape)),
        "joint": joint,
    }
    return joint, summarize(regimes, anchor, fixed_alpha)
