# Three royalty-free music beds for the price-cuts reel, composed on its beat grid (80 BPM, one beat = 0.75 s,
# 16 beats = 12 s). Everything is synthesised here, so the audio is Kyle's own ("Original audio" on Instagram).
#   python3 -I src/music/beds.py <out folder> [--bpm 80] [--beats 16]
# Structure: bar 1 = hook (pad only, a riser into the drop), bars 2–3 = the homes (kick on every beat, "boom
# boom boom"), bar 4 = closing frame (groove thins, final hit on the downbeat, fade so the loop restarts clean).
import sys, numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

SR = 44100
args = sys.argv[1:]; out = args[0]
BPM = float(args[args.index("--bpm") + 1]) if "--bpm" in args else 80.0
BEATS = int(args[args.index("--beats") + 1]) if "--beats" in args else 16
B = 60.0 / BPM; DUR = BEATS * B; N = int(DUR * SR)
rng = np.random.default_rng(7)

def t(n): return np.arange(n) / SR
def env(n, a=0.002, d=0.2, s=0.0, r=0.05, hold=0.0):
    segs = [np.linspace(0, 1, int(a * SR), endpoint=False), np.linspace(1, s, int(d * SR), endpoint=False),
            np.full(int(hold * SR), s), np.linspace(s, 0, int(r * SR), endpoint=False)]
    x = np.concatenate(segs)
    return np.pad(x, (0, max(0, n - len(x))))[:n]
def lp(x, f, o=2): return sosfilt(butter(o, min(f, SR / 2 - 100), "low", fs=SR, output="sos"), x)
def hp(x, f, o=2): return sosfilt(butter(o, max(f, 20), "high", fs=SR, output="sos"), x)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], "band", fs=SR, output="sos"), x)
def note(name):  # "A2" -> Hz
    semis = {"C": -9, "D": -7, "E": -5, "F": -4, "G": -2, "A": 0, "B": 2}
    k = semis[name[0]] + (1 if "#" in name else 0); o = int(name[-1])
    return 440.0 * 2 ** ((o - 4) + k / 12)

class Mix:
    def __init__(self): self.L = np.zeros(N); self.R = np.zeros(N)
    def add(self, at, sig, gain=1.0, pan=0.0):
        i = int(at * SR); sig = sig[: max(0, N - i)]
        if len(sig) == 0: return
        l = np.cos((pan + 1) * np.pi / 4); r = np.sin((pan + 1) * np.pi / 4)
        self.L[i:i + len(sig)] += sig * gain * l; self.R[i:i + len(sig)] += sig * gain * r
    def render(self, path, peak=0.89):
        x = np.stack([self.L, self.R], 1)
        x = np.tanh(x * 1.1) / np.tanh(1.1)                         # soft clip
        x *= peak / (np.abs(x).max() + 1e-9)
        # 40 ms fade in, and a fade over the last beat so the loop restarts clean
        f = int(0.04 * SR); x[:f] *= np.linspace(0, 1, f)[:, None]
        g = int(B * SR); x[-g:] *= np.linspace(1, 0, g)[:, None] ** 1.5
        wavfile.write(path, SR, (x * 32767).astype(np.int16)); print("wrote", path)

# ---- instruments ---------------------------------------------------------------------------------------------
def kick(dur=0.45, f0=160, f1=48, punch=1.0):
    n = int(dur * SR); tt = t(n)
    f = f1 + (f0 - f1) * np.exp(-tt * 28); ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-tt * 7)
    click = hp(rng.normal(0, 1, n), 2000) * np.exp(-tt * 400) * 0.5 * punch
    return np.tanh((body + click) * 1.6)
def kick808(dur=1.2, f0=120, f1=42):
    n = int(dur * SR); tt = t(n)
    f = f1 + (f0 - f1) * np.exp(-tt * 18); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.tanh(np.sin(ph) * 2.2 * np.exp(-tt * 2.4)) * env(n, 0.001, 0.05, 1, 0.3, hold=dur - 0.36)
def hat(dur=0.06, open_=False):
    n = int((0.35 if open_ else dur) * SR); tt = t(n)
    x = hp(rng.normal(0, 1, n), 7000, 4) * np.exp(-tt * (9 if open_ else 70))
    return x * 0.6
def clap():
    n = int(0.25 * SR); tt = t(n); x = np.zeros(n)
    for k, d in enumerate([0, 0.011, 0.021, 0.03]):
        i = int(d * SR); m = n - i
        x[i:] += bp(rng.normal(0, 1, m), 900, 5000) * np.exp(-t(m) * (60 if k < 3 else 14))
    return x * 0.5
def snare():
    n = int(0.22 * SR); tt = t(n)
    body = np.sin(2 * np.pi * 185 * tt) * np.exp(-tt * 30) * 0.6
    noise = bp(rng.normal(0, 1, n), 1500, 9000) * np.exp(-tt * 22)
    return (body + noise) * 0.7
def saw(f, n, detune=0.0):
    tt = t(n); x = np.zeros(n)
    for d in ([-detune, 0, detune] if detune else [0]):
        ff = f * 2 ** (d / 1200); ph = (tt * ff) % 1.0
        x += 2 * ph - 1
    return x / (3 if detune else 1)
def bass(f, dur, cutoff=260, drive=1.4):
    n = int(dur * SR)
    x = lp(saw(f, n) * 0.6 + np.sin(2 * np.pi * f * t(n)) * 0.6, cutoff, 2)
    return np.tanh(x * drive) * env(n, 0.004, 0.08, 0.7, 0.08, hold=max(0, dur - 0.17))
def stab(freqs, dur, cutoff=1800):
    n = int(dur * SR); x = sum(saw(f, n, detune=9) for f in freqs) / len(freqs)
    e = env(n, 0.003, 0.18, 0.25, 0.1, hold=max(0, dur - 0.3))
    return lp(x, cutoff) * e * 0.5
def pad(freqs, dur, cutoff=1200, a=0.8):
    n = int(dur * SR); x = sum(saw(f, n, detune=14) for f in freqs) / len(freqs)
    sweep = cutoff * (0.4 + 0.6 * np.linspace(0, 1, n))                  # filter opens over the note
    y = np.zeros(n); step = 2048
    for i in range(0, n, step):
        y[i:i + step] = lp(x[max(0, i - 4096):i + step], float(sweep[i]))[-min(step, n - i):]
    return y * env(n, a, 0.3, 0.8, 0.6, hold=max(0, dur - a - 0.9)) * 0.45
def rhodes(f, dur, tine=0.35):
    n = int(dur * SR); tt = t(n)
    x = np.sin(2 * np.pi * f * tt) * np.exp(-tt * 1.6) + tine * np.sin(2 * np.pi * f * 2 * tt) * np.exp(-tt * 5) \
        + 0.12 * np.sin(2 * np.pi * f * 7.02 * tt) * np.exp(-tt * 14)
    return np.tanh(x * 1.4) * env(n, 0.003, 0.3, 0.6, 0.4, hold=max(0, dur - 0.7)) * 0.4
def riser(dur):
    n = int(dur * SR); tt = t(n)
    x = bp(rng.normal(0, 1, n), 400, 6000) * (tt / dur) ** 2.2
    return hp(x, 300 + 4000 * (tt / dur)[-1]) * 0.35
def crackle(dur):
    n = int(dur * SR); x = rng.normal(0, 1, n) * (rng.random(n) < 0.0015) * 2.5
    return lp(x, 6000) + rng.normal(0, 0.012, n)
def impact():
    n = int(1.0 * SR); tt = t(n)
    return (np.sin(2 * np.pi * 55 * tt) * np.exp(-tt * 3) + lp(rng.normal(0, 1, n), 900) * np.exp(-tt * 9) * 0.5) * 0.8

# ---- arrangement helpers -------------------------------------------------------------------------------------
# One chord per bar: Am7, Fmaj7, Cmaj7, G6. Bar 1 is the hook, 2–3 the homes, 4 the closing frame.
PROG = [["A3", "C4", "E4", "G4"], ["F3", "A3", "C4", "E4"], ["C3", "E3", "G3", "B3"], ["G3", "B3", "D4", "E4"]]
ROOTS = ["A1", "F1", "C2", "G1"]
def bar_of(beat): return min(3, beat // 4)
def chord(beat): return [note(x) for x in PROG[bar_of(beat)]]
def root(beat): return note(ROOTS[bar_of(beat)])
HOME_BEATS = range(4, 12); HOOK = range(0, 4); CLOSE = range(12, BEATS)

# ---- Option A: deep house ------------------------------------------------------------------------------------
def deep_house(path):
    m = Mix()
    for bar in range(4): m.add(bar * 4 * B, pad(chord(bar * 4), 4 * B, cutoff=900), 0.8)
    m.add(2 * B, riser(2 * B), 0.9)
    m.add(4 * B, impact(), 0.7)
    for b in range(BEATS):
        if b in HOME_BEATS or b == 12: m.add(b * B, kick(), 1.0)
        if b in HOME_BEATS or b in CLOSE:
            m.add(b * B + B / 2, hat(open_=True), 0.5 if b in HOME_BEATS else 0.25, pan=0.3)
            for q in (0.25, 0.75): m.add(b * B + q * B, hat(), 0.35, pan=-0.2)
        if b in HOME_BEATS and b % 2 == 1: m.add(b * B, clap(), 0.7)
        if b in HOME_BEATS:
            m.add(b * B, bass(root(b), B * 0.45), 0.9); m.add(b * B + B / 2, bass(root(b), B * 0.4, cutoff=200), 0.6)
            m.add(b * B + B / 2, stab(chord(b), B * 0.5), 0.55, pan=0.15)
        if b in CLOSE and b > 12: m.add(b * B + B / 2, stab(chord(b), B * 0.5, cutoff=900), 0.3, pan=0.15)
    m.render(path)

# ---- Option B: lo-fi -----------------------------------------------------------------------------------------
def lofi(path):
    m = Mix(); swing = 0.09 * B
    m.add(0, crackle(DUR), 0.5)
    for bar in range(4):
        for f in chord(bar * 4): m.add(bar * 4 * B, rhodes(f, 4 * B), 0.55, pan=rng.uniform(-0.3, 0.3))
    m.add(2 * B, riser(2 * B), 0.5)
    for b in range(BEATS):
        if b in HOME_BEATS or b == 12: m.add(b * B, kick(dur=0.35, f0=120, f1=52, punch=0.4), 0.9)
        if b in HOME_BEATS and b % 2 == 1: m.add(b * B, snare(), 0.75)
        if b in HOME_BEATS or b in CLOSE:
            m.add(b * B, hat(dur=0.05), 0.3, pan=0.2); m.add(b * B + B / 2 + swing, hat(dur=0.05), 0.22, pan=0.2)
        if b in HOME_BEATS and b % 2 == 0: m.add(b * B, bass(root(b), B * 1.6, cutoff=180, drive=1.1), 0.8)
    m.render(path)

# ---- Option C: trap, half-time -------------------------------------------------------------------------------
def trap(path):
    m = Mix()
    for bar in range(4): m.add(bar * 4 * B, pad([f / 2 for f in chord(bar * 4)], 4 * B, cutoff=600, a=1.2), 0.7)
    m.add(2 * B, riser(2 * B), 1.0)
    m.add(4 * B, impact(), 0.9)
    for b in range(BEATS):
        if b in HOME_BEATS or b == 12: m.add(b * B, kick808(dur=B * 0.95, f1=root(b) / 2 if root(b) > 50 else root(b)), 1.0)
        if b in HOME_BEATS and b % 4 == 2: m.add(b * B, clap(), 0.8); m.add(b * B, snare(), 0.5)
        if b in HOME_BEATS or b in CLOSE:
            for q in range(4):
                g = 0.3 if q == 0 else 0.18
                m.add(b * B + q * B / 4, hat(dur=0.04), g, pan=0.25 if q % 2 else -0.25)
            if b in (7, 11):                                            # a 32nd roll into the next bar
                for q in range(8): m.add(b * B + B / 2 + q * B / 16, hat(dur=0.03), 0.22)
    m.render(path)

deep_house(f"{out}/bed-deep-house.wav"); lofi(f"{out}/bed-lofi.wav"); trap(f"{out}/bed-trap.wav")
