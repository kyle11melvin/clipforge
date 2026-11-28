# 2026-11-28 — Stroller math (walking talking head, lender account)

Kyle was on a walk with his son and dog and wanted to shoot a talking head ("not saying I'm gonna post it") to see
what the edit can do. Premise pitched from `clipforge-premise`; he took the stroller one but rewrote the angle himself:
not "do I hand him the down payment", but "here is what I'm doing: $250 a month into an ETF, 5 to 8% a year, what I
expect by 18, I hope it is his down payment. What are you doing?" Script went to him on a page with a Copy button for
his teleprompter app. He shot one continuous 51 s walking take and ad-libbed around the script.

## Footage

- Drive `Clipforge/Walk and talk` (49 MB, 1080x1920 HEVC, already SDR) came down with the usercontent URL. A second,
  unlabeled clip from the same minute sits in his Drive root, is not link-shared, and returned the sign-in page.
- One take, no dead air to trim. `cut.mp4` was made by hand: trimmed at 5.58 s (the "hope everyone had a great
  Thanksgiving" greeting, so it opens on the walk) with 7% punch-ins at 9.0, 20.5 and 38.5 (out at 13.9 and 31.8),
  keyframe every second; `transcript.json` is the whisper transcript shifted by 5.58 s with the stumble at
  "at an 8%, 5-8%" shown as "at 5 to 8%" and "he'll sort of down payment" as "that'll be sort of a down payment".
  Both are guesses at his words; flagged to him.
- Numbers: $250 x 216 months = $54,000 in; $87,300 at 5% and $120,000 at 8%, compounded monthly. He said "$87,500",
  so the screen says $87,500.

## Round one (never rendered in full)

Type above his head, a flat sand "savings app" card with a line chart, and the brass key from winter-swipe on "down
payment". Kyle, before seeing the cut: "You're already repeating some of the same graphics with the key. I want cool
looking things ... a 3-D kind of look to them ... they pop."

## Round two: everything big is real 3D

`graphics/stroller-math/overlay.html` (one alpha layer, `#zones` for the Reels chrome) and `assemble.sh`:

- **Extruded type.** Each big word is ~24 copies stepped back in Z inside a `preserve-3d` line that sways in
  perspective, the deepest copy carrying the cast shadow. Words pop by scale on their spoken time. No opacity on
  anything extruded (opacity flattens `preserve-3d`).
- **"$250"** at 318 px spins in above his head, then "a month → ETF".
- **The math, full screen on paper** (15.35–31.75 s) with him in a corner circle: 18 columns on a stage, drawn on a
  canvas with a small perspective camera that orbits 22° during the beat. Navy = what he puts in (rises year by year
  as the counter runs to $54,000), green = growth at 5%, pale green = the extra up to 8%. Counters land on his words.
  Footer: "Example: $250 a month for 18 years, compounded monthly. Not a promise."
- **The home:** a real photo (Unsplash, Avi Werde, free licence, `house.jpg`) as a tilted card over its own blurred
  copy, with a paper tag "his down payment".
- **His question** as extruded type, a drawn terracotta underline and a Caveat "drop your comments below" on the last
  line, ending on his smile.
- Captions: rounded, `--caption-y 0.19`, hidden under the type and for the whole paper beat.
- Sounds from `sfx.json` through `chalk.py` (needs `pip install scipy`). Not heard by Claude.
- Cover: `cover.html`, the rate-wait two-tone look on the smiling last frame (44.8 s).

The alpha render takes about ten minutes (the blur filters on the chart are slow). `shot.mjs`-style probing (Playwright
screenshot with `omitBackground`, composited over footage frames at full size) was much more useful than the 360 px
`--probe` tiles for judging depth.

Open: his verdict; sound levels; the two guessed caption lines; whether the Thanksgiving opener goes back; the second
clip.

Delivered: page "Stroller Math Reel" (video, Save MP4, stills, cover, caption draft) and the master in chat. The alpha
render took about 22 minutes, most of it in the paper beat (full-canvas blur on every frame); speed that up before
the next round. Measured levels: his voice mean -20.8 dB, sound effects mean -32.4 dB at `SFX=0.5`.

## Round three: the tight cut

Kyle on round two: "Not bad!!" Then: cut the dead space and the ums, make the graphics pop more, get rid of the small
picture of him ("I don't need to be in the entire thing"), "tighten and clip a lot. Make it tight", and on the chart
"give me an arrow and % going up".

- **Word timing.** Whisper's word times on this take were up to 0.7 s late (round two's graphics were landing late).
  Checked by transcribing short slices: `hyperframes transcribe -e parakeet` (after `npx hyperframes models install
  parakeet`, 640 MB) is right, and it writes the ums as words. An energy-based pause detector was useless outdoors.
  Parakeet also heard "I hope that helps for his down payment on his home, or at least with his education".
- **`graphics/stroller-math/tight-cut.py`** holds the keep-list (Parakeet word edges), writes `cut.mp4` (45.2 → 31.6 s),
  the remapped `transcript.json` and prints the new word times. Out: every um and uh, "at an 8%" (a false start),
  "So I was thinking like", the second "by the time he's 18 years old", "obviously", and "but I was just thinking about
  that and". Face segments alternate 1.0 / 1.08 zoom so jump cuts read as punch-ins. After each change the result was
  re-transcribed to check no word was clipped.
- **Overlay.** Corner circle gone; the paper beat is a hard cut in and out on picture cuts. Header steps through
  "$54,000" → "5–8% a year" → "$87,500 and $120,000". A terracotta arrow rides the column tops as the green stacks on,
  and an extruded "▲ 122%" counts up beside it (62% at $87,500, 122% at $120,000, both against his $54,000). Camera
  starts close and pulls back as the columns grow. Words slam in with more overshoot and pulse when a number lands.
- **Render speed.** `ctx.filter = blur` on the full canvas and the SVG turbulence grain were the 22 minutes. Shadows are
  now drawn on a 135x240 canvas and scaled up; the grain is one seeded data-URL tile.

## Round four: the director's notes

Kyle asked for a director's critique of round three, then "Go" on the fixes that need no reshoot ("definitely no
reshoot"). What changed, 31.6 → 25.7 s:

- **The number is on screen from frame one**: "for my son, $250 a month. $120,000 by 18?" over the walk line. This
  breaks the "his own first line as type" rule on purpose, at his go; the captions carry his words under it.
- "and I was just doing some quick math" is out. It **ends on "What are you doing for your kids?"** and 0.9 s of his
  smile from the end of the take; "I'd love to hear more about it" and "drop your comments below" are out.
- Captions hidden whenever type says the same words (the $250 beat, the paper beat, the question).
- Type is Sora and Playfair only (Caveat tag and line removed).
- The Tudor stock house is replaced by a Spanish-style stucco house (Unsplash, ubeyonroad, free licence), street number
  painted out. He offered to make an image or video in ChatGPT; two prompts are on the page with Copy buttons.
- Not changed: the shot itself, the 122% arrow (his request; flagged that it reads louder than "I expect").

## Round five: number timing and the ending

Kyle on round four: "Timing is off with the numbers and then the ending is as well."

- **Numbers.** The counters rolled for the whole phrase and only reached the figure as he finished saying it, and
  "$120,000" was on screen 0.24 s before the cut back to his face. Now each figure is complete within about a third of
  a second of the word starting (`roll1/2/3` in `T`), the columns and arrow still grow underneath, and the paper beat
  holds through "I hope that helps for his" (to 20.45 s), so the final numbers and 122% get over two seconds.
- **Frame-exact cut.** `tight-cut.py` now snaps every edge to a source frame. Unsnapped, picture and sound segments
  differed by fractions of a frame and the concat ran 0.07 s long by the end, so late cues drifted.
- **Ending.** "kids?" gets a 70 ms tail and a softer fade, the smile plays at half speed (1.8 s), and the audio fades
  over the last half second. 26.7 s.
- The smile: after 44.8 s of the take he is lowering the phone and the frame blurs, so the last segment is 44.30–44.80
  at half speed (motion-interpolated, not blended, which ghosted) and its last sharp frame is held 0.5 s. 26.5 s.

## Round six: clean it up

Kyle on round five: "this is not a clean cut whatsoever ... You can cut the very beginning of the video. You already
have numbers up that I haven't even said yet. What are you doing for your kids, cut it, clip the end of it to leave
hanging ... it's actually pretty good but we could do a little bit better ... cut away the stall moments, the math
moments ... if there's a math moment where I have a video just take the video away and put a graphic up."

- The walk line and the first-frame number hook are gone (round four's "number on screen from frame one" was wrong for
  him: nothing appears before he says it). It opens on "Right now I'm putting about $250 a month into a Vanguard ETF",
  one unbroken shot.
- Every cut now sits under a full-screen paper beat: the chart from "By the time he's 18" through "$120,000", then the
  house as its own paper beat for "I hope that helps for his down payment on his home, or at least with his
  education" (photo card, two paper tags). No jump cut is visible on his face anywhere.
- His face returns for "What are you doing for your kids?", one unbroken shot, and it ends on the word. No smile tail.
- No burned-in captions: the type and the paper beats carry every line. 20.6 s.
