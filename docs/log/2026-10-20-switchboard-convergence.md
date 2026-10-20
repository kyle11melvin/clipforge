# 2026-10-20 — "Switchboard Commercial V2: The Convergence" (the written brief)

A fourth brief today, this one a full spec: 22 s, 660 frames, eight scenes with exact copy, a new example
question ("I built an app. How do I turn it into a profitable business?"), four prompt areas, Claude,
Perplexity and Gemini as the selected models (ChatGPT fades back), a written final answer with a ding, and a
one-second brand hold. It calls itself V2; in this repo it is `graphics/switchboard-conv/` and
`videos/switchboard/conv/`, delivered as `Switchboard-Commercial-V2.mp4` so the file matches the brief.

## Build

- Icons for Claude, ChatGPT, Perplexity (from the routing panel) and Gemini (from the opening panel) cut
  from the 4× upscales with luminance alpha; the hub glyph and the convergence hub card likewise.
  `graphics/switchboard-conv/icons/`.
- Scene 1 is the floating-windows panel with a lateral camera glide, then a scale-back as a copper radial
  glow rises across the cut. Scene 2 is the tablet logo crop with a two-line prompt field (the question is
  too long for a pill), typed over 1.9 s, then a push into the field. Scene 3 is the question card growing
  a "Structured prompt" block with four copper chips; a glowing signal dot rises out of it across the cut.
  Scene 4 is HTML: the hub glyph, three glowing model cards with curved links drawing in, and two small
  dimmed cards for ChatGPT and "Other models". Scene 5 stacks three response cards with Done labels and
  one highlight each, landing at 12.3 / 13.1 / 13.9 with the hits, then tilting toward Switchboard in
  perspective. Scene 6 is the hero: three small model cards around the artwork's hub card inside a
  perspective container, insight and weak-spot tags, then SVG streams drawn from each card into the hub
  with a travelling dot and a glow bloom, camera easing back. Scene 7 is the Top answer card with the green
  indicator landing at 19.8 on the ding. Scene 8 is the lockup, held.
- `tools/audio.py --music conv --duration 22`: tension pad with digital ticks, a copper impact at 3.0,
  sub pulse, kick through the responses, pumping pad and riser through the convergence, A-major hold. A
  dedicated CONV effects track: typing, a transformation sparkle, three activation tones (E5, G5, B5),
  three DUMs, shimmer, the ding (E6 bell) and a three-note sonic logo. `place()` now ignores cues past the
  end of the file, which the shorter durations needed.
- QC: 660 frames at 30 fps, 22.000 s, AAC 48 kHz stereo, no frame under luma 26, no overlapping voice
  (cues 0.3 / 3.2 / 6.2 / 9.2 / 12.2 / 15.3 / 19.0 / 20.95), −17.4 LUFS.

## Delivered

Voiced and no-voice cuts and a contact sheet at the top of the artifact page; V3, V2 and V1 below.
