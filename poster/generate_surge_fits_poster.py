from pathlib import Path
import math
import textwrap

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"
PNG_PATH = OUTPUT_DIR / "surge-fits-poster-v1.png"
PDF_PATH = OUTPUT_DIR / "surge-fits-poster-v1.pdf"

WIDTH = 1600
HEIGHT = 2000

IVORY = (244, 239, 230, 255)
DARK = (9, 16, 38, 255)
NAVY = (14, 24, 56, 255)
NAVY_SOFT = (25, 38, 82, 255)
GOLD = (199, 154, 74, 255)
GOLD_BRIGHT = (231, 197, 118, 255)
MUTED = (112, 115, 126, 255)
WHITE = (255, 255, 255, 255)
SHADOW = (8, 12, 28, 80)


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size=size)


DISPLAY = font("BOD_B.TTF", 126)
DISPLAY_SMALL = font("BOD_B.TTF", 66)
QUOTE = font("BOD_B.TTF", 54)
SERIF = font("georgia.ttf", 34)
SERIF_ITALIC = font("georgiai.ttf", 34)
SANS = font("segoeui.ttf", 30)
SANS_SMALL = font("segoeui.ttf", 24)
SANS_BOLD = font("segoeuib.ttf", 30)
SANS_TINY = font("segoeui.ttf", 19)


def vertical_gradient(size, top, bottom):
    img = Image.new("RGBA", size)
    px = img.load()
    for y in range(size[1]):
        t = y / max(size[1] - 1, 1)
        color = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(4))
        for x in range(size[0]):
            px[x, y] = color
    return img


def add_shadow(base: Image.Image, box, radius=18, offset=(0, 12), color=SHADOW, corner=28):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    ox, oy = offset
    draw.rounded_rectangle((x0 + ox, y0 + oy, x1 + ox, y1 + oy), radius=corner, fill=color)
    layer = layer.filter(ImageFilter.GaussianBlur(radius))
    base.alpha_composite(layer)


def wrap(draw: ImageDraw.ImageDraw, text: str, font_obj, max_width: int):
    words = text.split()
    lines = []
    current = []
    for word in words:
        test = " ".join(current + [word])
        if draw.textbbox((0, 0), test, font=font_obj)[2] <= max_width:
            current.append(word)
        else:
            lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def draw_multiline(draw, xy, text, font_obj, fill, max_width, line_gap=8):
    lines = wrap(draw, text, font_obj, max_width)
    x, y = xy
    bbox = draw.textbbox((0, 0), "Ag", font=font_obj)
    line_height = bbox[3] - bbox[1] + line_gap
    for line in lines:
        draw.text((x, y), line, font=font_obj, fill=fill)
        y += line_height
    return y


def draw_glow_circle(layer, center, radius, color, blur=60):
    temp = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(temp)
    x, y = center
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)
    temp = temp.filter(ImageFilter.GaussianBlur(blur))
    layer.alpha_composite(temp)


def draw_gold_streak(layer, points, width=20, blur=12):
    temp = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(temp)
    draw.line(points, fill=(210, 169, 84, 170), width=width)
    draw.line(points, fill=(245, 220, 150, 90), width=max(2, width // 3))
    temp = temp.filter(ImageFilter.GaussianBlur(blur))
    layer.alpha_composite(temp)


def draw_panel(base, box, fill, outline=None, corner=34):
    add_shadow(base, box)
    panel = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(panel)
    draw.rounded_rectangle(box, radius=corner, fill=fill, outline=outline, width=2 if outline else 0)
    base.alpha_composite(panel)


def draw_suit_card(base, box, accent, title, style):
    draw_panel(base, box, (255, 255, 255, 246), outline=(240, 229, 208, 255), corner=24)
    panel = ImageDraw.Draw(base)
    x0, y0, x1, y1 = box
    panel.rounded_rectangle((x0 + 16, y0 + 16, x1 - 16, y1 - 16), radius=18, outline=(230, 224, 213, 255), width=2)
    cx = (x0 + x1) // 2
    panel.ellipse((cx - 26, y0 + 28, cx + 26, y0 + 80), fill=(218, 203, 183, 255))
    jacket = [(cx - 54, y0 + 94), (cx - 22, y0 + 80), (cx, y0 + 100), (cx + 22, y0 + 80), (cx + 54, y0 + 94), (cx + 48, y1 - 32), (cx - 48, y1 - 32)]
    panel.polygon(jacket, fill=accent)
    panel.polygon([(cx - 22, y0 + 80), (cx - 4, y0 + 132), (cx, y0 + 100)], fill=(245, 241, 236, 255))
    panel.polygon([(cx + 22, y0 + 80), (cx + 4, y0 + 132), (cx, y0 + 100)], fill=(245, 241, 236, 255))
    tie_color = (89, 64, 42, 255) if style == "classic" else (52, 46, 95, 255)
    panel.polygon([(cx, y0 + 100), (cx - 8, y0 + 128), (cx, y1 - 46), (cx + 8, y0 + 128)], fill=tie_color)
    panel.text((x0 + 22, y1 - 48), title, font=SANS_TINY, fill=(37, 41, 52, 255))


def draw_arrow_stack(draw, x, y, color):
    for i in range(4):
        top = y + i * 48
        draw.polygon([(x, top), (x + 38, top + 20), (x, top + 40), (x + 12, top + 20)], fill=color)


def draw_mannequin(draw, x, y, scale, jacket_color, shirt_color, gold_lines=False):
    head_w = 96 * scale
    head_h = 118 * scale
    draw.ellipse((x - head_w / 2, y, x + head_w / 2, y + head_h), fill=(232, 224, 212, 255))
    neck_y = y + head_h - 8 * scale
    shoulders = y + head_h + 12 * scale
    hem = shoulders + 290 * scale
    body = [(x - 70 * scale, shoulders), (x - 38 * scale, neck_y), (x, neck_y + 16 * scale), (x + 38 * scale, neck_y), (x + 70 * scale, shoulders), (x + 62 * scale, hem), (x - 62 * scale, hem)]
    draw.polygon(body, fill=jacket_color)
    draw.polygon([(x - 38 * scale, neck_y), (x - 10 * scale, shoulders + 60 * scale), (x, neck_y + 16 * scale)], fill=shirt_color)
    draw.polygon([(x + 38 * scale, neck_y), (x + 10 * scale, shoulders + 60 * scale), (x, neck_y + 16 * scale)], fill=shirt_color)
    if gold_lines:
        draw.line((x - 54 * scale, shoulders + 22 * scale, x - 16 * scale, hem - 18 * scale), fill=GOLD_BRIGHT, width=max(2, int(5 * scale)))
        draw.line((x + 54 * scale, shoulders + 22 * scale, x + 16 * scale, hem - 18 * scale), fill=GOLD_BRIGHT, width=max(2, int(5 * scale)))


def draw_main_figure(draw, x, y, scale):
    skin = (120, 74, 45, 255)
    head_w = 128 * scale
    head_h = 160 * scale
    draw.ellipse((x - head_w / 2, y, x + head_w / 2, y + head_h), fill=skin)
    shoulders = y + head_h + 28 * scale
    neck_y = y + head_h - 12 * scale
    waist = shoulders + 280 * scale
    hem = waist + 260 * scale
    draw.polygon([(x - 104 * scale, shoulders), (x - 54 * scale, neck_y), (x, neck_y + 18 * scale), (x + 54 * scale, neck_y), (x + 104 * scale, shoulders), (x + 86 * scale, hem), (x - 86 * scale, hem)], fill=(23, 31, 66, 255))
    draw.polygon([(x - 56 * scale, neck_y), (x - 10 * scale, shoulders + 100 * scale), (x, neck_y + 18 * scale)], fill=(247, 246, 243, 255))
    draw.polygon([(x + 56 * scale, neck_y), (x + 10 * scale, shoulders + 100 * scale), (x, neck_y + 18 * scale)], fill=(247, 246, 243, 255))
    draw.polygon([(x, neck_y + 18 * scale), (x - 18 * scale, shoulders + 120 * scale), (x, hem - 70 * scale), (x + 18 * scale, shoulders + 120 * scale)], fill=(63, 52, 39, 255))
    draw.line((x - 76 * scale, shoulders + 36 * scale, x - 24 * scale, hem - 18 * scale), fill=GOLD_BRIGHT, width=max(2, int(6 * scale)))
    draw.line((x + 76 * scale, shoulders + 36 * scale, x + 24 * scale, hem - 18 * scale), fill=GOLD_BRIGHT, width=max(2, int(6 * scale)))
    draw.line((x - 106 * scale, shoulders + 160 * scale, x - 192 * scale, shoulders + 340 * scale), fill=skin, width=max(6, int(26 * scale)))
    draw.line((x + 104 * scale, shoulders + 160 * scale, x + 176 * scale, shoulders + 318 * scale), fill=skin, width=max(6, int(26 * scale)))
    draw.line((x - 30 * scale, hem, x - 36 * scale, hem + 160 * scale), fill=(14, 14, 16, 255), width=max(6, int(22 * scale)))
    draw.line((x + 30 * scale, hem, x + 36 * scale, hem + 160 * scale), fill=(14, 14, 16, 255), width=max(6, int(22 * scale)))


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    poster = Image.new("RGBA", (WIDTH, HEIGHT), IVORY)
    left_w = int(WIDTH * 0.46)
    right = vertical_gradient((WIDTH - left_w, HEIGHT), NAVY_SOFT, DARK)
    poster.alpha_composite(right, (left_w, 0))

    glow = Image.new("RGBA", poster.size, (0, 0, 0, 0))
    draw_glow_circle(glow, (WIDTH - 120, 70), 210, (19, 24, 52, 230), blur=30)
    draw_glow_circle(glow, (WIDTH - 60, HEIGHT - 100), 230, (10, 14, 34, 210), blur=30)
    draw_glow_circle(glow, (180, HEIGHT - 140), 140, (215, 173, 95, 80), blur=55)
    poster.alpha_composite(glow)

    gold = Image.new("RGBA", poster.size, (0, 0, 0, 0))
    draw_gold_streak(gold, [(76, 820), (160, 730), (245, 610), (330, 470)], width=20, blur=10)
    draw_gold_streak(gold, [(980, 0), (940, 130), (890, 250)], width=18, blur=12)
    draw_gold_streak(gold, [(1240, 40), (1320, 112), (1410, 180)], width=16, blur=12)
    poster.alpha_composite(gold)

    draw = ImageDraw.Draw(poster)
    draw.rectangle((left_w - 2, 0, left_w + 2, HEIGHT), fill=(220, 211, 193, 255))

    y = 108
    draw.text((86, y), "SURGE", font=DISPLAY, fill=(22, 28, 36, 255))
    y += 102
    draw.text((86, y), "FITS", font=DISPLAY, fill=(22, 28, 36, 255))
    y += 128
    draw.text((90, y), "Quality Beyond Expression", font=SERIF_ITALIC, fill=GOLD)
    y += 90
    body = (
        "Premium tailoring for men who want to look refined, feel confident, "
        "and stand out with timeless craftsmanship."
    )
    y = draw_multiline(draw, (90, y), body, SANS, MUTED, 480, line_gap=12)

    panel_box = (82, y + 44, 504, y + 360)
    draw_panel(poster, panel_box, (31, 39, 69, 240), outline=(66, 79, 123, 255))
    draw.text((112, y + 78), "We Specialize In", font=SANS_BOLD, fill=WHITE)
    items = [
        "Custom Tailored Suits",
        "Wedding & Formal Wear",
        "Executive & Casual Fits",
        "Alterations & Restyling",
    ]
    iy = y + 140
    for item in items:
        draw.ellipse((118, iy + 12, 132, iy + 26), fill=GOLD_BRIGHT)
        draw.text((150, iy), item, font=SANS_SMALL, fill=(230, 234, 245, 255))
        iy += 54

    quote_box = (82, 1498, 560, 1758)
    draw_panel(poster, quote_box, (255, 252, 247, 248), outline=(229, 220, 204, 255), corner=28)
    draw.text((112, 1536), "Style that speaks", font=QUOTE, fill=(17, 24, 48, 255))
    draw.text((112, 1594), "before you do.", font=QUOTE, fill=(17, 24, 48, 255))
    draw.text((116, 1676), "Book your fit for weddings, office wear, events,", font=SANS_SMALL, fill=MUTED)
    draw.text((116, 1718), "or your next statement look.", font=SANS_SMALL, fill=MUTED)

    footer_box = (82, 1810, 560, 1942)
    draw_panel(poster, footer_box, (17, 25, 52, 255), outline=(58, 70, 109, 255), corner=24)
    draw.text((112, 1843), "@surge_fits", font=SANS_BOLD, fill=WHITE)
    draw.text((112, 1884), "DM or WhatsApp for fittings and orders", font=SANS_TINY, fill=(214, 219, 234, 255))

    draw.text((760, 172), "Modern luxury", font=SERIF_ITALIC, fill=(218, 196, 143, 255))
    draw.text((760, 224), "crafted for presence", font=SERIF, fill=(238, 238, 238, 255))

    draw_mannequin(draw, 980, 470, 1.05, (38, 45, 81, 255), (244, 239, 232, 255), gold_lines=True)
    draw_main_figure(draw, 1170, 380, 1.35)
    draw_mannequin(draw, 1430, 438, 1.15, (84, 86, 95, 255), (241, 237, 231, 255))
    draw_arrow_stack(draw, 1484, 876, (96, 103, 135, 255))

    cards = [
        ((666, 1440, 886, 1760), (196, 189, 174, 255), "Vintage Tux", "classic"),
        ((900, 1380, 1120, 1700), (36, 53, 98, 255), "Royal Cut", "classic"),
        ((1134, 1440, 1354, 1760), (118, 66, 101, 255), "Evening Fit", "modern"),
    ]
    for box, color, title, style in cards:
        draw_suit_card(poster, box, color, title, style)

    badge = Image.new("RGBA", poster.size, (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(badge)
    badge_box = (1256, 118, 1476, 222)
    bdraw.rounded_rectangle(badge_box, radius=20, fill=(214, 182, 114, 40), outline=(220, 190, 128, 160), width=2)
    poster.alpha_composite(badge.filter(ImageFilter.GaussianBlur(0)))
    draw.text((1292, 148), "Premium tailoring", font=SANS_TINY, fill=(241, 224, 188, 255))

    poster = poster.convert("RGB")
    poster.save(PNG_PATH, quality=95)
    poster.save(PDF_PATH, resolution=300.0)
    print(PNG_PATH)
    print(PDF_PATH)


if __name__ == "__main__":
    main()
