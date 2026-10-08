// Builds five synthetic talking-head clips with deliberate dead air, for an end-to-end run.
// Needs the local Kokoro TTS model in .tts/ (see README "Testing"). Speech is synthetic; the point
// is timing: leading/trailing silence, a mid-clip pause, mixed portrait and landscape sources.
import { mkdir, rm } from "node:fs/promises";
import { join } from "node:path";
import { run } from "../src/run.mjs";

const OUT = new URL("./fixtures/", import.meta.url).pathname;
await rm(OUT, { recursive: true, force: true });
await mkdir(OUT, { recursive: true });

const lines = [
  ["clip-1", "Hey everyone, Kyle here. If you're buying a house this year, here's the one thing nobody tells you about mortgage rates.", "1080x1920", 1.5, 2.0, 0],
  ["clip-2", "The rate you see advertised is almost never the rate you actually get.", "1080x1920", 2.2, 1.4, 0],
  ["clip-3", "Your credit score, your down payment, and the type of loan all move that number.", "1920x1080", 1.0, 2.5, 2.2],
  ["clip-4", "So before you fall in love with a listing, get a real quote based on your actual numbers.", "1080x1920", 1.8, 1.2, 0],
  ["clip-5", "Send me a message and I'll walk you through it. No pressure, no obligation.", "1920x1080", 1.3, 3.0, 0],
];

for (const [name, text, size, lead, tail, midPause] of lines) {
  const wav = join(OUT, `${name}.wav`);
  const text2 = midPause ? text.replace(/,? and /, " [[SPLIT]] and ") : text;
  if (midPause && text2.includes("[[SPLIT]]")) {
    const [a, b] = text2.split("[[SPLIT]]");
    await run("python3", ["test/say.py", a.trim(), wav + ".a.wav"]);
    await run("python3", ["test/say.py", b.trim(), wav + ".b.wav"]);
    await run("ffmpeg", ["-y", "-loglevel", "error", "-i", wav + ".a.wav", "-i", wav + ".b.wav",
      "-filter_complex", `[0:a]apad=pad_dur=${midPause}[a];[a][1:a]concat=n=2:v=0:a=1[o]`, "-map", "[o]", wav]);
  } else await run("python3", ["test/say.py", text, wav]);
  // Pad with silence, lay over a test pattern so the frame has visible motion for crop checks.
  const [w, h] = size.split("x");
  await run("ffmpeg", ["-y", "-loglevel", "error",
    "-f", "lavfi", "-i", `testsrc2=s=${size}:r=30`,
    "-i", wav,
    "-filter_complex", `[1:a]adelay=${lead * 1000}|${lead * 1000},apad=pad_dur=${tail}[a]`,
    "-map", "0:v", "-map", "[a]", "-shortest", "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-c:a", "aac",
    join(OUT, `${name}.mp4`)]);
  await rm(wav, { force: true }); await rm(wav + ".a.wav", { force: true }); await rm(wav + ".b.wav", { force: true });
  console.log(`fixture ${name}.mp4 (${w}x${h}, lead ${lead}s, tail ${tail}s${midPause ? `, mid pause ${midPause}s` : ""})`);
}
