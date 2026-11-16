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
SR = 44100; DUR = 21.2; N = int(SR * DUR)
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

O = 5.0; O2 = 5.8                                        # offsets since the two real game clips went in at the top
for at in (1.55, 2.95, 5.3, 7.35): add(at, thump(dur=0.2, f0=90, f1=45, g=0.35))   # the cuts to him watching
add(4.48, whoosh())                                      # whip to last week (both recaps carry their own broadcast audio)
add(3.9 + O, crowd(3.7, 0.022, a=0.6, r=0.4))            # bye week: quiet room, TV in the background
add(6.2 + O, chime(987.77, g=0.07)); add(6.34 + O, chime(1318.5, g=0.07))   # under her line
for k, at in enumerate((7.5, 7.75, 8.0)): add(at + O, thump(dur=0.25, f0=120, f1=50, g=0.6 + 0.15 * k))   # the punch-ins
add(8.25 + O, thump(dur=0.7, f0=70, f1=30, g=1.0))       # the recliner goes over
add(8.25 + O, lp(noise(0.5), 1800) * np.exp(-T(0.5) * 9) * 0.5)
add(8.33 + O, hp(noise(0.45), 3500) * np.exp(-T(0.45) * 11) * 0.22)   # coffee
tt = T(2.0); add(8.45 + O, lp(np.sin(2 * np.pi * (70 - 25 * tt / 2.0) * tt), 250) * 0.16 * np.sin(np.pi * tt / 2.0))   # slow motion: a falling low tone
add(8.45 + O, lp(noise(2.0), 500) * np.sin(np.pi * T(2.0) / 2.0) ** 2 * 0.05)
for i in range(12): add(9.75 + O2 + i * 0.45 / 12, hp(noise(0.02), 3000) * np.exp(-T(0.02) * 200) * 0.12)   # typed card
add(10.6 + O2, crowd(DUR - 10.6 - O2, 0.018, a=1.2, r=2.5))   # the ending: almost nothing

mix = np.tanh(mix * 1.4) * 0.85
wavfile.write(sys.argv[1], SR, (mix * 32767).astype(np.int16))
print("wrote", sys.argv[1], f"{DUR}s")
