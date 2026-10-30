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

# ---- shared: the front (hook) build and the back end that follows the typewriter -----------------------------
def tick():
    n = int(0.05 * SR); tt = t(n)
    return (hp(rng.normal(0, 1, n), 3500, 4) * np.exp(-tt * 180) + np.sin(2 * np.pi * 2400 * tt) * np.exp(-tt * 260) * 0.5) * 0.7
def ding(f=1760):
    n = int(1.2 * SR); tt = t(n)
    return (np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(2 * np.pi * f * 2.76 * tt) * np.exp(-tt * 6)) * np.exp(-tt * 3.2) * 0.35
def reverse_cymbal(dur):
    n = int(dur * SR); tt = t(n)
    return hp(rng.normal(0, 1, n), 5000, 4) * (tt / dur) ** 3 * 0.4
def front(m, heavy=True):
    # Hook bar: a muted half-time kick, a ticking hat, the pad opening, a reverse cymbal and a pre-drop stab.
    for b in (0, 2): m.add(b * B, lp(kick(punch=0.3), 400), 0.55 if heavy else 0.4)
    for b in range(4): m.add(b * B, hat(dur=0.04), 0.18, pan=0.2)
    m.add(2 * B, reverse_cymbal(2 * B), 0.8)
    m.add(3.5 * B, stab(chord(0), 0.5 * B, cutoff=2600), 0.5, pan=-0.15)
def typewriter(m, t0, rate=14.0, start=0.2, chars=25, last_f=1760):
    # Mirrors comp.html: n = floor((tt - START) * RATE); character k appears at tt = start + k / rate.
    # n = 13 is the space between the lines (no letter, so no tick). The last one is the question mark.
    for k in range(1, chars + 1):
        if k == 13: continue
        m.add(t0 + start + k / rate, tick(), 0.75 if k != chars else 0.4, pan=0.35)
    m.add(t0 + start + chars / rate, ding(last_f), 0.9, pan=0.1)
    m.add(t0 + start + chars / rate, kick(punch=0.6), 0.8)

# ---- Option A: deep house ------------------------------------------------------------------------------------
def deep_house(path):
    m = Mix()
    for bar in range(4): m.add(bar * 4 * B, pad(chord(bar * 4), 4 * B, cutoff=900), 0.8)
    m.add(2 * B, riser(2 * B), 0.9); front(m)
    m.add(4 * B, impact(), 0.7); typewriter(m, 12 * B)
    for b in range(BEATS):
        if b in HOME_BEATS: m.add(b * B, kick(), 1.0)
        if b in CLOSE: m.add(b * B, kick(), 0.6)
        if b in HOME_BEATS or b in CLOSE:
            m.add(b * B + B / 2, hat(open_=True), 0.5 if b in HOME_BEATS else 0.25, pan=0.3)
            for q in (0.25, 0.75): m.add(b * B + q * B, hat(), 0.35, pan=-0.2)
        if b in HOME_BEATS and b % 2 == 1: m.add(b * B, clap(), 0.7)
        if b in HOME_BEATS:
            m.add(b * B, bass(root(b), B * 0.45), 0.9); m.add(b * B + B / 2, bass(root(b), B * 0.4, cutoff=200), 0.6)
            m.add(b * B + B / 2, stab(chord(b), B * 0.5), 0.55, pan=0.15)
        if b in CLOSE:
            m.add(b * B + B / 2, stab(chord(b), B * 0.5, cutoff=1100), 0.35, pan=0.15)
            if b % 2 == 0: m.add(b * B, bass(root(b), B * 0.45), 0.55)
    m.render(path)

# ---- Option B: lo-fi -----------------------------------------------------------------------------------------
def lofi(path):
    m = Mix(); swing = 0.09 * B
    m.add(0, crackle(DUR), 0.5)
    for bar in range(4):
        for f in chord(bar * 4): m.add(bar * 4 * B, rhodes(f, 4 * B), 0.55, pan=rng.uniform(-0.3, 0.3))
    m.add(2 * B, riser(2 * B), 0.5); front(m, heavy=False); typewriter(m, 12 * B, last_f=1318)
    for b in range(BEATS):
        if b in HOME_BEATS: m.add(b * B, kick(dur=0.35, f0=120, f1=52, punch=0.4), 0.9)
        if b in CLOSE and b % 2 == 0: m.add(b * B, kick(dur=0.35, f0=120, f1=52, punch=0.4), 0.6)
        if b in CLOSE and b % 2 == 1: m.add(b * B, snare(), 0.4)
        if b in HOME_BEATS and b % 2 == 1: m.add(b * B, snare(), 0.75)
        if b in HOME_BEATS or b in CLOSE:
            m.add(b * B, hat(dur=0.05), 0.3, pan=0.2); m.add(b * B + B / 2 + swing, hat(dur=0.05), 0.22, pan=0.2)
        if b in HOME_BEATS and b % 2 == 0: m.add(b * B, bass(root(b), B * 1.6, cutoff=180, drive=1.1), 0.8)
    m.render(path)

# ---- Option C: trap, half-time -------------------------------------------------------------------------------
def trap(path):
    m = Mix()
    for bar in range(4): m.add(bar * 4 * B, pad([f / 2 for f in chord(bar * 4)], 4 * B, cutoff=600, a=1.2), 0.7)
    m.add(2 * B, riser(2 * B), 1.0); front(m)
    m.add(4 * B, impact(), 0.9); typewriter(m, 12 * B, last_f=880)
    for b in range(BEATS):
        if b in HOME_BEATS: m.add(b * B, kick808(dur=B * 0.95, f1=root(b) / 2 if root(b) > 50 else root(b)), 1.0)
        if b in CLOSE and b % 2 == 0: m.add(b * B, kick808(dur=B * 0.95, f1=root(b) / 2 if root(b) > 50 else root(b)), 0.7)
        if b in HOME_BEATS and b % 4 == 2: m.add(b * B, clap(), 0.8); m.add(b * B, snare(), 0.5)
        if b in HOME_BEATS or b in CLOSE:
            for q in range(4):
                g = 0.3 if q == 0 else 0.18
                m.add(b * B + q * B / 4, hat(dur=0.04), g, pan=0.25 if q % 2 else -0.25)
            if b in (7, 11):                                            # a 32nd roll into the next bar
                for q in range(8): m.add(b * B + B / 2 + q * B / 16, hat(dur=0.03), 0.22)
    m.render(path)

# ---- Option D: upbeat house (double time: two kicks per home, 160 BPM feel) ----------------------------------
def pluck(f, dur):
    n = int(dur * SR); tt = t(n)
    x = lp(saw(f, n, detune=6), 3200) * np.exp(-tt * 9) + np.sin(2 * np.pi * f * tt) * np.exp(-tt * 12) * 0.5
    return x * env(n, 0.002, 0.12, 0.3, 0.08, hold=max(0, dur - 0.2)) * 0.5
def upbeat_house(path):
    m = Mix(); H = B / 2
    # brighter voicings: the same progression an octave up, with the 9th on top
    for bar in range(4): m.add(bar * 4 * B, pad([f * 2 for f in chord(bar * 4)], 4 * B, cutoff=1600), 0.55)
    m.add(2 * B, riser(2 * B), 1.0); front(m)
    for q in range(4):                                                   # pre-drop: kick on every 8th of beat 3
        m.add(3 * B + q * B / 4, lp(kick(punch=0.5), 700), 0.5 + 0.12 * q)
    m.add(4 * B, impact(), 0.8); typewriter(m, 12 * B, last_f=2093)
    arp = [0, 2, 1, 3, 2, 3, 1, 2]                                       # chord-tone arpeggio, 16ths
    for b in range(BEATS):
        groove = b in HOME_BEATS; close = b in CLOSE
        if groove or close:
            for h in (0, 1): m.add(b * B + h * H, kick(dur=0.32, f0=170, f1=50), 1.0 if groove else 0.6)
            for h in (0, 1): m.add(b * B + h * H + H / 2, hat(open_=True), 0.4 if groove else 0.25, pan=0.3)
            for q in range(4): m.add(b * B + q * B / 4, hat(dur=0.04), 0.28, pan=-0.2)
            if b % 2 == 1: m.add(b * B, clap(), 0.8 if groove else 0.45)
            c = chord(b)
            for q in range(4): m.add(b * B + q * B / 4, pluck(c[arp[(b * 4 + q) % 8]] * 2, B / 4), 0.6 if groove else 0.35, pan=0.2 * (-1) ** q)
        if groove:
            m.add(b * B, bass(root(b) * 2, H * 0.8, cutoff=320), 0.8); m.add(b * B + H, bass(root(b) * 2, H * 0.8, cutoff=260), 0.65)
            if b % 2 == 0: m.add(b * B + B / 2 + B / 4, stab(c, B / 4, cutoff=2400), 0.45, pan=0.1)
    m.render(path)

# ---- Option E: bounce, in the style of the example reel's track ----------------------------------------------
# The example (analysed 2026-10-30): a dense kick pattern under the cuts, punchy backbeat, mid-heavy, hip-hop
# bounce rather than house. Same 80 BPM grid, two kicks per home, snare on two and four, an 808 that glides into
# each bar, 16th hats with a swing, and a phonk-style cowbell melody carrying the hook.
def cowbell(f, dur):
    n = int(dur * SR); tt = t(n)
    x = (np.sign(np.sin(2 * np.pi * f * tt)) * 0.5 + np.sign(np.sin(2 * np.pi * f * 1.48 * tt)) * 0.5) * np.exp(-tt * 10)
    return bp(x, 500, 4000) * 0.35
def bounce(path):
    m = Mix(); H = B / 2; sw = 0.06 * B
    for bar in range(4): m.add(bar * 4 * B, pad([f / 2 for f in chord(bar * 4)], 4 * B, cutoff=700, a=1.0), 0.6)
    m.add(2 * B, riser(2 * B), 1.0); front(m)
    for q in range(4): m.add(3 * B + q * B / 4, lp(kick(punch=0.5), 700), 0.45 + 0.12 * q)   # pre-drop stutter
    m.add(4 * B, impact(), 0.9); typewriter(m, 12 * B, last_f=1175)
    # cowbell melody on the chord tones, 8ths, two-bar phrase
    MEL = [0, 2, 1, 0, 3, 2, 1, 2, 0, 2, 1, 3, 2, 1, 0, 1]
    for b in range(BEATS):
        groove = b in HOME_BEATS; close = b in CLOSE; c = chord(b)
        if groove or close:
            g = 1.0 if groove else 0.6
            m.add(b * B, kick(dur=0.4, f0=180, f1=52, punch=1.2), g)                 # the "boom" on every home
            m.add(b * B + H + (sw if b % 2 else 0), kick(dur=0.3, f0=150, f1=55, punch=0.8), 0.7 * g)
            if b % 2 == 1: m.add(b * B, snare(), 0.9 * g); m.add(b * B, clap(), 0.5 * g)
            for q in range(4): m.add(b * B + q * B / 4 + (sw if q % 2 else 0), hat(dur=0.04), (0.32 if q % 2 == 0 else 0.2) * g, pan=0.25 * (-1) ** q)
            for h in (0, 1): m.add(b * B + h * H, cowbell(c[MEL[(b * 2 + h) % 16]] * 2, H * 0.9), 0.7 * g, pan=0.15)
        if groove and b % 2 == 0: m.add(b * B, kick808(dur=B * 1.9, f0=root(b) * 1.5, f1=root(b)), 0.9)
        if groove and b % 4 == 3: m.add(b * B + H, bass(root(b) * 2, H * 0.8, cutoff=300), 0.6)
    m.render(path)

# ---- Option F: piano house at 128, the lane of "Feel So Close" (own chords, own melody) ----------------------
# Grid in beats: hook 8, first home 3, six homes at 2, closing 8 = 31 beats. Run with --bpm 128 --beats 31 --style piano.
def supersaw(f, n, voices=7, spread=18):
    tt = t(n); x = np.zeros(n)
    for k in range(voices):
        d = (k - (voices - 1) / 2) / ((voices - 1) / 2) * spread
        x += 2 * ((tt * f * 2 ** (d / 1200) + k * 0.13) % 1.0) - 1
    return x / voices
def piano(f, dur):
    n = int(dur * SR); tt = t(n)
    x = np.sin(2 * np.pi * f * tt) * np.exp(-tt * 2.2) + 0.5 * np.sin(2 * np.pi * 2 * f * tt) * np.exp(-tt * 4) \
        + 0.25 * np.sin(2 * np.pi * 3 * f * tt) * np.exp(-tt * 7) + 0.12 * np.sin(2 * np.pi * 4.01 * f * tt) * np.exp(-tt * 12)
    return np.tanh(x * 1.3) * env(n, 0.002, 0.25, 0.5, 0.2, hold=max(0, dur - 0.45)) * 0.45
def lead(f, dur):
    n = int(dur * SR); tt = t(n); vib = 1 + 0.004 * np.sin(2 * np.pi * 5.5 * tt) * np.minimum(1, tt * 3)
    x = lp(supersaw(f, n, voices=5, spread=10) * vib, 3800) + np.sin(2 * np.pi * f * tt) * 0.3
    return x * env(n, 0.01, 0.15, 0.75, 0.12, hold=max(0, dur - 0.27)) * 0.5
def pump(n_total, kicks, depth=0.55, rel=0.28):
    e = np.ones(n_total)
    for k in kicks:
        i = int(k * SR); m = int(rel * SR); seg = e[i:i + m]
        seg *= 1 - depth * np.exp(-np.arange(len(seg)) / SR * (4 / rel))
    return e
def piano_house(path):
    HOOKB, FIRSTB, HOMEB, TAILB = 8, 3, 2, 8
    drop = HOOKB; close = HOOKB + FIRSTB + 6 * HOMEB; total = close + TAILB
    assert total == BEATS, (total, BEATS)
    # F major, I–V–vi–IV, one chord per bar
    PROGF = [["F3", "A3", "C4", "F4"], ["C3", "E3", "G3", "C4"], ["D3", "F3", "A3", "D4"], ["A#2", "D3", "F3", "A#3"]]
    ROOTF = ["F1", "C2", "D2", "A#1"]
    def ch(b): return [note(x) for x in PROGF[(b // 4) % 4]]
    def rt(b): return note(ROOTF[(b // 4) % 4])
    dry = Mix(); wet = Mix(); kicks = []
    # hook: piano chords on every beat, pushed on the "and" of 2 and 4, a riser and a snare roll into the drop
    for b in range(HOOKB):
        for f in ch(b): wet.add(b * B, piano(f * 2, B * 0.95), 0.5, pan=rng.uniform(-0.25, 0.25))
        if b % 2 == 1:
            for f in ch(b): wet.add(b * B + B / 2, piano(f * 2, B * 0.45), 0.3)
        wet.add(b * B, hat(dur=0.04), 0.18, pan=0.2)
        if b >= 4: dry.add(b * B, lp(kick(punch=0.3), 500), 0.5)
    for q in range(8): dry.add((HOOKB - 2) * B + q * B / 4, snare(), 0.25 + 0.07 * q)
    wet.add((HOOKB - 4) * B, riser(4 * B), 1.0); dry.add((HOOKB - 4) * B, reverse_cymbal(4 * B), 0.8)
    dry.add(drop * B, impact(), 0.9)
    # drop + closing: four-on-the-floor, offbeat bass, supersaw chords (pumped), lead melody during the homes
    MOTIF = [(0, 0.5), (2, 0.5), (3, 1.0), (2, 0.5), (0, 0.5), (1, 1.0), (3, 0.5), (2, 0.5), (1, 1.0), (0, 1.0)]   # chord-tone index, beats
    for b in range(drop, total):
        groove = b < close; g = 1.0 if groove else 0.7
        dry.add(b * B, kick(dur=0.4, f0=170, f1=50), g); kicks.append(b * B)
        dry.add(b * B + B / 2, hat(open_=True), 0.4 * g, pan=0.3)
        for q in (0.25, 0.75): dry.add(b * B + q * B, hat(dur=0.04), 0.3 * g, pan=-0.2)
        if b % 2 == 1: dry.add(b * B, clap(), 0.7 * g)
        dry.add(b * B + B / 2, bass(rt(b) * 2, B * 0.45, cutoff=420, drive=1.6), 0.8 * g)
        if b % 4 == 0:
            n = int(4 * B * SR); x = sum(lp(supersaw(f * 2, n), 5000) for f in ch(b)) / 4
            wet.add(b * B, x * env(n, 0.02, 0.1, 0.9, 0.3, hold=4 * B - 0.42) * 0.5, 0.75 * g)
            for f in ch(b): wet.add(b * B, piano(f * 2, 4 * B), 0.3)
    # the melody: an original two-bar motif, repeated over the homes, octave up over the last pass
    tb = drop; pos = 0.0; k = 0
    while tb + pos / 1.0 < close:
        idx, ln = MOTIF[k % len(MOTIF)]
        at = (drop + pos) * B; bb = drop + int(pos)
        if bb < close:
            oct_ = 4 if (pos >= 8) else 2
            wet.add(at, lead(ch(bb)[idx] * oct_, ln * B * 0.95), 0.55, pan=0.1)
        pos += ln; k += 1
    typewriter(wet, close * B, last_f=1397)
    m = Mix(); pe = pump(N, kicks)
    m.L = dry.L + wet.L * pe; m.R = dry.R + wet.R * pe
    m.render(path)

STYLE = args[args.index("--style") + 1] if "--style" in args else None
if STYLE == "piano": piano_house(f"{out}/bed-piano-house.wav")
else: deep_house(f"{out}/bed-deep-house.wav"); trap(f"{out}/bed-trap.wav"); bounce(f"{out}/bed-bounce.wav")
