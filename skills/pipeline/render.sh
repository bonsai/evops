#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${1:-artifacts/paper-animation}"
mkdir -p "$OUT_DIR" work/paper-animation

command -v rsvg-convert >/dev/null
command -v ffmpeg >/dev/null

for svg in papers/youtube/comics/P*.svg; do
  id="$(basename "$svg" .svg)"
  png="work/paper-animation/$id.png"
  mp4="$OUT_DIR/$id.mp4"

  rsvg-convert -w 2400 -h 1520 "$svg" -o "$png"

  ffmpeg -y -loglevel error -loop 1 -i "$png" \
    -filter_complex "
      [0:v]split=4[p1][p2][p3][p4];
      [p1]crop=1040:460:110:330,scale=1280:566,pad=1280:720:0:77,zoompan=z='min(zoom+0.0015,1.05)':x='iw*0.02':y='ih*0.01':d=75:s=1280x720:fps=25[v1];
      [p2]crop=1040:460:1220:330,scale=1280:566,pad=1280:720:0:77,zoompan=z='min(zoom+0.0015,1.05)':x='iw*0.02':y='ih*0.01':d=75:s=1280x720:fps=25[v2];
      [p3]crop=1040:460:110:870,scale=1280:566,pad=1280x720:0:77,zoompan=z='min(zoom+0.0015,1.05)':x='iw*0.02':y='ih*0.01':d=75:s=1280x720:fps=25[v3];
      [p4]crop=1040:460:1220:870,scale=1280:566,pad=1280x720:0:77,zoompan=z='min(zoom+0.0015,1.05)':x='iw*0.02':y='ih*0.01':d=75:s=1280x720:fps=25[v4];
      [v1][v2][v3][v4]concat=n=4:v=1:a=0,format=yuv420p[outv]
    " -map "[outv]" -t 12 -r 25 -c:v libx264 -preset veryfast -crf 20 -movflags +faststart "$mp4"
done

printf 'Rendered %s episodes into %s\n' "$(find "$OUT_DIR" -name 'P*.mp4' | wc -l)" "$OUT_DIR"
