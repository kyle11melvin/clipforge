# Procedural score + voiceover mix for THE CONVERGENCE (30 s, 48 kHz stereo).
# Pure numpy so it runs offline. Usage: python3 score.py <vo-dir> <voice> <out.wav>
import sys, numpy as np, soundfile as sf
SR = 48000; DUR = 30.0; N = int(SR*DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(3)

def env(start, end, attack=0.05, release=0.3):
    e = np.zeros(N); a = int(attack*SR); r = int(release*SR); s = int(start*SR); f = int(end*SR)
    if f > N: f = N
    e[s:min(s+a, f)] = np.linspace(0, 1, min(a, f-s)); e[s+a:f] = 1
    if f < N: e[f:min(f+r, N)] = np.linspace(1, 0, min(r, N-f))
    return e
def seg(start, dur, attack=0.05, release=0.3): return env(start, start+dur, attack, release)
def midi(n): return 440*2**((n-69)/12)
def pad(note, start, end, gain=1.0, detune=0.006, partials=(1,2,3,4,5), pw=(1,.45,.25,.14,.08), attack=1.2, release=1.5, lfo=0.11):
    f = midi(note); out = np.zeros(N)
    for k, w in zip(partials, pw):
        for d in (-detune, 0, detune):
            ph = rng.uniform(0, 6.28)
            out += w*np.sin(2*np.pi*f*k*(1+d)*t + ph)
    # slow filter-like shimmer: fade the upper partials with an LFO
    out *= (0.75 + 0.25*np.sin(2*np.pi*lfo*t + rng.uniform(0,6)))
    return gain*out*env(start, end, attack, release)/len(partials)
def pluck(note, start, dur=0.35, gain=1.0, bright=2.0):
    f = midi(note); s = int(start*SR); n = int(dur*SR); n = min(n, N-s)
    tt = np.arange(n)/SR
    w = np.sin(2*np.pi*f*tt) + 0.4*np.sin(2*np.pi*f*2*tt)*np.exp(-tt*bright*6) + 0.15*np.sin(2*np.pi*f*3*tt)*np.exp(-tt*bright*10)
    w *= np.exp(-tt*(4/dur))*gain
    out = np.zeros(N); out[s:s+n] += w; return out
def bell(note, start, dur=2.5, gain=1.0):
    f = midi(note); s = int(start*SR); n = min(int(dur*SR), N-s); tt = np.arange(n)/SR
    w = (np.sin(2*np.pi*f*tt)*np.exp(-tt*1.6) + 0.5*np.sin(2*np.pi*f*2.0*tt)*np.exp(-tt*3) + 0.25*np.sin(2*np.pi*f*3.01*tt)*np.exp(-tt*5))*gain
    w[:200] *= np.linspace(0,1,200)
    out = np.zeros(N); out[s:s+n] += w; return out
def noise_swell(start, end, gain=1.0, curve=2.5):
    e = np.zeros(N); s=int(start*SR); f=int(end*SR)
    e[s:f] = np.linspace(0,1,f-s)**curve
    n = rng.normal(0, 1, N)
    # cheap low-pass: moving average, then a second pass
    k = 24; n = np.convolve(n, np.ones(k)/k, 'same'); n = np.convolve(n, np.ones(k)/k, 'same')
    return gain*n*e
def boom(start, gain=1.0):
    s=int(start*SR); n=min(int(2.2*SR), N-s); tt=np.arange(n)/SR
    f = 42 + 70*np.exp(-tt*9)
    w = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*2.2)
    w += 0.5*rng.normal(0,1,n)*np.exp(-tt*18)
    out=np.zeros(N); out[s:s+n]+=gain*w; return out
def blip(start, f0=1800, f1=2600, dur=0.09, gain=0.25):
    s=int(start*SR); n=min(int(dur*SR), N-s); tt=np.arange(n)/SR
    f = np.linspace(f0, f1, n); w = np.sin(2*np.pi*np.cumsum(f)/SR)*np.hanning(n)*gain
    out=np.zeros(N); out[s:s+n]+=w; return out

L = np.zeros(N); R = np.zeros(N)
def add(sig, panL=1.0, panR=1.0):
    global L, R; L += sig*panL; R += sig*panR

# ---- 0-6 s: atmospheric tension (D minor drone, airy fifth) ----
add(pad(38, 0, 6.6, gain=.55, attack=1.5), 1, 1)            # D2
add(pad(57, 0, 6.6, gain=.22, attack=2.5), .9, 1)           # A3
add(pad(65, 1.2, 6.6, gain=.15, attack=2.0), 1, .8)         # F4 (minor colour)
add(noise_swell(0, 3.0, gain=.05, curve=1.5)*np.exp(-np.clip(t-3,0,None)*3), 1, 1)
# warm turn at Switchboard's entrance (3 s)
add(pad(50, 3.0, 9.3, gain=.35, attack=1.0), 1, 1)          # D3
add(pad(62, 3.2, 9.3, gain=.18, attack=1.2), .8, 1)         # D4
add(pad(69, 3.4, 9.3, gain=.10, attack=1.6), 1, .8)         # A4

# ---- 6-16 s: building rhythmic movement, 100 bpm ----
bpm = 100; beat = 60/bpm
seq = [62, 69, 74, 69, 65, 69, 74, 77]  # D A D A F A D F arpeggio
i = 0; tt0 = 6.0
while tt0 < 16.0:
    g = 0.10 + 0.12*min(1, (tt0-6)/8)
    note = seq[i % len(seq)] + (0 if tt0 < 12 else 0)
    add(pluck(note, tt0, dur=0.32, gain=g), 1 if i%2 else .7, .7 if i%2 else 1)
    if i % 4 == 0: add(pluck(38, tt0, dur=0.5, gain=.35, bright=.6), 1, 1)   # bass on the beat
    tt0 += beat/2; i += 1
add(pad(50, 9.0, 16.5, gain=.32, attack=.8), 1, 1)
add(pad(57, 9.0, 16.5, gain=.18, attack=.8), 1, 1)
add(pad(65, 12.0, 16.5, gain=.14, attack=1.0), .8, 1)
for s_ in (6.05, 9.05, 12.05): add(blip(s_))                                 # scene-change digital ticks
for s_ in (12.3, 13.4, 14.6): add(blip(s_, 1200, 1700, 0.06, .12))           # the three answers start

# ---- 16-19 s: tension during evaluation ----
add(pad(38, 16.0, 19.5, gain=.5, attack=.6), 1, 1)
add(pad(51, 16.2, 19.5, gain=.25, attack=.6), 1, 1)         # Eb3 against D: unease
add(pad(57, 16.0, 19.5, gain=.15, attack=.6), 1, 1)
for k in range(4): add(pluck(74 + (k%2), 16.65 + k*0.42, dur=0.25, gain=.18, bright=3), .8, 1)   # each finding
pulse = np.zeros(N); s_=int(16*SR); f_=int(19.3*SR); pulse[s_:f_] = (np.sin(2*np.pi*4*t[s_:f_])>0.6)*np.sin(2*np.pi*midi(38)*t[s_:f_])*0.18*np.linspace(.3,1,f_-s_)
add(pulse, 1, 1)

# ---- 19-23 s: the rise and the convergence impact ----
add(noise_swell(19.0, 21.55, gain=.22, curve=2.2), 1, 1)
rise_n = int(2.55*SR); s_=int(19.0*SR); tt = np.arange(rise_n)/SR
fr = midi(50)*2**(tt/2.55*1.0); sweep = np.sin(2*np.pi*np.cumsum(fr)/SR)*(tt/2.55)**2*0.18
tmp=np.zeros(N); tmp[s_:s_+rise_n]=sweep; add(tmp, .9, 1)
add(pad(50, 19.0, 21.6, gain=.3, attack=1.5), 1, 1)
add(pad(57, 19.5, 21.6, gain=.25, attack=1.2), 1, 1)
add(pad(62, 20.0, 21.6, gain=.22, attack=1.0), 1, 1)
add(boom(21.55, gain=.9), 1, 1)
# resolution chord on impact: D major add9, wide
for n_, g_ in ((38,.5),(50,.4),(57,.3),(66,.26),(69,.2),(76,.12)): add(pad(n_, 21.55, 30.0, gain=g_, attack=.08, release=.6), 1, 1)
add(bell(74, 21.6, dur=3, gain=.25), .8, 1); add(bell(81, 21.75, dur=3, gain=.15), 1, .8)

# ---- 23-30 s: confident resolution, soft pulse, sonic logo ----
tt0 = 23.0; i=0
while tt0 < 27.6:
    add(pluck([62,66,69,74][i%4], tt0, dur=0.4, gain=.09*(1-(tt0-23)/6)), 1 if i%2 else .7, .7 if i%2 else 1); tt0 += beat; i+=1
add(bell(74, 28.1, dur=2.0, gain=.3), .9, 1)   # sonic logo: three streams rise, one note lands
add(bell(81, 28.3, dur=2.0, gain=.25), 1, .9)
add(bell(86, 28.5, dur=1.8, gain=.2), 1, 1)
add(bell(62, 28.75, dur=1.3, gain=.45), 1, 1)
add(pad(38, 28.7, 30.0, gain=.35, attack=.05, release=.2), 1, 1)

music = np.stack([L, R], 1)
music /= np.max(np.abs(music)) + 1e-9
# gentle soft-clip for glue
music = np.tanh(music*1.4)/np.tanh(1.4)

# ---- voiceover ----
vo_dir, voice, out = sys.argv[1], sys.argv[2], sys.argv[3]
starts = {"vo1":0.25,"vo2":3.2,"vo3":6.2,"vo4":9.2,"vo5":12.2,"vo6":16.15,"vo7":19.25,"vo8":23.25,"vo9":28.35}
vo = np.zeros(N); duck = np.zeros(N)
for name, st in starts.items():
    a, sr = sf.read(f"{vo_dir}/{voice}-{name}.wav")
    if a.ndim > 1: a = a.mean(1)
    # resample 24k -> 48k by linear interpolation
    x = np.arange(len(a))/sr; xi = np.arange(int(len(a)*SR/sr))/SR; a = np.interp(xi, x, a)
    s_ = int(st*SR); n = min(len(a), N-s_); vo[s_:s_+n] += a[:n]
    duck[max(0,s_-int(.15*SR)):min(N,s_+n+int(.25*SR))] = 1
vo /= np.max(np.abs(vo)) + 1e-9
# smooth the duck envelope (120 ms)
k = int(0.12*SR); duck = np.convolve(duck, np.ones(k)/k, 'same'); duck = np.clip(duck, 0, 1)
gain_m = 10**(-7/20)  # music 7 dB under the voice while it speaks
music_level = 0.42; vo_level = 0.9
mixed = music*music_level*(1 - duck[:,None]*(1-gain_m)) + np.stack([vo, vo],1)*vo_level
# final fade on the last 150 ms to avoid a click at the cut
fade = np.ones(N); fade[-int(.15*SR):] = np.linspace(1, 0, int(.15*SR))
mixed *= fade[:,None]
mixed = np.clip(mixed, -1, 1)
sf.write(out, mixed, SR, subtype="PCM_24")
print("wrote", out, mixed.shape, "peak", float(np.max(np.abs(mixed))))
