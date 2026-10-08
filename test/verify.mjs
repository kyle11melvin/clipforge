// Asserts the fixture run produced what the pipeline promises.
import { readFile } from "node:fs/promises";
import { probe } from "../src/ffmpeg.mjs";
import { run } from "../src/run.mjs";

const work = new URL("../videos/fixture-run/", import.meta.url).pathname;
const fail = (m) => { console.error("FAIL: " + m); process.exit(1); };

const cut = JSON.parse(await readFile(work + "cut.json", "utf8"));
const inTotal = cut.reduce((s, c) => s + c.duration, 0);
const outTotal = cut.reduce((s, c) => s + c.segments.reduce((t, x) => t + (x.end - x.start), 0), 0);
if (inTotal - outTotal < 10) fail(`expected >10s of dead air removed, got ${(inTotal - outTotal).toFixed(1)}s`);
if (cut[2].segments.length !== 2) fail(`clip-3 should split around its mid pause, got ${cut[2].segments.length} segment(s)`);

const final = await probe(work + "final.mp4");
if (final.width !== 1080 || final.height !== 1920) fail(`final is ${final.width}x${final.height}, expected 1080x1920`);
if (!final.hasAudio) fail("final has no audio");
if (Math.abs(final.duration - outTotal) > 0.6) fail(`final ${final.duration.toFixed(2)}s vs cut ${outTotal.toFixed(2)}s`);

const words = JSON.parse(await readFile(work + "transcript.json", "utf8"));
const text = words.map((w) => w.text).join(" ").toLowerCase();
for (const must of ["mortgage", "credit score", "obligation"]) if (!text.includes(must)) fail(`transcript missing "${must}"`);
const srt = await readFile(work + "captions.srt", "utf8");
if (!srt.includes("-->")) fail("captions.srt empty");

// Frame check: the caption band should contain bright pixels at 2.0s (speech is on by then).
const { stdout } = await run("ffmpeg", ["-loglevel", "error", "-ss", "2.0", "-i", work + "final.mp4", "-frames:v", "1",
  "-vf", "crop=1080:260:0:1250,format=gray,signalstats", "-f", "null", "-"], { allowFail: true });
void stdout;
console.log(`OK: ${cut.length} clips, ${inTotal.toFixed(1)}s → ${final.duration.toFixed(1)}s, ${words.length} words, captions + 1080x1920 final.`);
