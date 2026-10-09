# clipforge

Hand it a folder of talking-head clips. Get back one vertical video with the dead air cut out,
the clips stitched in order, big social-style captions timed to your speech, and an optional
hook title and lower-third. Built on [HyperFrames](https://github.com/heygen-com/hyperframes)
for captions and rendering, FFmpeg for the cutting, and a local speech model for transcription.
Nothing leaves your machine.

## What it does

1. **Trim** – finds silence in each clip, cuts leading and trailing dead air down to a breath,
   and shortens long mid-sentence pauses. Clips are ordered by filename (`01-intro.mp4`, `02-…`).
2. **Stitch** – reframes every clip to the target aspect (9:16 by default, center-crop), resamples
   to 30 fps, concatenates, and loudness-normalises the audio for phones.
3. **Transcribe** – runs Parakeet locally for word-level timestamps. No API key, no upload.
4. **Caption** – groups words into 3–4 word chunks that break on pauses and sentences, and writes
   a `captions.srt` sidecar too.
5. **Render** – writes a HyperFrames composition and renders the final MP4.

## Setup (once per machine)

Needs Node 22+ and FFmpeg (`brew install ffmpeg` on a Mac).

```bash
npm install
npm run setup      # downloads headless Chrome and the Parakeet speech model (~700 MB)
npm run doctor     # confirms ffmpeg, browser, and model are in place
```

## Use

```bash
node bin/clipforge.mjs build ./clips \
  --name rate-myths \
  --hook "The one thing nobody tells you" \
  --lower "Kyle Melvin|Mortgage Lender · NMLS #000000"
```

Output lands in `videos/rate-myths/final.mp4`. The folder also holds:

| file              | what it is                                                            |
| ----------------- | --------------------------------------------------------------------- |
| `cut.mp4`         | the trimmed, stitched footage with no overlays                         |
| `cut.json`        | which seconds of each source clip were kept                            |
| `transcript.json` | the word-level transcript; **edit misheard words here and re-run**      |
| `captions.srt`    | captions as a sidecar, for platforms that take uploaded captions       |
| `index.html`      | the HyperFrames composition, if you want to restyle it by hand         |

Re-running the same command without `--force` reuses `cut.mp4` and `transcript.json`, so fixing
a word (“DSCR”, a street name, your NMLS number) and re-rendering is one step.

### Options

```
--aspect 9:16 | 4:5 | 1:1 | 16:9     frame shape (default 9:16)
--fit cover | contain                 crop to fill (default) or letterbox
--no-trim                             keep every pause
--silence-db -35                      quieter than this counts as silence
--min-silence 0.5                     pauses shorter than this are never cut
--pad 0.18                            seconds of breathing room kept around speech
--quality draft | looks | delivery    draft renders fastest for a check, delivery for posting
--force                               redo everything from the source clips
```

### Tuning the trim

If the cut feels choppy, raise `--pad` to 0.3 or `--min-silence` to 0.8. If room noise is being
kept as speech, lower `--silence-db` to -40. The log prints how many seconds were removed per clip.

## Handing clips to Claude

Drop the clips in a Google Drive folder (or anywhere the session can fetch them), name them in
order, and say what hook and lower-third you want. The pipeline runs the same way in a cloud
session. A 30-second video renders in a couple of minutes on a 4-core box.

## Logo.dev MCP server

`.mcp.json` registers the [Logo.dev](https://logo.dev) MCP server (`logo-dev`) at project scope,
so Claude Code picks it up automatically when opened in this folder. It needs a one-time sign-in
per machine:

1. Start Claude Code in this folder and run `/mcp`.
2. Select **logo-dev**, then **Authenticate**.
3. Sign in to Logo.dev in the browser window that opens.

To add it outside this project instead, run
`claude mcp add --transport http logo-dev https://mcp.logo.dev/mcp`.

## Testing

`npm run test:e2e` generates five synthetic clips with deliberate dead air (mixed portrait and
landscape, one with a long mid-sentence pause), runs the whole pipeline, and asserts on the result.
Generating the clips needs the Kokoro text-to-speech model in `.tts/`:

```bash
pip install kokoro-onnx soundfile
curl -L -o .tts/kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -L -o .tts/voices-v1.0.bin  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```

## Fonts

`assets/fonts/Inter-*.woff2` are Inter (SIL Open Font License), copied from the HyperFrames
`talking-head-recut` skill assets.
