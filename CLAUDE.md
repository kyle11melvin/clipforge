# clipforge — working notes for Claude

Kyle Melvin (mortgage lender, Rev Mortgage, Orange County CA) uses this repo to turn phone footage and
screenshots into social videos. He does not write code and usually works from his phone. Treat this file as
his standing brief. Read it before touching anything.

## Start here, every session

1. Run `git fetch origin` and check `git for-each-ref --sort=-committerdate refs/remotes | head`. **If any `claude/*`
   branch is newer than `main`, merge it into your branch before reading anything** (2026-11-16: main sat at Nov 6 for
   ten days while seven sessions wrote their notes to unmerged branches, and Kyle noticed the work getting worse). Then
   read this file and the newest notes in `docs/log/`. At the end of a session ask Kyle to let the branch go to `main`.
2. Run `npm install` and `npm run doctor`. If doctor reports a missing browser or speech model, run
   `npm run setup` (downloads about 700 MB once). Nothing renders or transcribes until this passes.
3. Footage: the Google Drive connector can now list his `Clipforge` folder (and subfolders, by `parentId`), but its download tool caps at
   10 MB. For a real clip, find it by name with `search_files`, then fetch
   `https://drive.usercontent.google.com/download?id=<id>&export=download&confirm=t` with curl (works when
   the file is link-shared, which his uploads have been; a 13 MB video came through on 2026-10-29). If that 403s, ask for a chat attachment.
   HEIC photos: `pip install pillow-heif`, then PIL with `exif_transpose` (ffmpeg and ImageMagick choke on the depth map).
4. Deliver on a private artifact page with a Save MP4 button, a contact sheet of stills and a reel cover
   (1080x1920 PNG, see `still.mjs`), then list what is still missing. End the session by adding a `docs/log/` note and folding any new preference into the matching skill (see "The four jobs").

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
  iPhone footage is HDR (HLG); the cut step tone-maps it to SDR and writes a keyframe every second, which
  HyperFrames needs. Check `transcript.json` for misheard numbers ("2%" for "20%") before the render.
- `bin/clipforge.mjs broll` — cuts graphics into footage as `cut` or `pip`. `pip` accepts `width`, `x`, `y`,
  `border`, `borderColor`. A cue may name its own `graphics` file and `pip` box, so a full-frame slide and a
  small alpha overlay can share one cues.json (see `videos/iq-quiz/cues.json` in the 2026-10-23 log). Render the graphics as a landscape 1080x640 card (`--size 1080x640`) and pip it at
  the top (`y: 48`) so it sits in the sky above his head and never touches the captions.
- `src/graphics/render.mjs` — motion graphics: an HTML composition with `window.seek(t)` rendered frame by
  frame through headless Chromium, encoded by FFmpeg. `--probe t1,t2,...` makes a contact sheet of stills.
  `--workers 3` renders on three browser pages at once (about 2.5x faster in a 4-core session).
  `--alpha` renders a transparent background to ProRes 4444 (`.mov`) so text can float over footage with no
  panel; `comp.html#nocard` is the variant switch `graphics/20-down-myth` uses for that.
  If Playwright's own browser is missing it falls back to `CLIPFORGE_CHROMIUM` or `/opt/pw-browsers/chromium`,
  so `npm run doctor` complaining about Chrome does not block graphics renders.
- `src/graphics/still.mjs` — one full-size still of a composition (`--t`, `--size`), for reel covers.
  `graphics/20-down-myth/cover.html` is the cover template: a frame from the footage (`cover-frame.png`,
  grabbed with ffmpeg at a smiling, mouth-closed moment) with the headline above his head in Nunito
  ExtraBold, white with a 7 px black stroke, the look of his "POV: you're waiting for rates to drop" cover.
  Keep the text inside the centre 4:5 so the profile grid crop shows it. He asks for a cover per reel and
  has his own opinion about the frame: show him a numbered strip of candidate frames (ffmpeg `tile` with
  `drawtext` of the index) and he answers with a number, or he sends his own selfie for it (2026-10-23; crop
  a phone screenshot's black bars first). Frames come from `cut.mp4`, which has no captions. The headline
  is his spoken hook, sentence case, and it should fill the space above his head: three lines at ~130 px
  from y=190 when his head starts around y=800 (Kyle, 2026-10-23: "move the text above my head since
  there's a lot of empty space above me").
- **Instagram Reels safe zone, every reel (Kyle, 2026-10-29, "Cuts off on the IG preview"):** on 1080x1920
  keep all type and anything that must be read below y=250 (back button, "Preview"), above y=1450 (username,
  audio, caption) and left of x=940 (like/comment/share column). Probe stills with those zones drawn in red
  before rendering. A three-line hook does not fit between the chrome and his head in a full-bleed selfie,
  so put the photo lower on a navy ground with a scrim blending the join (see `graphics/price-cuts/`).
- `.agents/skills/` — the 20 HyperFrames skills (symlinked into `.claude/skills/`), installed with
  `npx skills add heygen-com/hyperframes`. The ones that matter here: `talking-head-recut` (timed graphic
  cards over a clip that plays untouched, synced to the transcript, which is exactly the b-roll job),
  `embedded-captions` (35 caption identities, captions composited behind the subject), `motion-graphics`
  (HyperFrames' own version of a short graphic piece), `hyperframes-animation` / `hyperframes-keyframes`
  (GSAP timeline recipes). They route through `/hyperframes`. Use them for structure and caption styles,
  but Kyle's look and tone in this file win over any skill's defaults. HyperFrames skills want to update
  themselves on first use; ask before letting them.

## The four jobs (skills, 2026-11-21)

The rules for each kind of work live in a skill under `.claude/skills/`, not in this file. **Load the matching skill
with the Skill tool before doing that work**; each has a `SKILL.md` (the current rules and steps) and a `history.md`
(every past post of that kind, what Kyle said, which files to start from).

| When | Skill |
|---|---|
| A new post with no premise yet, ideas, a script, a skit, a caption, a Threads post | `clipforge-premise` |
| His footage of himself talking, for the lender account | `clipforge-talking-head` |
| Personal account: Broncos, family stories, screenshot jokes | `clipforge-meme` |
| A graphics-only post, carousel or Project brief (Coastal Money) | `clipforge-graphics` |
| Before he sees any stills or cut, and after every change | `clipforge-review` |

The order for a new post: premise → build (talking head, meme or graphics) → review → deliver → log.

**Keeping them current.** When Kyle states a standing preference, change the rule in that skill's `SKILL.md` (replace
the old rule, do not stack a "superseded" note on top), add the post and his verdict to its `history.md`, and add
anything he caught to the checklist in `clipforge-review`. This file only holds what applies to every job.

Parlay Derby (the pool's weekly recap) is a different repo; its notes are in `docs/parlay-derby.md`.

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
- Captions: he often writes his own and sends it; put it on the page as is. His caption voice: first
  person, plain talk, one idea per paragraph, the real math in dollars, no emoji, no hashtags. He has a
  free two-minute home-buying quiz he links from the comments ("Link is in the comments if you want it"),
  so a reel CTA can point there instead of a DM keyword.
- Keep replies short. He said "You're getting a little smarter" when the work matched the point of the post,
  and "you nailed that" when the shooting plan was concrete: five short lines, one take each, a reaction shot.
## Project log

`docs/log/` holds one note per working session: what was built, what Kyle asked for, what he reacted to.
Read the latest one at the start of a session. Add a new one at the end of any session that produced a
video or changed the pipeline, and fold any new standing preference into the matching skill.

## The Instagram brand: Coastal Money (2026-10-11)

Kyle's Instagram posts use his personal design system, **Coastal Money** (dictated as "Costa money" or
"coastal money guy"). The full guide is `graphics/brand/coastal-money/GUIDELINES.md`, with his portraits
beside it and the fonts in `graphics/fonts/` (Sora, Manrope, Caveat; load them with `@font-face`, never
substitute). Read the guide before any Instagram post. For Instagram, Coastal Money wins over the Rev
Mortgage flyer look above; the motion rules (word-by-word rises, back-eased pops, a beat before the turn)
stay. The short version:

- Personal brand, never Rev Mortgage. No logo, no icons, no emoji, no cards, shadows, stamps or gradients.
- Pacific navy `#173F4F` and warm sand `#EFE9DE` grounds; terracotta `#D77B52` only for the thing read
  first; sea glass `#A9C0B9` (on navy) / `#7E9A93` (on sand) for labels only; ink `#0E2A35` text on sand.
- Sora Bold headlines (sentence case, never all-caps), Manrope body and tracked uppercase eyebrows, one
  Caveat line per slide. Oversized numerals (`01`, `02`, `$203,090`, `DM`) are the signature device.
- Hook: two-tone headline, sand line then the terracotta turn, a muted continuation line at the bottom.
- CTA: DM keyword ask (keywords in use: CONV, VA, DSCR, WAIT, BUYDOWN, POINTS), hairline, circle portrait, name,
  NMLS #1486450, disclosure line. `graphics/wait-or-buy-cm/` is the reference composition.
- **Kyle's call (2026-10-11): ignore the guide's compliance section.** Rates and payments may appear on
  screen; he decides what he posts. Keep the sign-off and the small disclosure line unless he says otherwise.
- This repo is public: do not write anything private from his email into it.

## The Coastal Money Claude Project

Kyle also has (or is creating) a claude.ai Project named "Coastal Money" for planning posts from his
phone. Its instructions are `docs/claude-project-instructions.md`; keep that file in step with this one
when a brand or tone rule changes. The Project writes scripts, captions and carousel handoffs; it cannot
render. A brief that arrives here starting "send this to clipforge" came from it: build the video from the
brief, in `graphics/wait-or-buy-cm/` style, and deliver as usual.
