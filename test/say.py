import sys, soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro(".tts/kokoro-v1.0.onnx", ".tts/voices-v1.0.bin")
text, out = sys.argv[1], sys.argv[2]
samples, sr = k.create(text, voice="am_michael", speed=1.0, lang="en-us")
sf.write(out, samples, sr)
print(out, len(samples)/sr)
