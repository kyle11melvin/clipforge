# clipforge — working notes for Claude

Kyle Melvin (mortgage lender, Rev Mortgage, Orange County CA) uses this repo to turn phone footage and
screenshots into social videos. He does not write code and usually works from his phone. Treat this file as
his standing brief. Read it before touching anything.

## Start here, every session

1. Read this file, then the newest note in `docs/log/`.
2. Run `npm install` and `npm run doctor`. If doctor reports a missing browser or speech model, run
   `npm run setup` (downloads about 700 MB once). Nothing renders or transcribes until this passes.
3. Ask Kyle for the footage or screenshots as chat attachments. Not Drive.
4. Deliver on a private artifact page with a Save MP4 button and a contact sheet of stills, then list what
   is still missing. End the session by adding a `docs/log/` note and folding any new preference into this file.

## The standard job: a talking-head post with graphics

1. `node bin/clipforge.mjs build <clips folder> --name <post>` → `videos/<post>/final.mp4` (trimmed,
   captioned) and `transcript.json` (word timings).
2. Write the graphics composition at `graphics/<post>/comp.html`, starting from `graphics/siri-post/`.
   Probe stills, then `node src/graphics/render.mjs graphics/<post>/comp.html videos/<post>/final-graphics.mp4`.
3. Write `videos/<post>/cues.json`: for each phrase that calls for a visual, the footage time from the
   transcript, the graphics slice, `cut` or `pip`, and the phrase itself under `says`.
4. `node bin/clipforge.mjs broll videos/<post>/cues.json --output videos/<post>/final-broll.mp4`.
5. Contact sheet, artifact page, short report. Compare with the HyperFrames `talking-head-recut` route when
   time allows and note in the log which came out better.

## What exists

- `bin/clipforge.mjs build` — talking-head clips in, trimmed + captioned vertical video out (see README).
- `src/graphics/render.mjs` — motion graphics: an HTML composition with `window.seek(t)` rendered frame by
  frame through headless Chromium, encoded by FFmpeg. `--probe t1,t2,...` makes a contact sheet of stills.
  If Playwright's own browser is missing it falls back to `CLIPFORGE_CHROMIUM` or `/opt/pw-browsers/chromium`,
  so `npm run doctor` complaining about Chrome does not block graphics renders.
- `graphics/wait-or-buy/` — the first mortgage-math post (buy now vs wait 5 years): stat cards with
  counters, a to-scale bar chart, a two-column comparison table, a stamp. Start chart or table posts from it.
- `graphics/siri-post/` — the reference composition Kyle called "absolutely perfect". Start new ones from it.
- `.claude/skills/clipforge-graphics/` — the step-by-step workflow for a new graphics video in Kyle's style.
- `.agents/skills/` — the 20 HyperFrames skills (symlinked into `.claude/skills/`), installed with
  `npx skills add heygen-com/hyperframes`. The ones that matter here: `talking-head-recut` (timed graphic
  cards over a clip that plays untouched, synced to the transcript, which is exactly the b-roll job),
  `embedded-captions` (35 caption identities, captions composited behind the subject), `motion-graphics`
  (HyperFrames' own version of a short graphic piece), `hyperframes-animation` / `hyperframes-keyframes`
  (GSAP timeline recipes). They route through `/hyperframes`. Use them for structure and caption styles,
  but Kyle's look and tone in this file win over any skill's defaults. HyperFrames skills want to update
  themselves on first use; ask before letting them.

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

## How to work with him

- He reviews on his phone. Deliver video through a private artifact page with a Save MP4 button
  (`downloads` capability, saves to Photos via the share sheet) and a copyable caption. Attaching the file
  with SendUserFile as well does no harm. The Google Drive connector could not see files he uploaded; ask him
  to attach videos directly in chat instead.
- Show a contact sheet of 4–5 frames before the full render and after every change. He catches layout
  problems fast from stills.
- His messages are dictated and often garbled. Read for intent ("Whew see we at on this" = "Where are we at
  on this?"). Confirm the intended wording when it will appear on screen.
- Ship the whole edit, then list what is still missing. He prefers seeing a finished cut and reacting.
- Keep replies short. He said "You're getting a little smarter" when the work matched the point of the post,
  and "you nailed that" when the shooting plan was concrete: five short lines, one take each, a reaction shot.

## Talking-head + graphics rules (from the first experiment, 2026-10-11)

- Kyle's spoken script for the Siri post: "Listen, I have zero code experience and I built six apps and an
  entire website. How can Siri not understand my text messages? Does anyone else have this?"
- The graphics follow the words: icons popping while he says "six apps", the website while he says
  "entire website", the Morgan chat while he asks about Siri. Full-frame cut for a graphic that carries its
  own text; picture-in-picture (lower half, gold border, he stays visible) for a reaction moment.
- Captions on while he is on screen, off during a full-frame cut (the graphic has its own text). Caption
  style: Inter ExtraBold, uppercase, white with a dark outline, centred at 70% of frame height.
- Pipeline: `clipforge build` for trim + transcript + captions, `src/graphics/render.mjs` for the graphics,
  `clipforge broll videos/<name>/cues.json --output ...` to cut them together. The HyperFrames
  `talking-head-recut` skill is the more complete version of the broll step (cards written per moment,
  transcript-synced); try it on the Monday footage and keep whichever gives the better result. A cue is
  `{at, from, to, mode, says}`; `says` is the phrase the cue sits on, so timings can be re-derived from the
  transcript once audio exists.
- Getting footage in: Google Drive is unreachable from the session. Chat attachment is best. GitHub web
  upload works but Safari's Photo Library picker re-encodes and strips the audio; he must Save to Files
  first and upload from Files. A clip with no audio track cannot be captioned; say so immediately.

## Project log

`docs/log/` holds one note per working session: what was built, what Kyle asked for, what he reacted to.
Read the latest one at the start of a session. Add a new one at the end of any session that produced a
video or changed the pipeline, and fold any new standing preference into this file.

## Combining with the Instagram project (2026-10-11)

Kyle runs an Instagram account for his lending content with another Claude project and wants clipforge
to carry that project's instructions too. That project is not a GitHub repo; ask him to paste or attach
its instructions, then merge them into this file and note any conflicts with the look and tone above.
This repo is public: do not write his personal handles or anything from his email into it.

## Next planned step

Monday: Kyle shoots the five lines ("Listen, I have zero code experience" / "and I built six apps" / "and an
entire website" / "How can Siri not understand my text messages?" / "Does anyone else have this?") plus a
three-second reaction shot, saved to Files and uploaded with audio. Run the standard job above with the
existing `graphics/siri-post` composition: the cues are already sketched in `videos/siri-post/cues.json` and
only need their `at` times re-derived from the real transcript. The experiment on the silent take is
`videos/siri-post/talking-head-demo.mp4` in the log; known flaw there was a caption overlapping the
picture-in-picture box, so keep captions off while a pip is on screen.
