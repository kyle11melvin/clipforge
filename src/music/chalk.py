#!/usr/bin/env python3
"""Chalkboard sound effects, synthesised (numpy + scipy, no samples).

  python3 -I src/music/chalk.py <out.wav> <events.json> --dur 30.8

events.json is a list of {"type", "t", "d", ...} in seconds of the picture:
  write    chalk lettering: grainy strokes in a handwriting rhythm (four or five a second, no click per letter)
  stroke   one continuous chalk line (a circle, an underline, an arrow)
  erase    a felt eraser: two soft back-and-forth rubs
  whoosh   air, for something flying in
  thud     a soft knock, for the board landing or a stamp hitting

Kyle, 2026-11-12: "writing on the chalkboard to make sounds like you're writing on a chalkboard, and the eraser to
make a noise."
"""
import json, sys
import numpy as np
from scipy import signal
from scipy.io import wavfile

SR = 48000
a = sys.argv[1:]; out, ev_path = a[0], a[1]
DUR = float(a[a.index("--dur") + 1]) if "--dur" in a else 30.0
N = int(DUR * SR)
mix = np.zeros(N + SR)
rng = np.random.default_rng(12)


def band(x, lo, hi, order=2):
    sos = signal.butter(order, [lo, hi], btype="band", fs=SR, output="sos")
    return signal.sosfilt(sos, x)


def put(t, x, gain=1.0):
    i = int(t * SR)
    if i < 0 or i >= N: return
    x = x[: len(mix) - i]
    mix[i:i + len(x)] += x * gain


def lowpass(x, hz):
    return signal.sosfilt(signal.butter(2, hz, btype="low", fs=SR, output="sos"), x)


def scrape(d, speed=1.0):
    """One chalk stroke. Chalk on a board is a dry, grainy hiss whose loudness and brightness follow the speed of the
    hand: it swells through the middle of the stroke and dies at the ends. The grain is irregular (random flutter),
    never a steady buzz, and there is no click at the start. Round one had a tap per letter and a sawtooth chatter,
    and Kyle heard typing (2026-11-12: "sounds like annoying and typing not chalk board writing")."""
    # Round three (Kyle: "make it smooth, not scratching nails on a chalkboard"): nothing above ~1.8 kHz, no resonant
    # ring, slow soft edges. A muffled brush of soft chalk, closer to felt on slate than to a scrape.
    n = max(int(d * SR), 512)
    t = np.arange(n) / SR
    v = np.sin(np.pi * np.clip(t / d, 0, 1))                             # hand speed: swell and fade, no hard start
    # Round four (Kyle: "i want to hear the chalk just dont make it high pitch like earlier"): the muffled version was
    # too quiet to notice. Body up to ~2.6 kHz so it reads as chalk on a phone speaker, still nothing bright, and
    # write/stroke events are mixed louder than the other effects.
    x = lowpass(band(rng.standard_normal(n), 380, 2400, order=2), 2800)
    flutter = lowpass(rng.standard_normal(n), 40); flutter = 0.8 + 0.2 * flutter / (np.abs(flutter).max() + 1e-9)
    return x * flutter * v ** 1.2 * (0.85 + 0.15 * speed)


def touch():
    """Chalk meeting the board: a dull, quiet knock, used sparingly."""
    n = int(0.04 * SR); t = np.arange(n) / SR
    return lowpass(rng.standard_normal(n), 900) * np.exp(-t * 120) * 0.6 + np.sin(2 * np.pi * 170 * t) * np.exp(-t * 90) * 0.4


def ev_write(e):
    """Handwriting rhythm, not one hit per letter: about three soft strokes a second that run into each other."""
    t, end = e["t"], e["t"] + e["d"]
    first = True
    while t < end - 0.06:
        ln = min(rng.uniform(0.2, 0.42), end - t)
        put(t, scrape(ln, speed=rng.uniform(0.7, 1.2)), rng.uniform(1.0, 1.3))
        t += ln * 0.85 + rng.uniform(0.0, 0.05)                           # strokes overlap a little: one flowing hand
        first = False


def ev_stroke(e):
    put(e["t"], scrape(e["d"], speed=1.1), 1.2)


def ev_erase(e):
    t, d = e["t"], e["d"]
    for k, (off, ln) in enumerate([(0, 0.55), (0.42, 0.45)]):
        n = int(d * ln * SR); x = lowpass(band(rng.standard_normal(n), 200, 1300), 1500)       # soft felt, no hiss
        tt = np.linspace(0, 1, n)
        put(t + d * off, x * np.sin(np.pi * tt) ** 1.3, 0.8 if k == 0 else 0.62)


def ev_whoosh(e):
    n = int(e["d"] * SR); tt = np.linspace(0, 1, n)
    x = rng.standard_normal(n)
    # sweep a band-pass up and back down by cross-fading three fixed bands
    lo, mid, hi = band(x, 250, 900), band(x, 800, 2600), band(x, 2200, 6500)
    y = lo * (1 - tt) ** 2 + mid * np.sin(np.pi * tt) + hi * np.sin(np.pi * tt) ** 3 * 0.7
    put(e["t"], y * np.sin(np.pi * tt ** 0.8) ** 1.5, 0.5)


def ev_thud(e):
    n = int(0.22 * SR); t = np.arange(n) / SR
    f = 110 * np.exp(-t * 9) + 60
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 22) + 0.3 * band(rng.standard_normal(n), 400, 2500) * np.exp(-t * 90)
    put(e["t"], x, 0.7 * e.get("gain", 1.0))


for e in json.load(open(ev_path)):
    {"write": ev_write, "stroke": ev_stroke, "erase": ev_erase, "whoosh": ev_whoosh, "thud": ev_thud}[e["type"]](e)

x = mix[:N]
x = x / max(1e-9, np.abs(x).max()) * 0.7
wavfile.write(out, SR, (np.stack([x, x], 1) * 32767).astype(np.int16))
print("wrote", out, round(DUR, 2), "s")
