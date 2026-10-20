# 2026-10-20 — Switchboard Commercial V3 (the written refinement brief)

Brief: combine V1's atmosphere and narrator with Commercial V2's clearer story, 28 s, 840 frames, and
above all restore the V1 narrator exactly. The brief said the files were in his Drive folder; they are in
this repo (`videos/switchboard/final.mp4`, `videos/switchboard/conv/Switchboard-Commercial-V2.mp4`).

## The narrator question

V1's narrator is Kokoro `am_michael` through `npx hyperframes tts` at default speed, no processing. The
voice model and the voice ID are still in the project, so the V3 script was read by the identical voice
with identical settings: not an extraction, not a lookalike. Told Kyle so before rendering, in the reply.
The softened Emma–Lily blend used on the V2 cuts was not used here, per the brief.

## Build

`graphics/switchboard-final/comp.html` is the Convergence composition retimed to the V3 scene plan, with
the V2 per-window layers added to the hook so the four AI windows come forward in turn before the camera
pushes through them into copper. New copy where the brief changed it ("A stronger question.", "The right
AIs.", "It doesn't just combine. / It challenges.", the new top answer), and the convergence tags are now
Useful insight / Unsupported claim / Contradiction. Icons are shared from `graphics/switchboard-conv/icons/`.

`tools/audio.py --music final --duration 28`: the conv bed on the longer timeline, plus the conv effects
track retimed through a `T(conv, final)` helper: digital accents under the hook windows, copper impact at
4.0, transformation sparkle at 8.7, activation tones at 11.9 / 12.3 / 12.7, completion hits at 14.6 /
15.6 / 16.6, shimmer and rise from 20.2, the ding at 23.9, the sonic logo at 26.0. Voice cues 0.4 / 4.4 /
8.3 / 11.3 / 14.3 / 18.4 / 23.2 / 26.2, gain 0.85 as in V1, no speed changes.

QC: 840 frames, 28.000 s, AAC 48 kHz stereo, no dark frames, no narration overlap, −20.3 LUFS.

## Delivered

`Switchboard-Commercial-V3.mp4` and a no-voice cut at the top of the artifact page; everything earlier
remains below. V1 and Commercial V2 files untouched.
