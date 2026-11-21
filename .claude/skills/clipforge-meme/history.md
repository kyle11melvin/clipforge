# Personal-account meme history

Moved here word for word from CLAUDE.md on 2026-11-21. Each entry is one past post: what was built, what Kyle
said, and which file to start from. Where an entry and SKILL.md disagree, SKILL.md is current. Add new entries at the end.

- `graphics/broncos-4q/` (2026-11-02) — a **personal-account meme reel**, no Coastal Money ("this is the straight
  personal account"): photos with his reel-cover type (Nunito ExtraBold, white, black stroke) and Broncos orange.
  Kyle holding Asher = 1st quarter, Kyle alone draining to an aged black-and-white = 4th quarter, with a broadcast
  score bug (the real game's score, down and clock, found by web search; espn/cbssports are not reachable from
  the session and game footage is never an option) plus a blood-pressure / BPM monitor and an ECG trace, then
  Asher laughing: "they pull it off. Every time." A true face-aged photo needs a phone app (FaceApp); ask him
  for one rather than faking it. `src/music/heartbeat.py` is the baked-in sound bed (ticks, drone, toms,
  heartbeat, buzzer, crowd roar). Lesson: when he says "personal account", drop the brand rules and go for the
  joke, and he wants the real game on screen. **It worked**: ~15K views, 243 shares in 24 h (2026-11-03), his
  biggest reel so far (Rod Smith commented); average watch 8 s of 16, so keep a meme under ~10 s: 2 s hook,
  ~4 s tension, payoff. **Next game meme**: ask him for his own phone recording of the TV at the final play (the
  announcers' call) plus a reaction photo of Asher, and build the same night. He wants different music next time;
  ask for the lane (or a picker song on the silent version) before building the picture.
- `graphics/broncos-strip-sack/` (2026-11-09) — the **game clip + reaction photo** meme: his screen recording of a
  team reel (the play with the announcers), then a hard cut to him and Asher with two words ("WAIT… WE WON?!").
  A phone screen recording has Instagram's buttons burned in; crop to the clean window (recipe and coordinates in
  the 2026-11-09 log), show it as a card on its own blur, and punch in to follow the ball. The comp renders with
  `--alpha` (transparent over the clip, opaque on the photo). Check score and clock by web search before writing
  the hook. Tell him each time that broadcast footage can get a reel muted or pulled; posting is his call.
- `graphics/siriusxm-trick/` (2026-11-11) — a **screenshot meme for the personal account** (his SiriusXM renewal trick:
  tell the chatbot you're cancelling, get the $7.99 promo back; 12 s, silent, reel-cover type, no brand). When he sends
  screenshots of his own accounts, **redact before composing**: crop out account numbers, names and emails, bar anything
  that identifies him (car model) with a grey rounded bar in PIL, keep the raw screenshots out of the repo, and leave out
  any bubble that would need a bar through most of it. Hook on the number, his real message, a black beat, the payoff
  bubble with a stamp, one question at the end.
  **Threads (2026-11-13):** the same idea as a plain-text post on his personal Threads account, with no followers,
  got 266 likes and 88 replies in a day. Threads ranks by replies, not follows; a plain question in his caption voice
  ("am I the only one?") travels on its own. For the lender account: text posts there, Real Estate topic tag, reply to
  comments early. On Instagram, reach comes from Reels; Stories only reach followers.
- `graphics/broncos-pick/` (2026-11-08) — the **meme sequel, same night as the game** ("16 straight"): 10 s, payoff at
  7.3 s. New trick: the composition is rendered `--alpha` with a transparent hole (y 250–1302) and ffmpeg drops his
  screen recording of the broadcast replay into it, announcers at full level, a score bug whose status flips on the
  announcer's words and a BPM box above, the two of them draining to black-and-white below. He sends a phone screen
  recording of the highlight reel to Drive (five identical copies this time; take one); crop the Instagram chrome
  out (x 0–1130, y 560–1660 on 1290x2796) and transcribe it with `npx hyperframes transcribe` to find the beats.
  Broadcast footage he supplies is used at his request; it is Fox / NFL footage and Instagram may mute it, so say so
  on the page. `src/music/pick-bed.py` is the second sound lane (organ charge, heartbeat, impact + roar, warm pad).
  Facts come from web search (team sites and ESPN are blocked); put the real score and quarter on the bug and keep the
  clock off it unless a source gives it.
  **Kyle rejected the first cut** ("way too similar to last week… be a creative and art director… the organ is
  terrible, we'll figure out music on our own"). `comp2.html` is the keeper shape for a game meme: cold open on his
  replay recording full screen with the announcer's word slamming in, smash cut to his face on the key word, the
  two of them cut out (`npx hyperframes remove-background` works on a still PNG) on a flat Broncos-orange ground
  with a giant numeral or line *behind their heads*, one idea per second, a navy button card. **No music baked into
  a personal-account meme**; the recording's announcers are the only sound and he adds the song in Reels. An SFX-only
  version (`src/music/pick-sfx.py`: hit, ticks, slam, whoosh) is offered beside the clean one. A sequel must be a
  different piece, not last week's shape with new words.
  **He rejected that too** ("this is really the best you got? … come on be creative", and he considered handing the job
  to ChatGPT/Codex). What "creative" means to him: an *idea*, not a format. `comp4.html` (the toddler as the replay
  analyst: slow-mo insert with a telestrator ring, "Refs said incomplete." → Asher pointing, "My toddler: interception.")
  is the kind of thing he is asking for: find the joke in the photo and the argument in the game, then build around
  it. Lead with the controversy, make the kid the character, use the announcer's real words. A 1→16 counter and a
  caption are decoration, not an idea. `docs/handoff-broncos-pick.md` is the brief for handing a job to another tool;
  keep it current if he goes that way. Drive files he uploads to his **root** are private and unreachable; ask him to
  drop them in the `Clipforge` folder (link-shared) instead.
  **The cut that answered the brief** (`comp5.html`, `he-got-it.mp4`): real footage full-bleed from his screen recordings
  (the NFL reel's end-zone slow-mo, then the Fox ruling), captions that are only the announcers' exact words on their ASR
  onsets, a hard cut to the two of them **on the word "interception"** (his direction: "It's been ruled an interception
  and then show our faces. That's the cut."), then the ChatGPT-treated smile portrait he sent with his finish line baked
  in ("Another fourth-quarter win."). No counters, no slogans, no boxes, no isolated cutouts, nothing added to the
  announcers. His portrait look: navy `#001334`-ish ground, soft orange edge light, plain navy shirts; `yell-portrait.png`
  is the in-house imitation (cutout + blurred orange silhouette) until he sends the real one. For a game meme from now
  on: footage first and full screen, the reaction cut on the announcer's key word, one closing portrait with one line,
  10–12 s, payoff by 7 s.
- `graphics/bye-week-baby/` (2026-11-16) — the **AI-frame story meme** for the personal account: his daughter born on
  the Broncos' bye weekend, told with four Canva-generated frames of a "bronco dad" and a schedule card whose BYE gets
  flexed to "Dad vs. Baby Girl". **No heart-rate monitor twice in a row** (Kyle: "I'm not trying to do the exact same
  video over and over"); a repeat device from the last meme is a reason to find a new gag. He gives a storyboard in
  beats (relax, the line from his wife, "What?", the baby); follow it. For motion he has Grok and ChatGPT: put each
  frame on the page with a Save button and an image-to-video prompt, he sends the clips back, clipforge cuts them.
  **Type on a character piece (Kyle, same day): "you're covering the face … make it look more natural like an actual
  commercial."** Nothing over a face; dialogue as clean subtitles (Inter 700, ~56 px, white, soft shadow, no stroke) in
  the lower third, one small tracked super up top, graphics as a compact lower third. The stroked meme type is for
  photo memes, not for a story with a character.
  **Expression (Kyle, same day): "make them look more happy or animated."** Prompt every character frame for one big,
  readable emotion (bliss / shock / joy), not a neutral face. Canva's generate-image quota runs out after about eight
  images in a session; run jobs one at a time, and when it closes hand him `docs/handoff-bye-week-baby.md`-style briefs.
  **Other tools (2026-11-16):** ChatGPT's image tool, given our reference frames, returned the best still (real team
  gear, big expression, same character); plain ChatGPT chat cannot make video. Grok given a multi-shot brief returned
  storyboard sheets with baked-in text and a different character per panel ("Grok is awful"); only ever give it one
  picture and one "animate this exact image" line per clip.
  **What he approved in the end:** his own premise (Broncos stress → bye → "my water broke" → next Sunday), a
  **broadcast-style score bug** with real scores per beat ("like CBS or Fox, not so generic"), **smooth transitions**
  (whip, dissolves, one smash cut; `comp.html`'s scene list is the template for stills-as-video), a bigger fright
  (tight on the face, jump punch-ins, snap wide), effects-only sound with a very soft ending, song from the picker.
  My side gags (the flex, "Mom vs. Husband") he hated: build his premise, do not decorate it with a second joke.
  **Recap beats use the real clips** (his Logan screen recording for KC, the 2026-11-09 strip-sack reel for Carolina,
  pulled from that session's page with Artifact read-by-path) as preloaded frame sequences inside the comp; a TTS
  announcer over a still got "Absolutely not, we had a better one". **No TTS voices at all**: the Kokoro line for his
  wife was "such a machine thing"; her line is words on screen. Never clone a real announcer. The character has to
  **react** (arms up on the win, sat back on the bye), not hold one pose.
  **Smooth means the baby scene (round 13):** slow dissolves, slow pushes, quiet sound. He called reaction cut-ins,
  jump punch-ins, shake and thumps "too intense … terrible". Game footage goes **on the TV in the room** with its call
  as the sound (`.tv` inside `.room`), not full screen.
  **Flow (round 18, "very choppy"):** overlap the sound across picture changes (each call runs on 2 s under the next
  shot, one room tone under everything), dissolves of about a second, graphics fade in place. The punchline setup is
  short on purpose: the calm bye-week frame holds 1.3 s before "Honey… my water broke." The missing poses (fist pump,
  eyes-closed chill) came from one saved frame plus one pasted message to ChatGPT; do that first, not stand-ins.
  **The reaction follows the call (round 20):** a calm character under a rising announcer is "why it's terrible".
  Stage each game beat on the call's word onsets (room → eyes-wide close-up → fist pump) and caption the announcer's
  own words. His running order, verbatim: "Being a Broncos fan…" → game one → reaction → game two → reaction → calm
  bye week with a cup → "Honey, my water broke" → the ending. The room must read as a home, not a hotel lobby.
  **Rhythm he asked for (round 22):** tension → win → he sits back and breathes → again → calm → the interruption.
  Transitions "director, all swoosh": dissolve + a small sideways glide + a soft air sound. Voices for people in his
  life come from his own voice memos, never TTS.
  **Round 38:** "timing is still off with the announcer" meant the win pose was on the wrong word. Measure the call
  (speech-band energy per 0.1 s; whisper stamps can be a second off on crowd-heavy clips) and land the pose on the
  loudest word ("FIVE!", "FREE!"). He wants about 20 s: trim holds before trimming beats.
  **Round 35–36:** he disliked the first piano phrase and picked **the lullaby** from three labelled options (always
  give music as options to hear). A game beat needs at least three poses (sat back → nervous → win → sat back); one
  still held for a whole beat reads as "just sitting there". The win pose lands on the peak word of the call.
  **Round 33, the ending's sound:** soft original piano (`piano()` in `src/music/byeweek_flex.py`, C–G/B–Am–F then a held
  C) under the baby shot, a few dB under the calls; he heard the noise "room tone" there as "static". An emotional
  pay-off gets a warm tone even on a personal meme; noise beds are for under speech only.
  **Round 32, final timing:** the calm before the interruption holds about 2.6 s ("I want that to really marinate"),
  then her note flies in from the frame edge ("like it just came in from the other room") and holds 2 s. Earlier
  notes saying 1.3 s or "as soon as he sits down" are superseded.
  **Round 31, the score bug:** he wants "the actual score chips from the networks". `.bug2` now copies the real CBS bug
  cropped from his Panthers recording (dotted near-black bar, logo + huge white score, timeout dashes, team in focus
  on its colour, status in the centre); team logo SVGs come from upload.wikimedia.org into a gitignored `logos/`.
  Final running order and length he approved: 22 s, no Raiders line, her note big and held 2 s.
  **Round 27, where it landed:** type is the paper-cut strip (`paper()` in `comp.html`: torn sand strip, Playfair italic
  small words, Sora 800 big words, one orange key word, wiping on with words rising), her line a taped handwritten
  note in Caveat, the broadcast bug for scores. Plain captions "felt like reverting". Never crop a frame made for
  another moment into a new shot (the arms-up crop of the falling picture was "the one that really sucks"); if a beat
  has no frame of its own, hold the room shot and let the type carry it. Nunito captions from round 26 are superseded.
  **Round 26:** no pulsing or bumping on a still ("the freeze screen on his face that pulses" was wrong): a pose frame
  holds with one slow push. Captions in a character piece are **Nunito ExtraBold, white, soft shadow** (his reel
  caption look), not Inter. The pay-off shot (the baby) is "a peaceful, long lasting moment": 8 s or more, slow
  dissolve in, slow push, two unhurried lines, no score bug. This supersedes the `kick()` note below.
  **Round 24:** the excitement stays, but it moves with the call: he sits up as the announcer gets going and pumps on
  each yard line (`kick()` bumps the pose frame on the word onsets), a different pose for the second game, then the
  breath. "Don't be sitting there the entire time."
  **Round 23, the commercial rule:** one room, one camera angle, and a new pose for each turn of the story (leaning
  in and biting his nails when they are behind, sitting back when it is won, eyes closed on the bye). Never reuse one
  victory frame, never cut to a face from another angle ("randomized shots of the face, terrible"). List the poses the
  story needs and get them all from ChatGPT in one message **before** building the cut.
  Full-size Canva images come out through a scratch design + `export-design` (log 2026-11-16). When two chats are on
  the same job, find the other with `list_sessions`, read its page, and merge into one cut rather than showing two.
