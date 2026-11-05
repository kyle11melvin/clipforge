/**
 * Multi-take assembly: pick the best delivery of each line across several takes.
 *
 *   node src/edl.mjs videos/<post>/edl.json
 *
 * edl.json:
 *   { "output": "cut.mp4", "aspect": "9:16",
 *     "cuts": [ { "file": "takes/take2.mov", "start": 1.0, "end": 2.95, "gain": 0, "says": "What rate are you waiting for?" }, ... ] }
 *
 * Paths are relative to the edl file. `grade` (per cut or top-level, optional) is an ffmpeg video filter chain
 * applied after the HDR tone-map, e.g. "colortemperature=temperature=7200,eq=saturation=0.85" for warm indoor
 * light. `gain` (dB, optional) evens out levels between takes; the whole
 * assembly is then loudness-normalised like any `clipforge build` cut. Writes <output> next to the edl plus
 * cut.json, so `clipforge build <anything> --name <post>` reuses it (it only re-cuts when cut.mp4 is missing)
 * and goes straight to transcription, captions and the render.
 */
import { readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { probe, assemble, targetSize } from "./ffmpeg.mjs";
import { log } from "./run.mjs";

const edlFile = process.argv[2];
if (!edlFile) { console.error("usage: node src/edl.mjs <edl.json>"); process.exit(1); }
const base = dirname(resolve(edlFile));
const edl = JSON.parse(await readFile(edlFile, "utf8"));
const { width, height } = targetSize(edl.aspect ?? "9:16");
const fps = edl.fps ?? 30;

const byFile = new Map();
for (const c of edl.cuts) {
  const file = resolve(base, c.file);
  if (!byFile.has(file)) byFile.set(file, await probe(file));
}
// One clip entry per cut keeps the order of the EDL (a take may be used more than once, out of order).
const clips = edl.cuts.map((c) => ({ ...byFile.get(resolve(base, c.file)), segments: [{ start: c.start, end: c.end, gain: c.gain, grade: c.grade ?? edl.grade }] }));
const total = edl.cuts.reduce((s, c) => s + (c.end - c.start), 0);
edl.cuts.forEach((c, i) => log("cut", `${i + 1}. ${c.file} ${c.start.toFixed(2)}–${c.end.toFixed(2)} (${(c.end - c.start).toFixed(2)}s)${c.says ? `  "${c.says}"` : ""}`));
const output = resolve(base, edl.output ?? "cut.mp4");
await assemble({ clips, width, height, fps, output });
await writeFile(resolve(base, "cut.json"), JSON.stringify(clips, null, 2));
log("done", `${output} · ${total.toFixed(1)}s from ${edl.cuts.length} cuts`);
