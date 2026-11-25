# 2026-11-25 — Winter swipe carousel (seamless 8-slide, lender account)

Kyle sent a screen recording of a real-estate team's seamless carousel (dark ground, portraits and objects split across
slide seams, two small lines per slide) and asked for the same for the lender account, then supplied the winter-buyer
copy himself. Flagged that it repeats the 2026-11-17 winter reel; he went ahead.

- `graphics/winter-swipe/comp.html`: one 8640x1350 strip in Coastal Money navy. Portraits (cut out with `rembg`) sit on
  the 1|2 and 7|8 seams, a moving box on 3|4, keys on 5|6. `#seams` draws slide edges and the 64 px margins.
  `still.mjs --size 8640x1350`, then `slice.py strip.png outdir` for eight 1080x1350 slides.
- First pass used oversized numerals ("53", "$") on the middle seams. Kyle: good first pass, keep the brand colours,
  but use actual objects, from Unsplash. Box is Giorgio Trovato's, keys are Jozsef Hocza's (free licence).
- Unsplash: `unsplash.com` 401s from curl here, but the web-fetch agent can read `unsplash.com/s/photos/<query>?license=free`
  and `images.unsplash.com/photo-<id>?w=2600` downloads directly.
- The number: "53 median days on market, Orange County, week of Nov 16, 2026", from a search summary of the
  ocrealestateinc.com weekly report. The page itself could not be opened from this session, so it is unconfirmed and
  the page says so.
- Page: "Winter Swipe Carousel" (swipe preview, save button per slide, caption draft with a copy button).

Open: confirm the 53; his portraits are daylight shots on navy (a dark-wall portrait would sit better); slides 6 and 7
are Claude's wording; the guide says no portrait on a hook, and this format puts one there at his request.
