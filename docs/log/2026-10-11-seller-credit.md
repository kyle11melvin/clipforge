# 2026-10-11 — Seller credit: a carousel turned into a video, with b-roll

Kyle sent the three slides of his seller-credit carousel ("Stop negotiating the price. Negotiate this:
$48,000" / "Price is only part of the negotiation. Ask for a seller credit." / "How much can you ask for?
More than you think… and put the credit where it helps you most. Read the caption to find out") and asked
for a video clip "with effects and all, b-roll, you name it".

## What was built

`graphics/seller-credit/comp.html` → `videos/seller-credit/final-graphics.mp4` (40.5 s, 1080x1920, 30 fps),
in Coastal Money style, started from `graphics/wait-or-buy-cm/`. Delivered on the "Seller Credit Post"
artifact page with Save MP4, Open in new tab, the contact sheet, the math and a copyable caption.

Scenes: hook over a dusk photo (slow push-in, navy scrim) with the two-tone claim, $48,000 slamming in and
the carousel's scribble underline drawing itself; a terracotta field wiping up for "Price is only part of
the negotiation. Ask for a seller credit."; the sand setup slide ($800,000, 20% down, 7.40% Freddie Mac)
with the Caveat note "The seller can credit up to 6% of the price." and $48,000 counting up; 01/02 numerals
for "off the price" vs "toward your rate" with the rate ticking 7.40% → 6.00%; two to-scale bars ($266 vs
$594 a month) with counters; the big $31,680 over five years; DM BUYDOWN sign-off.

New effects added to the house style: an SVG scribble underline drawn with `stroke-dashoffset` (matches the
hand-drawn stroke on his carousel), a clip-path wipe between scenes instead of the cross-fade, a counter on
a rate inside a sentence, a Ken Burns push-in on a photo hook.

## The math (so it can be re-run)

$800,000 price, 20% down, $640,000 loan at 7.40% = $4,431/mo. Conventional seller-credit cap with 10–25%
down is 6% = $48,000. Off the price: loan $601,600 = $4,165/mo, saves $266. As a credit: $12,000 closing
costs, $36,000 in points at 0.25% per point = 7.40% → 6.00%, $3,837/mo, saves $594. Gap $328/mo × 60 =
$19,680, plus the $12,000 not brought to closing = $31,680. P&I only. Assumptions made without asking: the
price, the closing-cost figure and 0.25% per point; all stated on screen in scene 4 and on the page.

## Pictures

- Canva's `generate-image` works from here but the full-size file cannot be downloaded (media.canva.com is
  blocked by the network policy); only a 112 px thumbnail comes back. Not usable.
- Kyle, mid-session: "unsplash.com — greatest site if you need pics." `images.unsplash.com` is reachable
  (unsplash.com itself returns 401 to curl; WebFetch on a search page lists the photo ids). The hook uses
  photo-1785088477131-10d1ec43e3f8 by Kellen Riggin (palms and houses at dusk), fetched at 1080x1920 with
  `?w=1080&h=1920&fit=crop`. Use Unsplash for any photo hook from now on.

## Open items

- His verdict on the cut, and on the example figures ($800,000, $12,000 closing costs, 0.25% per point).
- DM keyword: BUYDOWN is reused; CREDIT would be a new one.
- No voice or music bed yet.
- Save MP4 still unconfirmed on his phone.
