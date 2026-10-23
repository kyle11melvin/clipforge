#!/usr/bin/env node
import { parseArgs } from "node:util";
import { build } from "../src/pipeline.mjs";
import { broll } from "../src/broll.mjs";

const HELP = `clipforge — folder of clips in, social-ready video out

USAGE
  clipforge build <folder-or-files...> [options]
  clipforge broll <cues.json> --output <file.mp4>

BROLL
  Cuts rendered graphics (src/graphics/render.mjs) into footage at the times listed in cues.json,
  full-frame ("cut") or picture-in-picture ("pip"). The footage audio is left untouched.
  See src/broll.mjs for the cues.json format.

BUILD OPTIONS
  --name <name>        Project name; output goes to videos/<name>/final.mp4 (default: folder name)
  --aspect <ratio>     9:16 (default), 4:5, 1:1, 16:9
  --fit <mode>         cover (crop to fill, default) or contain (letterbox)
  --hook <text>        Title shown at the top for the first 3 seconds
  --lower "<name>|<tagline>"   Lower-third shown from 0.8s to ~5.8s
  --no-trim            Keep dead air (skip silence removal)
  --silence-db <n>     Silence threshold in dBFS (default -35)
  --min-silence <s>    Shortest pause that counts as dead air (default 0.5)
  --pad <s>            Breathing room kept around speech (default 0.18)
  --caption-style <s>  classic (Inter, uppercase, outline) or rounded (Nunito, sentence case, soft shadow,
                       like Kyle's earlier reels). Default classic.
  --caption-hide <a-b[,a-b]>  Hide captions over these windows (seconds), e.g. while an overlay carries the words
  --caption-y <frac>   Where captions sit, as a fraction of frame height from the bottom (default 0.30;
                       use ~0.19 to keep them off the face, above Instagram's own caption overlay)
  --quality <q>        draft | looks (default) | delivery
  --out <dir>          Where project folders go (default: ./videos)
  --force              Redo the cut, transcript, and render from scratch

Re-running without --force reuses cut.mp4 and transcript.json, so you can fix
misheard words in videos/<name>/transcript.json and re-render in one step.
`;

const { values, positionals } = parseArgs({
  allowPositionals: true,
  options: {
    name: { type: "string" }, aspect: { type: "string", default: "9:16" }, fit: { type: "string", default: "cover" },
    hook: { type: "string" }, lower: { type: "string" }, trim: { type: "boolean", default: true },
    "silence-db": { type: "string" }, "min-silence": { type: "string" }, pad: { type: "string" },
    "caption-y": { type: "string" }, "caption-style": { type: "string", default: "classic" }, "caption-hide": { type: "string" },
    quality: { type: "string", default: "looks" }, out: { type: "string" }, force: { type: "boolean", default: false },
    output: { type: "string" },
    help: { type: "boolean", short: "h", default: false },
  },
});

const [cmd, ...inputs] = positionals;
if (values.help || !["build", "broll"].includes(cmd) || !inputs.length) { console.log(HELP); process.exit(values.help ? 0 : 1); }

if (cmd === "broll") {
  if (!values.output) { console.error("clipforge broll needs --output <file.mp4>"); process.exit(1); }
  try {
    await broll({ cuesFile: inputs[0], output: values.output });
  } catch (err) {
    console.error(`\nclipforge failed: ${err.message}`);
    process.exit(1);
  }
  process.exit(0);
}

const name = values.name ?? inputs[0].replace(/[\\/]+$/, "").split(/[\\/]/).pop().replace(/\.[^.]+$/, "");
try {
  await build({
    inputs, name, aspect: values.aspect, fit: values.fit, hook: values.hook, lower: values.lower,
    trim: values.trim, quality: values.quality, outDir: values.out, force: values.force,
    silence: { noiseDb: num(values["silence-db"], -35), minSilence: num(values["min-silence"], 0.5) },
    keep: { pad: num(values.pad, 0.18) },
    style: { captionFromBottom: num(values["caption-y"], 0.30), captionStyle: values["caption-style"] },
    captionHide: values["caption-hide"] ? values["caption-hide"].split(",") : [],
  });
} catch (err) {
  console.error(`\nclipforge failed: ${err.message}`);
  process.exit(1);
}
function num(v, d) { return v == null ? d : Number(v); }
