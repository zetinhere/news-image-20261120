#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news image (1024x1024 PNG).

Own work: every shape and word drawn with PIL from the news researched
on 20 Nov 2026 (US Senate war-powers vote + Hormuz tanker mine, Anthropic
+17% on debut as markets slide, Europe ready for Russia talks, COP31 draft
drops fossil fuels, Storm Dana evacuation in India, ICJ genocide ruling).
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 20            # outer margin
GAP = 14
COLS, ROWS = 2, 3
HEADER_H = 150
FOOTER_H = 74

PAPER = (247, 243, 234)
INK = (24, 24, 28)
RED = (178, 34, 34)
MUTED = (90, 86, 78)
CARD_BG = (255, 255, 255)
LINE = (200, 192, 176)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_in(d, xy, s, fnt, fill=INK, anchor="la"):
    d.text(xy, s, font=fnt, fill=fill, anchor=anchor)

# ---------- scene drawings (each takes draw + box) ----------
def scene_senate(d, x0, y0, x1, y1):
    # US Capitol dome in navy + a tanker on dark Gulf water with a mine
    d.rectangle([x0, y0, x1, y1], fill=(18, 44, 78))
    w, h = x1 - x0, y1 - y0
    # capitol dome, left
    cx = x0 + w * 0.24
    base = y0 + h * 0.66
    d.rectangle([cx - 40, base - 44, cx + 40, base], fill=(235, 230, 220))
    d.ellipse([cx - 30, base - 70, cx + 30, base - 40], fill=(235, 230, 220))
    d.rectangle([cx - 4, base - 82, cx + 4, base - 66], fill=(235, 230, 220))
    d.rectangle([cx - 56, base, cx + 56, base + 8], fill=(200, 195, 185))
    # gulf water, right
    d.rectangle([x0 + w * 0.52, y0 + h * 0.52, x1, y1], fill=(10, 60, 90))
    # tanker hull
    tx0, ty = x0 + w * 0.56, y0 + h * 0.60
    d.rectangle([tx0, ty, tx0 + w * 0.36, ty + 16], fill=(150, 40, 30))
    d.rectangle([tx0 + w * 0.05, ty - 18, tx0 + w * 0.12, ty], fill=(120, 30, 22))
    d.rectangle([tx0 + w * 0.24, ty - 12, tx0 + w * 0.30, ty], fill=(120, 30, 22))
    # mine with spikes
    mx, my = x0 + w * 0.88, y0 + h * 0.72
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        d.line([mx, my, mx + 16 * math.cos(a), my + 16 * math.sin(a)],
               fill=(255, 200, 60), width=3)
    d.ellipse([mx - 9, my - 9, mx + 9, my + 9], fill=(40, 40, 40))
    # flame
    d.polygon([(tx0 + w * 0.10, ty - 18), (tx0 + w * 0.14, ty - 34),
               (tx0 + w * 0.18, ty - 18)], fill=(255, 160, 40))

def scene_markets(d, x0, y0, x1, y1):
    # stock chart: one green line climbing (Anthropic), one red line falling
    d.rectangle([x0, y0, x1, y1], fill=(16, 26, 22))
    w, h = x1 - x0, y1 - y0
    for i in range(5):
        gy = y0 + h * (0.15 + i * 0.18)
        d.line([x0 + 8, gy, x1 - 8, gy], fill=(45, 60, 50), width=1)
    # falling red line (S&P / Nikkei)
    pts = [(0.05, 0.30), (0.25, 0.38), (0.45, 0.50), (0.65, 0.62),
           (0.85, 0.74), (0.97, 0.82)]
    for (fx1, fy1), (fx2, fy2) in zip(pts, pts[1:]):
        d.line([x0 + fx1 * w, y0 + fy1 * h, x0 + fx2 * w, y0 + fy2 * h],
               fill=(220, 70, 60), width=4)
    # rising green line (Anthropic)
    pts2 = [(0.05, 0.78), (0.25, 0.70), (0.45, 0.58), (0.65, 0.42),
            (0.85, 0.28), (0.97, 0.16)]
    for (fx1, fy1), (fx2, fy2) in zip(pts2, pts2[1:]):
        d.line([x0 + fx1 * w, y0 + fy1 * h, x0 + fx2 * w, y0 + fy2 * h],
               fill=(60, 200, 110), width=4)
    # arrow heads
    d.polygon([(x1 - 14, y0 + h * 0.16), (x1 - 30, y0 + h * 0.20),
               (x1 - 18, y0 + h * 0.26)], fill=(60, 200, 110))
    d.polygon([(x1 - 14, y0 + h * 0.82), (x1 - 30, y0 + h * 0.78),
               (x1 - 18, y0 + h * 0.72)], fill=(220, 70, 60))

def scene_berlin(d, x0, y0, x1, y1):
    # Berlin TV tower at dusk + two flags, a table with a handshake
    d.rectangle([x0, y0, x1, y1], fill=(232, 214, 178))
    w, h = x1 - x0, y1 - y0
    cx = x0 + w * 0.50
    base = y0 + h * 0.78
    d.rectangle([cx - 5, y0 + h * 0.30, cx + 5, base], fill=(90, 90, 95))
    d.ellipse([cx - 26, y0 + h * 0.16, cx + 26, y0 + h * 0.34],
              fill=(150, 160, 175))
    d.ellipse([cx - 12, y0 + h * 0.21, cx + 12, y0 + h * 0.29],
              fill=(255, 210, 90))
    d.line([cx, y0 + h * 0.05, cx, y0 + h * 0.16], fill=(90, 90, 95), width=3)
    # rooftops
    for fx, fh in [(0.03, 0.30), (0.16, 0.42), (0.68, 0.36), (0.82, 0.28)]:
        d.rectangle([x0 + fx * w, base - fh * h, x0 + (fx + 0.13) * w, base],
                    fill=(120, 80, 60))
    # two flags (EU blue, Russian white-blue-red) on a table line
    d.rectangle([x0, base, x1, base + 4], fill=(90, 70, 50))
    for i, cols in enumerate([[(30, 60, 160), (30, 60, 160), (30, 60, 160)],
                              [(255, 255, 255), (30, 90, 180), (200, 40, 40)]]):
        fx = x0 + w * (0.20 + i * 0.42)
        fy = y0 + h * 0.60
        d.line([fx, fy, fx, fy + 40], fill=(60, 60, 60), width=3)
        for j, c in enumerate(cols):
            d.rectangle([fx, fy + j * 9, fx + 44, fy + (j + 1) * 9], fill=c)
        d.ellipse([fx + 18, fy + 9, fx + 26, fy + 17], fill=(255, 220, 80))

def scene_cop31(d, x0, y0, x1, y1):
    # globe half in green, half grey smoke from a stack; a red line strikes the word out
    d.rectangle([x0, y0, x1, y1], fill=(176, 216, 228))
    w, h = x1 - x0, y1 - y0
    cx, cy = x0 + w * 0.38, y0 + h * 0.52
    r = h * 0.40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 140, 200))
    d.ellipse([cx - r * 0.55, cy - r * 0.75, cx + r * 0.25, cy - r * 0.1],
              fill=(80, 180, 90))
    d.ellipse([cx - r * 0.2, cy + r * 0.15, cx + r * 0.7, cy + r * 0.75],
              fill=(80, 180, 90))
    # smokestack
    sx = x0 + w * 0.74
    d.polygon([(sx, y0 + h * 0.30), (sx + 30, y0 + h * 0.30),
               (sx + 38, y1), (sx - 8, y1)], fill=(70, 70, 78))
    for i, (ox, oy, rr) in enumerate([(0, 0, 9), (14, -12, 12), (-8, -22, 11),
                                      (10, -34, 13)]):
        d.ellipse([sx + 13 + ox - rr, y0 + h * 0.28 + oy - rr,
                   sx + 13 + ox + rr, y0 + h * 0.28 + oy + rr],
                  fill=(150, 150, 155))
    # red strike line across the scene
    d.line([x0 + 8, y0 + h * 0.82, x1 - 8, y0 + h * 0.18], fill=RED, width=6)

def scene_storm(d, x0, y0, x1, y1):
    # cyclone spiral over a dark sea, coastline with shelters below
    d.rectangle([x0, y0, x1, y1], fill=(24, 52, 84))
    w, h = x1 - x0, y1 - y0
    cx, cy = x0 + w * 0.50, y0 + h * 0.46
    for k in range(5):
        r0 = 8 + k * 13
        for a in range(0, 300, 6):
            ang = math.radians(a + k * 52)
            ang2 = math.radians(a + 6 + k * 52)
            d.line([cx + r0 * math.cos(ang), cy + r0 * 0.8 * math.sin(ang),
                    cx + (r0 + 2) * math.cos(ang2),
                    cy + (r0 + 2) * 0.8 * math.sin(ang2)],
                   fill=(240, 240, 245), width=5)
    d.ellipse([cx - 8, cy - 7, cx + 8, cy + 7], fill=(255, 210, 90))
    # coastline + shelter tents
    d.rectangle([x0, y0 + h * 0.82, x1, y1], fill=(210, 190, 150))
    for i in range(4):
        tx = x0 + w * (0.10 + i * 0.22)
        ty = y0 + h * 0.86
        d.polygon([(tx, ty), (tx + 22, ty), (tx + 11, ty - 16)],
                  fill=(200, 60, 50))
        d.rectangle([tx + 2, ty, tx + 20, ty + 10], fill=(245, 240, 230))

def scene_icj(d, x0, y0, x1, y1):
    # Peace Palace columns in The Hague + scales of justice
    d.rectangle([x0, y0, x1, y1], fill=(226, 214, 188))
    w, h = x1 - x0, y1 - y0
    base = y0 + h * 0.72
    # columns
    for i in range(5):
        cx = x0 + w * (0.12 + i * 0.19)
        d.rectangle([cx - 11, y0 + h * 0.22, cx + 11, base], fill=(250, 246, 236))
        d.rectangle([cx - 15, y0 + h * 0.18, cx + 15, y0 + h * 0.24],
                    fill=(235, 228, 210))
        d.rectangle([cx - 15, base, cx + 15, base + 6], fill=(235, 228, 210))
    d.rectangle([x0 + w * 0.05, y0 + h * 0.12, x1 - w * 0.05, y0 + h * 0.20],
                fill=(200, 60, 50))
    # scales of justice, centre foreground
    sx, sy = x0 + w * 0.50, y0 + h * 0.52
    d.line([sx, sy - 26, sx, sy + 26], fill=(90, 70, 40), width=4)
    d.line([sx - 34, sy - 26, sx + 34, sy - 26], fill=(90, 70, 40), width=4)
    for s in (-1, 1):
        ex = sx + s * 34
        d.line([ex, sy - 26, ex, sy - 6], fill=(90, 70, 40), width=2)
        d.polygon([(ex - 16, sy - 6), (ex + 16, sy - 6), (ex, sy + 12)],
                  fill=(220, 180, 60))
    d.ellipse([sx - 5, sy - 34, sx + 5, sy - 24], fill=(220, 180, 60))

# ---------- page assembly ----------
PANELS = [
    ("WAR & THE GULF", scene_senate,
     "SENATE LETS IRAN",
     "STRIKES STAND",
     "Senate rejects war-powers curb 48\u201351; a tanker burns east of Hormuz as Gulf attacks widen."),
    ("MARKETS", scene_markets,
     "ANTHROPIC +17% ON DEBUT",
     "AS MARKETS SLIDE",
     "$81.3bn IPO, the largest ever; S&P 500 falls 2% for a fifth straight day, Nikkei down 4.7%."),
    ("EUROPE", scene_berlin,
     "EUROPE READY FOR",
     "RUSSIA TALKS",
     "Allies agree a united position in Berlin; Putin invites European leaders to Moscow."),
    ("CLIMATE", scene_cop31,
     "COP31 DRAFT DROPS",
     "FOSSIL FUELS",
     "Outcry as any reference to fossil fuels is cut from the latest UN climate deal text."),
    ("STORM", scene_storm,
     "INDIA EVACUATES 80,000",
     "AS STORM DANA NEARS",
     "Cyclone Dana bears down on the east coast; shelters open and trains cancelled."),
    ("JUSTICE", scene_icj,
     "UN COURT: MYANMAR",
     "COMMITTED GENOCIDE",
     "ICJ finds Myanmar guilty over the 2017 campaign against the Rohingya \u2014 a first against a state."),
]

FOOTER = ("ALSO TODAY:  Drones halt Genoa airport  \u2022  Kyiv hit by four missiles  \u2022  "
          "Fiona the hippo dies at Cincinnati Zoo  \u2022  Trump pardons Pete Rose  \u2022  "
          "Venezuela signs US military deal  \u2022  S. Korea exports top $1 trillion")

def draw_card(d, x0, y0, x1, y1, kicker, scene, hl1, hl2, caption):
    d.rectangle([x0, y0, x1, y1], fill=CARD_BG, outline=LINE, width=2)
    scene_h = int((y1 - y0) * 0.46)
    scene(d, x0 + 2, y0 + 2, x1 - 2, y0 + scene_h)
    d.rectangle([x0, y0 + scene_h, x1, y0 + scene_h + 2], fill=LINE)
    tx = x0 + 12
    ty = y0 + scene_h + 10
    text_in(d, (tx, ty), kicker, font(FB, 17), fill=RED)
    ty += 22
    text_in(d, (tx, ty), hl1, font(FB, 23))
    ty += 27
    text_in(d, (tx, ty), hl2, font(FB, 23))
    ty += 30
    for line in wrap(d, caption, font(FR, 17), (x1 - x0) - 24):
        text_in(d, (tx, ty), line, font(FR, 17), fill=MUTED)
        ty += 19

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    text_in(d, (W // 2, 18), "THE WORLD IN ONE DAY", font(FB, 52),
            anchor="ma")
    text_in(d, (W // 2, 82),
            "FRIDAY 20 NOVEMBER 2026  \u2014  THE DAY'S WORLD NEWS",
            font(FB, 26), fill=RED, anchor="ma")
    d.line([M, 122, W - M, 122], fill=RED, width=4)
    d.line([M, 130, W - M, 130], fill=INK, width=2)
    # grid
    gx0, gy0 = M, HEADER_H
    cw = (W - 2 * M - GAP) // COLS
    ch = (H - HEADER_H - FOOTER_H - M - (ROWS - 1) * GAP) // ROWS
    for i, (kicker, scene, hl1, hl2, caption) in enumerate(PANELS):
        r, c = divmod(i, COLS)
        x0 = gx0 + c * (cw + GAP)
        y0 = gy0 + r * (ch + GAP)
        draw_card(d, x0, y0, x0 + cw, y0 + ch, kicker, scene, hl1, hl2, caption)
    # footer
    fy = H - FOOTER_H + 6
    d.line([M, fy - 8, W - M, fy - 8], fill=INK, width=2)
    for line in wrap(d, FOOTER, font(FB, 17), W - 2 * M):
        text_in(d, (M, fy), line, font(FB, 17))
        fy += 22
    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)

if __name__ == "__main__":
    main()
