# 2026-11-11 — Rate buydown break-even, the chalkboard reel

Kyle sent a full brief (G1 hook → Clip A → one continuous chalkboard across Clips B and C with him in a
picture-in-picture → G6 CTA) with the Coastal Money kit, and the three clips plus a "Cover photo" HEIC in
Drive → Clipforge → Rate buydown. He chose "keep the board up and add on" over cutting to a second board: the
division from Clip B stays on screen and Clip C labels it and writes the verdict underneath; one eraser swipe
at the cut clears only the three setup lines.

## Footage

iPhone 15 Pro Max, 4K 60 fps HLG with rotation metadata, 52–213 MB per clip; Drive's usercontent download URL
worked for all three with curl. **The cut step OOM-killed on three 4K clips at once** (one ffmpeg graph decoding
and tone-mapping all three). Fix: pre-convert each clip on its own to 1080x1920 SDR 30 fps
(`footage/rate-buydown/sdr/`, same zscale/hable tone-map as `src/ffmpeg.mjs`, `-threads 2`), then run `clipforge
build` on that folder. Worth folding into the cut step: downscale per clip before the concat graph.

What he actually says (Parakeet, 103 words; "part rate" fixed to "par rate" in transcript.json):
- A (4.8 s): "Hey there. Did you know that you can pay for a lower rate and still lose money?"
- B (18.2 s): "Let's say you just got an accepted offer. That's exciting. But then you go to lock your interest
  rate and half a percent off the par rate is $10,000. Well let's say the savings is only $100 a month. It takes
  a hundred months to ever recoup that savings. So that's eight years and four months, I believe."
- C (7.7 s): "What you want to do is divide the cost by the monthly savings. If you're staying longer than
  that, buy it down. If you're not, keep the cash."

Indoor office shot, plain wall, head mid-frame, pale shirt → captions above his head (`--caption-y 0.66`,
rounded style), on Clip A only; the board carries the words for B and C.

## The board (`graphics/rate-buydown/board.html`)

Flat navy, everything drawn on a canvas. Each line is pre-rendered once to its own small canvas in Caveat 600
(sand; terracotta for the answer), a soft 0.5 px blur pass under a crisper pass, then two seeded noise tiles
knocked out with `destination-out` for the chalk grain (lettering only, the board stays flat). Write-on is a
left-to-right clip over the line's measured width between the word's start and end from transcript.json
(board time = cut.mp4 time − 4.81); the verdict lines pause at the arrow and finish on the second phrase.
Each line carries its own small rotation (±1.2°) for the uneven baseline. Circle, arrows and underline are
wobbly paths stroked progressively on a scratch layer with the same grain. The erase is a left-to-right clip
sweep over the three setup lines at 18.3 s (the cut into Clip C), 0.7 s, no dust.

Layout (1080x1920): setup lines at y 350/480/610, equation at 790, labels + arrows at 905 (written in Clip C
under $10,000 and $100), "100 months" at 1095 (156 px, circled, x 236 so the circle stays left of x 940),
"8 years, 4 months" at 1226, verdict lines at 1338/1440, underline at 1466. PiP: a 1080x1080 crop of the
footage from y=560 (head and shoulders) scaled to 400x400 with 16 px corners, at (64, 1472), bottom-left.
That square sits inside the Instagram username/caption strip; moving it top-right is the alternative.

## Assembly (`videos/rate-buydown/assemble.sh`)

hook.html (2.6 s) → final.mp4 0–4.81 (captioned Clip A) → board.mp4 (26.8 s) with the PiP overlay and
cut.mp4's audio from 4.81 s (last frame held 0.85 s so the underline finishes) → cta.html (3.5 s). 0.25 s
xfade + acrossfade at every join; silent AAC on the graphics so acrossfade has a stream. ~37.2 s total.

## Cover

`graphics/rate-buydown/cover.html`: his Drive "Cover photo" (HEIC → pillow-heif → 9:16 centre crop) under the
navy two-tone tint from `rate-wait/cover.html`, four lines at 118 px from y=250, terracotta turn, all above
his head (head top ≈ y 700).

## Delivered

Page https://claude.ai/artifact/TUb1JogTpCR8eiUCtesQAL with the reel, Save MP4 / Save cover PNG, a contact sheet, the caption, the numbers on the board,
and what is still open (PiP position vs. IG chrome, "keep your cash" vs. his "keep the cash", no music).
