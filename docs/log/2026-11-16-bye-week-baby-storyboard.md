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

## Round seven: "that's so good" and the full handoff

Kyle on the side-angle cut: "It's really good actually." He asked for more expression in the pictures (happy, animated:
bliss on "bye, finally", a big "what", joy with the baby) and for one document that carries everything he has said, to
give to Grok or ChatGPT, "pass them back off to you and then we're gonna learn from that". `docs/handoff-bye-week-baby.md`
is that document (story, character and set, feel, don'ts, three clips, what to return). **When the clips come back:**
cut them under the existing graphics, then write down here what the other tool did better or worse than Canva stills
(motion, expression, character consistency, logo) and fold the lesson into CLAUDE.md.

## Two briefs, and main is current

Kyle asked whether handing the other AI my frames restricts it too much. Recommendation given: run both. The tight
brief with the two frames to one tool (keeps the character and matches the graphics already cut), and
`docs/handoff-bye-week-baby-open.md` with no frames to the other (story, beats, feel, don'ts; its own ideas). Compare
what comes back; that comparison is the lesson. He said yes to main: this branch was pushed to `main` on 2026-11-16.

## First thing back from the other tool

ChatGPT (plain chat) could not make video ("I can't render actual video files") but returned a still for clip 3 from
the two reference frames: navy Nike Broncos hoodie, the foal awake and laughing up at him, a Broncos game on the TV,
framed a little closer. Much better than the Canva stills on expression and on the logo, and the character and room
held. It is now `side-couch.jpg` (gitignored), the ending and the cover. **Lesson: for a character still with real team
gear and a big expression, ChatGPT's image tool from a reference frame beats Canva; ChatGPT chat does not do video
(that is Sora), Grok Imagine does image-to-video.** Waiting on Grok's clips.

## Grok with the open brief: unusable

Kyle: "Grok is awful." The open brief (no frames) came back as storyboard contact sheets with titles and text baked in,
a different horse in every panel (white, cartoon, brown), a human wife and a human baby. **Lesson: never give Grok a
multi-shot brief. One reference picture, one short "animate this exact image" line, one clip at a time.** The page now
has that: three pictures (two Canva, one ChatGPT) each with its own one-line prompt. ChatGPT with reference frames is
the tool for stills; the long brief stays for ChatGPT only.

## The storyline he settled on (round eight)

Kyle: "Get rid of the mom versus the husband, I hate that one. The whole point is how stressful the Broncos games are."
His storyline, which is the cut now (13.2 s): two weeks ago, the win over the Chiefs (scorecard) → last week, Carolina,
last minute, nerve-racking → he sits down on the leather recliner with RedZone on, no Broncos, finally relaxing →
"Honey, my water broke" → the one that goes up in the air → the following week, Broncos on TV, holding baby girl, maybe
a bottle. He asked for "a couple vocals"; asked him for a voice memo of six lines (there is no footage to mismatch).
`comp.html`: one `card()` builder adds a row per beat (WK 8 vs KC W 28–24, WK 9 at CAR W 26–21, WK 10 BYE "FINALLY",
then BYE struck with "SO MUCH FOR RELAXING", then WK 11 vs Las Vegas "PARTY OF 2"). `stress-a.jpg` / `stress-b.jpg` are
tight crops of the old delivery-room and front-on shock frames, soft placeholders for the two recap beats.
**Lesson: the joke has to be his premise (Broncos stress), not a clever side gag of mine (the flex / Mom vs. Husband).**

Button line added at his request (14.8 s): after "Welcome to Broncos Country, baby girl." the subtitle turns to
"And it's the Raiders. I can still relax." and the card shows WK 11 vs Las Vegas, "STILL RELAXING". He asked twice
whether this can be "made into a video": told him it already is an MP4, what it lacks is the character moving, which
needs Grok image-to-video (one picture, one line) or Sora.

## Round nine: "smoother … like CBS or Fox … more fright … no music, very soft"

Kyle: "not bad", wants it "more video style / smooth", "smoother cuts"; the score to look like a network's score box
("Broncos 28 versus 24 … not so generic … don't worry about copyright"); more fright on "Honey, my water broke"; no
music, the ending very soft. Then: it is his personal account, so a licensed song or recommendations are welcome.

- `comp.html` is now a scene list with transitions in `seek()`: whip (slide + blur) A→B, dissolves B→C, D→E, E→F, a
  smash cut C→D; every still gets a slow handheld drift and an eased push. Frames use opacity, not display.
- `.bug2` is the broadcast bug: team-colour tiles with gloss, big scores, a FINAL / BYE WEEK status box, a white ticker
  strip (KC 24 DEN 28 "Roach sacks Mahomes on 4th & goal, 0:04 left"; DEN 26 CAR 21; DEN 7–2 BYE WEEK; BYE WEEK
  CANCELLED / BREAKING; LV at DEN TODAY). Network-style, no real network logo. The schedule card is gone.
- The fright: `side-fall.jpg` opens at 2.0x on his face (translated to centre), jumps to 2.35x and 2.7x, then snaps
  wide at 0.75 s as the recliner goes over.
- `byeweek_flex.py` is effects only now (hits, crowd swells, whoosh, chime, crash, splash, typed ticks, a faint crowd
  murmur to end). No pad, no brass, no lullaby.
- Song: not baked in (commercial track); he adds it from Instagram's picker on the personal account. Recommended
  "Under Pressure" (Spotify link on the page); Spotify would not return links for the two sweeter options.

## Round ten: the announcers

Kyle wanted announcer calls on the two recaps, "like Dave Logan" (copy the voice or pull from that type), then sent a
screen recording of the Broncos' own reel: Logan in the booth calling Coleman's catch-and-run against Kansas City
("Here we go… 35, 30… 25, 20… foot race, 15, 10… tackled at the 4!"), 1290x2796, 11.5 s.

- Told him a real person's voice is not something to clone; the real clip he supplied is used instead. Beat A (0–4.6 s)
  is that recording, 3.3–7.9 s, `crop=1069:1900:0:300` (clears the Instagram chrome), as 138 preloaded jpgs in
  `logan/` that `seek()` flips through, its own audio loudness-normalised under it, the FINAL bug sliding in at 3.3 s.
- Beat B (4.6–8.2 s): Kokoro TTS (`npx hyperframes tts … -v am_michael -s 1.35`, needs `pip install kokoro-onnx
  soundfile`), band-passed 280–3600 Hz and compressed for a radio sound: "He drops back, strip sack! Fumble! Broncos
  recover! Game over! Game over!", bug flips 1:24 4TH QTR → FINAL on the strip.
- Her line: `af_heart`, "Honey? My water broke.", low-passed with a short echo, at 10.45 s.
- Timeline is now 19.6 s (A 0, B 4.6, C 8.2, wife 10.4, D 11.7, E 13.8, F 14.8). Told him Instagram can mute or remove
  a reel carrying the Broncos / KOA clip, and that I cannot hear the mix.

Carolina call reworded to his line ("oh my God he got it, he got it, he got it") and revoiced: `am_adam -s 1.45`,
"Bonitto off the edge, strip sack! Oh my, he got it! He got it! He got it! Broncos win!", pitched down 7% (asetrate),
band-passed and compressed harder so it sits beside the real Logan call. A stock voice in that style, not a clone.

## Round eleven: "Absolutely not, we had a better one"

The TTS announcer over a horse close-up for the Panthers beat was wrong. Kyle: Chiefs with the Logan clip, then the
real Bonitto strip sack, then relax (coffee, couch), "my water broke", up in the air and slow, then the baby in new
Broncos gear. Beat B is now 1.2–5.6 s of `broncos-strip-sack.mp4` (fetched from the 2026-11-09 page with the Artifact
tool's read-by-path; the source recording is not in Drive), 132 frames in `strip/`, its CBS call under it ("Young in
the pocket… that ball's free!"), FINAL bug at 3.3 s. The fall holds 2 s longer with a slow push, a slight tilt and a
falling low tone (slow motion from a still). 21.2 s: A 0, B 4.6, C 9.0, wife 11.2, D 12.5, E 15.4, F 16.4.
**Lesson: when he has supplied the real clip for one beat, the matching beat gets a real clip too; look in earlier
sessions' pages before synthesising. A fake announcer next to a real one reads as a downgrade.**

## Round twelve: "Oh my God this is great … mix in the person watching"

Kyle loved the real footage and voices. Asked to tie it together smoothly: cut to the character watching, stressed,
during the clips, keep the Logan voice exactly, same for the strip sack, then the bye week where he sits down and pulls
out a book, then "my water broke". Added `react()`: reaction cut-ins (`stress-b.jpg` in A at 1.55–2.3 and 2.95–3.3,
`stress-a.jpg` tight at 1.45x in B at 0.7–1.35 and 2.75–3.3) with a TV-light flicker and a small push, the clip's audio
running on underneath, a soft thump on each cut. The book frame could not be generated (Canva quota); a ChatGPT line
for it is on the page.

## Round thirteen: "it gets too intense … make the transitions way more smooth"

Kyle on the cut with reaction cut-ins: "I don't like that it gets too intense … the creative editing is terrible, I
don't wanna hear that, I don't wanna see it. The very end is good with the baby." His fix: "Broncos make me stress",
the guy sitting in front of the TV with the Broncos game, "clip to the volume of the announcer, you don't need to go to
the actual game footage", then the next one. So beats A and B are now the living room (`side-relax.jpg`, slightly
darker) with the real clips playing **inside the TV screen** (`.tv` box at 497,387 590x380 over the screen, inside a
`.room` wrapper that takes the push), the calls as the sound, fading in and out. Every transition is a 0.35–0.9 s
dissolve; the reaction cut-ins, whip, jump punch-ins, shake and all percussive sounds are gone; the fall is one slow
push. **Lesson: his taste is the baby scene: slow dissolve, slow push, quiet. Hard cuts, shake and hits read as
"intense" and "terrible" to him even on the scare beat.** He also said the hand-offs to ChatGPT/Grok are painful
because the tools do not talk to each other; keep every request to them to one picture and one sentence.

## Round fourteen: reactions, and no "machine" voice

Kyle: "pretty good for the most part". Wants his attitude to change with the games: lean forward / "yes" when the
Broncos are about to win, same for the other game, then sit back on the bye. And: "I don't wanna see some machine,
honey my water broke … just with words", no stall after it. Done: `yes()` dissolves to a tight crop of `side-fall.jpg`
(arms up, mouth open; chair out of frame) at 3.2 s of each game beat with "YES!" / "They did it again!" and the FINAL
bug; the TTS wife line is out of the mix (text box only, the whole line at once); wife → fall gap cut to 1.0 s (20.2 s
total). Canva still refuses new images, so a real fist-pump frame has to come from ChatGPT (line on the page).
**Lesson: no TTS for a person in his life; he hears it as a machine. Words on screen instead.**

## Round fifteen: he asks for the fist pump again

"I need a little more action … something goes his way, he fist pumps … next game same thing … sit down with a cup of
coffee, nice and chill … honey my water broke … then him with his daughter watching the Broncos game. Use the
commentators' voices. Don't do the weird things. If you can't do it then give it to me." Canva refused again, so the
real blocker was said plainly: a fist-pump frame and a chill frame have to come from ChatGPT. The page now leads with
one job (save one picture, copy one message that asks for both images, send them back) and the video URLs carry a
`?v=` stamp so his phone cannot replay an older cut. **Lesson: when the missing piece is a picture I cannot make, say
so in the first line and hand him one copy-paste, instead of shipping another stand-in.**

## Round sixteen: the pictures arrive

He ran the one-message prompt in ChatGPT and sent back three stills from our reference frame: a fist pump on the edge
of the recliner with a Broncos celebration on the TV (`fist.jpg`), eyes closed with a steaming coffee and the four-game
TV (`chill.jpg`), and a calm watching pose (`watch.jpg`, unused so far). "That's what I'm talking about." Character,
room and logo held across all three. In the cut: `yes()` now dissolves to `fist.jpg` (full frame after the Chiefs, a
tighter crop after the strip sack) and beat C is `chill.jpg`. 20.2 s, dissolves only.
**Lesson: the fast path for a missing pose is one saved reference frame plus one pasted message to ChatGPT; it took him
a few minutes and fixed what three rounds of stand-ins could not.**

## Round seventeen: "that's perfect" and the timing of the joke

Kyle: "Yeah, that's perfect." One change: the bye-week picture should be "nice and calm, very quickly, and then honey
my water broke … that's the joke: nice and calm weekend finally, and then my water broke." The calm now lasts 1.3 s
(C 9.0, wife 10.3, D 11.2, E 13.8, F 14.7, end 19.5) with one line, "Bye week. A nice, calm weekend. Finally."
**Lesson: the setup for a punchline is short; the interruption is the joke.**

## Round eighteen: "make it connect … let it flow, it's very choppy"

Dissolves lengthened (1.1 s into each game beat and the calm, 0.7 into the fall, 0.9 / 1.2 around "Next Sunday"), the
fist pump melts in over 1.0 s starting earlier (2.9 / 2.8 s), the score bug fades in place instead of sliding, her box
eases down instead of popping, each scene's subtitle fades out before the next arrives. Sound: the calls are cut long
and overlapped (Logan 3.3–9.7 s of his recording with a 2 s tail, the strip-sack call from 4.3 s with a 1 s fade-in and
a 2 s tail into the calm) over one continuous quiet room tone, with a fade at each end of the reel.
**Lesson: "choppy" was mostly the sound starting and stopping per beat; overlap the audio across picture changes.**

## The memory problem

`main` had not moved since 2026-11-06. Every session from Nov 8 to Nov 16 pushed its log and its CLAUDE.md changes to
its own `claude/*` branch and none were merged, so each new chat started from the Nov 6 brief and missed everything
after (the "idea, not a format" lesson, no baked music on personal memes, the reach formula, the looser talking-head
rules). This branch now merges all of them (union of CLAUDE.md). It still has to reach `main`; asked Kyle.

## Open

- His clips from Grok / ChatGPT; then recut on real motion (text, card and sound stay).
- Permission to update `main`.
- Sound: per the 2026-11-08 rule he adds his own song on personal memes; the silent cut is on the page beside the bed.
