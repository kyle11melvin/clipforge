# British voiceover with Kokoro directly: blended voice styles and a softening chain (de-ess, low-pass,
# warmth shelf, gentle compression, a small room), because the raw output read as harsh on the phone.
# usage: vo_kokoro.py "bf_emma:0.3,bf_lily:0.7" out_dir lines.txt [speed]
import sys, numpy as np, soundfile as sf
from pathlib import Path
from scipy import signal
from kokoro_onnx import Kokoro
spec, out, lines = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]); speed = float(sys.argv[4]) if len(sys.argv) > 4 else 0.9
out.mkdir(parents=True, exist_ok=True)
k = Kokoro("/root/.cache/hyperframes/tts/models/kokoro-v1.0.onnx", "/root/.cache/hyperframes/tts/voices/voices-v1.0.bin")
style = sum(float(w)*k.get_voice_style(v) for v, w in (kv.split(":") for kv in spec.split(",")))
def bp(x, lo, hi, sr): b, a = signal.butter(2, [lo/(sr/2), hi/(sr/2)], btype="band"); return signal.lfilter(b, a, x)
def lp(x, fc, sr): b, a = signal.butter(2, fc/(sr/2)); return signal.lfilter(b, a, x)
def soften(a, sr):
    rng = np.random.default_rng(3)
    # de-ess: duck the 5-9.5 kHz band when it gets hot, and trim it a little always
    band = bp(a, 5000, 9500, sr); rest = a - band
    env = np.sqrt(signal.lfilter(*signal.butter(1, 40/(sr/2)), band**2)) + 1e-9
    thr = np.percentile(env, 70); gain = np.minimum(1.0, (thr/env)**0.6)
    a = rest + band*gain*0.65
    a = lp(a, 11000, sr)
    a = a + 0.35*lp(a, 220, sr)                      # warmth
    env = np.sqrt(signal.lfilter(*signal.butter(1, 12/(sr/2)), a**2)) + 1e-9   # gentle 2:1 above -18 dB
    over = np.maximum(env/0.125, 1.0); a = a / np.sqrt(over)
    room = np.zeros(int(0.28*sr)); 
    for d, g in ((0.007, 0.22), (0.013, 0.16), (0.023, 0.12), (0.031, 0.09)): room[int(d*sr)] += g
    tail = rng.standard_normal(len(room)) * np.exp(-np.arange(len(room))/sr*22) * 0.012; room += lp(tail, 5000, sr)
    a = a + signal.fftconvolve(a, room)[:len(a)]
    return a / (np.abs(a).max() + 1e-9) * 0.9
for ln in lines.read_text().strip().splitlines():
    n, text = ln.split("|", 1)
    a, sr = k.create(text, voice=style, speed=speed, lang="en-gb")
    a = soften(a.astype(np.float64), sr)
    sf.write(str(out/f"vo{n}.wav"), a.astype(np.float32), sr); print(n, round(len(a)/sr, 2))
