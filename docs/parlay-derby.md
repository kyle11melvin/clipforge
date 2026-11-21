# Parlay Derby weekly recap

Moved from CLAUDE.md on 2026-11-21. Work on this in the `kyle11melvin/Parlay-Derby` repo, never here.

- **Parlay Derby weekly recap (2026-11-19)** — the pool's site (`kyle11melvin/Parlay-Derby`, private; parlayderby.com) now
  carries a clipforge-style composition, `public/recap.js`: the week as a 35 s kart race (race → podium and margin → hit
  of the week → Big Bozo → parlays → season table), played at `/recap` and exported to MP4 on the phone for the group
  text. Work on it in that repo, never here: the riders' photos are private and this repo is public. Offline render:
  `node tools/render-recap.mjs out.mp4 --data <season.json>` there. The session cannot log in to the site, so a real
  week needs the branch live or the data pasted in. Log 2026-11-19.
  **Kyle's direction:** the first cut (flat lanes, results as chips) was "not bad, do better": he wants the 64-bit kart
  racer feel with the betting turned into play, so each pick is an item (horseshoe, nitro, seashell from the rider
  behind, bomb for the parlay killer), plus a ramp, stamps, punch-ins. He said "good" to that and asked for more of it.
  Round four (red/green shells, banana peel and shield, lightning shrink, a three-stretch course) he called "worse than
  what was before" and it was reverted: piling on items and scenery made it worse, not better. Change one thing per round.
  **Reference (Drive `Clipforge/Parlay derby`):** his recording of the N64 game. Use it for structure: camera behind one
  kart, portrait rank column, item window top centre, clock, course map, big place number. When ChatGPT's art arrives
  (white kart poses, item sheet, backdrop, drivers) build it into `recap.js` in place of the drawn ones.
  **Art (round eight):** ChatGPT's sheets are cut into `public/recap-art/` (kart-with-driver per rider id, busts, items,
  backdrop); a new rider needs a new sprite from ChatGPT or falls back to the drawn kart. Its turtle shells and eyed bomb
  were copies of Nintendo's items and were left out. Anything he must paste elsewhere goes in a code block in chat.
  **Round ten:** told "you know what I like, just do it", the race became rider by rider (last place to winner) with the
  taped paper call card and the cartoon busts in every scene, 37 s. All six library tracks were "garbage": do not pick
  music for him by description again. He generates a track in a music tool (Suno) from a prompt and sends the MP3.
  **Round twelve:** Suno wanted payment and he would not pay; do not send him to a paid tool again. The kart game he
  wants it to feel like has funk / jazz-fusion music, so look there (MacLeod: Funk Game Loop, Fast Talkin, Vivacity), not 8-bit.
  **Music picked (round thirteen):** "Funkorama" (Kevin MacLeod, CC BY 3.0), "closest" of four funk tracks; it is the
  site's recap theme now.
  **Live (round fourteen):** `/recap` is on parlayderby.com (PR #9). He then asked for a red shell and lightning by name,
  one item per kind of result; those two are in on the branch. After a merge restart the branch from main and push
  normally; force pushes are blocked. He has asked for the real game music three times; the answer stays no.
  **Round sixteen:** the first video he made on his iPhone and sent to the group was silent. Anything the riders will
  receive must be tried by him on his own phone first; say "send it to yourself before the group" every time the export changes.
  **Sound (round nine):** synthesised engine drone, hiss and whoosh beds are "absolutely terrible" to him; never put a
  continuous synthesised noise under anything. Theme recording plus a few short quiet hits only.
  **Music:** the synthesised chip loop was "fucking terrible"; use a real recording (Kevin MacLeod's 8-bit tracks on
  Wikimedia Commons, CC BY, fetched with the web-fetch tool) and give him labelled options against the picture.
  Items, karts and sound stay original drawings; never Nintendo's characters, art or music.
