import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, Easing } from "remotion";
import { C, CHAPTERS, CUES, FILE_NAME, FPS, LINES, MONO, SANS, SCAM_MSG, sceneEnd, sp } from "./theme";

/* ---------------- Background: drifting glow, grid, grain, vignette ---------------- */
export const Background: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  return (
    <AbsoluteFill style={{ background: C.bg, overflow: "hidden" }}>
      <div style={{ position: "absolute", width: 1300, height: 1300, borderRadius: "50%", left: -420 + Math.sin(t * 0.21) * 140, top: -380 + Math.cos(t * 0.17) * 120,
        background: "radial-gradient(circle, rgba(255,77,87,0.22) 0%, rgba(255,77,87,0) 62%)" }} />
      <div style={{ position: "absolute", width: 1400, height: 1400, borderRadius: "50%", right: -560 + Math.cos(t * 0.15) * 140, bottom: -420 + Math.sin(t * 0.19) * 140,
        background: "radial-gradient(circle, rgba(70,90,255,0.16) 0%, rgba(70,90,255,0) 62%)" }} />
      <AbsoluteFill style={{
        backgroundImage: "linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px)",
        backgroundSize: "90px 90px", backgroundPosition: `0px ${-(t * 12) % 90}px`,
        maskImage: "radial-gradient(ellipse at 50% 40%, black 20%, transparent 75%)", WebkitMaskImage: "radial-gradient(ellipse at 50% 40%, black 20%, transparent 75%)" }} />
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0, opacity: 0.06, mixBlendMode: "overlay" }}>
        <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={f % 12} stitchTiles="stitch" /></filter>
        <rect width="100%" height="100%" filter="url(#grain)" />
      </svg>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 45%, transparent 45%, rgba(0,0,0,0.7) 100%)" }} />
    </AbsoluteFill>
  );
};

/* ---------------- Scene shell: enter / exit ---------------- */
export const SceneShell: React.FC<{ dur: number; children: React.ReactNode }> = ({ dur, children }) => {
  const f = useCurrentFrame();
  const inP = interpolate(f, [0, 0.55 * FPS], [0, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const outP = interpolate(f, [dur * FPS - 0.45 * FPS, dur * FPS], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.in(Easing.cubic) });
  return (
    <AbsoluteFill style={{ opacity: inP * (1 - outP), transform: `translateY(${(1 - inP) * 40 - outP * 50}px) scale(${1 - outP * 0.02})`, filter: `blur(${(1 - inP) * 10 + outP * 10}px)` }}>
      {children}
    </AbsoluteFill>
  );
};

/* ---------------- Word-staggered headline ---------------- */
export const Reveal: React.FC<{ text: string; at: number; size?: number; weight?: number; color?: string; accent?: string[]; style?: React.CSSProperties; stagger?: number }> = ({
  text, at, size = 76, weight = 800, color = C.text, accent = [], style, stagger = 0.06 }) => {
  const f = useCurrentFrame();
  return (
    <div style={{ fontFamily: SANS, fontWeight: weight, fontSize: size, lineHeight: 1.05, letterSpacing: "-0.03em", color, ...style }}>
      {text.split(" ").map((w, i) => {
        const p = sp(f, at + i * stagger);
        const isAcc = accent.includes(w.replace(/[.,!?]/g, ""));
        return (
          <span key={i} style={{ display: "inline-block", marginRight: "0.26em", opacity: p, transform: `translateY(${(1 - p) * 0.5}em)`, filter: `blur(${(1 - p) * 8}px)`, color: isAcc ? C.red : undefined }}>
            {w}
          </span>
        );
      })}
    </div>
  );
};

export const Kicker: React.FC<{ children: React.ReactNode; at: number; color?: string }> = ({ children, at, color = C.red }) => {
  const f = useCurrentFrame();
  const p = sp(f, at);
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 14, fontFamily: MONO, fontWeight: 700, fontSize: 26, letterSpacing: "0.18em", color, opacity: p, transform: `translateX(${(1 - p) * -30}px)` }}>
      {children}
    </div>
  );
};

export const Chapter: React.FC<{ num: string; title: string }> = ({ num, title }) => (
  <div style={{ position: "absolute", left: 80, top: 210, width: 920 }}>
    <Kicker at={0.1}>
      <span style={{ display: "inline-block", width: 40, height: 3, background: C.red }} />
      CHAPTER {num}
    </Kicker>
    <Reveal text={title} at={0.2} size={84} style={{ marginTop: 18 }} />
  </div>
);

/* ---------------- Header: alert pill, chapter counter, segmented progress ---------------- */
export const Header: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  if (t >= CUES.H) return null;
  const ci = CHAPTERS.findIndex((k) => t >= CUES[k] && t < sceneEnd(k));
  const enter = sp(f, 0.1);
  const pulse = 0.55 + 0.45 * Math.abs(Math.sin(t * 2.4));
  return (
    <div style={{ position: "absolute", left: 80, top: 76, width: 920, opacity: enter }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12, padding: "10px 20px", borderRadius: 999, background: C.redSoft, border: "1px solid rgba(255,77,87,0.35)",
          fontFamily: MONO, fontWeight: 700, fontSize: 22, letterSpacing: "0.16em", color: C.red }}>
          <span style={{ width: 12, height: 12, borderRadius: "50%", background: C.red, opacity: pulse, boxShadow: `0 0 ${12 * pulse}px ${C.red}` }} />
          SECURITY ALERT
        </div>
        <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: "0.1em", color: C.muted, opacity: ci >= 0 ? 1 : 0 }}>
          <span style={{ color: C.text }}>{String(Math.max(ci, 0) + 1).padStart(2, "0")}</span> / {String(CHAPTERS.length).padStart(2, "0")}
        </div>
      </div>
      <div style={{ display: "flex", gap: 8, marginTop: 22 }}>
        {CHAPTERS.map((k) => {
          const p = interpolate(t, [CUES[k], sceneEnd(k)], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          return (
            <div key={k} style={{ flex: 1, height: 4, borderRadius: 2, background: "rgba(255,255,255,0.1)", overflow: "hidden" }}>
              <div style={{ width: `${p * 100}%`, height: "100%", background: C.text }} />
            </div>
          );
        })}
      </div>
    </div>
  );
};

/* ---------------- Captions: chunked, active-word pill ---------------- */
type Chunk = { st: number; en: number; words: { w: string; s: number; e: number }[] };
const CHUNKS: Chunk[] = (() => {
  const out: Chunk[] = [];
  for (const l of LINES) {
    if (l.cue === "h1") continue;
    let cur: Chunk["words"] = [];
    const groups: Chunk["words"][] = [];
    for (const w of l.words) {
      if (cur.length && (cur.length >= 5 || w.s - cur[cur.length - 1].e > 0.3)) { groups.push(cur); cur = []; }
      cur.push(w);
    }
    if (cur.length) groups.push(cur);
    groups.forEach((g, i) => out.push({ st: g[0].s - 0.05, en: i + 1 < groups.length ? groups[i + 1][0].s - 0.05 : g[g.length - 1].e + 0.3, words: g }));
  }
  return out;
})();

export const Captions: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  if (t >= CUES.H) return null;
  const ch = CHUNKS.find((c) => t >= c.st && t < c.en);
  return (
    <>
      <div style={{ position: "absolute", left: 0, top: 1540, width: 1080, height: 380, background: "linear-gradient(180deg, rgba(6,7,10,0) 0%, rgba(6,7,10,0.9) 40%, rgba(6,7,10,1) 100%)" }} />
      {ch && (
        <div style={{ position: "absolute", left: 80, width: 920, top: 1650, display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "6px 4px",
          opacity: sp(f, ch.st, 200, 6), transform: `translateY(${(1 - sp(f, ch.st, 200, 8)) * 14}px)` }}>
          {ch.words.map((w, i) => {
            const active = t >= w.s && t < Math.max(w.e, w.s + 0.12);
            const said = t >= w.s;
            const pop = sp(f, w.s, 14, 8);
            return (
              <span key={i} style={{ fontFamily: SANS, fontWeight: 700, fontSize: 48, letterSpacing: "-0.01em", padding: "4px 12px", borderRadius: 12,
                color: said ? C.text : "rgba(255,255,255,0.32)", background: active ? C.red : "transparent",
                transform: `scale(${active ? 1 + 0.06 * pop : 1})`, boxShadow: active ? "0 8px 24px rgba(255,77,87,0.35)" : "none" }}>
                {w.w}
              </span>
            );
          })}
        </div>
      )}
    </>
  );
};

/* ---------------- Glass card ---------------- */
export const Glass: React.FC<{ style?: React.CSSProperties; children: React.ReactNode; accent?: string }> = ({ style, children, accent }) => (
  <div style={{ background: C.panel, border: `1px solid ${C.line}`, borderRadius: 30, backdropFilter: "blur(24px)", boxShadow: "0 30px 60px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.06)",
    ...(accent ? { borderLeft: `6px solid ${accent}` } : {}), ...style }}>
    {children}
  </div>
);

/* ---------------- Phone with WhatsApp-style chat ---------------- */
export type PhoneProps = {
  showMsgAt?: number; showFileAt?: number; showTypingFrom?: number; showAutoReplyAt?: number | null;
  highlight?: { target: "msg" | "file" | "head" | "ar"; from: number; to: number }[]; dangerAt?: number | null;
};
const Ring: React.FC<{ on: number; color: string; radius?: number }> = ({ on, color, radius = 22 }) => (
  <div style={{ position: "absolute", inset: -9, borderRadius: radius, border: `4px solid ${color}`, opacity: on, boxShadow: `0 0 ${30 * on}px ${color}`, pointerEvents: "none" }} />
);
export const Phone: React.FC<PhoneProps> = ({ showMsgAt = 0, showFileAt = 0, showTypingFrom, showAutoReplyAt = null, highlight = [], dangerAt = null }) => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const hl = (k: string) => {
    const h = highlight.find((x) => x.target === k);
    if (!h) return 0;
    return Math.min(sp(f, h.from), 1 - sp(f, h.to - 0.3));
  };
  const bub = (at: number): React.CSSProperties => {
    const p = sp(f, at, 15);
    return { opacity: Math.min(1, p * 1.5), transform: `translateY(${(1 - p) * 30}px) scale(${0.9 + 0.1 * p})`, transformOrigin: "0% 100%" };
  };
  const typingOn = showTypingFrom !== undefined && t >= showTypingFrom && t < showMsgAt;
  const danger = dangerAt == null ? 0 : sp(f, dangerAt) * (0.65 + 0.35 * Math.abs(Math.sin((t - dangerAt) * 4)));
  return (
    <div style={{ width: 640, height: 1180, borderRadius: 92, padding: 14, background: "linear-gradient(145deg, #3A3F48, #15181D 40%, #0D0F12)",
      boxShadow: "0 0 0 2px #4A505B, 0 80px 140px rgba(0,0,0,0.65), inset 0 0 0 2px rgba(255,255,255,0.05)" }}>
      <div style={{ position: "relative", width: "100%", height: "100%", borderRadius: 80, overflow: "hidden", background: C.waBg, fontFamily: SANS }}>
        <div style={{ position: "absolute", left: "50%", top: 18, width: 180, height: 50, marginLeft: -90, borderRadius: 26, background: "#000", zIndex: 3 }} />
        <div style={{ height: 86, display: "flex", justifyContent: "space-between", alignItems: "flex-end", padding: "0 58px 10px", color: "#fff", fontWeight: 600, fontSize: 24 }}>
          <span>2:40</span><span style={{ fontFamily: MONO, fontSize: 20 }}>5G</span>
        </div>
        <div style={{ position: "relative", display: "flex", alignItems: "center", gap: 18, background: C.waHead, padding: "18px 26px 20px" }}>
          <svg width="20" height="32" viewBox="0 0 12 20"><path d="M10 2 2 10l8 8" stroke="#E9EDEF" strokeWidth="2.4" fill="none" strokeLinecap="round" /></svg>
          <div style={{ width: 66, height: 66, borderRadius: "50%", background: "linear-gradient(135deg,#7C8A99,#4E5A66)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff", fontWeight: 700, fontSize: 30 }}>F</div>
          <div><div style={{ color: "#E9EDEF", fontWeight: 600, fontSize: 30 }}>Friend</div><div style={{ color: "#8696A0", fontSize: 22, marginTop: 2 }}>saved contact</div></div>
          <Ring on={hl("head")} color={C.amber} radius={18} />
        </div>
        <div style={{ padding: 22, display: "flex", flexDirection: "column", gap: 14 }}>
          {typingOn && (
            <div style={{ alignSelf: "flex-start", background: C.waIn, borderRadius: 18, padding: "18px 22px", display: "flex", gap: 8 }}>
              {[0, 1, 2].map((i) => (
                <span key={i} style={{ width: 12, height: 12, borderRadius: "50%", background: "#8696A0", opacity: 0.4 + 0.6 * Math.abs(Math.sin(t * 6 - i * 0.7)) }} />
              ))}
            </div>
          )}
          {t >= showMsgAt && (
            <div style={{ ...bub(showMsgAt), position: "relative", alignSelf: "flex-start", maxWidth: 530, background: C.waIn, borderRadius: "0 18px 18px 18px", padding: "16px 20px 10px", color: "#E9EDEF", fontSize: 25, lineHeight: 1.36 }}>
              {SCAM_MSG.map((p, i) => <p key={i} style={{ margin: i ? "14px 0 0" : 0 }}>{p}</p>)}
              <div style={{ textAlign: "right", fontSize: 19, color: "#8696A0", marginTop: 6 }}>2:40 PM</div>
              <Ring on={hl("msg")} color={C.amber} />
            </div>
          )}
          {t >= showFileAt && (
            <div style={{ ...bub(showFileAt), position: "relative", alignSelf: "flex-start", background: C.waIn, borderRadius: 18, padding: "10px 10px 8px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 16, background: C.waFile, borderRadius: 12, padding: 16 }}>
                <div style={{ width: 52, height: 64, borderRadius: 6, background: "#8696A0", color: C.waBg, fontWeight: 800, fontSize: 16, display: "flex", alignItems: "flex-end", justifyContent: "center", paddingBottom: 8 }}>ZIP</div>
                <div>
                  <div style={{ fontFamily: MONO, fontWeight: 500, fontSize: 22, color: "#E9EDEF" }}>{FILE_NAME}</div>
                  <div style={{ fontSize: 19, color: "#8696A0", marginTop: 4 }}>4.0 MB · ZIP</div>
                </div>
              </div>
              <div style={{ textAlign: "right", fontSize: 19, color: "#8696A0", marginTop: 6, paddingRight: 8 }}>2:40 PM</div>
              <Ring on={hl("file")} color={C.amber} />
              <Ring on={danger} color={C.red} />
            </div>
          )}
          {showAutoReplyAt != null && t >= showAutoReplyAt && (
            <div style={{ ...bub(showAutoReplyAt), position: "relative", alignSelf: "flex-start", maxWidth: 530, background: C.waIn, borderRadius: "0 18px 18px 18px", padding: "16px 20px 10px", color: "#E9EDEF", fontSize: 25, lineHeight: 1.36 }}>
              Hi there! Thank you for messaging… I have received your message and will respond shortly.
              <div style={{ textAlign: "right", fontSize: 19, color: "#8696A0", marginTop: 6 }}>2:41 PM</div>
              <Ring on={hl("ar")} color={C.amber} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export const rel = (cue: string, scene: string) => CUES[cue] - CUES[scene];
