---
name: motion-graphics
description: Build a vertical motion-graphics video (animated text, screenshots, charts, chat mockups) in the approved clipforge style, from a brief and a few images. Use when Kyle asks for a graphics video, b-roll, animated captions over stills, or "something like the Siri video".
---

# Motion graphics video

Read `CLAUDE.md` first for the approved look, tone and Kyle's working preferences.

## Steps

1. **Pin the message.** Restate the point of the post in one line and the punchline. If the brief is dictated
   and garbled, infer intent and confirm any wording that will appear on screen.
2. **Collect assets.** Crop what is needed from his screenshots with Pillow (`python3 -I`): app icons as
   square 400 px PNGs, screenshots at full width (check the real pixel size first, phone screenshots are often
   1256 px wide or more). Put them beside the composition.
3. **Start from the reference.** Copy `graphics/siri-post/comp.html` to `graphics/<name>/comp.html`. Keep the
   helpers (`p`, `easeOut`, `easeInOut`, `back`, `sceneOpacity`) and the scene-window table `S`. Replace the
   scenes. Every element is positioned from `t` inside `window.seek(t)`; no CSS transitions or keyframes.
4. **Probe before rendering.** `node src/graphics/render.mjs graphics/<name>/comp.html /tmp/probe.png --probe
   t1,t2,...` with one time per scene, late enough that the scene's animation has landed. Look at the sheet.
   Fix clipping, wrapping and overlap (add `white-space: nowrap`, resize, or move the next element down).
5. **Render.** `node src/graphics/render.mjs graphics/<name>/comp.html videos/<name>/final-graphics.mp4
   --duration <s>`. A 20 s render takes about 40 s.
6. **Deliver.** Upload the MP4 as an asset to a private artifact page with a `<video>` player, a Save MP4
   button (`downloads` capability, filename ending in .mp4), an "Open in new tab" link, and a copyable
   caption. Keep the earlier cut linked for comparison. Also send the file with SendUserFile.
7. **Report.** Scene by scene in a short list, then what is still missing (footage, voice, data sources).

## Composition conventions

- Scenes are `div.scene` blocks, absolutely positioned, faded in and out over 0.25 s by `sceneOpacity`.
- Stagger text word by word (0.09 s apart). Pop icons with `back` easing and a counter in the headline.
- Chat mockups: grey left bubble for "what I said" typed out with a cursor, blue right bubble for the wrong
  version with the bad words in a red wavy underline. Label each with a small uppercase caption.
- Charts: draw to scale from real data, source in a corner, gold for the series, grey for the grid.
- Fonts are system Inter / Inter Display. Nothing is fetched from the network.
