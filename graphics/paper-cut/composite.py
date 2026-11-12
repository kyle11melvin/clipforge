#!/usr/bin/env python3
"""Composite the paper-cut layers into one MP4.

  python3 graphics/paper-cut/composite.py videos/<post> [out.mp4] [--stickers=path/to/stickers.json]

Expects in that folder: punched.mp4 (footage with punch-ins), bg.mov and fg.mov (comp.html#bg / #fg
rendered with --alpha), cutout.mov (hyperframes remove-background of punched.mp4).

Stack, bottom to top: footage, bg (type behind him + the paper grounds of the cutaways), Kyle
(the full-frame cutout on footage; inside a cutaway a bust "sticker" with a white cut edge, moving
on twos like stop-motion), fg (torn strips, stamp, cutaway type).
"""
import subprocess, sys
import numpy as np
from scipy import ndimage as ndi


# Stickers: one per full-screen paper cutaway, listed in a JSON file (default: stickers.json beside this script).
#   {"tag": "A", "t0": 5.2, "t1": 6.56, "crop": [x, y, w, h], "scale": 0.74, "x": 150, "y": 590}
# t0/t1 are the cutaway window in seconds and must match the comp; crop is the part of the 1080x1920 frame kept;
# x, y is where the sticker's top-left lands. An empty list means type and paper over footage only.
import json, os
cfg = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--stickers=")), os.path.join(os.path.dirname(__file__), "stickers.json"))
sys.argv = [a for a in sys.argv if not a.startswith("--stickers=")]
STICKERS = json.load(open(cfg))
# --overlay=file.mov@seconds  an extra alpha layer on top (e.g. the cash heap), starting at that time
# --sfx=file.wav@gain         sound effects mixed under his voice
OVER = [a.split("=", 1)[1].rsplit("@", 1) for a in sys.argv if a.startswith("--overlay=")]
SFX = next((a.split("=", 1)[1].rsplit("@", 1) for a in sys.argv if a.startswith("--sfx=")), None)
sys.argv = [a for a in sys.argv if not a.startswith(("--overlay=", "--sfx="))]
d = sys.argv[1].rstrip("/")
out = sys.argv[2] if len(sys.argv) > 2 else f"{d}/final-papercut.mp4"
PAD, FPS, LEAD = 40, 12, 0.1


def build_sticker(s):
    """Cut the bust out of cutout.mov, keep only the biggest matte region (drops ceiling lights, signs
    and the selfie arm the matte sometimes grabs), add a white cut edge and a soft shadow."""
    cx, cy, cw, ch = s["crop"]
    s.setdefault("slide", 900)
    w, h = int(cw * s["scale"]) // 2 * 2, int(ch * s["scale"]) // 2 * 2
    W, H = w + 2 * PAD, h + 2 * PAD
    path = f"{d}/sticker-{s['tag']}.mov"
    rd = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(s["t0"] - LEAD), "-t", str(s["t1"] - s["t0"] + LEAD + 0.1),
                           "-i", f"{d}/cutout.mov", "-vf", f"fps={FPS},crop={cw}:{ch}:{cx}:{cy},scale={w}:{h},format=rgba",
                           "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    wr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS),
                           "-i", "-", "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", path],
                          stdin=subprocess.PIPE)
    n = 0
    while True:
        buf = rd.stdout.read(w * h * 4)
        if len(buf) < w * h * 4:
            break
        f = np.frombuffer(buf, np.uint8).reshape(h, w, 4).astype(np.float32) / 255
        a = f[..., 3]
        lab, k = ndi.label(a > 0.4)
        if k:
            sizes = ndi.sum(np.ones_like(lab), lab, range(1, k + 1))
            keep = ndi.binary_dilation(lab == 1 + int(np.argmax(sizes)), iterations=4)
            a = a * keep
        A = np.zeros((H, W), np.float32); A[PAD:PAD + h, PAD:PAD + w] = a
        RGB = np.zeros((H, W, 3), np.float32); RGB[PAD:PAD + h, PAD:PAD + w] = f[..., :3]
        edge = np.clip((ndi.gaussian_filter(A, 6) - 0.10) * 12, 0, 1)            # white paper edge, ~12 px
        shadow = np.roll(ndi.gaussian_filter(edge, 20), 14, axis=0) * 0.5
        shadow[:14] = 0                                                         # np.roll wraps the bottom rows to the top
        # shadow (black) under edge (white) under the photo
        oa = edge + shadow * (1 - edge)
        orgb = np.where(oa[..., None] > 0, (edge / np.maximum(oa, 1e-6))[..., None] * 0.96, 0.0) * np.ones(3)
        fa = A + oa * (1 - A)
        frgb = (RGB * A[..., None] + orgb * (oa * (1 - A))[..., None]) / np.maximum(fa, 1e-6)[..., None]
        wr.stdin.write((np.dstack([frgb, fa]).clip(0, 1) * 255).astype(np.uint8).tobytes())
        n += 1
    wr.stdin.close(); wr.wait(); rd.wait()
    print(f"sticker {s['tag']}: {n} frames -> {path}")
    return path


inputs = ["-i", f"{d}/punched.mp4", "-i", f"{d}/bg.mov", "-i", f"{d}/cutout.mov", "-i", f"{d}/fg.mov"]
for s in STICKERS:
    inputs += ["-itsoffset", str(s["t0"] - LEAD), "-i", build_sticker(s)]

off = "+".join(f"between(t,{s['t0']},{s['t1'] - 0.001})" for s in STICKERS)
g = f"[0:v][1:v]overlay[x0];[x0][2:v]overlay=enable='not({off})'[x1];"
for i, s in enumerate(STICKERS, 1):
    g += (f"[x{i}][{3 + i}:v]overlay=x={s['x'] - PAD}:y='{s['y'] - PAD}+900*pow(max(0,1-(t-{s['t0']})/0.28),3)':"
          f"eof_action=pass:enable='between(t,{s['t0']},{s['t1'] - 0.001})'[x{i + 1}];")
n = len(STICKERS) + 1
g += f"[x{n}][3:v]overlay[y0];"
k = 4 + len(STICKERS)
for i, (f, off) in enumerate(OVER):
    inputs += ["-itsoffset", off, "-i", f]
    g += f"[y{i}][{k}:v]overlay=eof_action=pass:enable='gte(t,{off})'[y{i + 1}];"; k += 1
g += f"[y{len(OVER)}]format=yuv420p[v]"
amap = "0:a"
if SFX:
    inputs += ["-i", SFX[0]]
    g += f";[0:a]aformat=sample_rates=48000:channel_layouts=stereo[vo];[{k}:a]volume={SFX[1]}[fx];[vo][fx]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[au]"
    amap = "[au]"

subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", g, "-map", "[v]", "-map", amap,
                "-c:v", "libx264", "-crf", "18", "-maxrate", "6M", "-bufsize", "12M", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out],
               check=True)
print("wrote", out)
