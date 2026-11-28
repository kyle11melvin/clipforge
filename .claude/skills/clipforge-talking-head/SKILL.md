---
name: clipforge-talking-head
description: Build a talking-head reel for Kyle's lender account from his phone footage, with type, props and sounds timed to his words. Use when he sends clips of himself talking, asks for graphics or b-roll over his footage, a chalkboard, cards, a fake app screen, captions, or a cover for a talking-head reel.
---

# Talking-head reel

`history.md` beside this file has every past talking head, what Kyle said about it and which files to start from.
Read the entry for the nearest past post before copying its files. Run `clipforge-review` before he sees anything.

## The rules (Kyle approved these on 2026-11-12: "I approve this message")

He wants the rules "a little bit loose" while the brand image stays.

- **The look and feel is the brand, not the hex codes** (Kyle, 2026-11-21: "keep my brand image look and feel. It's
  fine to not always do the exact colors"). A piece should read as his at a glance: the paper and sand feel, the type
  pairing, calm navy and warm terracotta as the family. Shades and accent colours can move within that.
- **Fixed: the brand image.** Navy, sand, terracotta as the base; Sora for big words, Playfair italic for small
  ones, Caveat for handwriting; his plain first-person voice; no logo, no emoji, no DM/NMLS card in a talking head.
- **Loose: everything that makes it pop.** Extra accent colours with a meaning (orange = cost, mint = savings),
  texture, props that look like real things (framed chalkboard, taped note, stamp, strapped hundreds, a fake app
  window with a slider and a rolling number, a flow diagram whose boxes light on his words, paper cards spinning
  out from behind his head, month or count tiles that flip, tiles that flip from a question to his answer), glow, dust, wobble,
  punch-ins. One prop at a time, each tied to what he is saying at that moment.
- **Open on his face** with his own first line as word-by-word type. No hook slide, no full-screen navy, ever.
  **Nothing goes on screen before he says it** (2026-11-28, after a number-first hook was tried: "you already have
  numbers up that I haven't even said yet"). If his opening is slow, cut to where the number is, do not pre-show it.
- **His face stays clear.** Type above his head (or beside it in a wide shot); props above or below, never across.
- **No corner circle of him during a full-screen beat** (2026-11-28: "I don't need to be in the entire thing").
- **Leaving his face is allowed when it fits** (2026-11-21): a full-screen graphic beat where the words call for it
  (a list, a count, a comparison), on sand or paper, never flat navy. He liked cards flying out from behind the
  head. No 01/02/03 numbering on cards or rows.
- **Growth is shown climbing** (2026-11-28): a percent or a balance that grows counts up over the whole phrase and
  gets bigger as it goes, a line or arrow climbs with it, and a `riser` sound (chalk.py) rises under it. A spoken
  dollar figure still lands on its word.
- **He may not want his face in it** (2026-11-28, a hat-and-sunglasses walking selfie: "not flattering"). Ask before
  building around a shot like that; an all-graphics cut over his voice is an accepted shape.
- **Every graphic that moves makes a sound**, about 15 dB under his voice for a running sound. Real-world sounds
  come from real CC0 recordings (`src/music/samples/`); only whoosh, thud and ding are synthesised.
- **The quality bar for a graphic (2026-11-21).** Flat shapes with a number on them read as cheap to him. A prop needs
  a real image in it (a listing photo, a real screenshot, a document), depth (3D tilt, layers, a heavy soft shadow,
  something out of focus behind something sharp) and size (it fills the frame). Never a line drawing standing in
  for a real thing. If the real image does not exist, ask him for it or for one from ChatGPT before building.
- **Never the same device two videos running**, test cuts included ("the same chips as the previous post"). That covers
  images too: an object used in any earlier post (the winter-swipe key) is a repeat (2026-11-28).
- **Depth is real, not a tilt** (2026-11-28: "a 3-D kind of look ... they pop"). Big type is extruded and moves in
  perspective; a chart is built from solid objects on a stage with a moving camera; a flat card with a drop shadow
  does not count. Start from `graphics/stroller-math/overlay.html`.
- **One clear object beats a storm**, drawn crisp and detailed enough to read as the real thing.
- **Board and caption use his spoken words**, not the brief's.
- **A spoken number is fully on screen as he starts saying it** (2026-11-28: "timing is off with the numbers"). No
  slow count that arrives as he finishes; roll it in under 0.4 s, let the chart keep moving underneath, and hold the
  final figure at least two seconds before cutting away.
- **End with a payoff** on his last line (a prop and a sound), over the unused second of smile.
  End on his question, on the word, and leave it hanging (2026-11-28). No ask after it, no smile tail.
- **No visible jump cuts on his face** (2026-11-28: "not a clean cut whatsoever"). His face is on screen only in
  unbroken shots. Wherever the take is cut (ums, stalls, the math), cover it with a full-screen graphic beat: "if
  there's a math moment where I have a video just take the video away and put a graphic up".
- **No music** unless he asks. No emojis, chat bubbles or overshoot slides ("too busy and gimmicky").

## Steps

1. **Footage in.** Find the clips in Drive `Clipforge` and fetch with the usercontent URL (see CLAUDE.md). Convert
   each 4K HLG clip to 1080x1920 SDR 30 fps on its own into `footage/<post>/sdr/` (three in one graph get killed).
2. **Build.** `node bin/clipforge.mjs build footage/<post>/sdr --name <post> --caption-style rounded`. Read
   `transcript.json` for misheard numbers before going on.
   **Word times:** install Parakeet first (`npx hyperframes models install parakeet`); whisper's word times were up
   to 0.7 s late on a walking take (2026-11-28), which lands every graphic late. Parakeet also writes "um" and "uh"
   as words.
   **Cut it tight** (Kyle, 2026-11-28: "tighten and clip a lot"): take out every um, false start, repeated phrase
   and throat-clearing lead-in ("So I was thinking like"), not only silence. `graphics/stroller-math/tight-cut.py`
   is the keep-list tool: Parakeet word edges in, `cut.mp4` and a remapped transcript out, alternating punch-ins on
   the face segments. Re-transcribe the result to check no word was clipped.
3. **Plan the beats.** List each phrase that calls for a visual with its start and end from the transcript, and
   pick one prop per beat. Find where his face sits in the frame; that decides where type and props go.
4. **Start from the nearest past post:**
   - type above his head, torn paper, stamp: `graphics/paper-cut/`
   - chalkboard box for math: `graphics/rate-buydown/assemble-paper.sh`, `board-box.html#...&pop` (the board may run
     under the Reels buttons, its writing may not: lines are pulled left of x=940 automatically; probe with `&zones`)
   - fake app window, rolling counter, flow diagram: `graphics/20-down-myth/ui.html`, `assemble-ui.sh`
   - one floating widget over graded footage: `graphics/rate-wait/overlay.html`
   - cash heap ending: `graphics/rate-buydown/cash.html`
   - cutout (cards behind his head, live screen): `npx hyperframes remove-background`, seated still shots only
5. **Probe stills** with the Reels safe zone drawn, run `clipforge-review`, and show him a contact sheet.
6. **Render** overlays with `--alpha`, composite with ffmpeg, add sounds from `sfx-events.json` via
   `src/music/chalk.py`. Punch in about 7% at each turn of the script.
7. **Captions:** Nunito ExtraBold, sentence case, white, soft shadow. On his chest in an outdoor selfie
   (`--caption-y 0.19`), above his head against a plain indoor wall (`--caption-y 0.66`), hidden under any overlay
   (`--caption-hide a-b`) and during a full-frame cut.
8. **Cover:** `graphics/rate-wait/cover.html` two-tone look on the cover photo he sends, or a numbered strip of
   frames from `cut.mp4` for him to pick from.
9. **Deliver** as CLAUDE.md says. The page's side files cap at 15 MB: a ~3.2 Mbps copy on the page, master in chat.

## After he reacts

He reacts to one thing per message. Change only what he named, show stills again, and expect five to ten rounds.
Say plainly that Claude cannot hear audio and ask him to listen. Add the post and his verdict to `history.md`, and
change the rules above only when he states a standing preference.
