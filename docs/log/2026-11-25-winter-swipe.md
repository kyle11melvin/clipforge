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

## Third pass

Kyle: does not want his picture in twice ("or the same headshot", even in a different outfit), and asked what a
marketer would change about the look, copy and items. Rebuilt: one portrait only, on the 7|8 seam; a wreath on 1|2
(Unsplash, Spencer Imbrock) so each object sits beside the line it illustrates (holidays, moving, keys); hook is type
plus object, no face; copy rewritten ("Nobody house hunts in December. Good."); the unconfirmed 53 removed.

Open: his verdict on the rewritten copy; a real figure from one of his own deals; the objects come from three
different photographers and do not share lighting.

## Object set B

Kyle: "Good for now but I want to see another. Find a better matched Unsplash set." `comp-b.html` swaps in a twig
wreath (Mel Poole), an open kraft box with an orange edge (Giorgio Trovato) and a single key (Kelly Sikkema, tinted
brass with PIL `colorize` so all three sit in one kraft/brass family). Searching Unsplash for "dark background" objects
returned nothing usable; white-background studio shots cut out cleanly and match once graded. The page has a set A / set B
switch. Open: his pick; the key is stamped "Duplication prohibited".

## His pick

Kyle: the wreath from set A, the box and key from set B. `comp.html` is now that combination (wreath Spencer Imbrock,
box Giorgio Trovato, key Kelly Sikkema tinted brass); `comp-b.html` and the unused cutouts are gone.

Kyle asked for the key's "Duplication prohibited" stamp to be blurred; done in `key.png` (feathered blur with grain).
