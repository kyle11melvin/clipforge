#!/bin/bash
# Stroller math (2026-11-28): walking selfie + one alpha layer (extruded type, $250, the 3D column beat on paper with
# him in a corner circle, the house photo card, his question) + sounds.
# Needs videos/stroller-math/cut.mp4 (the take trimmed at 5.58 s with punch-ins; see docs/log/2026-11-28-stroller-math.md)
# and final.mp4 from:
#   clipforge build footage/stroller-math/sdr --name stroller-math --caption-style rounded --caption-y 0.19 --caption-hide 0-6.9,15.2-32.0,38.4-40.4
set -e
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; G="$ROOT/graphics/stroller-math"
cd "$ROOT/videos/stroller-math"
DUR=45.2; SFX=${SFX:-0.5}
PIN=15.35; POUT=31.75          # the paper beat (T.paperIn / T.paperOut in overlay.html)
CX=190; CY=1322; CR=120        # the corner circle (CIRCLE in overlay.html)
[ -f overlay.mov ] && [ -z "$FORCE" ] || node "$ROOT/src/graphics/render.mjs" "$G/overlay.html" overlay.mov --alpha --duration $DUR
python3 "$ROOT/src/music/chalk.py" sfx.wav "$G/sfx.json" --dur $DUR
D=$((CR*2))
ffmpeg -v error -y -i final.mp4 -i overlay.mov -i sfx.wav -i cut.mp4 -filter_complex "\
[3:v]crop=760:760:160:640,scale=$D:$D,format=yuva420p,geq=lum='lum(X,Y)':cb='cb(X,Y)':cr='cr(X,Y)':a='255*lte(hypot(X-$CR,Y-$CR),$CR)'[circ];\
[0:v][1:v]overlay=eof_action=pass[a];\
[a][circ]overlay=$((CX-CR)):$((CY-CR)):enable='between(t,$PIN+0.3,$POUT+0.02)',format=yuv420p[v];\
[0:a]aformat=sample_rates=48000:channel_layouts=stereo[vo];[2:a]volume=$SFX[fx];\
[vo][fx]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[au]" \
 -map "[v]" -map "[au]" -t $DUR -c:v libx264 -crf 17 -preset medium -r 30 -movflags +faststart -c:a aac -b:a 192k final-graphics.mp4
echo done
