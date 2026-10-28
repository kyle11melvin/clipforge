# 2026-10-28 — "Soft credit pull" reel: stitched from four takes

Kyle uploaded four takes of the same script to the Clipforge Drive folder (`Oct 28, 2026 at 2-54-45 PM.mov`
… `3-03-04 PM.mov`, 25–28 MB each, 1080x1920 HEVC SDR, 26–29 s, walking selfie through an outdoor mall).
"I didn't get a really solid full take. Each one has its own pros and cons. Use the best beginning of one
and the best ending of the other and stitch them together."

## How the stitch was chosen

Transcribed each take on its own (`npx hyperframes transcribe <take> -d <dir> --json`) and compared the
word timings line by line. Scorecard:

| take | problem |
| --- | --- |
| 1 (2:54) | one-second hang on "soft … credit pull"; otherwise clean, clean ending (spare ending) |
| 2 (2:56) | "I see your credit. I see your application." doubled; ends on "send them this" |
| 3 (2:58) | clean from the hook through "before you take the credit hit"; ending trips ("if what I qualify for, send in this video") |
| 4 (3:03) | "Fair. Here's what I s— here's how I do it." stumble; tightest ending of the four |

Cut: take 3 from 0 to 21.25 s (through "credit hit", silence 20.97–21.49 found with `silencedetect`), then
take 4 from 21.00 s ("Know someone who keeps saying… send them this video"). One jump cut, on the breath.
Takes 2 and 3 are the bright outdoor stretch (sky, canopy); 1 and 4 are under the covered walkway, so the
cut moves him from sky to walkway. Acceptable for a walking reel; worth checking with him.

Mechanics: re-encode each piece with ffmpeg (`-ss/-to`, libx264 crf 10, autorotate makes it 1080x1920) into
`clips/soft-pull-stitch/01-open-take3.mp4`, `02-close-take4.mp4`, then the standard
`clipforge build clips/soft-pull-stitch --name soft-pull --caption-style rounded --caption-y 0.19 --quality delivery`.
The build trims each piece's own dead air and stitches them. Transcript fixes before the render: "pool" →
"pulled"/"pull", "poll" → "pull", "deals" → "dings". Final is 24.8 s.

## Delivered

- Artifact page https://claude.ai/artifact/Td2SdfTNwmf2Et7cL6n2k3 : player, Save MP4 (`downloads`), the
  take map, contact sheet, cover + numbered frame strip, the spoken script to copy. Phone file 13.9 MB at
  crf 23; the 80 MB master is `videos/soft-pull/final.mp4` (gitignored).
- Cover `graphics/soft-pull/cover.html` → "Scared to have / your credit / pulled?" over the frame at 2.5 s
  of `cut.mp4` (mouth closed; found with a face-crop strip at 10 fps, since the 2 s strip only lands on
  open-mouth frames).

## Gotchas

- `ffprobe` takes one input; probing two files in one command fails with "already specified".
- `pkill -f "bin/clipforge.mjs build"` from inside a bash command that also contains that string kills the
  command itself (exit 144). Kill by pid, or do not chain the kill with the restart.

## Open

- Kyle's verdict on the splice (sky → walkway) and on the take 4 ending vs take 1's.
- No graphics in this one; he only asked for the stitch. A "soft pull vs hard pull" callout is the obvious
  pip if he wants one.
- His caption.

## "Add a soft pull vs hard pull callout above my head"

`graphics/soft-pull/callout.html` (1080x640, `--alpha`, pip width 1 at y 40, cues in
`graphics/soft-pull/cues.json`): "Soft pull" (sand, Sora 150 px) pops in at 7.8 s as he says it, "No hit to
your score" under it at 11.0 ("nothing dings your credit"), "Hard pull" (terracotta) at 14.8, "Only when
you're ready" at 15.8; out at 19.4, before the cut to take 4. First pass was a two-column card at 84 px in
a 0.8-width pip: it read small and left the sky empty, so it became a full-width stack at 150 px. Delivered
as `final-broll.mp4` (phone file 14 MB); the plain cut stays on the page as the alternate.

- "The soft pull and hard pull stay on the screen a little too long. Remove soft pull after I'm done
  talking about that and then move hard pull when I'm talking about that." Retimed as two separate
  appearances in the same slot: Soft pull 7.8–12.3 s, Hard pull 14.8–17.3 s, nothing in between. Rule for
  next time: a callout lives only while he is on its line, then leaves.
