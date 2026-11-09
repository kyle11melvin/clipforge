"""Sound effects only (no music) for the v2 Broncos "16 straight" reel: Kyle adds the song in Instagram.
A white-flash hit at the smash cut (2.35 s), a tick per count (3.10 + 0.1k, k = 0..15), a slam on 16 (4.60 s),
a soft whoosh into the bye-week card (7.0 s). numpy only. Usage: python3 pick-sfx.py out.wav
"""
import sys, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
SR = 44100; DUR = 9.0; N = int(SR * DUR); mix = np.zeros(N); rng = np.random.default_rng(5)
def lp(x, f): return sosfilt(butter(2, min(f, 20000), "low", fs=SR, output="sos"), x)
def hp(x, f): return sosfilt(butter(2, max(f, 20), "high", fs=SR, output="sos"), x)
def add(at, sig, g=1.0):
    i = int(at * SR); j = min(N, i + len(sig))
    if j > i: mix[i:j] += sig[: j - i] * g
def T(d): return np.arange(int(SR * d)) / SR
def tick(g=0.5, f=2600):
    t = T(0.05); return (hp(rng.normal(0, 1, len(t)), 2000) * 0.6 + np.sin(2 * np.pi * f * t) * 0.4) * np.exp(-t * 160) * g
def hit(g=0.9, dur=1.1):
    t = T(dur); boom = np.sin(2 * np.pi * np.cumsum(36 + 110 * np.exp(-t * 20)) / SR) * np.exp(-t * 3.5)
    return (boom + lp(rng.normal(0, 1, len(t)), 3500) * np.exp(-t * 30) * 0.7) * g
def whoosh(dur=0.5, g=0.3):
    t = T(dur); n = rng.normal(0, 1, len(t)); e = np.sin(np.pi * t / dur) ** 2
    return sosfilt(butter(2, [300, 4000], "band", fs=SR, output="sos"), n) * e * g
add(2.30, hit(0.8, 0.8))                                   # the smash cut
for k in range(16): add(3.10 + 0.1 * k, tick(0.35 + 0.02 * k, 2200 + 60 * k))
add(4.60, hit(1.0, 1.3))                                   # 16 lands
add(6.75, whoosh()); add(7.0, hit(0.5, 0.7))               # into the bye week
mix = np.tanh(mix * 1.3) * 0.9
wavfile.write(sys.argv[1], SR, (mix * 32767).astype(np.int16)); print("wrote", sys.argv[1])
