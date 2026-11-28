#!/usr/bin/env python3
"""VA county loan limit 2027 (2026-11-28): the cut. Same tool as graphics/stroller-math/tight-cut.py.

  python3 -I graphics/va-limit/tight-cut.py <parakeet transcript of videos/va-limit/full.mp4>

One 54 s walking take, ad-libbed around the script. KEEP is Parakeet word edges in full.mp4. He is on screen for five
unbroken takes (FACE); every edit point sits under a glass cutaway in overlay.html, so no cut shows on his face.
Writes videos/va-limit/cut.mp4, transcript.json (word times on the new timeline, ums dropped) and prints them."""
import json, subprocess, sys
OFF = 0.0
# (from, to, zoom)
KEEP = [(3.90, 7.04, 1),                                   # FACE A   just released this week, the VA County loan limit
        (7.20, 7.62, 1), (7.86, 9.28, 1),                  # cutaway  went up / for 2027
        (9.74, 12.88, 1.08),                               # FACE B   here's the new numbers for Orange County and San Diego
        (13.04, 14.40, 1), (14.64, 17.12, 1),              # cutaway  Orange County is now at / $1,283,000
        (18.16, 23.52, 1), (23.84, 26.48, 1),              # cutaway  that's almost up $34,000. San Diego County 1.143 / that's up $39,000
        (26.48, 30.64, 1),                                 # FACE C   But here's the thing most veterans don't know, and I just had a conversation with one this week
        (31.44, 35.04, 1), (35.44, 35.92, 1), (36.72, 38.72, 1),   # cutaway  if you have your full entitlement, the county loan limit actually doesn't matter / you can / zero percent down for whatever you qualify on
        (39.12, 45.76, 1.08),                              # FACE D   the limit only matters if you have a VA loan out there and you kept your first one, say as a rental
        (46.56, 48.24, 1), (48.72, 51.04, 1),              # cutaway  that's an extra $34,000 / more house you can buy down with nothing
        (51.44, 54.12, 1)]                                 # FACE E   Veterans, did you know you can use your loan twice?
GAMMA = {}
DROP = {"um", "uh"}
FIX = {}   # "I expect it return" is "to return"
src = "videos/va-limit/full.mp4"
fc, labels, t = [], [], 0.0
starts = []
FPS = 30
# Every edge sits on a source frame, so picture and sound segments are the same length and the times printed below
# are the real times in cut.mp4 (unsnapped, the concat drifted 0.07 s by the end).
KEEP = [(round((a + OFF) * FPS) / FPS - OFF, round((b + OFF) * FPS) / FPS - OFF, z) for a, b, z in KEEP]
SLOW = -1                       # round six: no slowed smile, it ends on his last word
HOLD = 0.5                      # then its last sharp frame is held (after 44.8 s he is lowering the phone and it blurs)
for i, (a, b, z) in enumerate(KEEP):
    v = f"[0:v]trim={a+OFF:.4f}:{b+OFF:.4f},setpts={'2*' if i == SLOW else ''}(PTS-STARTPTS)"
    if z != 1: v += f",scale={round(1080*z/2)*2}:{round(1920*z/2)*2}:flags=bicubic,crop=1080:1920:(iw-1080)/2:0"
    if i in GAMMA: v += f",eq=gamma={GAMMA[i]}"
    d = (b - a) * 2 + HOLD if i == SLOW else b - a
    fc.append(v + (f",minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,tpad=stop_mode=clone:stop_duration={HOLD}" if i == SLOW else "") + f",fps=30,setsar=1[v{i}]")
    fo = 0.06 if i == len(KEEP) - 1 else 0.022      # soft tail on his last word, slow fade at the very end
    fc.append(f"[0:a]atrim={a+OFF:.4f}:{b+OFF:.4f},asetpts=PTS-STARTPTS" + (f",atempo=0.5,apad=pad_dur={HOLD}" if i == SLOW else "") + f",afade=t=in:d=0.02,afade=t=out:st={d-fo:.3f}:d={fo}[a{i}]")
    labels.append(f"[v{i}][a{i}]"); starts.append(t); t += d
fc.append("".join(labels) + f"concat=n={len(KEEP)}:v=1:a=1[v][a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-crf", "15", "-preset", "fast", "-g", "30", "-r", "30", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                "videos/va-limit/cut.mp4"], check=True)
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
json.dump(words, open("videos/va-limit/transcript.json", "w"), indent=2)
print("length", round(t, 2), "cuts at", [round(s, 2) for s in starts])
print(" | ".join(f"{w['start']:.2f} {w['text']}" for w in words))
