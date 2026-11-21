# 2026-11-21 — Competition: the Claude Code Club ad (duncanrogoff)

Kyle: "I just saw a brand new competition and uploaded it to Google Drive Comp check it out."
File: Drive `Clipforge/Competition`, `ScreenRecording_11-20-2026 16-51-08_1.mp4` (65 MB, 74 s, fetched with the
usercontent URL). It is a Skool ad ("I taught Claude how to edit videos and it's INSANE"), a landscape video in a
vertical player, by the same creator as the 2026-11-12 reels. Transcribed with `npx hyperframes transcribe`.

## What is in it (time, his words, what is on screen)

- 0–10 s, face. "The captions, the motion graphics, the cards flying out from behind me": phone-shaped cards of his
  own reels fly out from behind his head and hang beside it, tilted in 3D. The hook shows the product doing the thing.
- 12–17 s, full-screen cutaways. "15 years … Apple, PlayStation, Nissan": a big "15 *years*" (sans + red serif italic)
  over stock-style b-roll, then the brand logos.
- 17–26 s, black ground, him as a small circle in the corner. "a *cheap* AI edit" with an example thumbnail and a
  counter; "this *isn't* one"; four labelled nodes on a dotted orbit (Video, Notes, Skill, Next video); "better faster".
- 26–37 s, white ground. A mock player with a prompt box typing "edit this video for me"; then split screens of him
  beside generic template cards ("Your big idea, made simple.") as the bad examples.
- 38–46 s. "five *months*" on a timeline with thumbnails landing month by month; "two things *changed*" with two
  labelled cards.
- 46–55 s, black. "*one* thing"; the over-long prompt as a white pill that snaps in two; a "BAD CHOICES" stamp.
- 55–62 s, white. "six *jobs*": six grey icon tiles that flip to coloured cards one by one as he names each job.
- 62–71 s. "saved *instructions*": the six pages fan out and drop into a dark box labelled video-editor.

## What is new compared with the three reels from 2026-11-12

- **He leaves his face.** About 55 of 74 s are full-screen graphics with him as a corner circle. Kyle's rule is the
  opposite (face stays, never a full-screen navy ground); the corner circle on a *sand* or paper ground is the only
  part of this that could fit, and only if he asks for it.
- **One two-word title per idea**, top of frame, plain word + red italic word. We already have this (paper-cut type).
- **Every graphic is a count or a sequence that completes on his words** (15 years, five months, two things, one
  thing, six jobs). The six-tiles-flip-as-he-lists-them device is the one worth taking.
- **A thing that breaks** (the prompt pill snapping) for "it was too much". A physical gag on the turn of the script.
- Cards flying out from behind the head needs a cutout matte (we have `remove-background`) and a seated, still shot.

## Offered to Kyle

Not built yet. Two props to add to the approved talking-head kit, both tied to a list he says out loud:
1. Cards from behind his head (real screenshots: Zillow listings, a rate sheet, a text from a buyer).
2. Tiles that flip one by one as he names the items ("three things the seller can pay for").
Needs a script with a spoken list and a seated tripod shot with room beside his head.

## Kyle's reply

Same creator, "I like his stuff". Two things: (1) he is fine with a reel leaving his face when it fits, and liked the
floating, spinning cards; folded into CLAUDE.md. (2) He asked whether splitting the work into six skills, as that
creator did, beats what we have. Answer given: yes in part. CLAUDE.md has grown into one long brief that every
session reads whole, with superseded rules still in it; proposed four skills (premise + script, talking-head build,
meme build, a review checklist run before he sees a cut) and a short CLAUDE.md. Waiting on his go-ahead.

## The four skills (built the same day, at his go-ahead)

CLAUDE.md went from 57 KB to 12 KB. It now holds only what applies to every job (session start, the tools, the safe
zone, how to work with him, the Coastal Money summary) and a table of which skill to load. New under `.claude/skills/`:
`clipforge-premise`, `clipforge-talking-head`, `clipforge-meme`, `clipforge-review`, each a `SKILL.md` with the
current rules and steps; the first three and `clipforge-graphics` also got a `history.md` holding the past-post entries
moved word for word out of CLAUDE.md. Parlay Derby notes went to `docs/parlay-derby.md`. No rule was changed; a
line-by-line check found the only lines not carried verbatim were the 2026-11-12 talking-head rules, which are
restated in that skill. Not yet tried on a real post.

## The review checklist run over twelve delivered cuts

Kyle merged nothing yet (direct push to main is blocked in the session; PR #2 is open) and asked to run
`clipforge-review` over past videos "to check out any differences". The cuts were pulled from their artifact pages
(Artifact read-by-path), one frame every ~1/24 of the length with the Reels safe zone drawn. Positions are read off
small stills, so within about 20 px. Sound was not checked.

Clean: rate-wait v2, SiriusXM, "he got it" (16 straight), bye-week-baby (20 s cut on the page; its baby shot runs
about 5 s against the 8 s rule, and it may not be the last round).

Misses the list found:
- **Right-hand button column (x > 940)** in five: rate-buydown v3 (board runs to about x=1026; the taped "8 years,
  4 months" note and "keep the cash" sit under the buttons), 20-down app props (cash figure to ~970, flow diagram to
  ~1010), price-cuts (address tails to ~967, one zip clipped by the card edge), strip-sack hook ("driving..." to
  ~990), and nothing else. This is the most common miss.
- 20-down app props: "earlier this week" touches his hair at 11 s.
- broncos-4q: 16 s (list says under ~12), and the last question's bottom line sits below y=1450 and across Asher's chin.
- winter-buyers: closing slide carries a headline, a body line and a Caveat note (list says one headline).
- address-advantage: program renamed, but the hook still names Rancho Mission Viejo and the ask is DM "RMV".
- family-growing: passes the review list; it is the premise formula it misses (a pitch with a CTA in the post).

Nothing re-rendered. Offered: fix the board position in the rate-buydown comp since it is the template for the next
math reel.
