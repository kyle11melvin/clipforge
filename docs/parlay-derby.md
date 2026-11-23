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

## 2026-11-22 to 11-23: films, the recap, new riders, grading

- **Films are compositions in the Parlay-Derby repo** (`tools/trailer/comp2.html`, `tools/promo/`, `tools/heist/`), rendered
  with this repo's `src/graphics/render.mjs`. Timing trick that held up: every move is a CSS animation whose delay is its
  time in the film, and `seek(t)` pauses and sets them all. Cuts go on the track's beats (hit at 2.0 s, then every 0.5 s).
  Giant CSS 3D planes glitched in the renderer; the driving scene is drawn on a canvas with plain perspective maths.
- **What he reacted to:** "that's so fucking money" for the trailer with the painted car, pop-up billboards (his idea:
  each rider's card springs up on the beat and slams flat) and the chase. A line-up of full figures packed shoulder to
  shoulder read badly to him: give each rider his own framed tile. He wants heist wording ("Eight on the job. One score."),
  cars, racing and loud endings. A 30 s edit cut from three films with mixed voices needed a re-cut "with one voice for a
  marketer": a caption layer with a clear window over the footage (`tools/promo/ad.html`, rendered with `--alpha`).
- **Art handoff that works every time:** a ChatGPT prompt for one object on a flat bright green ground, side view; key the
  green, crop off the ground shadow. Car, patrol car and cash bag all came this way. A portrait on a gradient ground
  needed a grow-from-the-edges cut.
- **The Heist recap is live at /recap** and replaced the kart race. On his iPhone it killed the tab until three things
  changed: one scene in the page at a time, the stage fitted with `zoom` (not `transform: scale`), and no drop shadows,
  spinning sunburst or blur on phones. He found it by noticing it only died with the music on: memory, not audio.
- **Weekly opener:** he tried the trailer film there, then chose his personal "Welcome back" page: "it changes every week".
- **Riders:** Caleb (p9), Dana (p10), Jonny (p11) added; Eric and Grant's logins deleted. He creates logins himself in
  Supabase from direct links and copy-paste blocks, one step per message. He said "one at a time, I hate hopping all over".
- **Pool rules learned:** there is no pot. The only money is what the two weekly parlays pay if they hit, split evenly;
  the header badge shows that payout and nothing per person. A pick saved after the lock counts for points but is not a
  parlay leg. Grading: results fill in from final scores when he opens Commish (2 credits a call, two-hour throttle).
- **Still unverified by him:** auto-grading against a real week.


## 2026-11-23: soft style, ten riders, hands-off grading

- **The whole site was redrawn in a softer flat cel-shaded look** (characters, four scenes, car, patrol car, bag). Sources
  and the green-key cutter are in the Parlay-Derby repo under `tools/soft/`.
- **Redrawing a face from an earlier drawing drifts ("copy of a copy").** What held the likeness: a fresh ChatGPT chat,
  the real photo cropped to the face plus one soft-style picture as the style reference, and the outfit described in
  words. When the old bold style came back, a short correction prompt naming the differences fixed it. Smoke and other
  wisps key badly off green: paint them in afterwards.
- **Ten riders now**, each with his own card colour (he asked that no two match): twelve colours in `public/derby.js`.
- **Promo for his boss:** he pulled "built by / one person / three days" lines, and any phone-mockup scene ("don't turn it
  into a phone thing"); cars zipping off screen, spinning rings and a bag drop stayed. He treats these as a job audition.
- **Hands-off grading:** grading now runs on the server when anyone opens the board and nightly, once the Supabase
  service key is in Vercel as `SUPABASE_SERVICE_ROLE_KEY`. He adds secrets himself, straight from Supabase to Vercel,
  never through chat; a new env var needs a deploy before it applies. Commish shows an ON/OFF line so he can check it
  without me, since a session cannot reach the live site.
- **Still unverified by him:** lock-in car on a real save, a late pick not adding a parlay leg, server grading on a real week.
