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

## Site reskin: Vice Coast Parlay (2026-11-22)

- Kyle asked for the pool site repainted in the style of a neon beach-city crime game, back end untouched. It is built on
  the `claude/admiring-volta-kgyu83` branch of the Parlay-Derby repo (see its README, "The look"); not live until he says go.
- **The line that held:** the feel (palette, poster portraits, menu furniture) is fine; the real game's name, logo,
  characters, screenshots and music stay out. He accepted that once he saw how close the feel gets.
- **What worked:** a rough mock first on a private artifact page, then his ChatGPT art dropped into it piece by piece.
  ChatGPT makes the art (one portrait per rider on a flat colour ground, one backdrop with no text or people); it is never
  the board itself, because it invents names and numbers. Portraits: one photo per message in one chat, his finished
  portrait attached as the style reference. Flat grounds cut out cleanly with a flood fill from the edges.
- **His calls:** name "Vice Coast Parlay" (URL unchanged); see-through scoreboard so the car, yacht and cash case show,
  darkness "B"; the big figure is the signed-in rider (he does not want to be the main image without a reason), leader
  when signed out; tap a rider for his full poster; a welcome character screen after login. He picks from lettered
  side-by-side options (A/B/C) quickly.
- Two riders are benched in code (`lib/roster.ts`), hidden everywhere, nothing deleted. The board's kart race box is
  switched off in the new look and `/recap` is still the kart race: he said the race replay can wait.
- **Live 2026-11-22 (Parlay-Derby PR #13).** After the look he asked for "graphics": a clipforge-style welcome intro
  (3D spinning title, flash, sunburst, character pop, season tiles flipping in), once per pool week per phone, with Skip.
  Everything kart-themed is off the pages (race box hidden, `/recap` redirects); he wants nothing on the site that does
  not match the new look.
- **Music, again:** a library track picked by measurement ("Voltaic") was "fucking terrible", like every library pick
  before it. What worked: a written prompt he ran in Suno himself, then the share link. `suno.com` and `cdn1.suno.ai`
  are allowed on his Default environment now; the share page's `cdn1.suno.ai/<id>.mp4` downloads with plain curl (the
  `.mp3` needs a login). Do not pick a track for him; hand him the prompt.
- The real game's theme (he sent a screen recording of a YouTube upload) was declined; he accepted a sound-alike he made.
- The session cannot reach parlayderby.com or sign in, so a live check is his: board, My Picks, Commish on his phone.

