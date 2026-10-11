# clipforge — working notes for Claude

Kyle Melvin (mortgage lender, Rev Mortgage, Orange County CA) uses this repo to turn phone footage and
screenshots into social videos. He does not write code and usually works from his phone. Treat this file as
his standing brief. Read it before touching anything.

## What exists

- `bin/clipforge.mjs build` — talking-head clips in, trimmed + captioned vertical video out (see README).
- `src/graphics/render.mjs` — motion graphics: an HTML composition with `window.seek(t)` rendered frame by
  frame through headless Chromium, encoded by FFmpeg. `--probe t1,t2,...` makes a contact sheet of stills.
- `graphics/siri-post/` — the reference composition Kyle called "absolutely perfect". Start new ones from it.
- `.claude/skills/motion-graphics/` — the step-by-step workflow for a new graphics video.

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

## Project log

`docs/log/` holds one note per working session: what was built, what Kyle asked for, what he reacted to.
Read the latest one at the start of a session. Add a new one at the end of any session that produced a
video or changed the pipeline, and fold any new standing preference into this file.

## Next planned step

Monday: Kyle shoots five short talking-head lines plus a three-second reaction shot. The job is to trim and
caption his clips with `clipforge build`, then cut the `siri-post` graphics in between his lines as b-roll.
That second pass (footage + composition → one video) is not built yet and is the next feature.
