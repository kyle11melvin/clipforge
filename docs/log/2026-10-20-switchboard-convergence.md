# 2026-10-20 — Switchboard commercial, "The Convergence"

Kyle handed over a 30-second commercial brief for Switchboard (his AI-orchestration app) that he and
ChatGPT had approved: ten frame-exact scenes, a voiceover script, a music arc, and a 1080x1920 / 30 fps /
900-frame spec. The storyboard images he mentioned never arrived in the session (the uploads folder was
empty), and an earlier conversation he asked about ("Where is the convo that we had") is not visible here.
The cut was built from the written scene list.

## What clipforge could and could not do

The renderer (`src/graphics/render.mjs`) draws any HTML composition frame by frame, so everything visual
was possible in one composition: 3D perspective, parallax and camera moves (a small projector in the
script places every window from world coordinates and a camera), glass panels, glowing light streams
(SVG paths with blur filters, dash offsets and pulses placed with `getPointAtLength`), masks, scene
cross-fades, and exact frame timing. What the repo lacked:

- **Voiceover.** No TTS in the repo. Kokoro (the model `test/say.py` already referenced) was installed
  from PyPI and the ONNX model fetched from Hugging Face into `.tts/` (git-ignored, ~350 MB). Nine lines
  rendered in four voices; `am_onyx` is in the cut.
- **Music and sound design.** No generator and no licensed track. `graphics/switchboard-convergence/score.py`
  synthesises the arc the brief asked for in numpy (D-minor pads, a 100 bpm pluck sequence, an Eb tension
  tone under the evaluation, a noise-and-sweep riser into a boom at 21.55 s, a D-major add9 resolution,
  a three-note bell logo at 28.1 s), mixes the voiceover over it with ducking, and FFmpeg loudness-normalises
  to about -15 LUFS. A real composer or a licensed track would beat it; the timing map is in the script.
- **Real logos.** The Logo.dev MCP server could not connect (proxy 403). Model windows use coloured dots
  and wordmarks, never redrawn logos.
- **Real-world footage (scene 9).** None supplied; a CSS laptop in a warm room stands in.
- **The Switchboard logo.** Only the 400 px home-screen icon from the Siri post existed. It was cropped,
  masked and upscaled to `switchboard-icon.png`.

## The composition: `graphics/switchboard-convergence/`

`comp.html` follows the house contract (`window.seek(t)`, no CSS animation) with a scene table that matches
the brief's frames exactly. New helpers worth reusing: `proj`/`place` (3D projection with depth fog, blur
and z-order from a camera), `rise` (word-by-word headline rises, now built by splitting text nodes),
seeded particles on their own slow dolly, the stream rig in scene 7. Render time: about 7 minutes for 900
frames on the 4-core session box. Audio is muxed afterwards with FFmpeg; `video.mp4` is picture only,
`final.mp4` is the deliverable.

## Scene 7

Three windows orbit a Switchboard "Synthesis" panel on a tall ellipse (x ±310 → ±230, y ±560 → ±380 world
units) while the radius tightens; copper, blue and violet streams draw in from 20.0 s, pulse, and intensify
from 20.9 s; the bloom and a white flash land at 21.55 s on the boom; the windows dissolve and the panel
flips to "Top answer". The camera pulls back 300 units over the shot.

## Delivery

Private artifact page with the player, Save MP4 (downloads capability), open-in-new-tab link, the ten-frame
contact sheet, scene list, a caption, and the missing-items list.

## Open items

- Storyboard images: attach in chat, then match the look to them.
- Scene 9 footage: 3 s of Switchboard on a laptop by a window.
- A vector or high-resolution Switchboard logo.
- Recorded voice and a licensed track, if the synthetic versions are not good enough for a launch.
- Confirm that the example answers, the "Selected" routing and the four findings read like the real app.
