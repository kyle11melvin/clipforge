# 2026-11-09 — "Wait… we won?!": the Bonitto strip sack, then Kyle and Asher

Kyle sent an 11.5 s iPhone screen recording of the Broncos' own Instagram reel (the CBS broadcast of Nik Bonitto's
strip sack and recovery at Carolina, 2026-11-08, Broncos 26-21, 1:24 left; score and clock checked by web search)
and a photo of him holding Asher, both open-mouthed. Ask: the play, then a cut to the two of them shocked they won.
Personal account, so the 2026-11-02 meme look (Nunito ExtraBold, white, black stroke, Broncos orange).

## What was built (9 s, `videos/broncos-strip-sack/broncos-strip-sack.mp4`)

- 0–7.0 s: the play, recording 1.5–8.5 s, with the announcers. The recording is 1290x2796 with Instagram chrome
  burned in (like column from x≈1150 / y≈1330, banner and account row from y≈1850). Clean windows:
  `crop=1130:1500:0:330` for the snap and sack, then a hard punch-in at 4.3 s to `crop=753:1000:537:330` on the
  pile, which follows the ball to the right edge and stays above the like column. Shown as a 1040x1378 card with
  a 4 px white edge at (20,500) on the same footage blurred and darkened. Hook above it, on frame one:
  "Up 5. 1:24 left. / Panthers driving…".
- 7.0–9.0 s: hard cut to the photo (white flash, slam from 1.22 with a shake, slow push toward the faces),
  "WAIT…" then "WE WON?!" in orange popping in above their heads, inside the safe zone.
- Audio: the recording's own sound from 1.5 s, running on under the photo to the reel's loop point (10.1 s in the
  recording), loudness-normalised, faded out over the last 0.45 s. The source reel is only ~10 s long, which caps
  the piece at about 9 s; that matches the "keep a meme under 10 s" lesson anyway.
- `graphics/broncos-strip-sack/comp.html` is rendered with `--alpha`: transparent under the hook while the clip
  plays, opaque on the photo, so one overlay carries both parts and ffmpeg puts the footage underneath. `#safe=1`
  draws the Reels safe zones for probes. The photo (`shock.jpg`) is gitignored like the earlier Asher photos.
- Cover: `still.mjs --t 8.9`. Page: https://claude.ai/artifact/4esdhQDgmoYLFTU2eDsvGd

## Told Kyle

The play is NFL/CBS footage from the Broncos' post; Instagram can mute or remove a reel carrying it. His call.

## Open

- His reaction to the hook wording, the punch-in, and the 2 s photo hold.
- Compare with posting it as an Instagram Remix of the Broncos reel, which keeps their clip licensed.
