"""Compare equal-power noise spectra on the three Supplementary 5 clips."""
from argparse import ArgumentParser
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.io import wavfile
from scipy.signal import hilbert, windows

CLIPS = ("flat", "modulated", "two-voice")
BANDS = ("broadband", "100_500", "500_3000")
SNRS = (-10, -5, 0, 5, 10, 20)
METRICS = ("spectrogram_loss", "spectrum_loss", "envelope_loss", "composite")
REPEATS = 200
RATE = 12000
SEED = 20261202
TOL = 1e-12
WINDOW = windows.hann(256, sym=False)


def load_clips(data):
    clips = {}
    for clip in CLIPS:
        path, = data.glob(f"Supplementary5*_{clip}.wav")
        rate, samples = wavfile.read(path)
        if rate != RATE or samples.ndim != 1 or samples.dtype != np.int16:
            raise ValueError(f"Unexpected audio format in {path.name}")
        values = samples.astype(float) / 32768
        clips[clip] = values - values.mean()
    return clips


def features(values):
    frames = np.lib.stride_tricks.sliding_window_view(values, 256)[::128]
    return (np.abs(np.fft.rfft(frames * WINDOW))[:, 1:].ravel(),
            np.abs(np.fft.rfft(values))[1:], np.abs(hilbert(values)))


def normalized(values):
    return tuple((x-x.mean()) / np.linalg.norm(x-x.mean()) for x in features(values))


def measure(clean, values):
    correlations = np.clip([x @ y for x, y in zip(clean, normalized(values))], -1., 1.)
    return np.r_[1-correlations, np.clip(correlations.mean(), 0., 1.)]


def rms(values):
    return np.sqrt(np.mean(values**2))


def noise_masks(size):
    hz = np.fft.rfftfreq(size, 1/RATE)
    return (hz > 0, (hz >= 100) & (hz <= 500), (hz > 500) & (hz <= 3000))


def rank(values):
    groups = []
    for index in np.argsort(-values, kind="stable"):
        if groups and values[groups[-1][0]] - values[index] <= TOL:
            groups[-1].append(index)
        else:
            groups.append([index])
    return ">".join("=".join(CLIPS[i] for i in sorted(group)) for group in groups)


def describe(values):
    low, high = np.quantile(values, [.025, .975])
    return dict(mean=values.mean(), low95=low, high95=high)


def run(data, output):
    clips = load_clips(data)
    clean = {name: normalized(values) for name, values in clips.items()}
    masks = {name: noise_masks(len(values)) for name, values in clips.items()}
    power = {name: rms(values) for name, values in clips.items()}
    sizes = max(map(len, clips.values()))
    rng = np.random.default_rng(SEED)
    scores = np.empty((REPEATS, len(CLIPS), len(BANDS), len(SNRS), len(METRICS)))
    achieved = np.empty(scores.shape[:-1])
    zero = []
    for name, values in clips.items():
        losses = measure(clean[name], values)
        np.testing.assert_allclose(losses, [0, 0, 0, 1], atol=TOL, rtol=0)
        zero.append(dict(clip=name, sample_rate_hz=RATE, samples=len(values),
                         **dict(zip(METRICS, losses))))
    for repeat in range(REPEATS):
        vector = rng.standard_normal(sizes)
        for i, (name, values) in enumerate(clips.items()):
            spectrum = np.fft.rfft(vector[:len(values)])
            for j, bins in enumerate(masks[name]):
                noise = np.fft.irfft(spectrum*bins, n=len(values))
                unit_noise = noise/rms(noise)
                for k, snr in enumerate(SNRS):
                    added = unit_noise * (power[name] * 10**(-snr/20))
                    achieved[repeat, i, j, k] = 20*np.log10(power[name]/rms(added))
                    scores[repeat, i, j, k] = measure(clean[name], values+added)
    np.testing.assert_allclose(achieved, np.broadcast_to(SNRS, achieved.shape), atol=TOL, rtol=0)

    summary, contrasts, ranks = [], [], []
    for j, band in enumerate(BANDS):
        for k, snr in enumerate(SNRS):
            composites = scores[:, :, j, k, -1]
            mean_rank = rank(composites.mean(axis=0))
            for ordering, count in sorted(Counter(map(rank, composites)).items()):
                ranks.append(dict(band=band, snr_db=snr, mean_rank=mean_rank,
                                  replicate_rank=ordering, count=count, repeats=REPEATS))
            for i, name in enumerate(CLIPS):
                labels = dict(clip=name, band=band, snr_db=snr, repeats=REPEATS)
                for m, metric in enumerate(METRICS):
                    values = scores[:, i, j, k, m]
                    summary.append(dict(labels, metric=metric, **describe(values),
                                        max_snr_error_db=np.abs(achieved[:, i, j, k]-snr).max()))
                    if j:
                        contrasts.append(dict(labels, metric=metric,
                                              **describe(values - scores[:, i, 0, k, m])))
    output.mkdir(parents=True, exist_ok=True)
    for name, rows in (("summary", summary), ("contrasts", contrasts), ("ranks", ranks), ("zero", zero)):
        pd.DataFrame(rows).to_csv(output / f"appendix5_noise_{name}.csv", index=False,
                                 lineterminator="\n", float_format="%.12g")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True, help="Directory containing Supplementary 5 WAV files")
    parser.add_argument("--output", type=Path, default=Path("results"))
    args = parser.parse_args()
    run(args.data, args.output)
