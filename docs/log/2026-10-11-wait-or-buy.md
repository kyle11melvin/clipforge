# 2026-10-11 — "Wait or buy": the first mortgage-math graphics post

Kyle's brief (dictated): a post showing home prices up 3% a year and rates moving 3%, "what does it
equal in five years", and that you end up ahead if you buy now. No footage; a graphics-only video.

## What was built

`graphics/wait-or-buy/comp.html` → `videos/wait-or-buy/final-graphics.mp4` (24 s, 1080x1920, 30 fps),
delivered on the "Wait or Buy" artifact page with Save MP4, Open in new tab, a contact sheet, the math
and a copyable caption.

Scenes: hook ("Waiting for rates to drop before you buy?"), three assumption cards with counters
(+3%/yr, 7.40% today from Freddie Mac PMMS Oct 8 2026, say rates drop to 4.40%), a six-bar chart of the
example home climbing $1.00M → $1.16M with "+$159,274" counting up, a buy-now vs wait-5-years table
(you pay, 20% down, rate in year 5, payment in year 5, equity gained) with a SAME RATE stamp, and the
punchline "Same rate. $203,090 apart. Still waiting? Comment your price range and I'll run your numbers."

## The math (so it can be re-run for another price)

$1,000,000 home, +3%/yr → $1,159,274 in year 5. Buy now: $800k at 7.40% = $5,539/mo, balance $756,184
after 60 payments, refinance at 4.40% = $3,787/mo; equity gained $159,274 + $43,816 = $203,090. Wait:
$927,419 at 4.40% = $4,644/mo, $31,855 more down, $0 equity. P&I only; rent vs payment, taxes,
insurance and refi costs are not in it, and the on-screen footer says so.

Assumption made without asking: "interest rates 3%" was read as "rates drop 3 points". The 4.40% figure
is the generous case for waiting, which makes the buy-now result stronger. Confirm with Kyle.

## Pipeline change

`src/graphics/render.mjs` now falls back to `CLIPFORGE_CHROMIUM` or `/opt/pw-browsers/chromium` when
Playwright's own browser build is missing (the cloud container ships a different Chromium version).

## Kyle's reaction, mid-session

"That's not bad because I did not give you much direction." Then: he already runs an Instagram account
for his lending content with another Claude project and wants clipforge combined with it. That project
is not one of his GitHub repos (checked `finance` and `alvestor`; neither has Instagram content). It is
most likely a Claude Project whose instructions this session cannot read. Ask him to paste or attach that
project's instructions. His Instagram handle is known to the session but is kept out of this public
repo on purpose.

## Kyle's verdict on the delivered cut

"Wow. Good work. Make note." So the math-post format landed on the first pass: a hook question, three
assumption cards with a visible source, a to-scale chart, a two-column comparison, a stamp, a punchline
and a question back to the audience. Keep that shape for future number posts.

## Open items

- Get the other project's instructions and fold them into CLAUDE.md (brand, voice, posting cadence,
  any caption or hashtag rules). Compare with this file's rules and keep one brief.
- Confirm the "rates drop 3 points" reading and the example price ($1,000,000). Re-render takes a minute.
- Save MP4 button still unconfirmed on his phone.
