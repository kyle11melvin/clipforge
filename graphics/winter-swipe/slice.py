# Slice the 8640x1350 strip into eight 1080x1350 slides: python3 graphics/winter-swipe/slice.py strip.png outdir
import sys
from PIL import Image
im = Image.open(sys.argv[1]).convert("RGB")
for i in range(im.width // 1080):
    im.crop((i * 1080, 0, (i + 1) * 1080, im.height)).save(f"{sys.argv[2]}/slide-{i + 1}.png")
