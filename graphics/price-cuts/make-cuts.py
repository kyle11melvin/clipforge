# Re-crop Kyle's Zillow screenshots into Instagram-safe 1080x1920 frames:
# the main house photo + the "Price cut" / price / address block, scaled 0.9, stacked so the price block ends
# above y=1440 (Instagram's username/caption area) and the photo starts below y=250 (the top chrome).
# The map row and the "Est. $/mo" bar between them are dropped; the bottom of the first photo peeks in at the top.
#   python3 -I make-cuts.py <folder with IMG_*.PNG> <out folder>
import sys, numpy as np
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
order = ["IMG_8646","IMG_8648","IMG_8649","IMG_8651","IMG_8652","IMG_8654","IMG_8655"]
S = 0.9; W = 1080; HERO = 808; TOP = 265
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
    lead = int(TOP / S)                                            # strip of the page above the hero, under IG chrome
    top_part = im.crop((0, hero_top - lead, im.width, hero_bot))
    price = im.crop((0, g1 + 1, im.width, H))
    sw = round(im.width * S)
    top_part = top_part.resize((sw, round(top_part.height * S)), Image.LANCZOS)
    price = price.resize((sw, round(price.height * S)), Image.LANCZOS)
    frame = Image.new("RGB", (W, 1920), (23, 63, 79))                # navy below the price block, not a white void
    x = (W - sw) // 2
    frame.paste(top_part, (x, 0))                                  # photos centred (crop both sides)
    frame.paste(price, (0, top_part.height))                       # price block keeps its left edge
    bottom = top_part.height + price.height
    frame.paste((255, 255, 255), (0, bottom, W, bottom + 24))          # a little page under the address, then navy
    frame.save(f"{out}/cut{i}.jpg", quality=90)
    print(i, n, "p1_end", p1_end, "green", g0, g1, "hero", hero_top, hero_bot, "-> price block ends at", bottom)
