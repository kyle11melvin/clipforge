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
