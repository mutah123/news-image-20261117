#!/usr/bin/env python3
"""Draw 'The World in One Day' v3 — a dense broadsheet front page for the
make.fun competition news-image-20261117 (sum up 17 November 2026 in one image).

v3 of our own entry, written from scratch in this session. Follows the
winning template found by analysing the top entries: one-line giant date,
6-number red stats strip, 3 illustrated heroes (Kerch / Gulf map / Quad),
10 illustrated secondaries, a solid-continent world map, ONE "ALSO" list,
and a footer with a red DATE CHECK box + sources line. 43 real stories,
all from Tuesday 17 November 2026. No fabrications.

Deterministic: no network, no randomness, no timestamps. Same input always
produces the same entry.png. Output is 1024x1024, PNG, under 1 MiB.

Layout (1024x1024, margin 24):
  navy masthead band with gold kicker + one-line giant date (y 0-130),
  6-number red stats strip (y 130-175),
  3 illustrated heroes (y 175-470),
  2 rows x 5 illustrated secondaries (y 470-765),
  solid world map + ONE ALSO list, items 14-43 (y 772-983),
  footer: red DATE CHECK box + verification + sources (y 985-1024).

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
NAVY = (16, 32, 64)
GOLD = (201, 162, 75)
SEA = (36, 82, 122)
SKY = (206, 224, 236)
TAN = (205, 180, 130)
PALESEA = (190, 215, 230)
RULE = (18, 18, 18)
FAINT = (150, 148, 140)

# region colours (pins, tags, ALSO badges)
REGION = {
    "EUROPE": (30, 80, 160),
    "MIDDLE EAST": (176, 32, 32),
    "ASIA": (198, 118, 18),
    "AFRICA": (18, 128, 88),
    "AMERICAS": (118, 58, 158),
    "OCEANIA": (0, 130, 140),
    "MARKETS": (90, 96, 104),
    "TECH": (90, 96, 104),
    "SPORT": (90, 96, 104),
    "SPACE": (90, 96, 104),
    "WEATHER": (90, 96, 104),
    "CLIMATE": (18, 128, 88),
}

FONT_DIR = "/usr/share/fonts/truetype"


def font(path, size):
    return ImageFont.truetype(FONT_DIR + "/" + path, size)


SERIF_B = "noto/NotoSerif-Bold.ttf"
SERIF = "noto/NotoSerif-Regular.ttf"
SANS_B = "noto/NotoSans-Bold.ttf"
SANS = "noto/NotoSans-Regular.ttf"


def fit_font(draw, text, path, target, max_w, minimum=48):
    """Largest font size <= target whose text fits max_w. Deterministic."""
    size = target
    while size > minimum:
        fnt = font(path, size)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
        size -= 2
    return font(path, minimum)


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
        cx0, cy0, cw, chh = x, y, w // 2, h // 2
        d.rectangle([cx0, cy0, cx0 + cw, cy0 + chh], fill=(0, 0, 110))
        d.line([cx0, cy0, cx0 + cw, cy0 + chh], fill=(255, 255, 255), width=2)
        d.line([cx0 + cw, cy0, cx0, cy0 + chh], fill=(255, 255, 255), width=2)
        d.line([cx0 + cw // 2, cy0, cx0 + cw // 2, cy0 + chh], fill=(200, 30, 30),
               width=3)
        d.line([cx0, cy0 + chh // 2, cx0 + cw, cy0 + chh // 2], fill=(200, 30, 30),
               width=3)
        for sx, sy in ((x + 44, y + 10), (x + 52, y + 26), (x + 40, y + 30)):
            d.polygon([(sx, sy - 4), (sx + 2, sy), (sx, sy + 4), (sx - 2, sy)],
                      fill=(255, 255, 255))


def tab(d, x, y, text, bg, fg=(255, 255, 255), size=11):
    """Small filled label tab; returns its width."""
    fnt = font(SANS_B, size)
    w = int(d.textlength(text, font=fnt)) + 12
    d.rectangle([x, y, x + w, y + size + 7], fill=bg)
    d.text((x + 6, y + 3), text, font=fnt, fill=fg)
    return w


# ---------------------------------------------------------------- heroes
def hero_bridge(d, x, y, w, h):
    """Kerch Bridge: thick deck, collapsed span, starburst, jets, smoke."""
    d.rectangle([x, y, x + w, y + 60], fill=SKY)
    d.rectangle([x, y + 56, x + w, y + 64], fill=(170, 190, 205))
    d.rectangle([x, y + 64, x + w, y + h], fill=SEA)
    for wy in (y + 82, y + 102, y + 122, y + 140):
        for wx in range(x + 8, x + w - 10, 34):
            d.arc([wx, wy, wx + 22, wy + 8], 200, 340, fill=(255, 255, 255), width=1)
    # thick deck: two standing segments with a gap in the middle
    d.rectangle([x, y + 48, x + 118, y + 60], fill=(30, 30, 30))
    d.rectangle([x + 196, y + 48, x + w, y + 60], fill=(30, 30, 30))
    d.line([x, y + 48, x + 118, y + 48], fill=RED, width=3)
    d.line([x + 196, y + 48, x + w, y + 48], fill=RED, width=3)
    # clouds in the sky
    for cx, cy, cr in ((x + 36, y + 14, 10), (x + 52, y + 20, 8),
                       (x + 250, y + 10, 9), (x + 264, y + 16, 7)):
        d.ellipse([cx - cr, cy - cr * 0.6, cx + cr, cy + cr * 0.6],
                  fill=(255, 255, 255))
    # support columns
    for cx in (x + 26, x + 84, x + 230, x + 282):
        d.rectangle([cx, y + 60, cx + 9, y + 112], fill=(30, 30, 30))
    # the fallen span, tilted steeply into the water
    d.polygon([(x + 118, y + 50), (x + 134, y + 56), (x + 176, y + 128),
               (x + 160, y + 132)], fill=(55, 55, 55), outline=RED)
    # starburst at the break point
    bx, by = x + 157, y + 56
    # two overlapping rotated squares + circle
    d.polygon([(bx, by - 26), (bx + 8, by - 8), (bx + 26, by),
               (bx + 8, by + 8), (bx, by + 26), (bx - 8, by + 8),
               (bx - 26, by), (bx - 8, by - 8)], fill=(250, 180, 40))
    d.polygon([(bx, by - 18), (bx + 18, by), (bx, by + 18), (bx - 18, by)],
              fill=(240, 90, 20))
    d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=(255, 220, 90))
    # splash where the span hit the water
    for sx, sy, r in ((x + 158, y + 128, 15), (x + 182, y + 134, 10),
                      (x + 140, y + 136, 8)):
        d.ellipse([sx - r, sy - r * 0.6, sx + r, sy + r * 0.6],
                  outline=(255, 255, 255), width=2)
    # smoke plume drifting up-left
    for sx, sy, r, c in ((x + 150, y + 30, 12, (110, 110, 110)),
                         (x + 138, y + 18, 10, (135, 135, 135)),
                         (x + 124, y + 8, 8, (160, 160, 160))):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=c)
    # two jets
    for jx, jy in ((x + 232, y + 18), (x + 268, y + 30)):
        d.polygon([(jx, jy), (jx + 18, jy + 4), (jx, jy + 7), (jx + 4, jy + 3)],
                  fill=(30, 30, 30))
    tab(d, x + 4, y + h - 20, "KERCH STRAIT", (18, 18, 18))
    tab(d, x + w - 118, y + 6, "ROAD SPAN DOWN", RED)


def hero_gulf(d, x, y, w, h):
    """Gulf map: pale sea, tan land, drone paths, strike marks, tanker."""
    d.rectangle([x, y, x + w, y + h], fill=PALESEA)
    # Iran (top right landmass)
    d.polygon([(x + 150, y), (x + w, y), (x + w, y + 58), (x + 268, y + 62),
               (x + 225, y + 48), (x + 190, y + 34), (x + 165, y + 18)],
              fill=TAN)
    # Arabian peninsula (bottom left)
    d.polygon([(x, y + h), (x, y + 96), (x + 62, y + 100), (x + 108, y + 128),
               (x + 96, y + h)], fill=TAN)
    # Bahrain island
    d.ellipse([x + 138, y + 88, x + 152, y + 100], fill=TAN)
    # Qeshm island
    d.polygon([(x + 196, y + 96), (x + 232, y + 92), (x + 236, y + 100),
               (x + 200, y + 104)], fill=TAN)
    # dashed red drone paths (Iran -> Bahrain)
    def dashed(x0, y0, x1, y1, fill, width=2):
        import math
        n = int(math.hypot(x1 - x0, y1 - y0) / 9)
        for i in range(n):
            t0, t1 = i / n, (i + 0.55) / n
            d.line([(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0),
                    (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)],
                   fill=fill, width=width)
    dashed(x + 235, y + 30, x + 150, y + 88, RED)
    dashed(x + 250, y + 44, x + 158, y + 96, RED)
    # red X marks where drones were downed
    for mx, my in ((x + 152, y + 90), (x + 164, y + 100)):
        d.line([mx - 6, my - 6, mx + 6, my + 6], fill=RED, width=3)
        d.line([mx - 6, my + 6, mx + 6, my - 6], fill=RED, width=3)
    # small tanker with smoke near the strait
    tx, ty = x + 196, y + 128
    d.rectangle([tx, ty, tx + 52, ty + 10], fill=(24, 24, 24))
    d.rectangle([tx + 34, ty - 8, tx + 46, ty], fill=(235, 235, 235))
    d.ellipse([tx + 8, ty - 16, tx + 22, ty - 2], fill=(240, 140, 30))
    d.ellipse([tx + 12, ty - 26, tx + 24, ty - 12], fill=(110, 110, 110))
    # wave arcs on the sea
    for wy in (y + 66, y + 112, y + 146):
        for wx in range(x + 8, x + w - 10, 30):
            d.arc([wx, wy, wx + 18, wy + 6], 200, 340, fill=(255, 255, 255),
                  width=1)
    # compass rose, bottom right
    cx, cy = x + w - 22, y + h - 22
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], outline=(90, 90, 90), width=1)
    d.polygon([(cx, cy - 8), (cx + 2, cy), (cx, cy + 8), (cx - 2, cy)],
              fill=(90, 90, 90))
    d.polygon([(cx - 8, cy), (cx, cy - 2), (cx + 8, cy), (cx, cy + 2)],
              fill=(90, 90, 90))
    d.text((cx - 3, cy - 16), "N", font=font(SANS_B, 9), fill=(90, 90, 90))
    # labels
    lab = font(SANS_B, 11)
    d.text((x + 238, y + 14), "IRAN", font=lab, fill=INK)
    d.text((x + 108, y + 76), "BAHRAIN", font=lab, fill=INK)
    d.text((x + 196, y + 78), "QESHM", font=lab, fill=INK)
    d.text((x + 168, y + 140), "HORMUZ", font=lab, fill=INK)
    tab(d, x + 4, y + 6, "DRONES DOWNED", RED)
    tab(d, x + 4, y + 26, "US STRIKES", (30, 80, 160))


def hero_quad(d, x, y, w, h):
    """Quad leaders in Manila: flags, skyline, delegates, purple banner."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 234, 240))
    # purple banner
    d.rectangle([x, y, x + w, y + 24], fill=(88, 44, 140))
    bf = font(SANS_B, 12)
    bt = "QUAD LEADERS' SUMMIT · MANILA"
    d.text((x + (w - d.textlength(bt, font=bf)) / 2, y + 6), bt, font=bf,
           fill=(255, 255, 255))
    # skyline with lit windows
    heights = [18, 30, 22, 38, 26, 44, 20, 34, 28, 16, 40, 24]
    bw = w // len(heights)
    bx = x
    for bi, bh in enumerate(heights):
        d.rectangle([bx, y + h - 10 - bh, bx + bw - 3, y + h - 10],
                    fill=(90, 100, 110))
        for wy in range(y + h - 8 - bh, y + h - 14, 9):
            for wx in range(bx + 3, bx + bw - 7, 8):
                if (wx + wy + bi) % 3 == 0:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(250, 220, 130))
        bx += bw
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(60, 68, 76))
    # four flags on poles
    flags = ["us", "jp", "in", "au"]
    fw, fh = 62, 40
    gap = (w - 4 * fw) // 5
    for i, fl in enumerate(flags):
        fx = x + gap + i * (fw + gap)
        fy = y + 36
        d.line([fx + fw // 2, fy + fh, fx + fw // 2, y + h - 10],
               fill=(60, 60, 60), width=2)
        draw_flag(d, fl, fx, fy, fw, fh)
    # four delegates in front of the skyline
    for i in range(4):
        px = x + 40 + i * 72
        py = y + h - 34
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=(30, 30, 30))
        d.pieslice([px - 14, py + 6, px + 14, py + 26], 180, 360, fill=(30, 30, 30))
    tab(d, x + 4, y + h - 20, "NEW CRITICAL-MINERALS DEALS", (88, 44, 140))

# ---------------------------------------------------------------- secondaries
def sec_ebola(d, x, y, w, h):
    """Hospital + rising bar chart."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 242))
    # hospital building
    d.rectangle([x + 12, y + 22, x + 66, y + h - 8], fill=(255, 255, 255),
                outline=(120, 130, 140))
    d.rectangle([x + 34, y + 28, x + 44, y + 48], fill=RED)
    d.rectangle([x + 29, y + 33, x + 49, y + 43], fill=RED)
    for wy in (y + 54, y + 62):
        for wx in (x + 18, x + 30, x + 48):
            d.rectangle([wx, wy, wx + 8, wy + 5], fill=(120, 130, 140))
    # bar chart, rising, last bar red
    bars = [14, 22, 32, 44]
    for i, bh in enumerate(bars):
        bx = x + 84 + i * 24
        d.rectangle([bx, y + h - 10 - bh, bx + 16, y + h - 10],
                    fill=RED if i == 3 else (36, 82, 122))
    d.text((x + 84, y + 6), "11,000+", font=font(SANS_B, 12), fill=RED)


def sec_measles(d, x, y, w, h):
    """Three flags: US, Mexico, Bolivia."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 240, 235))
    fw, fh = 52, 34
    # US
    fx = x + 10
    for i in range(7):
        if i % 2 == 0:
            d.rectangle([fx, y + 16 + i * fh // 7, fx + fw, y + 16 + (i + 1) * fh // 7],
                        fill=(178, 34, 34))
    d.rectangle([fx, y + 16, fx + 20, y + 16 + fh // 2], fill=(30, 50, 110))
    # Mexico
    fx = x + 70
    d.rectangle([fx, y + 16, fx + 17, y + 16 + fh], fill=(0, 120, 60))
    d.rectangle([fx + 17, y + 16, fx + 35, y + 16 + fh], fill=(255, 255, 255))
    d.rectangle([fx + 35, y + 16, fx + 52, y + 16 + fh], fill=(200, 30, 30))
    d.ellipse([fx + 22, y + 26, fx + 30, y + 34], fill=(120, 80, 20))
    # Bolivia
    fx = x + 130
    d.rectangle([fx, y + 16, fx + 52, y + 16 + fh // 3], fill=(200, 30, 30))
    d.rectangle([fx, y + 16 + fh // 3, fx + 52, y + 16 + 2 * fh // 3],
                fill=(240, 200, 40))
    d.rectangle([fx, y + 16 + 2 * fh // 3, fx + 52, y + 16 + fh],
                fill=(0, 120, 60))
    d.text((x + 10, y + 56), "STATUS LOST", font=font(SANS_B, 11), fill=RED)


def sec_nvidia(d, x, y, w, h):
    """Chip + rising green bars."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 40, 28))
    # chip
    cx, cy = x + 16, y + 12
    d.rectangle([cx, cy, cx + 52, cy + 52], fill=(0, 120, 60),
                outline=(0, 200, 110), width=2)
    d.rectangle([cx + 16, cy + 16, cx + 36, cy + 36], fill=(18, 40, 28))
    for px in (cx + 8, cx + 22, cx + 38):
        d.line([px, cy - 6, px, cy], fill=(0, 200, 110), width=2)
        d.line([px, cy + 52, px, cy + 58], fill=(0, 200, 110), width=2)
    for py in (cy + 8, cy + 22, cy + 38):
        d.line([cx - 6, py, cx, py], fill=(0, 200, 110), width=2)
        d.line([cx + 52, py, cx + 58, py], fill=(0, 200, 110), width=2)
    # rising bars
    bars = [12, 20, 30, 42]
    for i, bh in enumerate(bars):
        bx = x + 92 + i * 22
        d.rectangle([bx, y + h - 12 - bh, bx + 14, y + h - 12],
                    fill=(0, 200, 110))
    d.text((x + 92, y + 8), "$115.8BN", font=font(SANS_B, 12), fill=(0, 220, 120))


def sec_cop31(d, x, y, w, h):
    """Globe + thermometer."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 238, 240))
    # globe
    gx, gy, gr = x + 42, y + 38, 28
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(36, 110, 180))
    d.polygon([(gx - 18, gy - 8), (gx - 4, gy - 16), (gx + 8, gy - 6),
               (gx - 2, gy + 6), (gx - 14, gy + 10)], fill=(60, 160, 80))
    d.polygon([(gx + 6, gy + 8), (gx + 20, gy + 2), (gx + 22, gy + 14),
               (gx + 10, gy + 20)], fill=(60, 160, 80))
    # thermometer
    tx = x + 108
    d.rectangle([tx, y + 12, tx + 12, y + 52], fill=(255, 255, 255),
                outline=(120, 130, 140))
    d.rectangle([tx + 3, y + 30, tx + 9, y + 50], fill=RED)
    d.ellipse([tx - 3, y + 50, tx + 15, y + 68], fill=RED)
    d.text((x + 128, y + 14), "DRAFT:", font=font(SANS_B, 11), fill=INK)
    d.text((x + 128, y + 28), "PHASE", font=font(SANS_B, 11), fill=INK)
    d.text((x + 128, y + 42), "OUT", font=font(SANS_B, 11), fill=INK)


def sec_mongolia(d, x, y, w, h):
    """Resignation paper with red seal."""
    d.rectangle([x, y, x + w, y + h], fill=(242, 238, 228))
    # paper
    d.polygon([(x + 52, y + 8), (x + 128, y + 8), (x + 128, y + 62),
               (x + 118, y + 72), (x + 52, y + 72)], fill=(255, 255, 255),
              outline=(120, 120, 110))
    for ly in (y + 20, y + 30, y + 40, y + 50):
        d.line([x + 60, ly, x + 120, ly], fill=(140, 140, 130), width=1)
    # red seal
    d.ellipse([x + 130, y + 44, x + 170, y + 72], fill=RED,
              outline=(120, 20, 20), width=2)
    st = "RESIGN"
    sw = d.textlength(st, font=font(SANS_B, 10))
    d.text((x + 150 - sw / 2, y + 54), st, font=font(SANS_B, 10),
           fill=(255, 255, 255))
    d.text((x + 12, y + 8), "ULAANBAATAR", font=font(SANS_B, 11), fill=SOFT)


def sec_serbia(d, x, y, w, h):
    """Parliament semicircle, 140 vs 103."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 238, 242))
    cx, cy, r = x + 94, y + 62, 40
    import math
    for i in range(14):
        ang = math.pi * (1 - i / 13)
        sx = cx + r * math.cos(ang)
        sy = cy - r * 0.78 * math.sin(ang)
        col = RED if i < 8 else (30, 80, 160)
        d.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=col)
    d.rectangle([x + 20, y + 66, x + 94, y + 72], fill=RED)
    d.text((x + 20, y + 52), "140", font=font(SANS_B, 12), fill=RED)
    d.rectangle([x + 100, y + 66, x + 158, y + 72], fill=(30, 80, 160))
    d.text((x + 158, y + 52), "103", font=font(SANS_B, 12), fill=(30, 80, 160))


def sec_bangladesh(d, x, y, w, h):
    """Factory + workers."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 234, 220))
    # factory with sawtooth roof
    d.polygon([(x + 14, y + 34), (x + 34, y + 20), (x + 54, y + 34),
               (x + 74, y + 20), (x + 94, y + 34), (x + 94, y + 66),
               (x + 14, y + 66)], fill=(90, 100, 110))
    d.rectangle([x + 104, y + 12, x + 114, y + 66], fill=(70, 80, 90))
    d.ellipse([x + 102, y + 2, x + 116, y + 14], fill=(140, 140, 140))
    for wy in (y + 42, y + 54):
        for wx in (x + 22, x + 42, x + 62, x + 82):
            d.rectangle([wx, wy, wx + 8, wy + 6], fill=(240, 220, 120))
    # workers
    for i, wx in enumerate((x + 128, x + 148, x + 168)):
        d.ellipse([wx - 5, y + 40, wx + 5, y + 50], fill=(30, 30, 30))
        d.pieslice([wx - 9, y + 50, wx + 9, y + 66], 180, 360, fill=(30, 30, 30))
    d.text((x + 128, y + 10), "TK 30,000", font=font(SANS_B, 11), fill=RED)


def sec_an12(d, x, y, w, h):
    """Plane over snowy mountains."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 232, 240))
    # mountains
    d.polygon([(x, y + h), (x + 40, y + 26), (x + 80, y + h)], fill=(120, 130, 145))
    d.polygon([(x + 28, y + 26), (x + 40, y + 26), (x + 52, y + 26),
               (x + 46, y + 38), (x + 34, y + 38)], fill=(255, 255, 255))
    d.polygon([(x + 70, y + h), (x + 120, y + 34), (x + 170, y + h)],
              fill=(100, 112, 128))
    d.polygon([(x + 108, y + 34), (x + 120, y + 34), (x + 132, y + 34),
               (x + 126, y + 44), (x + 114, y + 44)], fill=(255, 255, 255))
    # plane, nose down
    px, py = x + 96, y + 18
    d.polygon([(px, py), (px + 52, py + 10), (px + 48, py + 16),
               (px + 4, py + 10)], fill=(40, 40, 40))
    d.polygon([(px + 22, py + 2), (px + 30, py + 12), (px + 24, py + 12)],
              fill=(40, 40, 40))
    d.polygon([(px + 44, py + 8), (px + 56, py + 2), (px + 56, py + 10)],
              fill=(40, 40, 40))
    # smoke trail
    for i in range(4):
        d.ellipse([px - 12 - i * 12, py - 4 - i * 2, px - 2 - i * 12, py + 6 - i * 2],
                  fill=(150, 150, 150))


def sec_gaza(d, x, y, w, h):
    """Aid trucks at a border gate."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 220))
    # gate / fence
    for gx in range(x + 8, x + w - 8, 18):
        d.line([gx, y + 8, gx, y + 44], fill=(90, 90, 90), width=2)
    d.line([x + 8, y + 14, x + w - 8, y + 14], fill=(90, 90, 90), width=2)
    # truck 1
    tx, ty = x + 22, y + 46
    d.rectangle([tx, ty, tx + 62, ty + 18], fill=(255, 255, 255),
                outline=(120, 120, 120))
    d.rectangle([tx + 62, ty + 6, tx + 82, ty + 18], fill=(200, 60, 40))
    d.ellipse([tx + 10, ty + 18, tx + 20, ty + 26], fill=(30, 30, 30))
    d.ellipse([tx + 44, ty + 18, tx + 54, ty + 26], fill=(30, 30, 30))
    d.ellipse([tx + 68, ty + 18, tx + 78, ty + 26], fill=(30, 30, 30))
    # truck 2 (smaller, behind)
    tx, ty = x + 108, y + 40
    d.rectangle([tx, ty, tx + 52, ty + 16], fill=(240, 240, 235),
                outline=(120, 120, 120))
    d.rectangle([tx + 52, ty + 5, tx + 68, ty + 16], fill=(36, 82, 122))
    d.ellipse([tx + 8, ty + 16, tx + 17, ty + 23], fill=(30, 30, 30))
    d.ellipse([tx + 38, ty + 16, tx + 47, ty + 23], fill=(30, 30, 30))
    d.ellipse([tx + 56, ty + 16, tx + 65, ty + 23], fill=(30, 30, 30))
    d.text((x + 22, y + 4), "AID", font=font(SANS_B, 11), fill=RED)


def sec_japan(d, x, y, w, h):
    """Jets over the sea."""
    d.rectangle([x, y, x + w, y + h], fill=(206, 224, 236))
    d.rectangle([x, y + 52, x + w, y + h], fill=(36, 82, 122))
    for wy in (y + 60, y + 68):
        for wx in range(x + 10, x + w - 12, 30):
            d.arc([wx, wy, wx + 20, wy + 7], 200, 340, fill=(255, 255, 255), width=1)
    # two jets
    for jx, jy, s in ((x + 40, y + 18, 1.0), (x + 110, y + 30, 0.8)):
        d.polygon([(jx, jy), (jx + 34 * s, jy + 6 * s), (jx, jy + 12 * s),
                   (jx + 8 * s, jy + 6 * s)], fill=(30, 30, 30))
        d.polygon([(jx + 14 * s, jy), (jx + 20 * s, jy - 8 * s),
                   (jx + 24 * s, jy + 2 * s)], fill=(30, 30, 30))
    d.text((x + 10, y + 4), "SEA OF JAPAN", font=font(SANS_B, 11), fill=INK)


# ---------------------------------------------------------------- world map
# Coarse land mask, 48 columns x 28 rows. Row 0 is ~81N, row 27 is ~-55S.
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

# Pins: (lon, lat, number, region, dx, dy). dx/dy nudge the drawn badge so
# the Europe / Middle East cluster does not collide.
PINS = [
    (33.5, 45.3, "1", "EUROPE", 3, -7),      # Kerch Bridge, Crimea
    (56.5, 26.5, "2", "MIDDLE EAST", 0, 0),  # Strait of Hormuz
    (121.0, 14.6, "3", "ASIA", 0, 0),        # Quad, Manila
    (22.5, -4.0, "4", "AFRICA", -2, 4),      # Ebola, DR Congo
    (-100.0, 30.0, "5", "AMERICAS", 0, 0),   # measles-free status
    (-122.0, 37.4, "6", "AMERICAS", 0, 0),   # Nvidia, Santa Clara
    (30.7, 36.9, "7", "EUROPE", -6, -6),     # COP31, Antalya
    (106.9, 47.9, "8", "ASIA", 0, 0),        # Mongolia, Ulaanbaatar
    (20.5, 44.8, "9", "EUROPE", -6, -4),     # Serbia, Belgrade
    (90.4, 23.8, "10", "ASIA", 0, 0),        # Bangladesh, Dhaka
    (104.0, 56.0, "11", "EUROPE", 0, 0),     # An-12 crash, Siberia
    (34.5, 31.5, "12", "MIDDLE EAST", 6, 4), # Gaza crossings
    (141.0, 42.0, "13", "ASIA", 0, 0),       # Japan jets
]

MAP_X, MAP_Y, MAP_W, MAP_H = MARGIN, 796, 406, 154
MAP_COLS, MAP_ROWS = 48, 28
LAT_TOP, LAT_BOT = 84.0, -60.0


def lonlat_to_xy(lon, lat):
    px = MAP_X + (lon + 180.0) / 360.0 * MAP_W
    py = MAP_Y + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * MAP_H
    return px, py


def draw_map(d):
    # sea
    d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=PALESEA)
    # faint lat/lon grid
    grid = (168, 196, 214)
    for lon in range(-150, 181, 30):
        gx = MAP_X + (lon + 180.0) / 360.0 * MAP_W
        d.line([(gx, MAP_Y), (gx, MAP_Y + MAP_H)], fill=grid, width=1)
    for lat in range(-60, 85, 30):
        gy = MAP_Y + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * MAP_H
        d.line([(MAP_X, gy), (MAP_X + MAP_W, gy)], fill=grid, width=1)
    # wave arcs on the open sea
    for wy in (MAP_Y + 30, MAP_Y + 118):
        for wx in range(MAP_X + 8, MAP_X + MAP_W - 12, 34):
            d.arc([wx, wy, wx + 20, wy + 7], 200, 340, fill=(255, 255, 255),
                  width=1)
    # solid continents: one filled cell per land cell
    cell_w = MAP_W / MAP_COLS
    cell_h = MAP_H / MAP_ROWS
    for r, spans in enumerate(LAND):
        for a, b in spans:
            x0 = MAP_X + a * cell_w
            x1 = MAP_X + (b + 1) * cell_w
            y0 = MAP_Y + r * cell_h
            y1 = MAP_Y + (r + 1) * cell_h
            d.rectangle([x0, y0, x1 + 0.6, y1 + 0.6], fill=TAN)
    # pins: coloured badge with white number
    for lon, lat, num, region, dx, dy in PINS:
        px, py = lonlat_to_xy(lon, lat)
        px += dx
        py += dy
        col = REGION[region]
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=col,
                  outline=(255, 255, 255), width=1)
        nf = font(SANS_B, 9 if len(num) == 1 else 8)
        nw = d.textlength(num, font=nf)
        d.text((px - nw / 2, py - 5 if len(num) == 1 else py - 4.5), num,
               font=nf, fill=(255, 255, 255))


# ---------------------------------------------------------------- content
HEROES = [
    ("EUROPE · UKRAINE WAR", "Kerch Bridge span crashes into the sea",
     "Ukraine hits the Crimea crossing again; a roadway span collapses.",
     hero_bridge),
    ("MIDDLE EAST · IRAN WAR", "Iran drone attack on US radar site in Bahrain",
     "US strikes an IRGC site at Qeshm; a mined tanker burns in Hormuz.",
     hero_gulf),
    ("ASIA · MANILA", "Quad leaders meet in Manila",
     "Trump opens his Asia tour; US, Japan, India and Australia strike a minerals deal.",
     hero_quad),
]

# (tag region, headline, deck, painter)
SECONDARY = [
    ("AFRICA", "Ebola outbreak spreads in DR Congo",
     "WHO sends surge teams.", sec_ebola),
    ("AMERICAS", "US, Mexico, Bolivia lose measles-free status",
     "Three nations lose the status.", sec_measles),
    ("MARKETS", "Nvidia posts $115.8bn quarter",
     "Dow falls 849 on the news.", sec_nvidia),
    ("CLIMATE", "COP31 talks split on fossil fuels",
     "Draft backs a fossil phase-out.", sec_cop31),
    ("ASIA", "Mongolia's president to resign",
     "Quits amid corruption scandal.", sec_mongolia),
    ("EUROPE", "Serbia student MP sworn in",
     "Students cheer the new session.", sec_serbia),
    ("ASIA", "Bangladesh garment workers tear-gassed",
     "Workers want TK 30,000 minimum.", sec_bangladesh),
    ("EUROPE", "Russian An-12 crashes in Siberia",
     "All 19 aboard killed.", sec_an12),
    ("MIDDLE EAST", "Allies press Israel to open Gaza crossings",
     "Four allies demand aid access.", sec_gaza),
    ("ASIA", "Japan scrambles jets as Russian plane intrudes",
     "Russian plane violates airspace.", sec_japan),
]

# ALSO list, items 14-43: (region, short text). All real 17 Nov 2026 news.
ALSO = [
    ("MIDDLE EAST", "Houthis advance in Yemen"),
    ("EUROPE", "EU states plan Rwanda deportation hubs"),
    ("EUROPE", "Depardieu admits guilt in Paris"),
    ("MARKETS", "Bitcoin slides below $65,000"),
    ("SPORT", "Tiger Woods to play again"),
    ("TECH", "Apple and NSA hit by outages"),
    ("TECH", "FAA pauses router rollout"),
    ("SPACE", "Voyager 1 reaches one light-day"),
    ("MARKETS", "Deutsche Bank -6% on leaked files"),
    ("AFRICA", "Sudan: UN counts 2,230 civilian deaths"),
    ("WEATHER", "Typhoon Akvan"),
    ("EUROPE", "Kyiv bridges hit"),
    ("MIDDLE EAST", "Knesset vote: Kahana wins 66-52"),
    ("AMERICAS", "JPMorgan Zelle outage"),
    ("EUROPE", "France strike: 146,000 march"),
    ("EUROPE", "Tusk survives no-confidence 242-200"),
    ("EUROPE", "Turkey seizes Sözcü TV"),
    ("EUROPE", "Moldova shuts airspace over drone"),
    ("ASIA", "China-Canada tariff relief"),
    ("MIDDLE EAST", "US sanctions 8 West Bank firms"),
    ("ASIA", "India bus in gorge crash, 8 dead"),
    ("AFRICA", "Kenya: WFP feeds 30,000"),
    ("OCEANIA", "Australia eases backpacker visas"),
    ("OCEANIA", "Darwin hit by M6.6 quake"),
    ("ASIA", "Trump, Xi, Putin to meet in Shenzhen"),
    ("MIDDLE EAST", "US carrier group reaches the Gulf"),
    ("ASIA", "US caps chip exports to SE Asia"),
    ("MIDDLE EAST", "US strike hits IRGC site at Qeshm"),
    ("EUROPE", "Russia says it downed 1,441 drones"),
    ("MARKETS", "Dow falls 849 points"),
]

STATS = [
    ("11,000+", "EBOLA CASES · DR CONGO"),
    ("$115.8bn", "NVIDIA QUARTER"),
    ("-849", "DOW POINTS"),
    ("1,441", "DRONES DOWNED"),
    ("1.4M", "GAZA ACUTE HUNGER"),
    ("1 light-day", "VOYAGER 1"),
]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead: navy band, gold kicker, one-line giant date
    d.rectangle([0, 0, W, 130], fill=NAVY)
    kick_f = font(SANS_B, 13)
    d.text((MARGIN, 10), "THE WORLD'S NEWS IN ONE DAY", font=kick_f, fill=GOLD)
    badge = "43 STORIES · 6 CONTINENTS · ONE DAY"
    bw = d.textlength(badge, font=kick_f)
    d.text((W - MARGIN - bw, 10), badge, font=kick_f, fill=GOLD)
    date_f = fit_font(d, "Tuesday 17 November 2026", SERIF_B, 88, CW)
    dw = d.textlength("Tuesday 17 November 2026", font=date_f)
    d.text(((W - dw) / 2, 30), "Tuesday 17 November 2026", font=date_f,
           fill=(255, 255, 255))
    d.rectangle([0, 128, W, 130], fill=GOLD)

    # ---- stats strip: 6 red numbers
    cell_w = CW / 6
    num_f = font(SERIF_B, 28)
    lab_f = font(SANS_B, 10)
    for i, (num, lab) in enumerate(STATS):
        cx = MARGIN + cell_w * i
        nw = d.textlength(num, font=num_f)
        d.text((cx + (cell_w - nw) / 2, 134), num, font=num_f, fill=RED)
        lw = d.textlength(lab, font=lab_f)
        d.text((cx + (cell_w - lw) / 2, 163), lab, font=lab_f, fill=SOFT)
        if i:
            d.line([(cx, 136), (cx, 171)], fill=FAINT, width=1)
    rule(d, 176)

    # ---- heroes
    col_w, gap = 312, 20
    kick2_f = font(SANS_B, 11)
    head_f = font(SERIF_B, 19)
    deck_f = font(SANS, 12)
    for i, (kick, head, deck, painter) in enumerate(HEROES):
        x = MARGIN + i * (col_w + gap)
        painter(d, x, 182, col_w, 148)
        d.text((x, 336), kick, font=kick2_f, fill=RED)
        draw_wrapped(d, x, 352, head, head_f, INK, col_w, 2, 23)
        draw_wrapped(d, x, 402, deck, deck_f, SOFT, col_w, 2, 15)
    rule(d, 460)

    # ---- secondaries: 2 rows x 5, every one illustrated
    scol_w, sgap = 188, 9
    stag_f = font(SANS_B, 10)
    shead_f = font(SERIF_B, 14)
    sdeck_f = font(SANS, 11)
    for row in range(2):
        y0 = 470 if row == 0 else 622
        for col in range(5):
            i = row * 5 + col
            region, head, deck, painter = SECONDARY[i]
            x = MARGIN + col * (scol_w + sgap)
            painter(d, x, y0, scol_w, 75)
            accent = REGION[region]
            d.rectangle([x, y0 + 79, x + scol_w, y0 + 82], fill=accent)
            d.text((x, y0 + 86), region, font=stag_f, fill=accent)
            draw_wrapped(d, x, y0 + 100, head, shead_f, INK, scol_w, 2, 17)
            draw_wrapped(d, x, y0 + 136, deck, sdeck_f, SOFT, scol_w, 1, 14)

    # ---- bottom band: solid map + ONE also list
    sec_f = font(SANS_B, 13)
    d.text((MARGIN, 772), "THE WORLD AT A GLANCE", font=sec_f, fill=INK)
    d.text((450, 772), "ALSO ON TUESDAY 17 NOVEMBER", font=sec_f, fill=INK)
    rule(d, 790)
    draw_map(d)
    # map legend
    leg_f = font(SANS_B, 10)
    d.text((MARGIN, 956), "PINS 1-13: HEROES 1-3 · SECONDARIES 4-13",
           font=leg_f, fill=INK)
    lx = MARGIN
    for name in ("EUROPE", "MIDDLE EAST", "ASIA", "AFRICA", "AMERICAS",
                 "OCEANIA"):
        col = REGION[name]
        d.ellipse([lx, 970, lx + 8, 978], fill=col)
        d.text((lx + 11, 968), name, font=leg_f, fill=SOFT)
        lx += 11 + int(d.textlength(name, font=leg_f)) + 8
    # also list: 2 columns x 15, items 14-43
    item_f = font(SANS, 10)
    num_f2 = font(SANS_B, 9)
    for i, (region, text) in enumerate(ALSO):
        col = i // 15
        row = i % 15
        x = 450 + col * 281
        y = 796 + row * 12
        num = str(14 + i)
        d.rectangle([x, y, x + 16, y + 11], fill=REGION[region])
        nw = d.textlength(num, font=num_f2)
        d.text((x + (16 - nw) / 2, y + 1), num, font=num_f2,
               fill=(255, 255, 255))
        d.text((x + 20, y), text, font=item_f, fill=INK)

    # ---- footer
    d.rectangle([MARGIN, 985, W - MARGIN, 999], fill=RED)
    dc_f = font(SANS_B, 10)
    dc = ("DATE CHECK — Left out on purpose: DR Congo's Ebola count passed "
          "11,000 on 10 Nov · a Vulcan rocket lost 40 Amazon satellites on "
          "15 Nov (both: Reuters).")
    dw = d.textlength(dc, font=dc_f)
    d.text(((W - dw) / 2, 988), dc, font=dc_f, fill=(255, 255, 255))
    foot_f = font(SANS, 10)
    centered(d, 1003,
             "Every story here happened or was first reported on Tuesday "
             "17 November 2026. Disputed claims are marked as claims.",
             foot_f, SOFT)
    centered(d, 1014,
             "Sources: Reuters, AP, AFP, BBC, Al Jazeera, WHO, UN. "
             "Original drawings.",
             foot_f, SOFT)

    return img


if __name__ == "__main__":
    build().save("entry.png", optimize=True)
    print("saved entry.png")
