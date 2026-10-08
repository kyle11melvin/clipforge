import { run } from "./run.mjs";

const ASPECTS = { "9:16": [1080, 1920], "1:1": [1080, 1080], "4:5": [1080, 1350], "16:9": [1920, 1080] };

export function targetSize(aspect) {
  const size = ASPECTS[aspect];
  if (!size) throw new Error(`Unknown aspect "${aspect}". Use one of: ${Object.keys(ASPECTS).join(", ")}`);
  return { width: size[0], height: size[1] };
}

export async function probe(file) {
  const { stdout } = await run("ffprobe", ["-v", "error", "-print_format", "json", "-show_format", "-show_streams", file]);
  const info = JSON.parse(stdout);
  const v = info.streams.find((s) => s.codec_type === "video");
  const a = info.streams.find((s) => s.codec_type === "audio");
  if (!v) throw new Error(`${file}: no video stream`);
  const [num, den] = (v.r_frame_rate || "30/1").split("/").map(Number);
  const rotation = Number(v.side_data_list?.find((d) => d.rotation != null)?.rotation ?? v.tags?.rotate ?? 0);
  const rotated = Math.abs(rotation) % 180 === 90;
  return {
    file,
    duration: Number(info.format.duration),
    width: rotated ? v.height : v.width,
    height: rotated ? v.width : v.height,
    fps: den ? num / den : 30,
    hasAudio: Boolean(a),
  };
}

/**
 * Find stretches of silence with ffmpeg's silencedetect.
 * Returns [{start, end}] in seconds, clamped to the clip.
 */
export async function detectSilence(file, duration, { noiseDb = -35, minSilence = 0.5 } = {}) {
  const { stderr } = await run("ffmpeg", [
    "-hide_banner", "-nostats", "-i", file, "-vn",
    "-af", `silencedetect=noise=${noiseDb}dB:d=${minSilence}`,
    "-f", "null", "-",
  ]);
  const silences = [];
  let open = null;
  for (const line of stderr.split("\n")) {
    const s = line.match(/silence_start:\s*(-?[\d.]+)/);
    const e = line.match(/silence_end:\s*(-?[\d.]+)/);
    if (s) open = Math.max(0, Number(s[1]));
    if (e && open != null) { silences.push({ start: open, end: Math.min(duration, Number(e[1])) }); open = null; }
  }
  if (open != null) silences.push({ start: open, end: duration }); // silent to the end
  return silences;
}

/**
 * Turn silences into the segments to KEEP.
 * - leading/trailing dead air is cut down to `pad` seconds
 * - internal pauses are shortened to about 2*pad seconds
 * - speech islands shorter than minSpeech (a cough, a click) are dropped
 */
export function keepSegments(silences, duration, { pad = 0.18, minSpeech = 0.2 } = {}) {
  const speech = [];
  let cursor = 0;
  for (const s of silences) {
    if (s.start > cursor) speech.push({ start: cursor, end: s.start });
    cursor = Math.max(cursor, s.end);
  }
  if (cursor < duration) speech.push({ start: cursor, end: duration });

  const kept = [];
  for (const seg of speech) {
    if (seg.end - seg.start < minSpeech) continue;
    const start = Math.max(0, seg.start - pad);
    const end = Math.min(duration, seg.end + pad);
    const last = kept[kept.length - 1];
    if (last && start <= last.end) last.end = Math.max(last.end, end);
    else kept.push({ start, end });
  }
  // A clip that is entirely "silent" by the threshold (music, b-roll) is kept whole rather than dropped.
  return kept.length ? kept : [{ start: 0, end: duration }];
}

/**
 * Build one video from many clips and their keep-segments.
 * Every segment is scaled to the target frame (cover or contain), resampled to `fps`,
 * audio normalised to stereo 48k, then concatenated and loudness-normalised.
 */
export async function assemble({ clips, width, height, fps = 30, fit = "cover", output }) {
  const args = ["-hide_banner", "-nostats", "-y"];
  const filters = [];
  const labels = [];
  let silentInputs = 0;
  clips.forEach((clip) => { args.push("-i", clip.file); });
  // One shared silent source for clips with no audio track.
  const silentIndex = clips.length;
  if (clips.some((c) => !c.hasAudio)) { args.push("-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"); silentInputs = 1; }

  const scale = fit === "contain"
    ? `scale=${width}:${height}:force_original_aspect_ratio=decrease,pad=${width}:${height}:(ow-iw)/2:(oh-ih)/2:color=black`
    : `scale=${width}:${height}:force_original_aspect_ratio=increase,crop=${width}:${height}`;

  clips.forEach((clip, i) => {
    clip.segments.forEach((seg, j) => {
      const v = `v${i}_${j}`, a = `a${i}_${j}`;
      filters.push(`[${i}:v]trim=start=${seg.start}:end=${seg.end},setpts=PTS-STARTPTS,${scale},fps=${fps},format=yuv420p,setsar=1[${v}]`);
      if (clip.hasAudio) {
        filters.push(`[${i}:a]atrim=start=${seg.start}:end=${seg.end},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo[${a}]`);
      } else {
        filters.push(`[${silentIndex}:a]atrim=start=0:end=${seg.end - seg.start},asetpts=PTS-STARTPTS[${a}]`);
      }
      labels.push(`[${v}][${a}]`);
    });
  });
  filters.push(`${labels.join("")}concat=n=${labels.length}:v=1:a=1[vcat][acat]`);
  filters.push(`[acat]loudnorm=I=-16:TP=-1.5:LRA=11[aout]`);

  args.push(
    "-filter_complex", filters.join(";"),
    "-map", "[vcat]", "-map", "[aout]",
    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", String(fps),
    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
    output,
  );
  void silentInputs;
  await run("ffmpeg", args);
}
