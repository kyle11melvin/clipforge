# Cuts the Nanit crib-cam screen recording (1288x1128, app chrome at the top) into a 14 s 1080x1920 base: the giggle
# bursts back to back, a punch-in per cut centred on the baby, a blurred feed behind the 1080x784 crib window at y=700,
# audio normalised. Then: node src/graphics/render.mjs graphics/mav-sleep-laugh/comp.html videos/mav-sleep-laugh/text.mov
# --alpha --duration 14, and overlay text.mov on base.mp4 with ffmpeg (see docs/log/2026-11-04-mav-sleep-laugh.md).
# usage: mkdir -p videos/mav-sleep-laugh/build && bash graphics/mav-sleep-laugh/cut.sh <screen-recording.mov>
set -e
IN=${1:-videos/mav-sleep-laugh/source.mov}   # the Nanit screen recording (gitignored)
ffmpeg -v error -y -ss 0.5 -i $IN -frames:v 1 -vf "crop=1288:936:0:192,scale=2640:1920,crop=1080:1920,gblur=sigma=45,eq=brightness=-0.25:saturation=0.8" videos/mav-sleep-laugh/build/bg.png
seg() { # idx start end z0 z1 fx fy
  D=$(python3 -c "print($3-$2)")
  ffmpeg -v error -y -ss $2 -to $3 -i $IN -filter_complex "
    [0:v]setpts=PTS-STARTPTS,crop=1288:936:0:192,scale=w='trunc(1080*($4+($5-$4)*t/$D)/2)*2':h=-2:eval=frame,crop=1080:784:x='clip(iw*$6-540,0,iw-1080)':y='clip(ih*$7-392,0,ih-784)',fps=30,format=yuv420p[v];
    [0:a]asetpts=PTS-STARTPTS[a]" -map "[v]" -map "[a]" -c:v libx264 -preset fast -crf 16 -c:a aac -b:a 192k videos/mav-sleep-laugh/build/seg$1.mp4
}
seg 1 0.9 4.3 1.00 1.12 0.62 0.53
seg 2 5.4 7.7 1.45 1.60 0.67 0.49
seg 3 10.2 12.3 1.95 2.10 0.72 0.455
seg 4 14.4 17.9 2.30 2.50 0.72 0.455
ffmpeg -v error -y -ss 17.85 -i $IN -frames:v 1 -vf "crop=1288:936:0:192" videos/mav-sleep-laugh/build/last.png
ffmpeg -v error -y -loop 1 -i videos/mav-sleep-laugh/build/last.png -t 2.7 -filter_complex "
  [0:v]scale=w='trunc(1080*(2.50+0.15*t/2.7)/2)*2':h=-2:eval=frame,crop=1080:784:x='clip(iw*0.72-540,0,iw-1080)':y='clip(ih*0.455-392,0,ih-784)',fps=30,format=yuv420p[v];
  anullsrc=r=48000:cl=stereo[a]" -map "[v]" -map "[a]" -t 2.7 -c:v libx264 -preset fast -crf 16 -c:a aac videos/mav-sleep-laugh/build/seg5.mp4
ffmpeg -v error -y -i videos/mav-sleep-laugh/build/seg1.mp4 -i videos/mav-sleep-laugh/build/seg2.mp4 -i videos/mav-sleep-laugh/build/seg3.mp4 -i videos/mav-sleep-laugh/build/seg4.mp4 -i videos/mav-sleep-laugh/build/seg5.mp4 -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a][3:v][3:a][4:v][4:a]concat=n=5:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -preset fast -crf 16 -c:a aac -b:a 192k videos/mav-sleep-laugh/build/window.mp4
ffmpeg -v error -y -loop 1 -i videos/mav-sleep-laugh/build/bg.png -i videos/mav-sleep-laugh/build/window.mp4 -filter_complex "
  [0:v]scale=1080:1920[bg];[bg][1:v]overlay=0:700:shortest=1,format=yuv420p[v];
  [1:a]volume=14dB,alimiter=limit=0.9,loudnorm=I=-14:TP=-1.5:LRA=11[a]" -map "[v]" -map "[a]" -t 14 -r 30 -c:v libx264 -preset fast -crf 16 -c:a aac -b:a 192k videos/mav-sleep-laugh/build/base.mp4
