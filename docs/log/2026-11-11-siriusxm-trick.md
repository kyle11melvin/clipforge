# 2026-11-11 — "SiriusXM every year": a screenshot meme for the personal account

Kyle sent three screenshots of his SiriusXM account page and the Harmony chatbot: the promo ending ($7.99 → $25.99 due
12/10/26), his message "I'm going to need to cancel my subscription because of the price increase :(", and the bot's
offer thirty seconds later: the same Music & Entertainment plan at $7.99 for another 12 months. He has done this every
year for about seven years and wants it as a tip post on the personal account, not the lending brand. His one
instruction: "let's take out the personal information". He asked whether it should be a video or a post.

## What was built

- `graphics/siriusxm-trick/comp.html`, 12.4 s, silent, personal-account look (Nunito ExtraBold white with the black
  stroke, no Coastal Money): "SiriusXM every year:" over the billing card and "$7.99 → $25.99" (green / red) → "Every
  year I tell the chatbot:" with the chat header and his cancel bubble popping in → black beat "30 seconds later…" →
  "Same plan. $7.99 again." with the offer bubble, "Yes, thank you!" and a red "7 YEARS" stamp slamming in → "Anyone
  else do this every year?". Ground is the account page blown up, blurred past legibility and darkened.
- Redaction, done in PIL before anything was composed: the account number, name and email rows were never cropped in;
  the car model in the offer bubble is covered with grey bars (`offer.png`); the "I found an account with…" bubble
  that names the car was left out of the cut altogether. The crops (`billing`, `header`, `cancel`, `offer`, `yes`) are
  committed; the raw screenshots are not in the repo.
- `videos/siriusxm-trick/siriusxm-trick.mp4` (silent AAC track added so the share sheet treats it as a normal video),
  `cover.png` (t = 2.4, the hook frame), `contact.png`. Page: https://claude.ai/artifact/YQiFqrqMtSvKv3GssT3XNn with
  Save MP4, Save cover, the caption, the frames and the four redacted stills as a carousel option.
- Recommendation given: video. The same stills work as a carousel, so both are on the page.

## Open

- His reaction to the wording (stamp, closing question) and the caption.
- Music from the Reels picker (personal account, so the picker works). No bed baked in.
- Whether the car model may show; it is barred by default.

## Result (2026-11-13)

Kyle posted the idea as **plain text on Threads** (ke_melvin, no followers there): "Does anyone else do this with
SiriusXM? I pay $7.99/mo. Every year the promo ends and it jumps to $24.99. Every year I hop on a chat, say I want to
cancel, and they drop it right back to $7.99. 7 years running.... Is this just a thing everybody knows or am I the only
one?" 266 likes, 88 replies, 12 shares in 21 h, more than any of his reels except the Broncos one. No video, no
screenshots. He asked how Threads works and whether to do the same for the lender account. Answer given: Threads ranks
by replies, not followers, so a relatable question in plain text can travel from zero; post the lender takes there as
text with the Real Estate topic tag and reply to every comment early. On Instagram the discovery format is a Reel
(Stories only reach followers), so the video goes up as a Reel on the personal account.

## Threads drafts for the lender account (2026-11-13)

Kyle asked for an example of a past post turned into a Threads text post. Page: https://claude.ai/artifact/XAUtogJHidw6rvSqa4GoYk,
a Threads feed mock (avatar, handle, the post, a first reply) with copy buttons and character counts. Three drafts: his
20% down caption cut to the SiriusXM shape (hook, short lines, $24,000 on $800,000, veterans zero down, "What number did
you think it was?"), the OC price-vs-rate math from rate-wait, and the $458K price-cuts total. Quiz link goes in his own
first reply, placeholder `[quiz link]`; the real link has never been given to this repo. Drafts live in
`videos/threads-draft/` (gitignored, like all deliverables).

Kyle: "this is sweet". Scheduled task "Threads post reminder" (trig_013jrEPfvqc6LYKKzDxEVncr): daily 11:40 Pacific,
fresh session with a push notification, quiet until Wednesday 2026-11-18, then post 1 / 2 / 3 on Wed / Thu / Fri and a
generic "post one text take today" after that. He also asked how the same thing works on Instagram: answered that text
reaches new people there as a carousel (or a text-only reel), not a Story.
