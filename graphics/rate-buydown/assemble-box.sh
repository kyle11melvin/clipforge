#!/bin/bash
# Round two of the rate-buydown reel (2026-11-11): Kyle full screen the whole time, the chalkboard as a box above
# his head from 9.5 s ("half a percent"), no CTA slide, ends on "keep the cash". Run from videos/rate-buydown/.
#   hook.mp4 (2.6 s) → final.mp4 (captions until the board arrives) with a 7% punch-in anchored at the top as the box
#   rises (so his hair clears the box) + board-box.mov overlaid at (64,246) from 9.4 s. 0.25 s cross-fade off the hook.
#   Writes final-reel-v2.mp4 (voice only) and final-reel-v2-music.mp4 (bed.wav from src/music/underbed.py under it).
set -e
cd "$(dirname "$0")/../../videos/rate-buydown"
XF=0.25; HOOK=2.6; OFF=$(python3 -c "print($HOOK-$XF)"); T0=9.4
Z="1+0.07*(1-pow(1-min(1,max(0,(on/30-9.5)/0.4)),2))"
ffmpeg -v error -y -i hook.mp4 -i final.mp4 -i board-box.mov -filter_complex "\
[1:v]scale=2160:3840:flags=bicubic,zoompan=z='$Z':x='iw/2-(iw/zoom/2)':y=0:d=1:s=1080x1920:fps=30,setsar=1[fz];\
[2:v]setpts=PTS+$T0/TB[bx];\
[fz][bx]overlay=64:246:eof_action=pass:enable='gte(t,$T0)',fps=30,format=yuv420p,settb=AVTB[fo];\
[0:v]fps=30,format=yuv420p,settb=AVTB[hk];\
[hk][fo]xfade=transition=fade:duration=$XF:offset=$OFF[v];\
[1:a]aformat=sample_rates=48000:channel_layouts=stereo,afade=t=in:d=0.08,adelay=$(python3 -c "print(int($OFF*1000))"):all=1[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 192k final-reel-v2.mp4
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 final-reel-v2.mp4)
# music: fuller on the silent hook (-8 dB), then down to -18 dB under his voice by the time he speaks
ffmpeg -v error -y -i final-reel-v2.mp4 -i bed.wav -filter_complex "\
[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume='if(lt(t,2.1),0.40,if(lt(t,2.8),0.40+(0.126-0.40)*(t-2.1)/0.7,0.126))':eval=frame[bed];\
[0:a][bed]amix=inputs=2:normalize=0:duration=longest,alimiter=limit=0.95[a]" \
 -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -t $DUR -movflags +faststart final-reel-v2-music.mp4
echo "$DUR"
