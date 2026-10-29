"""Card templates for social posts. Usage:
    from templates import quiz_img, tip_img, myth_img, ask_img, emblem_img, card
Each writes a 1080x1350 JPG into assets/social/daily/.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gfx_lib import *
import gfx_lib
OUTD = gfx_lib.OUT
os.makedirs(OUTD, exist_ok=True)
def save(im, fname):
    im.convert("RGB").save(f"{OUTD}/{fname}", quality=90)
CORAL = (240, 140, 120)

def save(im, fname):
    im.convert("RGB").save(f"{OUTD}/{fname}", quality=90)

def quiz_img(fname, n, q, opts):
    im = base(); d = ImageDraw.Draw(im); x, y, maxw = 80, 110, W - 160
    d.text((x, y), f"DAILY IPC QUIZ  ·  #{n}", font=font("sansm", 30), fill=GOLD); y += 70
    tf = font("serifb", 64)
    for ln in wrap(d, q, tf, maxw):
        d.text((x, y), ln, font=tf, fill=WHITE); y += 80
    y += 40
    of = font("sansb", 40)
    for letter, o in zip("ABC", opts):
        lines = wrap(d, o, of, maxw - 130)
        h = 50 * len(lines) + 50
        d.rounded_rectangle((x, y, W - 80, y + h), radius=18, outline=GOLD, width=3, fill=(28, 58, 112))
        d.ellipse((x + 24, y + h // 2 - 30, x + 84, y + h // 2 + 30), fill=GOLD)
        d.text((x + 54, y + h // 2), letter, font=font("sansb", 34), fill=NAVY, anchor="mm")
        ty = y + 25
        for ln in lines:
            d.text((x + 110, ty), ln, font=of, fill=WHITE); ty += 50
        y += h + 26
    assert y < H - 230, (fname, y)
    footer(im, "Comment A, B or C")
    save(im, fname)

def myth_img(fname, myth, fact):
    im = base(); d = ImageDraw.Draw(im); x, y, maxw = 80, 110, W - 160
    d.text((x, y), "MYTH VS. FACT", font=font("sansm", 30), fill=GOLD); y += 90
    for label, text, col, tf in (("MYTH", myth, CORAL, font("serifb", 58)), ("FACT", fact, GOLD, font("sansb", 44))):
        d.text((x, y), label, font=font("sansb", 36), fill=col); y += 60
        for ln in wrap(d, text, tf, maxw):
            d.text((x, y), ln, font=tf, fill=WHITE if label == "FACT" else MUTED); y += int(tf.size * 1.25)
        y += 50
    assert y < H - 230, (fname, y)
    footer(im, "Taught by a Certified IPC Trainer")
    save(im, fname)

def ask_img(fname, eyebrow, q, sub):
    im = base(); d = ImageDraw.Draw(im)
    tf = font("serifb", 74); lines = wrap(d, q, tf, W - 200)
    total = 70 + len(lines) * 92 + 80
    y = (H - 230 - total) // 2 + 20
    d.text((W // 2, y), eyebrow.upper(), font=font("sansm", 32), fill=GOLD, anchor="ma"); y += 70
    for ln in lines:
        d.text((W // 2, y), ln, font=tf, fill=WHITE, anchor="ma"); y += 92
    y += 30
    d.text((W // 2, y), sub + "  👇" if False else sub, font=font("sansm", 38), fill=GOLD, anchor="ma")
    footer(im, "Join the conversation")
    save(im, fname)

def emblem_img(fname, eyebrow, title, body, cta):
    im = base(); d = ImageDraw.Draw(im)
    em = EMBLEM.copy(); em.thumbnail((320, 320)); im.alpha_composite(em, ((W - em.width) // 2, 140))
    d.text((W // 2, 540), eyebrow.upper(), font=font("sansm", 32), fill=GOLD, anchor="mm")
    y = 600; tf = font("serifb", 70)
    for ln in wrap(d, title, tf, W - 200):
        d.text((W // 2, y), ln, font=tf, fill=WHITE, anchor="ma"); y += 86
    y += 30; bf = font("sans", 36)
    for ln in wrap(d, body, bf, W - 220):
        d.text((W // 2, y), ln, font=bf, fill=MUTED, anchor="ma"); y += 52
    assert y < H - 230, (fname, y)
    footer(im, cta)
    save(im, fname)

def tip_img(fname, n, title, body):
    im = base(); d = ImageDraw.Draw(im); x, y, maxw = 80, 150, W - 160
    d.text((x, y), f"TECH TIP  ·  #{n}", font=font("sansm", 32), fill=GOLD); y += 80
    tf = font("serifb", 84)
    for ln in wrap(d, title, tf, maxw):
        d.text((x, y), ln, font=tf, fill=WHITE); y += 102
    y += 30; d.line((x, y, x + 120, y), fill=GOLD, width=5); y += 50
    bf = font("sans", 48)
    for ln in wrap(d, body, bf, maxw):
        d.text((x, y), ln, font=bf, fill=MUTED); y += 66
    assert y < H - 230, (fname, y)
    footer(im, "Save this for your team")
    save(im, fname)

