/**
 * B-roll pass: cut rendered graphics into talking-head footage.
 *
 * The footage timeline (and its audio) is untouched. Each cue takes a slice of the graphics video
 * [from, to] and shows it over the footage starting at footage time `at`, either full-frame ("cut",
 * the speaker disappears for the length of the slice) or as a picture-in-picture box ("pip", the
 * speaker stays visible, the graphic sits in the lower half of the frame). Slices fade in and out
 * over 0.2 s.
 *
 * cues.json:
 *   {
 *     "footage": "videos/x/final.mp4",          // captioned output of `clipforge build`, or any clip
 *     "graphics": "videos/x/final-graphics.mp4", // output of src/graphics/render.mjs
 *     "cues": [
 *       { "at": 3.2, "from": 3.4, "to": 6.4, "mode": "cut" },
 *       { "at": 9.0, "from": 16.3, "to": 18.8, "mode": "pip" }
 *     ]
 *   }
 */
import { mkdir, readFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { run, log } from "./run.mjs";
import { probe, assemble } from "./ffmpeg.mjs";

const FADE = 0.2;

export async function loadCues(file) {
  const spec = JSON.parse(await readFile(file, "utf8"));
  const base = dirname(resolve(file));
  const rel = (p) => (p ? resolve(base, p) : p);
  if (!spec.footage || !spec.graphics) throw new Error(`${file}: needs "footage" and "graphics" paths`);
  if (!Array.isArray(spec.cues) || !spec.cues.length) throw new Error(`${file}: needs a non-empty "cues" array`);
  return { footage: rel(spec.footage), graphics: rel(spec.graphics), cues: spec.cues, pip: spec.pip ?? {} };
}

/** Make sure the footage is already at the target frame and fps; reframe it once if not. */
async function conform(footage, { width, height, fps, workDir }) {
  const info = await probe(footage);
  if (info.width === width && info.height === height && Math.abs(info.fps - fps) < 0.01) return { file: footage, info };
  const out = join(workDir, "footage.mp4");
  log("conform", `${info.width}x${info.height}@${info.fps.toFixed(0)} → ${width}x${height}@${fps}`);
  await assemble({ clips: [{ ...info, segments: [{ start: 0, end: info.duration }] }], width, height, fps, output: out });
  return { file: out, info: await probe(out) };
}

export async function broll({ cuesFile, output, width = 1080, height = 1920, fps = 30 }) {
  const spec = await loadCues(cuesFile);
  const workDir = dirname(resolve(output));
  await mkdir(workDir, { recursive: true });

  const { file: footage, info: f } = await conform(spec.footage, { width, height, fps, workDir });
  const g = await probe(spec.graphics);
  log("broll", `${f.duration.toFixed(1)}s footage, ${g.duration.toFixed(1)}s graphics, ${spec.cues.length} cue(s)`);

  const pipW = Math.round(width * (spec.pip.width ?? 0.56));
  const pipH = Math.round(pipW * (g.height / g.width));
  const pipX = spec.pip.x ?? Math.round((width - pipW) / 2);
  const pipY = spec.pip.y ?? Math.round(height - pipH - height * 0.07);
  const border = 8;

  const filters = [`[0:v]format=yuv420p[b0]`];
  const cues = [...spec.cues].sort((a, b) => a.at - b.at);
  cues.forEach((c, i) => {
    const from = Math.max(0, Number(c.from)), to = Math.min(g.duration, Number(c.to));
    let len = to - from;
    if (len <= FADE * 2) throw new Error(`cue ${i + 1}: graphics slice ${from}-${to} is too short`);
    if (c.at + len > f.duration) len = Math.max(FADE * 2, f.duration - c.at); // never run past the footage
    const end = c.at + len;
    const mode = c.mode === "pip" ? "pip" : "cut";
    log("cue", `${i + 1}: ${mode} graphics ${from.toFixed(1)}–${(from + len).toFixed(1)}s at footage ${c.at.toFixed(1)}–${end.toFixed(1)}s`);

    const chain = [
      `[1:v]trim=start=${from}:end=${from + len}`, "setpts=PTS-STARTPTS", "format=yuva420p",
      `fade=t=in:st=0:d=${FADE}:alpha=1`, `fade=t=out:st=${(len - FADE).toFixed(3)}:d=${FADE}:alpha=1`,
    ];
    let x = 0, y = 0;
    if (mode === "pip") {
      chain.push(`scale=${pipW}:${pipH}`, `pad=${pipW + border * 2}:${pipH + border * 2}:${border}:${border}:color=#C9A96A`);
      x = pipX - border; y = pipY - border;
    }
    chain.push(`setpts=PTS+${c.at}/TB`);
    filters.push(`${chain.join(",")}[g${i}]`);
    filters.push(`[b${i}][g${i}]overlay=x=${x}:y=${y}:eof_action=pass:enable='between(t,${c.at},${end.toFixed(3)})'[b${i + 1}]`);
  });

  const args = [
    "-hide_banner", "-nostats", "-y", "-i", footage, "-i", spec.graphics,
    "-filter_complex", filters.join(";"),
    "-map", `[b${cues.length}]`, "-map", "0:a?",
    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", String(fps), "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest",
    output,
  ];
  await run("ffmpeg", args);
  const out = await probe(output);
  log("done", `${output} · ${out.duration.toFixed(1)}s`);
  return { output, duration: out.duration };
}
