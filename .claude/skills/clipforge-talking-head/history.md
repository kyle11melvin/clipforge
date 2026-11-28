# Talking-head history

Moved here word for word from CLAUDE.md on 2026-11-21. Each entry is one past post: what was built, what Kyle
said, and which file to start from. Where an entry and SKILL.md disagree, SKILL.md is current. Add new entries at the end.

- `graphics/20-down-myth/` — the first talking-head reel with cards (2026-10-22): landscape Coastal Money
  cards, "20% down" with a terracotta X slamming through it, "3% down", "Seller credit / Buys your rate
  down." Start the next Instagram talking-head post from this one. **Kyle picked the no-card version**
  (`comp.html#nocard`, rendered with `--alpha`): type floating over the footage, no navy panel.
  **Mock-app props (2026-11-13)**: `ui.html` + `assemble-ui.sh` rebuild this reel with a fake app window above his
  head (a down payment calculator whose slider runs 20% → 3% and whose cash figure rolls $160,000 → $24,000) and a
  flow diagram (Seller credit → Buys your rate down → Lower payment), after a system-diagram reel in Drive
  `Clipforge/Competition`. Start a "fake app screen", counter or flow-diagram prop from here. Render it with a hash
  (`ui.html#render`); with no hash it paints a probe background. **Kyle: "that is absolutely money ... you still kept the same brand
  image and guidelines"**, so fake app screens, rolling counters and flow diagrams are approved props for talking heads.
- `graphics/iq-quiz/` (2026-10-23) — the first full-screen cutaway in a talking head: a sand slide with the
  real quiz-page screenshot while he pitches the quiz, then a floating "Comment IQ" when he gives the CTA.
  Kyle wants cutaways "so the camera's not just on my face the entire time"; he cut the numeral rows from
  the slide ("good but get rid of this part"), so keep slides to headline + real screenshot + one note.
- `graphics/rate-wait/` (2026-11-06) — the **live-screen talking head**: Kyle cut out of his footage and put on a rendered
  data screen, after a braidenshaw ETF reel he sent (presenter over a Robinhood-style ticker, price, past-year pill, glowing
  1Y line, cards, one-word captions). Three layers: `comp.html` background (header with the live number, a to-scale chart
  that draws in and flatlines on cue, cards sliding in from the sides with overshoot), the cutout, then `captions.html`
  foreground (one word at a time in Nunito ExtraBold, key words terracotta, chat bubbles, emojis sliding in on the beats).
  **Cutout:** `npx hyperframes remove-background videos/<post>/cut.mp4 -o videos/<post>/cutout.mov` (ProRes 4444 alpha,
  ~0.45 s/frame on CPU, clean on face and shoulders indoors and outdoors; the selfie arm smears at the frame edge, so shoot
  this format seated and still). Place him so his head top sits near y=760 (scale 0.86, overlay at 76,210) with a deep-navy
  desk band hiding the bottom edge; captions on the chest at y≈1400. Recipe in the 2026-11-06 log. Rate feeds
  (FRED, freddiemac.com, mortgagenewsdaily) are blocked from the session; `rates.js` was filled by web search week by week.
  **Kyle's direction for this format:** keep the Coastal Money colours, loosen the brand's rules a little ("I agree with
  the colors, but change up some shit"), but when the pass with emojis, a chat bubble and cards sliding in came back he
  called it **"too busy and gimmicky"**. What stays: the cutout on a live screen, one element on screen at a time, a chart
  that moves on cue, one-word white captions, soft rises and cross-fades. No emojis, no bubbles, no overshoot slides. The
  green app-look version lives in `comp-app.html` for comparison; the emoji pass is only on disk as `final-busy.mp4`.
  The close is the **price-vs-rate math** he asked for: C.A.R. Orange County median over two years (`prices.js`) and the
  rate you'd need today to match the old payment (5.5% as of Nov 2026). When he says "was it worth waiting on the rate",
  this is the screen: price then and now, payment then and now, break-even rate. car.org is blocked; the C.A.R. county
  tables are quoted on ocrealtors.org and instamortgage.com. **Then he pulled back from the cutout** ("not sure we should
  entirely blue screen, maybe keep the background"): `overlay.html` is the version to start from. Real footage, lightly
  graded with a punch-in at each turn of the script (ffmpeg zoompan + eq/colorbalance/vignette, recipe in the log), one
  floating widget above his head that swaps its contents per beat, captions on the chest. The cutout stays a tool for when
  he asks for it. **A voice memo does not pass for a missing line** (2026-11-06): two memos, same phone, outdoors, loudness matched,
  then EQ-matched with the plaza ambience under it, and he still heard a different take ("the sound is totally off",
  so the section was cut). The cutaway itself (`cutaway.html`: oversized numeral counting up, the answer slamming in, one
  Caveat note, spliced with ffmpeg concat) is the right shape for a full-screen math beat; the voice has to come from
  the same shoot. If a line is missing, re-shoot the take or cut the line. He asked for the cutaway "towards my brand
  image but also really cool", so brand slide language with motion on his words, not a dashboard. **No 01/02/03
  numbering on cards or rows** in a talking-head reel (Kyle, 2026-11-06: "get rid of the slide numbers on the cards");
  the oversized numeral is for the dollar figure or the rate, not for counting. **Cover for a Coastal Money talking
  head:** `graphics/rate-wait/cover.html`, the two-tone look (sand lines, terracotta turn, navy tint over the frame) that
  he picked over the white-stroke type on 2026-11-06, so the grid stays consistent with his "better deal" cover.
- `graphics/paper-cut/` (2026-11-12) — a **style test** after three Claude-edited reels by another creator that Kyle
  recorded into Drive `Clipforge/Competition`: mixed-size word-by-word type (Playfair italic for small words, Sora for the
  big ones, terracotta key word) sitting above and partly behind his head, and paper cutaways (Kyle as a white-edged
  sticker on a paper ground, torn strips, a stamp, moving on twos). Recipe in the 2026-11-12 log: punch-ins first, matte
  the punched footage, render `comp.html#bg` and `#fg` with `--alpha`, then `composite.py` (needs scipy). He said he is
  open to "blowing the lid off" the Coastal Money rules for talking heads as long as the brand image mostly holds and
  wants "more graphics like he has". **His verdict: "the fonts and new graphics are money", but "dont like the total blue
  clip"**: the type, torn paper, stamp and sand sticker cutaway are the direction for talking heads; never a full-screen
  navy ground (hook slides included). On a pale indoor wall set the type in ink, not sand. In a
  tight selfie his face fills y 630–1475: type goes above his head, never on the chest. **Redone to the 2026-11-12 rules as
  `final-rate-wait-v2.mp4`**: the navy cutaway replaced by torn paper above his head plus the cash heap
  (`cash.html#...&stacks=5`) under his chin, with sounds; `composite.py --overlay=... --sfx=...` builds it. Ask for a seated tripod shot
  with room beside his head for this style.
- `graphics/rate-buydown/` (2026-11-11) — the **chalkboard talking head**. Start from `board-box.html` and
  `assemble-box.sh`, the version Kyle steered to in round two. Round one followed his brief to the letter (full-screen
  chalkboard under Clips B and C with him in a small window, then a "DM POINTS" slide; `board.html`, `assemble.sh`,
  `cta.html`) and he reversed three things: **"get rid of the slide with the DM, just cut the video after I say keep
  the cash"**, **"start the scene with my face … bring the chalkboard up when I start talking about numbers, not at
  the beginning of the clip"**, and **"make the chalkboard not so large … a box like a picture in picture, not take up
  the entire screen"**. So the standing shape for a math talking head: hook slide → him full screen throughout → one
  952x480 navy box (20 px corners) at (64, 246), above his head, rising in a beat before the first number → the reel
  ends on his last word. The box is a canvas: Caveat lines in sand pre-rendered with a chalk grain (seeded noise
  knocked out of the lettering only), each wiped on left to right between the spoken word's start and end from
  transcript.json, the answer in terracotta circled by a wobbly stroke, one eraser sweep at the cut between takes that
  clears the setup lines so the verdict lines can go in their place. Rendered `--alpha --size 952x504` from
  `#t0=<start>` and overlaid with ffmpeg; the footage gets a 7% zoompan punch-in anchored at the top as the box rises,
  which drops his hair ~55 px clear of the box. Captions (`--caption-y 0.66`) run until the box arrives
  (`--caption-hide`), then the board carries the words. **A brief from the Project is a first draft, not a spec**: the
  standing rules in this file (no DM card in a talking head, cutaways only where the words call for them) outrank it;
  build to the rules and say what was changed. Lessons: **three 4K HLG clips in one ffmpeg graph OOM-kill the cut
  step**; pre-convert each clip to 1080x1920 SDR 30 fps on its own (`footage/<post>/sdr/`) and build from that folder.
  Drive's `usercontent` URL handled 213 MB fine. He now sends a "Cover photo" in the Drive folder; crop it 9:16 and use
  the `rate-wait/cover.html` two-tone look. The page's side files cap at 15 MB each, so encode a two-pass ~3.2 Mbps
  copy for the page and attach the full-quality master in chat.
- **Rate-buydown round three (2026-11-12)**: `graphics/rate-buydown/assemble-paper.sh` is now the version to start a
  chalkboard reel from. No hook slide, `type.html` (paper-cut type + stamp) until the board arrives, the board rendered
  with `board-box.html#...&full` so it **swoops in** from the upper right, and `src/music/chalk.py` for **chalk-writing,
  eraser, whoosh and stamp sounds** driven by `sfx-events.json` (Kyle: "I want the chalk board to swoop in and writing
  on the chalkboard to make sounds ... and the eraser to make a noise"). Sound effects go on every graphic that moves.
  The box is 952x540 with 64–78 px writing since he asked for it "larger" (2026-11-12); board text uses his spoken
  words ("keep the cash"), not the brief's.
  **He picked the no-music cut** ("2 is better"). **Chalk must not sound like typing** (his words on the first try:
  "annoying and typing"): no click per letter; soft flowing strokes with nothing above ~1.8 kHz (the brighter second try was "scratching nails on a
  chalkboard"; he wants it "smooth"), but loud enough to hear (about 6 dB under his voice; 14 dB under was inaudible to him). Claude cannot
  hear the result, so say that and ask him to listen.
  **He asked for more pop and looser brand rules (2026-11-12)**: "I would like stuff to pop a little bit more ... the
  chalkboard, the writing ... loosen restrictions ... get more creative". `board-box.html#...&pop` is that board: wood
  frame, dusty slate, bright white / orange (cost) / mint (savings) chalk with a glow, falling dust, eraser ghost, a
  taped paper note, a wobble on landing. For talking heads Coastal Money is now a starting palette, not a fence:
  texture, extra accent colours and physical props are welcome; full-screen navy and emoji clutter still are not.
  **The ending** is a heap of cut-paper cash rising on "keep the cash" with a bell ding (`cash.html`, `ding` in
  `chalk.py`), over the unused smile at the end of the take. When he asks to "bring up" a thing, show one clear object
  ("a lot of cash and then go ding"), not a particle storm across the frame, and draw it in the reel's cut-paper style
  ("sharpen it up to match the rest of the video"), detailed enough to read as the real thing (he asked for the
  bills "a little more realistic"), and **below his face**, never over it. Round nine got "perfect and so much better".
  **Use a real recording for real-world sounds.** Three synthesised chalk sounds missed; he then picked a CC0 clip
  (`src/music/samples/chalk-on-chalkboard.ogg`, credits beside it) and `chalk.py --sample` cuts it to each line,
  about 15 dB under his voice (he asked for "a little bit further" down from 12). Wikimedia Commons has CC0 audio; plain curl to upload.wikimedia.org gets a 429, the web
  fetch tool works. freesound and pixabay are blocked. Only CC0 / public-domain samples go in this public repo.
- `src/music/underbed.py` (2026-11-11) — a quiet bed for under a talking head (electric-piano chords, round sub, felt
  kick, brushed hat, low-passed), with a pad-only intro the length of the hook slide and a beat chosen so whole bars
  fill the footage (`--intro 2.35 --beat 0.77 --bars 10`). Mixed by `assemble-box.sh` at -8 dB on the silent hook,
  sliding to -18 dB (about 16 dB under his voice) before he speaks. Kyle: "willing to try that if you think that's an
  improvement"; deliver with-music and voice-only side by side until he picks.

## Talking-head + graphics rules (from the first experiment, 2026-10-11)

- Kyle's spoken script for the Siri post: "Listen, I have zero code experience and I built six apps and an
  entire website. How can Siri not understand my text messages? Does anyone else have this?"
- The graphics follow the words: icons popping while he says "six apps", the website while he says
  "entire website", the Morgan chat while he asks about Siri. Full-frame cut for a graphic that carries its
  own text; picture-in-picture (lower half, gold border, he stays visible) for a reaction moment.
- **No DM / name / NMLS card inside a talking-head video** (Kyle, 2026-10-22: "get rid of the last one that
  says DM me and gives my name and my NMLS number"). He says "message me" on camera; the caption carries
  the ask. The Coastal Money sign-off stays for graphics-only posts.
- Captions on while he is on screen, off during a full-frame cut (the graphic has its own text). **Caption
  style for Instagram reels: `--caption-style rounded`** (Nunito ExtraBold, sentence case, white, soft
  shadow, no outline), which matches the captions on his earlier reels; Kyle sent a screenshot of one
  ("Keep saying") on 2026-10-22 and asked for the same. The uppercase Inter outline style (`classic`) is
  the Siri-post look. **Position depends on the shot.** Outdoor selfie with sky and a high head:
  `--caption-y 0.19` (caption bottom 19% up, on his chest; Kyle, 2026-10-22: "Move the text so it's not on
  my face"). Indoor shot against a plain wall with his head mid-frame and a pale shirt: `--caption-y 0.66`,
  captions above his head where the wall is darker (Kyle, 2026-10-23, agreed to the suggestion). When an
  overlay sits above his head too, hide the captions under it with `--caption-hide a-b`.
- Pipeline: `clipforge build` for trim + transcript + captions, `src/graphics/render.mjs` for the graphics,
  `clipforge broll videos/<name>/cues.json --output ...` to cut them together. The HyperFrames
  `talking-head-recut` skill is the more complete version of the broll step (cards written per moment,
  transcript-synced); try it on the Monday footage and keep whichever gives the better result. A cue is
  `{at, from, to, mode, says}`; `says` is the phrase the cue sits on, so timings can be re-derived from the
  transcript once audio exists.
- Getting footage in: Google Drive is unreachable from the session. Chat attachment is best. GitHub web
  upload works but Safari's Photo Library picker re-encodes and strips the audio; he must Save to Files
  first and upload from Files. A clip with no audio track cannot be captioned; say so immediately.

## Next planned step

Monday: Kyle shoots the five lines ("Listen, I have zero code experience" / "and I built six apps" / "and an
entire website" / "How can Siri not understand my text messages?" / "Does anyone else have this?") plus a
three-second reaction shot, saved to Files and uploaded with audio. Run the standard job above with the
existing `graphics/siri-post` composition: the cues are already sketched in `videos/siri-post/cues.json` and
only need their `at` times re-derived from the real transcript. The experiment on the silent take is
`videos/siri-post/talking-head-demo.mp4` in the log; known flaw there was a caption overlapping the
picture-in-picture box, so keep captions off while a pip is on screen.

- **Chalkboard safe zone (2026-11-21).** The review run found the rate-buydown board's "keep the cash" and the taped
  "8 years, 4 months" note under Instagram's button column. `board-box.html` now pulls any line (and the note) left of
  canvas x=858 (frame x=922) and `#...&full&zones` paints the Reels chrome for probes. The board keeps its size. The
  posted reel was not re-rendered (footage is not kept in the session).

- **Rate-buydown remix (2026-11-21), a test cut, not posted.** Kyle asked to take an existing reel and "use these new
  features to make it better" to see what the props from the duncanrogoff Skool ad could do. Same footage, chalkboard
  out. `graphics/rate-buydown/remix.html` (`#bg` / `#fg`, `&zones`) and `assemble-remix.sh` (renders every layer,
  about ten minutes): three paper cards spin out from behind his head as he names each number (bg layer under a
  cutout of 9.9–16.4 s only), a full-screen paper beat for the math with him in a 240 px corner circle (ffmpeg crop +
  round mask of the same footage) and 100 month tiles, twelve to a row, flipping as the counter runs so eight rows
  read as 8 years and four are left over, a torn "divide the cost by the monthly savings" strip, and two tiles that
  flip from the question to his answer. Sounds from `sfx-remix.json` (whoosh, pop, thud, ding), about 16 dB under
  his voice. Start a cards / tiles / corner-circle reel from these two files. Notes: his head is left of centre in
  this take (x≈440), so measure it before placing the card origin; `remove-background` needs
  `onnxruntime-node` installed with `--onnxruntime-node-install-cuda=skip` here; the Parakeet timings in `words.js`
  differ from a fresh whisper transcript by up to half a second, so keep using `words.js`. **His verdict: "Looks good!!!"**, with one steer: "I do want to kind of keep my brand
  image look and feel. It's fine to not always do the exact colors though." So cards from behind the head, the paper
  count with a corner circle and flip tiles are approved props.

- **20% down myth remix (2026-11-21), a second test cut, not posted.** Kyle asked for one more past video redone.
  `graphics/20-down-myth/remix.html` + `assemble-remix.sh` + `sfx-remix.json`, one alpha layer over the same take
  (no cutout: it is a walking selfie): a paper "20% down" tag that lands on "20%" and snaps in two (two copies of
  the tag clipped along one jagged line, swinging apart and dropping), a full-screen paper beat with the corner
  circle where twenty blocks (one per 1% of the $800,000 example) flip on, seventeen fall away on "3%", the label
  tile turns from "20% down" to "3% down" and the cash rolls $160,000 → $24,000, then two paper cards joined by a
  drawn arrow for "seller credit → buys your rate down". `ui.html` still supplies the word-by-word type; its app
  window and flow are gated out in the overlay's `enable`. Start a "thing that breaks" or a block comparison from
  here.
  **Round two.** The first pass reused the flipping tiles from the rate-buydown remix for the comparison. Kyle: "It's
  good but I don't like how you did the same chips as the previous post", then, on the graphics in general: "Maybe
  you're not capable of putting the graphics together. We might need to get them from ChatGPT ... Can you do better
  image graphics? Look again at the graphics I recorded on that last video, they are very high quality." A flat
  line-drawn house was tried and thrown away before he saw it. What the Skool ad has that the first pass lacked:
  real images inside the cards, depth (3D tilt, stacked layers, heavy soft shadows, a card out of focus behind one in
  focus), and scale (graphics fill the frame). The comparison beat was rebuilt that way: the real $774,900 listing
  photo from the price-cuts reel as a tilted card over its own blurred, darkened photo, a "20% down $154,980" card
  that falls back and blurs, a "3% down" card that swings forward with the figure running down to $23,247.
  **His verdict on round two: "That's a lot better and I love it and that's a good new rule going forward. I can
  provide you with real pictures or videos."** So before a build, list the real images or clips each prop needs and
  ask him for them.

- **Stroller math (2026-11-28), walking selfie.** `graphics/stroller-math/overlay.html` + `assemble.sh` + `sfx.json`.
  Round one (flat sand app card, line chart, the winter-swipe key) was thrown out on his word before he saw a cut:
  "You're already repeating some of the same graphics with the key. I want cool looking things ... a 3-D kind of
  look ... they pop." Round two is the file to start a 3D reel from: extruded type (stacked copies in Z, swaying in
  perspective), a giant extruded numeral, a full-screen paper beat with 18 columns on a stage drawn by an orbiting
  perspective camera, and a real photo card over its own blurred copy. His verdict on round two: "Not bad!!", then: cut
  the dead space and the ums, no small picture of him, "tighten and clip a lot", more pop, and "an arrow and % going up"
  on the chart. Round three is `tight-cut.py` (45 s to 32 s) plus the arrow and the counting percent.
