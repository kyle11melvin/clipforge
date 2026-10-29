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
