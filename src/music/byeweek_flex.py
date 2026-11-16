"""Sound design for the bye-week baby reel (2026-11-16): numpy + scipy, no samples, nothing licensed.
Timeline (matches graphics/bye-week-baby/comp.html): 0-3.7 s the lazy Sunday (soft major-seventh pad, slow
plucks), 2.0 his wife's chime, 3.7 the needle drop, 3.9-7.0 the schedule alert (broadcast sting, a swipe, a hit, a held
brass chord; no heartbeat), 7.0-10.2 the pay-off: Brahms' Lullaby (1868, public domain) on a
synthesised music box over a warm chord.
Usage: python3 byeweek_flex.py out.wav
"""
import sys, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
SR = 44100; DUR = 10.2; N = int(SR * DUR)
CUT1, CUT2 = 3.7, 7.0
mix = np.zeros(N); rng = np.random.default_rng(11)
def lp(x, f, o=2): return sosfilt(butter(o, min(f, 20000), "low", fs=SR, output="sos"), x)
def hp(x, f, o=2): return sosfilt(butter(o, max(f, 20), "high", fs=SR, output="sos"), x)
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
def chord(freqs, dur, g=0.12, a=1.2, r=1.5, cutoff=1400):
    t = T(dur)
    s = sum(np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t) + 0.15 * np.sin(2 * np.pi * 3 * f * t) for f in freqs)
    e = np.minimum(1, t / a) * np.minimum(1, np.maximum(0, (dur - t) / r))
    return lp(s, cutoff) * e * g / len(freqs)
def pluck(f, dur=0.9, g=0.2):
    t = T(dur); s = np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 6)
    return s * np.exp(-t * 4.5) * np.minimum(1, t / 0.005) * g
def box(f, dur=1.4, g=0.22):
    """Music-box tine: fundamental plus two slightly inharmonic partials that die fast."""
    t = T(dur)
    s = np.sin(2 * np.pi * f * t) * np.exp(-t * 3.2) + 0.45 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 9) \
        + 0.2 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 16)
    return s * np.minimum(1, t / 0.002) * g

# 0-3.7: lazy Sunday. Dmaj7 pad, three slow plucks.
add(0.0, chord([146.83, 185.0, 220.0, 277.18], CUT1 + 0.1, g=0.16, a=0.4, r=0.15, cutoff=1200))
for at, f in [(0.25, 440.0), (0.95, 554.37), (1.65, 659.25)]: add(at, pluck(f))

# 2.0: his wife speaks: a soft two-note chime.
add(2.0, pluck(987.77, 0.5, 0.18)); add(2.14, pluck(1318.5, 0.7, 0.18))

# 3.7: the needle drop. A tone and the pad's top note sliding down to nothing in 0.3 s.
t = T(0.32); f = 520 * np.exp(-t * 9) + 40; ph = 2 * np.pi * np.cumsum(f) / SR
add(CUT1 - 0.02, (np.sign(np.sin(ph)) * 0.25 + np.sin(ph) * 0.5) * np.exp(-t * 5) * 0.4)
add(CUT1, hp(rng.normal(0, 1, int(SR * 0.12)), 2500) * np.exp(-T(0.12) * 30) * 0.3)

# 3.9-7.0: the schedule alert. A two-note broadcast sting, a swipe as BYE is struck, a hit when the flex lands,
# then a low held brass chord. No heartbeat: Kyle did not want the heart-rate gag twice in a row.
def brass(f, dur, g=0.2):
    t = T(dur); s = sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, 7))
    return lp(s, 1600) * np.minimum(1, t / 0.02) * np.minimum(1, np.maximum(0, (dur - t) / 0.12)) * g
for at, f, d in [(0.2, 392.0, 0.16), (0.38, 523.25, 0.16), (0.56, 659.25, 0.34)]:
    add(CUT1 + at, brass(f, d)); add(CUT1 + at, brass(f / 2, d, 0.12))
sw = T(0.3); add(CUT1 + 0.3, hp(rng.normal(0, 1, len(sw)), 1200) * np.sin(np.pi * sw / 0.3) ** 2 * 0.22)   # the strike
add(CUT1 + 0.9, tom(g=0.9)); add(CUT1 + 0.9, thump(dur=0.5, f0=80, f1=38, g=0.8))                                # the flex lands
for f in (130.81, 196.0, 261.63, 311.13): add(CUT1 + 0.9, brass(f, CUT2 - CUT1 - 1.0, 0.07))                     # held, uneasy
add(CUT1 + 1.15, beep(dur=0.09, f=1320, g=0.2)); add(CUT1 + 1.3, beep(dur=0.09, f=1320, g=0.2))                 # FLEXED tag
k = 0

# 7.0-10.2: she's here. One soft low hit, a warm C major chord, Brahms' Lullaby on the music box.
add(CUT2, thump(dur=0.5, f0=70, f1=36, g=0.5))
add(CUT2, chord([130.81, 164.81, 196.0, 261.63], DUR - CUT2, g=0.15, a=0.5, r=1.2, cutoff=1800))
E, G, A, B, C = 659.25, 783.99, 880.0, 987.77, 1046.5
EIGHTH = 0.165
melody = [(E, 1), (E, 1), (G, 4), (E, 1), (E, 1), (G, 4), (E, 1), (G, 1), (C, 2), (B, 2), (A, 2), (A, 2), (G, 4)]
at = CUT2 + 0.12
for f, n8 in melody:
    add(at, box(f)); at += n8 * EIGHTH
fade = int(SR * 0.6); mix[-fade:] *= np.linspace(1, 0, fade)
mix = np.tanh(mix * 1.5) * 0.85
wavfile.write(sys.argv[1], SR, (mix * 32767).astype(np.int16))
print("wrote", sys.argv[1], f"{DUR}s")
