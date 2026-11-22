#!/usr/bin/env python3
"""Draw entry.png: a one-page newspaper front page summing up the world news
of Sunday 22 November 2026, as reported that morning.

Stories (all found in news search results dated 22 Nov 2026):
  1. Poland  - Russian missiles landed on NATO soil in Poland (The Scottish Sun).
  2. COP31   - Climate talks in Antalya deadlocked in overtime over fossil fuels (Reuters).
  3. Mexico  - Cartel kingpin "El Chapo Isidro", an FBI top-10 fugitive, captured (Reuters/AP).
  4. Sudan   - Tasis Alliance seized the Bau region of Blue Nile (news aggregators, 22 Nov).
  5. India   - Adulterated alcohol killed 11 people in Manipur (news aggregators, 22 Nov).
  6. UN      - UN talks on lethal autonomous weapons fell short of binding rules (grand-star.eu).

Artwork: original iconic illustrations drawn with Pillow shapes only.
Run: python3 draw.py  ->  writes entry.png (1024x1024) beside this file.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

W = H = 1024
PAPER = (248, 244, 233)
PANEL_BG = (255, 253, 245)
INK = (26, 26, 26)
WHITE = (255, 255, 255)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size)


def fit_font(draw: ImageDraw.ImageDraw, text: str, max_width: float,
             start_size: int) -> ImageFont.FreeTypeFont:
    """Largest bold font, at most start_size, whose text fits max_width."""
    size = start_size
    while size > 10:
        fnt = font(size)
        box = draw.textbbox((0, 0), text, font=fnt)
        if box[2] - box[0] <= max_width:
            return fnt
        size -= 2
    return font(size)


def centered(draw: ImageDraw.ImageDraw, cx: float, y: float, text: str,
             fnt: ImageFont.FreeTypeFont, fill) -> None:
    box = draw.textbbox((0, 0), text, font=fnt)
    tw = box[2] - box[0]
    draw.text((cx - tw / 2 - box[0], y - box[1]), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- icons ----
# Each icon is drawn inside a box (x0, y0, x1, y1) with bold simple shapes.

def icon_missile(d: ImageDraw.ImageDraw, x0, y0, x1, y1, accent):
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    # ground line
    d.line([(x0 + 18, y1 - 8), (x1 - 18, y1 - 8)], fill=INK, width=6)
    # missile body, angled down-right: thick line + nose cone + fins
    bx, by = cx - 52, cy - 42          # tail point
    nx, ny = cx + 48, cy + 26          # nose point
    d.line([(bx, by), (nx, ny)], fill=INK, width=30)
    d.polygon([(nx, ny), (nx - 30, ny + 16), (nx - 40, ny - 14)], fill=INK)
    # fins at the tail
    d.polygon([(bx, by), (bx - 20, by + 20), (bx + 16, by + 12)], fill=INK)
    d.polygon([(bx, by), (bx + 20, by - 18), (bx + 10, by + 16)], fill=INK)
    # flame
    d.polygon([(bx - 4, by - 4), (bx - 34, by - 26), (bx - 22, by + 8),
               (bx - 40, by + 22)], fill=accent)
    # impact bursts near the ground
    for sx, sy in ((cx + 66, y1 - 26), (cx + 30, y1 - 18)):
        for dx, dy in ((0, -14), (11, -8), (-11, -8), (14, 4), (-14, 4)):
            d.line([(sx, sy), (sx + dx, sy + dy)], fill=accent, width=5)


def icon_globe(d: ImageDraw.ImageDraw, x0, y0, x1, y1, accent):
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 8
    r = 52
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=6)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=INK, width=3)
    d.line([(cx - r, cy), (cx + r, cy)], fill=INK, width=3)
    # continent blobs
    d.polygon([(cx - 34, cy - 30), (cx - 12, cy - 38), (cx - 8, cy - 14),
               (cx - 26, cy - 8)], fill=accent)
    d.polygon([(cx + 10, cy + 6), (cx + 34, cy + 2), (cx + 30, cy + 26),
               (cx + 12, cy + 22)], fill=accent)
    # smoke cloud rising from the top right
    for sx, sy, sr in ((cx + 40, cy - 58, 15), (cx + 58, cy - 66, 19),
                       (cx + 76, cy - 56, 13)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 120))


def icon_handcuffs(d: ImageDraw.ImageDraw, x0, y0, x1, y1, accent):
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    r = 38
    # two cuff rings
    d.ellipse([cx - 78, cy - 6, cx - 78 + 2 * r, cy - 6 + 2 * r],
              outline=INK, width=11)
    d.ellipse([cx + 4, cy - 46, cx + 4 + 2 * r, cy - 46 + 2 * r],
              outline=INK, width=11)
    # chain links between them
    for lx, ly in ((cx - 8, cy - 12), (cx + 6, cy - 24)):
        d.ellipse([lx, ly, lx + 20, ly + 13], outline=accent, width=6)
    # keyholes
    d.ellipse([cx - 46, cy + 22, cx - 34, cy + 34], fill=INK)
    d.ellipse([cx + 36, cy - 18, cx + 48, cy - 6], fill=INK)


def icon_flag(d: ImageDraw.ImageDraw, x0, y0, x1, y1, accent):
    cx = (x0 + x1) / 2
    top, bottom = y0 + 8, y1 - 14
    # pole
    d.line([(cx - 46, top), (cx - 46, bottom)], fill=INK, width=8)
    d.ellipse([cx - 53, top - 8, cx - 39, top + 6], fill=accent)
    # waving flag
    d.polygon([(cx - 46, top + 6), (cx + 52, top + 16), (cx + 40, top + 44),
               (cx + 52, top + 70), (cx - 46, top + 62)], fill=accent)
    # location pin beside the pole
    px, py = cx + 66, bottom - 40
    d.polygon([(px - 17, py), (px + 17, py), (px, py + 34)], fill=INK)
    d.ellipse([px - 19, py - 36, px + 19, py + 2], fill=INK)
    d.ellipse([px - 8, py - 25, px + 8, py - 9], fill=PANEL_BG)
    # ground
    d.line([(x0 + 20, bottom), (x1 - 20, bottom)], fill=INK, width=6)


def icon_bottle(d: ImageDraw.ImageDraw, x0, y0, x1, y1, accent):
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    # bottle: neck + shoulders + body
    d.rectangle([cx - 13, cy - 58, cx + 13, cy - 30], outline=INK, width=6)
    d.polygon([(cx - 13, cy - 30), (cx - 34, cy - 8), (cx - 34, cy + 56),
               (cx + 34, cy + 56), (cx + 34, cy - 8), (cx + 13, cy - 30)],
              outline=INK, width=6)
    # liquid
    d.rectangle([cx - 27, cy + 8, cx + 27, cy + 49], fill=accent)
    # big red X of danger across the bottle
    d.line([(cx - 30, cy - 2), (cx + 30, cy + 50)], fill=(178, 34, 34), width=9)
    d.line([(cx + 30, cy - 2), (cx - 30, cy + 50)], fill=(178, 34, 34), width=9)


def icon_robot(d: ImageDraw.ImageDraw, x0, y0, x1, y1, accent):
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    # antenna
    d.line([(cx, cy - 50), (cx, cy - 38)], fill=INK, width=6)
    d.ellipse([cx - 8, cy - 60, cx + 8, cy - 44], fill=accent)
    # ears
    d.rectangle([cx - 62, cy - 14, cx - 48, cy + 16], fill=INK)
    d.rectangle([cx + 48, cy - 14, cx + 62, cy + 16], fill=INK)
    # head
    d.rounded_rectangle([cx - 48, cy - 40, cx + 48, cy + 52], radius=14,
                        outline=INK, width=7)
    # eyes
    d.ellipse([cx - 30, cy - 16, cx - 12, cy + 2], fill=accent)
    d.ellipse([cx + 12, cy - 16, cx + 30, cy + 2], fill=accent)
    # mouth grille
    for i in range(4):
        gx = cx - 24 + i * 13
        d.line([(gx, cy + 22), (gx, cy + 38)], fill=INK, width=5)


# ---------------------------------------------------------------- layout ---

PANELS = [
    # (place, strip colour, icon fn, label lines)
    ("POLAND", (140, 43, 29), icon_missile,
     ["RUSSIAN MISSILES", "HIT NATO SOIL"]),
    ("COP31 - ANTALYA", (29, 111, 106), icon_globe,
     ["CLIMATE TALKS DEADLOCK", "ON FOSSIL FUELS"]),
    ("MEXICO", (31, 78, 121), icon_handcuffs,
     ["CARTEL KINGPIN", "EL CHAPO ISIDRO CAPTURED"]),
    ("SUDAN", (122, 92, 20), icon_flag,
     ["ALLIANCE SEIZES BAU", "IN BLUE NILE STATE"]),
    ("INDIA", (91, 42, 134), icon_bottle,
     ["TAINTED ALCOHOL", "KILLS 11 IN MANIPUR"]),
    ("UNITED NATIONS", (55, 71, 79), icon_robot,
     ["KILLER ROBOT TALKS", "FALL SHORT OF RULES"]),
]


def main() -> None:
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead ------------------------------------------------------------
    centered(d, W / 2, 22, "THE WORLD IN ONE PAGE", font(26), INK)
    date_text = "SUNDAY 22 NOVEMBER 2026"
    centered(d, W / 2, 54, date_text, fit_font(d, date_text, W - 48, 66), INK)
    d.line([(28, 160), (W - 28, 160)], fill=INK, width=5)
    d.line([(28, 168), (W - 28, 168)], fill=INK, width=2)

    # Panels ---------------------------------------------------------------
    margin, gap = 28, 14
    pw = (W - 2 * margin - gap) // 2          # 477
    ph, top = 258, 190
    strip_h = 46
    for i, (place, colour, icon, lines) in enumerate(PANELS):
        col, row = i % 2, i // 2
        px = margin + col * (pw + gap)
        py = top + row * (ph + gap)
        d.rectangle([px, py, px + pw, py + ph], fill=PANEL_BG, outline=INK, width=3)
        # place strip
        d.rectangle([px, py, px + pw, py + strip_h], fill=colour)
        centered(d, px + pw / 2, py + 8, place, font(30), WHITE)
        # icon
        icon(d, px + 10, py + strip_h + 6, px + pw - 10, py + strip_h + 128, colour)
        # label lines (auto-fitted so no line ever spills past the panel)
        ly = py + strip_h + 140
        for line in lines:
            centered(d, px + pw / 2, ly, line,
                     fit_font(d, line, pw - 20, 31), INK)
            ly += 40

    # Footer ---------------------------------------------------------------
    centered(d, W / 2, 996, "SIX STORIES - FIVE CONTINENTS - ONE DAY",
             font(19), INK)

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
