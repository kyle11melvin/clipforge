---
name: clipforge-meme
description: Build a meme or story reel for Kyle's personal account (Broncos game memes, family stories, screenshot jokes), where the Coastal Money brand rules do not apply. Use when he says "personal account", sends a game clip or screen recording with a reaction photo, a screenshot of something funny that happened to him, or a storyboard for a character piece.
---

# Personal-account meme

"This is the straight personal account": drop the brand rules and go for the joke. `history.md` beside this file
has every past meme, the rounds it took and the files to start from. Run `clipforge-review` before he sees a cut.

## Rules that hold for every meme

- **An idea, not a format.** Find the joke in the photo and the argument in the situation. A sequel must be a
  different piece; never repeat last week's device (no heart monitor twice).
- **Build his premise and his storyboard.** No side gags of your own.
- **Short.** Under about 12 s for a game meme, payoff by 7 s. A story piece about 20 s: trim holds before beats.
- **Real things on screen.** The real score, quarter and announcer's words, checked by web search (team sites and
  ESPN are blocked). Keep the clock off the bug unless a source gives it.
- **No music baked in.** The recording's own sound is the sound; he adds the song in Reels. Never a commercial
  track. If music is wanted for an ending, give labelled options to hear.
- **No TTS voices, ever.** Never clone an announcer. Voices of people in his life come from his own voice memos;
  otherwise the line is words on screen.
- **No continuous synthesised noise beds.** Short quiet hits only.
- **Broadcast footage he supplies is used at his request.** Tell him each time that it can get a reel muted or
  pulled; posting is his call.
- **Redact his own screenshots** before composing (account numbers, names, emails, car model). Raw screenshots and
  family photos stay out of this public repo.

## Game meme (clip + reaction)

Start from `graphics/broncos-pick/comp5.html`. Footage first and full screen from his screen recording; captions
are only the announcers' exact words on their onsets; hard cut to the two of them **on the announcer's key word**;
one closing portrait with one line. No counters, slogans, boxes or isolated cutouts.

1. Ask for his phone recording of the play with the call, and a reaction photo of Asher. Build the same night.
2. Take one copy from Drive `Clipforge`. Crop the Instagram chrome (x 0–1130, y 560–1660 on 1290x2796).
3. `npx hyperframes transcribe` for the beats. On a crowd-heavy clip, measure speech-band energy per 0.1 s and land
   the cut on the loudest word; whisper stamps can be a second off.
4. Render the comp `--alpha` over the clip, announcers at full level.

## Story or character piece (AI frames)

Start from `graphics/bye-week-baby/comp.html`. It plays like a commercial: one room, one camera angle, a new pose
for each turn of the story, and the reaction follows the call.

1. List every pose the story needs and get them all from ChatGPT's image tool in one message, before building.
   Prompt each for one big readable emotion. Never crop a frame made for another moment into a new shot.
2. Nothing over a face. Type is the torn paper strip (`paper()`); a line from a person is a taped Caveat note.
3. Scores go on the copied network bug (`.bug2`). Game footage plays on the TV in the room with its call as sound.
4. Transitions: dissolves of about a second with a small sideways glide and a soft air sound. Overlap sound across
   picture changes. No pulsing, shake, jump punch-ins or thumps.
5. The pay-off shot is long and peaceful (8 s or more, slow push, warm soft piano, no bug).

## Screenshot meme

Start from `graphics/siriusxm-trick/`. Hook on the number, his real message, a black beat, the payoff with a stamp,
one question at the end. Silent, about 12 s, reel-cover type (Nunito ExtraBold, white, black stroke).

## After he reacts

One thing per message; change only what he named. Add the post and his verdict to `history.md`.
