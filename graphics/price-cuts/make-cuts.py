# Re-crop Kyle's Zillow screenshots into Instagram-safe 1080x1920 frames:
# the main house photo + the "Price cut" / price / address block, scaled 0.9, stacked so the price block ends
# above y=1440 (Instagram's username/caption area) and the photo starts below y=250 (the top chrome).
# The map row and the "Est. $/mo" bar between them are dropped; the bottom of the first photo peeks in at the top.
#   python3 -I make-cuts.py <folder with IMG_*.PNG> <out folder>
import sys, numpy as np
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
order = ["IMG_8646","IMG_8648","IMG_8649","IMG_8651","IMG_8652","IMG_8654","IMG_8655"]
S = 0.9; W = 1080; HERO = 808; TOP = 250
for i, n in enumerate(order, 1):
    im = Image.open(f"{src}/{n}.PNG").convert("RGB"); a = np.asarray(im).astype(int); H = a.shape[0]
    sd = a.std(axis=(1, 2)); uni = sd < 8
    p1_end = next(y for y in range(200, H) if uni[y])            # first photo ends at the first uniform row
    med = np.median(a, axis=1); green = (med[:, 0] < 90) & (med[:, 1] > 90) & (med[:, 2] > 90) & (med[:, 1] < 140)
    runs = []; s = None
    for y in range(H):
        if green[y] and s is None: s = y
        if not green[y] and s is not None: runs.append((s, y)); s = None
    g0, g1 = [r for r in runs if r[1] - r[0] > 100][-1]          # the Est. $/mo bar is the last tall green run
    hero_top = p1_end + 4; hero_bot = hero_top + HERO
    hero = im.crop((0, hero_top, im.width, hero_bot))
    price = im.crop((0, g1 + 1, im.width, H))
    sw = round(im.width * S)
    hero_s = hero.resize((sw, round(hero.height * S)), Image.LANCZOS)
    price_s = price.resize((sw, round(price.height * S)), Image.LANCZOS)
    # Background: the house photo blown up, blurred and darkened, edge to edge, so nothing in the frame is a void
    # (Kyle, 2026-10-30: the navy under the card "still looks a little weird"). The listing floats on it as a card.
    from PIL import ImageFilter, ImageEnhance, ImageDraw
    bg = hero.resize((round(hero.width * 1920 / hero.height), 1920), Image.LANCZOS)
    bg = bg.crop(((bg.width - W) // 2, 0, (bg.width - W) // 2 + W, 1920)).filter(ImageFilter.GaussianBlur(45))
    frame = ImageEnhance.Brightness(bg).enhance(0.6)
    CW = 1000; cx = (W - CW) // 2; ox = (sw - CW) // 2                 # card 1000 wide, photo cropped both sides
    card = Image.new("RGB", (CW, hero_s.height + price_s.height + 12), "white")
    card.paste(hero_s.crop((ox, 0, ox + CW, hero_s.height)), (0, 0))
    card.paste(price_s.crop((0, 0, CW, price_s.height)), (0, hero_s.height))   # price block keeps its left edge
    mask = Image.new("L", card.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, card.width - 1, card.height - 1], radius=28, fill=255)
    frame.paste(card, (cx, TOP), mask)
    bottom = TOP + card.height
    frame.save(f"{out}/cut{i}.jpg", quality=90)
    print(i, n, "p1_end", p1_end, "green", g0, g1, "hero", hero_top, hero_bot, "-> price block ends at", bottom)
