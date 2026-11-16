#!/bin/bash
# Build the v2 family-growing reel (2026-11-13). Needs graphics/family-growing/photo.jpg (gitignored; Kyle's original).
#   videos/family-growing/v2-silent.mp4  for a picker song on the creator account (silent AAC track)
#   videos/family-growing/v2-warm.mp4    with the warm.py bed and two interface sounds (business account, Original audio)
set -e
cd "$(dirname "$0")/../.."
V=videos/family-growing; mkdir -p $V
node src/graphics/render.mjs graphics/family-growing/comp2.html $V/v2-picture.mp4 --duration 8.5
ffmpeg -v error -y -i $V/v2-picture.mp4 -f lavfi -i anullsrc=r=48000:cl=stereo -shortest -c:v libx264 -crf 17 -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart $V/v2-silent.mp4
python3 -I src/music/warm.py $V/bed.wav --dur 8.5 --swell 5.4
echo '[{"type":"whoosh","t":3.1,"d":0.35},{"type":"pop","t":3.88},{"type":"pop","t":6.65,"gain":0.8}]' > $V/sfx.json
python3 -I src/music/chalk.py $V/sfx.wav $V/sfx.json --dur 8.5
ffmpeg -v error -y -i $V/v2-picture.mp4 -i $V/bed.wav -i $V/sfx.wav -filter_complex "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,afade=t=out:st=7.9:d=0.6[b];[2:a]volume=0.4[f];[b][f]amix=inputs=2:normalize=0:duration=first[a]" \
  -map 0:v -map "[a]" -t 8.5 -c:v libx264 -crf 17 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart $V/v2-warm.mp4
echo done
