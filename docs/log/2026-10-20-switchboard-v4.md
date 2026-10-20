# 2026-10-20 — Switchboard Commercial V4 (marketing message, real logos, readable windows)

Fifth brief of the day. The asks: a consumer-friendly message ("Not all AI is created equal. So why rely on
just one?" → "One question. The right AIs. One top answer."), an eight-line script read by the V1
narrator, correct English inside the floating AI windows instead of the storyboard's gibberish, the real
provider logos, "Meet Switchboard" and "Just ask" as two separate moments, and the authentic Switchboard
logo. Kyle added mid-build: "Make sure to use our Switchboard logo!"

## The logo

Every earlier cut used the storyboard's own rendering of the mark (a four-node diamond with a serif
wordmark), cut out of the artwork. The real Switchboard mark is the app icon Kyle cropped from his home
screen for the Siri post, `graphics/siri-post/icons/switchboard.png`: three AI branches merging into one
copper node with an arrow, on a dark teal rounded square. V4 uses it in every logo moment: the "Meet
Switchboard" reveal, the prompt-field scene, the routing node, the convergence hub card (patched over the
drawn glyph) and the end card, upscaled 4× with Real-ESRGAN and cut to an iOS-style rounded square
(`graphics/switchboard-v4/logos/switchboard-icon.png`). The name is set as type (Fraunces Bold, copper) since
the only wordmark on hand was the storyboard's. If Kyle supplies a wordmark file, swap it in.

## Provider logos

Official brand marks from the `simple-icons` package: Claude, Google Gemini and Perplexity from the current
release, OpenAI from release 13 (later releases dropped it). Gemini carries its blue-to-red gradient,
Perplexity its teal, Claude its orange, OpenAI white on the dark glass. Grok is not shown. SVGs in
`graphics/switchboard-v4/logos/`. They identify the services only; nothing implies endorsement.

## Build

`graphics/switchboard-v4/comp.html`, 32 s, 960 frames. The hook is four HTML glass windows at different
depths in a perspective stage (parallax with a slow camera drift, a gentle float, a pull-back into copper),
each with its logo and one of the brief's example sentences; the original art sits behind them blurred to
pure light so no drawn text is legible. Scenes 2a/2b split the logo reveal and the empty prompt field with
"JUST ASK." Scene 3 types the question into the field and grows the sharpened prompt beneath it (Market
demand, Competition, Pricing, Launch strategy). Scenes 4–7 are the Convergence build with the real logos,
the three words COMPARE. / CHALLENGE. / COMBINE. in turn under the convergence, and the new top answer. The
end card carries the icon, the name and "ONE QUESTION. THE RIGHT AIs. ONE TOP ANSWER."

Narration: `am_michael`, no processing, cues 0.4 / 5.3 / 7.3 / 9.3 / 17.3 / 21.3 / 27.0 / 30.5; the long
"sharpens your prompt and picks the AIs" line runs across scenes 3 and 4 as written. Score
`--music v4 --duration 32`; effects retimed through a per-style table (impact 5.0, transformation 11.1,
tones 14.0 / 14.5 / 15.0, hits 17.6 / 18.6 / 19.6, rise from 24.2, ding 27.6, sonic logo 30.0).

QC: 960 frames, 32.000 s, no dark frames, no narration overlap, −20.6 LUFS.
