# Asher dreams (2026-11-04, round three). The Nanit crib-cam screen recording cut into baby segments only; the dream
# shots (images) are cut in by the comp, so this base is just the footage legs with the chrome cropped, a punch-in per
# leg centred on him, blurred feed behind the 1080x784 window at y=700, giggles normalised. Legs and gaps:
#   L1 0.9-4.3   hook + giggles 1,2        (out 0.0-3.4)
#   gap 1.4 s    dream 1                    (out 3.4-4.8)
#   L2 5.4-7.7   giggle 3 + roll over       (out 4.8-7.1)
#   gap 1.4 s    dream 2                    (out 7.1-8.5)
#   L3 10.3-12.3 giggle 4                   (out 8.5-10.5)
#   gap 1.4 s    dream 3                    (out 10.5-11.9)
#   L4 14.4-17.9 giggle 5, tightest         (out 11.9-15.4)
#   tail 3.0 s   Maverick punchline + question (out 15.4-18.4), silent
# The gaps are black (silent) in the base; the comp paints the dream shots over them.
# usage: mkdir -p videos/asher-dreams/build && bash graphics/asher-dreams/cut.sh <screen-recording.mov>
set -e
IN=${1:-videos/asher-dreams/source.mov}
B=videos/asher-dreams/build
ffmpeg -v error -y -ss 0.5 -i $IN -frames:v 1 -vf "crop=1288:936:0:192,scale=2640:1920,crop=1080:1920,gblur=sigma=45,eq=brightness=-0.25:saturation=0.8" $B/bg.png
leg() { # idx start end z0 z1 fx fy
  D=$(python3 -c "print($3-$2)")
  ffmpeg -v error -y -ss $2 -to $3 -i $IN -filter_complex "
    [0:v]setpts=PTS-STARTPTS,crop=1288:936:0:192,scale=w='trunc(1080*($4+($5-$4)*t/$D)/2)*2':h=-2:eval=frame,crop=1080:784:x='clip(iw*$6-540,0,iw-1080)':y='clip(ih*$7-392,0,ih-784)',fps=30,format=yuv420p[v];
    [0:a]asetpts=PTS-STARTPTS[a]" -map "[v]" -map "[a]" -c:v libx264 -preset fast -crf 16 -c:a aac -b:a 192k $B/leg$1.mp4
}
gap() { ffmpeg -v error -y -f lavfi -i "color=c=black:s=1080x784:r=30:d=$2" -f lavfi -i "anullsrc=r=48000:cl=stereo" -t $2 -c:v libx264 -preset fast -crf 16 -c:a aac $B/gap$1.mp4; }
leg 1 0.9 4.3 1.00 1.12 0.62 0.53
leg 2 5.4 7.7 1.45 1.60 0.67 0.49
leg 3 10.3 12.3 1.95 2.10 0.72 0.455
leg 4 14.4 17.9 2.30 2.50 0.72 0.455
gap 1 1.4; gap 2 1.4; gap 3 1.4; gap 4 3.0
ffmpeg -v error -y -i $B/leg1.mp4 -i $B/gap1.mp4 -i $B/leg2.mp4 -i $B/gap2.mp4 -i $B/leg3.mp4 -i $B/gap3.mp4 -i $B/leg4.mp4 -i $B/gap4.mp4 -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a][3:v][3:a][4:v][4:a][5:v][5:a][6:v][6:a][7:v][7:a]concat=n=8:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -preset fast -crf 16 -c:a aac -b:a 192k $B/window.mp4
ffmpeg -v error -y -loop 1 -i $B/bg.png -i $B/window.mp4 -filter_complex "
  [0:v]scale=1080:1920[bg];[bg][1:v]overlay=0:700:shortest=1,format=yuv420p[v];
  [1:a]volume=14dB,alimiter=limit=0.9,loudnorm=I=-14:TP=-1.5:LRA=11[a]" -map "[v]" -map "[a]" -t 18.4 -r 30 -c:v libx264 -preset fast -crf 16 -c:a aac -b:a 192k videos/asher-dreams/base.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 videos/asher-dreams/base.mp4
