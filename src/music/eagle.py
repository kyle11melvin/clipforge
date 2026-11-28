# Bed for graphics/eagle-chicken: a tight, airless build under the chicken (A pedal with a Bb rubbing against it, a
# dry tick on every thought), a held breath, then D major opens up when the eagle arrives: wide pad, low D, a bell on
# every thought climbing through D - Bm7 - G - A - D, all in a long hall. numpy only.
#   python3 -I src/music/eagle.py <out.wav>
# Timings mirror graphics/eagle-chicken/comp.html; change them in both places.
import sys, wave, numpy as np
SR = 44100
T_CHICKEN, C_START = 2.2, 2.9
C_DUR = [.45, .4, .36, .33, .3, .28, .26, .26, .25, .26, .25, .25, .7, .45, 1.0]
C_AT = list(C_START + np.concatenate([[0], np.cumsum(C_DUR)[:-1]]))
T_EAGLE = C_START + sum(C_DUR); E_START = T_EAGLE + 1.0; E_STEP = 0.7; NE = 9
DUR = E_START + NE * E_STEP + 1.6
TAIL = 1.2                       # audio rings a little past the last frame; ffmpeg trims to the picture
N = int((DUR + TAIL) * SR)
dry = np.zeros((N, 2)); wet = np.zeros((N, 2))      # wet goes through the hall
rng = np.random.default_rng(7)
def hz(n):
    k = {"C": -9, "D": -7, "E": -5, "F": -4, "G": -2, "A": 0, "B": 2}[n[0]] + (1 if "#" in n else 0) - (1 if "b" in n else 0)
    return 440.0 * 2 ** ((int(n[-1]) - 4) + k / 12)
def add(bus, at, sig, g=1.0, pan=0.0):
    i = int(at * SR); sig = sig[: max(0, N - i)]
    bus[i:i + len(sig), 0] += sig * g * np.cos((pan + 1) * np.pi / 4); bus[i:i + len(sig), 1] += sig * g * np.sin((pan + 1) * np.pi / 4)
def tt(d): return np.arange(int(d * SR)) / SR
def lowpass(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); return np.fft.irfft(X / (1 + (f / fc) ** 4), len(x))
def saw(f, t, det=0.0, harm=10):
    return sum(np.sin(2 * np.pi * f * (1 + det) * h * t) / h for h in range(1, harm + 1))

# ---- hook: one low A and a soft question mark of a note
t = tt(T_CHICKEN + 0.3)
add(dry, 0, np.sin(2 * np.pi * hz("A1") * t) * np.minimum(1, t / 0.6), 0.20)
t = tt(2.0); add(wet, 0.15, np.sin(2 * np.pi * hz("E4") * t) * np.exp(-t * 2.2) * (1 - np.exp(-t * 300)), 0.10, -0.2)
t = tt(1.6); add(wet, 1.05, np.sin(2 * np.pi * hz("F4") * t) * np.exp(-t * 2.5) * (1 - np.exp(-t * 300)), 0.09, 0.2)

# ---- chicken: pedal A with Bb grinding on it, getting louder and brighter; dry, almost no room
cd = T_EAGLE - T_CHICKEN; t = tt(cd); ramp = (t / cd) ** 1.6
trem = 0.6 + 0.4 * np.sin(2 * np.pi * (5 + 6 * t / cd) * t)            # tremolo speeds up
strings = sum(saw(hz(n), t, d, 8) for n in ("A2", "E3", "Bb3") for d in (-0.004, 0.004)) / 6
strings = lowpass(strings, 700) + ramp * (strings - lowpass(strings, 700)) * 0.5
add(dry, T_CHICKEN, strings * trem * (0.15 + 0.85 * ramp) * np.minimum(1, (cd - t) / 0.03), 0.30)
add(dry, T_CHICKEN, np.sin(2 * np.pi * hz("A1") * t) * (0.4 + 0.6 * ramp), 0.22)
riser = saw(hz("A4") * 2 ** (t / cd * 7 / 12), t, 0, 5) * ramp ** 2          # creeps up a fifth
add(dry, T_CHICKEN, lowpass(riser, 2500) * np.minimum(1, (cd - t) / 0.03), 0.07, 0.3)
def tick(f=1900):
    t = tt(0.07); return (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.7 * t)) * np.exp(-t * 90)
def thud():
    t = tt(0.22); return np.sin(2 * np.pi * (95 * np.exp(-t * 14) + 48) * t) * np.exp(-t * 16)
for i, at in enumerate(C_AT):
    add(dry, at, tick(1700 + 60 * i), 0.20 + 0.012 * i, pan=(-0.5 if i % 2 else 0.5))
    add(dry, at, thud(), 0.30 + 0.02 * i)
# "Hard to breathe." holds for a second: everything stops dead 0.28 s before the cut
gap = int((T_EAGLE - 0.28) * SR); cut = int(T_EAGLE * SR)
fade = np.linspace(1, 0, int(0.04 * SR))[:, None]
dry[gap:gap + len(fade)] *= fade; dry[gap + len(fade):cut] = 0

# ---- eagle: D major opens
def pad(notes, dur, att=0.35, rel=1.4):
    t = tt(dur)
    x = sum(saw(hz(n), t, d, 6) for n in notes for d in (-0.003, 0, 0.003)) / (3 * len(notes))
    x = lowpass(x, 1800)
    return x * np.minimum(1, t / att) * np.clip((dur - t) / rel, 0, 1)
def bell(f, dur=3.0):
    t = tt(dur)
    return (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2.0 * t) * np.exp(-t * 3) + 0.18 * np.sin(2 * np.pi * f * 3.01 * t) * np.exp(-t * 6)) * np.exp(-t * 1.5) * (1 - np.exp(-t * 500))
def sub(f, dur):
    t = tt(dur); return np.sin(2 * np.pi * f * t) * np.minimum(1, t / 0.08) * np.clip((dur - t) / 0.6, 0, 1)
e = lambda k: E_START + k * E_STEP
chords = [(T_EAGLE, e(2), ["D3", "A3", "D4", "F#4", "E5"], "D2"),
          (e(2), e(4), ["B2", "F#3", "D4", "A4", "F#5"], "B1"),
          (e(4), e(6), ["G2", "D3", "B3", "D4", "A4", "G5"], "G1"),
          (e(6), e(8), ["A2", "E3", "A3", "D4", "E4", "A5"], "A1"),
          (e(8), DUR + TAIL, ["D3", "A3", "D4", "F#4", "A4", "E5", "F#5"], "D2")]
for ci, (a, b, notes, bass) in enumerate(chords):
    d = b - a + 0.7
    add(wet, a, pad(notes, d, att=0.28 if ci == 0 else 0.45), 0.34 + 0.03 * ci)
    add(dry, a, pad(notes[:3], d, att=0.2), 0.10)
    add(dry, a, sub(hz(bass), b - a + 0.25), 0.34)
# the arrival: a soft low boom and a breath of air that opens upward
t = tt(1.6); add(dry, T_EAGLE, np.sin(2 * np.pi * (60 * np.exp(-t * 6) + 36.7) * t) * np.exp(-t * 2.6), 0.55)
t = tt(3.5); air = rng.standard_normal(len(t)); air = air - lowpass(air, 3500)
add(wet, T_EAGLE, air * np.minimum(1, t / 0.5) * np.exp(-t * 1.3), 0.035, -0.3)
add(wet, T_EAGLE, air[::-1] * np.minimum(1, t / 0.5) * np.exp(-t * 1.3), 0.035, 0.3)
# a bell on every thought, climbing
mel = ["F#5", "A5", "D6", "B5", "D6", "B5", "C#6", "E6", "F#6"]
for k, n in enumerate(mel):
    add(wet, e(k), bell(hz(n)), 0.16 + 0.008 * k, pan=(-0.35 if k % 2 else 0.35))
    add(wet, e(k), bell(hz(n) / 2, 2.0), 0.06)
for n, dt in (("D5", 0.0), ("A5", 0.12), ("D6", 0.24), ("A6", 0.36)):   # last thought gets a small flourish
    add(wet, e(8) + dt, bell(hz(n)), 0.07, 0.0)

# ---- hall: wet bus convolved with 3 s of decaying noise
L = int(3.0 * SR); t = np.arange(L) / SR
out = dry.copy()
for c in (0, 1):
    ir = rng.standard_normal(L) * np.exp(-t * 2.3); ir = lowpass(ir, 5000); ir[: int(0.012 * SR)] = 0; ir /= np.sqrt((ir ** 2).sum())
    n = N + L; rev = np.fft.irfft(np.fft.rfft(wet[:, c], n) * np.fft.rfft(ir, n), n)[:N]
    out[:, c] += wet[:, c] * 0.75 + rev * 0.55
t = np.arange(N) / SR
out *= np.clip((DUR + TAIL - t) / 2.4, 0, 1)[:, None]
out = np.tanh(out * 1.3) / np.tanh(1.3); out = out / np.abs(out).max() * 0.89
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())
print("wrote", sys.argv[1], f"picture {DUR:.2f}s, eagle at {T_EAGLE:.2f}s")
