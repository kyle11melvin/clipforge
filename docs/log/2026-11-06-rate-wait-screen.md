# 2026-11-06 — "What rate are you waiting for?" on a live rate screen (the ETF-reel technique)

Kyle sent six screenshots of a braidenshaw reel (AI presenter cut out over a Robinhood-style screen: ticker, price,
past-year pill, glowing 1Y line, "Tracks" and "Top holdings" cards, one-word captions on the chest) and asked, first,
whether clipforge could do that, then "take one of my videos and actually try to edit it towards this style". Mid-session
he corrected course twice: **"not copy their brand image … use a lot of that, change course a little"**, then
**"use some graphics, use some sliding in emojis, make it better … you don't have to stick to the same thing we've been
using, I agree with the colors but change up some shit."** So: keep the Coastal Money colours, loosen the rest, more motion.

## Footage

His Nov 5 shoot in the Drive `Clipforge` folder (five takes of the same script, walking selfie in a plaza, 1080x1920 with
rotation metadata). Script: "What rate are you waiting for? I was talking to a friend that's looking at buying this year
and I asked him that question and he didn't have a number. Waiting with no number isn't a plan. It's just waiting.
Meanwhile, my buyers are getting fifty thousand dollars in seller credits or price cuts. If you're waiting on rates to
drop, what rate are you waiting on?" The 11:32 take is the clean one (no "take two"); `clipforge build` trims it to 17.7 s.

## New in the pipeline: the cutout

`npx hyperframes remove-background videos/<post>/cut.mp4 -o videos/<post>/cutout.mov` (u2net_human_seg on CPU, about
0.45 s per frame, 4 minutes for 17.7 s; weights download once). Output is ProRes 4444 with alpha. The matte is clean on
his face, hair and shoulders, both indoors (IQ-quiz wall) and in the busy plaza; it smears for a few frames when the
selfie arm moves at the frame edge. Composite with ffmpeg: background render + cutout (scaled 0.86, placed at 76,210 so
his head top sits near y=760 like the reference and a navy "desk" band hides the bottom edge) + foreground alpha render.

```
node src/graphics/render.mjs graphics/rate-wait/comp.html videos/rate-wait/bg.mp4 --duration 17.7
node src/graphics/render.mjs graphics/rate-wait/captions.html videos/rate-wait/captions.mov --alpha --duration 17.7
ffmpeg -i bg.mp4 -i cutout.mov -i captions.mov -i cut.mp4 -filter_complex "[1]scale=928:1650[fg];[0][fg]overlay=76:210[a];[a][2]overlay=0:0,format=yuv420p[v]" -map "[v]" -map 3:a ... final-screen.mp4
```

`graphics/rate-wait/`: `comp.html` (background: "01 30-yr fixed" header with the live 7.18% and the past-year pill,
terracotta chart that draws in, flatlines to sand while he says "it's just waiting", "02 My buyers" with the $50,000
counting up, cards sliding in from the sides on each phrase), `captions.html` (foreground: one word at a time in Nunito
ExtraBold, key words in terracotta, the ME / MY FRIEND chat bubbles, emojis that slide in with overshoot: 🤔 ⏳ 💰 🏷️ ✂️ 👇),
`rates.js` (the data), `words.js` (from transcript.json), `comp-app.html` (the first pass in the green app look, kept for
comparison, rendered as `final-app-look.mp4`). The emoji font is Noto Color Emoji from the system.

## Data

fred.stlouisfed.org, freddiemac.com, freddiemac.gcs-web.com, mortgagenewsdaily.com and mortgagedaily.com are all
unreachable from the session (proxy 403 / DNS), including through the web-fetch agent. The 44 weekly values in `rates.js`
came from web search over Freddie Mac's weekly releases and news coverage; missing: 2026-04-02/09/16 (one of them is
6.30 in the archive snippet but undated), all of May, 06-18 and 06-25. The line runs straight across gaps (x is by date).
Nov 5, 2026: 7.18%; a year earlier 6.22%, so the pill reads +0.96 (+15.4%) and the line is terracotta, not green: rates
up is the point of his hook.

## Round two: "too busy and gimmicky"

Kyle's verdict on the emoji pass, from a four-option pick: **too busy and gimmicky** (not "not slick enough", not "the
cutout looks fake", not "wrong idea"). So `comp.html` / `captions.html` are now the quiet version: no emojis, no chat
bubble, no slides with overshoot, no punch on the $50,000. Cards rise 20 px with a fade, one element on screen at a time,
captions plain white, cross-fades only. The "seller credits or price cuts" card sat behind his head, so it is a sage
eyebrow line under the $50,000 instead. Lesson for this format: the technique (cutout on a live screen, one-word captions,
a chart that moves on cue) is what he wanted; decoration on top of it is not. `final-busy.mp4` keeps the emoji pass on disk.

He also asked whether this is a good follow-up to the price-cuts reel ("You want a better deal on a house? Maybe stop
looking exclusively at interest rates.", posted on ke_melvin with kylemylenderguy as collaborator, Calvin Harris song,
333 views). Answer given: yes, same thesis from the other side; make the link explicit in the caption and keep the cover
in the same navy two-tone look.

## Delivered

Page https://claude.ai/artifact/MAAcVbLWH2c7N3SmPY1ebc: the quiet cut and the app-look cut with a tab switch and Save MP4 (the MP4s are published
beside the page and fetched on click), seven-frame contact sheet, cover (frame at 1.3 s), caption draft, the numbers on
screen, what's missing. Also attached in chat.

## Open

- His reaction to the emojis / chat bubble / amount of motion, and whether the Coastal Money version or the app look wins.
- Next shoot for this format: seated, still, chest-up, plain background behind him; the matte is already fine outdoors.
- Music: none baked in; creator-account song from the picker, or a bed from `src/music/beds.py` on request.
