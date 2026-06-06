"""Render the Goalplz README demo GIF.

The source direction mirrors demo/goalplz-hyperframes/index.html: restrained,
terminal-like, and focused on the before/after behavior.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from PIL import Image, ImageDraw, ImageFont, ImageSequence


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "goalplz-demo.gif"

WIDTH = 960
HEIGHT = 540
FPS = 12
DURATION = 7.2
FRAME_COUNT = round(FPS * DURATION)

BG = "#0d1117"
PANEL = "#111827"
PANEL_HEAD = "#172033"
BORDER = "#2d3748"
TEXT = "#e5e7eb"
MUTED = "#9ca3af"
BLUE = "#60a5fa"
GREEN = "#34d399"
AMBER = "#fbbf24"
RED = "#f87171"

COMMAND = "fix the failing checkout tests and keep going until verified"
GOAL = "Reproduce the checkout failure, identify the root cause, and make the smallest safe change."
CHECKS = [
    "Scope: checkout failure only",
    "Constraint: do not skip or weaken tests",
    "Verify: failing test before and after",
    "Pause: failure cannot be reproduced",
]


def font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        r"C:\Windows\Fonts\CascadiaMono.ttf",
        r"C:\Windows\Fonts\consolab.ttf" if bold else r"C:\Windows\Fonts\consola.ttf",
        r"C:\Windows\Fonts\seguisb.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


FONT_TINY = font(12)
FONT_SMALL = font(14)
FONT_BODY = font(17)
FONT_BODY_BOLD = font(17, bold=True)
FONT_MONO = font(18)
FONT_TITLE = font(24, bold=True)
FONT_ARROW = font(30, bold=True)


def clamp(value: float, low: float = 0, high: float = 1) -> float:
    return max(low, min(high, value))


def ease(value: float) -> float:
    value = clamp(value)
    return 1 - (1 - value) ** 3


def progress(t: float, start: float, duration: float, fn: Callable[[float], float] = ease) -> float:
    return fn((t - start) / duration)


def rgba(color: str, alpha: float) -> tuple[int, int, int, int]:
    color = color.lstrip("#")
    return (
        int(color[0:2], 16),
        int(color[2:4], 16),
        int(color[4:6], 16),
        round(255 * clamp(alpha)),
    )


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    fnt: ImageFont.ImageFont,
    color: str = TEXT,
    alpha: float = 1,
    *,
    anchor: str | None = None,
) -> None:
    if alpha <= 0.001:
        return
    draw.text(xy, text, font=fnt, fill=rgba(color, alpha), anchor=anchor)


def text_width(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont) -> int:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont, max_width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split(" "):
        candidate = word if not current else f"{current} {word}"
        if text_width(draw, candidate, fnt) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def rounded(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    *,
    fill: str,
    alpha: float = 1,
    outline: str | None = BORDER,
    radius: int = 8,
    width: int = 1,
) -> None:
    if alpha <= 0.001:
        return
    draw.rounded_rectangle(
        xy,
        radius=radius,
        fill=rgba(fill, alpha),
        outline=rgba(outline, alpha) if outline else None,
        width=width,
    )


def card(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, title: str, alpha: float) -> None:
    if alpha <= 0.001:
        return
    rounded(draw, (x, y, x + w, y + h), fill=PANEL, alpha=alpha, radius=9)
    draw.rounded_rectangle(
        (x, y, x + w, y + 42),
        radius=9,
        fill=rgba(PANEL_HEAD, alpha),
        outline=rgba(BORDER, alpha),
        width=1,
    )
    draw.rectangle((x, y + 28, x + w, y + 42), fill=rgba(PANEL_HEAD, alpha))
    for i, color in enumerate([RED, AMBER, GREEN]):
        draw.ellipse((x + 18 + i * 17, y + 15, x + 28 + i * 17, y + 25), fill=rgba(color, alpha))
    draw_text(draw, (x + 82, y + 14), title, FONT_SMALL, MUTED, alpha)


def draw_header(draw: ImageDraw.ImageDraw, t: float) -> None:
    p = max(0.7, progress(t, -0.15, 0.35))
    draw_text(draw, (44, 30), "Goalplz", FONT_TITLE, TEXT, p)
    draw_text(draw, (44, 61), "rough prompt compiler for Codex Goal mode", FONT_SMALL, MUTED, p)

    rp = progress(t, 4.0, 0.45)
    rounded(draw, (790, 26, 916, 55), fill="#0d1b15", alpha=rp, outline=GREEN, radius=15)
    draw_text(draw, (853, 35), "READY_GOAL", FONT_TINY, GREEN, rp, anchor="ma")


def draw_input(draw: ImageDraw.ImageDraw, t: float) -> None:
    p = progress(t, -0.15, 0.4)
    x = 44 - round(18 * (1 - p))
    y = 110
    w = 370
    h = 270
    card(draw, x, y, w, h, "rough request", p)
    draw_text(draw, (x + 28, y + 72), "$ /goalplz", FONT_MONO, MUTED, p)

    typed = progress(t, 0.8, 1.45)
    command = COMMAND[: round(len(COMMAND) * typed)]
    cursor = "|" if int(t * 4) % 2 == 0 and t < 2.8 else ""
    cy = y + 118
    for i, line in enumerate(wrap(draw, command, FONT_MONO, w - 64)[:3]):
        suffix = cursor if i == len(wrap(draw, command, FONT_MONO, w - 64)[:3]) - 1 else ""
        draw_text(draw, (x + 28, cy + i * 31), line + suffix, FONT_MONO, TEXT, p)


def draw_arrow(draw: ImageDraw.ImageDraw, t: float) -> None:
    p = progress(t, 2.25, 0.3)
    draw_text(draw, (480, 239), "->", FONT_ARROW, BLUE, p, anchor="mm")


def draw_output(draw: ImageDraw.ImageDraw, t: float) -> None:
    p = progress(t, 2.45, 0.45)
    x = 528 + round(18 * (1 - p))
    y = 110
    w = 388
    h = 270
    card(draw, x, y, w, h, "compiled goal", p)

    line_p = [
        progress(t, 2.95, 0.35),
        progress(t, 3.25, 0.35),
        progress(t, 3.65, 0.35),
        progress(t, 3.85, 0.35),
        progress(t, 4.05, 0.35),
        progress(t, 4.25, 0.35),
    ]
    draw_text(draw, (x + 28, y + 72), "STATUS: READY_GOAL", FONT_BODY_BOLD, GREEN, p * line_p[0])

    gy = y + 105
    draw_text(draw, (x + 28, gy), "/goal", FONT_BODY_BOLD, BLUE, p * line_p[1])
    goal_lines = wrap(draw, GOAL, FONT_BODY, w - 105)
    for i, line in enumerate(goal_lines[:2]):
        draw_text(draw, (x + 90, gy + i * 25), line, FONT_BODY, TEXT, p * line_p[1])

    start_y = gy + 62
    for i, check in enumerate(CHECKS):
        draw_text(draw, (x + 30, start_y + i * 25), "-", FONT_BODY, MUTED, p * line_p[min(i + 2, len(line_p) - 1)])
        draw_text(draw, (x + 52, start_y + i * 25), check, FONT_SMALL, TEXT, p * line_p[min(i + 2, len(line_p) - 1)])


def draw_footer(draw: ImageDraw.ImageDraw, t: float) -> None:
    p = progress(t, 5.05, 0.45)
    draw.line((44, 425, 916, 425), fill=rgba(BORDER, p), width=1)
    draw_text(draw, (44, 456), "Rough prompt in. Scoped goal out.", FONT_BODY_BOLD, TEXT, p)
    draw_text(draw, (722, 456), "github.com/r2gul4r/goalplz", FONT_SMALL, BLUE, p)


def frame(index: int) -> Image.Image:
    t = index / FPS
    image = Image.new("RGBA", (WIDTH, HEIGHT), rgba(BG, 1))
    draw = ImageDraw.Draw(image)
    draw_header(draw, t)
    draw_input(draw, t)
    draw_arrow(draw, t)
    draw_output(draw, t)
    draw_footer(draw, t)
    return image.convert("RGB")


def quantize(image: Image.Image) -> Image.Image:
    return image.convert("P", palette=Image.Palette.ADAPTIVE, colors=64)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    frames = [quantize(frame(i)) for i in range(FRAME_COUNT)]
    frames[0].save(
        OUT,
        save_all=True,
        append_images=frames[1:],
        duration=round(1000 / FPS),
        loop=0,
        optimize=True,
        disposal=2,
    )

    saved = Image.open(OUT)
    durations = [f.info.get("duration", 0) for f in ImageSequence.Iterator(saved)]
    print(f"Wrote {OUT}")
    print(f"Saved frames: {len(durations)}")
    print(f"Duration: {sum(durations)} ms")
    print(f"Size: {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
