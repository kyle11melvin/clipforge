# 2026-11-08 — "16 straight": the Broncos meme sequel, built the same night

Kyle, three hours after the Panthers game: "Do you think you can make another Broncos victory post that you did last
week that went viral? There's 3 photos here. There's also a video and audio in Google Drive clipforge broncos 11/7."
Photos: him yelling with Asher reaching at the camera (patio), the two of them smiling (same spot), and someone else's
2016 / 2026 post (Von Miller on Cam Newton in Super Bowl 50 over Nik Bonitto on Bryce Young today, with the IG button
column still on the right). Drive `Clipforge/Broncos 11/7`: five identical uploads of one 15 s iPhone screen recording
(1290x2796, 60 fps, stereo) of the foxsports / nflonfox reel of Devon Key's pick, with the announcers on the replay.

## The game (web search; broncos.com, milehighreport, nbcsports and espn are all unreachable from the session)

Broncos 26-21 at Carolina, fifth straight win, 7-2. Key's end-zone interception came late in the 3rd quarter with
Carolina up 14-13 and the ball at the Denver 1: Young to Tommy Tremble, ruled incomplete, overturned on Payton's
challenge (the ball hit Tremble, never the ground), Key's first career pick. Denver went 80 yards for the go-ahead
score in the 4th; Bonitto's strip sack of Young with about 1:24 left ended it. **16th straight one-score win, an NFL
record** (previous 15, the 2008-09 Colts). Yahoo's "17th for Nix" counts differently; the team figure is 16.

## What the recording says

`npx hyperframes transcribe` (whisper small.en, downloaded once, 490 MB): "Overturned. This has been ruled an
interception for Devon Key because the ball hit Tremble's hand, never hit the ground. Key jumps in there, comes away with
the INT clean. Then the question is…" "Overturned" at 0.0 s, "interception" 2.3 s, "Key" ends at 4.15 s. The catch
itself is on screen 0.5–1.8 s. The reel's UI (like/comment column, Fox's "ONE OF THE WILDEST PICKS YOU'LL SEE" box,
caption) sits outside a crop of x 0–1130, y 560–1660, so `pick-crop.mp4` is that crop at 1080x1052, the first 4.4 s.

## The cut (10.0 s, `graphics/broncos-pick/comp.html`)

Last week's lesson applied: average watch was 8 s of 16, so the payoff is at 7.3 s and the whole thing is 10 s.

- 0–1.4 **hook**: the yell photo, "Broncos fans in the 1st quarter". Stadium-organ charge under it.
- 1.4–5.7 **the 3rd quarter**: the composition leaves a transparent hole at y 250–1302 and ffmpeg puts the replay
  crop there with the announcers at full level. Over the crowd: a score bug (CAR 14 · 3RD QTR · DEN 13) whose
  status flips UNDER REVIEW → OVERTURNED (flashing, on the word) → PICKED OFF (on "interception"), and a BPM box
  96 → 172. Below the hole: the two of them from the yell photo (both mouths open) draining to the aged black-and-
  white with shake and the red pulse, "the 3rd quarter" in the 150 px above the IG caption zone.
- 5.7–7.3 **then / now**: the 2016 / 2026 picture with the button column cropped off, "and then somehow… 16 straight
  one-score wins." across the seam. Impact, crowd roar, brass stab.
- 7.3–10 **payoff**: the smile photo, "They pull it off. Every time." then "NFL record. My blood pressure too."

Pipeline: `render.mjs … --alpha` (ProRes 4444 with the hole) → ffmpeg: black base, `pick-crop.mp4` overlaid at
0,250 between 1.4 and 5.7 s, the alpha layer on top; audio = `src/music/pick-bed.py` (new lane, as he asked for
different music: organ charge, low drone + accelerating heartbeat + monitor beep, riser, impact + roar + brass,
warm pad + calm pulse) at 0.8 plus `call.wav` (the recording's audio, 4.3 s, delayed 1.4 s) through amix and a
limiter. Mean −14.3 dB, peak −0.1 dB. `broncos-pick-callonly.mp4` has only the announcers, for a picker song.
Photo prep in PIL: 9:16 cover crops of both photos (x offset 180), the panic panel 700x401 → 1080x620 from the yell
photo, the aged version as last week (greyscale, contrast 0.85, warm tint, grain, vignette). Cover: `still.mjs --t 1.25`.

## Honest limits

- The replay is Fox / NFL broadcast footage that Kyle screen-recorded from the foxsports reel. Used because he
  supplied it and asked for it; Instagram's rights match may mute or remove it. If that happens, the fix is a still
  in the box, not a re-upload.
- The 2016 / 2026 picture is someone else's post, reused.
- No real clock on the bug (sources only say "late in the third"), so the bug shows the quarter and the status.

## Delivered

Artifact page (URL in the chat reply): both cuts with a toggle, Save MP4, Save cover PNG, caption draft, cover,
eight-frame sheet, the facts used, what is open. Files are gitignored (Asher is a toddler; the footage is not ours).

## Open

- His read on the wording, the bed vs a song, and whether the 2016 / 2026 card stays (it can be cut; the piece is
  8.4 s without it, jump 5.7 → 7.3).
- Whether Instagram lets the broadcast clip through.
