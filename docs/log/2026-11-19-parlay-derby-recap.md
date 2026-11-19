# 2026-11-19 — Parlay Derby weekly recap video

**Ask (Kyle, dictated):** engagement in the parlay pool is dropping; make a fun weekly recap video in the
site's kart-race style (who won, who lost, won by a little / a lot, the bozo) that goes to everyone in the
group text each week, using the clipforge video skills with the Parlay Derby site.

**Built (in `kyle11melvin/Parlay-Derby`, branch `claude/weekly-race-recap-video-he3oz5`, not in this repo
because the riders' photos are private and this repo is public):**

- `public/recap.js`: one canvas composition in the clipforge shape (`window.seek(t)`, everything a function
  of data and time), 1080x1920, about 35 s: title + start lights → the race (a lane per rider, college
  results land then NFL, win = boost, loss = spin-out, running dollars over each kart, places at the line) →
  podium with the margin called (photo finish under $3, blowout at $12+, otherwise "wins by") → hit of the
  week → Big Bozo (bomb, dunce cap, what it cost) → both parlays leg by leg with a HIT / BUSTED stamp →
  season table reshuffling → when next week locks. Sound is synthesised WebAudio on the same timeline
  (original chip loop, beeps, boosts, explosion, sad horn, stamp, ka-ching).
- `/recap` on the site plays it for every rider; **Make video for the group text** encodes an MP4 on the
  phone (WebCodecs + vendored mp4-muxer, 720x1280, no server) and opens the share sheet. Board and Commish
  link to it; the text recap ends with the link.
- `tools/render-recap.mjs`: the offline render (headless Chromium frame-stepping + FFmpeg) from a season
  JSON; `tools/demo-season.json` is a made-up season with the real names.

**Delivered:** a sample cut with made-up Week 3 results on a private page, said so on the page.

**Not verified / open:**
- The on-phone export was tested in desktop Chromium only (H.264 + sound came out, 35 s, ~11 MB). iPhone
  Safari is untested; if it fails there, the fallback is the offline render from an export of the week.
- Claude cannot hear the sound; Kyle has to judge it.
- Truly automatic sending to an iMessage group is not possible from a website. One tap from the share
  sheet is the route; email or per-person SMS would need addresses and a paid sending service.
- The site only changes when the branch is merged to `main` (Vercel deploys main). No PR was opened.
- "Won by a little / a lot" was read as the rider margin; game scores are not in the site's data.

## Round two and three (same day)

**Kyle:** "This isn't bad, but please do better, think of Nintendo 64 Mario Kart and make it more creative as far as
the betting and the players and the shells." Then: "Good, and then add like a ramp and other stuff, think of the
graphics that we have with clipforge."

**Changed:** the flat lane race became a behind-the-pack 3D race (road drawn row by row at 540x960 and blown up for
chunky pixels, painted beach as the sky), with a rider-select screen before it. Every pick is an item play: golden
horseshoe (underdog hits), nitro (favourite), a seashell thrown by the rider directly behind (a loss), the bomb (solo
parlay killer). Rank column down the left, item box top right, a call card at the bottom. Then a ramp between college
and NFL (whole pack gets air), clipforge stamps slamming in ("UNDERDOG +$24", "WRECKED", "PARLAY KILLER"), a camera
punch-in on the underdog, shake on the bomb, speed lines. About 43 s.

**Rule kept:** the genre and feel of a 64-bit kart racer, but every item, kart and sound is an original drawing; no
Nintendo characters, art or music.

## Round four

**Kyle:** "That is pretty good. Add a little more, like red shells and green shells and banana shields and lightning,
players shrink down ... Also make the course a little more interesting."

**Changed:** losses now split by kind: red seashell from the rider behind, green seashell off the wall when an
underdog misses, banana peel when a favourite of -150 or shorter loses; a push is a banana shield that blocks a shell;
the biggest win of the week is lightning that shrinks every other kart for two seconds. The course has three
stretches: beach road, a wooden pier over the water with the ramp clearing a gap, then a dirt track on turf with
pennants and a checkered finish arch. Sample week changed so every item shows.

## Round five

**Kyle on round four:** "that's actually worse than what was before", and asked for it to be as close to Mario Kart
as possible since it is not for sale. Round four was reverted (the site branch is back at the ramp-and-stamps cut he
called "pretty good"). Copying Nintendo's characters, item art, tracks or music stays off the table; asked him which
part of round four made it worse (the three-colour course, the lightning shrink, or the amount going on).

## Round six: music and a ChatGPT prompt

**Kyle:** the reverted cut is "better"; "the music is fucking terrible"; still wants it closer to Mario Kart; asked for
a prompt to give ChatGPT for the visuals.

**Done:** the synthesised chip loop is removed. `recap.js` now plays a recorded track from
`public/audio/recap-theme.mp3` when the site ships one (effects only otherwise), dipped under the bomb. Three options
rendered against the picture for him to pick: Bit Shift, Pixelland, 8bit Dungeon Boss (Kevin MacLeod, CC BY 3.0, from
Wikimedia Commons through the web-fetch tool; every other free-music site is blocked). No track is committed until he
picks. The page carries a copyable ChatGPT prompt for original 64-bit-style kart art (rear-view kart, item sheet,
backdrop strip, textures, big-head drivers from the rider photos).

## Round seven: his reference recording

**Kyle:** recorded a YouTube longplay of the N64 kart game into Drive `Clipforge/Parlay derby` ("look at everything
about it and make ours a little more like it"). ChatGPT asked him for a race screenshot and rider photos; both were
put on the page (one labelled sheet of the eight riders) with a line to paste.

**Taken from the reference (structure and feel only, our own art):** the camera sits close behind one kart, so the
race now rides behind whichever rider's pick is landing, with a white cut between riders; riders ahead in the running
order are up the road and a boost drives the camera kart past them. HUD in the console layout: square portraits with
places down the left, item window top centre, "WEEK 3/11" and a running race clock up top in italic stroked type, a
course map bottom right with a dot per rider, the big place number ("3rd") bottom left. Road speed nearly doubled,
engine drone and theme louder (the reference's music sits around -16 dB under nothing; ours was -24). 0.85 s per pick.

**Waiting on:** his music pick (A/B/C) and the ChatGPT art (karts, item sheet, backdrop, textures, drivers).

## Round eight: ChatGPT's art in, music set

- He asked what was decided on music ("we need to fix that ASAP"); nothing had been picked, so option A ("Bit Shift",
  Kevin MacLeod, CC BY 3.0) was built into the site at `public/audio/recap-theme.mp3` with a credit file and a credit
  line on `/recap`. B and C are a swap away.
- ChatGPT returned two sheets on a fake-transparency white ground: three white karts, eight items, a backdrop strip, two
  textures, eight small kart-with-driver sprites, and eight large driver busts. Cut into `public/recap-art/` by flood-
  filling near-white from each crop's border (the black outlines keep the fill out). Used: `kart-p1..p8` as the race
  sprites, `bust-p1..p8` on the field screen and the place column, the backdrop strip behind the road, the horseshoe,
  flame and crate. **Not used:** its red and green shells and its bomb, which came back as copies of Nintendo's item
  designs despite the prompt; the seashell and plain bomb drawn here stay.
- Paste text for him goes in a code block in chat, not only on the page ("just give it in a text").

## Round nine: the sound again

**Kyle:** "The music and the background noise is absolutely terrible." The background noise was the synthesised engine
drone (filtered noise + sawtooth) and the hiss/whoosh beds; a compressor on the bus was also pumping the music. All
removed: no continuous sound but the theme, only short low thuds and tonal blips left, at 0.4 against the music.
Six options on the page over one picture: Bit Shift, Pixelland, Monkeys Spinning Monkeys, Salty Ditty, Pixel Peeker
Polka, and Bit Shift with no effects. `tools/render-recap.mjs` gained `--fx` and `--wav-only` so one picture render
can be muxed with several sound mixes. Waiting on his number.
