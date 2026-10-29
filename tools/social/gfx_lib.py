import os, glob
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "assets", "social", "daily")
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1350
NAVY = (10, 31, 68); NAVY2 = (16, 44, 94); GOLD = (217, 184, 105); WHITE = (255, 255, 255); MUTED = (196, 210, 230)

def font(name, size):
    paths = {
        "serifb": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "sansb": glob.glob("/usr/share/fonts/**/Inter-Bold.*", recursive=True) or glob.glob("/usr/share/fonts/**/Inter*Bold*.ttf", recursive=True),
        "sans": glob.glob("/usr/share/fonts/**/Inter-Regular.*", recursive=True) or glob.glob("/usr/share/fonts/**/Inter*Regular*.ttf", recursive=True),
        "sansm": glob.glob("/usr/share/fonts/**/Inter-SemiBold.*", recursive=True) or glob.glob("/usr/share/fonts/**/Inter*SemiBold*.ttf", recursive=True),
    }
    p = paths[name]
    if isinstance(p, list):
        p = p[0] if p else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p, size)

LOGO = Image.open(f"{HERE}/logo/precision-logo-horizontal-reversed.png").convert("RGBA")
EMBLEM = Image.open(f"{HERE}/logo/precision-emblem.png").convert("RGBA")

def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def base():
    im = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(im)
    for y in range(H):  # soft vertical gradient
        t = y / H
        c = tuple(int(NAVY[i] * (1 - t) + NAVY2[i] * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    # faint target rings bottom-right (brand motif)
    ring = Image.new("RGBA", (W, H), (0, 0, 0, 0)); rd = ImageDraw.Draw(ring)
    cx, cy = W - 120, H - 330
    for r in (120, 220, 320, 420):
        rd.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(255, 255, 255, 18), width=3)
    rd.line((cx - 460, cy, cx + 460, cy), fill=(255, 255, 255, 14), width=2)
    rd.line((cx, cy - 460, cx, cy + 460), fill=(255, 255, 255, 14), width=2)
    im = Image.alpha_composite(im.convert("RGBA"), ring)
    return im

def footer(im, cta):
    d = ImageDraw.Draw(im)
    d.line((80, H - 210, W - 80, H - 210), fill=GOLD, width=2)
    lg = LOGO.copy(); lg.thumbnail((400, 115))
    im.alpha_composite(lg, (80, H - 172))
    f = font("sansm", 27)
    d.text((W - 80, H - 135), cta, font=f, fill=GOLD, anchor="rm")
    d.text((W - 80, H - 92), "precisioncertifications.com", font=font("sans", 26), fill=MUTED, anchor="rm")
    return im

def card(fname, eyebrow, title, items=None, body=None, cta="Request a quote", numbered=False):
    im = base(); d = ImageDraw.Draw(im)
    x, y, maxw = 80, 110, W - 160
    d.text((x, y), eyebrow.upper(), font=font("sansm", 30), fill=GOLD); y += 70
    tf = font("serifb", 76)
    for ln in wrap(d, title, tf, maxw):
        d.text((x, y), ln, font=tf, fill=WHITE); y += 92
    y += 30
    if body:
        bf = font("sans", 38)
        for para in body:
            for ln in wrap(d, para, bf, maxw):
                d.text((x, y), ln, font=bf, fill=MUTED); y += 54
            y += 22
    if items:
        hf = font("sansb", 40); bf = font("sans", 34)
        for i, it in enumerate(items, 1):
            head, sub = it if isinstance(it, tuple) else (it, None)
            mark = f"{i}" if numbered else ""
            if numbered:
                d.ellipse((x, y + 2, x + 52, y + 54), outline=GOLD, width=3)
                d.text((x + 26, y + 28), mark, font=font("sansb", 30), fill=GOLD, anchor="mm")
            else:
                d.rectangle((x + 4, y + 18, x + 20, y + 34), fill=GOLD)
            tx = x + 76 if numbered else x + 44
            for ln in wrap(d, head, hf, maxw - (tx - x)):
                d.text((tx, y), ln, font=hf, fill=WHITE); y += 52
            if sub:
                for ln in wrap(d, sub, bf, maxw - (tx - x)):
                    d.text((tx, y), ln, font=bf, fill=MUTED); y += 46
            y += 26
    assert y < H - 230, (fname, y)
    footer(im, cta)
    im.convert("RGB").save(f"{OUT}/{fname}", quality=92)
    return y
