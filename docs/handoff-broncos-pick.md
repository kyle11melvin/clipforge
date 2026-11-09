# Handoff: the Broncos "16 straight" reel (2026-11-09)

A brief another tool (ChatGPT, Codex, Grok, a human editor) can pick up. Everything below is in this public repo
except the media, which Kyle attaches himself.

## What the post is

A personal-account Instagram Reel (@ke_melvin style, not the Coastal Money brand) about the Denver Broncos'
26-21 win at Carolina on Sunday 2026-11-08. Goal: more views and followers than last week's reel (about 15K views,
243 shares in 24 hours; average watch 8 of 16 seconds, so keep it near 10 seconds with the payoff by 7 seconds).
No music baked in: Kyle adds the song in Instagram. Vertical 1080x1920, 30 fps.

## The facts

- Final 26-21, Broncos' fifth straight win, now 7-2. Bye week next; Raiders at home on Nov 22.
- Late in the 3rd quarter, Carolina up 14-13 with the ball at the Denver 1, Bryce Young threw to Tommy Tremble in
  the end zone. Ruled incomplete on the field. Sean Payton challenged; the replay showed the ball hit Tremble and
  never hit the ground, and safety Devon Key came away with it. Overturned to an interception, Key's first in the NFL.
  Denver then drove 80 yards for the go-ahead touchdown in the 4th.
- Nik Bonitto's strip sack of Young with about 1:24 left sealed it.
- It was Denver's 16th straight one-score win, an NFL record (the 2008-09 Colts had 15).

## The assets Kyle has (he attaches these; they are not in the repo)

1. Photo: Kyle yelling, mouth open, holding Asher (toddler, Broncos shirt) who is pointing at the camera. Patio, daylight.
2. Photo: the same spot, both smiling.
3. Screenshot of another account's post: Von Miller on Cam Newton (2016) above Nik Bonitto on Bryce Young (2026).
4. Screen recording (15 s, 1290x2796, with sound) of the Fox Sports Instagram reel of the Key replay. The announcer
   says: "Overturned. This has been ruled an interception for Devon Key, because the ball hit Tremble's hand, never
   hit the ground. Key jumps in there, comes away with the INT clean." The catch is on screen from 0.5 to 1.8 s.
   Instagram's buttons and the caption are baked into the recording (crop x 0-1130, y 560-1660 to lose them).
5. Screen recording (33 MB) of the live TV call: "I think this is an interception… it is an interception."
6. Cutouts already made with background removal: both of them from photo 1 (`yell-cut.png`), both from photo 2
   (`smile-cut.png`), Asher alone chest-up pointing (`asher-bust.png`). Kyle can export these from the artifact page.

## What has been tried (all in `graphics/broncos-pick/`)

- `comp.html`: photo hook → split screen (replay above, the two of them draining to black-and-white below with a
  score bug and a BPM box) → 2016/2026 card → smile payoff. Kyle: "way too similar to last week."
- `comp2.html`: cold open on the replay with "OVERTURNED." → smash cut to his face → 1-to-16 counter behind the
  cutout → "I have a toddler. I don't need this." → "Bye week. Thank God." Kyle: "this is really the best you got?"
- `comp4.html`: slow-motion of the catch with a telestrator ring while the announcer says "never hit the ground";
  "Refs said incomplete." → Asher slides in pointing at it, "My toddler: interception." → the real ruling → smash
  cut → 16 straight → Asher alone: "He thinks this is normal."

## Kyle's direction, in his words

- "Be a creative and art director. Imagine you're trying to get more followers and more likes on your reel. You
  don't have to keep the same format."
- "Get the announcers' play calling at the very beginning… then cut to Ash and me with our mouths open like oh, and
  'go Broncos, pull off another fourth-quarter victory' or something like that. Be pretty loose on that."
- "We'll figure out music on our own on Instagram." (Nothing licensed in the file; his personal account can add
  songs from the picker.)
- Last week's reel that worked: Asher laughing "Broncos fans in the 1st quarter", Kyle alone aging in the 4th with
  a heart monitor, "they pull it off. Every time." He wants this one to feel new, not a repeat.

## Look

Nunito ExtraBold, white with a thick black stroke, for anything on photos or footage (his reel-cover type).
Broncos orange `#FB4F14` and navy `#002244` as flat grounds. No Coastal Money, no logos. Keep all type inside the
Instagram safe zone: below y=250, above y=1450, left of x=940 on a 1080x1920 frame.
