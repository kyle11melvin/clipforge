/**
 * Group word-level transcript entries into short caption chunks.
 * Rules: max `maxWords` words, max `maxChars` characters, break on sentence punctuation,
 * and break when the speaker pauses longer than `gap` seconds.
 */
export function groupWords(words, { maxWords = 4, maxChars = 26, gap = 0.45, minShow = 0.5, hold = 0.35 } = {}) {
  const clean = words.map((w) => ({ text: String(w.text ?? "").trim(), start: w.start, end: w.end })).filter((w) => w.text);
  const endsSentence = (t) => /[.!?]$/.test(t);
  const groups = [];
  let cur = null;
  for (let i = 0; i < clean.length; i++) {
    const w = clean[i];
    if (cur) {
      const joined = cur.text + " " + w.text;
      const full = cur.words.length >= maxWords || joined.length > maxChars;
      // Let a sentence's final word ride along rather than flash alone for a few hundred ms.
      const lastOfSentence = endsSentence(w.text) && joined.length <= maxChars + 8 && cur.words.length < maxWords + 2;
      const breakHere =
        (full && !lastOfSentence) ||
        w.start - cur.end > gap ||
        endsSentence(cur.words[cur.words.length - 1]);
      if (!breakHere) { cur.words.push(w.text); cur.text = joined; cur.end = w.end; continue; }
    }
    cur = { words: [w.text], text: w.text, start: w.start, end: w.end };
    groups.push(cur);
  }
  // Hold each caption until the next one starts (up to `hold`), and never flash shorter than minShow.
  for (let i = 0; i < groups.length; i++) {
    const g = groups[i], next = groups[i + 1];
    const latest = next ? next.start : g.end + hold;
    g.end = Math.max(g.end + Math.min(hold, latest - g.end), Math.min(g.start + minShow, latest));
  }
  return groups.map(({ text, start, end }) => ({ text, start: round(start), end: round(end) }));
}

export function toSrt(groups) {
  const ts = (s) => {
    const ms = Math.round(s * 1000);
    const h = Math.floor(ms / 3600000), m = Math.floor((ms % 3600000) / 60000), sec = Math.floor((ms % 60000) / 1000), r = ms % 1000;
    return `${pad(h)}:${pad(m)}:${pad(sec)},${String(r).padStart(3, "0")}`;
  };
  return groups.map((g, i) => `${i + 1}\n${ts(g.start)} --> ${ts(g.end)}\n${g.text}\n`).join("\n");
}

const pad = (n) => String(n).padStart(2, "0");
const round = (n) => Math.round(n * 1000) / 1000;
