# 2026-10-20 — Switchboard V2: recomposed for the phone, voice auditions

Kyle's third brief of the day, pasted in full with the storyboard re-attached. The ask: keep V1, build V2
separately with portrait composition as the main improvement (bigger product visuals, easier copy, a more
memorable ending), a new nine-line voiceover with a revised timeline, two voice auditions (British preferred,
Australian as the alternative) before the final render, and a no-voice version. The prompt also referred to
two standalone pictures (floating windows, prompt bar) that were not attached; the cleaned storyboard panels
stood in for both.

## Voice auditions

Audition line set from the brief, level-matched, 0.4 s of silence either side:

- **A, British:** Kokoro `bf_emma` at speed 0.95. Chosen over `bf_isabella` for the lower register
  (median pitch 183 Hz vs 205 Hz, measured by autocorrelation since nobody here can listen).
- **B, Australian:** Piper Willow (speaker 9) at length scale 0.9. Kirra (speaker 3) is lower still
  (141 Hz) but her takes carried extra syllables in the earlier transcription pass.

Sent as `.m4a` in chat and as title-card MP4s on the artifact page. The brief said to continue the edit
while he chose, so V2 was finished in both voices: the swap is a re-mux, not a re-render.

## V2 edit: `graphics/switchboard-v2/comp.html`, output `videos/switchboard/v2/`

Reuses V1's cleaned and upscaled panels, backgrounds, streams and logo cutout from `graphics/switchboard/`.
Each scene now shows a crop of the 4× panel at or below 1:1 of the upscale (no further softening), filling
the width, with the headline below at 96 px Fraunces and card text at 44–54 px Inter.

1. 0–3 Hook: the four AI windows at full width; each window is its own feathered crop layer that comes
   forward in turn (Claude, ChatGPT, Gemini, Perplexity) while the whole shot pushes in.
2. 3–6 Just ask: tablet logo crop, a 150 px prompt bar typing the question, copper submit pulse; the pulse
   grows into a warm flash that carries the cut into scene 3.
3. 6–9 Better question: card with the question, then "Sharpened" with three teal chips (Target market,
   Pricing, Risks) popping with a highlight sweep. No wall of text.
4. 9–12 Perspectives: hub and three cards at 0.9× of the upscale, full labels visible; hub glows, each card
   lights and grows a small response window above it.
5. 12–17 Evaluation: close crop on the ChatGPT and Perplexity windows, amber flags "Conflicting advice"
   and "Overlooked risk" on real response lines, then the art dims and the analysis panel rises with the
   same two findings.
6. 17–22 Convergence: streams flow into the hub (crop shifted so the artwork's own pills stay off-frame),
   hub glow, four teal check pills, slow push.
7. 22–25 Result: large final-answer card, three items at 54 px (Recommended approach, Key risks, Next steps).
8. 25–27 Confidence: person-at-laptop crop, slow push and drift.
9. 27–30 Brand: logo at 900 px wide, copper and teal orbits, lockup settled by 27.5 s, held to 30.

## Audio

`tools/audio.py --music v2` is the third score: F# minor to A major at 96 bpm, pad-only opening, sub pulse
from 6 s, soft kick from 12 s, riser into 17 s, wide pad and arpeggio through the convergence, held A chord
from 27 s with a 1.6 s breathing fade. Effects follow the V2 timeline (`V2` flag in the script). `--cues`
places any number of lines; `--speed ""` disables the V1 speed-ups, since the brief said not to rush the
voice. Willow's "One stronger answer" runs 3.1 s, so her cues for lines 7–9 sit at 22.1 / 25.4 / 27.35.

## Delivered

Switchboard-V2.mp4 (British), Switchboard-V2-australian.mp4, Switchboard-V2-no-voice.mp4, auditions, a
contact sheet, all on the same artifact page with V1 beneath. V1 files untouched.

## Open

- Kyle's voice pick (both cuts exist; the page leads with British as the brief preferred).
- Whisper keeps hearing an extra syllable after "Ask once" from both engines; likely a transcription
  artefact on a short final word, but worth an ear.

## Redo: "that is a terrible voice. It's so harsh"

Kyle on the first V2: loves British accents, Emma was far too harsh; also asked for smoother clips.

- **Voice.** Measured the high-band to mid-band energy of every British Kokoro voice on the audition text:
  Emma is the brightest (−12.5 dB), Lily the darkest (−16 dB), Daniel (male) low and dark. The redo uses
  a blend of 30 % Emma and 70 % Lily through `tools/vo_kokoro.py`, which drives Kokoro directly
  (`kokoro_onnx`, blended style vectors) at speed 0.9 and then softens: dynamic de-ess on 5–9.5 kHz,
  low-pass at 11 kHz, a warmth shelf, gentle 2:1 compression, a small room. Voice gain 0.8 instead of 0.85.
  Daniel went through the same chain as an alternate cut.
- **Motion.** Crossfades 0.5 s, no overshoot easing on pops (a mild `soft` curve replaces `back`), window
  layers come forward over 0.8 s with less brightness, the submit flash at 60 % over a full second, sweeps
  slower and dimmer, glows breathe at half rate, flags and cards ease in over 0.7–0.9 s, result card settles
  without a bounce. Kick and UI ticks turned down in the V2 score.

Delivered as the new V2 (female blend), a Daniel alternate, and the no-voice cut; the Australian V2 cut was
retired from the page.

## V3: "just make the thing shorter"

Kyle's own flow, in his words: ask a question, figure out which AI agents are best, get the best prompt,
each one answers, Switchboard analyzes each answer, gives the best of all AI solutions. V3 is that, in
20 s, at `graphics/switchboard-v3/comp.html` (reusing V2's styles and crops) and `videos/switchboard/v3/`:

0–2.6 ask (prompt bar, submit flash) · 2.6–5.2 picks the best AIs (hub and cards light) · 5.2–7.6 builds
the best prompt (chips) · 7.6–10.2 each one answers (three windows illuminate) · 10.2–13 analyzes every
answer (panel: two flags plus "Strongest ideas kept") · 13–14.8 takes the best of each (streams into the
hub) · 14.8–17 the best of all AI solutions (best-answer card) · 17–20 brand, settled by 17.6.

Eight voice lines in the softened Emma–Lily blend at speed 0.92 with `--cues` set so no line overlaps the
next. `tools/audio.py --music v3 --duration 20` is the same language as the V2 bed on the shorter timeline;
effects follow the V3 cues. Delivered as Switchboard-V3.mp4 and a no-voice cut at the top of the page.
