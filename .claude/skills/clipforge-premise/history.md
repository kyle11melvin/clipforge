# Premise and script history

Moved here word for word from CLAUDE.md on 2026-11-21. Each entry is one past post: what was built, what Kyle
said, and which file to start from. Where an entry and SKILL.md disagree, SKILL.md is current. Add new entries at the end.

- **Skits (2026-11-10).** Kyle's "Creative" reference (a joey_roquet reel, Instagram-labelled AI content): a loan
  officer skit, six shots, 31 words, no graphics, no captions, two four-second silent stares and a location change
  for the punchline. When he asks for "creative", he means a scripted joke with shot-reverse-shot coverage, not more
  graphics on a talking head. Clipforge cannot generate actors; offer a script + shot list he can shoot (tripod, wide
  two-shot, a close-up per person, one punchline location) and cut it with the silences held. Breakdown in the
  2026-11-10 log.
- `graphics/siriusxm-trick/` (2026-11-11) — a **screenshot meme for the personal account** (his SiriusXM renewal trick:
  tell the chatbot you're cancelling, get the $7.99 promo back; 12 s, silent, reel-cover type, no brand). When he sends
  screenshots of his own accounts, **redact before composing**: crop out account numbers, names and emails, bar anything
  that identifies him (car model) with a grey rounded bar in PIL, keep the raw screenshots out of the repo, and leave out
  any bubble that would need a bar through most of it. Hook on the number, his real message, a black beat, the payoff
  bubble with a stamp, one question at the end.
  **Threads (2026-11-13):** the same idea as a plain-text post on his personal Threads account, with no followers,
  got 266 likes and 88 replies in a day. Threads ranks by replies, not follows; a plain question in his caption voice
  ("am I the only one?") travels on its own. For the lender account: text posts there, Real Estate topic tag, reply to
  comments early. On Instagram, reach comes from Reels; Stories only reach followers.
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

## Tone and content rules

- Comedic, not corporate. The Siri video is a joke about a trillion-dollar company's assistant failing at
  dictation while a self-described "normal person" ships apps and a website with zero code. He rejected a
  "Siri launched in 2011, it's 2026 Apple" timeline as preachy. He liked "Who is Morgan?" and ending with a
  question to the audience ("Does anyone else's Siri do this?", "Tag the friend whose Siri needs help").
- His real dictation fails, usable as evidence: he said "Sorry about your Oregon loss", Siri typed
  "Sorry about Morgan's loss" (use this exact wording, it matches his screenshot); he said "voice-to-text",
  Siri typed "voice to talk".
- Facts he wants stated: knows zero code; built six apps (ANVIL, Ledger, The Edge, Markup, Switchboard,
  Huddle); built the website defenditownit.com (VA home-buying site "powered by Rev Mortgage").
- For a mortgage explainer with b-roll: when he says a number or a trend ("housing prices in 2008 went
  down"), cut to a chart of that exact thing with real data and a visible source. Full-screen cutaway for
  charts, picture-in-picture for small stat callouts. He asked Claude to make that call per graphic.
- Math posts (approved 2026-10-11, "Wow. Good work."): hook question → assumption cards with counters and
  a visible source (Freddie Mac for rates) → to-scale chart → buy-now vs wait table → stamp → punchline →
  a question back to the audience ("Still waiting?"). Round example price ($1,000,000), P&I only, with an
  on-screen "example, not a quote" footer. Spell out any assumption made from a garbled brief in the report.
