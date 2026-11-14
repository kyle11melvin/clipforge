# 2026-11-13 — "Is your family growing?": a photo reel with type and music

After the Threads drafts, Kyle sent a family maternity photo (him, his wife and Asher in a field) and asked: "What about
a photo and then have the text on it with music? Something like is your family growing? If you need an additional
bedroom I have some amazing agents I work with." Lender account, so Coastal Money.

## What was built

- `graphics/family-growing/comp.html`, 10.5 s: the photo full-bleed (1200x1800 from y=150, slow push-in 1.0 → 1.08),
  navy scrim top and bottom, three beats of Sora type in the lower safe-zone window (bottom: 500 px): "Is your family /
  growing?" → "Need another / bedroom?" → "I work with some / amazing agents." with a Caveat "message me." Terracotta on
  the second line each time. Words rise one by one; beats cross-fade. No cards, no sign-off.
- First scrim pass hid the whole lower half of the photo (percent stops on a 1920 canvas); switched to pixel stops so
  the photo shows down to her shorts and Asher's jeans. Lesson: write scrim stops in px on these frames.
- `src/music/warm.py`: a soft bed with numpy only (Rhodes-like chords Cmaj7 / Am9 / Fmaj7 / G add9 over a sine pad, a
  low swell under the last line), since scipy is not installed in this session. Two files: `family-growing-silent.mp4`
  for a picker song from ke_melvin (beats at 0 / 3.5 / 7 s) and `family-growing-warm.mp4` with the bed (Original audio).
- Cover at 2.8 s, contact sheet, page https://claude.ai/artifact/JNjT6wPxrj24PnBvTdRe1t (silent / bed toggle, Save MP4,
  Save cover, caption in his voice, notes). The photo is gitignored in `graphics/family-growing/`.

## Open

- His call on the wording (lightly trimmed from his dictation) and the caption.
- Which audio: picker song on the creator account, or the bed from the business account.

## Result (2026-11-14)

46 views as a story, 2 likes as a reel. Kyle: "I thought the video was good but we need to figure out what the sweet
spot is", against the SiriusXM text on Threads (now ~300 likes, ~120 comments from strangers). Pattern across the whole
log: what travelled was unbranded, personal, about something he actually did, with a number and a question, and no
pitch (Broncos meme ~15K, SiriusXM text ~300 likes). The polished Coastal Money reels with a CTA sit in the hundreds of
views: price-cuts 333, this one 2 likes. Reach is not coming from the graphics; it comes from the relatable premise and
the question. Plan given: Threads text daily on the lender account (reminders already running), phone-shot ten-second
talking heads about a real client this week ending in a question, brand graphics kept for the grid, not for discovery.
