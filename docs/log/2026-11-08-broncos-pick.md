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

## Round two (2026-11-09, 02:00): "way too similar to last week"

Kyle on the first cut: "No, no no this is way too similar to last week. I want you to be a creative and art director.
Imagine you're trying to get more followers and more likes on your reel. You don't have to keep the same format. …
the organ that you're doing the music is terrible. We'll figure something out on our own on Instagram reels for that."
So: a new structure, no music in the file, and he will add the song himself (personal account, the picker works).

`comp2.html`, 9.0 s, `broncos-16.mp4` (announcers only) and `broncos-16-sfx.mp4` (plus a hit on the cut, a tick per
count, a slam on 16, a whoosh; `src/music/pick-sfx.py`):

- 0–2.35 **cold open on the replay**, full screen (`replay-full.mp4`: crop 1130x1300 at 0,420 of the recording,
  scaled to 1669x1920, a crop window pushing in 1.12 → 1.32 biased 78% down so the catch sits mid-frame), the
  announcer's "Overturned" at 0.0 with "OVERTURNED." slamming in on the word, white flash into the cut.
- 2.35–3.05 **smash cut to his face** on "interception": `hook.jpg` at 1.6x on the region x 300–975, y 330–1530,
  a punch that settles, a shake that doesn't.
- 3.05–5.0 **the counter**: orange ground, the two of them cut out (`npx hyperframes remove-background` on a still:
  `yell-src.png` 1080x1440 → `yell-cut.png`, clean on both, 0.5 s), a 760 px navy numeral behind their heads
  ripping 1 → 16 at 10 per second, 16 turning white with a navy stroke and slamming with a jolt, "straight /
  one-score wins" rising over the shirt, NFL RECORD eyebrow at y 1395.
- 5.0–7.0 **the joke**: "I have a toddler." → "I don't need this.", navy type above the heads.
- 7.0–9.0 **the button**: navy ground, the smile cutout, "Bye week." in orange, "Thank God." in white.

The 2016 / 2026 picture is out (another account's post; it slowed the piece). Cover: `still.mjs --t 4.95` (the 16).
Mean −20.2 dB / peak −1.3 dB on the clean cut (only the announcers). The artifact page was updated in place with v2;
round one's files stay on disk (`broncos-pick.mp4`, `comp.html`).

Lessons: a sequel is not a template; after a hit he wants a *different* piece, not the same shape with new words.
"Creative and art director" = lead with the strongest real asset (the broadcast moment with sound), use the photos
as cutouts with type behind the heads, one idea per second, and leave music to him.

## Round three (02:30–03:00): "this is really the best you got? … come on, be creative"

Kyle's structure: the live TV call first ("I think this is an interception… it is an interception"; a new 33 MB screen
recording in his Drive **root**, private, so unreachable: the usercontent URL returns a sign-in page, the connector
caps at 10 MB, and copying it into the shared folder was refused by the session's permission rules; asked him to move
it into `Broncos 11/7`), then the Fox replay, then the two of them "with our mouths open like oh", then "Broncos pull
off another fourth-quarter victory or something". He also floated handing the job to ChatGPT / Codex.

The idea that answers "be creative": **the toddler is the replay analyst.** The controversy (did the ball touch?)
is the hook, Asher's outstretched arm in the yell photo is the punchline. `comp4.html`, 12.6 s, `toddler-analyst.mp4`:

- 0–2.4 slow-motion of the catch as a landscape broadcast insert (recording 0.75–1.95 s, crop 980x650 at 150,1050,
  0.5x: the source is 60 fps so the slow-mo has no interpolation) with a yellow telestrator ring drawing on and
  following the ball (`BALL` keys in insert px), a SLOW MOTION tag, "Refs said *incomplete.*" above; the announcer's
  "never hit the ground" (recording 6.70–8.40) under it.
- 2.4–4.4 freeze (recording 1.95 s), dimmed, the ring breathes, Asher's bust (`asher-bust.png`: 350x480 from
  `yell-cut.png` at 590,160, soft-faded bottom edge) slides up from the bottom with overshoot pointing at the ring,
  "My toddler: *interception.*"
- 4.4–7.85 the replay full screen (`replay-c.mp4`, 3.47 s) with "OVERTURNED." / "INTERCEPTION." on the words.
- 7.85–8.55 smash cut to the two of them tight; 8.55–10.9 the 1→16 counter behind the yell cutout; 10.9–12.6
  navy, Asher alone big, "He thinks *this is normal.*"
- Sound: only the two announcer pieces (`voice4.wav`), −20.6 dB mean. He adds the song.

Portrait crops of this replay put the goal-line action at the bottom of the frame (the Fox caption box sits at
y 1680 of the 2796 recording and blocks cropping lower), so the slow-mo lives in a 1080x716 insert at y 600 with
dark bands above and below; that also leaves room for the headline and for Asher.

`docs/handoff-broncos-pick.md` is a brief another tool (ChatGPT, Codex, Grok) can work from; the cutouts are on the
page with Save buttons so he can attach them. Page updated: toddler-analyst main tab, counter cut second tab.
