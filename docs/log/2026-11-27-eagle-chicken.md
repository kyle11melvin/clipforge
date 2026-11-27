# 2026-11-27 — Eagle or chicken short (photo + type, not a mortgage post)

Kyle sent two text-heavy graphics someone else made ("Live like a chicken or soar like an eagle", and a murky glass vs
ocean analogy) and asked to make them better. He wanted a prompt for ChatGPT first: it made text-free 4:5 photo plates
(eagle on flat blue sky, hen pecking in a desert), and the type is set here. Only the eagle and chicken came back.

- `graphics/eagle-chicken/comp.html`, 23.2 s, silent. Hook: eagle above, chicken below, title band between. Chicken:
  his thoughts flash as hard swaps that speed up (0.62 s down to 0.32 s), ink type in the hazy sky. Hard cut to the
  eagle: a beat of empty sky, then thoughts fade in one at a time at 0.95 s each, cream type. The pacing is the idea.
- A 4:5 plate with a flat sky extends to 9:16 by filling the ground with the sky colour and masking the photo's top edge.
- Wording is the original's with typos fixed (beginning, higher) and each thought as its own sentence. Not Coastal
  Money colours; Sora and Manrope only for legibility. He did not say which account it is for.
- Page: "Eagle or Chicken Short" (Save MP4, cover, stills, caption draft).

Open: his verdict; the glass and ocean plates for the murky-water half; music; which account.

## Second pass: faster, with music

Kyle: "Speed up the content but otherwise great", and music: once the eagle hits it should be uplifting, "like someone
just saw the sunset in the sky for the first time in their entire life".

- Timings cut from 23.2 s to 17.6 s: hook 2.2 s, chicken thoughts 0.45 s down to 0.25 s, eagle thoughts 0.7 s each.
- `src/music/eagle.py` (numpy only): an A pedal with a Bb rubbing on it and a tick plus thud on every chicken thought,
  0.28 s of silence before the cut, then D major (D, Bm7, G, A, D) with a wide pad, low D and a bell on every eagle
  thought, in a 3 s hall. Timings are duplicated from the comp. Mean level -17 dB under the chicken, -11 dB under the eagle.
- `videos/eagle-chicken/final.mp4` is the muxed file. Not heard by Claude.
