#!/usr/bin/env python3
"""THE WORLD IN ONE DAY — Wednesday, November 18, 2026.

Builds a 1024x1024 newspaper front-page image that sums up the world news
of 18 November 2026 and writes it to /output/entry.png.

The composition is fully deterministic: a fixed editorial illustration
(assets/illustration.png, no text in it) is cover-cropped into a band and
every word is rendered by this program with the bundled DejaVu fonts, so
two runs always produce byte-identical output. No network is used.

Stories shown (the day's verified top world news):
  1. US jets strike an IRGC missile site on Qeshm Island; Iran answers
     with drone attacks on US sites in Bahrain and Kuwait.
  2. Ukraine hits the Kerch (Crimea) Bridge for a second day; part of
     the road span collapses.
  3. Trump, Xi Jinping and Putin meet in Shenzhen for APEC.
  4. Ebola in DR Congo passes 11,000 cases and ~5,400 deaths.
  5. The US loses its measles elimination status after 26 years.
  6. NASA's Voyager 1 reaches one light-day from Earth.
  7. A Russian military plane crashes in Siberia (Kemerovo), 19 dead.
  8. Mary Peltola wins Alaska's Senate seat; Democrats take 56-44.

Requires: Python 3.13 with Pillow (pip install pillow).
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
ILLUSTRATION = ROOT / "assets" / "illustration.png"
FONT_DIR = ROOT / "assets" / "fonts"
OUTPUT = Path("/output/entry.png")

W, H = 1024, 1024

NAVY = (10, 34, 58)
NAVY_DARK = (6, 22, 40)
GOLD = (232, 178, 60)
GOLD_DARK = (176, 128, 20)
PAPER = (247, 242, 231)
INK = (24, 26, 30)
GREY = (92, 96, 104)
RED = (178, 34, 44)
TEAL = (8, 110, 118)
GREEN = (30, 110, 66)
PURPLE = (86, 54, 140)
WHITE = (255, 255, 255)
RULE = (205, 198, 182)


def bold(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / "DejaVuSans-Bold.ttf"), size)


def regular(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / "DejaVuSans.ttf"), size)


def text_w(draw: ImageDraw.ImageDraw, s: str, f) -> float:
    return draw.textlength(s, font=f)


def centered(draw, cx, y, s, f, fill):
    draw.text((cx - text_w(draw, s, f) / 2, y), s, font=f, fill=fill)


def wrap(draw, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def cover_crop(img: Image.Image, tw: int, th: int, valign: str = "center") -> Image.Image:
    """Resize + crop img to exactly tw x th (cover behaviour)."""
    scale = max(tw / img.width, th / img.height)
    nw, nh = round(img.width * scale), round(img.height * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - tw) // 2
    y = 0 if valign == "top" else (nh - th) // 2
    return img.crop((x, y, x + tw, y + th))


def story(draw, x, y, w, kicker, kicker_color, headline, sub, head_size):
    """Draw one story block; return the y just below it."""
    draw.text((x, y), kicker, font=bold(17), fill=kicker_color)
    yy = y + 27
    for line in wrap(draw, headline, bold(head_size), w):
        draw.text((x, yy), line, font=bold(head_size), fill=INK)
        yy += head_size + 6
    for line in wrap(draw, sub, regular(20), w):
        draw.text((x, yy), line, font=regular(20), fill=GREY)
        yy += 26
    return yy


def story_height(draw, w, headline, sub, head_size):
    """Measure a story block's height without drawing it."""
    h = 27
    h += len(wrap(draw, headline, bold(head_size), w)) * (head_size + 6)
    h += len(wrap(draw, sub, regular(20), w)) * 26
    return h


def build() -> Image.Image:
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- Masthead ------------------------------------------------------
    draw.rectangle([0, 0, W, 128], fill=NAVY)
    centered(draw, W // 2, 14, "THE WORLD IN ONE DAY", bold(58), WHITE)
    centered(draw, W // 2, 84, "WEDNESDAY, NOVEMBER 18, 2026", bold(29), GOLD)
    draw.rectangle([0, 128, W, 134], fill=GOLD)

    # ---- Illustration band --------------------------------------------
    band_y, band_h = 134, 318
    art = Image.open(ILLUSTRATION).convert("RGB")
    img.paste(cover_crop(art, W, band_h, valign="top"), (0, band_y))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, band_y + band_h, W, band_y + band_h + 4], fill=NAVY)

    # ---- Geometry -------------------------------------------------------
    margin, gutter = 24, 32
    col_w = (W - 2 * margin - gutter) // 2  # 472
    lx, rx = margin, margin + col_w + gutter
    foot_y = H - 54
    y = band_y + band_h + 20  # first story row top (476)

    # ---- Lead stories ---------------------------------------------------
    leads = [
        (lx, "GULF ESCALATION", RED,
         "US JETS STRIKE IRAN MISSILE SITE",
         "On Qeshm Island — Iran answers with drone attacks on US sites "
         "in Bahrain and Kuwait"),
        (rx, "UKRAINE WAR", TEAL,
         "CRIMEA BRIDGE HIT AGAIN",
         "Road span collapses in a second day of Ukrainian strikes "
         "on the Kerch Bridge"),
    ]
    lead_h = 0
    for x, kicker, color, head, sub in leads:
        draw.rectangle([x, y, x + 6, y + 118], fill=color)
        end = story(draw, x + 18, y, col_w - 18, kicker, color, head, sub, 29)
        lead_h = max(lead_h, end - y)
    y += lead_h + 14
    draw.line([margin, y, W - margin, y], fill=RULE, width=2)
    y += 14

    # ---- Six more stories, 2 columns x 3 rows ---------------------------
    stories = [
        ("SUMMIT · SHENZHEN", PURPLE, "TRUMP–XI–PUTIN MEET AT APEC",
         "A rare three-way summit in Shenzhen"),
        ("HEALTH · CONGO", RED, "EBOLA PASSES 11,000 CASES",
         "About 5,400 dead; children hit hardest"),
        ("SPACE", NAVY, "VOYAGER 1: ONE LIGHT-DAY OUT",
         "16 billion miles — the farthest ever"),
        ("HEALTH · USA", GREEN, "US LOSES MEASLES-FREE STATUS",
         "Ends 26 years; 5,400+ cases in 2026"),
        ("RUSSIA", TEAL, "MILITARY PLANE CRASH IN SIBERIA",
         "19 dead in the Kemerovo crash"),
        ("US POLITICS", GOLD_DARK, "PELTOLA WINS ALASKA SENATE SEAT",
         "Democrats take a 56–44 majority"),
    ]
    for row in range(3):
        pair = stories[row * 2: row * 2 + 2]
        heights = [story_height(draw, col_w, h, s, 24) for _, _, h, s in pair]
        for j, (kicker, color, head, sub) in enumerate(pair):
            story(draw, lx if j == 0 else rx, y, col_w,
                  kicker, color, head, sub, 24)
        y += max(heights) + 12

    assert y <= foot_y - 6, f"stories overflow: {y} > {foot_y}"

    # ---- Footer ticker (auto-fitted to width) ---------------------------
    draw.rectangle([0, foot_y, W, H], fill=NAVY_DARK)
    ticker = ("US STRIKES IRAN  •  CRIMEA BRIDGE HIT  •  SHENZHEN SUMMIT  •  "
              "EBOLA 11,000+  •  VOYAGER LIGHT-DAY")
    size = 19
    while size > 12 and text_w(draw, ticker, bold(size)) > W - 32:
        size -= 1
    centered(draw, W // 2, foot_y + 15, ticker, bold(size), GOLD)

    return img


def main() -> None:
    img = build()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    # Prefer a real PNG; if it would exceed the 1 MiB cap, store JPEG bytes
    # under the same name (the rules allow either, told apart by first bytes).
    tmp = OUTPUT.with_suffix(".tmp.png")
    img.save(tmp, format="PNG", optimize=True)
    if tmp.stat().st_size <= 1_048_576:
        tmp.replace(OUTPUT)
    else:
        tmp.unlink()
        img.save(OUTPUT, format="JPEG", quality=88, subsampling=1)
    print(f"wrote {OUTPUT} ({OUTPUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
