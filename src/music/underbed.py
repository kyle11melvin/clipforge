# A quiet music bed to sit UNDER a talking head (rate-buydown reel, 2026-11-11). Everything is synthesised, so the
# audio is Kyle's own ("Original audio" on Instagram). Soft electric-piano chords, a round sub, a felt kick and a
# brushed hat, all low-passed so nothing fights his voice; ffmpeg ducks it further under the speech.
#   python3 -I src/music/underbed.py <out.wav> --intro 2.35 --beat 0.77 --bars 10
# --intro: seconds of pad-only opening (the silent hook slide); the groove's first downbeat lands right after it.
# --beat:  seconds per beat (0.77 = 78 BPM; ten 4-beat bars = 30.8 s, the length of the footage).
import sys, numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

SR = 48000
a = sys.argv[1:]; out = a[0]
def opt(k, d): return float(a[a.index(k) + 1]) if k in a else d
INTRO, B, BARS = opt("--intro", 2.35), opt("--beat", 0.77), int(opt("--bars", 10))
DUR = INTRO + BARS * 4 * B; N = int(DUR * SR)
rng = np.random.default_rng(11)
L = np.zeros(N); R = np.zeros(N)

def tt(n): return np.arange(n) / SR
def lp(x, f, o=2): return sosfilt(butter(o, f, "low", fs=SR, output="sos"), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, "high", fs=SR, output="sos"), x)
def hz(name):
    semis = {"C": -9, "D": -7, "E": -5, "F": -4, "G": -2, "A": 0, "B": 2}
    return 440.0 * 2 ** ((int(name[-1]) - 4) + (semis[name[0]] + (1 if "#" in name else 0)) / 12)
def add(at, sig, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N: return
    sig = sig[: N - i]; l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
    L[i:i + len(sig)] += sig * gain * l; R[i:i + len(sig)] += sig * gain * r

def epiano(f, dur):                       # sine + soft bell partial, slow tremolo
    n = int(dur * SR); t = tt(n)
    x = np.sin(2 * np.pi * f * t) + 0.32 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 5) + 0.10 * np.sin(2 * np.pi * 4.01 * f * t) * np.exp(-t * 14)
    env = np.minimum(1, t / 0.012) * np.exp(-t * 1.5) * np.minimum(1, (dur - t) / 0.08).clip(0, 1)
    return x * env * (1 + 0.08 * np.sin(2 * np.pi * 4.2 * t))
def pad(freqs, dur):
    n = int(dur * SR); t = tt(n); x = np.zeros(n)
    for f in freqs:
        for d in (-0.35, 0.35): x += np.sin(2 * np.pi * (f + d) * t + rng.uniform(0, 6.28))
    env = np.minimum(1, t / (dur * 0.45)) * np.minimum(1, (dur - t) / (dur * 0.35)).clip(0, 1)
    return lp(x, 900) * env / len(freqs)
def sub(f, dur):
    n = int(dur * SR); t = tt(n)
    return np.sin(2 * np.pi * f * t) * np.minimum(1, t / 0.02) * np.exp(-t * 1.1) * np.minimum(1, (dur - t) / 0.06).clip(0, 1)
def kick():
    n = int(0.35 * SR); t = tt(n); f = 46 + 70 * np.exp(-t * 30)
    return lp(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9), 220)
def hat():
    n = int(0.09 * SR); t = tt(n)
    return lp(hp(rng.normal(0, 1, n), 5000, 4), 9000) * np.exp(-t * 55)
def rim():
    n = int(0.12 * SR); t = tt(n)
    return (np.sin(2 * np.pi * 820 * t) * np.exp(-t * 60) + 0.4 * hp(rng.normal(0, 1, n), 2500) * np.exp(-t * 90))

# Fmaj7 – Em7 – Dm7 – Cmaj7, a calm descending loop; last two bars Fmaj7 → Cmaj9 so it ends resolved.
PROG = [(["F3", "A3", "C4", "E4"], "F2"), (["E3", "G3", "B3", "D4"], "E2"), (["D3", "F3", "A3", "C4"], "D2"), (["C3", "E3", "G3", "B3"], "C2")]
END = [(["F3", "A3", "C4", "E4"], "F2"), (["C3", "G3", "B3", "D4", "E4"], "C2")]
bars = [PROG[i % 4] for i in range(BARS - 2)] + END

# intro: one pad swell on the first chord, into the downbeat
add(0, pad([hz(x) for x in bars[0][0]], INTRO + B), 0.5)
for b, (ch, root) in enumerate(bars):
    t0 = INTRO + b * 4 * B; last = b == BARS - 1
    # chord: struck on beat 1, a lighter re-strike on the "and" of 2 (not in the last bar, which rings out)
    for k, nme in enumerate(ch):
        add(t0 + 0.012 * k, epiano(hz(nme), 4 * B if last else 2.4 * B), 0.20, pan=(k - 1.5) * 0.25)
        if not last: add(t0 + 2.5 * B + 0.012 * k, epiano(hz(nme), 1.5 * B), 0.11, pan=(1.5 - k) * 0.25)
    add(t0, sub(hz(root), 3.2 * B if not last else 4 * B), 0.42)
    if not last: add(t0 + 2.5 * B, sub(hz(root), 1.2 * B), 0.25)
    add(t0, pad([hz(x) for x in ch[1:]], 4 * B), 0.16)
    if last: continue
    for beat in (0, 2): add(t0 + beat * B, kick(), 0.5)
    add(t0 + 2.75 * B, kick(), 0.28)
    for beat in (1, 3): add(t0 + beat * B, rim(), 0.10, pan=0.2)
    for e in range(8): add(t0 + e * B / 2 + (0.02 if e % 2 else 0), hat(), 0.05 if e % 2 else 0.03, pan=-0.3)

x = np.stack([L, R], 1)
x = np.stack([lp(x[:, 0], 6500), lp(x[:, 1], 6500)], 1)
x = np.tanh(x * 1.2) / np.tanh(1.2)
x *= 0.85 / (np.abs(x).max() + 1e-9)
f = int(0.05 * SR); x[:f] *= np.linspace(0, 1, f)[:, None]
g = int(0.45 * SR); x[-g:] *= (np.linspace(1, 0, g) ** 1.5)[:, None]        # quick fade: the reel cuts on his last word
wavfile.write(out, SR, (x * 32767).astype(np.int16)); print("wrote", out, round(DUR, 2), "s")
