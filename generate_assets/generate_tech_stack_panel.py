from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

W, H = 1200, 760
SCALE = 2
SW, SH = W * SCALE, H * SCALE

BG = (10, 14, 23)
CYAN = (0, 246, 255)
TEAL = (93, 255, 233)
BLUE = (108, 181, 255)
MAGENTA = (255, 46, 209)
TEXT = (230, 237, 243)
MUTED = (139, 150, 165)

FONT_MONO = r"C:\Windows\Fonts\consola.ttf"
FONT_MONO_BOLD = r"C:\Windows\Fonts\consolab.ttf"
FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"

FONT_CACHE: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    key = (path, size)
    if key not in FONT_CACHE:
        FONT_CACHE[key] = ImageFont.truetype(path, size * SCALE)
    return FONT_CACHE[key]


def sc(v: float) -> int:
    return int(round(v * SCALE))


def color_lerp(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


def path_color(t: float):
    if t < 0.52:
        return color_lerp(TEAL, BLUE, t / 0.52)
    return color_lerp(BLUE, MAGENTA, (t - 0.52) / 0.48)


def add_glow(base: Image.Image, layer: Image.Image, blur: int, alpha: float = 1.0) -> None:
    glow = layer.filter(ImageFilter.GaussianBlur(sc(blur)))
    if alpha != 1:
        glow.putalpha(glow.getchannel("A").point(lambda p: int(p * alpha)))
    base.alpha_composite(glow)
    base.alpha_composite(layer)


def rounded(draw: ImageDraw.ImageDraw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(tuple(sc(v) for v in box), radius=sc(radius), fill=fill, outline=outline, width=sc(width))


def text(draw: ImageDraw.ImageDraw, xy, value, fill, font_obj, anchor=None, stroke_width=0, stroke_fill=None):
    draw.text((sc(xy[0]), sc(xy[1])), value, fill=fill, font=font_obj, anchor=anchor, stroke_width=stroke_width, stroke_fill=stroke_fill)


def line(draw: ImageDraw.ImageDraw, pts, fill, width=1, joint="curve"):
    draw.line([(sc(x), sc(y)) for x, y in pts], fill=fill, width=sc(width), joint=joint)


def hex_points(cx, cy, r):
    return [(sc(cx + math.cos(math.pi / 6 + i * math.tau / 6) * r), sc(cy + math.sin(math.pi / 6 + i * math.tau / 6) * r)) for i in range(6)]


def draw_hex(draw: ImageDraw.ImageDraw, cx, cy, r, edge, pulse):
    halo = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
    hd = ImageDraw.Draw(halo)
    hd.polygon(hex_points(cx, cy, r + 7), outline=(*edge, int(75 + 90 * pulse)), width=sc(5))
    hd.polygon(hex_points(cx, cy, r), fill=(13, 24, 34, 238), outline=(*edge, int(170 + 75 * pulse)), width=sc(4))
    draw._image.alpha_composite(halo.filter(ImageFilter.GaussianBlur(sc(5))))
    draw.polygon(hex_points(cx, cy, r), fill=(13, 24, 34, 240), outline=(*edge, 245), width=sc(4))
    draw.polygon(hex_points(cx, cy, r * 0.58), fill=(21, 39, 49, 230), outline=(*edge, 92), width=sc(2))


def draw_background(img: Image.Image):
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, SW, SH), fill=(*BG, 255))
    # subtle vignette
    for cx, cy, r, col, alpha in [(260, 360, 360, CYAN, 34), (960, 350, 380, MAGENTA, 30), (600, 360, 450, BLUE, 20)]:
        glow = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        gd.ellipse((sc(cx - r), sc(cy - r), sc(cx + r), sc(cy + r)), fill=(*col, alpha))
        img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(sc(42))))

    random.seed(21)
    # right-angle traces around edges, intentionally behind the diagram.
    def traces(side: str, col):
        xbase = 20 if side == "left" else 850
        for i in range(16):
            y = random.randint(102, 650)
            x = xbase + random.randint(0, 110)
            pts = [(x, y), (x + random.randint(45, 115), y), (x + random.randint(80, 165), y + random.choice([-1, 1]) * random.randint(20, 45))]
            line(draw, pts, (*col, 118), 1.4)
            for px, py in pts[1:]:
                draw.ellipse((sc(px - 3), sc(py - 3), sc(px + 3), sc(py + 3)), outline=(*col, 140), width=sc(1))
    traces("left", CYAN)
    traces("right", MAGENTA)
    # Stronger reference-style PCB routes that frame the diagram without becoming the focal point.
    left_routes = [
        [(18, 126), (178, 126), (212, 160), (395, 160)],
        [(18, 145), (160, 145), (195, 180), (340, 180)],
        [(26, 455), (184, 455), (222, 420), (386, 420)],
        [(18, 654), (168, 654), (205, 620), (402, 620)],
        [(30, 682), (176, 682), (220, 638), (460, 638)],
    ]
    right_routes = [
        [(820, 126), (980, 126), (1022, 162), (1170, 162)],
        [(768, 180), (930, 180), (976, 222), (1164, 222)],
        [(792, 420), (948, 420), (994, 456), (1170, 456)],
        [(752, 650), (958, 650), (1008, 684), (1178, 684)],
    ]
    for route in left_routes:
        line(draw, route, (0, 94, 104, 255), 1.4)
        for px, py in route[1:-1]:
            draw.ellipse((sc(px - 4), sc(py - 4), sc(px + 4), sc(py + 4)), outline=(0, 122, 132, 255), width=sc(1))
    for route in right_routes:
        line(draw, route, (118, 28, 101, 255), 1.4)
        for px, py in route[1:-1]:
            draw.ellipse((sc(px - 4), sc(py - 4), sc(px + 4), sc(py + 4)), outline=(145, 35, 124, 255), width=sc(1))
    # hex outlines in far corners.
    for ox, oy, col in [(28, 540, CYAN), (1080, 535, MAGENTA), (1025, 92, MAGENTA)]:
        for row in range(3):
            for c in range(3):
                cx, cy = ox + c * 34 + (row % 2) * 17, oy + row * 30
                draw.polygon(hex_points(cx, cy, 17), outline=(*col, 84), width=sc(1))
    # ambient particles, no sparkle glyphs.
    for _ in range(180):
        x = random.randint(70, 1130)
        y = random.randint(100, 615)
        col = CYAN if x < W / 2 else MAGENTA
        a = random.randint(28, 82)
        draw.ellipse((sc(x), sc(y), sc(x + 1.3), sc(y + 1.3)), fill=(*col, a))


def draw_header(img: Image.Image, pulse: float):
    draw = ImageDraw.Draw(img)
    layer = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.line([(sc(24), sc(46)), (sc(608), sc(46)), (sc(594), sc(88)), (sc(24), sc(88)), (sc(24), sc(46))], fill=(*CYAN, int(150 + 80 * pulse)), width=sc(3))
    ld.line([(sc(606), sc(46)), (sc(1176), sc(46)), (sc(1176), sc(88)), (sc(594), sc(88)), (sc(606), sc(46))], fill=(*MAGENTA, int(145 + 80 * pulse)), width=sc(3))
    add_glow(img, layer, 7, .85)
    text(draw, (38, 55), "> tech_stack --list", TEXT, font(FONT_MONO_BOLD, 26), stroke_width=1, stroke_fill=(0, 0, 0, 180))


def draw_labels(draw: ImageDraw.ImageDraw):
    text(draw, (132, 200), "MOBILE STACK", (147, 255, 244), font(FONT_MONO_BOLD, 25))
    text(draw, (490, 200), "FULL STACK WEB", (142, 220, 255), font(FONT_MONO_BOLD, 25))
    text(draw, (890, 200), "VISION & AI", (255, 161, 238), font(FONT_MONO_BOLD, 25))


def tube_points():
    # Exactly five vertices: top, valley, top, valley, top.
    return [(225, 267), (410, 374), (600, 267), (790, 374), (975, 267)]


def draw_gradient_tube(img: Image.Image, pulse: float, frame_phase: float):
    pts = tube_points()
    dense = []
    for a, b in zip(pts, pts[1:]):
        ax, ay = a
        bx, by = b
        steps = 60
        for i in range(steps):
            t = i / steps
            # Smooth easing makes the corners feel rounded even though the path is a W.
            x = ax * (1 - t) + bx * t
            y = ay * (1 - t) + by * t
            dense.append((x, y))
    dense.append(pts[-1])

    for width, alpha, blur in [(60, 42, 16), (44, 74, 9), (32, 120, 4)]:
        glow = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        for i in range(len(dense) - 1):
            t = i / (len(dense) - 2)
            col = path_color(t)
            gd.line([(sc(dense[i][0]), sc(dense[i][1])), (sc(dense[i + 1][0]), sc(dense[i + 1][1]))], fill=(*col, int(alpha * (.72 + .28 * pulse))), width=sc(width))
        img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(sc(blur))))
    core = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
    cd = ImageDraw.Draw(core)
    for i in range(len(dense) - 1):
        t = i / (len(dense) - 2)
        col = path_color(t)
        cd.line([(sc(dense[i][0]), sc(dense[i][1])), (sc(dense[i + 1][0]), sc(dense[i + 1][1]))], fill=(*col, 205), width=sc(26))
    img.alpha_composite(core)

    draw = ImageDraw.Draw(img)
    for idx, (x, y) in enumerate(pts):
        node_pulse = 0.5 + 0.5 * math.sin(frame_phase + idx * 0.58)
        draw_hex(draw, x, y, 23, path_color(idx / 4), node_pulse)


def tile(draw: ImageDraw.ImageDraw, x, y, label, color, size=58, fs=24):
    rounded(draw, (x, y, x + size, y + size), 11, (27, 33, 44, 235), None, 1)
    text(draw, (x + size / 2, y + size * 0.64), label, color, font(FONT_BOLD, fs), anchor="mm")


def draw_icons(draw: ImageDraw.ImageDraw):
    # Mobile
    tile(draw, 150, 346, "Fl", (82, 217, 255), 72, 32)
    tile(draw, 245, 346, "Da", (43, 213, 196), 72, 30)
    # Web
    tile(draw, 525, 346, "Re", (97, 218, 251), 66, 28)
    tile(draw, 635, 346, "JS", (140, 200, 75), 66, 29)
    text(draw, (505, 492), "Express", TEXT, font(FONT_BOLD, 26))
    # Mongo leaf in lower valley
    draw.path if False else None
    leaf = [(sc(655), sc(454)), (sc(687), sc(495)), (sc(655), sc(550)), (sc(625), sc(495))]
    draw.polygon(leaf, fill=(77, 179, 61, 220))
    draw.line([(sc(655), sc(458)), (sc(655), sc(545))], fill=(168, 225, 145, 125), width=sc(2))
    # Vision + AI, no Gemini/sparkle mark.
    tile(draw, 895, 346, "Py", (255, 212, 59), 62, 27)
    tile(draw, 1005, 346, "Tf", (255, 140, 0), 62, 27)
    tile(draw, 895, 455, "Pt", (238, 76, 44), 62, 27)
    text(draw, (985, 493), "Py", (238, 93, 44), font(FONT_BOLD, 26))
    text(draw, (1018, 493), "Spark", TEXT, font(FONT_BOLD, 24))


def draw_bottom_tools(draw: ImageDraw.ImageDraw, pulse: float):
    rounded(draw, (318, 620, 882, 733), 24, (43, 48, 56, 242), (172, 180, 192, int(175 + 55 * pulse)), 3)
    labels = [("Fg", (255, 97, 246)), ("Xd", (255, 97, 246)), ("VS", (58, 167, 255)), ("Tx", (248, 250, 252)), ("Dc", (36, 150, 237)), ("Gh", (248, 250, 252)), ("Gl", (252, 109, 56))]
    x = 358
    for label, col in labels:
        tile(draw, x, 640, label, col, 58, 25)
        x += 70
    text(draw, (600, 718), "DEV TOOLS & WORKFLOW", TEXT, font(FONT_MONO_BOLD, 17), anchor="mm")


def draw_panel_frame(img: Image.Image, pulse: float):
    draw = ImageDraw.Draw(img)
    frame = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
    fd = ImageDraw.Draw(frame)
    fd.rounded_rectangle((sc(10), sc(8), sc(1190), sc(752)), radius=sc(22), outline=(*CYAN, int(78 + 64 * pulse)), width=sc(3))
    fd.rounded_rectangle((sc(14), sc(12), sc(1186), sc(748)), radius=sc(20), outline=(*MAGENTA, int(44 + 52 * pulse)), width=sc(2))
    img.alpha_composite(frame.filter(ImageFilter.GaussianBlur(sc(6 + 4 * pulse))))
    draw.rounded_rectangle((sc(10), sc(8), sc(1190), sc(752)), radius=sc(22), outline=(*CYAN, int(118 + 72 * pulse)), width=sc(2))


def draw_frame(frame_idx: int, total: int) -> Image.Image:
    phase = math.tau * frame_idx / total
    pulse = 0.5 + 0.5 * math.sin(phase)
    img = Image.new("RGBA", (SW, SH), (*BG, 255))
    draw_background(img)
    draw_panel_frame(img, pulse)
    draw_header(img, pulse)
    draw = ImageDraw.Draw(img)
    draw_labels(draw)
    draw_gradient_tube(img, pulse, phase)
    draw_icons(draw)
    draw_bottom_tools(draw, pulse * .45 + .25)
    return img.resize((W, H), Image.Resampling.LANCZOS).convert("P", palette=Image.ADAPTIVE, colors=96)


def main() -> None:
    total = 20
    frames = [draw_frame(i, total) for i in range(total)]
    frames[0].save(ASSETS / "tech-stack-panel.gif", save_all=True, append_images=frames[1:], duration=150, loop=0, optimize=True)
    print("generated assets/tech-stack-panel.gif")


if __name__ == "__main__":
    main()
