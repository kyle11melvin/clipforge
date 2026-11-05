import { probe } from "./ffmpeg.mjs";
import { run } from "./run.mjs";

/**
 * Reframe a vertical clip: punch in by `zoom` and slide the window down so empty sky above the
 * subject's head is cropped away. Output is a plain SDR 1080x1920 (or `width`x`height`) file,
 * audio copied through untouched. `top` is where the crop window starts, as a fraction of the
 * source height (0 = keep the top, 1 - 1/zoom = keep the bottom). `x` likewise for horizontal
 * (default 0.5 = centred).
 *
 * With `probe: [t1, t2, ...]` it writes a numbered strip of stills with the crop box drawn in gold
 * instead of a video, so Kyle can pick the framing from his phone.
 */
export async function reframe({ input, output, zoom = 1.3, top, x = 0.5, width = 1080, height = 1920, probe: times, fps }) {
  const info = await probe(input);
  // Make the stills tone-map and audio handling consistent with the cut step.
  const sw = info.width, sh = info.height;
  if (zoom < 1) throw new Error("zoom must be >= 1");
  // Crop window in source pixels at the target aspect.
  let cw = Math.round(sw / zoom), ch = Math.round(cw * height / width);
  if (ch > sh) { ch = sh; cw = Math.round(ch * width / height); }
  const maxTop = (sh - ch) / sh;
  const topFrac = top == null ? maxTop : Math.min(Math.max(top, 0), maxTop);
  const cy = Math.round(topFrac * sh), cx = Math.round((sw - cw) * Math.min(Math.max(x, 0), 1));
  const sdr = "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv";
  const tone = info.hdr ? `${sdr},` : "";
  const box = { cx, cy, cw, ch, sw, sh, zoom, top: +topFrac.toFixed(3) };

  if (times?.length) {
    // One still per time, the full source frame with the crop box drawn, numbered, tiled in a row.
    const cols = times.length;
    const args = ["-hide_banner", "-nostats", "-y"];
    const filters = [], labels = [];
    times.forEach((t, i) => {
      args.push("-ss", String(t), "-i", input);
      filters.push(`[${i}:v]${tone}scale=540:-2,drawbox=x=${Math.round(cx / 2)}:y=${Math.round(cy / 2)}:w=${Math.round(cw / 2)}:h=${Math.round(ch / 2)}:color=#C9A96A@1:t=6,` +
        `drawtext=text='${i + 1}':x=24:y=24:fontsize=72:fontcolor=white:borderw=6:bordercolor=black,` +
        `drawtext=text='${t}s':x=24:y=110:fontsize=36:fontcolor=white:borderw=4:bordercolor=black[s${i}]`);
      labels.push(`[s${i}]`);
    });
    filters.push(`${labels.join("")}xstack=inputs=${cols}:layout=${times.map((_, i) => `${i * 540}_0`).join("|")}[out]`);
    args.push("-filter_complex", filters.join(";"), "-map", "[out]", "-frames:v", "1", output);
    await run("ffmpeg", args);
    return box;
  }

  const args = ["-hide_banner", "-nostats", "-y", "-i", input,
    "-vf", `crop=${cw}:${ch}:${cx}:${cy},scale=${width}:${height}:flags=lanczos,${tone}${fps ? `fps=${fps},` : ""}format=yuv420p,setsar=1`,
    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", output];
  await run("ffmpeg", args);
  return box;
}
