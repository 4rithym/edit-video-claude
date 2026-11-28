import React from "react";
import { Audio, Sequence, spring, staticFile, useCurrentFrame, interpolate, Easing } from "remotion";
import noir from "../cues_noir.json";
import swiss from "../cues_swiss.json";
import kinetic from "../cues_kinetic.json";
import terminal from "../cues_terminal.json";
import soft from "../cues_soft.json";

export const FPS = 30;
export const DURATION = 60 * FPS;
export type Style = "noir" | "swiss" | "kinetic" | "terminal" | "soft";
export type Word = { w: string; s: number; e: number };
export type Line = { cue: string; t: number; d: number; text: string; words: Word[] };
export type Data = { cues: Record<string, number>; lines: Line[] };
export const DATA: Record<Style, Data> = { noir, swiss, kinetic, terminal, soft } as unknown as Record<Style, Data>;
export const KEYS = ["A", "B", "C", "D", "E", "F", "G"] as const;
export type Key = (typeof KEYS)[number];
export const sceneEnd = (c: Record<string, number>, k: Key) => {
  const i = KEYS.indexOf(k);
  return i + 1 < KEYS.length ? c[KEYS[i + 1]] : 60;
};
export const FILE_NAME = "20261127134525.CC28C3AC.zip";
export const SANS = "'Inter Display', sans-serif";
export const MONO = "'JetBrains Mono', monospace";

/** spring starting at `at` seconds (local to current Sequence) */
export const sp = (f: number, at: number, damping = 200, dur?: number) =>
  spring({ frame: f - at * FPS, fps: FPS, config: { damping, mass: 0.9 }, durationInFrames: dur });
/** eased 0..1 ramp between a and b seconds */
export const ramp = (t: number, a: number, b: number, ease = Easing.inOut(Easing.cubic)) =>
  interpolate(t, [a, b], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });

export type SceneProps = { c: Record<string, number>; t0: number; dur: number };
/** local time (s) inside a scene + helper to get cue time relative to the scene */
export const useLocal = (p: SceneProps) => {
  const f = useCurrentFrame();
  return { f, t: f / FPS, r: (cue: string) => p.c[cue] - p.t0 };
};

export const Scenes: React.FC<{ data: Data; map: Record<Key, React.FC<SceneProps>>; shell?: React.FC<{ dur: number; k: Key; children: React.ReactNode }> }> = ({ data, map, shell: Shell }) => (
  <>
    {KEYS.map((k) => {
      const t0 = data.cues[k];
      const dur = sceneEnd(data.cues, k) - t0;
      const Comp = map[k];
      const inner = <Comp c={data.cues} t0={t0} dur={dur} />;
      return (
        <Sequence key={k} from={Math.round(t0 * FPS)} durationInFrames={Math.round(dur * FPS)} name={`Scene ${k}`}>
          {Shell ? <Shell dur={dur} k={k}>{inner}</Shell> : inner}
        </Sequence>
      );
    })}
  </>
);

/* ---------- caption chunks ---------- */
export type Chunk = { st: number; en: number; words: Word[] };
export const makeChunks = (lines: Line[], maxWords = 5, gap = 0.3, skip: string[] = []): Chunk[] => {
  const out: Chunk[] = [];
  for (const l of lines) {
    if (skip.includes(l.cue)) continue;
    const groups: Word[][] = [];
    let cur: Word[] = [];
    for (const w of l.words) {
      if (cur.length && (cur.length >= maxWords || w.s - cur[cur.length - 1].e > gap)) { groups.push(cur); cur = []; }
      cur.push(w);
    }
    if (cur.length) groups.push(cur);
    groups.forEach((g, i) => out.push({ st: g[0].s - 0.04, en: i + 1 < groups.length ? groups[i + 1][0].s - 0.04 : g[g.length - 1].e + 0.3, words: g }));
  }
  return out;
};

export type CapStyle = { top: number; size: number; font?: string; weight?: number; said: string; unsaid: string; activeBg: string; activeColor: string; radius?: number; upper?: boolean; plate?: string; };
export const Captions: React.FC<{ data: Data; s: CapStyle; until?: number }> = ({ data, s, until = 60 }) => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const chunks = React.useMemo(() => makeChunks(data.lines, 5, 0.3, ["g1"]), [data]);
  if (t >= until) return null;
  const ch = chunks.find((c) => t >= c.st && t < c.en);
  return (
    <>
      {s.plate && <div style={{ position: "absolute", left: 0, top: s.top - 110, width: 1080, height: 1920 - s.top + 110, background: s.plate }} />}
      {ch && (
        <div style={{ position: "absolute", left: 80, width: 920, top: s.top, display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "6px 2px",
          opacity: sp(f, ch.st, 200, 6), transform: `translateY(${(1 - sp(f, ch.st, 200, 8)) * 14}px)` }}>
          {ch.words.map((w, i) => {
            const active = t >= w.s && t < Math.max(w.e, w.s + 0.12);
            return (
              <span key={i} style={{ fontFamily: s.font ?? SANS, fontWeight: s.weight ?? 700, fontSize: s.size, letterSpacing: "-0.01em", padding: "4px 12px", borderRadius: s.radius ?? 12,
                textTransform: s.upper ? "uppercase" : undefined, color: active ? s.activeColor : t >= w.s ? s.said : s.unsaid, background: active ? s.activeBg : "transparent" }}>
                {w.w}
              </span>
            );
          })}
        </div>
      )}
    </>
  );
};

/* ---------- sound ---------- */
export const Sound: React.FC<{ style: Style; data: Data; music?: number; sfx?: [string, string | number, number][] }> = ({ style, data, music = 0.2, sfx = [] }) => (
  <>
    <Audio src={staticFile(`v6/${style}/vo.wav`)} />
    <Audio src={staticFile(`v6/${style}/music.wav`)} volume={music} />
    {sfx.map(([n, at, v], i) => {
      const t = typeof at === "number" ? at : data.cues[at];
      return (
        <Sequence key={i} from={Math.max(0, Math.round(t * FPS))} durationInFrames={45} name={`sfx-${n}`}>
          <Audio src={staticFile(`${n}.wav`)} volume={v} />
        </Sequence>
      );
    })}
  </>
);
/** standard SFX map: whoosh at each scene change + clicks on list cues */
export const stdSfx = (data: Data, whoosh = 0.14, click = 0.11): [string, string | number, number][] => [
  ...(["B", "C", "D", "E", "F", "G"] as Key[]).map((k) => ["whoosh", data.cues[k] - 0.2, whoosh] as [string, number, number]),
  ...["c1", "c2", "c3", "d1", "d2", "d3", "e1", "e2", "e3", "e4"].map((c) => ["click", c, click] as [string, string, number]),
];
