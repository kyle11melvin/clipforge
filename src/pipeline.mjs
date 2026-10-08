import { mkdir, readdir, readFile, writeFile, stat, cp, rm } from "node:fs/promises";
import { existsSync } from "node:fs";
import { basename, extname, join, resolve } from "node:path";
import { run, log } from "./run.mjs";
import { probe, detectSilence, keepSegments, assemble, targetSize } from "./ffmpeg.mjs";
import { groupWords, toSrt } from "./captions.mjs";
import { composition } from "./compose.mjs";

const VIDEO_EXT = new Set([".mp4", ".mov", ".m4v", ".mkv", ".webm", ".avi"]);
const ROOT = resolve(new URL("..", import.meta.url).pathname);

/** Resolve the input: a directory (sorted by name) or an explicit list of files. */
export async function collectClips(inputs) {
  const files = [];
  for (const input of inputs) {
    const p = resolve(input);
    if ((await stat(p)).isDirectory()) {
      const names = (await readdir(p)).filter((n) => VIDEO_EXT.has(extname(n).toLowerCase()) && !n.startsWith("."));
      names.sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
      files.push(...names.map((n) => join(p, n)));
    } else files.push(p);
  }
  if (!files.length) throw new Error("No video clips found. Pass a folder of .mp4/.mov files or the files themselves.");
  return files;
}

export async function build(opts) {
  const { name, aspect = "9:16", fit = "cover", fps = 30, trim = true, quality = "looks", force = false } = opts;
  const files = await collectClips(opts.inputs);
  const work = resolve(opts.outDir ?? join(ROOT, "videos"), name);
  const { width, height } = targetSize(aspect);
  await mkdir(join(work, "public"), { recursive: true });
  if (force) for (const f of ["cut.mp4", "transcript.json", "captions.srt", "final.mp4"]) await rm(join(work, f), { force: true });

  log("clips", `${files.length} clip(s) → ${work}`);

  // 1. Probe + silence detection per clip, then one FFmpeg pass that trims, reframes, concatenates, normalises.
  const cutPath = join(work, "cut.mp4");
  if (!existsSync(cutPath)) {
    const clips = [];
    let inTotal = 0, outTotal = 0;
    for (const file of files) {
      const info = await probe(file);
      const silences = trim && info.hasAudio ? await detectSilence(file, info.duration, opts.silence) : [];
      const segments = trim ? keepSegments(silences, info.duration, opts.keep) : [{ start: 0, end: info.duration }];
      const kept = segments.reduce((s, x) => s + (x.end - x.start), 0);
      inTotal += info.duration; outTotal += kept;
      log("trim", `${basename(file)}: ${info.width}x${info.height} ${info.duration.toFixed(2)}s → ${kept.toFixed(2)}s (${segments.length} segment${segments.length === 1 ? "" : "s"})`);
      clips.push({ ...info, segments });
    }
    await assemble({ clips, width, height, fps, fit, output: cutPath });
    log("cut", `${inTotal.toFixed(1)}s of footage → ${outTotal.toFixed(1)}s (removed ${(inTotal - outTotal).toFixed(1)}s of dead air)`);
    await writeFile(join(work, "cut.json"), JSON.stringify(clips, null, 2));
  } else log("cut", "reusing cut.mp4 (pass --force to redo)");
  const cutInfo = await probe(cutPath);

  // 2. Transcribe locally (word timestamps). Reused if transcript.json exists so corrections survive re-runs.
  const transcriptPath = join(work, "transcript.json");
  if (!existsSync(transcriptPath)) {
    log("asr", "transcribing (local model)…");
    const { stdout } = await run("npx", ["hyperframes", "transcribe", cutPath, "-d", work, "--json"], { cwd: ROOT });
    const result = JSON.parse(stdout.trim().split("\n").pop());
    if (!result.ok) throw new Error(`transcription failed: ${result.error}`);
    log("asr", `${result.wordCount} words via ${result.engine}`);
  } else log("asr", "reusing transcript.json (edit it to fix words, delete it to re-transcribe)");
  const words = JSON.parse(await readFile(transcriptPath, "utf8"));

  // 3. Captions.
  const captions = groupWords(words, opts.captions).filter((c) => c.start < cutInfo.duration)
    .map((c) => ({ ...c, end: Math.min(c.end, cutInfo.duration) }));
  await writeFile(join(work, "captions.srt"), toSrt(captions));
  log("captions", `${captions.length} caption chunks`);

  // 4. Composition.
  await cp(cutPath, join(work, "public", "cut.mp4"));
  await cp(join(ROOT, "assets"), join(work, "assets"), { recursive: true });
  const lower = opts.lower ? parseLower(opts.lower) : null;
  const html = composition({ width, height, fps, duration: cutInfo.duration, videoSrc: "public/cut.mp4", captions, hook: opts.hook, lower, style: opts.style });
  await writeFile(join(work, "index.html"), html);
  const lint = await run("npx", ["hyperframes", "lint", work, "--json"], { cwd: ROOT, allowFail: true });
  const findings = safeJson(lint.stdout);
  const errors = Array.isArray(findings) ? findings.filter((f) => f.severity === "error") : [];
  if (errors.length) throw new Error(`composition failed lint:\n${errors.map((e) => `${e.rule}: ${e.message}`).join("\n")}`);
  log("compose", "index.html written and linted");

  // 5. Render.
  const finalPath = join(work, "final.mp4");
  log("render", `rendering ${width}x${height}@${fps} (${quality})…`);
  const t0 = Date.now();
  await run("npx", ["hyperframes", "render", work, "--output", finalPath, "--quality", quality, "--quiet"], { cwd: ROOT });
  const out = await probe(finalPath);
  log("done", `${finalPath} · ${out.duration.toFixed(1)}s · ${((Date.now() - t0) / 1000).toFixed(0)}s render`);
  return { finalPath, cutPath, transcriptPath, captions, duration: out.duration, work };
}

function parseLower(s) {
  const [name, tagline] = String(s).split("|").map((x) => x.trim());
  return { name, tagline };
}
function safeJson(s) { try { return JSON.parse(s); } catch { return null; } }
