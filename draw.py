#!/usr/bin/env python3
"""Draw the front page for news-image-20261117.

Concept: "The World in One Day" — a classic broadsheet front page on light
paper that sums up Tuesday 17 November 2026 in sixteen real stories.
Everything here is drawn with PIL inside this session. No photos, no network.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 24
CW = W - 2 * MARGIN

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


PAPER = (250, 246, 236)
INK = (26, 26, 26)
NAVY = (31, 56, 100)
RED = (168, 46, 32)
GOLD = (176, 138, 38)
SKY = (191, 217, 232)
SKY_PALE = (216, 232, 240)
SEA = (44, 110, 145)
SEA_DARK = (28, 82, 112)
SAND = (216, 203, 168)
SAND_DARK = (196, 180, 140)
LAND = (210, 216, 196)
LAND_LINE = (150, 160, 140)
OCEAN = (228, 238, 242)
RULE = (178, 172, 160)
GRAY = (110, 108, 100)
WHITE = (255, 255, 255)
CHIP_GREEN = (118, 185, 0)
DUSK1 = (238, 205, 158)
DUSK2 = (226, 178, 120)


def wrap(text, fnt, width):
    """Split text into lines that fit width (in pixels) for the given font."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, lines, fnt, x, y, fill, leading, max_lines=None):
    """Draw wrapped lines; returns the y below the last drawn line."""
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def text_h(fnt):
    box = fnt.getbbox("Ag")
    return box[3] - box[1]


def tracked_width(fnt, text, tracking):
    return sum(fnt.getlength(c) for c in text) + tracking * max(0, len(text) - 1)


def draw_tracked(d, text, fnt, cx, y, tracking, fill):
    """Draw text centred on cx with letter tracking."""
    w = tracked_width(fnt, text, tracking)
    x = cx - w / 2
    for ch in text:
        d.text((x, y), ch, font=fnt, fill=fill)
        x += fnt.getlength(ch) + tracking


def section_label(d, text, y):
    """Small-caps section label with hairlines on both sides."""
    fnt = F(SANS_B, 13)
    w = tracked_width(fnt, text, 3)
    cx = W / 2
    mid = y + 8
    d.line([(MARGIN, mid), (cx - w / 2 - 14, mid)], fill=RULE, width=1)
    d.line([(cx + w / 2 + 14, mid), (W - MARGIN, mid)], fill=RULE, width=1)
    draw_tracked(d, text, fnt, cx, y, 3, NAVY)


# ---------------------------------------------------------------- world map

# Simplified continent outlines in (lon, lat). Rough on purpose: the map is
# small and only needs to read as a world map with numbered pins.
CONTINENTS = [
    # North America
    [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-115, 73), (-100, 73),
     (-90, 74), (-85, 70), (-80, 73), (-75, 62), (-65, 60), (-60, 52),
     (-55, 47), (-60, 44), (-70, 42), (-75, 35), (-80, 26), (-84, 30),
     (-88, 21), (-90, 16), (-95, 16), (-97, 20), (-105, 20), (-110, 24),
     (-115, 30), (-120, 35), (-125, 42), (-125, 49), (-135, 58),
     (-150, 60), (-160, 58), (-168, 66)],
    # Greenland
    [(-58, 64), (-45, 60), (-32, 68), (-22, 70), (-25, 76), (-40, 78),
     (-55, 75), (-60, 70), (-58, 64)],
    # South America
    [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
     (-70, -23), (-70, -30), (-70, -40), (-73, -50), (-68, -55), (-65, -45),
     (-62, -38), (-57, -30), (-52, -32), (-48, -27), (-41, -22), (-39, -17),
     (-35, -9), (-35, -6), (-40, -3), (-44, -2), (-50, 0), (-55, 5),
     (-60, 8), (-68, 11), (-75, 11), (-79, 9)],
    # Africa
    [(-17, 15), (-16, 20), (-13, 27), (-9, 31), (-5, 35), (0, 36), (9, 37),
     (11, 34), (19, 33), (25, 32), (30, 31), (32, 31), (35, 28), (38, 22),
     (39, 15), (43, 12), (48, 11), (51, 11), (51, 2), (46, -5), (41, -10),
     (40, -15), (36, -20), (33, -26), (28, -33), (20, -35), (17, -32),
     (14, -22), (13, -12), (12, -6), (9, -1), (9, 4), (4, 6), (-8, 5),
     (-13, 8), (-17, 12), (-17, 15)],
    # Europe
    [(-9, 37), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (0, 50), (2, 51),
     (5, 53), (8, 55), (8, 57), (10, 59), (13, 56), (18, 56), (21, 55),
     (21, 59), (24, 60), (25, 65), (28, 71), (32, 70), (40, 68), (44, 66),
     (40, 60), (38, 55), (35, 50), (30, 46), (28, 45), (23, 40), (22, 37),
     (19, 42), (15, 44), (12, 44), (8, 39), (3, 38), (-1, 37), (-6, 36),
     (-9, 37)],
    # Asia
    [(28, 41), (36, 36), (43, 30), (48, 29), (52, 27), (57, 26), (61, 25),
     (66, 25), (70, 23), (73, 20), (76, 10), (80, 7), (81, 13), (85, 19),
     (89, 22), (92, 21), (95, 16), (98, 10), (100, 6), (103, 2), (104, 9),
     (107, 11), (109, 14), (109, 20), (113, 22), (117, 24), (120, 28),
     (122, 31), (121, 35), (122, 38), (126, 40), (130, 42), (133, 43),
     (136, 44), (139, 46), (141, 50), (142, 54), (150, 60), (160, 60),
     (170, 66), (180, 66), (170, 70), (150, 72), (130, 72), (110, 74),
     (90, 75), (70, 73), (55, 69), (45, 68), (35, 66), (30, 60), (28, 55),
     (28, 48), (28, 41)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (140, 39),
     (141, 41), (141, 44), (140, 42), (138, 38), (136, 35), (133, 34),
     (130, 31)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (0, 53), (1, 51), (-3, 50),
     (-5, 50)],
    # Sumatra
    [(95, 5), (100, 0), (104, -5), (106, -6), (102, -2), (98, 3), (95, 5)],
    # Borneo
    [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (113, -4),
     (110, -2), (109, 1)],
    # Java
    [(105, -6), (110, -7), (114, -8), (114, -9), (108, -8), (105, -7)],
    # New Guinea
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -9), (147, -9),
     (143, -8), (138, -8), (134, -4), (131, -1)],
    # Australia
    [(114, -22), (114, -28), (115, -33), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11),
     (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17),
     (118, -20), (114, -22)],
]

# (story number, lon, lat, dx, dy) — dx/dy nudge the pin circle away from a
# crowded spot; a thin leader line joins it back to the true position.
PINS = [
    (1, 36.5, 45.3, 0, -9),    # Kerch Bridge
    (2, 56.5, 26.5, 0, 0),     # Strait of Hormuz
    (3, 121.0, 14.6, 0, 0),    # Manila
    (4, 114.0, 22.5, 0, 0),    # Shenzhen
    (5, -122.0, 37.4, 0, 0),   # Nvidia, Santa Clara
    (6, 34.5, 31.5, 10, 4),    # Gaza
    (7, 142.0, 43.0, 0, 0),    # Hokkaido
    (8, 45.0, 15.0, 0, 0),     # Yemen
    (9, 30.0, -2.0, 0, 0),     # Rwanda
    (10, 2.3, 48.8, 0, 0),     # Paris
    (11, 30.7, 36.9, 0, 0),    # Antalya
    (12, 106.9, 47.9, 0, 0),   # Mongolia
    (13, -74.0, 40.7, 0, 0),   # New York markets
    (14, -77.0, 25.0, 8, 2),   # Bahamas, Tiger Woods
]


def project(lon, lat, box):
    x0, y0, x1, y1 = box
    px = x0 + (lon + 170) / 360.0 * (x1 - x0)
    py = y0 + (75 - lat) / 130.0 * (y1 - y0)
    return (px, py)


def draw_map(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=OCEAN, outline=RULE)
    for poly in CONTINENTS:
        pts = [project(lon, lat, box) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    fnt = F(SANS_B, 8)
    for num, lon, lat, dx, dy in PINS:
        px, py = project(lon, lat, box)
        cx, cy = px + dx, py + dy
        if dx or dy:
            d.line([(px, py), (cx, cy)], fill=INK, width=1)
            d.ellipse([px - 1.5, py - 1.5, px + 1.5, py + 1.5], fill=INK)
        r = 6
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED, outline=WHITE)
        label = str(num)
        tw = fnt.getlength(label)
        th = text_h(fnt)
        d.text((cx - tw / 2, cy - th / 2 - 1), label, font=fnt, fill=WHITE)


# ------------------------------------------------------------- illustrations


def frame(d, box):
    d.rectangle(box, outline=RULE, width=1)


def draw_kerch(d, box):
    """A bridge span falling into the sea, smoke rising from the break."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    horizon = y0 + int(h * 0.52)
    d.rectangle([x0, y0, x1, horizon], fill=SKY)
    d.rectangle([x0, horizon, x1, y1], fill=SEA)
    # pale sun
    d.ellipse([x1 - 52, y0 + 10, x1 - 22, y0 + 40], fill=(245, 238, 210))
    # wave lines
    for i, wy in enumerate((0.62, 0.74, 0.88)):
        yy = y0 + int(h * wy)
        d.arc([x0 + 8 + i * 30, yy - 5, x0 + 60 + i * 30, yy + 5],
              200, 340, fill=(120, 175, 200), width=2)
        d.arc([x0 + 150 + i * 20, yy - 5, x0 + 205 + i * 20, yy + 5],
              200, 340, fill=(120, 175, 200), width=2)
    deck_y = y0 + int(h * 0.50)
    # piers
    for px in (x0 + 42, x1 - 50):
        d.rectangle([px, deck_y, px + 10, y1 - 6], fill=(96, 96, 96))
    # deck, left and right of the break
    cx = (x0 + x1) / 2
    d.rectangle([x0 + 4, deck_y - 7, cx - 36, deck_y + 1], fill=(74, 74, 74))
    d.rectangle([cx + 36, deck_y - 7, x1 - 4, deck_y + 1], fill=(74, 74, 74))
    # railing posts
    for rx in range(x0 + 12, x1 - 8, 22):
        if abs(rx - cx) > 44:
            d.line([(rx, deck_y - 13), (rx, deck_y - 7)], fill=(74, 74, 74),
                   width=2)
    # fallen span, tilted into the water
    d.polygon([(cx - 36, deck_y - 7), (cx + 34, deck_y + 30),
               (cx + 26, deck_y + 38), (cx - 30, deck_y + 1)],
              fill=(96, 96, 96))
    # splash where the span hits the water
    for sx in (cx - 18, cx + 2, cx + 22):
        d.arc([sx - 8, deck_y + 34, sx + 8, deck_y + 46], 180, 360,
              fill=(220, 235, 240), width=2)
    # small flame at the break, then smoke
    d.polygon([(cx - 8, deck_y - 6), (cx, deck_y - 26), (cx + 8, deck_y - 6)],
              fill=(230, 126, 34))
    d.polygon([(cx - 4, deck_y - 6), (cx, deck_y - 18), (cx + 4, deck_y - 6)],
              fill=(241, 196, 15))
    for sx, sy, sr, col in ((cx - 26, deck_y - 44, 13, (150, 150, 150)),
                            (cx + 2, deck_y - 62, 16, (130, 130, 130)),
                            (cx + 26, deck_y - 46, 12, (160, 160, 160)),
                            (cx - 4, deck_y - 84, 14, (145, 145, 145))):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=col)
    frame(d, box)


def draw_hormuz(d, box):
    """A tanker on fire in a strait at dusk, a carrier group far behind."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    horizon = y0 + int(h * 0.55)
    d.rectangle([x0, y0, x1, horizon], fill=DUSK1)
    d.rectangle([x0, y0 + int(h * 0.28), x1, horizon], fill=DUSK2)
    d.ellipse([x0 + 34, y0 + 12, x0 + 66, y0 + 44], fill=(250, 226, 170))
    d.rectangle([x0, horizon, x1, y1], fill=SEA_DARK)
    # distant carrier group on the horizon, right side
    cgx = x1 - 118
    d.rectangle([cgx, horizon - 7, cgx + 96, horizon - 3], fill=(52, 66, 80))
    d.rectangle([cgx + 62, horizon - 16, cgx + 72, horizon - 7],
                fill=(52, 66, 80))
    d.rectangle([cgx - 130, horizon - 5, cgx - 84, horizon - 2],
                fill=(62, 76, 90))
    # tanker hull
    hull_y = y0 + int(h * 0.72)
    d.polygon([(x0 + 14, hull_y), (x1 - 14, hull_y), (x1 - 34, hull_y + 22),
               (x0 + 34, hull_y + 22)], fill=(43, 43, 43))
    d.rectangle([x0 + 40, hull_y - 16, x0 + 96, hull_y], fill=(230, 230, 230))
    d.rectangle([x0 + 104, hull_y - 10, x0 + 150, hull_y], fill=(200, 200, 200))
    d.rectangle([x1 - 96, hull_y - 20, x1 - 66, hull_y], fill=(190, 60, 40))
    # flames from the middle of the ship
    fx = x0 + int(w * 0.55)
    d.polygon([(fx - 34, hull_y - 12), (fx - 8, hull_y - 66),
               (fx + 6, hull_y - 30), (fx + 20, hull_y - 58),
               (fx + 38, hull_y - 12)], fill=(230, 126, 34))
    d.polygon([(fx - 18, hull_y - 12), (fx - 4, hull_y - 48),
               (fx + 14, hull_y - 12)], fill=(241, 196, 15))
    d.polygon([(fx - 8, hull_y - 12), (fx, hull_y - 30),
               (fx + 8, hull_y - 12)], fill=(250, 235, 180))
    # black smoke column drifting right
    for sx, sy, sr in ((fx - 6, hull_y - 78, 12), (fx + 10, hull_y - 96, 15),
                       (fx + 30, hull_y - 108, 13), (fx + 50, hull_y - 112, 11)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(70, 70, 70))
    # waves
    for wy in (0.82, 0.92):
        yy = y0 + int(h * wy)
        d.arc([x0 + 20, yy - 4, x0 + 70, yy + 4], 200, 340,
              fill=(90, 140, 165), width=2)
        d.arc([x0 + 190, yy - 4, x0 + 240, yy + 4], 200, 340,
              fill=(90, 140, 165), width=2)
    frame(d, box)


def draw_quad(d, box):
    """A grand meeting hall with four flags and steps."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=SKY_PALE)
    d.ellipse([x0 + 24, y0 + 10, x0 + 54, y0 + 40], fill=(245, 238, 210))
    # hall body
    bx0, bx1 = x0 + 34, x1 - 34
    by0, by1 = y0 + int(h * 0.30), y0 + int(h * 0.82)
    d.rectangle([bx0, by0, bx1, by1], fill=(216, 205, 180))
    # pediment
    d.polygon([(bx0 - 8, by0), (bx1 + 8, by0), ((bx0 + bx1) / 2, by0 - 26)],
              fill=(200, 188, 160))
    d.ellipse([((bx0 + bx1) / 2) - 7, by0 - 22, ((bx0 + bx1) / 2) + 7,
               by0 - 8], fill=NAVY)
    # columns
    for i in range(4):
        cx = bx0 + 30 + i * ((bx1 - bx0 - 60) / 3)
        d.rectangle([cx - 8, by0 + 8, cx + 8, by1], fill=(238, 232, 210))
        d.rectangle([cx - 11, by0 + 4, cx + 11, by0 + 10], fill=(226, 218, 192))
    # dark door
    d.rectangle([((bx0 + bx1) / 2) - 16, by1 - 44, ((bx0 + bx1) / 2) + 16,
                 by1], fill=(70, 60, 45))
    # steps
    for i, sy in enumerate((by1, by1 + 8, by1 + 16)):
        d.rectangle([bx0 - 14 - i * 8, sy, bx1 + 14 + i * 8, sy + 8],
                    fill=(196, 188, 168))
    # four flags on poles above the hall
    flag_cols = [
        [(190, 60, 40), (255, 255, 255), (190, 60, 40)],   # stripes
        [(255, 255, 255)],                                  # Japan: white
        [(230, 140, 40), (255, 255, 255), (40, 140, 60)],  # India bands
        [(40, 60, 140)],                                    # Australia: blue
    ]
    for i, bands in enumerate(flag_cols):
        fx = x0 + 52 + i * ((w - 104) / 3)
        d.line([(fx, y0 + 12), (fx, by0 - 28)], fill=INK, width=2)
        fw, fh = 34, 20
        fy = by0 - 28
        if i == 0:
            for j, col in enumerate(bands):
                d.rectangle([fx, fy + j * 7, fx + fw, fy + (j + 1) * 7],
                            fill=col)
            d.rectangle([fx, fy, fx + 14, fy + 10], fill=NAVY)
        elif i == 1:
            d.rectangle([fx, fy, fx + fw, fy + fh], fill=WHITE,
                        outline=GRAY)
            d.ellipse([fx + 12, fy + 5, fx + 22, fy + 15], fill=RED)
        elif i == 2:
            for j, col in enumerate(bands):
                d.rectangle([fx, fy + j * 7, fx + fw, fy + (j + 1) * 7],
                            fill=col)
        else:
            d.rectangle([fx, fy, fx + fw, fy + fh], fill=bands[0])
            for sx, sy in ((8, 5), (20, 9), (12, 14), (26, 14)):
                d.ellipse([fx + sx, fy + sy, fx + sx + 3, fy + sy + 3],
                          fill=WHITE)
    # trees at the sides
    for tx in (x0 + 16, x1 - 30):
        d.ellipse([tx, by1 - 34, tx + 22, by1 - 6], fill=(90, 140, 80))
        d.rectangle([tx + 9, by1 - 8, tx + 13, by1], fill=(110, 85, 50))
    frame(d, box)


def draw_nvidia(d, box):
    """A green chip on a dark board with a red falling arrow."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(31, 42, 54))
    cx, cy = (x0 + x1) / 2 - 12, (y0 + y1) / 2
    s = 30
    # gold pins
    for i in range(4):
        off = -18 + i * 12
        d.rectangle([cx - s - 9, cy + off - 2, cx - s, cy + off + 2],
                    fill=(201, 162, 39))
        d.rectangle([cx + s, cy + off - 2, cx + s + 9, cy + off + 2],
                    fill=(201, 162, 39))
        d.rectangle([cx + off - 2, cy - s - 9, cx + off + 2, cy - s],
                    fill=(201, 162, 39))
        d.rectangle([cx + off - 2, cy + s, cx + off + 2, cy + s + 9],
                    fill=(201, 162, 39))
    d.rectangle([cx - s, cy - s, cx + s, cy + s], fill=CHIP_GREEN)
    d.rectangle([cx - s + 9, cy - s + 9, cx + s - 9, cy + s - 9],
                fill=(90, 150, 0))
    d.line([(cx - s + 9, cy), (cx + s - 9, cy)], fill=(140, 200, 40),
           width=2)
    d.line([(cx, cy - s + 9), (cx, cy + s - 9)], fill=(140, 200, 40),
           width=2)
    # red falling arrow, right side
    ax = x1 - 32
    d.rectangle([ax - 4, y0 + 14, ax + 4, y0 + 46], fill=RED)
    d.polygon([(ax - 11, y0 + 44), (ax + 11, y0 + 44), (ax, y0 + 64)],
              fill=RED)
    frame(d, box)


def draw_gaza(d, box):
    """A convoy of aid trucks on a desert road, a gate ahead."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y0 + int(h * 0.45)], fill=SKY_PALE)
    d.rectangle([x0, y0 + int(h * 0.45), x1, y1], fill=SAND)
    road_y = y0 + int(h * 0.62)
    d.rectangle([x0, road_y, x1, road_y + 26], fill=(150, 148, 142))
    d.line([(x0 + 6, road_y + 13), (x1 - 6, road_y + 13)], fill=WHITE,
           width=2)
    # gate at the right end
    gx = x1 - 34
    for bx in range(gx, x1 - 4, 6):
        d.line([(bx, road_y - 26), (bx, road_y + 26)], fill=(90, 88, 80),
               width=2)
    d.rectangle([gx - 4, road_y - 30, gx + 2, road_y + 26], fill=(90, 88, 80))
    # three trucks
    for i, tx in enumerate((x0 + 14, x0 + 86, x0 + 158)):
        cab_x = tx + 44
        d.rectangle([tx, road_y - 22, tx + 42, road_y + 2], fill=WHITE,
                    outline=GRAY)
        d.rectangle([cab_x, road_y - 14, cab_x + 20, road_y + 2],
                    fill=(210, 225, 235), outline=GRAY)
        # red cross on the box
        d.rectangle([tx + 17, road_y - 18, tx + 25, road_y - 6], fill=RED)
        d.rectangle([tx + 13, road_y - 14, tx + 29, road_y - 10], fill=RED)
        for wx in (tx + 10, tx + 32, cab_x + 14):
            d.ellipse([wx - 5, road_y + 2, wx + 5, road_y + 12], fill=INK)
    # crates by the roadside
    for cx, cy in ((x0 + 30, road_y + 34), (x0 + 52, road_y + 30),
                   (x0 + 44, road_y + 44)):
        d.rectangle([cx, cy, cx + 16, cy + 12], fill=(176, 142, 90),
                    outline=(120, 95, 55))
    frame(d, box)


def draw_japan(d, box):
    """Two jets intercepting a larger plane in a pale sky."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y0 + int(h * 0.78)], fill=SKY)
    d.rectangle([x0, y0 + int(h * 0.78), x1, y1], fill=SEA)
    for cx, cy, cr in ((x0 + 30, y0 + 18, 16), (x0 + 130, y0 + 12, 20),
                       (x0 + 190, y0 + 30, 14)):
        d.ellipse([cx - cr, cy - cr // 2, cx + cr, cy + cr // 2],
                  fill=WHITE)
    # airliner, upper middle
    ax, ay = x0 + int(w * 0.42), y0 + int(h * 0.30)
    d.ellipse([ax - 52, ay - 8, ax + 52, ay + 8], fill=WHITE, outline=GRAY)
    d.polygon([(ax + 40, ay - 6), (ax + 56, ay - 22), (ax + 56, ay - 2)],
              fill=WHITE, outline=GRAY)
    for wx in range(-36, 40, 12):
        d.ellipse([ax + wx, ay - 2, ax + wx + 4, ay + 2], fill=NAVY)
    # fighter jets below, in pursuit
    for jx, jy in ((x0 + 44, y0 + int(h * 0.58)),
                   (x0 + 108, y0 + int(h * 0.66))):
        d.polygon([(jx, jy - 12), (jx + 46, jy), (jx, jy + 12),
                   (jx + 10, jy)], fill=(90, 96, 104))
        d.polygon([(jx + 8, jy - 4), (jx + 26, jy - 18), (jx + 30, jy - 4)],
                  fill=(90, 96, 104))
        d.ellipse([jx + 18, jy - 4, jx + 26, jy + 4], fill=RED)
        d.line([(jx - 26, jy), (jx - 6, jy)], fill=WHITE, width=2)
        d.line([(jx - 18, jy + 10), (jx - 2, jy + 10)], fill=WHITE, width=2)
    frame(d, box)


def draw_houthi(d, box):
    """Desert coast with red arrows pushing along the shoreline."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=SAND)
    # sea on the left edge
    d.polygon([(x0, y0), (x0 + 44, y0), (x0 + 30, y1), (x0, y1)], fill=SEA)
    d.polygon([(x0 + 44, y0), (x0 + 58, y0), (x0 + 44, y1), (x0 + 30, y1)],
              fill=(190, 205, 195))
    # dunes
    d.arc([x0 + 60, y0 + int(h * 0.55), x0 + 200, y0 + int(h * 0.95)],
          200, 330, fill=SAND_DARK, width=2)
    d.arc([x0 + 120, y0 + int(h * 0.70), x0 + 260, y1 + 20], 200, 330,
          fill=SAND_DARK, width=2)
    # town blocks, bottom right
    for bx, by, bw, bh in ((x1 - 96, y1 - 44, 26, 30), (x1 - 64, y1 - 34, 22, 20),
                           (x1 - 38, y1 - 50, 24, 36)):
        d.rectangle([bx, by, bx + bw, by + bh], fill=(238, 232, 210),
                    outline=(170, 160, 140))
    # red advance arrows along the coast
    for ax, ay, s in ((x0 + 66, y0 + 18, 13), (x0 + 84, y0 + 46, 15),
                      (x0 + 104, y0 + 72, 17)):
        d.polygon([(ax, ay), (ax + s, ay + s // 2), (ax, ay + s),
                   (ax + 7, ay + s // 2)], fill=RED)
        d.line([(ax - 16, ay + s // 2), (ax + 2, ay + s // 2)], fill=RED,
               width=3)
    frame(d, box)


# ---------------------------------------------------------------- grid icons

def draw_icon(d, kind, cx, cy, r=13):
    """Small white pictogram on a navy disc."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=NAVY)
    if kind == "globe":
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], outline=WHITE, width=2)
        d.ellipse([cx - 3, cy - 7, cx + 3, cy + 7], outline=WHITE, width=1)
        d.line([(cx - 7, cy), (cx + 7, cy)], fill=WHITE, width=1)
    elif kind == "gavel":
        d.line([(cx - 6, cy + 7), (cx + 7, cy - 6)], fill=WHITE, width=3)
        d.rectangle([cx - 9, cy - 9, cx + 1, cy - 1], fill=WHITE)
    elif kind == "leaf":
        d.ellipse([cx - 7, cy - 5, cx + 6, cy + 7], outline=WHITE, width=2)
        d.line([(cx - 5, cy + 5), (cx + 5, cy - 5)], fill=WHITE, width=1)
    elif kind == "flag":
        d.line([(cx - 4, cy - 8), (cx - 4, cy + 8)], fill=WHITE, width=2)
        d.polygon([(cx - 4, cy - 8), (cx + 8, cy - 5), (cx - 4, cy - 2)],
                  fill=WHITE)
    elif kind == "coin":
        fnt = F(SANS_B, 13)
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], outline=WHITE, width=2)
        tw = fnt.getlength("B")
        th = text_h(fnt)
        d.text((cx - tw / 2, cy - th / 2 - 1), "B", font=fnt, fill=WHITE)
    elif kind == "golf":
        d.line([(cx - 3, cy - 8), (cx - 3, cy + 8)], fill=WHITE, width=2)
        d.polygon([(cx - 3, cy - 8), (cx + 8, cy - 5), (cx - 3, cy - 2)],
                  fill=WHITE)
        d.ellipse([cx + 4, cy + 5, cx + 8, cy + 9], fill=WHITE)
    elif kind == "screen":
        d.rectangle([cx - 8, cy - 7, cx + 8, cy + 4], outline=WHITE, width=2)
        d.line([(cx, cy + 4), (cx, cy + 8)], fill=WHITE, width=2)
        d.line([(cx - 5, cy + 8), (cx + 5, cy + 8)], fill=WHITE, width=2)
        d.line([(cx + 2, cy - 6), (cx - 2, cy + 2)], fill=WHITE, width=2)
    elif kind == "plane":
        d.polygon([(cx - 8, cy), (cx + 8, cy - 3), (cx + 4, cy + 2),
                   (cx - 2, cy + 6)], fill=WHITE)
        d.polygon([(cx - 1, cy - 2), (cx + 3, cy - 9), (cx + 5, cy - 2)],
                  fill=WHITE)


# ------------------------------------------------------------------- layout

def compose():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.line([(MARGIN, 14), (W - MARGIN, 14)], fill=INK, width=1)
    d.line([(MARGIN, 18), (W - MARGIN, 18)], fill=NAVY, width=2)
    draw_tracked(d, "THE WORLD IN ONE DAY", F(SANS_B, 15), W / 2, 28, 6,
                 NAVY)
    f_mast = F(SERIF_B, 50)
    mt = "TUESDAY 17 NOVEMBER 2026"
    d.text(((W - f_mast.getlength(mt)) / 2, 48), mt, font=f_mast, fill=INK)
    f_sub = F(SANS, 15)
    st = "16 stories · six continents · one day"
    d.text(((W - f_sub.getlength(st)) / 2, 104), st, font=f_sub, fill=GRAY)
    d.line([(MARGIN, 126), (W - MARGIN, 126)], fill=NAVY, width=3)
    d.line([(MARGIN, 131), (W - MARGIN, 131)], fill=INK, width=1)

    # hero row: three big illustrated stories
    hero = [
        ("UKRAINE", "Kerch Bridge Span Crashes Into the Sea",
         "Traffic stops after Ukraine hits the crossing to Crimea again, "
         "dropping a roadway section into the water.", draw_kerch),
        ("THE GULF", "Tanker Burns in the Strait of Hormuz",
         "A mine sets a tanker ablaze — the fourth in a day — as a U.S. "
         "carrier group arrives and Iran strikes a radar site in Bahrain.",
         draw_hormuz),
        ("ASIA", "Quad Leaders Meet in Manila",
         "Trump opens his Asia tour as the allies gather, and a three-way "
         "meeting with Xi and Putin is expected in Shenzhen on Thursday.",
         draw_quad),
    ]
    for i, (kick, head, cap, fn) in enumerate(hero):
        x0 = MARGIN + i * (317 + 12)
        x1 = x0 + 317
        fn(d, (x0, 142, x1, 302))
        draw_tracked(d, kick, F(SANS_B, 11), x0 + 317 / 2, 308, 2, RED)
        lines = wrap(head, F(SERIF_B, 19), 317)
        draw_lines(d, lines, F(SERIF_B, 19), x0, 324, INK, 23, max_lines=2)
        clines = wrap(cap, F(SANS, 12), 317)
        draw_lines(d, clines, F(SANS, 12), x0, 372, INK, 15, max_lines=3)
        d.line([(x0, 422), (x1, 422)], fill=RULE, width=1)

    # second row: four stories
    section_label(d, "ALSO TODAY", 428)
    row2 = [
        ("TECH", "Nvidia Chief Quits in Spy Scandal",
         "Jensen Huang resigns over an affair with a woman said to be a "
         "Chinese spy, as Washington tightens chip-export rules.",
         draw_nvidia),
        ("GAZA", "Allies Press Israel to Open Aid Crossings",
         "Britain, Australia, Canada and Italy urge access as 1.7 million "
         "are displaced and 1.4 million face acute hunger.", draw_gaza),
        ("JAPAN", "Japan Scrambles Jets as Russian Plane Intrudes",
         "Fighters go up after a Russian aircraft enters Japanese airspace.",
         draw_japan),
        ("YEMEN", "Houthis Advance in Yemen",
         "Government forces pull back from the Red Sea coast toward Aden as "
         "the rebels press on.", draw_houthi),
    ]
    for i, (kick, head, cap, fn) in enumerate(row2):
        x0 = MARGIN + i * (235 + 12)
        x1 = x0 + 235
        fn(d, (x0, 450, x1, 546))
        draw_tracked(d, kick, F(SANS_B, 10), x0 + 235 / 2, 550, 2, RED)
        lines = wrap(head, F(SERIF_B, 15), 235)
        draw_lines(d, lines, F(SERIF_B, 15), x0, 564, INK, 19, max_lines=2)
        clines = wrap(cap, F(SANS, 11), 235)
        draw_lines(d, clines, F(SANS, 11), x0, 604, INK, 14, max_lines=3)
        d.line([(x0, 650), (x1, 650)], fill=RULE, width=1)

    # small grid: eight more stories
    section_label(d, "IN BRIEF", 656)
    grid = [
        ("globe", "EU Plans Rwanda Deportation Hubs",
         "Five states plan a joint centre for rejected asylum seekers."),
        ("gavel", "Depardieu Admits Guilt in Paris",
         "The actor pleads guilty to sexual assault and drops his appeal."),
        ("leaf", "Climate Talks Reach Crunch Point",
         "COP31 in Antalya enters its decisive phase."),
        ("flag", "Mongolia's President Resigns",
         "Khürelsükh steps down amid a corruption scandal."),
        ("coin", "Bitcoin Slides Below $65,000",
         "Down more than 15% in a month; stocks fall too."),
        ("golf", "Tiger Woods to Play Again",
         "The golfer returns at the Hero World Challenge in December."),
        ("screen", "Outages Hit Apple and the NSA",
         "Computer systems go down at the iPhone maker and the spy agency."),
        ("plane", "FAA Pauses Router Rollout",
         "The aviation agency halts new routers after a nationwide ground "
         "stop."),
    ]
    for i, (icon, head, cap) in enumerate(grid):
        col, row = i % 4, i // 4
        x0 = MARGIN + col * (235 + 12)
        y0 = 678 + row * (74 + 12)
        draw_icon(d, icon, x0 + 18, y0 + 20)
        lines = wrap(head, F(SERIF_B, 12), 191)
        draw_lines(d, lines, F(SERIF_B, 12), x0 + 38, y0 + 6, INK, 15,
                   max_lines=2)
        clines = wrap(cap, F(SANS, 10), 191)
        draw_lines(d, clines, F(SANS, 10), x0 + 38, y0 + 38, INK, 12,
                   max_lines=2)
    for gx in (259, 506, 753):
        d.line([(gx, 678), (gx, 838)], fill=RULE, width=1)
    d.line([(MARGIN, 758), (W - MARGIN, 758)], fill=RULE, width=1)
    d.rectangle([MARGIN, 678, W - MARGIN, 838], outline=RULE, width=1)

    # bottom: world map with numbered pins + numbered index
    d.text((MARGIN, 850), "THE DAY'S PLACES", font=F(SANS_B, 12), fill=NAVY)
    d.text((576, 850), "INDEX", font=F(SANS_B, 12), fill=NAVY)
    draw_map(d, (MARGIN, 866, 560, 986))
    index = [
        "Kerch Bridge falls",
        "Tanker burns in Hormuz",
        "Quad summit in Manila",
        "Shenzhen three-way talks",
        "Nvidia chief resigns",
        "Gaza aid crossings",
        "Japan scrambles jets",
        "Houthis advance",
        "Rwanda deportation hubs",
        "Depardieu guilty plea",
        "COP31 crunch talks",
        "Mongolia president quits",
        "Bitcoin below $65,000",
        "Tiger Woods returns",
        "Apple & NSA outages",
        "FAA pauses routers",
    ]
    f_num = F(SANS_B, 10)
    f_it = F(SANS, 10)
    for i, title in enumerate(index):
        col, row = i % 2, i // 2
        x = 576 + col * 212
        y = 868 + row * 15
        num = str(i + 1) + "."
        d.text((x, y), num, font=f_num, fill=RED)
        d.text((x + f_num.getlength(num) + 4, y), title, font=f_it,
               fill=INK)

    # market strip
    d.rectangle([9, 994, 1015, 1015], fill=NAVY)
    f_mk = F(SANS_B, 13)
    mk = ("MARKETS · Bitcoin below $65,000 · Stocks slide · "
          "Oil up on Hormuz fears · Nvidia falls")
    d.text(((W - f_mk.getlength(mk)) / 2, 1002), mk, font=f_mk, fill=WHITE)

    # outer border
    d.rectangle([8, 8, 1016, 1016], outline=NAVY, width=2)
    return img


def main():
    img = compose()
    out = Path(__file__).parent / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print(f"saved {out} {img.size} {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
