# Graphics-only post history

Moved here word for word from CLAUDE.md on 2026-11-21. Each entry is one past post: what was built, what Kyle
said, and which file to start from. Where an entry and SKILL.md disagree, SKILL.md is current. Add new entries at the end.

- `graphics/wait-or-buy/` — the first mortgage-math post (buy now vs wait 5 years) in the Rev flyer look:
  stat cards with counters, a to-scale bar chart, a comparison table, a stamp.
- `graphics/wait-or-buy-cm/` — the same post in the Coastal Money brand: two-tone hook, sand setup slide,
  01/02 numeral rows, oversized counter, DM sign-off with portrait. Start Instagram posts from this one.
- `graphics/siri-post/` — the reference composition Kyle called "absolutely perfect". Start new ones from it.
- `graphics/price-cuts/` (2026-10-29) — a **format copy** reel with no talking head: his photo with a Playfair
  Display hook + sage pill, then Zillow price-cut screenshots hard-cut at 0.75 s each (he started at 0.5 s and
  asked for 0.75), then a closing frame on the photo with one question ("What are you waiting for?"). Video only; he adds the song in Instagram. When he says "copy this format exactly"
  and attaches an example video, match the example's timing and structure, but he then asked for the type and
  colours to be Coastal Money anyway ("match kylemylenderguy brand"), so: structure from the example, look from
  the brand. Photo hooks get a navy gradient scrim top and bottom so sand type reads. A closing frame carries
  one headline only, no line under it (Kyle, 2026-10-29). Playfair Display (4 faces) is in `graphics/fonts/`
  if a brief ever asks for it. He pre-crops Zillow screenshots himself; `make-cuts.py` turns each one into
  a rounded card (house photo + price block, map row and Est. bar dropped) floating on the same photo blown
  up and blurred, inside the safe zone. Kyle, 2026-10-30: "that's it, much better". A flat navy void under a
  screenshot "looks a little weird" to him; fill the frame with blurred imagery instead.
- `graphics/family-growing/` (2026-11-13) — the **photo + type + music** reel for the lender account: one family photo
  full-bleed with a slow push-in, navy scrim top and bottom (write the scrim stops in px, not %), three beats of Sora type
  in the lower safe-zone window, Caveat "message me." at the end. `src/music/warm.py` is a soft numpy-only bed (no scipy
  in the session); ship a silent cut for the picker and a bed cut for Original audio. Family photos stay gitignored.
  **Result: 46 story views, 2 reel likes (2026-11-14).** The lesson Kyle drew with me: the polished brand reel with a
  pitch does not travel; the unbranded, personal, number-plus-question post does (Broncos ~15K, SiriusXM text ~300 likes
  and ~120 comments from strangers). **Reach formula:** something he actually did or saw, one real number, a question
  back ("am I the only one?"), no CTA in the post, the ask in a reply or the caption. Brand graphics are for the grid and
  credibility, not for discovery. **Kyle, 2026-11-14: keep the graphics machine; the ideas have to get better.** So the
  rule is about the premise, not the tooling: every post starts from the formula above, and the graphics serve it the way
  they did in the winners (real screenshots, the real score bug, big type, one number, a question), not as cards with a
  sign-off. Pitch him premises before building.
- `src/music/beds.py` (2026-10-30) — synthesised music beds (numpy + scipy, no samples) composed on a beat
  grid. **Kyle's Instagram account cannot add songs** (business account), so music is baked into the MP4 and
  Instagram labels it "Original audio". Never embed a commercial track. Build the picture on the bed's grid
  (80 BPM = 0.75 s per cut) so every hard cut lands on a kick; the first home can hold two beats. Give him
  two or three styles to choose from; deep house was the recommendation for the price-cuts format. Sound design
  follows the picture: a tick per typed letter under a typewriter line, a hit when the last character lands.
  **He will ask for a real song anyway** (2026-10-30, Dua Lipa, then Calvin Harris "Feel So Close"). Never bake
  a commercial track into the file, even if he says he is not worried. Do this instead: preview songs for him
  with Spotify links (the connector finds tracks; he does not want to dig through the app), then render the
  reel silent at the song's tempo with `comp.html#bpm=128&hook=8&first=3&home=2&tail=8` (beats) so he posts
  it from a creator account with the song from Instagram's picker, business account tagged as collaborator.
  Give him one and two beats per home; tell him to drag the song start to the drop.
- `graphics/rmv-special/` (2026-11-17) — a five-slide Coastal Money graphics reel with **hard cuts** (3/4/5/3/3 s), built
  from a Project brief; `comp.html#zones` paints the Reels safe zone for probes. **Never name a loan program after a
  neighborhood** (Kyle: "RMV special" looks like a special discount for one area, a fair-lending problem); the program
  got a neutral name ("The Address Advantage" in the first cut, his pick pending). Check a brief's program names for this.
- `graphics/winter-buyers/` (2026-11-17) — the **template for a Project-brief type reel**: each line has a `data-at`
  time, one `seek` loop, hard cuts; `#move` adds the push-up transition, `#zones` paints the Reels chrome, `#car` lays
  the same scenes out for 1080x1350 carousel stills (`still.mjs --size 1080x1350`). When a brief says "flat, hard cuts"
  ship that and the `#move` version side by side until he picks one for the series.

## The look Kyle approved (use it unless he asks for something else)

- 1080x1920, 30 fps, 9:16. Navy background `#0E1A2B`, gold accent `#C9A96A`, off-white text `#F3EFE6`,
  muted grey `#9AA4B4`. These are the Rev Mortgage flyer colours; the brand should feel consistent.
- Type: Inter Display ExtraBold for headlines, Inter for chat bubbles and small labels. Headlines are big
  (90–130 px), 3–5 words per line, left-aligned for statements, centred for punchlines. White headline with the
  key phrase or the second line in gold.
- Motion: words rise in one by one; icons pop in with overshoot (`back` easing) and a counter ticking in the
  headline; screenshots slide up with a slow drift; stamps ("NO CODE") slam in from large to small, rotated;
  chat bubbles type out with a blinking cursor; scenes cross-fade over 0.25 s. One beat of nothing before a
  punchline lands. Total length around 20 s.
- Evidence on screen: real screenshots, real app icons cropped from his home screen, his real dictation
  errors. Never staged examples. When a URL matters, show it as a gold pill on screen and also put it in the
  caption, since video posts have no clickable links.
- No invented handles, taglines or sources. If a tag line is needed, ask or leave it out.
