#!/bin/bash
# Rate-buydown remix (2026-11-21): the same take with cards from behind his head, a full-screen paper beat for the
# math with him in a corner circle, and two flip tiles. A test of the props taken from the Skool ad; not for posting.
# Needs videos/rate-buydown/cut.mp4 (clipforge build footage/rate-buydown/sdr) and footage/rate-buydown/sdr/c.mp4.
# Renders every layer itself; takes about ten minutes. Writes final-remix.mp4.
set -e
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; G="$ROOT/graphics/rate-buydown"; R="node $ROOT/src/graphics/render.mjs"
cd "$ROOT/videos/rate-buydown"
DUR=31.75; SFX=${SFX:-0.5}
PIN=16.12; POUT=22.86          # the paper beat (TIMES.paperIn / paperOut in remix.html)
CX=190; CY=1322; CR=120         # the corner circle (CIRCLE in remix.html)

# 1. punch-ins, top-anchored: +10% on "and still lose money", +8% on "That's exciting", +7% from 9.78 s on
Z="1+0.10*between(on/30,3.6,4.79)+0.08*between(on/30,7.2,7.99)+0.07*(1-pow(1-min(1,max(0,(on/30-9.78)/0.4)),2))"
ffmpeg -v error -y -i cut.mp4 -vf "fps=30,scale=2160:3840:flags=bicubic,zoompan=z='$Z':x='iw/2-(iw/zoom/2)':y=0:d=1:s=1080x1920:fps=30,setsar=1,eq=contrast=1.04:saturation=1.06" \
 -c:v libx264 -crf 15 -pix_fmt yuv420p -c:a aac -b:a 256k punched.mp4
# the unused smile after "keep the cash", held a moment for the cash and the ding
ffmpeg -v error -y -ss 8.73883 -t 0.65 -i ../../footage/rate-buydown/sdr/c.mp4 -vf "fps=30,scale=1156:2054:flags=bicubic,crop=1080:1920:38:0,eq=contrast=1.04:saturation=1.06,tpad=stop_mode=clone:stop_duration=0.4" \
 -af "aformat=sample_rates=48000:channel_layouts=stereo,apad=pad_dur=0.4" -c:v libx264 -crf 15 -pix_fmt yuv420p -c:a aac -b:a 256k tail.mp4
ffmpeg -v error -y -i punched.mp4 -i tail.mp4 -filter_complex "[0:v]fps=30,format=yuv420p,setsar=1[a];[1:v]fps=30,format=yuv420p,setsar=1[b];[a][b]concat=n=2:v=1:a=0[v];[0:a]aformat=sample_rates=48000:channel_layouts=stereo[x];[1:a]afade=t=in:d=0.03[y];[x][y]concat=n=2:v=0:a=1[au]" \
 -map "[v]" -map "[au]" -c:v libx264 -crf 15 -pix_fmt yuv420p -c:a aac -b:a 256k punched-ext.mp4

# 2. cutouts, only where something sits behind him: the hook type (0-4.85) and the cards (9.9-16.4)
ffmpeg -v error -y -i punched-ext.mp4 -t 4.85 -an -c:v libx264 -crf 14 seg-a.mp4
ffmpeg -v error -y -ss 9.9 -i punched-ext.mp4 -t 6.5 -an -c:v libx264 -crf 14 seg-b.mp4
# if the first run fails installing onnxruntime-node (its GPU download is blocked here), install it once with:
#   npm install onnxruntime-node@1.21.1 --prefix ~/.cache/hyperframes/optional/onnxruntime-node@1.21.1 --onnxruntime-node-install-cuda=skip
(cd "$ROOT" && npx hyperframes remove-background videos/rate-buydown/seg-a.mp4 -o videos/rate-buydown/cutout-a.mov && npx hyperframes remove-background videos/rate-buydown/seg-b.mp4 -o videos/rate-buydown/cutout-b.mov)

# 3. graphics layers
$R "$G/type.html#bg" type-bg.mov --alpha --duration 9.9
$R "$G/type.html#fg" type-fg.mov --alpha --duration 9.9
$R "$G/remix.html#bg" remix-bg.mov --alpha --duration 16.6
$R "$G/remix.html#fg" remix-fg.mov --alpha --duration $DUR
$R "$G/cash.html#t0=30.1" cash.mov --alpha --duration 1.65
python3 "$ROOT/src/music/chalk.py" sfx-remix.wav "$G/sfx-remix.json" --dur $DUR

# 4. composite. The corner circle is his face from the same footage, masked round, only while the paper is up.
D=$((CR*2))
ffmpeg -v error -y -i punched-ext.mp4 -i type-bg.mov -i cutout-a.mov -i type-fg.mov -i remix-bg.mov -itsoffset 9.9 -i cutout-b.mov -i remix-fg.mov -itsoffset 30.1 -i cash.mov -i sfx-remix.wav -filter_complex "\
[0:v]split[base][f];\
[f]crop=740:740:70:880,scale=$D:$D,format=yuva420p,geq=lum='lum(X,Y)':cb='cb(X,Y)':cr='cr(X,Y)':a='255*lte(hypot(X-$CR,Y-$CR),$CR)'[circ];\
[base][1:v]overlay=eof_action=pass[a];\
[a][2:v]overlay=eof_action=pass:enable='lt(t,4.80)'[b];\
[b][3:v]overlay=eof_action=pass[c];\
[c][4:v]overlay=eof_action=pass:enable='gte(t,9.9)'[d];\
[d][5:v]overlay=eof_action=pass:enable='between(t,9.9,16.38)'[e];\
[e][6:v]overlay=eof_action=pass[g];\
[g][circ]overlay=$((CX-CR)):$((CY-CR)):enable='between(t,$PIN+0.42,$POUT+0.02)'[h];\
[h][7:v]overlay=eof_action=pass:enable='gte(t,30.1)',format=yuv420p[v];\
[0:a]aformat=sample_rates=48000:channel_layouts=stereo[vo];[8:a]volume=$SFX[fx];\
[vo][fx]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[au]" \
 -map "[v]" -map "[au]" -t $DUR -c:v libx264 -crf 17 -preset medium -r 30 -movflags +faststart -c:a aac -b:a 192k final-remix.mp4
echo done
