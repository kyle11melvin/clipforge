# 2026-10-20 — The Switchboard 30-second commercial

Kyle sent a written brief (not dictated this time) for a 30 s vertical commercial for Switchboard, one of
his six apps, with a single attachment: a 1024×1536 storyboard JPEG laid out as ten numbered panels with
timestamps and production labels. The brief fixed the scene timings, the voiceover lines and the on-screen
copy, asked for a version without voiceover, and said plainly: no invented capabilities, websites, badges
or launch claims; do not stretch the pictures; do not substitute an animated web page for a video.

## What was built

`graphics/switchboard/` and `videos/switchboard/`. Delivered on a private artifact page with both cuts, Save
MP4 buttons, a contact sheet, the scene list and the voiceover script.

1. **Panels.** `tools/clean_panels.py` splits the storyboard on its grid lines, then removes the scene
   numbers, timestamps, labels and the baked-in headline copy from each panel with OpenCV inpainting (mask
   by brightness inside hand-set rectangles, Telea fill, soft blend). Panels 07 and 08 were drawn as one
   continuous image, so the convergence shot stitches the left strip of 08 onto 07. The icon row was
   removed from the brand panel; the orbit lines survived.
2. **Upscale.** The panels are only 507 px wide. `tools/upscale.py` runs Real-ESRGAN x4 (ONNX, CPU, tiled)
   so the art holds up at 1080 wide. The model is `Meeperomi/RealESRGAN_x4-onnx` on Hugging Face (69 MB);
   `graphics/switchboard/up/` is git-ignored and regenerates in about ten minutes.
3. **Layers.** `tools/layers.py` makes the blurred 9:16 backgrounds, the bright-streams cutout for the
   convergence scene, and the logo + wordmark cutout for the end card (alpha from brightness, stray orbit
   sparkle masked out).
4. **Composition.** `comp.html`, same `window.seek(t)` contract as the Siri post. Art floats in the upper
   two thirds with a push-in or parallax; the headline copy is live Fraunces Bold (downloaded once into
   `graphics/fonts/`), white with the key word in copper, teal or blue, word-by-word rises. Three scenes
   rebuild the artwork's UI as crisp HTML over the blurred panel: the optimizing-prompt card (typing, teal
   highlight sweep), the analysis panel (red and amber findings popping in) and the final-answer card
   (checks lighting up). The brand reveal draws two copper orbits in SVG, settles the logo cutout, and is
   fully still from 28.5 s. Light sweeps on the main cuts; incoming scenes fade in on top so there is no
   brightness dip.
5. **Audio.** `tools/audio.py` synthesises everything with numpy/scipy: a D-minor pad bed at 92 bpm
   resolving to D major on the brand, a soft sub pulse, a sparse pluck arpeggio that thickens into the
   convergence, typing clicks, a submit chime, airy whooshes on the sweeps, a shimmer at the convergence and
   a warm bell on the reveal. Voiceover is Kokoro (local, through `npx hyperframes tts`, voice am_michael);
   lines placed at scene cue + 0.2 s, the music ducked 55 % under speech. Line 9 is sped up 8 % so it clears
   before the last line. The whole mix sits around −20 LUFS.
6. **Render.** `node src/graphics/render.mjs graphics/switchboard/comp.html videos/switchboard/final-video.mp4
   --duration 30` (900 frames in 87 s), then FFmpeg muxes `mix-vo.wav` → `final.mp4` and `mix-novo.wav` →
   `final-novoice.mp4`, both exactly 30.000 s.

## Things learned

- The storyboard route works: one storyboard image in, a finished spot out, as long as the panels are
  cleaned and upscaled first. Real-ESRGAN over ONNX runs fine on the session CPU.
- "AIs" must be written plainly for Kokoro; "A.I.s" reads the S as a letter. Checked with faster-whisper
  (installed into the session, model base.en; feed it a numpy array, its bundled `av` is too old).
- `npx hyperframes tts` inside a `while read` loop eats stdin; redirect `< /dev/null`.
- The Kokoro model downloads from Hugging Face the first time (reachable from the session); ElevenLabs,
  OpenAI, HeyGen and Bing speech are not reachable, so Kokoro is the voice unless Kyle supplies audio.

## Open items

- Kyle's verdict on the synthetic voice; a human read can be dropped in without re-rendering the picture.
- Whether he wants the end card's "See Switchboard in action" to point anywhere (the brief said no link).
- Save MP4 on his phone is still unconfirmed from earlier sessions.

## Second pass, same day: "try another voice and music. lets do an female austrailina"

Kyle liked the cut ("you did really good") and asked for a female Australian voice and different music.
Kokoro has no Australian voice. Hugging Face has `DataCraftsmanAustralia/piper-en_AU-librivox-medium`, a
ten-voice Australian-English Piper model (77 MB, CPU). `tools/vo_piper.py` generates the lines with it:
speaker 9 "Willow" chosen after transcribing all six female voices with faster-whisper (speaker ids 1, 2, 3,
7, 8, 9); Willow and Kirra read cleanest, Willow scored higher. Piper reads at audiobook pace with long
sentence gaps, so the tool trims the ends, caps pauses at 0.22 s, and for the three closing lines runs at
length scale 0.78 and keeps the shortest of eight takes (VITS durations vary per run). Below about 0.7 the
words smear. Phonemes for "AIs" are already right (ˌeɪˈaɪz); whisper just transcribes the word oddly.

`tools/audio.py` grew a second score, `--music pulse`: A major, 100 bpm, a soft kick with the pad pumping
under it, a plucked motif, an airy high pad from 12 s, a wide A-major resolve at 28 s. The first score is
`--music pad`. Cue times for lines 8–10 and the small speed-ups are flags now (`--late-cues`, `--speed`).

Delivered as Cut 3 (Willow + pulse) and Cut 4 (pulse, no voice) at the top of the same artifact page, the
first-pass cuts kept underneath for comparison.
