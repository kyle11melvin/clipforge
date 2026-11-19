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
