#!/bin/bash
# Stroller math (2026-11-28), the tight cut: walking selfie + one alpha layer (extruded type, $250, the full-screen 3D
# column beat with the arrow and percent, the house photo card, his question) + sounds.
# Order (see docs/log/2026-11-28-stroller-math.md):
#   1. npx hyperframes models install parakeet; npx hyperframes transcribe <the 45 s cut> -e parakeet   (word edges)
#   2. python3 -I graphics/stroller-math/tight-cut.py <that transcript.json>      -> cut.mp4, transcript.json
#   3. this script                                                                -> final-graphics.mp4
# No burned-in captions: the type over his takes and the paper cutaways carry every line, so it composites over cut.mp4.
set -e
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; G="$ROOT/graphics/stroller-math"
cd "$ROOT/videos/stroller-math"
DUR=20.83; SFX=${SFX:-0.5}
[ -f overlay.mov ] && [ -z "$FORCE" ] || node "$ROOT/src/graphics/render.mjs" "$G/overlay.html" overlay.mov --alpha --duration $DUR
python3 "$ROOT/src/music/chalk.py" sfx.wav "$G/sfx.json" --dur $DUR
ffmpeg -v error -y -i cut.mp4 -i overlay.mov -i sfx.wav -filter_complex "\
[0:v][1:v]overlay=eof_action=pass,format=yuv420p[v];\
[0:a]aformat=sample_rates=48000:channel_layouts=stereo[vo];[2:a]volume=$SFX[fx];\
[vo][fx]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[au]" \
 -map "[v]" -map "[au]" -t $DUR -c:v libx264 -crf 17 -preset medium -r 30 -movflags +faststart -c:a aac -b:a 192k final-graphics.mp4
echo done
