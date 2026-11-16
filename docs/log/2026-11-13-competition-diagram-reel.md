# 2026-11-13 — a fourth reference reel (system-diagram style)

Kyle added one more screen recording to Drive `Clipforge/Competition` (an _anthonygallo story ad, 40 s, also says it is
edited with Claude) and asked whether clipforge can do that on future videos. No build yet; this is the read.

What it does, one frame per second:

- Dark canvas with the graphic on top and the speaker in a small rounded box at the bottom, captions on his box.
- A flow diagram: raw clip → cuts / color / captions / sound / graphics → finished clip, ticks landing one by one.
- Mock app UI: a progress card, an edit timeline with coloured blocks, a bank balance counting up, a download card,
  app-icon chips, a circular minutes counter.
- Serif kinetic type on the dark ground between sections; a 2x2 grid of labelled clips; a checklist over a wide desk
  shot; a title card.
- One AI-generated picture (him eating spaghetti, "this isn't AI slop") and two extra camera set-ups.

Read for clipforge: the diagrams, mock UI, counters, grid, checklist, type and title card are HTML compositions, the
same engine as everything else. The speaker-in-a-box layout is `broll` pip. Outside clipforge: the AI-generated image
(needs an image model; the Canva connector has one) and the extra angles / b-roll (he has to shoot them).

Caution: this layout is graphic-first with the speaker small on a dark ground, which Kyle has rejected three times for
his own reels (full-screen board, hook slide, navy cutaway). The parts to borrow are the diagram, the mock UI and the
checklist as props above his head or in a framed box, not the layout.

## Built on a past reel: the 20% down myth

Kyle: "I kinda wanna see what it looks like now can we use one of the past videos that we did?" Picked the 20% down
myth take (2026-10-22; `20% down myth .MOV` in Drive, 265 MB, pre-converted to 1080p SDR, 30.8 s after trim) because
its script has a number that changes and a cause-and-effect line.

`graphics/20-down-myth/ui.html` (one alpha layer) + `assemble-ui.sh` → `videos/20-down/final-ui.mp4`:

- The 2026-11-12 word-by-word type above his head wherever no card is up (sand on a navy scrim; outdoor sky).
- **Fake app window, "Down payment calculator"** (12.3–21.6 s): $800,000 home, slider at 20% = $160,000 in orange; a
  two-stroke X slams on the 20% right after he says it; on "as little as 3% down" the slider runs down, the cash
  needed rolls to $24,000, everything turns mint and a "✓ as little as 3% down" badge pops.
- **Flow diagram, "How a seller credit works"** (25.05–28.7 s): Seller credit → Buys your rate down → Lower payment,
  each node lighting with a tick on his word, a dot travelling the dashed links.
- Cards drop in from above with a bounce and lift out; footage punches in 8% (top-anchored) while one is up so his
  hair clears it. His layout rules hold: he is full frame, nothing crosses his face, no dark full screen.
- Sounds (`sfx-events.json`, synthesised; new `pop` event in `chalk.py`): whoosh and knock per card, two hits for the
  X, a whir and ding for the slider, a blip per node.

Gotcha: `ui.html` paints a blue probe ground when the URL has no hash; render with `ui.html#render` or the alpha
layer comes out opaque (first composite was a flat blue screen).

Not in it: any AI-generated image or extra camera angle from the reference; no cover or caption (a look test).

## Verdict

Kyle: "Yes, that is absolutely money! I like how you still kept the same brand image and guidelines good work."
Mock-app props (fake app window, slider and rolling counter, flow diagram) are approved for future talking heads, in
his layout. Not yet asked: reposting this cut (it would need the 2026-10-22 cover and his caption put on the page).
