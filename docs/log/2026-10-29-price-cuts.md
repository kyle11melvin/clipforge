# 2026-10-29 — The "Price cuts" reel: a format copy, no talking head

Kyle sent a brief for a reel that copies another creator's format exactly ("Example of price cut homes _1.mp4"
in Drive, `Clipforge/Price cuts`): his photo with a two-line hook and a sage pill, then Zillow price-cut
screenshots cut hard on the beat, then back to the photo so it loops. No audio; he adds the song in Instagram.

## Inputs (Drive worked this time)

The Drive connector listed the folder and `drive.usercontent.google.com/download?id=…&confirm=t` fetched every
file with curl, including the 13 MB example video. The photo was a HEIC with a depth map; ffmpeg and
ImageMagick both refused it, `pip install pillow-heif` + PIL converted it (keep `ImageOps.exif_transpose`).
The "PNG" screenshots were JPEGs inside; PIL does not care. He had already cropped them to the listing
(no status bar, cut at the address), 1290x~2148, so the only crop needed was 36 px off each side to reach 9:16.

## What was built

- `graphics/price-cuts/comp.html`: a `window.seek(t)` composition with pre-cropped 1080x1920 images.
  Hook 0–2.5 s (push-in 100→105 %), seven cuts at 0.5 s each (one beat at 120 BPM, punch-in 100→103 %,
  eased), hook again 1.5 s easing back from 105 to 100 % so the loop reads as one slow move. 7.5 s total.
- Type exactly as briefed: Playfair Display (Regular / Bold Italic / Italic, now in `graphics/fonts/`),
  cream `#F5EFE6` with a soft shadow for the hook at 80 px from y=160, which clears his head (hair starts
  around y=480 in this photo); pill `#A9BCA6` with `#1D2A22` Playfair Italic at 56 px, top 1390.
- Rendered with `render.mjs` (video only, so "no audio" needs nothing extra), re-encoded crf 22 for the
  phone (5.2 MB). Contact sheet from `--probe`, cover from `still.mjs --t 0`.
- Delivery page: https://claude.ai/artifact/Vxr6uQKZcLirt3rLVm1h1H (player, Save MP4, frames, cover, notes).

## Assumptions to confirm with Kyle

- Screenshot order = IMG number order (8646, 8648, 8649, 8651, 8652, 8654, 8655). He said "in the order I
  want them" about files named cut1…cutN that never arrived as such.
- Brief said "about 9 seconds"; the spec adds up to 7.5 s. The example holds its last cut ~1.5 s before
  returning to the hook; doing that here would give 8.5 s.

## Open

- His reaction to the hook size and the pill position; his caption.

## Round two (same session)

- "Make the frame 1 fonts and colors match kylemylenderguy brand" = Coastal Money. Playfair and the sage pill are
  gone: Sora Bold 96 px sand hook with "better deal" in terracotta, left at x=64 from y=150; the interest-rates
  line in Manrope 500 44 px sand at the bottom; a navy gradient scrim top and bottom over the photo (the guide's
  "photo under a gradient scrim") so sand type reads on the wood wall. Playfair stays in `graphics/fonts/`.
- Closing frame now holds 3 s (9 s total) with its own line, "Let's find you / a deal." ("a deal." terracotta),
  rising in word-row by word-row, slow push-in. I had added "Send me the address. I'll tell you if it still
  works." underneath; Kyle: "get rid of the bottom text on the last frame". Headline only.
- Page restyled to the brand palette too.
- Round three: each home 0.75 s instead of 0.5 (he asked after seeing the 0.5 s cut), and the closing line is
  "What are you / waiting for?" ("waiting for?" terracotta), his wording. 10.75 s total.
- Round four: Kyle sent two Instagram preview screenshots: the hook ran under the back button / "Preview"
  label, the interest-rates line and the price block ran under the username + caption block. **Instagram
  Reels safe zone (1080x1920): keep type below y=250, above y=1450, and left of x=940.** Fixes:
  photo frames put the photo at 1230x1640 anchored at y=280 on a navy ground with the scrim blending the
  join, so the three-line hook (88 px from y=290) clears both the chrome and his hair; the bottom line sits
  at bottom:480. Home frames are rebuilt by `graphics/price-cuts/make-cuts.py`: the main house photo
  (second photo on the Zillow page, 808 px) plus the price-cut/price/address block, scaled 0.9 and stacked
  from y=265 so the block ends at ~1420; the map row and the "Est. $/mo" bar are cut out, and the bottom of
  the first photo peeks in under the chrome so it still reads as the page. Probe with the chrome zones
  drawn over the stills (red bands) before rendering.
- 2026-10-30: "the bottom font looks a little too faint to read" on frame 1 → Manrope 700 at 58 px (was
  500 at 44) and the bottom scrim goes almost solid navy in the last quarter. "So much white space below"
  the listings → `make-cuts.py` fills under the price block with navy (24 px of page, then navy).
- "Still big empty space even though it's colored now": the listing is now a 1000 px rounded card (house
  photo + price block, scale 0.9, y=250 to ~1420) floating on the same house photo blown up to 1920, blurred
  45 px and darkened to 60 %. Full frame, no void, and the chrome-covered bottom is just blurred photo.
- Kyle: typewriter on the closing line instead of the rise? Yes: 14 characters a second after a 0.2 s beat,
  terracotta bar cursor, done at about 1.8 s into the 3 s hold, cursor blinking after. Kept the two-tone.
- First home held longer: Kyle knows the listing agent ("a little more visibility, don't make it awkward").
  1.5 s (two beats) instead of 0.75; the rest unchanged.
- **Music.** Kyle: Instagram will not let his account add a song (business account, no licensed library), so
  "set up the music behind it and we call it original audio". A commercial track baked into the file would be
  muted or flagged, so the beds are synthesised: `src/music/beds.py` composes three 12 s beds at 80 BPM
  (one beat = 0.75 s = one home) in A minor, Am7–Fmaj7–Cmaj7–G6, one chord per bar: bar 1 pad + riser under
  the hook, kick drops on the first home, bars 2–3 groove, bar 4 thins under "What are you waiting for?" and
  fades so the loop restarts. Options: deep house (recommended, closest to the example), lo-fi, trap
  half-time. To make the cuts sit on the kicks the picture moved to the same grid: hook 3.0 s (4 beats),
  first home 1.5, six at 0.75, closing 3.0; 12 s = 4 bars. Muxed with ffmpeg (`-c:a aac -b:a 192k`); a silent
  version stays on the page. WAVs are gitignored; rerun the script to regenerate.
- Kyle likes the beds, especially the groove between the houses, and wants the front and back "spiced up",
  the back matching the typewriter. Added to all three: hook bar gets a muted half-time kick, a ticking hat, a
  reverse cymbal and a pre-drop stab; the closing bar keeps a softer groove and plays a keyboard tick on every
  typed letter (same formula as comp.html: 0.2 s + k/14), a ding plus a kick when the "?" lands.
- He asked again whether Claude could add a real song: no. The block is the license, not the account; a
  commercial track baked into the file gets muted or blocked by Instagram's audio matching. Only owned or
  royalty-free music goes into the file.
