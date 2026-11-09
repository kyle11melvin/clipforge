"""Sound bed for the Broncos "16 straight" reel (2026-11-08): numpy + scipy, no samples, nothing licensed.
Different lane from heartbeat.py (Kyle asked for different music): a stadium-organ hook, then a tense low pulse
under the announcers' call (mixed in by ffmpeg, not here), a big hit + crowd roar on the then/now card, a warm
brass-ish chord and a calm pulse under the payoff. Timeline matches graphics/broncos-pick/comp.html.
Usage: python3 pick-bed.py out.wav
"""
import sys, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
SR = 44100; DUR = 10.0; N = int(SR * DUR); A, B, C, D = 0.0, 1.4, 5.7, 7.3
mix = np.zeros(N); rng = np.random.default_rng(11)
def lp(x, f, o=2): return sosfilt(butter(o, min(f, 20000), "low", fs=SR, output="sos"), x)
def hp(x, f, o=2): return sosfilt(butter(o, max(f, 20), "high", fs=SR, output="sos"), x)
def bpf(x, lo, hi): return sosfilt(butter(2, [lo, hi], "band", fs=SR, output="sos"), x)
def add(at, sig, g=1.0):
    i = int(at * SR); j = min(N, i + len(sig))
    if j > i: mix[i:j] += sig[: j - i] * g
def T(d): return np.arange(int(SR * d)) / SR
def env(t, a, r, d):
    return np.minimum(1, t / max(a, 1e-4)) * np.minimum(1, np.maximum(0, (d - t) / max(r, 1e-4)))
def thump(dur=0.2, f0=95, f1=42, g=1.0):
    t = T(dur); f = f1 + (f0 - f1) * np.exp(-t * 22); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14) * g
def organ(freqs, dur, g=0.12, a=0.02, r=0.08, cutoff=3000):
    """Ballpark organ: square-ish stack with a little vibrato."""
    t = T(dur); vib = 1 + 0.004 * np.sin(2 * np.pi * 5.5 * t)
    s = sum(np.sign(np.sin(2 * np.pi * f * vib * t)) * 0.5 + np.sin(2 * np.pi * 2 * f * t) * 0.3 + np.sin(2 * np.pi * 3 * f * t) * 0.15 for f in freqs)
    return lp(s, cutoff) * env(t, a, r, dur) * g / len(freqs)
def brass(freqs, dur, g=0.15, a=0.06, r=0.6):
    t = T(dur); s = sum(sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, 9)) for f in freqs)
    cut = lp(s, 900) * (1 - np.exp(-t * 6)) + lp(s, 2500) * np.exp(-t * 6)
    return cut * env(t, a, r, dur) * g / len(freqs)
def beep(dur=0.07, f=1100, g=0.2):
    t = T(dur); return np.sin(2 * np.pi * f * t) * env(t, 0.004, 0.01, dur) * g
def impact(g=0.9):
    t = T(1.4); boom = np.sin(2 * np.pi * np.cumsum(34 + 90 * np.exp(-t * 18)) / SR) * np.exp(-t * 3.2)
    crack = lp(rng.normal(0, 1, len(t)), 4000) * np.exp(-t * 28) * 0.6
    return (boom + crack) * g
def roar(dur, a=0.6, r=1.0, g=0.06):
    t = T(dur); n = bpf(rng.normal(0, 1, len(t)), 250, 3200)
    flutter = 1 + 0.25 * lp(rng.normal(0, 1, len(t)), 6) * 3
    return n * flutter * env(t, a, r, dur) * g
def crowd_hush(dur, g=0.025): return lp(rng.normal(0, 1, int(SR * dur)), 500) * g

# A: the hook. Crowd hush + the stadium organ "charge" (G-C-E-G-C, the ballpark call), a snare-less lead into the cut.
add(A, crowd_hush(B - A + 0.3) * np.minimum(1, T(B - A + 0.3) / 0.3))
G3, C4, E4, G4, C5 = 196.0, 261.63, 329.63, 392.0, 523.25
for k, (f, dur) in enumerate([(G3, .14), (C4, .14), (E4, .14), (G4, .22), (E4, .14), (G4, .5)]):
    at = A + 0.1 + sum(d for _, d in [(G3, .14), (C4, .14), (E4, .14), (G4, .22), (E4, .14)][:k])
    add(at, organ([f, f * 2], dur, g=0.16))
add(B - 0.02, thump(dur=0.5, f0=120, f1=40, g=0.9))                                   # the cut lands

# B: the 3rd quarter. A low drone rising, a heartbeat accelerating 96 -> 172 BPM with a monitor beep, all under the call.
L = C - B; tt = T(L)
drone = np.sin(2 * np.pi * (46 + 26 * (tt / L) ** 2) * tt) + 0.5 * np.sin(2 * np.pi * (92 + 52 * (tt / L) ** 2) * tt)
add(B, lp(drone, 380) * (0.07 + 0.16 * (tt / L) ** 2))
t = B; k = 0
while t < C - 0.15:
    p = (t - B) / L; bpm = 96 + (172 - 96) * (1 - (1 - p) ** 3); g = 0.45 + 0.4 * p
    add(t, thump(g=g)); add(t + 0.16 * (60 / bpm) ** 0.5, thump(f0=80, f1=38, g=g * 0.7))
    if p > 0.5: add(t, beep(g=0.06 + 0.16 * p))
    t += 60 / bpm; k += 1
add(C - 0.7, hp(rng.normal(0, 1, int(SR * 0.7)), 1500) * np.linspace(0, 0.12, int(SR * 0.7)) ** 2)   # riser into the hit

# C: then / now. The hit, the crowd, a brass-ish C major stab.
add(C, impact()); add(C, roar(D - C + 1.6, a=0.25, r=1.4, g=0.07))
add(C + 0.05, brass([130.81, 196.0, 261.63, 329.63], 1.7, g=0.16, a=0.03, r=0.5))

# D: payoff. A warm F major -> C major swell with a calm 64 BPM pulse, crowd fading, soft out.
add(D, brass([174.61, 220.0, 261.63, 349.23], 1.4, g=0.11, a=0.3, r=0.4))
add(D + 1.3, brass([130.81, 164.81, 196.0, 261.63, 329.63], DUR - D - 1.3, g=0.12, a=0.4, r=1.2))
t = D + 0.2
while t < DUR - 0.4: add(t, thump(g=0.3)); add(t + 0.2, thump(f0=80, f1=38, g=0.22)); t += 60 / 64
mix = np.tanh(mix * 1.4) * 0.85
mix[-int(SR * 0.3):] *= np.linspace(1, 0, int(SR * 0.3))
wavfile.write(sys.argv[1], SR, (mix * 32767).astype(np.int16)); print("wrote", sys.argv[1], f"{DUR}s, {k} heartbeats")
