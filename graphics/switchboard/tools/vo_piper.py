# Voiceover lines with the Australian-English Piper model (DataCraftsmanAustralia/piper-en_AU-librivox-medium).
# usage: vo_piper.py model.onnx speaker_id out_dir [lines.txt]
import sys, wave
from pathlib import Path
from piper import PiperVoice, SynthesisConfig
model, spk, out = sys.argv[1], int(sys.argv[2]), Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=True)
LS = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
TRIES = int(sys.argv[6]) if len(sys.argv) > 6 else 1  # VITS durations vary per run; keep the shortest of several takes
lines = Path(sys.argv[4] if len(sys.argv) > 4 else "videos/switchboard/vo/lines.txt").read_text().strip().splitlines()
voice = PiperVoice.load(model)
cfg = SynthesisConfig(speaker_id=spk, length_scale=LS, noise_scale=0.5, noise_w_scale=0.6)
for ln in lines:
    n, text = ln.split("|", 1)
    import numpy as np, soundfile as sf
    best = None
    for _ in range(TRIES):
        chunks = list(voice.synthesize(text, cfg)); sr = chunks[0].sample_rate
        cand = np.concatenate([c.audio_float_array for c in chunks])
        if best is None or len(cand) < len(best): best = cand
    a = best
    # trim leading/trailing silence and cap pauses inside the line at 0.35 s
    thr = 0.02; w = int(0.02*sr)
    env = np.sqrt(np.convolve(a**2, np.ones(w)/w, mode="same"))
    loud = env > thr
    idx = np.where(loud)[0]; a = a[max(0, idx[0]-int(0.05*sr)):min(len(a), idx[-1]+int(0.12*sr))]
    env = np.sqrt(np.convolve(a**2, np.ones(w)/w, mode="same")); loud = env > thr
    keep = np.ones(len(a), bool); run = 0
    for i in range(len(a)):
        run = run + 1 if not loud[i] else 0
        if run > int(0.22*sr): keep[i] = False
    a = a[keep]
    sf.write(str(out/f"vo{n}.wav"), a.astype(np.float32), sr)
    print(n, round(len(a)/sr, 2))
print("done", spk)
