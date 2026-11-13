#!/bin/bash
# The 20% down myth reel with mock-app props (2026-11-13). Works in videos/20-down/.
# Needs there: cut.mp4 (clipforge build of the pre-converted SDR clip, "2%" fixed to "20%" in transcript.json),
#   ui.mov   node src/graphics/render.mjs "graphics/20-down-myth/ui.html#render" videos/20-down/ui.mov --alpha --duration 30.8   (any hash turns the blue probe ground off)
#   sfx.wav  python3 -I src/music/chalk.py videos/20-down/sfx.wav graphics/20-down-myth/sfx-events.json --dur 30.8
# The footage punches in 8% (top-anchored, eased) while a card is up, which drops his hair clear of it.
set -e
cd "$(dirname "$0")/../../videos/20-down"
SFX=${SFX:-0.5}
S() { echo "(1-pow(1-min(1,max(0,(on/30-$1)/0.4)),2))"; }
Z="1+0.08*($(S 12.2)-$(S 21.6)+$(S 25.0)-$(S 28.7))"
ffmpeg -v error -y -i cut.mp4 -i ui.mov -i sfx.wav -filter_complex "\
[0:v]scale=2160:3840:flags=bicubic,zoompan=z='$Z':x='iw/2-(iw/zoom/2)':y=0:d=1:s=1080x1920:fps=30,setsar=1,eq=contrast=1.04:saturation=1.05[f];\
[f][1:v]overlay=eof_action=pass,format=yuv420p[v];\
[0:a]aformat=sample_rates=48000:channel_layouts=stereo[vo];[2:a]volume=$SFX[fx];\
[vo][fx]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[au]" \
 -map "[v]" -map "[au]" -c:v libx264 -crf 18 -maxrate 3400k -bufsize 6800k -preset medium -r 30 -movflags +faststart -c:a aac -b:a 192k final-ui.mp4
echo done
