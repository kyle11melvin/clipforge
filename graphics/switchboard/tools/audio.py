# Synthesised soundtrack for the Switchboard spot: a restrained cinematic-electronic bed, typing,
# a submit chime, airy transition sweeps, a convergence shimmer, and the voiceover lines placed on
# their scene cues with the music ducked beneath them. Writes mix-vo.wav and mix-novo.wav.
import numpy as np, soundfile as sf
from scipy import signal
from pathlib import Path
SR = 48000; DUR = 30.0; N = int(SR*DUR); t = np.arange(N)/SR
rng = np.random.default_rng(7)
vo_dir = Path("videos/switchboard/vo"); out_dir = Path("videos/switchboard")

def env_adsr(n, a, d, s, r, sr=SR):
    a, d, r = int(a*sr), int(d*sr), int(r*sr); e = np.ones(n)
    a = min(a, n); e[:a] = np.linspace(0, 1, a)
    if d: e[a:a+d] = np.linspace(1, s, min(d, max(0, n-a)))
    e[a+d:n-r] = s if n-r > a+d else e[a+d:n-r]
    if r: e[-r:] *= np.linspace(1, 0, r)
    return e
def place(buf, sig, at):
    i = int(at*SR); j = min(N, i+len(sig)); buf[i:j] += sig[:j-i]
def lowpass(x, fc, order=2):
    b, a = signal.butter(order, fc/(SR/2)); return signal.lfilter(b, a, x)
def bandpass(x, lo, hi, order=2):
    b, a = signal.butter(order, [lo/(SR/2), hi/(SR/2)], btype="band"); return signal.lfilter(b, a, x)
def saw(f, n, detune=0.0):
    tt = np.arange(n)/SR; out = np.zeros(n)
    for k in range(1, 24): out += np.sin(2*np.pi*f*(1+detune)*k*tt)/k
    return out
def midi(m): return 440*2**((m-69)/12)

# ---- music bed: D minor, 92 bpm, chords every 4 beats; resolves to D major at 28 s
chords = [  # (start, end, midi notes)
    (0, 3, [50, 57, 60, 65]),      # Dm
    (3, 6, [46, 53, 58, 62]),      # Bb
    (6, 9, [50, 57, 60, 65]),      # Dm
    (9, 12, [48, 55, 60, 64]),     # C
    (12, 16, [46, 53, 57, 62]),    # Bb
    (16, 19, [45, 52, 57, 60]),    # Am
    (19, 23, [46, 53, 58, 62]),    # Bb (build)
    (23, 26, [48, 55, 60, 64]),    # C
    (26, 28, [50, 57, 62, 65]),    # Dm(add4)
    (28, 30, [50, 57, 62, 66]),    # D major (resolve)
]
music = np.zeros(N)
for (a, b, notes) in chords:
    n = int((b-a+0.6)*SR); e = env_adsr(n, 0.9, 0.0, 1.0, 0.7)
    pad = np.zeros(n)
    for m in notes:
        f = midi(m)
        pad += saw(f, n, 0.003) + saw(f, n, -0.004) + 0.5*np.sin(2*np.pi*f*np.arange(n)/SR)
    # slow filter opening: brighter during the convergence and the resolve
    fc = 900 + 1800*(1 if a >= 19 else 0.35)
    pad = lowpass(pad*e, fc) * 0.035
    place(music, pad, a)
# sub pulse on the beat, soft
beat = 60/92
for k in range(int(DUR/beat)):
    at = k*beat
    root = [c for c in chords if c[0] <= at < c[1]]
    if not root: continue
    f = midi(root[0][2][0]-12); n = int(0.5*SR); tt = np.arange(n)/SR
    s = np.sin(2*np.pi*f*tt) * np.exp(-tt*6) * 0.22
    place(music, s, at)
# sparse pluck arpeggio, growing from 12 s, busiest in the convergence
for k in range(int(DUR/(beat/2))):
    at = k*beat/2
    if at < 6 or at >= 28.6: continue
    c = [c for c in chords if c[0] <= at < c[1]][0]
    dens = 0.35 if at < 12 else (0.6 if at < 19 else (0.9 if at < 23 else 0.5))
    if rng.random() > dens: continue
    m = c[2][rng.integers(1, len(c[2]))] + 12*rng.integers(1, 3)
    f = midi(m); n = int(0.6*SR); tt = np.arange(n)/SR
    s = (np.sin(2*np.pi*f*tt) + 0.3*np.sin(2*np.pi*2*f*tt)) * np.exp(-tt*9) * 0.06
    place(music, s, at + rng.uniform(-0.01, 0.01))
# riser into the convergence hub (19.3 -> 21.0) and a soft swell into the brand (27.4 -> 28.2)
for (a, b, g) in ((19.3, 21.0, 0.05), (27.3, 28.1, 0.04)):
    n = int((b-a)*SR); noise = rng.standard_normal(n)
    sw = np.zeros(n)
    for i in range(0, n, 2400):
        seg = noise[i:i+2400]; fc = 300 + 2500*(i/n)**2
        sw[i:i+2400] = bandpass(seg, fc, fc*2.2)
    sw *= np.linspace(0, 1, n)**2 * g
    place(music, sw, a)
music = lowpass(music, 9000)
# tail: fade to silence over the last 0.6 s so the cut is clean
music[-int(0.6*SR):] *= np.linspace(1, 0, int(0.6*SR))

# ---- sfx
sfx = np.zeros(N)
# typing 3.55 -> 4.9
at = 3.55
while at < 4.9:
    n = int(0.03*SR); s = bandpass(rng.standard_normal(n), 1800, 5200) * np.exp(-np.arange(n)/SR*180) * 0.5
    place(sfx, s, at); at += rng.uniform(0.032, 0.058)
# second typing pass for the improved prompt (quieter, faster) 6.9 -> 8.1
at = 6.9
while at < 8.1:
    n = int(0.025*SR); s = bandpass(rng.standard_normal(n), 2200, 6000) * np.exp(-np.arange(n)/SR*220) * 0.28
    place(sfx, s, at); at += rng.uniform(0.022, 0.04)
# submit chime 5.15
n = int(1.2*SR); tt = np.arange(n)/SR
chime = (np.sin(2*np.pi*880*tt)*np.exp(-tt*5) + 0.7*np.sin(2*np.pi*1318.5*tt)*np.exp(-tt*4) + 0.3*np.sin(2*np.pi*2637*tt)*np.exp(-tt*7)) * 0.2
chime[:int(0.004*SR)] *= np.linspace(0, 1, int(0.004*SR)); place(sfx, chime, 5.15)
# teal highlight sweep 8.05: soft airy whoosh
def whoosh(dur, lo, hi, gain):
    n = int(dur*SR); x = bandpass(rng.standard_normal(n), lo, hi); e = np.sin(np.linspace(0, np.pi, n))**1.5; return x*e*gain
place(sfx, whoosh(0.9, 1200, 4000, 0.15), 8.0)
# airy transitions on the light sweeps
for s0 in (3, 9, 16, 23, 28): place(sfx, whoosh(0.7, 500, 2500, 0.17), s0 - 0.1)
# card / glow pops: tiny soft ticks
for at in (9.75, 10.05, 10.35, 12.4, 12.9, 13.4, 16.45, 16.85, 17.25, 17.65, 21.1, 21.35, 21.6, 21.85, 23.9, 24.2, 24.5, 24.8):
    n = int(0.12*SR); tt = np.arange(n)/SR; f = 1500 if at < 21 else 2100
    s = np.sin(2*np.pi*f*tt)*np.exp(-tt*40)*0.12; place(sfx, s, at)
# convergence shimmer 19.3 -> 22.5: sparkling pings over a rising air
for i in range(70):
    at = 19.3 + 3.0*rng.random()**0.8; f = rng.uniform(1800, 6500); n = int(0.5*SR); tt = np.arange(n)/SR
    s = np.sin(2*np.pi*f*tt)*np.exp(-tt*10)*0.05*(0.4 + 0.6*(at-19.3)/3); place(sfx, s, at)
place(sfx, whoosh(2.2, 2000, 8000, 0.08), 19.4)
# brand resolve 28.0: warm bell + shimmer, settled by 28.5
n = int(2.0*SR); tt = np.arange(n)/SR
bell = (np.sin(2*np.pi*587.3*tt)*np.exp(-tt*2.2) + 0.5*np.sin(2*np.pi*1174.7*tt)*np.exp(-tt*3) + 0.25*np.sin(2*np.pi*1760*tt)*np.exp(-tt*4)) * 0.16
place(sfx, bell, 28.0); place(sfx, whoosh(0.6, 2500, 9000, 0.1), 28.0)
sfx = lowpass(sfx, 12000)

# ---- voiceover placement (scene cue + a breath), with a gentle speed-up on the two tight lines
cues = {1: 0.3, 2: 3.2, 3: 6.2, 4: 9.2, 5: 12.2, 6: 16.2, 7: 19.2, 8: 23.2, 9: 25.85, 10: 28.25}
speed = {9: 1.08}
vo = np.zeros(N)
for k, at in cues.items():
    a, sr = sf.read(vo_dir/f"vo{k:02d}.wav", dtype="float32")
    if a.ndim > 1: a = a.mean(axis=1)
    if sr != SR: a = signal.resample_poly(a, SR, sr)
    if k in speed:  # resample-based speed change keeps it simple; the shift is tiny
        n2 = int(len(a)/speed[k]); a = signal.resample(a, n2)
    a = a / (np.abs(a).max() + 1e-9) * 0.85
    place(vo, a, at)
    print(f"vo{k:02d} at {at:.2f}s -> {at + len(a)/SR:.2f}s")
vo = lowpass(vo, 14000)

# ---- mix: duck the bed under the voice
def rms_env(x, win=0.05):
    w = int(win*SR); e = np.sqrt(np.convolve(x**2, np.ones(w)/w, mode="same")); return e
env = rms_env(vo); duck = 1 - 0.55*np.clip(env/0.08, 0, 1)
duck = signal.lfilter(*signal.butter(1, 6/(SR/2)), duck)  # smooth the gain so it breathes
def normalize(x, peak=0.89): return x / (np.abs(x).max() + 1e-9) * peak
bed = normalize(music, 0.3)
mix_vo = bed*duck + sfx*0.9 + vo
mix_novo = bed + sfx*0.9
mix_vo = normalize(mix_vo, 0.95); mix_novo = normalize(mix_novo, 0.95)
sf.write(out_dir/"mix-vo.wav", mix_vo.astype(np.float32), SR)
sf.write(out_dir/"mix-novo.wav", mix_novo.astype(np.float32), SR)
print("music rms dB", 20*np.log10(np.sqrt(np.mean(bed**2))+1e-9), "vo rms dB", 20*np.log10(np.sqrt(np.mean(vo[vo!=0]**2))+1e-9))
