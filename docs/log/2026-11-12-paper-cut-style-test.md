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
