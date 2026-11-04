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
