"""Heartbeat sound design for the Broncos 4th-quarter reel (2026-11-02): no samples, numpy + scipy.
Quiet under Asher (0-3 s), a lub-dub that accelerates 72 -> 178 BPM under Kyle (3-9 s) with a rising
hum, a monitor beep per beat once it is racing, one short silence on the black card (9-10.4 s), then a
relief chord and a slow 60 BPM heartbeat under the last Asher frame. Usage: python3 heartbeat.py out.wav
"""
import sys, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
SR = 44100; DUR = 14.0; N = int(SR * DUR)
mix = np.zeros(N)
def lp(x, f): return sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)
def add(at, sig, g=1.0):
    i = int(at * SR); j = min(N, i + len(sig)); mix[i:j] += sig[: j - i] * g
def thump(dur=0.18, f0=95, f1=42, g=1.0):
    t = np.arange(int(SR * dur)) / SR
    f = f1 + (f0 - f1) * np.exp(-t * 22); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 14) * g
def beep(dur=0.07, f=1100, g=0.25):
    t = np.arange(int(SR * dur)) / SR
    e = np.minimum(1, t / 0.004) * np.minimum(1, (dur - t) / 0.01)
    return np.sin(2 * np.pi * f * t) * e * g
def chord(freqs, dur, g=0.12):
    t = np.arange(int(SR * dur)) / SR
    s = sum(np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t) for f in freqs)
    e = np.minimum(1, t / 1.2) * np.minimum(1, np.maximum(0, (dur - t) / 1.5))
    return lp(s, 1400) * e * g / len(freqs)

# 3-9 s: accelerating lub-dub. BPM follows the picture's easeOut(p) curve.
t0, t1 = 3.0, 9.0; t = t0; k = 0
while t < t1:
    p = (t - t0) / (t1 - t0); bpm = 72 + (178 - 72) * (1 - (1 - p) ** 3)
    g = 0.55 + 0.45 * p
    add(t, thump(g=g)); add(t + 0.17 * (60 / bpm) ** 0.5, thump(f0=80, f1=38, g=g * 0.7))
    if p > 0.45: add(t, beep(g=0.08 + 0.2 * p))
    t += 60 / bpm; k += 1
# rising tension hum under it
tt = np.arange(int(SR * 6)) / SR
hum = np.sin(2 * np.pi * (55 + 40 * (tt / 6) ** 2) * tt) * (tt / 6) ** 2 * 0.18
add(3.0, lp(hum, 300))
# 10.4-14: relief chord (C major, warm) and a slow calm heartbeat.
add(10.4, chord([130.81, 164.81, 196.0, 261.63], 3.6, g=0.16))
t = 10.6
while t < 14: add(t, thump(g=0.35)); add(t + 0.2, thump(f0=80, f1=38, g=0.25)); t += 1.0
mix = np.tanh(mix * 1.6) * 0.85
wavfile.write(sys.argv[1], SR, (mix * 32767).astype(np.int16))
print("wrote", sys.argv[1], f"{DUR}s, {k} beats")
