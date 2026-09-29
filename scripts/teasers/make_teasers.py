"""Generate the project teaser figures shown on /projects/.

Every figure is drawn from published results or from the algorithm the
project describes; see the per-figure docstrings for sources.

    python scripts/teasers/make_teasers.py            # writes images/teasers/*.svg
    python scripts/teasers/make_teasers.py --refresh-context

--refresh-context re-aggregates data/situation_hour_counts.csv from the
public Deezer dataset (Zenodo record 5552288, ~108 MB download).
"""

import argparse
import urllib.request
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap
from scipy.signal import fftconvolve, istft, stft

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "images" / "teasers"
DATA = Path(__file__).resolve().parent / "data"

# Card teasers are displayed at a 2:1 aspect ratio (see .archive__item-teaser
# in _sass/_custom.scss). Keep the physical size small so that 8-9 pt text
# stays legible when the card is ~350-480 px wide.
FIG_SIZE = (4.4, 2.2)

# Site palette (_sass/_variables.scss).
INK = "#1e293b"
MUTED = "#64748b"
RULE = "#cbd5e1"
FAINT = "#e2e8f0"
NAVY = "#1d3557"
TEAL = "#0891b2"
NEUTRAL = "#a3afbf"

SEQ = LinearSegmentedColormap.from_list(
    "site_seq", ["#ffffff", "#cfe9f0", TEAL, NAVY], N=256
)


def setup_style():
    family = "Inter"
    if not any(f.name == family for f in font_manager.fontManager.ttflist):
        print("warning: Inter not found, falling back to DejaVu Sans")
        family = "DejaVu Sans"
    plt.rcParams.update(
        {
            "font.family": family,
            "font.size": 8.5,
            "text.color": INK,
            "axes.edgecolor": RULE,
            "axes.labelcolor": MUTED,
            "axes.labelsize": 8,
            "axes.linewidth": 0.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.titlesize": 9,
            "axes.titleweight": "semibold",
            "axes.titlelocation": "left",
            "axes.titlepad": 6,
            "axes.titlecolor": INK,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "xtick.labelsize": 7.5,
            "ytick.labelsize": 7.5,
            "xtick.major.size": 2.5,
            "ytick.major.size": 2.5,
            "xtick.major.width": 0.8,
            "ytick.major.width": 0.8,
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
            "svg.fonttype": "path",
            "svg.hashsalt": "teasers",
            "image.interpolation": "antialiased",
        }
    )


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.svg"
    fig.savefig(path, dpi=220, metadata={"Date": None})
    plt.close(fig)
    print(f"wrote {path.relative_to(ROOT)}")


# --------------------------------------------------------------------------
# Contextual music recommendation
# --------------------------------------------------------------------------

ZENODO_CSV = (
    "https://zenodo.org/api/records/5552288/files/warm_12Labels.csv/content"
)


def refresh_context_counts():
    import pandas as pd

    tmp = Path("/tmp/warm_12Labels.csv")
    if not tmp.exists():
        print(f"downloading {ZENODO_CSV}")
        urllib.request.urlretrieve(ZENODO_CSV, tmp)
    streams = pd.read_csv(tmp, usecols=["readable_time", "matches"])
    counts = pd.crosstab(streams.matches, streams.readable_time)
    counts.index.name = "situation"
    counts.to_csv(DATA / "situation_hour_counts.csv")


def load_context_counts():
    raw = np.genfromtxt(
        DATA / "situation_hour_counts.csv", delimiter=",", dtype=str
    )
    names = list(raw[1:, 0])
    counts = raw[1:, 1:].astype(float)
    return names, counts


def context_teaser():
    """When each listening situation is streamed, by hour of day.

    Streams on Deezer (France and Brazil, August 2019) labelled with a
    listening situation through playlist titles: the ISMIR 2022 dataset.
    """
    names, counts = load_context_counts()
    share = counts / counts.sum(axis=1, keepdims=True) * 100

    # Order rows by circular mean hour so the daily progression reads
    # top-to-bottom, starting from the early morning.
    angle = np.arange(24) / 24 * 2 * np.pi
    mean_hour = (
        np.angle((share * np.exp(1j * angle)).sum(axis=1)) / (2 * np.pi) * 24
    ) % 24
    order = np.argsort((mean_hour - 4) % 24)
    share = share[order]
    names = [names[i] for i in order]

    fig = plt.figure(figsize=FIG_SIZE)
    ax = fig.add_axes([0.14, 0.19, 0.73, 0.69])
    cax = fig.add_axes([0.9, 0.19, 0.018, 0.69])

    mesh = ax.pcolormesh(
        np.arange(25),
        np.arange(len(names) + 1),
        share,
        cmap=SEQ,
        vmin=0,
        vmax=11,
        edgecolors="white",
        linewidth=0.6,
    )
    ax.set_ylim(len(names), 0)
    ax.set_yticks(np.arange(len(names)) + 0.5, [n.capitalize() for n in names])
    ax.tick_params(axis="y", length=0, pad=4, labelsize=7.5, labelcolor=INK)
    ax.set_xticks([0, 6, 12, 18, 24], ["00:00", "06:00", "12:00", "18:00", "24:00"])
    ax.set_xlabel("Hour of day (local time)", labelpad=3)
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(False)
    ax.set_title("When each listening situation is streamed", x=-0.155)

    cb = fig.colorbar(mesh, cax=cax, ticks=[0, 5, 10])
    cb.outline.set_visible(False)
    cb.ax.tick_params(length=0, labelsize=7, pad=2)
    cb.ax.set_yticklabels(["0", "5", "10%"])
    save(fig, "context-teaser")


# --------------------------------------------------------------------------
# Primary-ambient extraction
# --------------------------------------------------------------------------

FS = 16000
AMBIENT_LEVEL = 0.3


def _pluck(freq, dur, rng):
    t = np.arange(int(dur * FS)) / FS
    note = np.zeros_like(t)
    for k in range(1, 9):
        decay = np.exp(-t * (12 + 3 * k))
        note += decay * np.sin(2 * np.pi * k * freq * t + rng.uniform(0, 2 * np.pi)) / k**0.7
    return note * np.minimum(1, t / 0.003)


def _synthetic_stereo(rng):
    """Short dry notes, amplitude-panned, plus a decorrelated reverb."""
    dur = 4.0
    dry = np.zeros(int(dur * FS))
    melody = [
        (0.15, 196.0), (0.50, 246.9), (0.85, 293.7), (1.20, 392.0),
        (1.90, 329.6), (2.25, 293.7), (2.60, 246.9), (2.95, 220.0),
    ]
    for onset, f0 in melody:
        note = _pluck(f0, 0.5, rng)
        i = int(onset * FS)
        n = min(len(note), len(dry) - i)
        dry[i:i + n] += note[:n]
    dry /= np.abs(dry).max()

    # Primary: the same dry signal in both channels, panned right of centre.
    primary = np.stack([0.55 * dry, 0.85 * dry])

    # Ambient: independent exponentially decaying noise per channel makes the
    # left/right reverb mutually uncorrelated, as assumed by PCA-based PAE.
    rt60 = 2.0
    t_ir = np.arange(int(rt60 * FS)) / FS
    envelope = np.exp(-6.9 * t_ir / rt60) * np.minimum(1, t_ir / 0.03)
    envelope *= np.exp(-t_ir * 1.5)
    ambient = np.stack(
        [
            fftconvolve(dry, rng.standard_normal(len(t_ir)) * envelope)[: len(dry)]
            for _ in range(2)
        ]
    )
    ambient *= AMBIENT_LEVEL * np.abs(primary).max() / np.abs(ambient).max()
    return primary, ambient


def pca_pae(stereo, nperseg=1024, hop=256, context=4, threshold=0.9):
    """Adaptive-weighting PCA primary-ambient extraction (SMC 2016).

    Per STFT bin, the 2x2 inter-channel covariance is estimated over
    2 * context + 1 adjacent frames. The primary estimate is the projection
    onto the dominant eigenvector, scaled by w = 1 - lambda2 / lambda1 and
    zeroed where w < threshold; the ambient estimate is the residual.
    """
    _, _, X = stft(stereo, FS, nperseg=nperseg, noverlap=nperseg - hop)
    x = np.moveaxis(X, 0, -1)  # bins, frames, channels
    outer = np.einsum("bfi,bfj->bfij", x, x.conj())
    padded = np.pad(outer, ((0, 0), (context, context), (0, 0), (0, 0)))
    csum = np.cumsum(padded, axis=1)
    csum = np.concatenate([np.zeros_like(csum[:, :1]), csum], axis=1)
    cov = csum[:, 2 * context + 1:] - csum[:, : -(2 * context + 1)]
    vals, vecs = np.linalg.eigh(cov + 1e-12 * np.eye(2))
    v = vecs[..., -1]
    w = 1 - vals[..., 0] / np.maximum(vals[..., 1], 1e-12)
    w = np.where(w > threshold, w, 0.0)
    proj = np.einsum("bfi,bfi->bf", v.conj(), x)
    P = np.moveaxis(v * (w * proj)[..., None], -1, 0)
    A = X - P
    _, p = istft(P, FS, nperseg=nperseg, noverlap=nperseg - hop)
    _, a = istft(A, FS, nperseg=nperseg, noverlap=nperseg - hop)
    return p[:, : stereo.shape[1]], a[:, : stereo.shape[1]]


def _spec_db(x, nperseg=256, hop=64):
    f, t, Z = stft(x, FS, nperseg=nperseg, noverlap=nperseg - hop)
    return f, t, 20 * np.log10(np.abs(Z) + 1e-6)


def pae_teaser():
    """Stereo mix, PCA primary estimate and PCA ambient estimate.

    Illustrative: runs the PCA extraction on a synthetic stereo recording
    (no audio from the original studies is in the repository).
    """
    rng = np.random.default_rng(7)
    mix = sum(_synthetic_stereo(rng))
    primary, ambient = pca_pae(mix)

    rows = [
        ("Stereo mix", "input", mix[0]),
        ("Primary", "direct sound", primary[0]),
        ("Ambient", "diffuse reverb", ambient[0]),
    ]
    specs = [_spec_db(x) for _, _, x in rows]
    ref = max(s[2].max() for s in specs)
    fmax = 3500

    fig, axes = plt.subplots(
        3, 1, figsize=FIG_SIZE, sharex=True,
        gridspec_kw={"left": 0.2, "right": 0.91, "top": 0.97, "bottom": 0.165, "hspace": 0.14},
    )
    for ax, (label, sub, _), (f, t, S) in zip(axes, rows, specs):
        keep = f <= fmax
        ax.imshow(
            np.clip(S[keep] - ref, -45, 0),
            origin="lower", aspect="auto", cmap=SEQ, vmin=-45, vmax=0,
            extent=[t[0], t[-1], 0, fmax / 1000],
        )
        ax.text(-0.025, 0.62, label, transform=ax.transAxes, ha="right", va="center",
                fontsize=8.5, fontweight="semibold", color=INK)
        ax.text(-0.025, 0.3, sub, transform=ax.transAxes, ha="right", va="center",
                fontsize=7, color=MUTED)
        ax.yaxis.tick_right()
        ax.set_yticks([1, 3], ["1", "3 kHz"])
        ax.tick_params(axis="y", labelsize=6.5, pad=2, length=0)
        ax.tick_params(axis="x", length=0)
        for side in ("left", "bottom"):
            ax.spines[side].set_visible(False)
    axes[-1].set_xlabel("Time (s)", labelpad=3)
    axes[-1].set_xlim(0, 4)
    save(fig, "pae-teaser")


# --------------------------------------------------------------------------
# Singing voice intelligibility
# --------------------------------------------------------------------------

# ISMIR 2017, Fig. 2: leave-one-out SVM confusion matrix on 100 excerpts.
# Rows are listener-rated classes (43 / 42 / 15 excerpts), columns predictions.
IOSL_CONFUSION = np.array([[33, 9, 1], [10, 30, 2], [4, 8, 3]])
# ISMIR 2017, Table 1: classification accuracy per genre.
IOSL_GENRE_ACC = {"Classical": 70, "Pop/Rock": 60, "Jazz": 60, "Folk": 55, "R&B": 55}
IOSL_OVERALL_ACC = 66


def singing_teaser():
    """Predicting lyric intelligibility from acoustic features (ISMIR 2017)."""
    fig = plt.figure(figsize=FIG_SIZE)
    ax_cm = fig.add_axes([0.205, 0.2, 0.3, 0.64])
    ax_g = fig.add_axes([0.695, 0.2, 0.275, 0.64])
    title_y = 0.92

    classes = ["High", "Moderate", "Low"]
    cm = IOSL_CONFUSION
    rate = cm / cm.sum(axis=1, keepdims=True)
    ax_cm.pcolormesh(
        np.arange(4), np.arange(4), rate, cmap=SEQ, vmin=0, vmax=1,
        edgecolors="white", linewidth=1.5,
    )
    for i in range(3):
        for j in range(3):
            ax_cm.text(
                j + 0.5, i + 0.5, str(cm[i, j]), ha="center", va="center",
                fontsize=8.5, fontweight="semibold" if i == j else "normal",
                color="white" if rate[i, j] > 0.5 else INK,
            )
    ax_cm.set_xlim(0, 3)
    ax_cm.set_ylim(3, 0)
    ax_cm.set_xticks(np.arange(3) + 0.5, classes)
    ax_cm.set_yticks(np.arange(3) + 0.5, classes)
    ax_cm.tick_params(length=0, labelcolor=INK, pad=3)
    ax_cm.set_xlabel("Predicted", labelpad=4)
    ax_cm.set_ylabel("Listener-rated", labelpad=4)
    for side in ("left", "bottom"):
        ax_cm.spines[side].set_visible(False)
    fig.text(0.025, title_y, "Predicted intelligibility (n = 100)",
             fontsize=9, fontweight="semibold", color=INK)

    genres = list(IOSL_GENRE_ACC)
    acc = [IOSL_GENRE_ACC[g] for g in genres]
    y = np.arange(len(genres))
    ax_g.barh(y, acc, height=0.58, color=TEAL, zorder=2)
    ax_g.axvline(IOSL_OVERALL_ACC, color=NAVY, lw=1, ls=(0, (3, 2)), zorder=3)
    ax_g.text(
        IOSL_OVERALL_ACC + 2, -0.62, f"all {IOSL_OVERALL_ACC}%",
        fontsize=7, color=NAVY, va="center", ha="left",
    )
    for yi, a in zip(y, acc):
        ax_g.text(a - 2, yi, f"{a}%", va="center", ha="right", fontsize=7, color="white", zorder=4)
    ax_g.set_yticks(y, genres)
    ax_g.set_ylim(len(genres) - 0.45, -0.9)
    ax_g.set_xlim(0, 100)
    ax_g.set_xticks([0, 50, 100], ["0", "50", "100%"])
    ax_g.tick_params(axis="y", length=0, labelcolor=INK, pad=3)
    ax_g.spines["left"].set_visible(False)
    ax_g.grid(axis="x", color=FAINT, lw=0.8, zorder=0)
    ax_g.set_xlabel("Accuracy", labelpad=3)
    fig.text(0.575, title_y, "Accuracy by genre", fontsize=9, fontweight="semibold", color=INK)
    save(fig, "singing-teaser")


# --------------------------------------------------------------------------
# Speech emotion recognition
# --------------------------------------------------------------------------

# ICASSP 2024, Table 2: accuracy (%) with 95% CI over 5-fold cross-validation
# of wav2vec 2.0. SD / SI = speaker dependent / speaker independent splits.
ORIG, AUG, CONV = "Original data", "+ Audio augmentation", "+ Emotion conversion"
SER_RESULTS = {
    ("IEMOCAP", "seen speakers"): {ORIG: (74.16, 2.00), AUG: (74.17, 1.37), CONV: (76.19, 1.95)},
    ("IEMOCAP", "new speakers"): {ORIG: (63.97, 2.93), AUG: (65.32, 3.44), CONV: (66.06, 2.21)},
    ("RAVDESS", "seen speakers"): {ORIG: (91.08, 2.93), AUG: (92.71, 2.20), CONV: (93.05, 2.12)},
    ("RAVDESS", "new speakers"): {ORIG: (81.01, 3.19), AUG: (82.29, 2.96), CONV: (81.29, 2.77)},
}


def ser_teaser():
    """wav2vec 2.0 accuracy with and without emotion-conversion augmentation."""
    fig = plt.figure(figsize=FIG_SIZE)
    ax = fig.add_axes([0.25, 0.22, 0.72, 0.64])

    setups = [ORIG, AUG, CONV]
    style = {
        ORIG: dict(color=NEUTRAL, marker="o", ms=4.5, mfc="white", mew=1.2),
        AUG: dict(color=NEUTRAL, marker="s", ms=4, mew=0),
        CONV: dict(color=NAVY, marker="D", ms=4.5, mew=0),
    }
    offsets = {ORIG: -0.2, AUG: 0.0, CONV: 0.2}

    groups = list(SER_RESULTS)
    for gi, g in enumerate(groups):
        dataset = g[0]
        if gi % 2 == 0:
            ax.axhspan(gi - 0.5, gi + 1.5, color="#f5f7fa", zorder=0, lw=0)
            ax.text(-0.235, 1 - (gi + 1) / len(groups), dataset, transform=ax.transAxes,
                    ha="left", va="center", fontsize=8.5, fontweight="semibold", color=INK)
        for s in setups:
            mean, ci = SER_RESULTS[g][s]
            st = style[s]
            ax.errorbar(
                mean, gi + offsets[s], xerr=ci, fmt=st["marker"], color=st["color"],
                ms=st["ms"], mfc=st.get("mfc", st["color"]), mec=st["color"],
                mew=st["mew"] or 0, elinewidth=1, capsize=0, zorder=3,
                label=s if gi == 0 else None,
            )
    ax.set_yticks(np.arange(len(groups)), [split for _, split in groups])
    ax.set_ylim(len(groups) - 0.5, -0.5)
    ax.set_xlim(58, 97)
    ax.set_xticks([60, 70, 80, 90], ["60", "70", "80", "90%"])
    ax.tick_params(axis="y", length=0, labelcolor=MUTED, labelsize=7, pad=4)
    ax.spines["left"].set_visible(False)
    ax.grid(axis="x", color=FAINT, lw=0.8, zorder=1)
    ax.set_axisbelow(True)
    ax.set_xlabel("Emotion recognition accuracy (mean, 95% CI)", labelpad=3)
    leg = ax.legend(
        loc="lower left", bbox_to_anchor=(-0.235, 1.03), ncol=3, frameon=False,
        fontsize=7.5, handletextpad=0.3, columnspacing=1.0, borderaxespad=0,
    )
    for text in leg.get_texts():
        if text.get_text() == CONV:
            text.set_color(NAVY)
            text.set_fontweight("semibold")
    save(fig, "ser-teaser")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh-context", action="store_true")
    args = parser.parse_args()
    if args.refresh_context:
        refresh_context_counts()
    setup_style()
    context_teaser()
    pae_teaser()
    singing_teaser()
    ser_teaser()


if __name__ == "__main__":
    main()
