# Synthesised soundtrack for the Switchboard spot: a restrained cinematic-electronic bed, typing,
# a submit chime, airy transition sweeps, a convergence shimmer, and the voiceover lines placed on
# their scene cues with the music ducked beneath them. Writes mix-vo.wav and mix-novo.wav.
import sys, argparse, numpy as np, soundfile as sf
from scipy import signal
from pathlib import Path
ap = argparse.ArgumentParser(); ap.add_argument("--vo", default="videos/switchboard/vo"); ap.add_argument("--music", default="pad", choices=["pad", "pulse", "v2", "v3", "conv", "final"]); ap.add_argument("--suffix", default=""); ap.add_argument("--late-cues", default="23.2,25.85,28.25", help="start times of lines 8, 9, 10"); ap.add_argument("--duration", type=float, default=30.0); ap.add_argument("--vo-gain", type=float, default=0.85); ap.add_argument("--cues", default="", help="explicit start times for lines 1..n (overrides the V1 cue table)"); ap.add_argument("--speed", default="9:1.08", help="line:factor,... small resample speed-ups")
ARGS = ap.parse_args()
SR = 48000; DUR = ARGS.duration; N = int(SR*DUR); t = np.arange(N)/SR
rng = np.random.default_rng(7)
vo_dir = Path(ARGS.vo); out_dir = Path("videos/switchboard")

def env_adsr(n, a, d, s, r, sr=SR):
    a, d, r = int(a*sr), int(d*sr), int(r*sr); e = np.ones(n)
    a = min(a, n); e[:a] = np.linspace(0, 1, a)
    if d: e[a:a+d] = np.linspace(1, s, min(d, max(0, n-a)))
    e[a+d:n-r] = s if n-r > a+d else e[a+d:n-r]
    if r: e[-r:] *= np.linspace(1, 0, r)
    return e
def place(buf, sig, at):
    i = int(at*SR)
    if i >= N or i < 0: return
    j = min(N, i+len(sig)); buf[i:j] += sig[:j-i]
def lowpass(x, fc, order=2):
    b, a = signal.butter(order, fc/(SR/2)); return signal.lfilter(b, a, x)
def bandpass(x, lo, hi, order=2):
    b, a = signal.butter(order, [lo/(SR/2), hi/(SR/2)], btype="band"); return signal.lfilter(b, a, x)
def saw(f, n, detune=0.0):
    tt = np.arange(n)/SR; out = np.zeros(n)
    for k in range(1, 24): out += np.sin(2*np.pi*f*(1+detune)*k*tt)/k
    return out
def midi(m): return 440*2**((m-69)/12)

def music_pad():
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
  return music


def music_pulse():
  """Brighter, more rhythmic bed: A major, 100 bpm, soft four-on-the-floor kick with a pumping pad,
  a plucked motif that answers the voice, a sine bass on the roots. Resolves on a wide A major at 28 s."""
  bpm = 100; beat = 60/bpm
  chords = [
    (0, 3, [57, 61, 64, 69]),     # A
    (3, 6, [54, 61, 64, 69]),     # F#m7-ish
    (6, 9, [50, 57, 62, 66]),     # D
    (9, 12, [52, 59, 64, 68]),    # E
    (12, 16, [54, 61, 64, 69]),   # F#m
    (16, 19, [50, 57, 62, 66]),   # D
    (19, 23, [52, 59, 64, 68]),   # E (build)
    (23, 26, [57, 61, 64, 69]),   # A
    (26, 28, [50, 57, 62, 66]),   # D
    (28, 30, [57, 61, 64, 69, 73]),  # A wide
  ]
  m = np.zeros(N)
  for (a, b, notes) in chords:
    n = int((b-a+0.5)*SR); e = env_adsr(n, 0.4, 0.0, 1.0, 0.5); pad = np.zeros(n); tt = np.arange(n)/SR
    for mm in notes:
      f = midi(mm); pad += 0.6*saw(f, n, 0.004) + 0.6*saw(f, n, -0.003) + np.sin(2*np.pi*f*tt)
    pad = lowpass(pad*e, 1600 + (1400 if a >= 19 else 0)) * 0.03
    place(m, pad, a)
  # pump: duck the pad on every beat so it breathes with the kick
  pump = np.ones(N)
  for k in range(int(DUR/beat)):
    i = int(k*beat*SR); L = int(0.28*SR); pump[i:i+L] *= np.minimum(1, 0.45 + 0.55*(np.arange(min(L, N-i))/L))
  m *= pump
  # soft kick + sine bass
  for k in range(int(DUR/beat)):
    at = k*beat
    if at >= 28.4: break
    n = int(0.25*SR); tt = np.arange(n)/SR
    kick = np.sin(2*np.pi*(55 + 90*np.exp(-tt*40))*tt) * np.exp(-tt*14) * 0.3
    place(m, kick, at)
    c = [c for c in chords if c[0] <= at < c[1]]
    if c and k % 2 == 0:
      f = midi(c[0][2][0]-12); n2 = int(beat*0.9*SR); t2 = np.arange(n2)/SR
      place(m, np.sin(2*np.pi*f*t2)*env_adsr(n2, 0.01, 0.0, 1.0, 0.08)*0.16, at)
  # plucked motif: a repeating 8-note pattern on chord tones, answering the voice lines
  for k in range(int(DUR/(beat/2))):
    at = k*beat/2
    if at < 3 or at >= 28.4: continue
    c = [c for c in chords if c[0] <= at < c[1]][0]
    pat = [0, 2, 1, 3, 2, 1, 3, 0][k % 8]
    if (k % 8) in (5, 7) and at < 19: continue
    mm = c[2][pat % len(c[2])] + 12; f = midi(mm); n = int(0.45*SR); tt = np.arange(n)/SR
    g = 0.05 if at < 12 else (0.07 if at < 23 else 0.055)
    s_ = (np.sin(2*np.pi*f*tt) + 0.35*np.sin(2*np.pi*2*f*tt) + 0.15*np.sin(2*np.pi*3*f*tt)) * np.exp(-tt*8) * g
    place(m, s_, at)
  # airy high pad from 12 s, wider in the convergence
  for (a, b, g) in ((12, 19, 0.012), (19, 28, 0.02), (28, 30, 0.025)):
    n = int((b-a+0.4)*SR); e = env_adsr(n, 1.0, 0.0, 1.0, 0.4); tt = np.arange(n)/SR; hp = np.zeros(n)
    for mm in (76, 80, 83): hp += np.sin(2*np.pi*midi(mm)*tt*(1+0.002*np.sin(2*np.pi*0.3*tt)))
    place(m, lowpass(hp*e, 6000)*g, a)
  # riser into the hub and swell into the brand
  for (a, b, g) in ((19.3, 21.0, 0.05), (27.3, 28.1, 0.04)):
    n = int((b-a)*SR); noise = rng.standard_normal(n); sw = np.zeros(n)
    for i in range(0, n, 2400):
      seg = noise[i:i+2400]; fc = 300 + 2500*(i/n)**2; sw[i:i+2400] = bandpass(seg, fc, fc*2.2)
    place(m, sw*np.linspace(0, 1, n)**2*g, a)
  return lowpass(m, 10000)


def music_v2():
  """V2 bed: sparse opening, pulse from the question, build through the evaluation, lift at the
  convergence, resolve into the brand hold and breathe out. F# minor -> A major, 96 bpm."""
  bpm = 96; beat = 60/bpm
  chords = [
    (0, 3, [54, 61, 64]),           # F#m, sparse
    (3, 6, [50, 57, 61, 66]),       # D
    (6, 9, [57, 61, 64, 68]),       # A
    (9, 12, [52, 59, 64, 68]),      # E
    (12, 17, [54, 61, 64, 69]),     # F#m (evaluation, tension)
    (17, 22, [50, 57, 61, 66, 69]), # D wide (lift)
    (22, 25, [57, 61, 64, 68]),     # A
    (25, 27, [52, 59, 64, 68]),     # E
    (27, 30, [57, 61, 64, 69, 73]), # A wide, held
  ]
  m = np.zeros(N)
  for (a, b, notes) in chords:
    n = int((b-a+0.6)*SR); e = env_adsr(n, 0.6 if a else 1.6, 0.0, 1.0, 0.6); pad = np.zeros(n); tt = np.arange(n)/SR
    for mm in notes:
      f = midi(mm); pad += 0.5*saw(f, n, 0.004) + 0.5*saw(f, n, -0.003) + np.sin(2*np.pi*f*tt)
    bright = 700 if a < 6 else (1300 if a < 17 else 2600)
    pad = lowpass(pad*e, bright) * (0.025 if a < 6 else 0.03)
    place(m, pad, a)
  # pulse: soft sub on the beat from the question onward; a gentle kick from the evaluation
  for k in range(int(DUR/beat)):
    at = k*beat
    if at < 6 or at >= 27.2: continue
    c = [c for c in chords if c[0] <= at < c[1]][0]
    f = midi(c[2][0]-12); n = int(0.4*SR); tt = np.arange(n)/SR
    place(m, np.sin(2*np.pi*f*tt)*np.exp(-tt*7)*0.18, at)
    if at >= 12:
      kick = np.sin(2*np.pi*(55 + 80*np.exp(-tt*40))*tt) * np.exp(-tt*16) * (0.11 if at < 17 else 0.18)
      place(m, kick[:int(0.25*SR)], at)
  # pump the pad under the kick during the lift
  pump = np.ones(N)
  for k in range(int(DUR/beat)):
    at = k*beat
    if at < 17 or at >= 27: continue
    i = int(at*SR); L = int(0.3*SR); pump[i:i+L] *= np.minimum(1, 0.5 + 0.5*(np.arange(min(L, N-i))/L))
  m *= pump
  # arpeggio: enters at 9, thickens through the evaluation, sings in the convergence, rests on the brand
  for k in range(int(DUR/(beat/2))):
    at = k*beat/2
    if at < 9 or at >= 27.2: continue
    c = [c for c in chords if c[0] <= at < c[1]][0]
    pat = [0, 2, 1, 3, 2, 1, 3, 0][k % 8]
    dens = 0.5 if at < 12 else (0.75 if at < 17 else (1.0 if at < 22 else 0.6))
    if rng.random() > dens: continue
    mm = c[2][pat % len(c[2])] + 12; f = midi(mm); n = int(0.5*SR); tt = np.arange(n)/SR
    g = 0.045 if at < 17 else 0.065
    place(m, (np.sin(2*np.pi*f*tt) + 0.3*np.sin(2*np.pi*2*f*tt) + 0.12*np.sin(2*np.pi*3*f*tt))*np.exp(-tt*8)*g, at)
  # airy high layer in the lift and the hold
  for (a, b, g) in ((17, 27, 0.02), (27, 30, 0.028)):
    n = int((b-a+0.5)*SR); e = env_adsr(n, 1.2, 0.0, 1.0, 0.8); tt = np.arange(n)/SR; hp = np.zeros(n)
    for mm in (76, 81, 85): hp += np.sin(2*np.pi*midi(mm)*tt*(1+0.002*np.sin(2*np.pi*0.3*tt)))
    place(m, lowpass(hp*e, 6000)*g, a)
  # risers: into the convergence (15.6 -> 17) and into the brand (26.3 -> 27)
  for (a, b, g) in ((15.6, 17.0, 0.05), (26.3, 27.0, 0.035)):
    n = int((b-a)*SR); noise = rng.standard_normal(n); sw = np.zeros(n)
    for i in range(0, n, 2400):
      seg = noise[i:i+2400]; fc = 300 + 2500*(i/n)**2; sw[i:i+2400] = bandpass(seg, fc, fc*2.2)
    place(m, sw*np.linspace(0, 1, n)**2*g, a)
  return lowpass(m, 10000)


def music_v3():
  """20 s bed for the short cut: same language as v2 on a tighter timeline. Sparse for the question,
  pulse from the AIs, build through the analysis, lift at the convergence, held chord from the brand."""
  bpm = 96; beat = 60/bpm
  chords = [
    (0, 2.6, [54, 61, 64]),           # F#m, sparse
    (2.6, 5.2, [50, 57, 61, 66]),     # D
    (5.2, 7.6, [57, 61, 64, 68]),     # A
    (7.6, 10.2, [52, 59, 64, 68]),    # E
    (10.2, 13.0, [54, 61, 64, 69]),   # F#m (analysis)
    (13.0, 14.8, [50, 57, 61, 66, 69]),  # D wide (lift)
    (14.8, 17.0, [57, 61, 64, 68]),   # A
    (17.0, 20.0, [57, 61, 64, 69, 73]),  # A wide, held
  ]
  m = np.zeros(N)
  for (a, b, notes) in chords:
    n = int((b-a+0.6)*SR); e = env_adsr(n, 0.5 if a else 1.2, 0.0, 1.0, 0.6); pad = np.zeros(n); tt = np.arange(n)/SR
    for mm in notes:
      f = midi(mm); pad += 0.5*saw(f, n, 0.004) + 0.5*saw(f, n, -0.003) + np.sin(2*np.pi*f*tt)
    bright = 700 if a < 2.6 else (1300 if a < 13 else 2600)
    pad = lowpass(pad*e, bright) * (0.025 if a < 2.6 else 0.03)
    place(m, pad, a)
  for k in range(int(DUR/beat)):
    at = k*beat
    if at < 2.6 or at >= 17.2: continue
    c = [c for c in chords if c[0] <= at < c[1]][0]
    f = midi(c[2][0]-12); n = int(0.4*SR); tt = np.arange(n)/SR
    place(m, np.sin(2*np.pi*f*tt)*np.exp(-tt*7)*0.18, at)
    if at >= 7.6:
      kick = np.sin(2*np.pi*(55 + 80*np.exp(-tt*40))*tt) * np.exp(-tt*16) * (0.11 if at < 13 else 0.18)
      place(m, kick[:int(0.25*SR)], at)
  pump = np.ones(N)
  for k in range(int(DUR/beat)):
    at = k*beat
    if at < 13 or at >= 17: continue
    i = int(at*SR); L = int(0.3*SR); pump[i:i+L] *= np.minimum(1, 0.5 + 0.5*(np.arange(min(L, N-i))/L))
  m *= pump
  for k in range(int(DUR/(beat/2))):
    at = k*beat/2
    if at < 5.2 or at >= 17.2: continue
    c = [c for c in chords if c[0] <= at < c[1]][0]
    pat = [0, 2, 1, 3, 2, 1, 3, 0][k % 8]
    dens = 0.5 if at < 7.6 else (0.75 if at < 13 else (1.0 if at < 14.8 else 0.6))
    if rng.random() > dens: continue
    mm = c[2][pat % len(c[2])] + 12; f = midi(mm); n = int(0.5*SR); tt = np.arange(n)/SR
    g = 0.045 if at < 13 else 0.065
    place(m, (np.sin(2*np.pi*f*tt) + 0.3*np.sin(2*np.pi*2*f*tt) + 0.12*np.sin(2*np.pi*3*f*tt))*np.exp(-tt*8)*g, at)
  for (a, b, g) in ((13, 17, 0.02), (17, 20, 0.028)):
    n = int((b-a+0.5)*SR); e = env_adsr(n, 1.0, 0.0, 1.0, 0.8); tt = np.arange(n)/SR; hp = np.zeros(n)
    for mm in (76, 81, 85): hp += np.sin(2*np.pi*midi(mm)*tt*(1+0.002*np.sin(2*np.pi*0.3*tt)))
    place(m, lowpass(hp*e, 6000)*g, a)
  for (a, b, g) in ((11.8, 13.0, 0.05), (16.3, 17.0, 0.035)):
    n = int((b-a)*SR); noise = rng.standard_normal(n); sw = np.zeros(n)
    for i in range(0, n, 2400):
      seg = noise[i:i+2400]; fc = 300 + 2500*(i/n)**2; sw[i:i+2400] = bandpass(seg, fc, fc*2.2)
    place(m, sw*np.linspace(0, 1, n)**2*g, a)
  return lowpass(m, 10000)


def music_conv():
  """22 s bed for the Convergence brief: atmospheric tension with digital pulses, a warm copper impact
  when Switchboard appears, a build from the responses into the convergence, a clean landing on the answer,
  and a short held chord under the brand. F# minor to A major, 100 bpm."""
  bpm = 100; beat = 60/bpm
  chords = [
    (0, 3, [54, 61, 64]), (3, 6, [50, 57, 61, 66]), (6, 9, [57, 61, 64, 68]), (9, 12, [52, 59, 64, 68]),
    (12, 15, [54, 61, 64, 69]), (15, 19, [50, 57, 61, 66, 69]), (19, 21, [57, 61, 64, 68]), (21, 22, [57, 61, 64, 69, 73]),
  ]
  m = np.zeros(N)
  for (a, b, notes) in chords:
    n = int((b-a+0.6)*SR); e = env_adsr(n, 0.4 if a else 1.0, 0.0, 1.0, 0.6); pad = np.zeros(n); tt = np.arange(n)/SR
    for mm in notes:
      f = midi(mm); pad += 0.5*saw(f, n, 0.004) + 0.5*saw(f, n, -0.003) + np.sin(2*np.pi*f*tt)
    bright = 600 if a < 3 else (1300 if a < 15 else 2600)
    pad = lowpass(pad*e, bright) * (0.022 if a < 3 else 0.03)
    place(m, pad, a)
  # digital pulses in the opening: filtered ticks on the off-beats
  for k in range(int(3/(beat/2))):
    at = k*beat/2 + 0.2; n = int(0.12*SR); tt = np.arange(n)/SR
    place(m, bandpass(rng.standard_normal(n), 1800, 2600)*np.exp(-tt*60)*0.05, at)
  # copper impact at 3.0: low boom plus a soft swell
  n = int(1.6*SR); tt = np.arange(n)/SR
  place(m, np.sin(2*np.pi*(48 + 30*np.exp(-tt*8))*tt)*np.exp(-tt*2.2)*0.28, 3.0)
  place(m, lowpass(rng.standard_normal(n), 900)*np.exp(-tt*4)*0.08, 3.0)
  # sub pulse from the question, soft kick from the responses, pumping pad in the convergence
  for k in range(int(DUR/beat)):
    at = k*beat
    if at < 3 or at >= 20.6: continue
    c = [c for c in chords if c[0] <= at < c[1]][0]
    f = midi(c[2][0]-12); n = int(0.4*SR); tt = np.arange(n)/SR
    place(m, np.sin(2*np.pi*f*tt)*np.exp(-tt*7)*0.17, at)
    if 12 <= at < 19:
      kick = np.sin(2*np.pi*(55 + 80*np.exp(-tt*40))*tt) * np.exp(-tt*16) * (0.11 if at < 15 else 0.18)
      place(m, kick[:int(0.25*SR)], at)
  pump = np.ones(N)
  for k in range(int(DUR/beat)):
    at = k*beat
    if at < 15 or at >= 19: continue
    i = int(at*SR); L = int(0.3*SR); pump[i:i+L] *= np.minimum(1, 0.5 + 0.5*(np.arange(min(L, N-i))/L))
  m *= pump
  # arpeggio: from the prompt, thicker through the responses, singing in the convergence, out for the answer
  for k in range(int(DUR/(beat/2))):
    at = k*beat/2
    if at < 6 or at >= 19: continue
    c = [c for c in chords if c[0] <= at < c[1]][0]
    pat = [0, 2, 1, 3, 2, 1, 3, 0][k % 8]
    dens = 0.45 if at < 12 else (0.75 if at < 15 else 1.0)
    if rng.random() > dens: continue
    mm = c[2][pat % len(c[2])] + 12; f = midi(mm); n = int(0.5*SR); tt = np.arange(n)/SR
    g = 0.045 if at < 15 else 0.065
    place(m, (np.sin(2*np.pi*f*tt) + 0.3*np.sin(2*np.pi*2*f*tt) + 0.12*np.sin(2*np.pi*3*f*tt))*np.exp(-tt*8)*g, at)
  # airy high layer in the convergence and the hold
  for (a, b, g) in ((15, 19, 0.02), (19, 22, 0.024)):
    n = int((b-a+0.5)*SR); e = env_adsr(n, 1.0, 0.0, 1.0, 0.6); tt = np.arange(n)/SR; hp = np.zeros(n)
    for mm in (76, 81, 85): hp += np.sin(2*np.pi*midi(mm)*tt*(1+0.002*np.sin(2*np.pi*0.3*tt)))
    place(m, lowpass(hp*e, 6000)*g, a)
  # cinematic rise 15 -> 19.6
  n = int(4.6*SR); noise = rng.standard_normal(n); sw = np.zeros(n)
  for i in range(0, n, 2400):
    seg = noise[i:i+2400]; fc = 250 + 2600*(i/n)**2; sw[i:i+2400] = bandpass(seg, fc, fc*2.2)
  place(m, sw*np.linspace(0, 1, n)**2.2*0.06, 15.0)
  return lowpass(m, 10000)


def music_final():
  """28 s bed for Commercial V3: the conv bed's language on the longer timeline. Atmosphere and digital
  accents under the hook, copper impact at the reveal, build through the responses, a long rise through
  the five-second convergence, a clean landing on the answer, a held chord under the brand."""
  bpm = 100; beat = 60/bpm
  chords = [
    (0, 4, [54, 61, 64]), (4, 8, [50, 57, 61, 66]), (8, 11, [57, 61, 64, 68]), (11, 14, [52, 59, 64, 68]),
    (14, 18, [54, 61, 64, 69]), (18, 23, [50, 57, 61, 66, 69]), (23, 26, [57, 61, 64, 68]), (26, 28, [57, 61, 64, 69, 73]),
  ]
  m = np.zeros(N)
  for (a, b, notes) in chords:
    n = int((b-a+0.6)*SR); e = env_adsr(n, 0.4 if a else 1.2, 0.0, 1.0, 0.6); pad = np.zeros(n); tt = np.arange(n)/SR
    for mm in notes:
      f = midi(mm); pad += 0.5*saw(f, n, 0.004) + 0.5*saw(f, n, -0.003) + np.sin(2*np.pi*f*tt)
    bright = 600 if a < 4 else (1300 if a < 18 else 2600)
    pad = lowpass(pad*e, bright) * (0.022 if a < 4 else 0.03)
    place(m, pad, a)
  for k in range(int(4/(beat/2))):
    at = k*beat/2 + 0.2; n = int(0.12*SR); tt = np.arange(n)/SR
    place(m, bandpass(rng.standard_normal(n), 1800, 2600)*np.exp(-tt*60)*0.05, at)
  n = int(1.6*SR); tt = np.arange(n)/SR
  place(m, np.sin(2*np.pi*(48 + 30*np.exp(-tt*8))*tt)*np.exp(-tt*2.2)*0.28, 4.0)
  place(m, lowpass(rng.standard_normal(n), 900)*np.exp(-tt*4)*0.08, 4.0)
  for k in range(int(DUR/beat)):
    at = k*beat
    if at < 4 or at >= 25.6: continue
    c = [c for c in chords if c[0] <= at < c[1]][0]
    f = midi(c[2][0]-12); n = int(0.4*SR); tt = np.arange(n)/SR
    place(m, np.sin(2*np.pi*f*tt)*np.exp(-tt*7)*0.17, at)
    if 14 <= at < 23:
      kick = np.sin(2*np.pi*(55 + 80*np.exp(-tt*40))*tt) * np.exp(-tt*16) * (0.11 if at < 18 else 0.18)
      place(m, kick[:int(0.25*SR)], at)
  pump = np.ones(N)
  for k in range(int(DUR/beat)):
    at = k*beat
    if at < 18 or at >= 23: continue
    i = int(at*SR); L = int(0.3*SR); pump[i:i+L] *= np.minimum(1, 0.5 + 0.5*(np.arange(min(L, N-i))/L))
  m *= pump
  for k in range(int(DUR/(beat/2))):
    at = k*beat/2
    if at < 8 or at >= 23: continue
    c = [c for c in chords if c[0] <= at < c[1]][0]
    pat = [0, 2, 1, 3, 2, 1, 3, 0][k % 8]
    dens = 0.45 if at < 14 else (0.75 if at < 18 else 1.0)
    if rng.random() > dens: continue
    mm = c[2][pat % len(c[2])] + 12; f = midi(mm); n = int(0.5*SR); tt = np.arange(n)/SR
    g = 0.045 if at < 18 else 0.065
    place(m, (np.sin(2*np.pi*f*tt) + 0.3*np.sin(2*np.pi*2*f*tt) + 0.12*np.sin(2*np.pi*3*f*tt))*np.exp(-tt*8)*g, at)
  for (a, b, g) in ((18, 23, 0.02), (23, 28, 0.024)):
    n = int((b-a+0.5)*SR); e = env_adsr(n, 1.0, 0.0, 1.0, 0.6); tt = np.arange(n)/SR; hp = np.zeros(n)
    for mm in (76, 81, 85): hp += np.sin(2*np.pi*midi(mm)*tt*(1+0.002*np.sin(2*np.pi*0.3*tt)))
    place(m, lowpass(hp*e, 6000)*g, a)
  n = int(5.6*SR); noise = rng.standard_normal(n); sw = np.zeros(n)
  for i in range(0, n, 2400):
    seg = noise[i:i+2400]; fc = 250 + 2600*(i/n)**2; sw[i:i+2400] = bandpass(seg, fc, fc*2.2)
  place(m, sw*np.linspace(0, 1, n)**2.2*0.06, 18.0)
  return lowpass(m, 10000)

music = {"pad": music_pad, "pulse": music_pulse, "v2": music_v2, "v3": music_v3, "conv": music_conv, "final": music_final}[ARGS.music]()
# tail: fade out so the cut is clean (longer, breathing fade on the V2 bed)
_tail = int((1.6 if ARGS.music in ('v2', 'v3') else (0.9 if ARGS.music in ('conv', 'final') else 0.6))*SR); music[-_tail:] *= np.linspace(1, 0, _tail)**1.5

# ---- sfx (cue times follow the edit: V1 scene times, or the V2 timeline)
V2 = ARGS.music == 'v2'; V3 = ARGS.music == 'v3'; CONV = ARGS.music in ('conv', 'final'); FINAL = ARGS.music == 'final'
sfx = np.zeros(N)
# typing under the prompt bar
at = 0.45 if V3 else 3.55
while at < (1.55 if V3 else 4.9):
    n = int(0.03*SR); s = bandpass(rng.standard_normal(n), 1800, 5200) * np.exp(-np.arange(n)/SR*180) * 0.5
    place(sfx, s, at); at += rng.uniform(0.032, 0.058)
# second typing pass for the improved prompt (quieter, faster)
at = 6.9
while at < (6.9 if V3 else (7.0 if V2 else 8.1)):
    n = int(0.025*SR); s = bandpass(rng.standard_normal(n), 2200, 6000) * np.exp(-np.arange(n)/SR*220) * 0.28
    place(sfx, s, at); at += rng.uniform(0.022, 0.04)
# submit chime 5.15
n = int(1.2*SR); tt = np.arange(n)/SR
chime = (np.sin(2*np.pi*880*tt)*np.exp(-tt*5) + 0.7*np.sin(2*np.pi*1318.5*tt)*np.exp(-tt*4) + 0.3*np.sin(2*np.pi*2637*tt)*np.exp(-tt*7)) * 0.2
chime[:int(0.004*SR)] *= np.linspace(0, 1, int(0.004*SR)); place(sfx, chime, 1.75 if V3 else 5.15)
# teal highlight sweep 8.05: soft airy whoosh
def whoosh(dur, lo, hi, gain):
    n = int(dur*SR); x = bandpass(rng.standard_normal(n), lo, hi); e = np.sin(np.linspace(0, np.pi, n))**1.5; return x*e*gain
place(sfx, whoosh(0.9, 1200, 4000, 0.15), 6.0 if V3 else (7.2 if V2 else 8.0))
# airy transitions on the light sweeps
for s0 in ((5.2, 10.2, 13.0, 17.0) if V3 else ((9, 12, 17, 22, 25, 27) if V2 else (3, 9, 16, 23, 28))): place(sfx, whoosh(0.7, 500, 2500, 0.17), s0 - 0.1)
# card / glow pops: tiny soft ticks
for at in ((3.3, 3.7, 4.1, 6.0, 6.3, 6.6, 7.9, 8.4, 8.9, 10.8, 11.3, 11.9, 15.2, 15.5, 15.8) if V3 else (7.25, 7.55, 7.85, 9.8, 10.3, 10.8, 12.5, 13.3, 15.0, 15.6, 19.6, 19.9, 20.2, 20.5, 22.6, 22.95, 23.3) if V2 else (9.75, 10.05, 10.35, 12.4, 12.9, 13.4, 16.45, 16.85, 17.25, 17.65, 21.1, 21.35, 21.6, 21.85, 23.9, 24.2, 24.5, 24.8)):
    n = int(0.12*SR); tt = np.arange(n)/SR; f = 1500 if at < 21 else 2100
    s = np.sin(2*np.pi*f*tt)*np.exp(-tt*40)*(0.07 if V2 else 0.12); place(sfx, s, at)
# convergence shimmer 19.3 -> 22.5: sparkling pings over a rising air
for i in range(70):
    at = (13.1 if V3 else (17.3 if V2 else 19.3)) + (1.6 if V3 else 3.0)*rng.random()**0.8; f = rng.uniform(1800, 6500); n = int(0.5*SR); tt = np.arange(n)/SR
    s = np.sin(2*np.pi*f*tt)*np.exp(-tt*10)*0.05*(0.4 + 0.6*(at-19.3)/3); place(sfx, s, at)
place(sfx, whoosh(1.6 if V3 else 2.2, 2000, 8000, 0.08), 13.1 if V3 else (17.4 if V2 else 19.4))
# brand resolve 28.0: warm bell + shimmer, settled by 28.5
n = int(2.0*SR); tt = np.arange(n)/SR
bell = (np.sin(2*np.pi*587.3*tt)*np.exp(-tt*2.2) + 0.5*np.sin(2*np.pi*1174.7*tt)*np.exp(-tt*3) + 0.25*np.sin(2*np.pi*1760*tt)*np.exp(-tt*4)) * 0.16
_b = 17.0 if V3 else (27.0 if V2 else 28.0)
place(sfx, bell, _b); place(sfx, whoosh(0.6, 2500, 9000, 0.1), _b)
sfx = lowpass(sfx, 12000)

if CONV:
  sfx = np.zeros(N)
  T = (lambda c, f: f if FINAL else c)
  # typing
  at = T(3.5, 4.9)
  while at < T(5.4, 7.0):
    n = int(0.03*SR); place(sfx, bandpass(rng.standard_normal(n), 1800, 5200)*np.exp(-np.arange(n)/SR*180)*0.45, at); at += rng.uniform(0.03, 0.05)
  # digital transformation at 6.6: a quick rising sparkle and an airy sweep
  for i in range(14):
    at = T(6.6, 8.7) + i*0.045; f = 1200*2**(i/7); n = int(0.25*SR); tt = np.arange(n)/SR
    place(sfx, np.sin(2*np.pi*f*tt)*np.exp(-tt*18)*0.06, at)
  place(sfx, whoosh(0.8, 1500, 6000, 0.12), T(6.5, 8.6))
  # subtle digital accents as the windows come forward in the hook
  if FINAL:
    for at in (0.5, 1.1, 1.7, 2.3):
      n = int(0.3*SR); tt = np.arange(n)/SR; place(sfx, bandpass(rng.standard_normal(n), 2500, 5000)*np.exp(-tt*30)*0.05 + np.sin(2*np.pi*1760*tt)*np.exp(-tt*25)*0.03, at)
  # three activation tones, distinct pitches, with the model lights
  for at, f in ((T(9.9, 11.9), 659.3), (T(10.3, 12.3), 783.9), (T(10.7, 12.7), 987.8)):
    n = int(0.7*SR); tt = np.arange(n)/SR
    place(sfx, (np.sin(2*np.pi*f*tt) + 0.4*np.sin(2*np.pi*2*f*tt))*np.exp(-tt*6)*0.16, at)
  # three completion hits: DUM. DUM. DUM.
  for at in ((14.6, 15.6, 16.6) if FINAL else (12.3, 13.1, 13.9)):
    n = int(0.5*SR); tt = np.arange(n)/SR
    thump = np.sin(2*np.pi*(70 + 60*np.exp(-tt*30))*tt)*np.exp(-tt*12)*0.5
    tone = np.sin(2*np.pi*440*tt)*np.exp(-tt*14)*0.12
    place(sfx, thump + tone, at)
  # convergence shimmer and rise 16.6 -> 19
  for i in range(60):
    L = T(2.3, 2.8); at = T(16.6, 20.2) + L*rng.random()**0.8; f = rng.uniform(1800, 6500); n = int(0.5*SR); tt = np.arange(n)/SR
    place(sfx, np.sin(2*np.pi*f*tt)*np.exp(-tt*10)*0.045*(0.4 + 0.6*(at-T(16.6, 20.2))/L), at)
  place(sfx, whoosh(T(2.4, 2.9), 2000, 8000, 0.08), T(16.6, 20.2))
  # the ding at 19.8
  n = int(1.8*SR); tt = np.arange(n)/SR
  ding = (np.sin(2*np.pi*1318.5*tt)*np.exp(-tt*3.5) + 0.6*np.sin(2*np.pi*2637*tt)*np.exp(-tt*5) + 0.3*np.sin(2*np.pi*3951*tt)*np.exp(-tt*7) + 0.35*np.sin(2*np.pi*659.3*tt)*np.exp(-tt*3)) * 0.42
  ding[:int(0.003*SR)] *= np.linspace(0, 1, int(0.003*SR)); place(sfx, ding, T(19.8, 23.9))
  # sonic logo at 21.0: three quick notes landing on a warm bell
  for i, (f, dt) in enumerate(((587.3, 0.0), (880.0, 0.12), (1174.7, 0.24))):
    n = int(1.4*SR); tt = np.arange(n)/SR
    place(sfx, (np.sin(2*np.pi*f*tt) + 0.3*np.sin(2*np.pi*2*f*tt))*np.exp(-tt*(2.5 if i == 2 else 9))*0.2, T(21.0, 26.0) + dt)
  place(sfx, whoosh(0.6, 2500, 9000, 0.08), T(21.0, 26.0))
  sfx = lowpass(sfx, 12000)

# ---- voiceover placement (scene cue + a breath), with a gentle speed-up on the two tight lines
c8, c9, c10 = (float(x) for x in ARGS.late_cues.split(","))
cues = {1: 0.3, 2: 3.2, 3: 6.2, 4: 9.2, 5: 12.2, 6: 16.2, 7: 19.2, 8: c8, 9: c9, 10: c10}
if ARGS.cues: cues = {i+1: float(x) for i, x in enumerate(ARGS.cues.split(','))}
speed = {int(k): float(v) for k, v in (kv.split(":") for kv in ARGS.speed.split(",") if kv)}
vo = np.zeros(N)
for k, at in cues.items():
    if not (vo_dir/f"vo{k:02d}.wav").exists(): continue
    a, sr = sf.read(vo_dir/f"vo{k:02d}.wav", dtype="float32")
    if a.ndim > 1: a = a.mean(axis=1)
    if sr != SR: a = signal.resample_poly(a, SR, sr)
    if k in speed:  # resample-based speed change keeps it simple; the shift is tiny
        n2 = int(len(a)/speed[k]); a = signal.resample(a, n2)
    a = a / (np.abs(a).max() + 1e-9) * ARGS.vo_gain
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
sf.write(out_dir/f"mix-vo{ARGS.suffix}.wav", mix_vo.astype(np.float32), SR)
sf.write(out_dir/f"mix-novo{ARGS.suffix}.wav", mix_novo.astype(np.float32), SR)
print("music rms dB", 20*np.log10(np.sqrt(np.mean(bed**2))+1e-9), "vo rms dB", 20*np.log10(np.sqrt(np.mean(vo[vo!=0]**2))+1e-9))
