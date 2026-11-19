#!/usr/bin/env python3
"""Draw entry.png: the world news of Thursday 19 November 2026 on one wall.

Concept — "THE WORLD IN ONE PICTURE: the global news control room".
A dark mission-control wall as the day ends in London:
one big main screen names the day, a strip of world clocks shows the
day arriving timezone by timezone, and twelve glowing monitors carry
the day's twelve biggest stories as flat editorial scenes, each with a
camera tag, a headline and a one-line caption. Below the monitors, an
"ALSO TODAY" wire wall adds 24 more stories as emoji one-liners, and a
red news ticker closes the picture. Everything is drawn here with PIL
(no photographic assets), so the render is deterministic: same bytes
every run.

The stories are the full-day set for Thursday 19 November 2026,
gathered from the day's wires and editions (Reuters, AP, AFP, The Times,
Euronews), from the overnight wires through the evening close.

Panels:
 1. Kuwait repels Iran's attack overnight — the first Iranian attack
    on Kuwait in two months; Saudi Civil Defence sounds then clears a
    missile warning over Riyadh (Reuters).
 2. GTA VI sells over 17 million copies on day one after a 13-year
    wait, New Zealand first; Metacritic 99/100, leave requests up 32%
    worldwide (Euronews / AFP).
 3. Trump, Xi and Putin hold the first-ever US-China-Russia trilateral
    in Shenzhen and issue a joint declaration: UN reform, a nuclear
    pledge, more refined oil supply; Ukraine unmentioned (The Times).
 4. House Democrats nominate Hakeem Jeffries for Speaker 251-11; he
    would be the first Black Speaker, taking the gavel on 3 January.
 5. A Turkish court gives jailed Istanbul mayor Ekrem Imamoglu two
    more years in prison and a third political ban (Reuters).
 6. Indonesia's El Nino peat fires are among the worst since 2015,
    with about 2 million hectares burned and haze over SE Asia (WMO).
 7. WHO keeps Congo's Bundibugyo Ebola outbreak a global health
    emergency: 11,376 cases; strain-specific vaccine trials start
    next week (WHO / ECDC).
 8. A Nature study explains Earth's "missing billion years" of rock:
    mantle currents plus ancient ice sheets planed the record away.
 9. Two Russian Tu-95 bombers land at Da Nang, Vietnam, after flights
    that skirted Taiwan and breached Japanese airspace; Tokyo lodges a
    stern protest (Reuters).
10. COP31 in Antalya enters its final hours as ministers meet in
    informal session to unblock a final text; Vanuatu urges reform
    of the climate talks.
11. Mary Peltola's Alaska win seals a 56-44 Democratic Senate
    majority after nine midterm flips; the House is called too (AP).
12. Amazon pledges $7 billion for renewable energy projects in India
    by 2030.

Briefs (13-36) are listed in BRIEFS below with their sources.
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024

# ---------------- palette ----------------
WALL = (252, 206, 44)
WALL2 = (250, 196, 32)
BEZEL = (116, 58, 180)
BEZEL_HI = (150, 94, 216)
SCREEN_EDGE = (160, 90, 0)
INK = (252, 250, 255)
SUB = (252, 250, 255)
FAINT = (252, 250, 255)
GOLD = (150, 84, 0)
CYAN = (0, 104, 150)
RED = (235, 51, 60)
DARKBAR = (250, 214, 80)

CATCOL = {
    "WAR": (153, 55, 43),
    "CULTURE": (153, 66, 119),
    "SUMMIT": (150, 118, 39),
    "POLITICS": (57, 99, 150),
    "CLIMATE": (44, 133, 76),
    "HEALTH": (27, 127, 114),
    "SCIENCE": (115, 79, 151),
    "SECURITY": (150, 87, 36),
    "BUSINESS": (151, 134, 42),
}

NOTO = "/usr/share/fonts/truetype/noto"
SANS_BLACK = f"{NOTO}/NotoSans-Black.ttf"
SANS_XB = f"{NOTO}/NotoSans-ExtraBold.ttf"
SANS_B = f"{NOTO}/NotoSans-Bold.ttf"
SANS_R = f"{NOTO}/NotoSans-Regular.ttf"
SANS_CB = f"{NOTO}/NotoSans-CondensedBold.ttf"
SANS_CXB = f"{NOTO}/NotoSans-CondensedExtraBold.ttf"
EMOJI_TTF = f"{NOTO}/NotoColorEmoji.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def tw(d, s, f):
    return d.textlength(s, font=f)


def wrap(d, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if tw(d, t, f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def fit_lines(d, s, sizes, max_w, max_lines):
    """Wrap s at the first size (largest first) that fits max_lines."""
    for sz in sizes:
        f = font(SANS_B, sz)
        lines = wrap(d, s, f, max_w)
        if len(lines) <= max_lines:
            return f, lines
    f = font(SANS_B, sizes[-1])
    lines = wrap(d, s, f, max_w)[:max_lines]
    return f, lines


def ellipsize(d, s, f, max_w):
    if tw(d, s, f) <= max_w:
        return s
    while s and tw(d, s + "…", f) > max_w:
        s = s[:-1]
    return s + "…"


def spaced(d, s, cx, y, f, fill, tracking):
    """Draw letter-spaced text centred on cx."""
    widths = [tw(d, ch, f) for ch in s]
    total = sum(widths) + tracking * (len(s) - 1)
    x = cx - total / 2
    for ch, wch in zip(s, widths):
        d.text((x, y), ch, font=f, fill=fill)
        x += wch + tracking
    return total


# ---------------- emoji (Noto Color Emoji, rendered once, cached) ----------
_emoji_cache = {}


def emoji_img(ch, h):
    if ch not in _emoji_cache:
        tile = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
        td = ImageDraw.Draw(tile)
        td.text((6, 6), ch, font=font(EMOJI_TTF, 109), embedded_color=True)
        bbox = tile.getbbox()
        _emoji_cache[ch] = tile.crop(bbox) if bbox else tile
    src = _emoji_cache[ch]
    w = max(1, round(src.width * h / src.height))
    return src.resize((w, h), Image.LANCZOS)


# ---------------- scene helpers ----------------
def vgrad(w, h, top, bottom):
    img = Image.new("RGB", (w, h), top)
    dr = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(1, h - 1)
        dr.line([(0, y), (w, y)], fill=tuple(
            round(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return img


def paste_scene(base, scene, x, y):
    base.paste(scene, (x, y))


def stars(dr, w, h, n, seed, ymax=None):
    rng = random.Random(seed)
    for _ in range(n):
        sx = rng.uniform(0, w)
        sy = rng.uniform(0, ymax or h)
        r = rng.uniform(0.6, 1.6)
        dr.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(220, 232, 255))


def person(dr, cx, by, s, col):
    """Simple standing figure: head circle + rounded body. by = feet y."""
    dr.ellipse([cx - 0.16 * s, by - s, cx + 0.16 * s, by - 0.68 * s], fill=col)
    dr.rounded_rectangle([cx - 0.30 * s, by - 0.66 * s, cx + 0.30 * s, by],
                         radius=0.20 * s, fill=col)


def flag_pole(dr, x, ytop, ybot, flag):
    dr.line([(x, ytop), (x, ybot)], fill=(203, 213, 225), width=3)
    dr.ellipse([x - 3, ytop - 3, x + 3, ytop + 3], fill=GOLD)
    flag(dr, x + 2, ytop + 4)


# ---------------- the twelve monitor scenes (232 x 116 each) ----------------
SW, SH = 232, 116


def sc_kuwait():
    img = vgrad(SW, SH, (7, 12, 34), (24, 32, 58))
    dr = ImageDraw.Draw(img, "RGBA")
    stars(dr, SW, SH, 40, 11, ymax=60)
    # moon
    dr.ellipse([196, 8, 214, 26], fill=(226, 232, 240))
    dr.ellipse([190, 5, 208, 23], fill=(16, 24, 48))
    # distant base silhouettes + runway
    dr.rectangle([0, 92, SW, SH], fill=(5, 8, 16))
    dr.polygon([(0, 92), (60, 92), (46, 78), (10, 78)], fill=(10, 15, 26))
    dr.rectangle([150, 82, 205, 92], fill=(10, 15, 26))
    dr.rectangle([168, 74, 178, 82], fill=(10, 15, 26))
    for i in range(9):  # runway lights
        dr.ellipse([12 + i * 26, 100, 16 + i * 26, 103], fill=(250, 197, 66))
    # incoming arcs (orange) and interceptor streaks (cyan)
    for (x0, y0, x1, y1, col, wd) in [
            (8, 6, 120, 66, (255, 122, 40), 3), (30, 2, 150, 60, (255, 84, 40), 3),
            (58, 0, 178, 56, (255, 150, 60), 2),
            (96, 92, 128, 60, (120, 240, 255), 3), (150, 92, 168, 54, (120, 240, 255), 2),
            (60, 92, 108, 64, (180, 250, 255), 2)]:
        dr.line([(x0, y0), (x1, y1)], fill=col, width=wd)
    for (cx, cy, r) in [(128, 60, 7), (170, 53, 5), (110, 65, 4)]:  # bursts
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 214, 130, 230))
        dr.ellipse([cx - r * 2, cy - r * 2, cx + r * 2, cy + r * 2],
                   outline=(255, 150, 70, 120), width=2)
    return img


def sc_gta():
    img = vgrad(SW, SH, (88, 28, 110), (255, 110, 120))
    dr = ImageDraw.Draw(img, "RGBA")
    # sun low on the horizon
    dr.ellipse([88, 38, 144, 94], fill=(255, 196, 86))
    dr.ellipse([88, 38, 144, 94], outline=(255, 160, 90), width=2)
    for yy in (58, 68, 78):  # retro sun stripes
        dr.rectangle([88, yy, 144, yy + 3], fill=(255, 110, 120))
    # palms
    for (px, ph, lean) in [(18, 74, -8), (206, 84, 7), (44, 52, -5)]:
        dr.line([(px, SH), (px + lean, SH - ph)], fill=(24, 16, 34), width=5)
        tx, ty = px + lean, SH - ph
        for dx, dy in [(-24, 2), (-14, -8), (0, -12), (14, -8), (24, 2), (-20, 10), (20, 10)]:
            dr.line([(tx, ty), (tx + dx, ty + dy)], fill=(24, 16, 34), width=3)
    # storefront
    dr.rectangle([52, 66, 180, SH], fill=(16, 12, 28))
    dr.rectangle([52, 66, 180, 74], fill=(255, 62, 165))
    dr.rectangle([64, 84, 104, SH], fill=(30, 220, 255, 90))
    dr.rectangle([128, 84, 168, SH], fill=(30, 220, 255, 90))
    # midnight queue
    cols = [(15, 23, 42), (42, 20, 38), (20, 34, 48), (34, 26, 20), (24, 20, 44), (16, 30, 30)]
    for i, col in enumerate(cols):
        person(dr, 66 + i * 17, SH - 1, 26, col)
    return img


def _flag_us(dr, x, y):
    for i in range(4):
        dr.rectangle([x, y + i * 4, x + 26, y + i * 4 + 2],
                     fill=(220, 60, 60) if i % 2 == 0 else (240, 240, 240))
    dr.rectangle([x, y, x + 12, y + 8], fill=(40, 60, 160))


def _flag_cn(dr, x, y):
    dr.rectangle([x, y, x + 26, y + 17], fill=(222, 41, 16))
    for (sx, sy) in [(4, 3), (12, 2), (14, 6), (12, 10), (9, 12)]:
        dr.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 222, 0))


def _flag_ru(dr, x, y):
    dr.rectangle([x, y, x + 26, y + 6], fill=(245, 245, 245))
    dr.rectangle([x, y + 6, x + 26, y + 12], fill=(30, 60, 170))
    dr.rectangle([x, y + 12, x + 26, y + 17], fill=(210, 40, 40))


def sc_shenzhen():
    img = vgrad(SW, SH, (10, 40, 52), (18, 74, 84))
    dr = ImageDraw.Draw(img, "RGBA")
    # skyline
    rng = random.Random(19)
    x = 0
    while x < SW:
        bw = rng.randint(14, 26)
        bh = rng.randint(18, 44)
        dr.rectangle([x, 62 - bh, x + bw, 62], fill=(8, 26, 34))
        for wy in range(62 - bh + 4, 58, 7):
            for wx in range(x + 3, x + bw - 3, 6):
                if rng.random() < 0.4:
                    dr.rectangle([wx, wy, wx + 3, wy + 3], fill=(250, 220, 130))
        x += bw + 3
    dr.rectangle([0, 62, SW, SH], fill=(12, 30, 38))
    # three flags over a long table
    flag_pole(dr, 40, 30, 84, _flag_us)
    flag_pole(dr, 103, 24, 84, _flag_cn)
    flag_pole(dr, 166, 30, 84, _flag_ru)
    dr.polygon([(28, 96), (204, 96), (220, SH), (12, SH)], fill=(94, 58, 30))
    dr.polygon([(28, 96), (204, 96), (208, 101), (24, 101)], fill=(140, 92, 48))
    for cx in (66, 116, 166):  # seated silhouettes
        dr.ellipse([cx - 7, 78, cx + 7, 92], fill=(10, 14, 22))
        dr.rounded_rectangle([cx - 11, 90, cx + 11, 102], radius=5, fill=(10, 14, 22))
    return img


def sc_capitol():
    img = vgrad(SW, SH, (16, 24, 58), (238, 150, 92))
    dr = ImageDraw.Draw(img, "RGBA")
    stars(dr, SW, SH, 22, 7, ymax=34)
    dr.ellipse([16, 12, 34, 30], fill=(240, 244, 255))
    sil = (12, 18, 38)
    # Capitol: base, columns, dome
    dr.rectangle([52, 84, 180, SH], fill=sil)
    for i in range(6):
        dr.rectangle([60 + i * 20, 66, 66 + i * 20, 84], fill=sil)
    dr.rectangle([48, 62, 184, 67], fill=sil)
    dr.pieslice([76, 18, 156, 74], start=180, end=360, fill=sil)
    dr.rectangle([112, 8, 120, 22], fill=sil)
    dr.ellipse([111, 2, 121, 12], fill=sil)
    dr.rectangle([0, 108, SW, SH], fill=(8, 12, 26))
    # gavel, foreground right
    dr.line([(176, 96), (214, 62)], fill=(146, 94, 44), width=7)
    dr.rounded_rectangle([196, 44, 228, 60], radius=6, fill=(176, 118, 58))
    dr.rounded_rectangle([196, 44, 228, 60], radius=6, outline=(120, 76, 30), width=2)
    dr.rectangle([186, 100, 226, 106], fill=(120, 76, 30))
    return img


def sc_istanbul():
    img = vgrad(SW, SH, (40, 32, 84), (250, 130, 90))
    dr = ImageDraw.Draw(img, "RGBA")
    dr.ellipse([176, 16, 206, 46], fill=(255, 190, 90))
    sil = (22, 18, 44)
    # skyline with domes and minarets
    dr.rectangle([0, 74, SW, 88], fill=sil)
    for (cx, r) in [(52, 17), (86, 12), (150, 14)]:
        dr.pieslice([cx - r, 74 - r, cx + r, 74 + r], start=180, end=360, fill=sil)
    for mx in (28, 108, 196):
        dr.rectangle([mx, 34, mx + 4, 76], fill=sil)
        dr.polygon([(mx - 3, 36), (mx + 7, 36), (mx + 2, 24)], fill=sil)
        dr.rectangle([mx - 2, 52, mx + 6, 56], fill=sil)
    # Bosphorus
    dr.rectangle([0, 88, SW, SH], fill=(26, 60, 104))
    for i in range(14):
        rx = random.Random(i * 3).uniform(0, SW - 16)
        dr.line([(rx, 94 + (i % 4) * 6), (rx + 12, 94 + (i % 4) * 6)],
                fill=(120, 180, 230), width=2)
    # courthouse portico, foreground: pediment + four stout columns
    dr.polygon([(8, 92), (88, 92), (48, 80)], fill=(226, 232, 240))
    for i in range(4):
        dr.rectangle([16 + i * 20, 94, 24 + i * 20, SH], fill=(226, 232, 240))
    dr.rectangle([10, 110, 86, SH], fill=(203, 213, 225))
    return img


def sc_fires():
    img = vgrad(SW, SH, (120, 52, 20), (214, 110, 40))
    dr = ImageDraw.Draw(img, "RGBA")
    dr.ellipse([92, 10, 140, 58], fill=(255, 176, 92))  # hazed sun
    # smoke plumes
    for (cx, cy, r) in [(40, 26, 20), (76, 18, 26), (150, 22, 22), (196, 14, 28), (116, 12, 18)]:
        dr.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2], fill=(90, 70, 66, 150))
    # palm plantation silhouettes
    for px in range(6, SW, 24):
        dr.line([(px, 88), (px + 3, 62)], fill=(30, 18, 12), width=3)
        for dx, dy in [(-11, -4), (-6, -9), (0, -11), (7, -9), (12, -4)]:
            dr.line([(px + 3, 62), (px + 3 + dx, 62 + dy)], fill=(30, 18, 12), width=2)
    dr.rectangle([0, 86, SW, SH], fill=(24, 12, 8))
    # fire line
    rng = random.Random(5)
    for fx in range(4, SW, 9):
        fh = rng.randint(8, 22)
        dr.polygon([(fx, 92), (fx + 7, 92), (fx + 3, 92 - fh)], fill=(255, 106, 26))
        dr.polygon([(fx + 2, 92), (fx + 6, 92), (fx + 3, 92 - fh // 2)], fill=(255, 196, 60))
    return img


def sc_ebola():
    img = vgrad(SW, SH, (8, 60, 62), (14, 96, 92))
    dr = ImageDraw.Draw(img, "RGBA")
    # virus dots
    rng = random.Random(23)
    for _ in range(9):
        cx, cy = rng.uniform(6, SW - 6), rng.uniform(6, SH - 6)
        dr.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], outline=(94, 234, 212), width=1)
    # vaccine vial
    dr.rounded_rectangle([52, 30, 96, 100], radius=8, fill=(203, 240, 238))
    dr.rounded_rectangle([52, 56, 96, 100], radius=8, fill=(45, 190, 200))
    dr.rectangle([58, 18, 90, 32], fill=(148, 163, 184))
    dr.rectangle([52, 46, 96, 54], fill=(240, 249, 255))
    # syringe diagonal
    dr.line([(104, 78), (150, 40)], fill=(226, 232, 240), width=7)
    dr.line([(150, 40), (166, 24)], fill=(226, 232, 240), width=3)
    dr.polygon([(166, 24), (176, 14), (170, 28)], fill=(226, 232, 240))
    dr.rectangle([128, 52, 146, 66], fill=(148, 163, 184))
    # health worker in PPE
    dr.ellipse([182, 30, 214, 62], fill=(254, 240, 138))
    dr.ellipse([188, 38, 208, 54], fill=(186, 230, 253))
    dr.rounded_rectangle([176, 60, 220, 106], radius=10, fill=(254, 240, 138))
    dr.line([(184, 76), (204, 76)], fill=(202, 138, 4), width=3)
    return img


def sc_canyon():
    img = Image.new("RGB", (SW, SH), (146, 84, 52))
    dr = ImageDraw.Draw(img, "RGBA")
    bands = [(176, 108, 66, 0, 16), (158, 88, 52, 16, 32), (196, 128, 78, 32, 46),
             (120, 66, 44, 46, 60), (168, 96, 58, 60, 76), (140, 78, 48, 76, 92),
             (186, 116, 70, 92, 116)]
    for bi, (r, g, b, y0, y1) in enumerate(bands):
        # wavy-edged strata: polygon whose top edge undulates
        pts = []
        for x in range(0, SW + 16, 16):
            pts.append((x, y0 + 2.5 * math.sin(x / 28 + bi * 1.7)))
        pts += [(SW, y1), (0, y1)]
        dr.polygon(pts, fill=(r, g, b))
        rng = random.Random(y0)
        for _ in range(12):
            sx = rng.uniform(0, SW)
            sy = rng.uniform(y0 + 2, y1 - 2)
            dr.line([(sx, sy), (sx + rng.uniform(4, 18), sy)],
                    fill=(0, 0, 0, 40), width=1)
    # the missing band: dark gap with glowing edges, 46..60 replaced visually
    dr.rectangle([0, 46, SW, 60], fill=(38, 26, 30))
    dr.line([(0, 46), (SW, 46)], fill=(255, 220, 120), width=2)
    dr.line([(0, 59), (SW, 59)], fill=(255, 220, 120), width=2)
    f = font(SANS_BLACK, 15)
    dr.text((10, 45), "?", font=f, fill=(255, 220, 120))
    dr.text((SW - 22, 45), "?", font=f, fill=(255, 220, 120))
    # magnifier over the gap
    dr.ellipse([86, 30, 146, 90], outline=(240, 248, 255), width=5)
    dr.line([(138, 82), (168, 108)], fill=(240, 248, 255), width=7)
    return img


def sc_bombers():
    img = vgrad(SW, SH, (38, 84, 140), (140, 190, 230))
    dr = ImageDraw.Draw(img, "RGBA")
    # sea + two island blobs
    dr.rectangle([0, 92, SW, SH], fill=(24, 84, 130))
    dr.ellipse([16, 88, 76, 102], fill=(52, 120, 74))
    dr.ellipse([168, 90, 216, 103], fill=(52, 120, 74))
    # dashed flight path
    for t in range(0, 101, 6):
        x = 8 + t * 2.2
        y = 16 + 26 * math.sin(t / 100 * math.pi * 0.9)
        dr.ellipse([x, y, x + 3, y + 3], fill=(255, 255, 255, 170))
    sil = (16, 24, 40)
    # Tu-95 silhouette: long body, swept wings, four props
    dr.polygon([(58, 44), (150, 40), (186, 46), (150, 52), (58, 52)], fill=sil)
    dr.polygon([(96, 50), (128, 74), (142, 74), (122, 48)], fill=sil)
    dr.polygon([(96, 44), (124, 24), (138, 24), (120, 46)], fill=sil)
    dr.polygon([(58, 46), (44, 34), (52, 46), (46, 56), (58, 52)], fill=sil)
    for px in (104, 124, 144, 162):
        dr.ellipse([px, 52, px + 4, 66], fill=sil)
    # two escort jets
    for (jx, jy, s) in [(196, 26, 1.0), (30, 74, 0.8)]:
        dr.polygon([(jx, jy), (jx + 22 * s, jy + 3 * s), (jx, jy + 6 * s)], fill=sil)
        dr.polygon([(jx + 8 * s, jy + 2 * s), (jx + 14 * s, jy + 10 * s),
                    (jx + 17 * s, jy + 9 * s), (jx + 12 * s, jy + 1 * s)], fill=sil)
    return img


def sc_cop31():
    img = Image.new("RGB", (SW, SH), (24, 34, 44))
    dr = ImageDraw.Draw(img, "RGBA")
    dr.rectangle([0, 0, SW // 2, SH], fill=(146, 52, 24))     # hot half
    dr.rectangle([SW // 2, 0, SW, SH], fill=(16, 84, 88))     # cool half
    # globe
    dr.ellipse([66, 8, 166, 100], fill=(56, 140, 200))
    dr.ellipse([66, 8, 116, 100], fill=(222, 110, 44))        # hot side of globe
    dr.ellipse([116, 8, 166, 100], fill=(52, 168, 130))       # green side
    for (cx, cy, r) in [(92, 34, 9), (128, 58, 11), (104, 72, 7), (140, 30, 6)]:
        dr.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2], fill=(30, 90, 60, 160))
    dr.ellipse([66, 8, 166, 100], outline=(226, 240, 250), width=3)
    # delegate silhouettes at a curved table
    dr.pieslice([26, 78, 206, 128], start=0, end=180, fill=(30, 26, 22))
    for cx in (52, 82, 112, 142, 172):
        person(dr, cx, 104, 22, (12, 12, 16))
    return img


def sc_alaska():
    img = vgrad(SW, SH, (8, 14, 40), (16, 34, 62))
    dr = ImageDraw.Draw(img, "RGBA")
    stars(dr, SW, SH, 30, 41, ymax=40)
    # aurora ribbons
    for (off, col) in [(0, (52, 255, 150, 90)), (10, (80, 200, 255, 70)), (20, (170, 120, 255, 50))]:
        pts = [(x, 14 + off + 10 * math.sin(x / 34 + off)) for x in range(0, SW + 8, 8)]
        dr.line(pts, fill=col, width=7)
    # mountains with snow caps
    for (x0, x1, peak) in [(-10, 90, 44), (60, 170, 30), (140, 250, 40)]:
        dr.polygon([(x0, 96), ((x0 + x1) // 2, peak), (x1, 96)], fill=(30, 44, 70))
        cx = (x0 + x1) // 2
        dr.polygon([(cx - 13, peak + 15), (cx, peak), (cx + 13, peak + 15),
                    (cx + 5, peak + 13), (cx, peak + 18), (cx - 5, peak + 13)],
                   fill=(240, 246, 255))
    dr.rectangle([0, 96, SW, SH], fill=(226, 234, 244))
    # ballot box
    dr.rounded_rectangle([88, 82, 144, 110], radius=4, fill=(36, 86, 166))
    dr.rectangle([98, 78, 134, 84], fill=(240, 246, 255))
    dr.line([(104, 90), (112, 98), (128, 84)], fill=(74, 222, 128), width=4)
    return img


def sc_india():
    img = vgrad(SW, SH, (64, 150, 220), (190, 228, 250))
    dr = ImageDraw.Draw(img, "RGBA")
    dr.ellipse([182, 8, 216, 42], fill=(255, 214, 80))
    for a in range(8):
        ang = math.radians(a * 45)
        dr.line([(199 + 24 * math.cos(ang), 25 + 24 * math.sin(ang)),
                 (199 + 31 * math.cos(ang), 25 + 31 * math.sin(ang))],
                fill=(255, 214, 80), width=3)
    # wind turbines
    for (tx, th) in [(36, 62), (70, 48)]:
        dr.line([(tx, SH - 26), (tx, SH - 26 - th)], fill=(240, 246, 250), width=3)
        cy = SH - 26 - th
        for a in (90, 210, 330):
            ang = math.radians(a)
            dr.line([(tx, cy), (tx + 15 * math.cos(ang), cy + 15 * math.sin(ang))],
                    fill=(240, 246, 250), width=3)
    # warehouse silhouette
    dr.rectangle([150, 66, 224, 92], fill=(70, 84, 104))
    dr.polygon([(150, 66), (224, 66), (214, 56), (160, 56)], fill=(52, 64, 82))
    # solar field in perspective rows
    for r in range(3):
        y0 = 94 + r * 8
        for c in range(7):
            x0 = 8 + c * 32 - r * 5
            dr.polygon([(x0, y0), (x0 + 24, y0), (x0 + 28, y0 + 6), (x0 + 4, y0 + 6)],
                       fill=(30, 80, 160), outline=(150, 200, 245))
    return img


SCENES = [sc_kuwait, sc_gta, sc_shenzhen, sc_capitol, sc_istanbul, sc_fires,
          sc_ebola, sc_canyon, sc_bombers, sc_cop31, sc_alaska, sc_india]


# ---------------- content ----------------
# (camera tag, category, emoji, headline, caption)
STORIES = [
    ("CAM 01 · KUWAIT", "WAR", "🚀",
     "KUWAIT REPELS IRAN ATTACK",
     "First Iranian attack in two months — Reuters"),
    ("CAM 02 · AUCKLAND", "CULTURE", "🎮",
     "GTA VI SELLS 17M ON DAY ONE",
     "Metacritic 99/100; leave requests up 32%"),
    ("CAM 03 · SHENZHEN", "SUMMIT", "🤝",
     "A JOINT DECLARATION IN SHENZHEN",
     "UN reform, nuclear pledge; Ukraine unmentioned — Times"),
    ("CAM 04 · WASHINGTON", "POLITICS", "🏛️",
     "JEFFRIES WINS THE GAVEL RACE",
     "Would be the first Black Speaker in US history"),
    ("CAM 05 · ISTANBUL", "POLITICS", "⚖️",
     "JAILED MAYOR GETS 2 MORE YEARS",
     "Erdogan's jailed rival, banned again — Reuters"),
    ("CAM 06 · SUMATRA", "CLIMATE", "🔥",
     "PEAT FIRES CHOKE SOUTHEAST ASIA",
     "Worst El Niño fire season since 2015 — WMO"),
    ("CAM 07 · CONGO", "HEALTH", "💉",
     "EBOLA EMERGENCY STAYS ON",
     "11,376 cases; vaccine trials start next week"),
    ("CAM 08 · GRAND CANYON", "SCIENCE", "🪨",
     "THE MISSING BILLION YEARS, FOUND",
     "Mantle currents + ice sheets erased the record"),
    ("CAM 09 · DA NANG", "SECURITY", "✈️",
     "RUSSIAN BOMBERS LAND IN VIETNAM",
     "Tokyo protests airspace breach — Reuters"),
    ("CAM 10 · ANTALYA", "CLIMATE", "🌍",
     "COP31 MINISTERS RACE THE CLOCK",
     "Informal talks push for a final text — Antalya"),
    ("CAM 11 · ALASKA", "POLITICS", "🗳️",
     "ALASKA FLIPS IT: SENATE 56–44",
     "Democrats take Senate 56–44 + House — AP"),
    ("CAM 12 · INDIA", "BUSINESS", "☀️",
     "AMAZON BETS $7 BILLION ON INDIA",
     "For renewable energy across India by 2030"),
]

# (emoji, text) — briefs 13..36, all from the 19 Nov 2026 full-day wires
BRIEFS = [
    ("🇲🇲", "ICJ rules on the Rohingya genocide case"),
    ("🇧🇩", "Yunus's home torched; 28 districts hit by violence"),
    ("🌉", "Crimea bridge hit again; car traffic halted"),
    ("🇺🇦", "Abu Dhabi talks end with no breakthrough"),
    ("🇩🇪", "30+ leaders meet in Berlin for Ukraine"),
    ("🇪🇺", "EU proposes a €45bn loan for Ukraine"),
    ("🇻🇪", "US and Venezuela sign military cooperation deal"),
    ("🇮🇱", "Israel's rare ground raid in Gaza beyond the yellow line"),
    ("🛢️", "IEA: Hormuz crisis gravest ever threat to energy security"),
    ("🚢", "Tanker struck in the Strait of Hormuz; crew safe"),
    ("🎨", "Van Gogh sells for $190.4M — a record for the artist"),
    ("🤖", "Anthropic's $81.3B IPO sets a record at $1.5T value"),
    ("🧒", "589M children lived in conflict zones in 2025"),
    ("🇮🇩", "Indonesia passes asset-forfeiture bill"),
    ("🌀", "Cyclone Akvan bears down on Andhra–Odisha"),
    ("🇫🇯", "Fiji declares disaster over El Niño drought"),
    ("🌀", "Cyclone Xavier: 100-knot winds near Cook Islands"),
    ("💻", "N-able confirms server breach; mail portals off"),
    ("🇪🇨", "Ecuador fishermen sue US over drone strike"),
    ("🇵🇭", "US–Philippines pursue a $2B+ loan package"),
    ("🇲🇾", "UNHCR stops registering new asylum cases in Malaysia"),
    ("📉", "Markets slide: Brent $89.59, Hang Seng −1.90%"),
    ("🇮🇳", "India–Japan hold 2+2 defence talks in Tokyo"),
    ("🐧", "Ozone hole is 7th-largest in 48 years"),
]

CLOCKS = [("AUCKLAND", "12:12", "FRI", 12, 12), ("TOKYO", "08:12", "FRI", 8, 12),
          ("JAKARTA", "06:12", "FRI", 6, 12), ("LONDON", "23:12", "THU", 11, 12),
          ("NEW YORK", "18:12", "THU", 6, 12), ("LOS ANGELES", "15:12", "THU", 3, 12)]

TICKER = ("+++ KUWAIT REPELS IRAN ATTACK +++ GTA VI SELLS 17M +++ TRUMP–XI–PUTIN "
          "DECLARE +++ ICJ RULES ON ROHINGYA +++ COP31 AT THE WIRE +++")


# ---------------- composition ----------------
def rounded(dr, box, r, **kw):
    dr.rounded_rectangle(box, radius=r, **kw)


def draw_main_screen(img):
    dr = ImageDraw.Draw(img, "RGBA")
    rounded(dr, [16, 14, 1008, 158], 14, fill=(255, 244, 200), outline=SCREEN_EDGE, width=2)
    rounded(dr, [22, 20, 1002, 152], 10, outline=(18, 60, 78), width=1)
    # LIVE bug, top-left
    dr.ellipse([38, 32, 50, 44], fill=RED)
    dr.text((56, 30), "LIVE", font=font(SANS_XB, 15), fill=(26, 22, 8))
    # control-room label, right-aligned inside the screen
    lab, lf2, trk = "GLOBAL NEWS CONTROL ROOM", font(SANS_CB, 13), 2
    total = sum(tw(dr, ch, lf2) for ch in lab) + trk * (len(lab) - 1)
    x = 1002 - 18 - total
    for ch in lab:
        dr.text((x, 30), ch, font=lf2, fill=(140, 90, 0))
        x += tw(dr, ch, lf2) + trk
    # title
    tf = font(SANS_BLACK, 40)
    s = "THE WORLD IN ONE PICTURE"
    dr.text(((W - tw(dr, s, tf)) / 2, 44), s, font=tf, fill=(26, 22, 8))
    # date
    df = font(SANS_XB, 30)
    s = "THURSDAY · 19 NOVEMBER 2026"
    dr.text(((W - tw(dr, s, df)) / 2, 92), s, font=df, fill=GOLD)
    # strap
    spaced(dr, "36 STORIES · 7 CONTINENTS · ONE DAY · EVERY ONE FROM THURSDAY",
           W / 2, 128, font(SANS_CB, 14), CYAN, 2)


def draw_clocks(img):
    dr = ImageDraw.Draw(img, "RGBA")
    y = 160
    slot = (W - 32) / 6
    for i, (city, tstr, day, hh, mm) in enumerate(CLOCKS):
        cx = 16 + slot * i + slot / 2
        r = 10
        cy = y + 11
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(148, 180, 205), width=2)
        ha = math.radians((hh % 12 + mm / 60) * 30 - 90)
        ma = math.radians(mm * 6 - 90)
        dr.line([(cx, cy), (cx + 7 * math.cos(ha), cy + 7 * math.sin(ha))],
                fill=(160, 96, 0), width=3)
        dr.line([(cx, cy), (cx + 10 * math.cos(ma), cy + 10 * math.sin(ma))],
                fill=(30, 26, 10), width=2)
        label = f"{city} {tstr} {day}"
        lf = font(SANS_CB, 11)
        dr.text((cx - tw(dr, label, lf) / 2, y + 25), label, font=lf, fill=(90, 74, 20))


def draw_monitor(img, idx, x, y):
    tag, cat, emo, head, cap = STORIES[idx]
    col = CATCOL[cat]
    dr = ImageDraw.Draw(img, "RGBA")
    mw, mh = 242, 194
    rounded(dr, [x, y, x + mw, y + mh], 10, fill=BEZEL, outline=BEZEL_HI, width=1)
    # scene
    scene = SCENES[idx]()
    img.paste(scene, (x + 5, y + 5))
    dr = ImageDraw.Draw(img, "RGBA")
    rounded(dr, [x + 5, y + 5, x + mw - 5, y + 121], 6, outline=(90, 110, 135), width=1)
    # recording LED
    dr.ellipse([x + mw - 16, y + 8, x + mw - 9, y + 15], fill=RED)
    # text zone
    tx = x + 10
    ty = y + 127
    # number badge
    dr.ellipse([tx, ty, tx + 17, ty + 17], fill=col)
    nf = font(SANS_B, 10)
    ns = str(idx + 1)
    dr.text((tx + 8.5 - tw(dr, ns, nf) / 2, ty + 2), ns, font=nf, fill=(10, 12, 18))
    dr.text((tx + 23, ty + 2), tag, font=font(SANS_CB, 11), fill=(255, 255, 255))
    dr.text((tx + 23 + tw(dr, tag, font(SANS_CB, 11)) + 8, ty + 2), "· " + cat,
            font=font(SANS_CB, 11), fill=FAINT)
    e = emoji_img(emo, 15)
    img.paste(e, (x + mw - 12 - e.width, ty), e)
    dr = ImageDraw.Draw(img, "RGBA")
    # headline (up to 2 lines)
    hf, lines = fit_lines(dr, head, (14, 13, 12), mw - 20, 2)
    hy = ty + 21
    for ln in lines:
        dr.text((tx, hy), ln, font=hf, fill=INK)
        hy += hf.size + 2
    # caption (1 line, shrunk then ellipsised)
    cf = font(SANS_R, 10)
    dr.text((tx, ty + 56), ellipsize(dr, cap, cf, mw - 20), font=cf, fill=SUB)


def draw_briefs(img):
    dr = ImageDraw.Draw(img, "RGBA")
    y0 = 806
    rounded(dr, [16, y0, 1008, 978], 10, fill=(255, 248, 214), outline=(214, 170, 40), width=1)
    dr.text((30, y0 + 9), "ALSO TODAY — THE OVERNIGHT WIRES",
            font=font(SANS_XB, 15), fill=(26, 22, 8))
    s = "24 MORE STORIES · ALL FROM THURSDAY 19 NOV (SO FAR)"
    dr.text((1008 - 30 - tw(dr, s, font(SANS_CB, 12)), y0 + 12), s,
            font=font(SANS_CB, 12), fill=FAINT)
    dr.line([(30, y0 + 36), (994, y0 + 36)], fill=(214, 170, 40), width=1)
    cols, rows = 3, 8
    cw = (1008 - 32 - 2 * 18) / cols
    rh = 16.5
    for i, (emo, text) in enumerate(BRIEFS):
        c, r = divmod(i, rows)
        bx = 32 + c * (cw + 18)
        by = y0 + 44 + r * rh
        num = 13 + i
        nf = font(SANS_B, 10)
        dr.text((bx, by + 1), f"{num}", font=nf, fill=GOLD)
        e = emoji_img(emo, 13)
        img.paste(e, (int(bx + 20), int(by + 1)), e)
        dr = ImageDraw.Draw(img, "RGBA")
        tf = font(SANS_R, 11)
        dr.text((bx + 40, by + 1), ellipsize(dr, text, tf, cw - 44), font=tf,
                fill=(30, 26, 10))


def draw_ticker(img):
    dr = ImageDraw.Draw(img, "RGBA")
    y0 = 986
    dr.rectangle([0, y0, W, H], fill=(168, 24, 34))
    dr.rectangle([0, y0, 118, H], fill=(110, 12, 20))
    dr.text((16, y0 + 11), "NEWSWIRE", font=font(SANS_XB, 14), fill=(255, 255, 255))
    tf = font(SANS_B, 13)
    segs = [seg.strip() for seg in TICKER.split("+++") if seg.strip()]
    s = ""
    for seg in segs:
        cand = (s + " +++ " + seg) if s else ("+++ " + seg)
        if tw(dr, cand, tf) <= W - 148:
            s = cand
        else:
            break
    s += " +++"
    dr.text((134, y0 + 12), s, font=tf, fill=(255, 240, 240))


def main():
    img = Image.new("RGB", (W, H), WALL)
    dr = ImageDraw.Draw(img, "RGBA")
    # wall panel seams + soft glow behind the main screen
    for gx in range(128, W, 128):
        dr.line([(gx, 0), (gx, H)], fill=(255, 255, 255, 10), width=1)
    for gy in range(128, H, 128):
        dr.line([(0, gy), (W, gy)], fill=(255, 255, 255, 8), width=1)
    draw_main_screen(img)
    draw_clocks(img)
    for i in range(12):
        c, r = i % 4, i // 4
        draw_monitor(img, i, 16 + c * (242 + 8), 206 + r * (194 + 6))
    draw_briefs(img)
    draw_ticker(img)
    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
