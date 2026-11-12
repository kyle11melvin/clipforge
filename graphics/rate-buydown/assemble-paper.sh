#!/bin/bash
# Round three of the rate-buydown reel (2026-11-12): no hook slide, paper-cut type until the board arrives, the
# chalkboard box swooping in at 9.78 s, chalk and eraser sounds. Run from anywhere; works in videos/rate-buydown/.
#
# Needs there:  punched.mp4      cut.mp4 with the punch-ins (zoompan, top-anchored; see the 2026-11-12 log)
#               cutout-a.mov     hyperframes remove-background of the first 4.85 s of punched.mp4 (Clip A)
#               type-bg.mov / type-fg.mov   graphics/rate-buydown/type.html#bg / #fg, --alpha, 9.9 s
#               board-full.mov   board-box.html#t0=9.7&in=9.78&full, --alpha, 21.1 s
#               sfx.wav          src/music/chalk.py from graphics/rate-buydown/sfx-events.json
#               bed0.wav         src/music/underbed.py --intro 0 --beat 0.77 --bars 10
# Writes final-reel-v3.mp4 (voice + chalk sounds) and final-reel-v3-music.mp4 (the bed under it as well).
set -e
cd "$(dirname "$0")/../../videos/rate-buydown"
SFX=${SFX:-0.55}; BED=${BED:-0.126}
ffmpeg -v error -y -i punched.mp4 -i type-bg.mov -i cutout-a.mov -i type-fg.mov -itsoffset 9.7 -i board-full.mov -i sfx.wav -filter_complex "\
[0:v][1:v]overlay=eof_action=pass[a];\
[a][2:v]overlay=eof_action=pass:enable='lt(t,4.80)'[b];\
[b][3:v]overlay=eof_action=pass[c];\
[c][4:v]overlay=eof_action=repeat:enable='gte(t,9.7)',format=yuv420p[v];\
[0:a]aformat=sample_rates=48000:channel_layouts=stereo[vo];[5:a]volume=$SFX[fx];\
[vo][fx]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[au]" \
 -map "[v]" -map "[au]" -t 30.8 -c:v libx264 -crf 17 -preset medium -r 30 -movflags +faststart -c:a aac -b:a 192k final-reel-v3.mp4
ffmpeg -v error -y -i final-reel-v3.mp4 -i bed0.wav -filter_complex "\
[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=$BED,afade=t=in:d=0.3[bed];\
[0:a][bed]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[au]" \
 -map 0:v -map "[au]" -c:v copy -c:a aac -b:a 192k -movflags +faststart final-reel-v3-music.mp4
echo done
