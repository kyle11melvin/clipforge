# Remove the storyboard's scene numbers, timestamps, production labels and baked-in headline copy
# from each panel crop so the artwork can carry clean text overlays. Text pixels inside the given
# rectangles are masked by brightness and filled with OpenCV's Telea inpainting.
import sys, cv2, numpy as np
from pathlib import Path
src = Path(sys.argv[1]); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
R = {  # panel: (crop x0, [rects to inpaint (x0,y0,x1,y1)], threshold)
  1: (0, [(0,0,180,52),(10,178,152,345)], 105),
  2: (0, [(0,0,225,52),(10,135,137,335)], 105),
  3: (0, [(0,0,235,52),(10,100,165,260)], 105),
  4: (0, [(0,0,230,52),(10,88,152,228)], 105),
  5: (0, [(0,0,240,52),(10,135,160,255)], 105),
  6: (0, [(0,0,220,52),(10,65,207,280)], 105),
  7: (0, [(0,0,210,52),(10,80,190,178)], 105),
  8: (75, [(0,0,240,52)], 105),
  9: (0, [(0,0,215,52),(10,75,200,220)], 105),
  10: (0, [(15,0,185,50),(70,170,490,250)], 95),
}
for n,(cx,rects,thr) in R.items():
    im = cv2.imread(str(src/f"panel{n:02d}.png"))
    im = im[:, cx:]
    mask = np.zeros(im.shape[:2], np.uint8)
    for (x0,y0,x1,y1) in rects:
        roi = im[y0:y1, x0:x1]
        m = (roi.max(axis=2) > thr).astype(np.uint8)*255
        m = cv2.dilate(m, np.ones((5,5),np.uint8), iterations=1)
        mask[y0:y1, x0:x1] = m
    res = cv2.inpaint(im, mask, 4, cv2.INPAINT_TELEA)
    # soften the inpainted region slightly so filled patches blend with the bokeh
    blur = cv2.GaussianBlur(res, (0,0), 2.0)
    soft = cv2.GaussianBlur(mask, (0,0), 3.0).astype(np.float32)/255.0
    res = (res*(1-soft[...,None]) + blur*soft[...,None]).astype(np.uint8)
    cv2.imwrite(str(out/f"clean{n:02d}.png"), res)
    print(n, im.shape[1], im.shape[0])
# stitch panel 07 with the left strip of panel 08 (the storyboard drew them as one continuous image)
p7 = cv2.imread(str(out/"clean07.png")); p8 = cv2.imread(str(src/"panel08.png"))
strip = p8[:, 0:62]
h = min(p7.shape[0], strip.shape[0])
st = np.concatenate([p7[:h], strip[:h]], axis=1)
cv2.imwrite(str(out/"clean07w.png"), st); print("07w", st.shape[1], st.shape[0])
