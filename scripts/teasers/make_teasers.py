"""Generate the project teaser illustrations shown on /projects/.

    python scripts/teasers/make_teasers.py    # writes images/teasers/*.svg

Each teaser is drawn on a 440 x 220 unit canvas (1 unit = 0.01 in) so that
layout coordinates below map directly onto the 2:1 card image.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap, to_rgb
from matplotlib.patches import Ellipse, FancyArrowPatch, FancyBboxPatch, Rectangle
from scipy.signal import fftconvolve, istft, stft

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "images" / "teasers"

# Card teasers are displayed at a 2:1 aspect ratio (see .archive__item-teaser
# in _sass/_custom.scss).
W, H = 440, 220

# Site palette (_sass/_variables.scss) plus three muted accents.
INK = "#1e293b"
MUTED = "#64748b"
RULE = "#cbd5e1"
NAVY = "#1d3557"
TEAL = "#0891b2"
STEEL = "#3f6f9e"
BRICK = "#b4583f"
OCHRE = "#c0902f"
VIOLET = "#6e69a3"
SLATE = "#8c98aa"

SEQ = LinearSegmentedColormap.from_list(
    "site_seq", ["#ffffff", "#cfe9f0", TEAL, NAVY], N=256
)


def tint(color, amount):
    """Mix a colour with white; amount=1 gives white."""
    r, g, b = to_rgb(color)
    return (r + (1 - r) * amount, g + (1 - g) * amount, b + (1 - b) * amount)


def shade(color, amount):
    """Mix a colour with black; amount=1 gives black."""
    r, g, b = to_rgb(color)
    return (r * (1 - amount), g * (1 - amount), b * (1 - amount))


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
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
            "svg.fonttype": "path",
            "svg.hashsalt": "teasers",
            "image.interpolation": "antialiased",
        }
    )


def canvas():
    fig = plt.figure(figsize=(W / 100, H / 100))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_axis_off()
    return fig, ax


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.svg"
    fig.savefig(path, dpi=220, metadata={"Date": None})
    plt.close(fig)
    print(f"wrote {path.relative_to(ROOT)}")


def box(ax, x, y, w, h, fc="white", ec=RULE, lw=0.9, radius=5):
    ax.add_patch(
        FancyBboxPatch(
            (x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}",
            fc=fc, ec=ec, lw=lw, zorder=2,
        )
    )


def arrow(ax, start, end, color=MUTED):
    ax.add_patch(
        FancyArrowPatch(
            start, end, arrowstyle="-|>", mutation_scale=7, color=color,
            lw=0.9, shrinkA=0, shrinkB=0, zorder=3,
        )
    )


def waveform_bars(ax, x0, x1, y, envelope, color, half_height, rng, n_bars=None):
    """Audio-editor style waveform: one rounded vertical bar per column."""
    n = n_bars or int((x1 - x0) / 1.9)
    xs = np.linspace(x0, x1, n)
    amp = envelope(np.linspace(0, 1, n)) * (0.55 + 0.45 * rng.random(n))
    amp = np.maximum(amp, 0.03)
    ax.vlines(xs, y - amp * half_height, y + amp * half_height, color=color,
              lw=1.0, capstyle="round", zorder=3)


def bumps(t, centers, widths, heights, attack=1.0):
    """Sum of asymmetric syllable-like envelopes."""
    env = np.zeros_like(t)
    for c, w, h in zip(centers, widths, heights):
        rise = np.exp(-0.5 * ((t - c) / (w * attack)) ** 2)
        fall = np.exp(-0.5 * ((t - c) / w) ** 2)
        env += h * np.where(t < c, rise, fall)
    return np.minimum(env, 1.0)


# --------------------------------------------------------------------------
# Speech emotion recognition: the same utterance in five emotions
# --------------------------------------------------------------------------


def ser_teaser():
    rng = np.random.default_rng(3)
    fig, ax = canvas()

    def syllables(n, start, end, jitter, widths, heights):
        c = np.linspace(start, end, n) + rng.uniform(-jitter, jitter, n)
        return c, np.full(n, widths), heights

    angry = syllables(11, 0.05, 0.95, 0.015, 0.03, rng.uniform(0.8, 1.0, 11))
    happy = syllables(9, 0.06, 0.92, 0.02, 0.035, 0.55 + 0.25 * np.sin(np.linspace(0, 3 * np.pi, 9)) ** 2)
    sad = (np.array([0.1, 0.32, 0.54, 0.76]), np.full(4, 0.04), np.array([0.36, 0.3, 0.24, 0.16]))
    fear_c = np.array([0.06, 0.13, 0.2, 0.42, 0.48, 0.55, 0.62, 0.84, 0.9])
    fear = (fear_c, np.full(9, 0.028), rng.uniform(0.35, 0.7, 9))
    neutral = syllables(8, 0.07, 0.9, 0.01, 0.04, np.full(8, 0.42))

    rows = [
        ("Angry", BRICK, lambda t: bumps(t, *angry, attack=0.5)),
        ("Happy", OCHRE, lambda t: bumps(t, *happy)),
        ("Sad", STEEL, lambda t: bumps(t, *sad, attack=1.3)),
        ("Fearful", VIOLET, lambda t: bumps(t, *fear) * (0.75 + 0.25 * np.sin(2 * np.pi * 38 * t))),
        ("Neutral", SLATE, lambda t: bumps(t, *neutral)),
    ]
    ys = np.linspace(186, 34, len(rows))
    for (label, color, env), y in zip(rows, ys):
        ax.text(20, y, label, ha="left", va="center", fontsize=9.5, fontweight="semibold", color=INK)
        ax.hlines(y, 96, 424, color=tint(color, 0.7), lw=0.6, zorder=2)
        waveform_bars(ax, 96, 424, y, env, color, half_height=15, rng=rng)
    save(fig, "ser-teaser")


# --------------------------------------------------------------------------
# Contextual music recommendation: tracks grouped by listening context
# --------------------------------------------------------------------------


def context_teaser():
    rng = np.random.default_rng(11)
    fig, ax = canvas()

    clusters = [
        # label, colour, centre, spread (major, minor), angle, label position, alignment
        ("Workout", BRICK, (150, 148), (30, 20), 70, (118, 150), "right"),
        ("Party", VIOLET, (292, 150), (38, 20), 15, (344, 162), "left"),
        ("Sleep / Relax", STEEL, (78, 84), (38, 17), 10, (80, 44), "center"),
        ("Focus / Study", TEAL, (212, 68), (26, 20), 0, (212, 26), "center"),
        ("Commute", OCHRE, (358, 80), (36, 18), 30, (366, 40), "center"),
    ]
    for label, color, (cx, cy), (a, b), angle, (lx, ly), ha in clusters:
        n = 170
        pts = np.clip(rng.standard_normal((n, 2)), -2.2, 2.2) * [a / 2, b / 2]
        th = np.deg2rad(angle)
        rot = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
        pts = pts @ rot.T + [cx, cy]
        ax.add_patch(Ellipse((cx, cy), 2.3 * a, 2.3 * b, angle=angle, fc=tint(color, 0.9),
                             ec=tint(color, 0.6), lw=0.7, zorder=2))
        ax.scatter(pts[:, 0], pts[:, 1], s=4.5, color=color, alpha=0.85, lw=0, zorder=3)
        ax.text(lx, ly, label, ha=ha, va="center", fontsize=9.5, fontweight="semibold",
                color=shade(color, 0.2), zorder=4)
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    save(fig, "context-teaser")


# --------------------------------------------------------------------------
# Singing voice intelligibility: features -> SVM -> intelligibility class
# --------------------------------------------------------------------------


def singing_teaser():
    rng = np.random.default_rng(5)
    fig, ax = canvas()
    mid = 110

    # Input
    box(ax, 10, 78, 80, 64)
    t_env = lambda t: bumps(t, np.linspace(0.1, 0.9, 5), np.full(5, 0.07), [0.5, 0.9, 0.7, 1.0, 0.6])
    waveform_bars(ax, 28, 72, 122, t_env, NAVY, half_height=9, rng=rng, n_bars=20)
    ax.text(50, 96, "Singing voice", ha="center", va="center", fontsize=8.5, fontweight="semibold")

    # Features (ISMIR 2017, Sec. 4.2)
    arrow(ax, (90, mid), (108, mid))
    box(ax, 108, 36, 146, 148)
    ax.text(120, 168, "Acoustic features", ha="left", va="center", fontsize=8.5, fontweight="semibold")
    ax.hlines(156, 120, 242, color=RULE, lw=0.7, zorder=3)
    features = [
        "Vocal-to-music ratio",
        "Harmonics-to-residual",
        "High-frequency energy",
        "Syllable rate",
        "MFCCs",
    ]
    for i, f in enumerate(features):
        y = 141 - i * 22
        ax.add_patch(Rectangle((120, y - 2), 4, 4, fc=TEAL, ec="none", zorder=3))
        ax.text(131, y, f, ha="left", va="center", fontsize=7.8, color=INK)

    # Classifier
    arrow(ax, (254, mid), (270, mid))
    box(ax, 270, 84, 64, 52, fc=tint(NAVY, 0.92), ec=tint(NAVY, 0.55))
    ax.text(302, 116, "SVM", ha="center", va="center", fontsize=9.5, fontweight="semibold", color=NAVY)
    ax.text(302, 100, "classifier", ha="center", va="center", fontsize=7.5, color=MUTED)

    # Outputs
    ax.text(394, 192, "Intelligibility", ha="center", va="center", fontsize=7.5, color=MUTED)
    outputs = [("High", TEAL, 164), ("Medium", OCHRE, mid), ("Low", BRICK, 56)]
    jx = 347
    ax.plot([334, jx], [mid, mid], color=MUTED, lw=0.9, zorder=3)
    ax.plot([jx, jx], [outputs[-1][2], outputs[0][2]], color=MUTED, lw=0.9, zorder=3,
            solid_capstyle="butt")
    for label, color, y in outputs:
        arrow(ax, (jx, y), (360, y))
        box(ax, 360, y - 15, 68, 30, fc=tint(color, 0.85), ec=tint(color, 0.35), radius=15)
        ax.text(394, y, label, ha="center", va="center", fontsize=8.5, fontweight="semibold",
                color=shade(color, 0.35))
    save(fig, "singing-teaser")


# --------------------------------------------------------------------------
# Primary-ambient extraction: stereo mix -> primary + ambient
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
    dry = np.zeros(int(4.0 * FS))
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

    primary = np.stack([0.55 * dry, 0.85 * dry])

    # Independent decaying noise per channel makes the left/right reverb
    # mutually uncorrelated, as assumed by PCA-based extraction.
    rt60 = 2.0
    t_ir = np.arange(int(rt60 * FS)) / FS
    envelope = np.exp(-6.9 * t_ir / rt60) * np.minimum(1, t_ir / 0.03) * np.exp(-t_ir * 1.5)
    ambient = np.stack(
        [fftconvolve(dry, rng.standard_normal(len(t_ir)) * envelope)[: len(dry)] for _ in range(2)]
    )
    ambient *= AMBIENT_LEVEL * np.abs(primary).max() / np.abs(ambient).max()
    return primary + ambient


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


def _spec_db(x, nperseg=256, hop=64, fmax=3500):
    f, _, Z = stft(x, FS, nperseg=nperseg, noverlap=nperseg - hop)
    return 20 * np.log10(np.abs(Z[f <= fmax]) + 1e-6)


def pae_teaser():
    rng = np.random.default_rng(7)
    mix = _synthetic_stereo(rng)
    primary, ambient = pca_pae(mix)
    specs = {
        "L": _spec_db(mix[0]), "R": _spec_db(mix[1]),
        "primary": _spec_db(primary[0]), "ambient": _spec_db(ambient[0]),
    }
    ref = max(s.max() for s in specs.values())

    fig, ax = canvas()

    def panel(key, x, y, w, h):
        ax.imshow(np.clip(specs[key] - ref, -45, 0), origin="lower", aspect="auto",
                  cmap=SEQ, vmin=-45, vmax=0, extent=[x, x + w, y, y + h], zorder=2)
        ax.add_patch(Rectangle((x, y), w, h, fc="none", ec=RULE, lw=0.8, zorder=3))

    def heading(x, y, title, sub):
        ax.text(x, y, title, ha="left", va="baseline", fontsize=9.5, fontweight="semibold")
        ax.text(x, y - 13, sub, ha="left", va="baseline", fontsize=7.5, color=MUTED)

    heading(12, 196, "Stereo mix", "left and right channels")
    ax.text(12, 142, "L", ha="left", va="center", fontsize=8, fontweight="semibold", color=MUTED)
    ax.text(12, 70, "R", ha="left", va="center", fontsize=8, fontweight="semibold", color=MUTED)
    panel("L", 26, 112, 160, 60)
    panel("R", 26, 40, 160, 60)

    arrow(ax, (196, 106), (234, 106), color=NAVY)
    ax.text(215, 115, "PCA", ha="center", va="baseline", fontsize=7.5, fontweight="semibold", color=NAVY)

    heading(246, 196, "Primary", "direct sound")
    panel("primary", 246, 124, 182, 44)
    heading(246, 98, "Ambient", "diffuse reverb")
    panel("ambient", 246, 26, 182, 44)
    save(fig, "pae-teaser")


def main():
    setup_style()
    ser_teaser()
    context_teaser()
    singing_teaser()
    pae_teaser()


if __name__ == "__main__":
    main()
