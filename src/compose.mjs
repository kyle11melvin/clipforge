/**
 * Write the HyperFrames composition: the cut video full-frame, captions timed to speech,
 * an optional hook title at the top for the first seconds, and an optional lower-third.
 * Everything is driven by data-start/data-duration so the renderer seeks it deterministically.
 */
export function composition({ width, height, fps, duration, videoSrc, captions, hook, lower, style = {} }) {
  const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  const d = (n) => Math.round(n * 1000) / 1000;
  const accent = style.accent ?? "#ffd400";
  const captionSize = Math.round(width * (style.captionScale ?? 0.064));
  const captionBottom = Math.round(height * (style.captionFromBottom ?? 0.30));

  const capEls = captions.map((c, i) =>
    `  <div id="cap-${i + 1}" class="clip cap" data-start="${d(c.start)}" data-duration="${d(c.end - c.start)}" data-track-index="1">${esc(c.text)}</div>`
  ).join("\n");

  const hookEl = hook
    ? `  <div id="hook" class="clip hook" data-start="0" data-duration="${d(Math.min(3, duration))}" data-track-index="2">${esc(hook)}</div>`
    : "";

  const lowerEl = lower
    ? `  <div id="lower" class="clip lower" data-start="${d(Math.min(0.8, duration))}" data-duration="${d(Math.min(5, duration - 0.8))}" data-track-index="3">
    <div class="lower-name">${esc(lower.name)}</div>${lower.tagline ? `\n    <div class="lower-tag">${esc(lower.tagline)}</div>` : ""}
  </div>`
    : "";

  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>clipforge</title>
<style>
  @font-face { font-family: "Inter"; font-weight: 400; src: url("assets/fonts/Inter-400-latin.woff2") format("woff2"); }
  @font-face { font-family: "Inter"; font-weight: 700; src: url("assets/fonts/Inter-700-latin.woff2") format("woff2"); }
  html, body { margin: 0; background: #000; }
  #stage { position: relative; width: ${width}px; height: ${height}px; overflow: hidden; background: #000; font-family: "Inter", system-ui, sans-serif; }
  #main-video { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }

  .cap {
    position: absolute; left: ${Math.round(width * 0.06)}px; right: ${Math.round(width * 0.06)}px; bottom: ${captionBottom}px;
    text-align: center; font-weight: 700; font-size: ${captionSize}px; line-height: 1.12;
    color: #fff; text-transform: uppercase; letter-spacing: 0.01em;
    text-shadow: 0 2px 0 rgba(0,0,0,.9), 0 0 18px rgba(0,0,0,.85), 0 6px 28px rgba(0,0,0,.6);
    -webkit-text-stroke: ${Math.max(1, Math.round(captionSize * 0.02))}px rgba(0,0,0,.55);
    animation-name: cap-pop; animation-duration: 160ms; animation-timing-function: cubic-bezier(.2,.9,.3,1.2);
    animation-iteration-count: 1; animation-fill-mode: both;
  }
  @keyframes cap-pop { from { opacity: 0; transform: translateY(14px) scale(.94); } to { opacity: 1; transform: none; } }

  .hook {
    position: absolute; left: ${Math.round(width * 0.07)}px; right: ${Math.round(width * 0.07)}px; top: ${Math.round(height * 0.11)}px;
    text-align: center; font-weight: 700; font-size: ${Math.round(width * 0.075)}px; line-height: 1.1; color: #fff;
    text-shadow: 0 2px 0 rgba(0,0,0,.9), 0 0 22px rgba(0,0,0,.8);
    animation-name: hook-in; animation-duration: 320ms; animation-timing-function: cubic-bezier(.2,.9,.3,1);
    animation-iteration-count: 1; animation-fill-mode: both;
  }
  .hook::after { content: ""; display: block; width: ${Math.round(width * 0.14)}px; height: 8px; margin: 18px auto 0; background: ${accent}; border-radius: 4px; }
  @keyframes hook-in { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: none; } }

  .lower {
    position: absolute; left: ${Math.round(width * 0.06)}px; bottom: ${Math.round(height * 0.16)}px;
    padding: 14px 22px 16px; background: rgba(0,0,0,.72); border-left: 8px solid ${accent}; border-radius: 6px;
    animation-name: lower-in; animation-duration: 360ms; animation-timing-function: cubic-bezier(.2,.9,.3,1);
    animation-iteration-count: 1; animation-fill-mode: both;
  }
  .lower-name { font-weight: 700; font-size: ${Math.round(width * 0.04)}px; color: #fff; line-height: 1.15; }
  .lower-tag { font-weight: 400; font-size: ${Math.round(width * 0.028)}px; color: #ddd; margin-top: 4px; }
  @keyframes lower-in { from { opacity: 0; transform: translateX(-30px); } to { opacity: 1; transform: none; } }
</style>
</head>
<body>
<div id="stage" data-composition-id="main" data-start="0" data-duration="${d(duration)}" data-width="${width}" data-height="${height}" data-fps="${fps}" data-no-timeline>
  <video id="main-video" class="clip" data-start="0" data-duration="${d(duration)}" data-track-index="0" data-has-audio="true" src="${esc(videoSrc)}" playsinline></video>
${capEls}
${hookEl}
${lowerEl}
</div>
</body>
</html>
`;
}
