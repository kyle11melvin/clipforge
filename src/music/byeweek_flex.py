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
SR = 44100; DUR = 23.6; N = int(SR * DUR)
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
def swoosh(dur=0.9, g=0.05):                              # soft air, no attack: the sound of each dissolve
    t = T(dur); return lp(hp(noise(dur), 500), 2600) * np.sin(np.pi * t / dur) ** 2 * g
def exhale(dur=1.1, g=0.06):                              # him breathing out after a win
    t = T(dur); return lp(hp(noise(dur), 350), 1500) * np.minimum(1, t / 0.15) * np.exp(-t * 2.6) * g
add(0.0, crowd(DUR, 0.013, a=1.0, r=2.5))                 # one quiet room under everything
for at in (1.2, 9.1, 14.8, 18.2, 19.1): add(at, swoosh())
for at in (7.5, 13.3): add(at, exhale())
add(15.0, crowd(3.4, 0.016, a=0.8, r=0.8))                # the calm: TV murmuring in the background
add(19.3, crowd(DUR - 19.3, 0.015, a=1.5, r=2.5))         # the ending

mix = np.tanh(mix * 1.4) * 0.85
wavfile.write(sys.argv[1], SR, (mix * 32767).astype(np.int16))
print("wrote", sys.argv[1], f"{DUR}s")
