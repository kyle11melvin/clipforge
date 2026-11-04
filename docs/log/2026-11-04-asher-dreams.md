# 2026-11-04 — "Maverick laughing in his sleep": a personal-account meme reel from a crib-cam recording

Kyle sent a 19 s Nanit screen recording (night vision, the baby alone in the crib, giggling in his sleep in five
bursts and rolling over at 7 s) and asked for "a cute funny video for a short reel of my son laughing, cracking
himself up, get creative". Dictation read: "I have an Australian grey and black laughing at" = "I have no idea what
he's laughing at". He called the baby Maverick; the notes only knew Asher, so the name is assumed (caption only,
not on screen) and flagged on the page.

## What was built (14 s)

- Footage: `graphics/mav-sleep-laugh/cut.sh`. The Nanit chrome is cropped off (feed is y 192–1128 of 1288x1128),
  the four laugh segments (0.9–4.3, 5.4–7.7, 10.2–12.3, 14.4–17.9 s) are cut back to back so a giggle lands every
  two seconds, each cut punches in further (zoom 1.0 → 1.5 → 2.0 → 2.4, then a 2.7 s freeze pushing to 2.65) centred on
  him, in a fixed 1080x784 window at y=700 over the same frame blurred and darkened. Audio +14 dB, limited, loudnorm.
  Zoom is done with `scale=w='…t…':eval=frame` then a fixed crop; crop w/h cannot animate.
- Text: `graphics/mav-sleep-laugh/comp.html`, rendered `--alpha` and overlaid with ffmpeg. Reel-cover type (Nunito
  ExtraBold, white, black stroke), a yellow `#FFD60A` "THEORY n" eyebrow. Hook "My son laughs in his sleep." →
  "Nobody knows what at." on the second giggle → Theory 1 "The Chiefs on 4th and goal." (callback to the Broncos
  reel) → Theory 2 "Mom saying 'he's a great sleeper.'" → Theory 3 "Today's mortgage rates." → Theory 4 "He already
  knows what time he's waking me up." → freeze: "What is he laughing at?" / "Wrong answers only." Each theory lands a
  beat before its giggle so the laugh reads as the reply. Three lines at 96 px fit between y=262 and the window.
- Page: https://claude.ai/artifact/BR64zvU1hc39TBpUybC3ah (Save MP4, caption, cover, frames, timing list).
- Cover: frame at 1.3 s of final.mp4 (hook fully in, wide crib). No sound bed: his giggles are the audio.

## Open

- Whether "Maverick" is right; which theories he keeps (the rates one is the lender in-joke, swap for "Dad's fantasy
  team" if he wants it fully personal); whether he wants a sound bed or a song from the picker (then re-mux silent).

## Round two (what is on the page now)

Kyle: "add a little Maverick in there… he's dreaming, can you add an animation? If you can't I'll ask ChatGPT", and the
financial theory should be "knowing that rates are coming down tomorrow". So: the name is confirmed and in the hook
("*Maverick* laughs in his sleep."); a cartoon thought bubble (three dots trailing from his head, a cloud of
stroked circles at the window's top-left, bobbing) pops in on every block with an SVG drawing animated in `seek`:
a top-down fighter jet crossing with contrails (the Top Gun nod to his name), a bouncing spinning football, Zzz
floating up, a red rate line drawing itself downhill with a green arrow, an alarm clock with spinning hands, a
pulsing "?" on the freeze. Theory 3 is now "He knows rates are coming down tomorrow." Cover: frame at 2.0 s (jet
in the bubble). Lesson: when he asks for "an animation", a cartoon device drawn in SVG inside the comp is enough;
no stock or AI imagery needed.

## Round three: the names were wrong and the graphics were "fucking awful"

Kyle: "That is a god-awful video for one. My son's name is Asher. My dog's name is Maverick so I was saying he's
laughing at Maverick. Those graphics are fucking awful… get more creative… Send a prompt to ChatGPT Images because
they are better images than you are." Then, calmer: "I want you to reach outside the box a little bit. I wanna start
getting some graphics in our clips. I don't know if I need to feed you graphics or what."

Read: "I have an Australian grey and black laughing at" was "I have an Australian [Shepherd], grey and black, [he's]
laughing at [him]". Two lessons folded into CLAUDE.md: never hand-drawn SVG clip-art again; real photos, real
screenshots, or images he generates in ChatGPT from his own photos with prompts written here.

The post folder is renamed `asher-dreams`. New concept: every giggle is a reaction to a dream shot of Maverick living
Asher's life. Hook "Asher laughing in his sleep." / "He's dreaming about the dog." → "Maverick took the crib."
(night-vision look, the dog in the crib) → giggle → "Maverick took the high chair." → giggle → "Maverick in the 4th
quarter." (jersey, paws over eyes, the Broncos callback) → the longest laugh → punchline on a photo of the dog awake,
staring: "Meanwhile, Maverick." / "Zero idea what's so funny." 18.4 s; `cut.sh` now leaves black gaps in the base
and the comp paints the dream shots (image blown up and blurred behind a 768x952 card at y=480, slow push).

Images: the Canva connector's `generate-image` made four usable stand-ins of a blue merle Aussie in about a minute,
but `media.canva.com` is denied by the session's network policy, so only the 161x200 thumbnails came through; they are
upscaled with lanczos + grain and pass as "dream haze" at review size, nowhere near post quality. The page carries
one ChatGPT prompt per shot with a copy button (each starts "Use the attached photo of my dog and keep his exact
face, markings and colouring"), and asks for a real flash photo of Maverick for the punchline. When his four images
arrive: drop them in `videos/asher-dreams/img/` under the same names, rerun the three commands, republish.
