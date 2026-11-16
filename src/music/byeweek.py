# Sound design for the bye-week meme, numpy only (no scipy in the session): a soft pad under the recliner,
# a scratch-stop at the cut, monitor beeps that accelerate with the on-screen BPM, a low drone and a red-pulse thump,
# then a warm chord swell under the baby frame. python3 -I src/music/byeweek.py out.wav
import sys, wave, numpy as np
SR = 44100; T2, T3, END = 2.6, 6.6, 10.0; N = int(END * SR)
L = np.zeros(N); R = np.zeros(N); rng = np.random.default_rng(3)
def add(at, sig, g=1.0, pan=0.0):
    i = int(at * SR); sig = sig[: max(0, N - i)]
    L[i:i + len(sig)] += sig * g * np.cos((pan + 1) * np.pi / 4); R[i:i + len(sig)] += sig * g * np.sin((pan + 1) * np.pi / 4)
def tone(f, dur, a=0.005, d=0.2):
    t = np.arange(int(dur * SR)) / SR
    env = np.minimum(1, t / a) * np.exp(-np.maximum(0, t - a) / d)
    return np.sin(2 * np.pi * f * t) * env
def pad(freqs, dur, att=0.8, rel=1.0):
    t = np.arange(int(dur * SR)) / SR
    x = sum(np.sin(2 * np.pi * f * t * (1 + d)) for f in freqs for d in (-0.003, 0, 0.003)) / (3 * len(freqs))
    return x * np.minimum(1, t / att) * np.minimum(1, np.maximum(0, (dur - t) / rel))
def noise(dur, lo=0.0):
    return rng.standard_normal(int(dur * SR)) * 0.5
# 1. recliner: a soft major pad, fading out at the cut
add(0, pad([261.6, 329.6, 392.0], T2 + 0.1, 0.6, 0.25), 0.12)
# 2. the cut: a short noise hit (scratch-stop), then a rising drone + monitor beeps that speed up with the BPM
x = noise(0.25) * np.exp(-np.arange(int(0.25 * SR)) / SR * 18); add(T2, x, 0.5)
t = np.arange(int((T3 - T2) * SR)) / SR; p = t / (T3 - T2)
drone = np.sin(2 * np.pi * (55 + 25 * p) * t) * (0.15 + 0.35 * p); add(T2, drone, 0.5)
tt = T2; k = 0
while tt < T3 - 0.05:
    pp = (tt - T2) / (T3 - T2); bpm = 80 + 110 * (1 - (1 - pp) ** 3)
    add(tt, tone(1320, 0.07, 0.002, 0.03), 0.22 + 0.2 * pp, pan=0.3)           # monitor beep
    thump = tone(60, 0.25, 0.002, 0.09); add(tt, thump, 0.5 + 0.5 * pp)        # red-pulse thump
    tt += 60 / bpm; k += 1
# flatline-ish buzzer at the end of the chaos, cut hard at T3
add(T3 - 0.35, tone(880, 0.35, 0.002, 0.5), 0.25)
# 3. the baby: warm swell, holds to the end and fades
add(T3, pad([196.0, 246.9, 293.7, 392.0], END - T3, 1.2, 1.4), 0.22)
add(T3 + 0.4, tone(1568, 1.2, 0.01, 0.5), 0.08, pan=-0.3)
x = np.stack([L, R], 1); x = np.tanh(x * 1.3) / np.tanh(1.3); x = x / max(1e-9, np.abs(x).max()) * 0.85
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype(np.int16).tobytes())
print("wrote", sys.argv[1], k, "beats")
