"""Sound for the bye-week baby reel (2026-11-16): effects only, no music (Kyle: "you're not gonna do music ... very
soft"). numpy + scipy, no samples. Matches graphics/bye-week-baby/comp.html: 0 and 2.0 the two nail-biters (a low hit,
a tense rumble, a short crowd swell), 2.0 a whip, 4.0 calm room with a faint TV crowd, 6.2 a soft two-note chime for
her line, 7.5 the fright (three quick hits, then a crash and a splash at 8.25), 9.6 soft typed ticks on black, 10.6 on:
almost nothing, a faint warm crowd murmur from the TV fading out.
Usage: python3 byeweek_flex.py out.wav
"""
import sys, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
SR = 44100; DUR = 22.4; N = int(SR * DUR)
mix = np.zeros(N); rng = np.random.default_rng(11)
def lp(x, f, o=2): return sosfilt(butter(o, min(f, 20000), "low", fs=SR, output="sos"), x)
def hp(x, f, o=2): return sosfilt(butter(o, max(f, 20), "high", fs=SR, output="sos"), x)
def add(at, sig, g=1.0):
    i = int(at * SR); j = min(N, i + len(sig))
    if j > i: mix[i:j] += sig[: j - i] * g
def T(dur): return np.arange(int(SR * dur)) / SR
def noise(dur): return rng.normal(0, 1, int(SR * dur))
def thump(dur=0.4, f0=85, f1=38, g=1.0):
    t = T(dur); f = f1 + (f0 - f1) * np.exp(-t * 22); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 10) * g
def crowd(dur, g, a=0.3, r=0.5):
    t = T(dur); e = np.minimum(1, t / a) * np.minimum(1, np.maximum(0, (dur - t) / r))
    return lp(hp(noise(dur), 350), 2600) * e * g
def whoosh(dur=0.35, g=0.2):
    t = T(dur); return hp(lp(noise(dur), 5000), 700) * np.sin(np.pi * t / dur) ** 2 * g
def chime(f, dur=0.7, g=0.12):
    t = T(dur); return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 8)) * np.exp(-t * 5) * np.minimum(1, t / 0.004) * g

# Round 22 order: opener 0-1.5, game one 1.5 (breather at 8.0), game two 9.4 (breather at 13.7), the calm 15.1,
# her line 17.1, black 18.5, the ending 19.3. The two real calls are mixed in by ffmpeg.
def swoosh(dur=0.9, g=0.035):                              # soft air, no attack: the sound of each dissolve
    t = T(dur); return lp(hp(noise(dur), 500), 2600) * np.sin(np.pi * t / dur) ** 2 * g
def exhale(dur=1.1, g=0.045):                              # him breathing out after a win
    t = T(dur); return lp(hp(noise(dur), 350), 1500) * np.minimum(1, t / 0.15) * np.exp(-t * 2.6) * g
add(0.0, crowd(17.0, 0.006, a=1.0, r=1.2))                # a quiet room under the story; it fades out before the ending
for at in (1.0, 6.5, 11.7, 16.3): add(at, swoosh())
add(14.5, swoosh(dur=0.4, g=0.09))                        # her note flying in from the other room
for at in (5.7, 10.7): add(at, exhale())
add(11.9, crowd(4.8, 0.007, a=0.8, r=0.8))                # the calm: TV murmuring in the background
# The ending (round 33, Kyle: "a happy and bright noise, not just a static ... some piano ... uplifting and calming,
# he's holding his baby girl for the first time"). An original soft piano phrase in C major, synthesised (no samples):
# it starts under "Next Sunday…" and opens up on the picture of the two of them.
def piano(f, dur=2.6, g=0.2):
    t = T(dur); s = np.zeros(len(t))
    for k in range(1, 8):
        fk = f * k * (1 + 0.0004 * k * k)                      # a touch of string inharmonicity
        s += np.sin(2 * np.pi * fk * t) * np.exp(-t * (1.1 + 0.55 * k)) / k ** 1.25
    return lp(s, 4200) * np.minimum(1, t / 0.006) * g
NOTE = {"C3": 130.81, "G3": 196.0, "B2": 123.47, "A2": 110.0, "F2": 87.31, "C4": 261.63, "D4": 293.66, "E4": 329.63, "G4": 392.0, "A4": 440.0,
     "C5": 523.25, "D5": 587.33, "E5": 659.25, "G5": 783.99, "F3": 174.61, "E3": 164.81, "A3": 220.0, "D3": 146.83, "B3": 246.94}
t0, bar = 16.5, 1.15
bars = [("C3", "G3", "E4", "E5", "G5"), ("B2", "G3", "D4", "D5", "G5"), ("A2", "E3", "C4", "C5", "E5"), ("F2", "C3", "A3", "A4", "C5")]
for i, (bass, mid, top, m1, m2) in enumerate(bars):
    at = t0 + i * bar; vol = (0.42, 0.62, 0.82, 1.0)[i]         # round 34: a clearer swell, quiet under the black card up to full on the two of them
    add(at, piano(NOTE[bass], 3.0, 0.20 * vol)); add(at + bar * 0.25, piano(NOTE[mid], 2.4, 0.13 * vol))
    add(at + bar * 0.5, piano(NOTE[top], 2.4, 0.13 * vol)); add(at + bar * 0.75, piano(NOTE[mid], 2.0, 0.10 * vol))
    add(at, piano(NOTE[m1], 2.6, 0.17 * vol)); add(at + bar * 0.5, piano(NOTE[m2], 2.6, 0.15 * vol))
end = t0 + 4 * bar                                              # the last chord rings out
for n, g in (("C3", 0.22), ("G3", 0.14), ("C4", 0.14), ("E4", 0.14), ("G4", 0.13), ("C5", 0.16), ("E5", 0.14)): add(end, piano(NOTE[n], 3.4, g * 1.12))
# a little room on the piano: two soft echoes of everything from the ending on
i0 = int(16.4 * SR); tail = mix[i0:].copy()
for d, g in ((0.11, 0.22), (0.27, 0.14)):
    k = int(d * SR); mix[i0 + k:] += lp(tail[: len(tail) - k], 2600) * g

mix = np.tanh(mix * 1.4) * 0.85
wavfile.write(sys.argv[1], SR, (mix * 32767).astype(np.int16))
print("wrote", sys.argv[1], f"{DUR}s")
