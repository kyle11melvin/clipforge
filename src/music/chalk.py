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
    n = max(int(d * SR), 256)
    t = np.arange(n) / SR
    v = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.8                      # hand speed through the stroke
    w = rng.standard_normal(n)
    body = band(w, 900, 3800, order=1)                                   # the dry scrape
    air = band(rng.standard_normal(n), 3500, 9000, order=1)              # brighter when the hand moves fast
    ring = signal.sosfilt(signal.butter(2, [2300, 2900], btype="band", fs=SR, output="sos"), w) * 0.5   # chalky tone
    flutter = lowpass(rng.standard_normal(n), 140); flutter = 0.6 + 0.4 * flutter / (np.abs(flutter).max() + 1e-9)
    x = (body + ring + air * 0.7 * v * speed) * flutter * v
    edge = min(int(0.012 * SR), n // 4); x[:edge] *= np.linspace(0, 1, edge); x[-edge:] *= np.linspace(1, 0, edge)
    return x


def touch():
    """Chalk meeting the board: a dull, quiet knock, used sparingly."""
    n = int(0.04 * SR); t = np.arange(n) / SR
    return lowpass(rng.standard_normal(n), 900) * np.exp(-t * 120) * 0.6 + np.sin(2 * np.pi * 170 * t) * np.exp(-t * 90) * 0.4


def ev_write(e):
    """Handwriting rhythm, not one hit per letter: four or five strokes a second, uneven lengths, short lifts."""
    t, end = e["t"], e["t"] + e["d"]
    first = True
    while t < end - 0.06:
        ln = min(rng.uniform(0.11, 0.26), end - t)
        if first or rng.random() < 0.2: put(t, touch(), 0.10)
        put(t, scrape(ln, speed=rng.uniform(0.7, 1.2)), rng.uniform(0.42, 0.6))
        t += ln + rng.uniform(0.015, 0.07) + (0.09 if rng.random() < 0.15 else 0)   # now and then a longer lift
        first = False


def ev_stroke(e):
    put(e["t"], touch(), 0.10)
    put(e["t"], scrape(e["d"], speed=1.1), 0.6)


def ev_erase(e):
    t, d = e["t"], e["d"]
    for k, (off, ln) in enumerate([(0, 0.55), (0.42, 0.45)]):
        n = int(d * ln * SR); x = band(rng.standard_normal(n), 250, 2600)
        x += 0.25 * band(rng.standard_normal(n), 3000, 7000)
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
