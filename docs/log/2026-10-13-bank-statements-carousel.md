# 2026-10-13 — "Bank statements": the first Instagram carousel (stills, not video)

Kyle's brief arrived fully specified, slide by slide, with font, colour and role per line, in Coastal Money
terms (Sora/Manrope/Caveat, navy/sand/terracotta/sage). "Create slides for a carousel, not a video for IG."

## What was built

`graphics/bank-statements/slides.html` → `videos/bank-statements/slide-01.png` … `slide-05.png`
(1080x1350 each) and `contact-sheet.jpg`. Delivered on a private artifact page with a Save button per slide
(PNG to Photos via the share sheet), a Save-all button and a copyable caption.

1. Hook (navy): "Moving money before you buy?" sand, "Your lender will ask." terracotta, continuation
   "What your bank statements show →".
2. Editorial (sand): eyebrow WHAT THEY REVIEW, "Your last two months of statements.", body line, Caveat
   note "Keep the paper trail."
3. Numerals (navy): "Before you apply." then 01 (terracotta) / 02 / 03 (sage) rows.
4. Big number (navy): THE LINE, oversized $6,000, "Earn $12,000 a month? A deposit over $6,000 needs a
   source if you're using it to buy."
5. CTA (navy): "Not sure where you're at?", the readiness-quiz ask (link in Story and bio), hairline,
   primary portrait, Kyle Melvin, NMLS, a one-line disclosure.

Two calls made without asking: NMLS #1486450 and a short disclosure line ("For education only. Every
file is different. Equal Housing Opportunity.") were added under the sign-off, per the standing rule to keep
them unless he says otherwise. The brief listed only hairline · portrait · name. One word removes them.
The CTA is a quiz link, not a DM keyword; built as briefed.

## Pipeline change

New `src/graphics/slides.mjs`: screenshots every `section.slide` in an HTML file at its own pixel size and
writes a contact sheet with FFmpeg. Same Chromium fallback as `render.mjs`. Usage:
`node src/graphics/slides.mjs graphics/<post>/slides.html videos/<post>/`.

## Open items

- Kyle's verdict on the slides; whether to keep NMLS and the disclosure line on a non-numbers post.
- The quiz link itself is not in the repo; the caption says "link in my bio".
