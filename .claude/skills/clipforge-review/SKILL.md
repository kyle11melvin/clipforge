---
name: clipforge-review
description: Check a cut against Kyle's standing rules before he sees it. Use after probe stills and again after the full render of any clipforge video (talking head, meme, graphics-only), and after every change he asks for.
---

# Review before Kyle sees it

Most of his first-round notes have been things on this list. Make a contact sheet at one frame per second plus
every frame where something lands, look at each frame, and go down the list. Fix what fails, then show him. In the
report, say what was checked and anything that could not be (sound, always).

## Every video

- [ ] **Reels safe zone.** On 1080x1920 nothing that must be read sits above y=250, below y=1450 or right of
      x=940. Probe with the zones drawn in red.
- [ ] **Nothing over a face.** Type, props, bugs and captions clear of every face, his or a character's.
- [ ] **Wording.** On-screen words match what he said or wrote. Numbers checked against the transcript ("2%" vs
      "20%") and against their source.
- [ ] **No invented handles, taglines, sources or facts.**
- [ ] **Not a repeat.** Different device and shape from his last post of this kind (check the newest logs). No
      object or photo reused from any earlier post.
- [ ] **Looks made, not drawn.** Each prop has a real image in it, depth and size; no flat tiles or line drawings
      standing in for real things.
- [ ] **One thing at a time.** One prop or idea on screen per beat; no clutter, no particle storms.
- [ ] **Private things.** Account numbers, names, emails redacted; family photos and raw screenshots not committed.
- [ ] **No commercial music** in the file. No TTS voices.
- [ ] **Length** fits the format (meme under ~12 s, payoff by 7 s; story ~20 s; graphics ~20 s).
- [ ] **File plays:** has an audio track if it should, AAC not Opus, under 15 MB for the page copy.

## Talking head

- [ ] Opens on his face with his first line as type. No hook slide. No full-screen navy anywhere.
- [ ] A full-screen graphic beat only where his words call for it, on sand or paper.
- [ ] Each graphic lands on the word it belongs to (start and end from `transcript.json`).
- [ ] Tight: no ums, false starts, repeated phrases or dead air left in. Word times from Parakeet, not whisper.
- [ ] The personal setup and the reason he gives are still in. Nothing he would call the point of the clip is cut.
- [ ] Each cutaway looks bought: a real image behind it (his blurred footage), glass, glow, depth. No flat paper charts.
- [ ] No corner circle of him over a full-screen beat.
- [ ] Nothing on screen before he says it. Ends on his question, on the word.
- [ ] No jump cut visible on his face: every edit point sits under a full-screen graphic.
- [ ] He is still the main shot (about half the running time or more), and the takes match in exposure.
- [ ] Every spoken number is complete on screen within 0.4 s of the word starting and stays up 2 s or more.
- [ ] Any house, street or place shown looks like Orange County, not the East Coast. Street numbers painted out.
- [ ] Captions hidden under overlays and during full-frame cuts; right position for the shot.
- [ ] No DM / name / NMLS card. No emoji, chat bubbles, overshoot slides, 01/02/03 numbering.
- [ ] Every moving graphic has a sound event; running sounds about 15 dB under his voice (measure with ffmpeg
      `volumedetect` on the two stems).
- [ ] Ends on his last word with a payoff. No music unless he asked.

## Personal-account meme

- [ ] Real score, quarter and words; the reaction cut is on the announcer's key word.
- [ ] The character reacts with the call; no pose held for a whole beat, no frame reused or cropped from another
      moment, one room and one angle.
- [ ] No pulsing, shake or thumps on a still; no continuous synthesised noise.
- [ ] No brand type or colours. No side gag that was not in his premise.
- [ ] The page says broadcast footage can get the reel muted or pulled.

## Graphics-only post (lender account)

- [ ] Coastal Money guide followed (`graphics/brand/coastal-money/GUIDELINES.md`); fonts loaded, not substituted.
- [ ] Closing frame carries one headline only. No flat navy void under a screenshot.
- [ ] No loan program named after a neighborhood. "Example, not a quote" on math.

## What Claude cannot check

Claude cannot hear. State the measured levels, say so, and ask him to listen. Anything the group or the public will
receive from his phone he should send to himself first.

When he catches something this list missed, add it here.
