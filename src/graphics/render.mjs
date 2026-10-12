// Render a motion-graphics composition (an HTML page that exposes `window.seek(t)`)
// frame by frame with headless Chromium, then encode it with FFmpeg.
//
//   node src/graphics/render.mjs <comp.html> <out.mp4> [--duration 20] [--fps 30] [--size 1080x1920]
//   node src/graphics/render.mjs <comp.html> <probe.png> --probe 1.5,6.9,9.6      (one still per time, side by side)
//   ... --probe 3.6,9.6 --stills <dir>     also keeps each full-size still as <dir>/still_<i>.png
//   ... --mode carousel                    loads the page as comp.html#carousel (a layout switch in the composition)
//
// The composition contract is simple: the page draws itself for any time `t` (seconds) when
// `window.seek(t)` is called, with no CSS transitions or animations of its own. That makes every
// frame deterministic, so the render is exact at any fps and can be resumed or probed.

import { createRequire } from "node:module";
import { mkdir, rm } from "node:fs/promises";
import { basename, dirname, join, resolve } from "node:path";
import { tmpdir } from "node:os";
import { execFileSync } from "node:child_process";

const require = createRequire(import.meta.url);

function loadPlaywright() {
  try {
    return require("playwright");
  } catch {
    console.error("playwright is not installed. Run `npm install` (it is a devDependency), then `npx playwright install chromium`\n" +
      "or point PLAYWRIGHT_BROWSERS_PATH at an existing Chromium.");
    process.exit(1);
  }
}

function parseArgs(argv) {
  const opts = { duration: 20, fps: 30, width: 1080, height: 1920, probe: null, stills: null, mode: "", positional: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--duration") opts.duration = parseFloat(argv[++i]);
    else if (a === "--fps") opts.fps = parseInt(argv[++i], 10);
    else if (a === "--size") [opts.width, opts.height] = argv[++i].split("x").map(Number);
    else if (a === "--probe") opts.probe = argv[++i].split(",").map(Number);
    else if (a === "--stills") opts.stills = argv[++i];
    else if (a === "--mode") opts.mode = argv[++i];
    else opts.positional.push(a);
  }
  if (opts.positional.length < 2) {
    console.error("usage: render.mjs <comp.html> <out.mp4|probe.png> [--duration s] [--fps n] [--size WxH] [--probe t1,t2,...] [--stills dir] [--mode name]");
    process.exit(2);
  }
  return opts;
}

// Launch Chromium. Playwright wants the exact browser build it was installed with; when that build is
// missing (a pre-installed browser of another version, as in cloud sessions), fall back to
// CLIPFORGE_CHROMIUM or the pre-installed /opt/pw-browsers/chromium.
async function launchChromium(chromium) {
  const { existsSync } = await import("node:fs");
  const candidates = [process.env.CLIPFORGE_CHROMIUM, "/opt/pw-browsers/chromium"].filter(Boolean);
  try {
    return await chromium.launch();
  } catch (err) {
    for (const executablePath of candidates) {
      if (existsSync(executablePath)) return chromium.launch({ executablePath });
    }
    throw err;
  }
}

export async function render({ comp, out, duration, fps, width, height, probe, stills = null, mode = "" }) {
  const { chromium } = loadPlaywright();
  const frames = join(tmpdir(), `clipforge-frames-${process.pid}`);
  await rm(frames, { recursive: true, force: true });
  await mkdir(frames, { recursive: true });
  await mkdir(dirname(resolve(out)), { recursive: true });

  const browser = await launchChromium(chromium);
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
  await page.goto("file://" + resolve(comp) + (mode ? "#" + mode : ""));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);

  try {
    if (probe) {
      if (stills) await mkdir(resolve(stills), { recursive: true });
      for (let i = 0; i < probe.length; i++) {
        await page.evaluate((t) => window.seek(t), probe[i]);
        const path = stills ? join(resolve(stills), `still_${i}.png`) : join(frames, `probe_${i}.png`);
        await page.screenshot({ path, type: "png" });
      }
      const inputs = probe.flatMap((_, i) => ["-i", stills ? join(resolve(stills), `still_${i}.png`) : join(frames, `probe_${i}.png`)]);
      const scaled = probe.map((_, i) => `[${i}]scale=360:-1[p${i}]`).join(";");
      const stack = probe.length === 1 ? "[p0]copy" : probe.map((_, i) => `[p${i}]`).join("") + `hstack=${probe.length}`;
      execFileSync("ffmpeg", ["-y", "-v", "error", ...inputs, "-filter_complex", `${scaled};${stack}`, out]);
      return out;
    }

    const total = Math.round(duration * fps);
    const t0 = Date.now();
    for (let f = 0; f < total; f++) {
      await page.evaluate((t) => window.seek(t), f / fps);
      await page.screenshot({ path: join(frames, `f_${String(f).padStart(5, "0")}.jpg`), type: "jpeg", quality: 94 });
      if (f % 150 === 0) process.stderr.write(`  frame ${f}/${total}\n`);
    }
    process.stderr.write(`  ${total} frames in ${((Date.now() - t0) / 1000).toFixed(1)}s\n`);
    execFileSync("ffmpeg", ["-y", "-v", "error", "-framerate", String(fps), "-i", join(frames, "f_%05d.jpg"),
      "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]);
    return out;
  } finally {
    await browser.close();
    await rm(frames, { recursive: true, force: true });
  }
}

if (process.argv[1] && basename(process.argv[1]) === "render.mjs") {
  const opts = parseArgs(process.argv.slice(2));
  const [comp, out] = opts.positional;
  render({ comp, out, ...opts }).then((o) => console.log(`wrote ${o}`)).catch((e) => { console.error(e); process.exit(1); });
}
