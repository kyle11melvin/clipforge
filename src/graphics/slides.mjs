#!/usr/bin/env node
// Render carousel slides to PNG. The HTML holds one `section.slide` per slide at its final pixel size
// (1080x1350 for an Instagram feed post). Each slide is screenshotted with headless Chromium and a
// contact sheet of all slides is written beside them.
//
//   node src/graphics/slides.mjs graphics/<post>/slides.html videos/<post>/
//
// Output: <outdir>/slide-01.png ... and <outdir>/contact-sheet.jpg
import { existsSync, mkdirSync } from "node:fs";
import { resolve, join } from "node:path";
import { pathToFileURL } from "node:url";
import { execFileSync } from "node:child_process";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const [,, htmlArg, outArg] = process.argv;
if (!htmlArg || !outArg) {
  console.error("usage: node src/graphics/slides.mjs <slides.html> <outdir>");
  process.exit(2);
}
const html = resolve(htmlArg);
const outdir = resolve(outArg);
mkdirSync(outdir, { recursive: true });

const { chromium } = require("playwright");
async function launch() {
  const candidates = [process.env.CLIPFORGE_CHROMIUM, "/opt/pw-browsers/chromium"].filter(Boolean);
  try { return await chromium.launch(); }
  catch (err) {
    for (const executablePath of candidates) if (existsSync(executablePath)) return chromium.launch({ executablePath });
    throw err;
  }
}

const browser = await launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(html).href, { waitUntil: "load" });
await page.evaluate(() => document.fonts.ready);
const slides = await page.$$("section.slide");
const files = [];
for (let i = 0; i < slides.length; i++) {
  const file = join(outdir, `slide-${String(i + 1).padStart(2, "0")}.png`);
  await slides[i].screenshot({ path: file, type: "png" });
  files.push(file);
  console.log("wrote", file);
}
await browser.close();

// Contact sheet: all slides in one row at 1/3 size, 24 px gutters, via FFmpeg.
const n = files.length;
const inputs = files.flatMap(f => ["-i", f]);
const scaled = files.map((_, i) => `[${i}:v]scale=iw/3:-1[s${i}]`).join(";");
const chain = files.map((_, i) => `[s${i}]`).join("");
const sheet = join(outdir, "contact-sheet.jpg");
execFileSync("ffmpeg", ["-y", "-loglevel", "error", ...inputs, "-filter_complex",
  `${scaled};${chain}hstack=inputs=${n}:shortest=1,pad=iw+${24 * (n + 1)}:ih+48:0:0:black,format=yuv420p`,
  "-q:v", "3", sheet]);
console.log("wrote", sheet);
