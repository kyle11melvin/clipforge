# 2026-11-12 — paper-cut style test

Kyle sent three screen recordings of another creator's reels (lshankula: Claude-edited talking heads) in the Drive
folder `Clipforge/Competition` and asked whether that level of graphics is really something Claude can make, and
whether we can do it. He is "totally open to blowing the lid off" the Coastal Money rules for talking heads as long as
the brand image stays mostly the same; he wants "more graphics like he has".

## What the reference reels do

One frame per second through all three (ffmpeg `fps=1,tile`):

- Mixed-size word-by-word type: small serif italic for function words, heavy sans for content words, one accent colour,
  words placed beside and partly behind the speaker.
- Paper cutaways: the speaker as a white-edged cutout on a paper ground, torn strips with condensed caps, rubber stamps,
  film-strip frames, low frame rate like stop-motion.
- Punch-ins and angle changes on almost every sentence (he shoots seated with two cameras).
- A 2x2 grid of the same take in four styles; a hand-tracked 3D logo with a glass shatter (not attempted here).

Everything except the 3D tracking is HTML/CSS type and shapes, a matte, and ffmpeg: the same parts clipforge already has.

## What was built

`graphics/paper-cut/` on the Nov 5 rate-wait take (`Nov 5, 2026 at 11-32-46 AM.mov`, 17.7 s after trim), Coastal Money
colours, Sora + Playfair Display italic:

- `comp.html#bg` — word-by-word type above his head (classes `s` italic 72, `m` 112, `l` 150 terracotta, `x` 200), a navy
  scrim at the top so it reads over signs and sky, and the paper grounds of the two cutaways (SVG feTurbulence grain +
  feDiffuseLighting crumple).
- `comp.html#fg` — cutaway type, torn strips (seeded jagged `clip-path`, moving on twos with a small wobble), the
  "NO NUMBER" stamp (feDisplacementMap for the rough ink edge), the $50,000 count-up.
- `composite.py` — stack: footage, bg, cutout, fg. Outside the cutaways the full-frame cutout goes back over the footage
  so his head covers the bottom of the words. Inside a cutaway it builds a bust sticker at 12 fps: crop, keep only the
  largest matte region (scipy `ndimage.label`; drops ceiling lights, signs and the selfie arm), white cut edge, soft shadow.

```
ffmpeg -i cut.mp4 ... crop=940:1670:70:82,scale=1080:1920 overlaid on the sentences that punch in ... punched.mp4
npx hyperframes remove-background videos/<post>/punched.mp4 -o videos/<post>/cutout.mov
node src/graphics/render.mjs "graphics/paper-cut/comp.html#bg" videos/<post>/bg.mov --alpha --duration 17.7
node src/graphics/render.mjs "graphics/paper-cut/comp.html#fg" videos/<post>/fg.mov --alpha --duration 17.7
python3 graphics/paper-cut/composite.py videos/<post>        # needs: pip install scipy numpy
```

## Lessons

- In his walking selfie the face runs from about y=630 to y=1475, so there is no chest inside the Reels safe zone. Type
  goes in the strip above his head (y 250–600) and tucks behind it. The first pass put words on his mouth.
- Keep the punch-in crop anchored so the top of his head does not move (crop y=82 for a 1.15x punch), or the words lose
  their strip.
- Make the punched footage first, then matte that, so one cutout serves both the footage and the stickers.
- A seated, tripod shot with room beside his head is what makes the reference look designed; ask for one for the next
  post in this style.

## Delivered

Page https://claude.ai/artifact/Nromc5S3qZrnVJj1RMohW3 (video, Save MP4, six-frame sheet, what was matched, what is not).

## Open

- His reaction: is this the direction, or too much (he called the Nov 6 emoji pass "too busy and gimmicky")?
- No sound design yet (whooshes, paper, stamp hit). No cover, no caption: this is a style test, not a post.
- Not attempted: the 2x2 four-styles grid, the hand-tracked 3D logo.

## Kyle's verdict on the test, and round three of the rate-buydown reel

Kyle: "its good just dont like the total blue clip. but the fonts and new graphics are money." So the mixed type, the
torn paper, the stamp and the sand sticker cutaway are in; a full-screen navy ground is out (third time he has said it:
price-cuts, rate-wait, now this).

He then asked for the same direction on the unposted rate-buydown reel (2026-11-11 log), and while that was building:
**"I want the chalk board to swoop in and writing on the chalkboard to make sounds like you're writing on a chalkboard
and the eraser to make a noise."** The board stays; the new type goes on the ten seconds before it.

Round three (`graphics/rate-buydown/assemble-paper.sh`, 30.8 s):

- No hook slide (it was 2.6 s of full-screen navy). The reel opens on his face; the hook is his own first line as type.
- `type.html`: ink type on his cream office wall (sand type vanishes there), terracotta turn, left-aligned. Clip A block
  bottom at y=770/820 with the Clip A cutout laid back over it; Clip B block kept above y=600 and left of x=700 because
  a framed picture and a bookcase sit behind him. "OFFER ACCEPTED" stamp on "accepted". Replaces the rounded captions.
- `board-box.html#t0=9.7&in=9.78&full`: rendered on the full frame, the box flies in from the upper right tilted 16
  degrees and settles with a small overshoot (0.5 s), drop shadow under it. Entrance moved from 9.5 to 9.78 so "rate"
  has time to land before the board covers it.
- Punch-ins in one top-anchored zoompan: +10% on "and still lose money", +8% on "That's exciting", +7% eased as the
  board lands.
- `src/music/chalk.py` + `sfx-events.json`: synthesised chalk strokes (one per letter, tap + band-passed scrape with
  stick-slip chatter) on every line, long strokes for circle/arrows/underline, a two-rub felt eraser at 23.1 s, a whoosh
  and knock for the swoop, a thud for the stamp. Mixed at 0.55 (chalk about 8 dB under his voice).
- With-music cut uses `underbed.py --intro 0`.

The three 4K clips were pre-converted one at a time (zscale/hable, 1080x1920, 30 fps) before `clipforge build`.

Page https://claude.ai/artifact/TUb1JogTpCR8eiUCtesQAL (same link as round two): New with music / New no music /
Yesterday's cut.

Open: nobody has listened to the chalk and eraser sounds; they were set by level, not by ear. Music or no music. The
board still says "keep your cash" where he says "keep the cash".

## Round four: the chalk sound

Kyle: "2 is better" (the no-music cut) "but that does not sound like chalk. it's sounds like annoying and typing not
chalk board writing". The first synth put a click and a short buzzy scrape on every letter, which is a keyboard.
`chalk.py` now writes in a handwriting rhythm: four or five strokes a second of uneven length (0.11–0.26 s) with short
lifts, each a grainy band-passed hiss that swells and brightens through the stroke (random flutter, no periodic
chatter), a dull touch only on the first stroke and now and then, and no per-letter anything. Mixed at 0.45. Music is
off; the page carries the new cut and yesterday's cut. Still set by level and spectrogram, not by ear.

## Round five: smooth chalk

Kyle on the second chalk sound: "that's the most annoying chalk sound. come on make it smooth, not scratching nails on
a chalkboard". The hiss (3.5–9 kHz) and the 2.6 kHz ring were the nails. `chalk.py` strokes are now low-passed at
1.8 kHz (band 280–1500 Hz), 0.2–0.42 s each, overlapping so the hand flows, no touch clicks; the eraser lost its
highs too. Mixed at 0.36 (about 14 dB under his voice). Rule: board sounds are soft and low, never bright.

## Round six: bigger board, "keep the cash"

Kyle: "change the board to say keep the cash and make it larger". Read as the board and its writing (the round-two box
text was small on a phone): `board-box.html` is 952x540 (was 480; bottom edge at y=786, hair at ~820 in Clip C), setup
lines 70 px, equation 78, answer 104, verdict lines 64/68, labels 44. Last line: "leaving sooner? → keep the cash".
Caption on the page matched. If he meant only that one line bigger, the verdict lines have room to grow to ~72.

## Round seven: "keep the cash" bigger, chalk audible

Kyle: "make the keep the cash line bigger. also i want to hear the chalk just dont make it high pitch like earlier".
`board-box.html`: "keep the cash" is its own 90 px piece of writing after a 60 px "leaving sooner? →" (new `after`
field places a line right of another), underline under the whole phrase. `chalk.py`: stroke body 380–2400 Hz,
low-passed at 2.8 kHz, write/stroke events mixed about twice as loud as the other effects; overall 0.5, which puts the
chalk about 6 dB under his voice (the smooth round was 14 dB under and he could not hear it). The target is now known
from both sides: audible, mid-range, never bright.

## Round eight: a real chalk recording

Kyle on the louder synth: "Now the sound is going over my voice and it still does not sound like chalk", and asked how
to get a real clip to the session. He picked `264944_chalk-on-chalkboard.wav` on Wikimedia Commons (fattirewhitey, CC0).
`curl` to upload.wikimedia.org is refused (429 for automated clients); the session's web fetch tool got the file, and it
now lives at `src/music/samples/chalk-on-chalkboard.ogg` with `samples/CREDITS.md`. `chalk.py --sample <file>` plays
the next stretch of the recording under each write/stroke event (pauses over 0.25 s removed, hard taps softened with a
tanh, low-passed at 7 kHz, 30 ms fades), levelled on its own bus (`--chalk-rms`, default 0.05). At the 0.5 mix the chalk
sits 12–13 dB under his voice. The synthesised eraser, whoosh and thuds are unchanged.

Lesson: three rounds of synthesised chalk were three misses. For a sound he will judge by ear (chalk, paper, a pen),
start from a real CC0 recording; synthesise only abstract sounds (whoosh, thud, ticks).

## Round nine: quieter chalk, a board that pops

Kyle on the real chalk: "Much better can we bring the decibels down just a little bit further". `--chalk-rms 0.035`
(about 15 dB under his voice, was 12). And: "I know we're working with the coastal money brand guidelines, but I would
like stuff to pop a little bit more maybe like the chalkboard the writing we need to start opening up the scope and
loosen restrictions guidelines, but maybe get more creative."

`board-box.html#...&full&pop` (the plain box is still there without `pop`):

- A framed slate: 14 px wood frame, darker navy with a soft vignette, seeded chalk-dust blotches and old wipe marks,
  resting 1.2 degrees crooked, a wobble as it lands, deeper shadow.
- Three chalks: bright white (Caveat 700) with a soft glow, orange for the cost ($10,000), mint for the savings
  ($100 / month, "keep the cash"). Colours outside the brand palette, on purpose.
- Specks of dust fall from the chalk while a line writes; the eraser leaves a faint blurred ghost of what it wiped.
- "100 months" in white inside a thicker orange circle with an orange scribble under it; double underline under
  "keep the cash".
- "8 years, 4 months" is a torn paper note with a strip of tape, slapped onto the board (thud), instead of a chalk line.
- Footage punches in another 6% while he says "a hundred months to ever recoup that savings".

Open: whether this much is right or "too busy" (his word on 2026-11-06); `pop` can be dialled back piece by piece.
