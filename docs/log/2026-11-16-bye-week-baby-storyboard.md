# 2026-11-16 — bye-week baby, second pass: the storyboard cut, and the memory problem

Same day as `2026-11-16-bye-week.md`, in the chat that started the job ("Funny video with daughter"). Kyle had two
chats building the same reel and asked which to use, then to combine them. This chat is the one he works from.

## What he said

- On the combined cut with the heart monitor: **"be more creative … I literally just did a video where my heart rate
  was going up … I'm not trying to do the exact same video over and over."** No BPM / blood-pressure monitor again
  unless he asks. He liked the chill opening.
- His storyboard: Broncos on the bye week, the guy sips his coffee and takes a relaxing breath, "Honey, we're going
  into labor, she's coming", "What?", he sits up, then the baby in his hands.
- His idea for motion: storyboard here, have **Grok or ChatGPT animate the frames** (he pays for both), send the clips
  back, clipforge ties them together. Agreed; the page carries each frame with a Save button and a copy-paste
  image-to-video prompt.
- "I'm wondering if I'm working off the right memory." He was not: see below.

## What was built

`graphics/bye-week-baby/comp.html` (10.2 s, four AI frames, jpgs gitignored; `shock.jpg` is new: bolting upright,
coffee flying). Beats: 0–3.7 recliner, "Broncos fans on the bye week", "No stress this weekend.", then MY WIFE:
"Honey… she's coming." → 3.7–5.3 "WHAT?!" → 5.3–7.0 delivery room, "Me on the bye week" → 7.0–10.2 "Welcome to Broncos
Country, baby girl." with an injury-report chip ("Dad: questionable (sleep)"). The running gag replaces the monitor: a
schedule card (Wk 9 at Carolina / Wk 10 BYE / Wk 11 vs Las Vegas, real schedule) whose BYE is struck by a "schedule
change" alert and flexed to "Dad vs. Baby Girl". `src/music/byeweek_flex.py` is its bed (pad, chime on her line, needle
drop, broadcast sting, Brahms' Lullaby on a music box; needs scipy). The other chat's version stays in `graphics/bye-week/`.

Canva route that works for full-size generated images: put the media on a page of a scratch design (`edit-design`
`insert_fill`), commit, `export-design` as jpg, curl from `export-download.canva.com` (now on the Default allowlist).
Changing the size in a signed `media.canva.com` thumbnail URL is not allowed.

Page: https://claude.ai/artifact/UJjktSJW9FX8oCGWy7xu1p

## Round three: his second storyboard ("be smarter … not quite enough graphics")

Kyle: Sunday morning after a lot of stressful weeks, Broncos bye week, he finally sits down relaxed → his wife from the
other room, "Honey, it's time" → him perked up, "what the…" → "Next Sunday…" → him with his daughter in his arm on the
couch watching Sunday football. He will animate the frames in ChatGPT or Grok. He likes the character and the graphics
("you've been using a lot, which is good, but not quite enough").

`comp.html` is now that, 10.8 s: 0–4.4 recliner, "Broncos bye week. Finally.", the schedule card with real results
(Wk 8 vs KC W 28–24, Wk 9 at CAR W 26–21, both tagged NAIL-BITER, Wk 10 BYE stamped FINALLY), at 2.6 a punch-in and a
white speech bubble sliding in from the right edge ("FROM THE OTHER ROOM · Honey… it's time.") → 4.4–6.0 `shock.jpg`,
"WHAT?!", the card turns to SCHEDULE CHANGE, BYE struck and flexed to "Dad vs. Baby Girl" → 6.0–7.1 black card typed
"Next Sunday…" / WEEK 11 → 7.1–10.8 `couch.jpg` (same recliner, foal in his arm, football on the TV), "Welcome to
Broncos Country, baby girl.", card: Wk 10 Dad vs. Baby Girl SHE WON, Wk 11 vs Las Vegas PARTY OF 2. The delivery-room
and hospital frames are out. Page prompts cover three clips (relax + hears the voice, bolts up, couch with the baby).

## Round four: "you're covering the face … make it look more natural like an actual commercial"

The big stroked meme type, the white speech bubble and the slammed "WHAT?!" are gone. Now: one small tracked super at
the top ("SUNDAY MORNING"), dialogue as clean subtitles at y≈1040–1150 (Inter 700, 56 px, white, soft shadow, no
stroke; her line in italics under a small "FROM THE OTHER ROOM" label), the schedule card shrunk to a 688 px lower third
at y≥1166, "Next Sunday…" in light Inter. Nothing sits above y=1040 except the super, so every face is clear.

## Round five: "very close"

Kyle: not Dad vs. Baby Girl, it is **Mom vs. Husband**; keep the previous-weeks scorecard ("I like scoring previous
week"); "Honey it's time" in its own separate box in a corner; something that looks like NFL RedZone on the TV; for
"Next Sunday" a blue shirt instead of orange; the Broncos logo, as close as possible ("this is not going public, it's
not a public product"); dad and the girl watching the game together.

Canva's image credits ran out after one edit: `relax.jpg` is a clean re-render (four-game grid on the TV, Broncos logo
on the hoodie; the earlier one is `relax-plain.jpg`). `shock.jpg` and `couch.jpg` are PIL edits of the `*-plain.jpg`
files: the TV screen copied from the new frame 1 through a mask of the dark screen, the logo lifted from frame 1's
chest, the hoodie and blanket recoloured to navy with an HSV mask grown through shadows and highlights (rough at his
left shoulder). The corner box is `.honey` at (560, 872). Told him to have ChatGPT redo frame 3 cleanly before animating.

## Round six: side angle, "my water broke", and a handoff brief

Kyle: straight-on makes no sense with the TV behind him; turn him to the side, legs on the lounger, coffee; "honey it's
happening"; the lounger collapses and the coffee goes up; next Sunday, Broncos game, holding his daughter, new colour.
Lines he then gave: "I finally get to relax… Broncos on a bye", "Honey… my water broke". Then: "give me something to
give to another AI agent like ChatGPT or Grok … they take it over the top … I pass it back to you."

Canva gave two more images before the credit quota closed again (it seems to refill slowly; three parallel jobs fail,
one at a time sometimes works): `side-relax.jpg` (profile on the recliner facing a four-game TV, Broncos logo hoodie)
and `side-fall.jpg` (recliner collapsing, legs up, coffee flying). `side-couch.jpg` is a hand-made placeholder (navy
recolour plus the foal bundle pasted from the front-on frame). The comp uses the side frames; her box sits top right
at (500, 256). `docs/handoff-bye-week-baby.md` is the brief for ChatGPT / Grok (three 5 s clips, no text, bottom third
clear); it is on the page with the two reference frames. Next: he sends the clips, cut them under the same graphics.

## The memory problem

`main` had not moved since 2026-11-06. Every session from Nov 8 to Nov 16 pushed its log and its CLAUDE.md changes to
its own `claude/*` branch and none were merged, so each new chat started from the Nov 6 brief and missed everything
after (the "idea, not a format" lesson, no baked music on personal memes, the reach formula, the looser talking-head
rules). This branch now merges all of them (union of CLAUDE.md). It still has to reach `main`; asked Kyle.

## Open

- His clips from Grok / ChatGPT; then recut on real motion (text, card and sound stay).
- Permission to update `main`.
- Sound: per the 2026-11-08 rule he adds his own song on personal memes; the silent cut is on the page beside the bed.
