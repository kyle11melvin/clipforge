# Derived layers: blurred 1080x1920 backgrounds, the bright "streams" cutout for the convergence scene,
# and the logo + wordmark cutout for the end card.
import numpy as np, cv2
from pathlib import Path
from PIL import Image, ImageFilter
root = Path("graphics/switchboard"); (root/"bg").mkdir(exist_ok=True)
for n in range(1, 11):
    im = Image.open(root/"clean"/f"clean{n:02d}.png").convert("RGB")
    # cover-crop to 9:16 from the centre, then blur and darken
    w, h = im.size; tw = int(h*1080/1920)
    if tw <= w: c = im.crop(((w-tw)//2, 0, (w-tw)//2+tw, h))
    else: th = int(w*1920/1080); c = im.crop((0, max(0,(h-th)//2), w, max(0,(h-th)//2)+th))
    c = c.resize((1080, 1920), Image.LANCZOS).filter(ImageFilter.GaussianBlur(34))
    a = np.asarray(c).astype(np.float32)*0.62
    Image.fromarray(a.clip(0,255).astype(np.uint8)).save(root/"bg"/f"bg{n:02d}.jpg", quality=90)
# streams: bright saturated pixels of the convergence art, alpha from brightness
im = cv2.imread(str(root/"up"/"up07w.png")); hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV).astype(np.float32)
sat, val = hsv[...,1]/255, hsv[...,2]/255
alpha = np.clip((val-0.45)/0.35, 0, 1) * np.clip((sat-0.35)/0.3, 0, 1)
alpha = cv2.GaussianBlur(alpha, (0,0), 2)
rgba = np.dstack([im, (alpha*255).astype(np.uint8)])
cv2.imwrite(str(root/"streams.png"), rgba)
# logo + wordmark cutout from the brand panel
im = cv2.imread(str(root/"up"/"up10.png"))[40:520, 596:1624]
mx = im.max(axis=2).astype(np.float32)
alpha = np.clip((mx-28)/70, 0, 1)
# drop stray orbit sparkle: keep only pixels connected to large bright blobs
m8 = (alpha > 0.5).astype(np.uint8)
n, lab, stats, _ = cv2.connectedComponentsWithStats(m8, 8)
keep = np.zeros_like(m8)
for i in range(1, n):
    if stats[i, cv2.CC_STAT_AREA] > 400: keep[lab == i] = 1
keep = cv2.dilate(keep, np.ones((9,9), np.uint8))
alpha = alpha * keep
rgba = np.dstack([im, (alpha*255).astype(np.uint8)])
cv2.imwrite(str(root/"logo.png"), rgba); print("logo", rgba.shape)
