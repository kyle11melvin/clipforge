"""Sound design for the Broncos 4th-quarter reel (2026-11-02): numpy + scipy, no samples, nothing licensed.
Timeline (matches graphics/broncos-4q/comp.html): 0-3 s both of them (warm pad, a crowd-ish hush), 3-10.5 s
the 4th quarter (ticking clock, a low drone rising, stadium toms building, a lub-dub that accelerates 72 ->
178 BPM with a monitor beep once it races, a final buzzer at 0:01), 10.5-11.9 black card (silence, one low
hit), 11.9-16 relief (major chord swell, crowd-roar noise swell, a calm 60 BPM pulse).
Usage: python3 heartbeat.py out.wav
"""
import sys, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
SR = 44100; DUR = 16.0; N = int(SR * DUR)
mix = np.zeros(N); rng = np.random.default_rng(7)
def lp(x, f, o=2): return sosfilt(butter(o, min(f, 20000), "low", fs=SR, output="sos"), x)
def hp(x, f, o=2): return sosfilt(butter(o, max(f, 20), "high", fs=SR, output="sos"), x)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], "band", fs=SR, output="sos"), x)
def add(at, sig, g=1.0):
    i = int(at * SR); j = min(N, i + len(sig))
    if j > i: mix[i:j] += sig[: j - i] * g
def T(dur): return np.arange(int(SR * dur)) / SR
def thump(dur=0.18, f0=95, f1=42, g=1.0):
    t = T(dur); f = f1 + (f0 - f1) * np.exp(-t * 22); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 14) * g
def tom(dur=0.5, f0=190, f1=70, g=1.0):
    t = T(dur); f = f1 + (f0 - f1) * np.exp(-t * 9); ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * 6); skin = lp(rng.normal(0, 1, len(t)), 2500) * np.exp(-t * 40) * 0.5
    return (body + skin) * g
def beep(dur=0.07, f=1100, g=0.25):
    t = T(dur); e = np.minimum(1, t / 0.004) * np.minimum(1, (dur - t) / 0.01)
    return np.sin(2 * np.pi * f * t) * e * g
def tick(g=0.3):
    t = T(0.03); return hp(rng.normal(0, 1, len(t)), 3000) * np.exp(-t * 180) * g
def chord(freqs, dur, g=0.12, a=1.2, cutoff=1400):
    t = T(dur)
    s = sum(np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t) + 0.15 * np.sin(2 * np.pi * 3 * f * t) for f in freqs)
    e = np.minimum(1, t / a) * np.minimum(1, np.maximum(0, (dur - t) / 1.5))
    return lp(s, cutoff) * e * g / len(freqs)
def buzzer(dur=0.9, g=0.35):
    t = T(dur); s = np.sign(np.sin(2 * np.pi * 220 * t)) * 0.6 + np.sin(2 * np.pi * 110 * t) * 0.4
    return lp(s, 1800) * np.minimum(1, t / 0.01) * np.minimum(1, (dur - t) / 0.15) * g

# 0-3: a warm, easy pad (D major) with a soft hush of crowd noise.
add(0.0, chord([146.83, 185.0, 220.0, 293.66], 3.4, g=0.11, a=0.6, cutoff=1100))
add(0.0, lp(rng.normal(0, 1, int(SR * 3.4)), 600) * 0.03 * np.minimum(1, T(3.4) / 0.5))

# 3-10.5: the 4th quarter. Clock ticks once a second, drone rises, toms build, heartbeat accelerates.
t0, t1 = 3.0, 10.5; L = t1 - t0
tt = T(L); drone = np.sin(2 * np.pi * (49 + 30 * (tt / L) ** 2) * tt) + 0.5 * np.sin(2 * np.pi * (98 + 60 * (tt / L) ** 2) * tt)
add(t0, lp(drone, 400) * (0.08 + 0.2 * (tt / L) ** 2))
for k in range(8): add(t0 + 0.7 + k * (L - 1.2) / 7, tick(0.25 + 0.05 * k))                 # the game clock
beat = 0.5                                                                                     # toms at 120 BPM, swelling
t = t0
while t < t1 - 0.3:
    p = (t - t0) / L; n = round((t - t0) / beat)
    if n % 4 == 0: add(t, tom(g=0.25 + 0.5 * p))
    elif n % 4 == 2: add(t, tom(f0=150, f1=60, g=0.15 + 0.4 * p))
    elif p > 0.5: add(t, tom(f0=240, f1=90, dur=0.3, g=0.15 + 0.3 * p))
    t += beat
t = t0; k = 0
while t < t1 - 0.2:
    p = (t - t0) / L; bpm = 72 + (178 - 72) * (1 - (1 - p) ** 3); g = 0.55 + 0.45 * p
    add(t, thump(g=g)); add(t + 0.17 * (60 / bpm) ** 0.5, thump(f0=80, f1=38, g=g * 0.7))
    if p > 0.45: add(t, beep(g=0.08 + 0.2 * p))
    t += 60 / bpm; k += 1
add(t1 - 0.5, buzzer())                                                                        # 0:01, last play

# 10.5-11.9: black card. One low hit, then nothing.
add(10.5, thump(dur=0.6, f0=70, f1=35, g=0.6))

# 11.9-16: relief. C major swell, crowd roar (shaped noise), calm heartbeat.
add(11.9, chord([130.81, 164.81, 196.0, 261.63, 329.63], 4.2, g=0.17, a=1.0, cutoff=2000))
roar = bp(rng.normal(0, 1, int(SR * 4.1)), 300, 3000); re = np.minimum(1, T(4.1) / 1.4) * np.minimum(1, np.maximum(0, (4.1 - T(4.1)) / 1.2))
add(11.9, roar * re * 0.05)
t = 12.2
while t < 16: add(t, thump(g=0.35)); add(t + 0.2, thump(f0=80, f1=38, g=0.25)); t += 1.0
mix = np.tanh(mix * 1.5) * 0.85
wavfile.write(sys.argv[1], SR, (mix * 32767).astype(np.int16))
print("wrote", sys.argv[1], f"{DUR}s, {k} heartbeats")
