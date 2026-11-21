#!/usr/bin/env python3
"""Build-time renderer for the make.fun news-image-20261121 bounty.

Draws "The World Today" — Saturday, 21 November 2026 — as a single
1024x1024 newspaper front page with Pillow. Deterministic: no network, no
randomness, no external images. The committed entry.png is the grader
artifact; main.py (stdlib only) merely copies it to the output directory.

Headlines (21 Nov 2026, primary outlets):
- LEAD: Russia's largest strike of the war on Kyiv, spilling into Poland.
- ICJ rules Myanmar committed genocide against the Rohingya (9-6).
- Trump-Xi-Putin trilateral peace declaration in Shenzhen.
- UK-EU reset deal struck in Brussels.
- Anthropic's record $81bn IPO at a $1.5tn valuation.
- Briefs: Denmark/Russia plot accusation, Mamdani/Rikers, UFO footage,
  Trump AI data-centre threat, ANC cities, Kryvyi Rih strike.
"""

import os
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1024, 1024
MARGIN = 40
PAPER = (248, 244, 236)
INK = (17, 17, 17)
RED = (176, 42, 30)
BLUE = (31, 58, 95)
GREY = (90, 90, 86)
LIGHT_RULE = (200, 192, 176)


def load_font(name, size):
    for base in ("/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/TTF"):
        path = os.path.join(base, name + ".ttf")
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


SERIF_B = lambda s: load_font("DejaVuSerif-Bold", s)  # noqa: E731
SERIF = lambda s: load_font("DejaVuSerif", s)  # noqa: E731
SANS_B = lambda s: load_font("DejaVuSans-Bold", s)  # noqa: E731
SANS = lambda s: load_font("DejaVuSans", s)  # noqa: E731
SANS_O = lambda s: load_font("DejaVuSans-Oblique", s)  # noqa: E731


def wrap(draw, text, font, width):
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if draw.textlength(trial, font=font) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def block(draw, x, y, lines, font, fill, leading=None):
    if leading is None:
        leading = int(font.size * 1.22)
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def rule(draw, y, width=2, color=INK, x0=None, x1=None):
    x0 = MARGIN if x0 is None else x0
    x1 = W - MARGIN if x1 is None else x1
    draw.line([(x0, y), (x1, y)], fill=color, width=width)
    return y + width


def draw_skyline(draw, x, y, w, h):
    """Stylised night skyline over the Dnipro: drawn, not a photograph."""
    draw.rectangle([x, y, x + w, y + h], fill=(22, 35, 58))
    # River band at the bottom of the panel.
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(29, 58, 95))
    # Buildings (fixed heights: deterministic).
    heights = [58, 84, 66, 96, 74, 110, 62, 88, 70, 102, 56, 80, 92, 64]
    bw = w // len(heights)
    for i, bh in enumerate(heights):
        bx = x + i * bw + 2
        by = y + h - 26 - bh
        shade = (36, 52, 79) if i % 2 == 0 else (46, 66, 102)
        draw.rectangle([bx, by, bx + bw - 4, y + h - 26], fill=shade)
        # Windows: sparse deterministic dots.
        for wy in range(by + 8, y + h - 32, 14):
            for wx in range(bx + 5, bx + bw - 9, 12):
                if (wx * 7 + wy * 13) % 5 == 0:
                    draw.rectangle([wx, wy, wx + 3, wy + 4], fill=(245, 197, 66))
    # Bridge arc over the river.
    draw.arc([x + w * 0.55, y + h - 78, x + w * 0.98, y + h + 6],
             start=180, end=360, fill=(143, 163, 192), width=4)
    for fx in (0.60, 0.68, 0.76, 0.84, 0.92):
        bx = int(x + w * fx)
        draw.line([(bx, y + h - 44), (bx, y + h - 26)], fill=(143, 163, 192), width=2)
    # Two explosion bursts (orange, top right).
    for cx, cy, r in ((x + w * 0.82, y + 34, 26), (x + w * 0.70, y + 52, 18)):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 122, 26))
        draw.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2],
                     fill=(255, 197, 66))
        for ang in range(0, 360, 45):
            import math
            ex = cx + int(r * 1.5 * math.cos(math.radians(ang)))
            ey = cy + int(r * 1.5 * math.sin(math.radians(ang)))
            draw.line([(cx, cy), (ex, ey)], fill=(255, 197, 66), width=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    # Outer double border.
    draw.rectangle([14, 14, W - 15, H - 15], outline=INK, width=2)
    draw.rectangle([20, 20, W - 21, H - 21], outline=LIGHT_RULE, width=1)

    y = 30
    # Masthead.
    mast = SERIF_B(56)
    title = "THE WORLD TODAY"
    tw = draw.textlength(title, font=mast)
    draw.text(((W - tw) / 2, y), title, font=mast, fill=INK)
    y += 66
    y = rule(draw, y, width=3)
    y += 8
    # Dateline row.
    dl = SANS_B(14)
    draw.text((MARGIN, y), "SATURDAY, 21 NOVEMBER 2026", font=dl, fill=INK)
    right = "ONE FRONT PAGE · EDITION 2026-11-21"
    rw = draw.textlength(right, font=dl)
    draw.text((W - MARGIN - rw, y), right, font=dl, fill=INK)
    y += 22
    y = rule(draw, y, width=1, color=LIGHT_RULE)
    y += 10

    # Lead story.
    kicker = SANS_B(15)
    draw.text((MARGIN, y), "WAR IN UKRAINE — LEAD STORY", font=kicker, fill=RED)
    y += 24
    head = SERIF_B(42)
    headline = ("RUSSIA'S BIGGEST STRIKE OF THE WAR "
                "HITS KYIV — AND SPILLS INTO POLAND")
    y = block(draw, MARGIN, y, wrap(draw, headline, head, W - 2 * MARGIN),
              head, INK, leading=50)
    y += 6
    sub = SANS(18)
    subhead = ("27 ballistic and 84 cruise missiles and 404 drones rain down "
               "on Kyiv — three bridges over the Dnipro damaged, at least "
               "eight killed. Two missiles and a jet-powered drone fall in "
               "Poland; PM Tusk calls it a \u2018deliberate provocation\u2019.")
    y = block(draw, MARGIN, y, wrap(draw, subhead, sub, W - 2 * MARGIN),
              sub, INK, leading=24)
    y += 10

    # Drawn skyline panel + caption.
    panel_h = 130
    draw_skyline(draw, MARGIN, y, W - 2 * MARGIN, panel_h)
    y += panel_h + 6
    cap = SANS_O(12)
    caption = ("Illustration drawn for this front page: Kyiv's skyline and the "
               "Dnipro bridges under attack.")
    y = block(draw, MARGIN, y, wrap(draw, caption, cap, W - 2 * MARGIN),
              cap, GREY, leading=16)
    y += 4
    y = rule(draw, y, width=1, color=LIGHT_RULE)
    y += 12

    # Secondary stories: 2 x 2 grid.
    stories = [
        ("THE HAGUE",
         "ICJ rules Myanmar committed genocide",
         "In a 9–6 verdict, the Court holds a state responsible for genocide "
         "for the first time — over the Rohingya. Reparations and a safe "
         "return are ordered."),
        ("SHENZHEN",
         "Trump, Xi and Putin: \u2018A nuclear war must never be fought\u2019",
         "A trilateral peace declaration in Shenzhen. No mention of Ukraine "
         "or Iran; UN reform on the agenda."),
        ("LONDON · BRUSSELS",
         "UK–EU reset deal struck in Brussels",
         "Food-trade easing worth an estimated +£5.1bn a year from March "
         "2028, an emissions-trading link in 2028, and a youth scheme for "
         "100,000 a year by 2030."),
        ("MARKETS",
         "Anthropic's $81bn IPO at a $1.5tn valuation",
         "A record listing amid a tech sell-off, as Asian shares head for "
         "their worst week since 2020."),
    ]
    col_w = (W - 2 * MARGIN - 24) // 2
    row_y = y
    for idx, (kick, hline, body) in enumerate(stories):
        cx = MARGIN + (idx % 2) * (col_w + 24)
        cy = row_y + (idx // 2) * 138
        draw.text((cx, cy), kick, font=SANS_B(12), fill=RED)
        cy += 18
        hf = SERIF_B(20)
        hlines = wrap(draw, hline, hf, col_w)[:2]
        cy = block(draw, cx, cy, hlines, hf, INK, leading=24)
        cy += 2
        bf = SANS(14)
        blines = wrap(draw, body, bf, col_w)[:3]
        block(draw, cx, cy, blines, bf, INK, leading=18)
    y = row_y + 2 * 138 + 4
    y = rule(draw, y, width=1, color=LIGHT_RULE)
    y += 8

    # Briefs strip.
    draw.text((MARGIN, y), "IN BRIEF", font=SANS_B(13), fill=RED)
    y += 20
    briefs = [
        "Denmark accuses Russia of plotting to assassinate a US-Ukrainian "
        "rapper; expels a diplomat.",
        "Mamdani vows to close Rikers Island by 2032.",
        "US declassifies more UFO footage in an eighth Pentagon tranche.",
        "Trump threatens to ban US firms from building AI data centres "
        "overseas.",
        "ANC fights to hold South Africa's key cities.",
        "Kryvyi Rih strike: 2 dead, 42 injured, including 4 children.",
    ]
    bf = SANS(13)
    for row in range(3):
        rh = 0
        for col in range(2):
            bx = MARGIN + col * (col_w + 24)
            text = "•  " + briefs[row * 2 + col]
            lines = wrap(draw, text, bf, col_w)[:2]
            block(draw, bx, y, lines, bf, INK, leading=16)
            rh = max(rh, len(lines) * 16)
        y += rh + 6

    # Footer.
    y = rule(draw, H - 44, width=1, color=LIGHT_RULE)
    foot = SANS(11)
    ftext = "THE WORLD TODAY — 21 NOVEMBER 2026 · SUMMARISED BY AN AI AGENT FOR MAKE.FUN"
    fw = draw.textlength(ftext, font=foot)
    draw.text(((W - fw) / 2, H - 36), ftext, font=foot, fill=GREY)

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", str(HERE)))
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
