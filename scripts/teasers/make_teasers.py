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
from matplotlib.colors import to_rgb
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle
from matplotlib.textpath import TextPath

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
FLOOR = "#f6f8fb"

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
# Singing voice intelligibility: one lyric line at three intelligibility levels
# --------------------------------------------------------------------------

LYRIC = "every word you sing"
GLYPHS = "DejaVu Sans"  # Inter has no music-note glyphs


def text_width(s, size, weight="normal"):
    """Advance width of a string in canvas units (1 unit = 0.72 pt)."""
    if not s:
        return 0.0
    prop = FontProperties(family="Inter", weight=weight)
    probe = TextPath((0, 0), s + "|", size=size, prop=prop).get_extents().x1
    bar = TextPath((0, 0), "|", size=size, prop=prop).get_extents().x1
    return (probe - bar) / 0.72


def pill(ax, x, y, label, color, w=62, h=24, size=8.5):
    box(ax, x - w / 2, y - h / 2, w, h, fc=tint(color, 0.85), ec=tint(color, 0.35), radius=h / 2)
    ax.text(x, y, label, ha="center", va="center", fontsize=size, fontweight="semibold",
            color=shade(color, 0.35), zorder=4)


def singer_side(ax, x, y, color=NAVY, s=1.0):
    """Standing singer facing right holding a microphone; (x, y) = feet centre."""
    ax.add_patch(FancyBboxPatch((x - 14 * s, y), 28 * s, 52 * s,
                                boxstyle=f"round,pad=0,rounding_size={11 * s}", fc=color, ec="none", zorder=3))
    ax.add_patch(Circle((x + 1 * s, y + 66 * s), 11 * s, fc=color, ec="none", zorder=3))
    ax.plot([x + 8 * s, x + 19 * s], [y + 36 * s, y + 55 * s], color=color, lw=4 * s,
            solid_capstyle="round", zorder=3)
    ax.plot([x + 19 * s, x + 23 * s], [y + 55 * s, y + 62 * s], color=INK, lw=2.4 * s,
            solid_capstyle="round", zorder=4)
    ax.add_patch(Circle((x + 24.5 * s, y + 64.5 * s), 3.6 * s, fc=INK, ec="none", zorder=4))
    return (x + 30 * s, y + 66 * s)


def singing_teaser():
    rng = np.random.default_rng(1)
    fig, ax = canvas()
    mouth = singer_side(ax, 42, 44, s=1.05)
    ax.add_patch(Rectangle((14, 40), 76, 4, fc=RULE, ec="none", zorder=2))

    x0, size = 118, 12
    rows = [(164, "High", TEAL), (110, "Medium", OCHRE), (56, "Low", BRICK)]
    for y, label, color in rows:
        ax.add_patch(FancyArrowPatch(mouth, (x0 - 8, y), arrowstyle="-", color=RULE, lw=0.9,
                                     ls=(0, (2, 2)), zorder=2))
        pill(ax, 400, y, label, color)

    # High: crisp.
    ax.text(x0, 164, LYRIC, fontsize=size, fontweight="semibold", color=INK, va="center")

    # Medium: a faint offset copy behind the line reads as smudged.
    ax.text(x0 + 1.4, 110 - 1.2, LYRIC, fontsize=size, fontweight="semibold", color=tint(INK, 0.72),
            va="center", zorder=3)
    ax.text(x0, 110, LYRIC, fontsize=size, fontweight="semibold", color=tint(INK, 0.3), va="center", zorder=4)

    # Low: letters drift and fade, then turn into music notes.
    n = len(LYRIC)
    for i, ch in enumerate(LYRIC):
        k = i / (n - 1)
        x = x0 + text_width(LYRIC[:i], size, "semibold")
        if ch == " ":
            continue
        if k < 0.62:
            ax.text(x, 56 + rng.uniform(-3, 3) * k * 2, ch, fontsize=size, fontweight="semibold",
                    va="center", color=tint(INK, 0.35 + 0.5 * k), rotation=rng.uniform(-25, 25) * k,
                    zorder=3)
        else:
            glyph = "♪" if rng.random() < 0.6 else "♫"
            ax.text(x + 2, 58 + (k - 0.6) * 28 + rng.uniform(-4, 4), glyph, fontsize=10 + 3 * rng.random(),
                    color=tint(BRICK, 0.1 + 0.5 * (k - 0.6)), rotation=rng.uniform(-20, 20),
                    ha="center", va="center", fontfamily=GLYPHS, zorder=4)
    save(fig, "singing-teaser")


# --------------------------------------------------------------------------
# Primary-ambient extraction: direct sound and hall reflections pulled apart
# --------------------------------------------------------------------------


def person_top(ax, x, y, facing=90, color=NAVY, s=1.0):
    """Person seen from above; facing is the direction of the nose in degrees."""
    th = np.deg2rad(facing)
    fwd = np.array([np.cos(th), np.sin(th)])
    ax.add_patch(Ellipse((x, y) - fwd * 1.5 * s, 28 * s, 12 * s, angle=facing - 90,
                         fc=tint(color, 0.6), ec="none", zorder=4))
    tip = fwd * 9.5 * s + [x, y]
    side = np.array([-fwd[1], fwd[0]]) * 2.4 * s
    base = fwd * 5 * s + [x, y]
    ax.add_patch(Polygon([tip, base + side, base - side], fc=color, ec="none", zorder=5))
    ax.add_patch(Circle((x, y), 6 * s, fc=color, ec="none", zorder=5))


def _mirror(p, wall, value):
    return (p[0], 2 * value - p[1]) if wall == "y" else (2 * value - p[0], p[1])


def _hit(a, b, wall, value):
    i = 1 if wall == "y" else 0
    t = (value - a[i]) / (b[i] - a[i])
    return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))


def reflection_paths(src, dst, x0, y0, x1, y1):
    """Image-source paths off each side wall, and side wall then back wall."""
    paths = []
    for wall in (("y", y1), ("y", y0)):
        img = _mirror(src, *wall)
        paths.append([src, _hit(dst, img, *wall), dst])
        img2 = _mirror(img, "x", x1)
        p2 = _hit(dst, img2, "x", x1)
        paths.append([src, _hit(p2, img, *wall), p2, dst])
    return paths


def dashed_path(ax, pts, color, lw=1.0):
    pts = np.asarray(pts, float)
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, ls=(0, (3, 2.2)), zorder=3)
    ax.add_patch(FancyArrowPatch(tuple(pts[-2] + (pts[-1] - pts[-2]) * 0.8), tuple(pts[-1]),
                                 arrowstyle="-|>", mutation_scale=6, color=color, lw=0,
                                 shrinkA=0, shrinkB=0, zorder=3))


def hall(ax, x0, y0, x1, y1, singer, listener, direct=True, ambient=True, s=1.0):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=FLOOR, ec=SLATE, lw=1.3, zorder=1))
    ax.add_patch(Rectangle((x0, y0), (x1 - x0) * 0.2, y1 - y0, fc=tint(OCHRE, 0.86), ec="none", zorder=1.5))
    if ambient:
        for path in reflection_paths(singer, listener, x0, y0, x1, y1):
            dashed_path(ax, path, TEAL, lw=1.0 * s)
    if direct:
        ax.add_patch(FancyArrowPatch((singer[0] + 11 * s, singer[1]), (listener[0] - 12 * s, listener[1]),
                                     arrowstyle="-|>", mutation_scale=10 * s, color=NAVY, lw=2.4 * s,
                                     shrinkA=0, shrinkB=0, zorder=4))
    person_top(ax, *singer, facing=0, color=NAVY, s=s)
    person_top(ax, *listener, facing=180, color=INK, s=s)


def heading(ax, x, y, title, sub, color=INK, size=9):
    ax.text(x, y, title, fontsize=size, fontweight="semibold", va="center", color=color)
    ax.text(x + text_width(title, size, "semibold") + 5, y, sub, fontsize=7.5, va="center", color=MUTED)


def pae_teaser():
    fig, ax = canvas()
    heading(ax, 14, 204, "In the hall", "voice and room arrive together")
    hall(ax, 14, 22, 222, 190, (44, 106), (184, 100))

    arrow(ax, (230, 146), (254, 160), color=NAVY)
    arrow(ax, (230, 66), (254, 52), color=shade(TEAL, 0.1))

    heading(ax, 262, 204, "Primary", "direct sound", color=NAVY)
    hall(ax, 262, 122, 428, 192, (284, 157), (398, 155), ambient=False, s=0.7)
    heading(ax, 262, 106, "Ambient", "reflections", color=shade(TEAL, 0.2))
    hall(ax, 262, 22, 428, 92, (284, 57), (398, 55), direct=False, s=0.7)
    save(fig, "pae-teaser")


def main():
    setup_style()
    ser_teaser()
    context_teaser()
    singing_teaser()
    pae_teaser()


if __name__ == "__main__":
    main()
