#!/bin/bash
# Assemble the rate-buydown reel: hook → Clip A (captioned) → chalkboard with Kyle in a PiP over Clip B+C → CTA.
# Cross-fades of 0.25 s at every join. Board = cut.mp4 4.81 s to the end (+0.85 s hold on the last frame).
set -e
cd "$(dirname "$0")"
A_END=4.81; BC_LEN=$(python3 -c "print(30.757-4.81)")
HOLD=0.85; XF=0.25
# clip A with captions, silent-padded audio format
ffmpeg -v error -y -i final.mp4 -t $A_END -af "aformat=sample_rates=48000:channel_layouts=stereo" -c:v libx264 -crf 16 -preset fast -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k segA.mp4
# board + PiP (square crop of the footage around his head, rounded corners), audio from the cut
ffmpeg -v error -y -i board.mp4 -ss $A_END -i cut.mp4 -i pip-mask.png -filter_complex "\
[1:v]crop=1080:1080:0:560,scale=400:400,tpad=stop_mode=clone:stop_duration=$HOLD[pv];\
[2:v]format=gray,loop=loop=-1:size=1[m];[pv][m]alphamerge[pa];\
[0:v][pa]overlay=64:1472:shortest=1,format=yuv420p[v];\
[1:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=pad_dur=$HOLD[a]" \
 -map "[v]" -map "[a]" -t 26.8 -c:v libx264 -crf 16 -preset fast -r 30 -c:a aac -b:a 192k segBC.mp4
# silent audio on the graphics
for s in hook cta; do ffmpeg -v error -y -i $s.mp4 -f lavfi -i anullsrc=r=48000:cl=stereo -shortest -c:v copy -c:a aac -b:a 192k seg-$s.mp4; done
D0=2.6; D1=$A_END; D2=26.8
O1=$(python3 -c "print($D0-$XF)"); O2=$(python3 -c "print($O1+$D1-$XF)"); O3=$(python3 -c "print($O2+$D2-$XF)")
ffmpeg -v error -y -i seg-hook.mp4 -i segA.mp4 -i segBC.mp4 -i seg-cta.mp4 -filter_complex "\
[0:v][1:v]xfade=transition=fade:duration=$XF:offset=$O1[v1];[v1][2:v]xfade=transition=fade:duration=$XF:offset=$O2[v2];[v2][3:v]xfade=transition=fade:duration=$XF:offset=$O3[v];\
[0:a][1:a]acrossfade=d=$XF[a1];[a1][2:a]acrossfade=d=$XF[a2];[a2][3:a]acrossfade=d=$XF[a]" \
 -map "[v]" -map "[a]" -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 192k final-reel.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 final-reel.mp4
