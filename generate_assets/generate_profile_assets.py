from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

W, H = 1200, 820
BG = (6, 9, 14)
CYAN = (0, 246, 255)
MAGENTA = (255, 46, 209)
TEXT = (230, 237, 243)
MUTED = (139, 150, 165)
GREEN = (57, 255, 20)


FONT_CACHE: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    key = (path, size)
    if key not in FONT_CACHE:
        FONT_CACHE[key] = ImageFont.truetype(path, size)
    return FONT_CACHE[key]


FONT_MONO = r"C:\Windows\Fonts\consola.ttf"
FONT_MONO_BOLD = r"C:\Windows\Fonts\consolab.ttf"
FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"


def add_glow(base: Image.Image, layer: Image.Image, radius: int = 10, alpha: float = 1.0) -> None:
    glow = layer.filter(ImageFilter.GaussianBlur(radius))
    if alpha != 1:
        a = glow.getchannel("A").point(lambda p: int(p * alpha))
        glow.putalpha(a)
    base.alpha_composite(glow)
    base.alpha_composite(layer)


def rounded_rect(draw: ImageDraw.ImageDraw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def gradient_text(base: Image.Image, xy, text: str, font_obj, left=(0, 246, 255), right=(255, 46, 209), stroke=2):
    x, y = xy
    mask = Image.new("L", base.size, 0)
    md = ImageDraw.Draw(mask)
    md.text((x, y), text, font=font_obj, fill=255, stroke_width=stroke, stroke_fill=255)
    grad = Image.new("RGBA", base.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    text_w = int(md.textlength(text, font=font_obj))
    for i in range(max(1, text_w)):
        t = i / max(1, text_w - 1)
        col = tuple(int(left[j] * (1 - t) + right[j] * t) for j in range(3)) + (255,)
        gd.line((x + i, y, x + i, y + 90), fill=col)
    glow_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    glow_layer.putalpha(mask)
    tint = Image.new("RGBA", base.size, (*CYAN, 90))
    glow_layer = Image.composite(tint, glow_layer, mask)
    add_glow(base, glow_layer, 9, .75)
    base.alpha_composite(Image.composite(grad, Image.new("RGBA", base.size, (0, 0, 0, 0)), mask))


def draw_circuit(draw: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int, color, alpha=90):
    random.seed(7)
    for _ in range(34):
        x = random.randint(x0, x1)
        y = random.randint(y0, y1)
        pts = [(x, y)]
        for _ in range(random.randint(2, 4)):
            x += random.choice([-1, 1]) * random.randint(35, 120)
            y += random.choice([-1, 0, 1]) * random.randint(0, 38)
            x = max(x0, min(x1, x))
            y = max(y0, min(y1, y))
            pts.append((x, y))
        draw.line(pts, fill=(*color, alpha), width=1)
        for px, py in pts[1::2]:
            draw.ellipse((px - 3, py - 3, px + 3, py + 3), fill=(*color, alpha + 20))


def draw_energy_ring(size, outer_angle: float, inner_angle: float) -> Image.Image:
    scale = 2
    sw, sh = size[0] * scale, size[1] * scale
    layer = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))

    def ribbon_points(
        cx: float,
        cy: float,
        rx: float,
        ry: float,
        rotation: float,
        wobble: float,
        twist: float,
        samples: int = 520,
    ) -> list[tuple[int, int]]:
        pts: list[tuple[int, int]] = []
        for i in range(samples + 1):
            t = i / samples
            local = math.tau * t
            a = local + rotation
            organic = math.sin(local * 2.25) * wobble
            organic += math.sin(local * 5.1 + 0.8) * wobble * 0.28
            x = cx + math.cos(a) * (rx + organic)
            y = cy + math.sin(a + math.sin(local * 1.4) * 0.045) * (ry + math.cos(local * 2.7) * twist)
            pts.append((int(x * scale), int(y * scale)))
        return pts

    def ring_color(t: float) -> tuple[int, int, int]:
        # Color belongs to the rotating ring segment, so the cyan/magenta boundary travels with the geometry.
        blend = 0.5 + 0.5 * math.sin(math.tau * (t - 0.06))
        return tuple(int(CYAN[i] * (1 - blend) + MAGENTA[i] * blend) for i in range(3))

    def draw_ribbon(points: list[tuple[int, int]], hot_offset: float, widths: tuple[int, int, int]) -> None:
        # Blurred continuous underpainting: no points, vertices, or node marks.
        for width, alpha, blur in [(widths[0], 42, 14), (widths[1], 76, 8), (widths[2], 122, 3)]:
            glow = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
            gd = ImageDraw.Draw(glow)
            for i in range(len(points) - 1):
                t = i / (len(points) - 2)
                gd.line((points[i], points[i + 1]), fill=(*ring_color(t), alpha), width=width * scale)
            layer.alpha_composite(glow.filter(ImageFilter.GaussianBlur(blur * scale)))

        # Hot inner ribbon, drawn as densely sampled connected curve segments with tapering opacity.
        core = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
        cd = ImageDraw.Draw(core)
        for i in range(len(points) - 1):
            t = i / (len(points) - 2)
            hot = 0.32 + 0.68 * (0.5 + 0.5 * math.sin((t - hot_offset) * math.tau * 2.0))
            width = int(widths[2] * 0.42 * scale)
            alpha = int(72 + 168 * hot)
            cd.line((points[i], points[i + 1]), fill=(*ring_color(t), alpha), width=max(2, width))
        layer.alpha_composite(core)

        highlight = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
        hd = ImageDraw.Draw(highlight)
        hd.line(points, fill=(230, 255, 255, 76), width=2 * scale, joint="curve")
        layer.alpha_composite(highlight.filter(ImageFilter.GaussianBlur(0.35 * scale)))

    # Outer ring: larger, thicker, counter-clockwise. Inner ring: tighter, thinner, clockwise and faster.
    outer_path = ribbon_points(600, 204, 372, 232, outer_angle, 18, 16)
    inner_path = ribbon_points(600, 204, 314, 185, inner_angle + 0.7, 10, 9)
    draw_ribbon(outer_path, (outer_angle % math.tau) / math.tau, (42, 27, 14))
    draw_ribbon(inner_path, (inner_angle % math.tau) / math.tau, (22, 14, 8))

    return layer.resize(size, Image.Resampling.LANCZOS)


def draw_hero_frame(phase: float, outer_angle: float | None = None, inner_angle: float | None = None) -> Image.Image:
    img = Image.new("RGBA", (W, H), (*BG, 255))
    draw = ImageDraw.Draw(img)

    # digital rain and lab haze
    for col in range(0, W, 28):
        for row in range(-20, H, 28):
            val = "1010" if (col + row) % 3 else "011"
            draw.text((col, row + int((phase * 15 + col) % 28)), val, fill=(0, 246, 255, 22), font=font(FONT_MONO, 12))
    for x, y, r, color, amp in [
        (210 + int(math.sin(phase) * 75), 150, 210, CYAN, 62),
        (920 + int(math.cos(phase * .9) * 80), 150, 230, MAGENTA, 58),
        (240 + int(math.sin(phase * .7) * 90), 650, 260, CYAN, 36),
        (930 + int(math.cos(phase * .8) * 90), 635, 250, MAGENTA, 38),
    ]:
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        gd.ellipse((x - r, y - r, x + r, y + r), fill=(*color, amp))
        img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(55)))

    # hero panel
    metal = (46, 51, 61, 190)
    rounded_rect(draw, (62, 52, 1138, 396), 30, (12, 18, 24, 206), metal, 8)
    for inset, alpha, width in [(18, 190, 3), (34, 125, 2), (50, 70, 1)]:
        border = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        bd = ImageDraw.Draw(border)
        bd.rounded_rectangle((62 + inset, 52 + inset, 1138 - inset, 396 - inset), radius=26, outline=(*CYAN, alpha), width=width)
        bd.rounded_rectangle((62 + inset, 52 + inset, 1138 - inset, 396 - inset), radius=26, outline=(*MAGENTA, alpha // 2), width=width)
        add_glow(img, border, 7, .7)

    circuit = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(circuit)
    draw_circuit(cd, 105, 105, 505, 330, CYAN, 70)
    draw_circuit(cd, 700, 105, 1095, 330, MAGENTA, 68)
    img.alpha_composite(circuit)
    if outer_angle is None:
        outer_angle = phase
    if inner_angle is None:
        inner_angle = phase * -2
    img.alpha_composite(draw_energy_ring((W, H), outer_angle, inner_angle))

    # terminal controls
    for i, c in enumerate([CYAN, MAGENTA, (120, 130, 145)]):
        x = 112 + i * 28
        rounded_rect(draw, (x, 91, x + 18, 109), 4, (8, 26, 31, 220), (*c, 120), 1)
        draw.ellipse((x + 6, 97, x + 12, 103), fill=(*c, 200))

    title = "Muhammad Aswab Khalil"
    title_font = font(FONT_BOLD, 58)
    tw = draw.textlength(title, font=title_font)
    gradient_text(img, ((W - tw) / 2, 145), title, title_font)
    draw.text((W / 2, 230), "Software Engineer | Flutter | MERN | Computer Vision + AI", fill=TEXT, font=font(FONT_BOLD, 22), anchor="mm")
    draw.text((W / 2, 282), "building production-ready mobile, web, and intelligent systems", fill=(150, 255, 255), font=font(FONT_MONO_BOLD, 17), anchor="mm")
    rounded_rect(draw, (390, 326, 810, 370), 22, (9, 22, 28, 215), (*CYAN, 150), 2)
    draw.text((600, 349), "aswab007-ops :: Lahore, Pakistan", fill=TEXT, font=font(FONT_MONO_BOLD, 14), anchor="mm")

    # mission strip
    draw.text((130, 440), "> Active Mission Profile:", fill=(183, 251, 255), font=font(FONT_MONO, 19))
    draw.text((130, 478), "I turn pixels, APIs, and models into real p_", fill=TEXT, font=font(FONT_MONO_BOLD, 29))
    badge_y = 520
    badges = [("PROFILE VIEWS", "4", 130, 180), ("MODE:", "BUILDER", 340, 205), ("BASE:", "LAHORE, PAKISTAN", 580, 285)]
    for label, value, x, bw in badges:
        rounded_rect(draw, (x, badge_y, x + bw, badge_y + 48), 2, (7, 17, 24, 208), (*CYAN, 90), 1)
        draw.text((x + 14, badge_y + 15), label, fill=TEXT, font=font(FONT_MONO_BOLD, 15))
        draw.text((x + bw - 20, badge_y + 15), value, fill=(196, 253, 255), font=font(FONT_MONO_BOLD, 15), anchor="ra")
    for i, c in enumerate([CYAN, MAGENTA, (80, 130, 145)]):
        draw.ellipse((560 + i * 42, 590, 573 + i * 42, 603), fill=(*c, 230))

    # lower terminal shell
    rounded_rect(draw, (38, 624, 1162, 805), 24, (4, 10, 13, 224), (35, 247, 255, 88), 2)
    draw.text((520, 668), "⚙ booting profile...", fill=(220, 247, 255), font=font(FONT_MONO_BOLD, 17), anchor="mm")
    lines = [
        ("▣ loading mobile systems.............", "done"),
        ("▤ loading full-stack architecture....", "done"),
        ("◉ loading computer vision models.....", "done"),
        ("◆ loading product instincts..........", "done"),
    ]
    y = 700
    for left, done in lines:
        draw.text((405, y), left, fill=TEXT, font=font(FONT_MONO, 17))
        draw.text((760, y), done, fill=GREEN, font=font(FONT_MONO_BOLD, 17))
        y += 25
    draw.text((250, 798), "✳ status: building things that look good, work hard, and survive real users", fill=(218, 253, 255), font=font(FONT_MONO, 15))
    return img.convert("P", palette=Image.ADAPTIVE, colors=192)


def make_hero_gif():
    total = 60
    frames = []
    for i in range(total):
        t = i / total
        # Static phase remains fixed; only the two ring layers rotate.
        outer = -math.tau * t
        inner = math.tau * 2 * t
        frame = draw_hero_frame(0, outer, inner).convert("RGBA").crop((0, 0, 1200, 420))
        frames.append(frame.convert("P", palette=Image.ADAPTIVE, colors=192))
    frames[0].save(ASSETS / "hero-banner.gif", save_all=True, append_images=frames[1:], duration=300, loop=0, optimize=True)


def draw_terminal_frame(chars: int, blink: bool) -> Image.Image:
    w, h = 1160, 310
    img = Image.new("RGBA", (w, h), (3, 8, 10, 255))
    draw = ImageDraw.Draw(img)
    pulse = 165 if blink else 112
    border_glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    bgd = ImageDraw.Draw(border_glow)
    bgd.rounded_rectangle((8, 8, w - 8, h - 8), radius=24, outline=(*CYAN, pulse), width=3)
    img.alpha_composite(border_glow.filter(ImageFilter.GaussianBlur(7)))
    rounded_rect(draw, (8, 8, w - 8, h - 8), 24, (6, 16, 20, 240), (*CYAN, pulse), 2)
    rounded_rect(draw, (34, 34, w - 34, h - 34), 16, (2, 12, 14, 228), (230, 255, 255, 28), 1)
    for x in list(range(55, 185, 14)) + list(range(950, 1095, 14)):
        for y in range(50, 260, 18):
            draw.text((x, y), random.choice(["0", "1"]), fill=(0, 246, 255, 32), font=font(FONT_MONO, 9))
    boot = [
        "⚙ booting profile...",
        "▣ loading mobile systems.............. done",
        "▤ loading full-stack architecture...... done",
        "◉ loading computer vision models....... done",
        "◆ loading product instincts............ done",
        "✳ status: building things that look good, work hard, and survive real users",
        "> _",
    ]
    text = "\n".join(boot)
    visible = text[:chars]
    y = 64
    for line in visible.split("\n"):
        if " done" in line:
            left, done = line.rsplit(" done", 1)
            draw.text((320, y), left, fill=TEXT, font=font(FONT_MONO, 18))
            draw.text((742, y), "done", fill=GREEN, font=font(FONT_MONO_BOLD, 18))
        else:
            shown = line.replace("_", "█" if blink else " ")
            draw.text((250, y), shown, fill=(220, 252, 255), font=font(FONT_MONO, 18))
        y += 29
    return img.convert("P", palette=Image.ADAPTIVE, colors=128)


def make_terminal_gif():
    full = "\n".join([
        "⚙ booting profile...",
        "▣ loading mobile systems.............. done",
        "▤ loading full-stack architecture...... done",
        "◉ loading computer vision models....... done",
        "◆ loading product instincts............ done",
        "✳ status: building things that look good, work hard, and survive real users",
        "> _",
    ])
    counts = list(range(0, len(full) + 1, 6)) + [len(full)] * 12
    frames = [draw_terminal_frame(c, i % 2 == 0) for i, c in enumerate(counts)]
    frames[0].save(ASSETS / "terminal-boot.gif", save_all=True, append_images=frames[1:], duration=45, loop=0, optimize=True)


def make_circuit_overlay():
    svg = """<svg width="1200" height="360" viewBox="0 0 1200 360" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="1200" height="360" fill="#0A0E17"/>
  <g opacity=".42" stroke="#00F6FF" stroke-width="1">
    <path d="M80 90H230L272 132H410"/><path d="M80 145H210L256 190H380"/><path d="M790 92H945L1008 155H1120"/><path d="M730 205H900L960 265H1115"/>
    <circle cx="230" cy="90" r="4" fill="#00F6FF"/><circle cx="945" cy="92" r="4" fill="#FF2ED1"/><circle cx="900" cy="205" r="3" fill="#FF2ED1"/>
  </g>
  <g opacity=".34" stroke="#FF2ED1" stroke-width="1">
    <path d="M108 245H310L350 285H485"/><path d="M730 138H870L928 196H1060"/>
  </g>
</svg>
"""
    (ASSETS / "circuit-overlay.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    if not (ASSETS / "hero-banner.gif").exists():
        make_hero_gif()
    make_terminal_gif()
    make_circuit_overlay()
    print("generated hero-banner.gif, terminal-boot.gif, circuit-overlay.svg")
