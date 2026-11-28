import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import { DATA, FILE_NAME, FPS, KEYS, MONO, SANS, Sound, sp, Word, Key } from "./shared";

const D = DATA.kinetic;
const KEYWORDS = new Set(["spreading", "whatsapp", "don't", "hijacked", "harith's", "zip", "four", "finance", "strange", "trust", "infected", "taken", "spreads", "protect", "unexpected", "call",
  "two-step", "linked", "disconnect", "scan", "cyber999", "share", "love", "everyone", "again", "confirm"]);
const THEME: Record<Key, { bg: string; fg: string; key: string }> = {
  A: { bg: "#0A0A0A", fg: "#FFFFFF", key: "#FF3B3B" },
  B: { bg: "#E8261C", fg: "#FFFFFF", key: "#111111" },
  C: { bg: "#0A0A0A", fg: "#FFFFFF", key: "#FFD23F" },
  D: { bg: "#111111", fg: "#FFFFFF", key: "#FF3B3B" },
  E: { bg: "#F4F1EA", fg: "#111111", key: "#13A35A" },
  F: { bg: "#0A0A0A", fg: "#FFFFFF", key: "#FFD23F" },
  G: { bg: "#FFD23F", fg: "#111111", key: "#E8261C" },
};
type Group = { st: number; en: number; words: Word[]; scene: Key; i: number };
const GROUPS: Group[] = (() => {
  const out: Group[] = [];
  let n = 0;
  for (const l of D.lines) {
    const scene = KEYS.filter((k) => l.t >= D.cues[k] - 0.01).slice(-1)[0] as Key;
    let cur: Word[] = [];
    const gs: Word[][] = [];
    for (const w of l.words) {
      if (cur.length && (cur.length >= 3 || w.s - cur[cur.length - 1].e > 0.22 || /[.,?]$/.test(cur[cur.length - 1].w))) { gs.push(cur); cur = []; }
      cur.push(w);
    }
    if (cur.length) gs.push(cur);
    gs.forEach((g, i) => out.push({ st: g[0].s - 0.03, en: i + 1 < gs.length ? gs[i + 1][0].s - 0.03 : g[g.length - 1].e + 0.35, words: g, scene, i: n++ }));
  }
  return out;
})();

const clean = (w: string) => w.toLowerCase().replace(/[.,?!]/g, "");

const Stage: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const scene = (KEYS.filter((k) => t >= D.cues[k]).slice(-1)[0] ?? "A") as Key;
  const th = THEME[scene];
  const g = GROUPS.find((x) => t >= x.st && t < x.en);
  // background wipe at scene change
  const sStart = D.cues[scene];
  const prev = KEYS[Math.max(0, KEYS.indexOf(scene) - 1)];
  const wipe = scene === "A" ? 1 : interpolate(t, [sStart - 0.05, sStart + 0.3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const layout = g ? g.i % 4 : 0;
  return (
    <AbsoluteFill style={{ background: THEME[prev].bg }}>
      <div style={{ position: "absolute", left: 0, top: 0, width: 1080, height: 1920, background: th.bg, clipPath: `circle(${wipe * 130}% at 50% 50%)` }} />
      {g && (
        <div style={{ position: "absolute", left: 70, right: 70, top: 0, bottom: 0, display: "flex", flexDirection: "column", justifyContent: "center",
          alignItems: layout === 1 ? "flex-start" : layout === 3 ? "flex-end" : "center", transform: `scale(${1 + (t - g.st) * 0.025})` }}>
          {g.words.map((w, i) => {
            const c = clean(w.w);
            const isKey = KEYWORDS.has(c);
            const len = Math.max(3, w.w.length);
            const size = Math.min(isKey ? 250 : 200, Math.floor(1420 / len));
            const q = sp(f, w.s - 0.02, 13, 14);
            const rot = (i % 2 ? 1 : -1) * (layout === 2 ? 3 : 0);
            return (
              <div key={i} style={{ fontFamily: SANS, fontWeight: 900, fontSize: size, lineHeight: 0.92, letterSpacing: "-0.05em", textTransform: "uppercase",
                color: isKey ? th.key : th.fg, opacity: t >= w.s - 0.02 ? 1 : 0.0, transform: `translateY(${(1 - q) * 60}px) scale(${0.7 + 0.3 * q}) rotate(${rot}deg)`,
                filter: `blur(${(1 - q) * 6}px)`, whiteSpace: "nowrap" }}>
                {w.w.replace(/[,]/g, "")}
              </div>
            );
          })}
        </div>
      )}
      {/* scene accents */}
      {scene === "A" && t > D.cues.a1 + 1.4 && (
        <div style={{ position: "absolute", left: 80, bottom: 220, width: 920, display: "flex", justifyContent: "center", opacity: sp(f, D.cues.a1 + 1.4) }}>
          <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 30, color: "#fff", border: "3px solid #FF3B3B", padding: "16px 24px", borderRadius: 14 }}>📎 {FILE_NAME}</div>
        </div>
      )}
      {scene === "B" && (
        <div style={{ position: "absolute", left: 80, top: 250, fontFamily: MONO, fontWeight: 700, fontSize: 44, color: "#111", opacity: sp(f, D.cues.B + 0.3) }}>27.11.2026 · 14:38</div>
      )}
      {scene === "F" && t > D.cues.f2 + 0.8 && (
        <div style={{ position: "absolute", left: 80, bottom: 260, width: 920, textAlign: "center", fontFamily: MONO, fontWeight: 700, fontSize: 64, color: "#FFD23F", opacity: sp(f, D.cues.f2 + 0.8) }}>
          1-300-88-2999
        </div>
      )}
      {scene === "G" && t > D.cues.g1 + 3 && (
        <div style={{ position: "absolute", left: 80, bottom: 300, width: 920, textAlign: "center", fontFamily: MONO, fontWeight: 700, fontSize: 46, color: "#111", opacity: sp(f, D.cues.g1 + 3) }}>#DONTOPENTHEZIP</div>
      )}
      {/* corner furniture */}
      <div style={{ position: "absolute", left: 80, top: 90, right: 80, display: "flex", justifyContent: "space-between", fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: "0.14em", color: th.fg, opacity: 0.75 }}>
        <span>⚠ SECURITY ALERT</span>
        <span>00:{String(Math.floor(t)).padStart(2, "0")}</span>
      </div>
      <div style={{ position: "absolute", left: 80, bottom: 100, width: 920, height: 6, background: th.fg, opacity: 0.18 }} />
      <div style={{ position: "absolute", left: 80, bottom: 100, width: 920 * (t / 60), height: 6, background: th.key }} />
    </AbsoluteFill>
  );
};

export const V3Kinetic: React.FC = () => (
  <AbsoluteFill>
    <Stage />
    <Sound style="kinetic" data={D} music={0.22} sfx={[...KEYS.slice(1).map((k) => ["whoosh", D.cues[k] - 0.15, 0.18] as [string, number, number]), ["pop", "a2", 0.2], ["ding", "g1", 0.14]]} />
  </AbsoluteFill>
);
