#!/usr/bin/env python3
"""Chalkboard sound effects, synthesised (numpy + scipy, no samples).

  python3 -I src/music/chalk.py <out.wav> <events.json> --dur 30.8

events.json is a list of {"type", "t", "d", ...} in seconds of the picture:
  write    chalk lettering: short scraping strokes with a tap at the start of each, about one per letter ("n")
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


def scrape(d, centre, grit=1.0):
    """One chalk stroke: band-passed noise with the stick-slip chatter chalk makes on slate."""
    n = max(int(d * SR), 64)
    x = band(rng.standard_normal(n), centre * 0.6, min(centre * 1.7, 11000))
    x += 0.35 * band(rng.standard_normal(n), 5500, 10500)          # the dry hiss on top
    t = np.arange(n) / SR
    chatter = 0.62 + 0.38 * signal.sawtooth(2 * np.pi * rng.uniform(55, 95) * t + rng.uniform(0, 6), 0.3) * grit
    env = np.minimum(1, t / 0.006) * np.minimum(1, (d - t) / 0.02).clip(0) * (0.75 + 0.25 * np.sin(np.pi * t / d))
    return x * chatter * env


def tap():
    n = int(0.03 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 240 * t) * np.exp(-t * 160) + 0.5 * band(rng.standard_normal(n), 1500, 6000) * np.exp(-t * 260))


def ev_write(e):
    t, d, n = e["t"], e["d"], max(2, int(e.get("n", 6)))
    slot = d / n
    for k in range(n):
        if rng.random() < 0.12: continue                            # a space between words
        s = t + k * slot + rng.uniform(0, slot * 0.15)
        ln = slot * rng.uniform(0.55, 0.9)
        put(s, tap(), 0.22)
        put(s + 0.004, scrape(ln, rng.uniform(2300, 3900)), 0.55)


def ev_stroke(e):
    put(e["t"], tap(), 0.25)
    put(e["t"], scrape(e["d"], 2800, grit=0.7), 0.6)


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
