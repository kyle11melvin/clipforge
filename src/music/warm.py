# A soft, royalty-free bed for a photo reel: Rhodes-like chords over a sine pad, no drums, a small swell on the
# last beat of type. Synthesised with numpy, so the audio is Kyle's own ("Original audio").
#   python3 -I src/music/warm.py <out.wav> [--dur 10.5] [--swell 7.0]
import sys, numpy as np
import wave
SR = 44100
a = sys.argv[1:]; out = a[0]
DUR = float(a[a.index("--dur") + 1]) if "--dur" in a else 10.5
SWELL = float(a[a.index("--swell") + 1]) if "--swell" in a else 7.0
N = int(DUR * SR); L = np.zeros(N); R = np.zeros(N)
def hz(n):
    k = {"C": -9, "D": -7, "E": -5, "F": -4, "G": -2, "A": 0, "B": 2}[n[0]] + (1 if "#" in n else 0)
    return 440.0 * 2 ** ((int(n[-1]) - 4) + k / 12)
def add(at, sig, g=1.0, pan=0.0):
    i = int(at * SR); sig = sig[: max(0, N - i)]
    L[i:i + len(sig)] += sig * g * np.cos((pan + 1) * np.pi / 4); R[i:i + len(sig)] += sig * g * np.sin((pan + 1) * np.pi / 4)
def rhodes(f, dur):
    t = np.arange(int(dur * SR)) / SR
    env = np.exp(-t * 1.6) * (1 - np.exp(-t * 400))
    tine = np.sin(2 * np.pi * f * 7 * t) * np.exp(-t * 9) * 0.08
    return (np.sin(2 * np.pi * f * t + tine) + 0.25 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 3)) * env
def pad(freqs, dur):
    t = np.arange(int(dur * SR)) / SR
    x = sum(np.sin(2 * np.pi * f * t * (1 + d)) for f in freqs for d in (-0.002, 0, 0.002)) / (3 * len(freqs))
    env = np.minimum(1, t / 1.2) * np.minimum(1, np.maximum(0, (dur - t) / 1.5))
    return x * env
# Cmaj7 - Am9 - Fmaj7 - G(add9), one chord per 2.625 s (four chords across the reel), arpeggiated softly.
chords = [["C3", "E4", "G4", "B4"], ["A2", "E4", "G4", "B4"], ["F2", "A3", "C4", "E4"], ["G2", "B3", "D4", "A4"]]
step = DUR / 4
for ci, ch in enumerate(chords):
    t0 = ci * step
    add(t0, pad([hz(n) for n in ch[:3]], step + 0.6), 0.10)
    for k, n in enumerate(ch):
        add(t0 + k * 0.19, rhodes(hz(n), 2.6), 0.16 if k else 0.22, pan=(k - 1.5) * 0.25)
    add(t0 + step * 0.5, rhodes(hz(ch[-1]) * 2, 1.8), 0.07, pan=0.4)
# swell under the last line, then let everything ring out.
t = np.arange(N) / SR
sw = np.clip((t - SWELL) / 1.2, 0, 1) * np.clip((DUR - t) / 2.0, 0, 1)
add(0, np.sin(2 * np.pi * hz("C2") * t) * sw, 0.10)
x = np.stack([L, R], 1); x = np.tanh(x * 1.2) / np.tanh(1.2)
fade = np.minimum(1, np.maximum(0, (DUR - t) / 1.0))[:, None]
x = x * fade; x = x / max(1e-9, np.abs(x).max()) * 0.8
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype(np.int16).tobytes())
print("wrote", out, f"{DUR}s")
