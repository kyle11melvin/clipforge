// Render one full-size still of a composition (a cover photo, a thumbnail).
//   node src/graphics/still.mjs <comp.html> <out.png|out.jpg> [--t 0] [--size 1080x1920]
import { basename, resolve } from "node:path";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);

const argv = process.argv.slice(2);
const opts = { t: 0, width: 1080, height: 1920, positional: [] };
for (let i = 0; i < argv.length; i++) {
  if (argv[i] === "--t") opts.t = parseFloat(argv[++i]);
  else if (argv[i] === "--size") [opts.width, opts.height] = argv[++i].split("x").map(Number);
  else opts.positional.push(argv[i]);
}
const [comp, out] = opts.positional;
if (!comp || !out) { console.error("usage: still.mjs <comp.html> <out.png|jpg> [--t s] [--size WxH]"); process.exit(2); }

const { chromium } = require("playwright");
const { existsSync } = await import("node:fs");
let browser;
try { browser = await chromium.launch(); }
catch (err) {
  const alt = [process.env.CLIPFORGE_CHROMIUM, "/opt/pw-browsers/chromium"].filter(Boolean).find((p) => existsSync(p));
  if (!alt) throw err;
  browser = await chromium.launch({ executablePath: alt });
}
const page = await browser.newPage({ viewport: { width: opts.width, height: opts.height }, deviceScaleFactor: 1 });
const [compPath, hash = ""] = comp.split("#");
await page.goto("file://" + resolve(compPath) + (hash ? "#" + hash : ""));
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(300);
await page.evaluate((t) => { if (window.seek) window.seek(t); }, opts.t);
const jpg = /\.jpe?g$/i.test(out);
await page.screenshot({ path: out, type: jpg ? "jpeg" : "png", ...(jpg ? { quality: 92 } : {}) });
await browser.close();
console.log(`wrote ${out}`);
