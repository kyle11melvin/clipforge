#!/bin/bash
# VA county loan limit 2027 (2026-11-28): five unbroken takes of him, four glass cutaways over the edits, sounds.
#   1. npx hyperframes models install parakeet; npx hyperframes transcribe videos/va-limit/full.mp4 -e parakeet
#   2. python3 -I graphics/va-limit/tight-cut.py <that transcript.json>      -> videos/va-limit/cut.mp4
#   3. this script                                                           -> videos/va-limit/final-graphics.mp4
# No burned-in captions: the type over his takes and the cutaways carry every line.
set -e
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; G="$ROOT/graphics/va-limit"
cd "$ROOT/videos/va-limit"
DUR=43.53; SFX=${SFX:-0.5}
# his footage is blurred and darkened under each cutaway (CUT in overlay.html): the glass and the cards sit over it
CUTAWAYS="between(t,3.13,4.97)+between(t,8.10,19.97)+between(t,24.13,30.23)+between(t,36.87,40.83)"
[ -f overlay.mov ] && [ -z "$FORCE" ] || node "$ROOT/src/graphics/render.mjs" "$G/overlay.html" overlay.mov --alpha --duration $DUR --workers 3
python3 "$ROOT/src/music/chalk.py" sfx.wav "$G/sfx.json" --dur $DUR
ffmpeg -v error -y -i cut.mp4 -i overlay.mov -i sfx.wav -filter_complex "\
[0:v]split=2[sharp][b];[b]gblur=sigma=34,eq=brightness=-0.06[soft];\
[sharp][soft]overlay=enable='$CUTAWAYS'[base];\
[base][1:v]overlay=eof_action=pass,format=yuv420p[v];\
[0:a]aformat=sample_rates=48000:channel_layouts=stereo[vo];[2:a]volume=$SFX[fx];\
[vo][fx]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[au]" \
 -map "[v]" -map "[au]" -t $DUR -c:v libx264 -crf 17 -preset medium -r 30 -movflags +faststart -c:a aac -b:a 192k final-graphics.mp4
echo done
