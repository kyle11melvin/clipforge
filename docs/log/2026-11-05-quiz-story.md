# 2026-11-05 — Buyer quiz story: reframe only

Kyle shot a 14.6 s selfie for an Instagram story about the free buyer quiz (IMG_8877.MOV, 1:48 PM, 4K 60 fps
HLG, in the Clipforge Drive folder) and asked for one thing: no captions, "there's so much space above my
head, can you help reframe that?"

## What happened

- The Drive file was owner-only. The direct-download URL bounced to a sign-in page, the connector's own
  download caps at 10 MB, and the auto-mode permission check refused `share_file` from the session. Kyle pasted
  the "Anyone with the link" share URL and the 153 MB file came through curl in seconds.
- New `clipforge reframe <clip> --output <file> --zoom 1.3 [--top f] [--x f] [--probe t1,t2,...]`
  (`src/reframe.mjs`): crops a smaller 9:16 window as low in the frame as the zoom allows, tone-maps HLG to
  SDR, copies audio. `--probe` draws the crop box on numbered stills.
- Head top sat 38% down the frame with only shirt below. Showed four framings side by side at 9 s (as shot,
  1.2, 1.3, 1.4). Recommended **1.3**: head clear of the story's top bar, shoulders in. Rendered 1.3 and 1.4
  at full quality (`videos/quiz-story/`, gitignored, 68 MB each at 60 fps) and as 13.7 MB 30 fps delivery
  encodes (crf 22, 7 Mb/s cap) because artifact assets cap at 15 MB.
- Page: https://claude.ai/artifact/JWzxnWsRLcQXy9Tz8r4kuF (1.3 / 1.4 toggle, Save MP4, the framings strip,
  a contact sheet). The 1.3 MP4 was also attached in chat.

## Open

- Kyle's pick between 1.3 and 1.4, and whether Save MP4 works from his phone this time.
