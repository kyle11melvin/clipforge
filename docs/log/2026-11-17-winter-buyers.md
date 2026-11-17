# 2026-11-17 — "Isn't winter the best time to buy?" (first-time buyer questions, post 1)

Brief from the Coastal Money Project: 18 s graphics-only reel, four full-screen type scenes (4/4/5/5 s), navy and sand
alternating, no CTA scene, no audio, plus the four scenes as 1080x1350 carousel stills.

- `graphics/winter-buyers/comp.html`: every line carries a `data-at` time and fades in on it; hard cuts. All type inside
  x 64-940, y 250-1450 (`#zones` paints the chrome). The brief's bottom margin (400 px) is looser than our 470; ours won.
- `#move` is the same copy with the push-up transition and slow drift Kyle asked for on the Address Advantage reel the
  same morning. The brief said "flat, hard cuts", so both went on the page for him to pick.
- `#car` shifts each scene up 205 px for 1080x1350 stills:
  `node src/graphics/still.mjs "graphics/winter-buyers/comp.html#car" out.png --t 3.9|7.9|12.9|17.9 --size 1080x1350`.
- Output in `videos/winter-buyers/`: `final-graphics.mp4`, `final-graphics-move.mp4`, `carousel-1..4.png`, `cover.png`
  (the hook slide). Page has a caption draft in his voice since the brief had none.

Open: his pick of flat vs moving, and the caption.
