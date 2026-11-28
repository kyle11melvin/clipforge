#!/usr/bin/env python3
"""Stroller math, the tight cut (2026-11-28, Kyle: "tighten and clip a lot. Make it tight", ums out).

  python3 -I graphics/stroller-math/tight-cut.py <parakeet transcript of the 45 s cut> 

Reads videos/stroller-math/cut-full.mp4 (the whole take; the 45 s cut starts 5.58 s into it), keeps only KEEP,
alternates a punch-in on the face segments so the jump cuts read as intended, and writes cut.mp4, transcript.json
(word times moved to the new timeline, fillers dropped) and cues.json (new time of each word a graphic lands on).
KEEP times are Parakeet word edges in the 45 s cut. Whisper's were up to 0.7 s late on this take; do not use them."""
import json, subprocess, sys
OFF = 5.58
# (from, to, zoom)  zoom 1 = as shot, 1.08 = punched in
KEEP = [(1.58, 2.80, 1), (2.96, 5.94, 1), (6.22, 8.52, 1),          # I'm on a walk with my / son ... quick math / just thinking ... his future
        (8.70, 10.52, 1.08), (10.70, 11.70, 1.08), (11.74, 13.46, 1.08),               # Right now I'm putting about $250 / a month into / a Vanguard ETF
        (15.02, 16.24, 1), (16.80, 18.22, 1), (18.30, 19.42, 1),                       # By the time he's 18 / that's $54,000 / of my money
        (21.26, 22.22, 1), (22.38, 22.98, 1), (23.06, 23.92, 1),                       # 5 to 8% / I expect / to return
        (24.22, 24.64, 1), (24.80, 26.86, 1), (26.94, 28.62, 1),                       # somewhere / between $87,500 / and $120,000
        (31.42, 34.02, 1), (34.02, 34.88, 1.08), (35.04, 35.64, 1.08),                 # I hope that helps for his down payment on his home / or at least with his / education
        (38.86, 40.26, 1), (40.26, 41.70, 1), (41.90, 45.20, 1.08)]                    # What are you doing for your kids / And I'd love to hear more about it / drop your comments below
DROP = {"um", "uh"}
FIX = {"it": "to", "$120,000": "$120,000."}   # "I expect it return" is "to return"
src = "videos/stroller-math/cut-full.mp4"
fc, labels, t = [], [], 0.0
starts = []
for i, (a, b, z) in enumerate(KEEP):
    v = f"[0:v]trim={a+OFF:.3f}:{b+OFF:.3f},setpts=PTS-STARTPTS"
    if z != 1: v += f",scale={round(1080*z/2)*2}:{round(1920*z/2)*2}:flags=bicubic,crop=1080:1920:(iw-1080)/2:0"
    d = b - a
    fc.append(v + f",setsar=1[v{i}]")
    fc.append(f"[0:a]atrim={a+OFF:.3f}:{b+OFF:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={d-0.014:.3f}:d=0.014[a{i}]")
    labels.append(f"[v{i}][a{i}]"); starts.append(t); t += d
fc.append("".join(labels) + f"concat=n={len(KEEP)}:v=1:a=1[v][a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-crf", "15", "-preset", "fast", "-g", "30", "-r", "30", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                "videos/stroller-math/cut.mp4"], check=True)
def remap(x):
    for (a, b, _), s in zip(KEEP, starts):
        if a - 0.03 <= x <= b + 0.03: return round(s + min(max(x, a), b) - a, 2)
    return None
words = []
for w in json.load(open(sys.argv[1])):
    k = w["text"].lower().strip(".,?")
    mid = (w["start"] + w["end"]) / 2
    if k in DROP or remap(mid) is None: continue
    s, e = remap(max(w["start"], [a for a, b, _ in KEEP if a - .03 <= mid <= b + .03][0])), remap(mid)
    e2 = remap(min(w["end"], [b for a, b, _ in KEEP if a - .03 <= mid <= b + .03][0]))
    words.append({"text": FIX.get(w["text"], w["text"]), "start": s, "end": e2, "id": f"w{len(words)}"})
json.dump(words, open("videos/stroller-math/transcript.json", "w"), indent=2)
print("length", round(t, 2), "cuts at", [round(s, 2) for s in starts])
print(" | ".join(f"{w['start']:.2f} {w['text']}" for w in words))
