#!/bin/bash
# 20% down myth, remix (2026-11-21): the same take with a tag that snaps, a full-screen paper beat with him in a
# corner circle, and two seller-credit cards. A test of the Skool-ad props; not for posting.
# Needs videos/20-down/cut.mp4 (clipforge build footage/20-down-myth/sdr --name 20-down). Writes final-remix.mp4.
set -e
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; G="$ROOT/graphics/20-down-myth"; R="node $ROOT/src/graphics/render.mjs"
cd "$ROOT/videos/20-down"
DUR=30.8; SFX=${SFX:-0.5}
PIN=17.06; POUT=21.72          # the paper beat (TIMES.in / TIMES.out in remix.html)
CX=190; CY=1322; CR=120        # the corner circle (CIRCLE in remix.html)
$R "$G/ui.html#render" ui.mov --alpha --duration $DUR          # the word-by-word type; its app window and flow are gated out below
$R "$G/remix.html#render" remix.mov --alpha --duration $DUR
python3 "$ROOT/src/music/chalk.py" sfx-remix.wav "$G/sfx-remix.json" --dur $DUR
S() { echo "(1-pow(1-min(1,max(0,(on/30-$1)/0.4)),2))"; }
Z="1+0.08*($(S 12.2)-$(S 21.6)+$(S 25.0)-$(S 28.7))"
D=$((CR*2))
ffmpeg -v error -y -i cut.mp4 -i ui.mov -i remix.mov -i sfx-remix.wav -filter_complex "\
[0:v]scale=2160:3840:flags=bicubic,zoompan=z='$Z':x='iw/2-(iw/zoom/2)':y=0:d=1:s=1080x1920:fps=30,setsar=1,eq=contrast=1.04:saturation=1.05,split[base][f];\
[f]crop=820:820:238:640,scale=$D:$D,format=yuva420p,geq=lum='lum(X,Y)':cb='cb(X,Y)':cr='cr(X,Y)':a='255*lte(hypot(X-$CR,Y-$CR),$CR)'[circ];\
[base][1:v]overlay=eof_action=pass:enable='not(between(t,12.27,21.8))*not(between(t,25.02,28.76))'[a];\
[a][2:v]overlay=eof_action=pass[b];\
[b][circ]overlay=$((CX-CR)):$((CY-CR)):enable='between(t,$PIN+0.42,$POUT+0.02)',format=yuv420p[v];\
[0:a]aformat=sample_rates=48000:channel_layouts=stereo[vo];[3:a]volume=$SFX[fx];\
[vo][fx]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[au]" \
 -map "[v]" -map "[au]" -t $DUR -c:v libx264 -crf 17 -preset medium -r 30 -movflags +faststart -c:a aac -b:a 192k final-remix.mp4
echo done
