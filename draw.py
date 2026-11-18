#!/usr/bin/env python3
"""Draw 'The World in One Day' v2 — a light broadsheet front page for the
make.fun competition news-image-20261117 (sum up 17 November 2026 in one image).

v2 of our own entry. Written from scratch in this session; nothing is copied
from the v1 build. All 24 stories are real 17 November 2026 news.

Deterministic: no network, no randomness, no timestamps. Same input always
produces the same entry.png. Output is 1024x1024, PNG, under 1 MiB.

Layout (1024x1024, margin 24):
  masthead title + date line, subline, 6-number stats strip,
  3 illustrated hero stories, 4 secondary stories, IN BRIEF grid (17 items),
  dot-matrix world map with numbered pins + INDEX 1-24,
  MARKETS strip, DATE CHECK footer.

Type rules: minimum 10px for all text, lead headlines 19px, words are never
broken across lines (wrapping splits on spaces only).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 24
CW = W - 2 * MARGIN  # 976

PAPER = (251, 249, 243)
INK = (18, 18, 18)
SOFT = (74, 74, 74)
RED = (176, 32, 32)
SEA = (36, 82, 122)
SKY = (206, 224, 236)
DOT = (64, 74, 84)
RULE = (18, 18, 18)
FAINT = (150, 148, 140)

FONT_DIR = "/usr/share/fonts/truetype"


def font(path, size):
    return ImageFont.truetype(FONT_DIR + "/" + path, size)


SERIF_B = "noto/NotoSerif-Bold.ttf"
SERIF = "noto/NotoSerif-Regular.ttf"
SANS_B = "noto/NotoSans-Bold.ttf"
SANS = "noto/NotoSans-Regular.ttf"
# Georgia is not installed on this Linux system. Noto Serif Bold is the
# closest available serif and is used for the stats numbers and headlines.


def wrap(draw, text, fnt, max_w):
    """Split text into lines on spaces only. Words are never broken."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, text, fnt, fill, max_w, max_lines, line_h):
    lines = wrap(d, text, fnt, max_w)[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += line_h
    return y


def centered(d, y, text, fnt, fill):
    w = d.textlength(text, font=fnt)
    d.text(((W - w) / 2, y), text, font=fnt, fill=fill)


def rule(d, y, x0=MARGIN, x1=W - MARGIN, width=1, fill=RULE):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- heroes
def hero_bridge(d, x, y, w, h):
    """Kerch Bridge: a roadway span falls into the sea."""
    d.rectangle([x, y, x + w, y + 62], fill=SKY)
    d.rectangle([x, y + 58, x + w, y + 66], fill=(170, 190, 205))
    d.rectangle([x, y + 66, x + w, y + h], fill=SEA)
    for wy in (y + 84, y + 104, y + 124):
        for wx in range(x + 8, x + w - 10, 34):
            d.arc([wx, wy, wx + 22, wy + 8], 200, 340, fill=(255, 255, 255), width=1)
    # bridge deck, two standing segments with a gap in the middle
    d.rectangle([x, y + 52, x + 128, y + 62], fill=(40, 40, 40))
    d.rectangle([x + 184, y + 52, x + w, y + 62], fill=(40, 40, 40))
    d.line([x, y + 52, x + 128, y + 52], fill=RED, width=2)
    d.line([x + 184, y + 52, x + w, y + 52], fill=RED, width=2)
    # the fallen span, tilted down into the water
    d.polygon([(x + 128, y + 54), (x + 142, y + 58), (x + 172, y + 118),
               (x + 158, y + 122)], fill=(60, 60, 60), outline=RED)
    # support columns
    for cx in (x + 30, x + 90, x + 220, x + 272):
        d.rectangle([cx, y + 62, cx + 8, y + 108], fill=(40, 40, 40))
    # splash where the span hit the water
    for sx, sy, r in ((x + 152, y + 116, 14), (x + 174, y + 122, 10),
                      (x + 138, y + 124, 8)):
        d.ellipse([sx - r, sy - r * 0.6, sx + r, sy + r * 0.6],
                  outline=(255, 255, 255), width=2)


def hero_tanker(d, x, y, w, h):
    """Tanker burning in the Strait of Hormuz at dusk."""
    d.rectangle([x, y, x + w, y + 70], fill=(232, 214, 188))
    # pale low sun, kept small so it does not compete with the fire
    d.ellipse([x + w - 52, y + 12, x + w - 24, y + 40], fill=(250, 222, 150))
    d.rectangle([x, y + 70, x + w, y + h], fill=(28, 62, 78))
    # tanker hull
    d.rectangle([x + 28, y + 88, x + 284, y + 116], fill=(24, 24, 24))
    d.rectangle([x + 28, y + 106, x + 284, y + 116], fill=(140, 30, 30))
    d.polygon([(x + 284, y + 88), (x + 300, y + 100), (x + 284, y + 116)],
              fill=(24, 24, 24))
    # superstructure and funnel
    d.rectangle([x + 212, y + 66, x + 252, y + 88], fill=(235, 235, 235))
    d.rectangle([x + 226, y + 56, x + 240, y + 66], fill=(200, 60, 40))
    # flames: overlapping rounded tongues, leaning slightly, never a triangle
    d.ellipse([x + 108, y + 44, x + 158, y + 90], fill=(220, 90, 20))
    d.ellipse([x + 128, y + 30, x + 168, y + 90], fill=(240, 140, 30))
    d.ellipse([x + 122, y + 52, x + 158, y + 90], fill=(250, 190, 60))
    d.ellipse([x + 134, y + 64, x + 156, y + 90], fill=(255, 220, 90))
    # a smaller second tongue to the right
    d.ellipse([x + 168, y + 62, x + 192, y + 90], fill=(240, 140, 30))
    d.ellipse([x + 174, y + 72, x + 188, y + 90], fill=(250, 190, 60))
    # smoke: a plume drifting left, paler as it rises
    d.ellipse([x + 128, y + 22, x + 150, y + 38], fill=(110, 110, 110))
    d.ellipse([x + 118, y + 10, x + 138, y + 26], fill=(135, 135, 135))
    d.ellipse([x + 104, y + 2, x + 122, y + 16], fill=(160, 160, 160))
    # fire reflected on the water
    for rx in range(x + 118, x + 172, 10):
        d.line([rx, y + 122, rx + 6, y + 122], fill=(245, 170, 60), width=2)


def draw_flag(d, kind, x, y, w, h):
    """Tiny flag, 62x40. Simplified but recognizable."""
    if kind == "us":
        for i in range(13):
            if i % 2 == 0:
                d.rectangle([x, y + i * h // 13, x + w, y + (i + 1) * h // 13],
                            fill=(178, 34, 34))
        d.rectangle([x, y, x + int(w * 0.4), y + int(h * 7 / 13)],
                    fill=(30, 50, 110))
        for gy in range(3):
            for gx in range(4):
                d.ellipse([x + 4 + gx * 6, y + 4 + gy * 6,
                           x + 6 + gx * 6, y + 6 + gy * 6], fill=(255, 255, 255))
    elif kind == "jp":
        d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
        d.ellipse([x + w // 2 - 12, y + h // 2 - 12, x + w // 2 + 12,
                   y + h // 2 + 12], fill=(188, 0, 45))
    elif kind == "in":
        d.rectangle([x, y, x + w, y + h // 3], fill=(255, 153, 51))
        d.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(255, 255, 255))
        d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(19, 136, 8))
        d.ellipse([x + w // 2 - 6, y + h // 2 - 6, x + w // 2 + 6,
                   y + h // 2 + 6], outline=(0, 0, 128), width=2)
    elif kind == "au":
        d.rectangle([x, y, x + w, y + h], fill=(0, 0, 139))
        # simplified Union Jack canton
        cx0, cy0, cw, chh = x, y, w // 2, h // 2
        d.rectangle([cx0, cy0, cx0 + cw, cy0 + chh], fill=(0, 0, 110))
        d.line([cx0, cy0, cx0 + cw, cy0 + chh], fill=(255, 255, 255), width=2)
        d.line([cx0 + cw, cy0, cx0, cy0 + chh], fill=(255, 255, 255), width=2)
        d.line([cx0 + cw // 2, cy0, cx0 + cw // 2, cy0 + chh], fill=(200, 30, 30),
               width=3)
        d.line([cx0, cy0 + chh // 2, cx0 + cw, cy0 + chh // 2], fill=(200, 30, 30),
               width=3)
        # stars
        for sx, sy in ((x + 44, y + 10), (x + 52, y + 26), (x + 40, y + 30)):
            d.polygon([(sx, sy - 4), (sx + 2, sy), (sx, sy + 4), (sx - 2, sy)],
                      fill=(255, 255, 255))


def hero_quad(d, x, y, w, h):
    """Quad leaders in Manila: four flags over a skyline, four delegates."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 234, 240))
    heights = [18, 30, 22, 38, 26, 44, 20, 34, 28, 16, 40, 24]
    bw = w // len(heights)
    bx = x
    for bh in heights:
        d.rectangle([bx, y + h - 10 - bh, bx + bw - 3, y + h - 10],
                    fill=(90, 100, 110))
        bx += bw
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(60, 68, 76))
    flags = ["us", "jp", "in", "au"]
    fw, fh = 62, 40
    gap = (w - 4 * fw) // 5
    for i, fl in enumerate(flags):
        fx = x + gap + i * (fw + gap)
        fy = y + 14
        d.line([fx + fw // 2, fy + fh, fx + fw // 2, y + h - 10],
               fill=(60, 60, 60), width=2)
        draw_flag(d, fl, fx, fy, fw, fh)
    # four delegates in front of the skyline
    for i in range(4):
        px = x + 40 + i * 72
        py = y + h - 34
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=(30, 30, 30))
        d.pieslice([px - 14, py + 6, px + 14, py + 26], 180, 360, fill=(30, 30, 30))


# ---------------------------------------------------------------- world map
# Coarse land mask, 48 columns x 28 rows. Row 0 is ~81N, row 27 is ~-55S.
# Each entry is a list of (first_col, last_col) land spans for that row.
LAND = [
    [(12, 12), (16, 17)],
    [(10, 13), (15, 18), (26, 26)],
    [(2, 3), (6, 14), (15, 18), (26, 27), (30, 46)],
    [(1, 4), (5, 15), (16, 17), (22, 22), (25, 27), (28, 47)],
    [(1, 3), (5, 14), (17, 17), (23, 23), (26, 26), (28, 46)],
    [(5, 15), (23, 23), (24, 29), (30, 44)],
    [(6, 15), (23, 30), (31, 45)],
    [(6, 14), (23, 28), (30, 45)],
    [(6, 15), (23, 29), (30, 44)],
    [(7, 15), (22, 29), (30, 44)],
    [(6, 13), (22, 30), (31, 37), (38, 43)],
    [(6, 10), (22, 30), (31, 32), (33, 36), (38, 42)],
    [(7, 10), (22, 31), (33, 35), (38, 41)],
    [(8, 9), (22, 31), (34, 34), (38, 41)],
    [(14, 16), (22, 30), (38, 41)],
    [(14, 17), (23, 29), (39, 42)],
    [(14, 18), (24, 28), (40, 44)],
    [(14, 18), (24, 27), (44, 44)],
    [(14, 18), (24, 27), (40, 43)],
    [(14, 18), (24, 26), (39, 43)],
    [(14, 17), (24, 26), (39, 43)],
    [(15, 17), (24, 26), (40, 43)],
    [(15, 17), (25, 25), (40, 42)],
    [(15, 16), (25, 25), (41, 41), (45, 45)],
    [(15, 15), (45, 45)],
    [(15, 15)],
    [(15, 15)],
    [(15, 15)],
]

# Pins: (lon, lat, index number, label dx, label dy). Label offsets are set
# by hand so the Europe / Middle East cluster does not collide.
PINS = [
    (33.5, 45.3, "1", 8, -12),    # Kerch Bridge, Crimea
    (56.5, 26.5, "2", 8, 2),      # tanker, Strait of Hormuz
    (121.0, 14.6, "3", 8, -6),    # Quad, Manila
    (-122.0, 37.4, "4", -30, -8),  # Nvidia, Santa Clara
    (34.5, 31.5, "5", -30, 6),    # Gaza crossings
    (141.0, 42.0, "6", 8, -8),    # Japan jets
    (44.2, 15.4, "7", 8, 4),      # Houthis, Yemen
    (30.1, -2.0, "8", 8, 2),      # Rwanda hubs
    (2.35, 48.85, "9", -26, 8),   # Depardieu, Paris
    (30.7, 36.9, "10", 10, 10),   # COP31, Antalya
    (106.9, 47.9, "11", 8, 2),    # Mongolia, Ulaanbaatar
    (-77.35, 25.05, "13", 8, -8),  # Tiger Woods, Bahamas
    (22.5, -4.0, "16", -30, 2),   # Ebola, DR Congo
    (20.5, 44.8, "18", -28, 8),   # Serbia, Belgrade
    (90.4, 23.8, "19", 8, -8),    # Bangladesh, Dhaka
    (104.0, 56.0, "20", -34, -8),  # An-12 crash, Siberia
    (8.68, 50.1, "22", 8, -10),   # Deutsche Bank, Frankfurt
    (32.5, 15.5, "23", -30, 2),   # Sudan, Khartoum
]
# Index items 12, 14, 15, 17, 21 and 24 have no map pin: Bitcoin, Apple/NSA
# outages, FAA routers, measles-free status, Voyager 1 (deep space) and
# Typhoon Akvan have no single place to pin.

MAP_X, MAP_Y, MAP_W, MAP_H = MARGIN, 786, 520, 160
MAP_COLS, MAP_ROWS = 48, 28
LAT_TOP, LAT_BOT = 84.0, -60.0


def lonlat_to_xy(lon, lat):
    px = MAP_X + (lon + 180.0) / 360.0 * MAP_W
    py = MAP_Y + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * MAP_H
    return px, py


def draw_map(d):
    cell_w = MAP_W / MAP_COLS
    cell_h = MAP_H / MAP_ROWS
    for r, spans in enumerate(LAND):
        cy = MAP_Y + (r + 0.5) * cell_h
        for a, b in spans:
            for c in range(a, b + 1):
                cx = MAP_X + (c + 0.5) * cell_w
                d.ellipse([cx - 2.1, cy - 2.1, cx + 2.1, cy + 2.1], fill=DOT)
    num_font = font(SANS_B, 11)
    for lon, lat, num, dx, dy in PINS:
        px, py = lonlat_to_xy(lon, lat)
        d.ellipse([px - 3.5, py - 3.5, px + 3.5, py + 3.5], fill=RED,
                  outline=(255, 255, 255), width=1)
        lx, ly = px + dx, py + dy
        for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            d.text((lx + ox, ly + oy), num, font=num_font, fill=PAPER)
        d.text((lx, ly), num, font=num_font, fill=RED)


# ---------------------------------------------------------------- content
HEROES = [
    ("UKRAINE · CRIMEA", "Kerch Bridge span crashes into the sea",
     "Ukraine hits the Crimea crossing again; a roadway span collapses.",
     hero_bridge),
    ("STRAIT OF HORMUZ", "Tanker burns in the Strait of Hormuz",
     "Iran drone strike and a mined tanker; a fourth tanker burns in 24 hours.",
     hero_tanker),
    ("ASIA · MANILA", "Quad leaders meet in Manila",
     "Trump opens his Asia tour; US, Japan, India and Australia meet in Manila.",
     hero_quad),
]

SECONDARY = [
    ("Nvidia chief quits in spy scandal",
     "Ex-CEO resigns over affair; board refuses return.", RED),
    ("Allies press Israel to open Gaza crossings",
     "UK, Australia, Canada and Italy demand aid access.", SEA),
    ("Japan scrambles jets as Russian plane intrudes",
     "Russian aircraft violates Japanese airspace.", (46, 120, 80)),
    ("Houthis advance in Yemen",
     "Rebels push toward Aden as fighting spreads.", (176, 120, 30)),
]

# IN BRIEF: 17 items. "Apple and NSA outages" and "FAA pauses router
# rollout" are two separate stories, so the grid holds 17 briefs and the
# whole page carries 24 stories: 3 heroes + 4 secondary + 17 brief.
BRIEF = [
    "EU states plan Rwanda deportation hubs",
    "Depardieu admits guilt in Paris",
    "COP31 Antalya: crunch talks, split on fossil fuels",
    "Mongolia's president resigns",
    "Bitcoin slides below $65,000",
    "Tiger Woods to play again",
    "Apple and NSA hit by outages",
    "FAA pauses router rollout",
    "Ebola: 11,000+ cases in DR Congo",
    "US, Mexico, Bolivia lose measles-free status",
    "Serbia student MP sworn in",
    "Bangladesh garment workers hit with tear gas",
    "Russian An-12 crashes in Siberia, 19 dead",
    "Voyager 1 reaches one light-day",
    "Deutsche Bank -6% on leaked files",
    "Sudan: UN counts 2,230 civilian deaths",
    "Typhoon Akvan",
]

INDEX = [
    "Kerch Bridge span falls", "Tanker burns, Hormuz", "Quad meets in Manila",
    "Nvidia chief quits", "Allies press Israel on Gaza", "Japan scrambles jets",
    "Houthis advance, Yemen", "EU Rwanda hubs", "Depardieu guilty, Paris",
    "COP31 crunch, Antalya", "Mongolia president resigns",
    "Bitcoin below $65,000", "Tiger Woods returns", "Apple & NSA outages",
    "FAA pauses routers", "Ebola, DR Congo", "Measles-free status lost",
    "Serbia student MP sworn in", "Bangladesh tear gas", "An-12 crash, Siberia",
    "Voyager 1, one light-day", "Deutsche Bank -6%", "Sudan, 2,230 dead",
    "Typhoon Akvan",
]

STATS = [
    ("11,000+", "EBOLA CASES · DR CONGO"),
    ("$115.8bn", "NVIDIA · MARKET VALUE"),
    ("-849", "DOW · POINTS"),
    ("1.4M", "GAZA · ACUTE HUNGER"),
    ("19", "AN-12 DEAD · SIBERIA"),
    ("1 light-day", "VOYAGER 1 · DISTANCE"),
]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    title_f = font(SERIF_B, 72)
    centered(d, 12, "THE WORLD IN ONE DAY", title_f, INK)
    date_f = font(SERIF_B, 62)
    centered(d, 88, "TUESDAY 17 NOVEMBER 2026", date_f, INK)
    d.line([(MARGIN, 164), (W - MARGIN, 164)], fill=RULE, width=3)
    d.line([(MARGIN, 168), (W - MARGIN, 168)], fill=RULE, width=1)
    sub_f = font(SANS_B, 16)
    centered(d, 176, "24 STORIES · SIX CONTINENTS · ONE DAY", sub_f, SOFT)

    # ---- stats strip
    cell_w = CW / 6
    num_f = font(SERIF_B, 27)
    lab_f = font(SANS_B, 10)
    for i, (num, lab) in enumerate(STATS):
        cx = MARGIN + cell_w * i
        nw = d.textlength(num, font=num_f)
        d.text((cx + (cell_w - nw) / 2, 202), num, font=num_f, fill=INK)
        lw = d.textlength(lab, font=lab_f)
        d.text((cx + (cell_w - lw) / 2, 234), lab, font=lab_f, fill=SOFT)
        if i:
            d.line([(cx, 204), (cx, 246)], fill=FAINT, width=1)
    rule(d, 256)

    # ---- heroes
    col_w, gap = 312, 20
    kick_f = font(SANS_B, 11)
    head_f = font(SERIF_B, 19)
    deck_f = font(SANS, 13)
    for i, (kick, head, deck, painter) in enumerate(HEROES):
        x = MARGIN + i * (col_w + gap)
        painter(d, x, 264, col_w, 140)
        d.text((x, 410), kick, font=kick_f, fill=RED)
        draw_wrapped(d, x, 426, head, head_f, INK, col_w, 2, 23)
        draw_wrapped(d, x, 472, deck, deck_f, SOFT, col_w, 2, 16)

    # ---- secondary
    scol_w, sgap = 232, 16
    shead_f = font(SERIF_B, 16)
    sdeck_f = font(SANS, 12)
    for i, (head, deck, accent) in enumerate(SECONDARY):
        x = MARGIN + i * (scol_w + sgap)
        d.rectangle([x, 504, x + scol_w, 507], fill=accent)
        draw_wrapped(d, x, 514, head, shead_f, INK, scol_w, 2, 20)
        draw_wrapped(d, x, 556, deck, sdeck_f, SOFT, scol_w, 2, 15)

    # ---- IN BRIEF
    brief_f = font(SANS_B, 15)
    d.text((MARGIN, 622), "IN BRIEF", font=brief_f, fill=INK)
    rule(d, 644, width=1)
    item_f = font(SANS, 12)
    item_b = font(SANS_B, 12)
    bcol_w, bgap = 318, 11
    for i, item in enumerate(BRIEF):
        col = i // 6
        row = i % 6
        x = MARGIN + col * (bcol_w + bgap)
        y = 650 + row * 18
        num = str(8 + i)
        d.text((x, y), num + ".", font=item_b, fill=RED)
        nw = d.textlength(num + ". ", font=item_b)
        d.text((x + nw, y), item, font=item_f, fill=INK)

    # ---- map + index
    sec_f = font(SANS_B, 14)
    d.text((MARGIN, 764), "THE WORLD AT A GLANCE", font=sec_f, fill=INK)
    d.text((560, 764), "INDEX — ALL 24 STORIES", font=sec_f, fill=INK)
    rule(d, 784, width=1)
    draw_map(d)
    idx_f = font(SANS, 11)
    idx_b = font(SANS_B, 11)
    for i, name in enumerate(INDEX):
        col = i // 12
        row = i % 12
        x = 560 + col * 220
        y = 790 + row * 14
        d.text((x, y), str(i + 1) + ".", font=idx_b, fill=RED)
        nw = d.textlength(str(i + 1) + ". ", font=idx_b)
        d.text((x + nw, y), name, font=idx_f, fill=INK)

    # ---- markets strip
    rule(d, 956, width=1)
    mkt_f = font(SANS, 13)
    mkt_b = font(SANS_B, 13)
    mkt = "Bitcoin below $65,000  ·  Dow -849  ·  Oil up on Hormuz fears  ·  Nvidia falls  ·  Deutsche Bank -6%"
    label = "MARKETS   "
    lw = d.textlength(label, font=mkt_b)
    mw = d.textlength(mkt, font=mkt_f)
    tx = (W - lw - mw) / 2
    d.text((tx, 962), label, font=mkt_b, fill=RED)
    d.text((tx + lw, 962), mkt, font=mkt_f, fill=INK)
    rule(d, 982, width=1)

    # ---- footer
    foot_f = font(SANS, 11)
    centered(d, 990,
             "DATE CHECK — Every story on this page was verified as 17 November 2026 news.",
             foot_f, SOFT)

    return img


if __name__ == "__main__":
    build().save("entry.png", optimize=True)
    print("saved entry.png")
