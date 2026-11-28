import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from "remotion";
import { Ban, Bug, FileX2, Laptop, Lock, MessageCircle, PhoneCall, ScanSearch, ShieldCheck, UserX, Users, WifiOff, Briefcase, FileArchive, UserCheck } from "lucide-react";
import { Phone } from "../components";
import { Captions, DATA, FILE_NAME, FPS, MONO, SANS, SceneProps, Scenes, Sound, sp, ramp, stdSfx, useLocal, Key } from "./shared";

const D = DATA.soft;
const S = { ink: "#1D1D1F", sub: "#6E6E73", red: "#FF3B30", orange: "#FF9500", blue: "#0071E3", green: "#34C759", card: "rgba(255,255,255,0.72)" };
const grad = { background: `linear-gradient(90deg, ${S.red}, ${S.orange})`, WebkitBackgroundClip: "text", backgroundClip: "text", color: "transparent" } as React.CSSProperties;

const Shell: React.FC<{ dur: number; k: Key; children: React.ReactNode }> = ({ dur, children }) => {
  const f = useCurrentFrame();
  const i = interpolate(f, [0, 20], [0, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const o = interpolate(f, [dur * FPS - 14, dur * FPS], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.in(Easing.cubic) });
  return <AbsoluteFill style={{ opacity: i * (1 - o), transform: `scale(${0.96 + 0.04 * i + o * 0.04})`, filter: `blur(${(1 - i) * 14 + o * 14}px)` }}>{children}</AbsoluteFill>;
};
const H: React.FC<{ at: number; children: React.ReactNode; size?: number; top: number; sub?: boolean }> = ({ at, children, size = 84, top, sub }) => {
  const f = useCurrentFrame();
  const q = sp(f, at, 200, 26);
  return (
    <div style={{ position: "absolute", left: 80, top, width: 920, textAlign: "center", fontFamily: SANS, fontWeight: sub ? 500 : 700, fontSize: size, lineHeight: 1.08, letterSpacing: sub ? "-0.01em" : "-0.035em",
      color: sub ? S.sub : S.ink, opacity: q, transform: `translateY(${(1 - q) * 40}px)`, filter: `blur(${(1 - q) * 8}px)` }}>
      {children}
    </div>
  );
};
const Card: React.FC<{ style?: React.CSSProperties; children: React.ReactNode }> = ({ style, children }) => (
  <div style={{ background: S.card, borderRadius: 40, border: "1px solid rgba(255,255,255,0.9)", backdropFilter: "blur(30px)", boxShadow: "0 30px 80px rgba(60,50,90,0.14), 0 2px 6px rgba(0,0,0,0.04)", ...style }}>{children}</div>
);

const A: React.FC<SceneProps> = (p) => {
  const { f, t, r } = useLocal(p);
  const a2 = r("a2");
  const zoom = ramp(t, a2 - 0.5, a2 + 0.4);
  const float = Math.sin(t * 1.4) * 10;
  const rotY = interpolate(t, [0, a2 - 0.5], [-24, -6], { extrapolateRight: "clamp" }) * (1 - zoom);
  return (
    <AbsoluteFill>
      <div style={{ opacity: 1 - zoom }}><H at={r("a1")} top={250} size={78}>This file is <span style={grad}>spreading</span> on WhatsApp.</H></div>
      <div style={{ position: "absolute", left: 220, top: 500, perspective: 2400 }}>
        <div style={{ transformOrigin: "50% 62%", transform: `translateY(${(1 - sp(f, 0.1, 20)) * 800 + float - zoom * 200}px) rotateY(${rotY}deg) rotateX(${6 * (1 - zoom)}deg) scale(${0.92 + zoom * 0.2})`,
          filter: "drop-shadow(0 60px 80px rgba(60,50,90,0.35))" }}>
          <Phone showMsgAt={0.5} showFileAt={1.0} dangerAt={a2 + 0.2} />
        </div>
      </div>
      <div style={{ position: "absolute", left: 0, width: 1080, top: 1420, display: "flex", justifyContent: "center", opacity: sp(f, a2 + 0.15), transform: `translateY(${(1 - sp(f, a2 + 0.15, 14)) * 40}px)` }}>
        <div style={{ display: "flex", alignItems: "center", gap: 14, padding: "22px 40px", borderRadius: 999, background: S.red, color: "#fff", fontFamily: SANS, fontWeight: 700, fontSize: 46, boxShadow: "0 24px 60px rgba(255,59,48,0.4)" }}>
          <Ban size={46} strokeWidth={2.4} /> Don’t open it.
        </div>
      </div>
    </AbsoluteFill>
  );
};

const TIMES = ["2:38 PM", "2:39 PM", "2:40 PM", "2:40 PM", "2:41 PM", "2:42 PM"];
const B: React.FC<SceneProps> = (p) => {
  const { f, t, r } = useLocal(p);
  const at = TIMES.map((_, i) => r("b2") + 0.3 + i * 0.62);
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 0, width: 1080, top: 250, display: "flex", justifyContent: "center", opacity: sp(f, r("b1")) }}>
        <div style={{ padding: "12px 26px", borderRadius: 999, background: "rgba(255,255,255,0.8)", fontFamily: SANS, fontWeight: 600, fontSize: 30, color: S.sub, boxShadow: "0 10px 30px rgba(60,50,90,0.1)" }}>27 November 2026 · 2:38 PM</div>
      </div>
      <H at={r("b1") + 1.6} top={350} size={76}>Harith’s account was <span style={grad}>hijacked.</span></H>
      <div style={{ position: "absolute", left: 90, top: 620, width: 900 }}>
        {TIMES.map((tm, i) => {
          if (t < at[i] - 0.05) return null;
          const q = sp(f, at[i], 15);
          let y = 0;
          for (let j = i + 1; j < at.length; j++) y += sp(f, at[j], 18) * 140;
          return (
            <div key={i} style={{ position: "absolute", width: 900, transform: `translateY(${y + (1 - q) * -90}px) scale(${0.92 + 0.08 * q})`, opacity: Math.min(1, q * 1.4) * (1 - Math.max(0, (y - 560) / 140)) }}>
              <Card style={{ height: 120, borderRadius: 34, display: "flex", alignItems: "center", gap: 22, padding: "0 28px" }}>
                <div style={{ width: 66, height: 66, borderRadius: 16, background: "linear-gradient(135deg,#5AE07A,#25B04A)", display: "flex", alignItems: "center", justifyContent: "center" }}><MessageCircle size={36} color="#fff" /></div>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", fontFamily: SANS, fontWeight: 700, fontSize: 30, color: S.ink }}><span>Harith</span><span style={{ fontWeight: 500, fontSize: 24, color: S.sub }}>{tm}</span></div>
                  <div style={{ fontFamily: MONO, fontSize: 23, color: S.sub, marginTop: 4 }}>📎 {FILE_NAME}</div>
                </div>
              </Card>
            </div>
          );
        })}
      </div>
      <H at={r("b2") + 4.2} top={1440} size={36} sub>Sent to the whole contact list in about 4 minutes.</H>
    </AbsoluteFill>
  );
};

const Cc: React.FC<SceneProps> = (p) => {
  const { f, r } = useLocal(p);
  const items = [{ cue: "c1", I: Briefcase, t: "A formal “Finance” request", c: S.blue }, { cue: "c2", I: FileArchive, t: "A ZIP with a strange name", c: S.orange }, { cue: "c3", I: UserCheck, t: "From someone you trust", c: S.red }];
  return (
    <AbsoluteFill>
      <H at={r("c0")} top={260} size={84}>Watch for these <span style={grad}>signs.</span></H>
      {items.map(({ cue, I, t, c }, i) => {
        const q = sp(f, r(cue), 16);
        return (
          <div key={cue} style={{ position: "absolute", left: 90, top: 520 + i * 300, width: 900, perspective: 1600 }}>
            <div style={{ opacity: q, transform: `rotateX(${(1 - q) * 50}deg) translateY(${(1 - q) * 80}px)`, transformOrigin: "50% 0" }}>
              <Card style={{ padding: "40px 44px", display: "flex", alignItems: "center", gap: 34 }}>
                <div style={{ width: 120, height: 120, borderRadius: 32, background: `${c}18`, display: "flex", alignItems: "center", justifyContent: "center" }}><I size={62} color={c} strokeWidth={1.9} /></div>
                <div>
                  <div style={{ fontFamily: SANS, fontWeight: 600, fontSize: 26, color: S.sub }}>Sign {i + 1}</div>
                  <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 48, letterSpacing: "-0.025em", color: S.ink, marginTop: 4 }}>{t}</div>
                </div>
              </Card>
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

const Dd: React.FC<SceneProps> = (p) => {
  const { f, t, r } = useLocal(p);
  const nodes = [{ cue: "d1", I: Bug, t: "Device\ninfected" }, { cue: "d2", I: UserX, t: "Account\ntaken over" }, { cue: "d3", I: Users, t: "Spreads\nagain" }];
  return (
    <AbsoluteFill>
      <H at={0.15} top={300} size={84}>If you open it…</H>
      <div style={{ position: "absolute", left: 90, top: 820, width: 900, height: 4, background: "rgba(29,29,31,0.08)", borderRadius: 2 }} />
      <div style={{ position: "absolute", left: 90, top: 820, width: 900 * ramp(t, r("d1"), r("d3") + 0.3), height: 4, background: `linear-gradient(90deg, ${S.orange}, ${S.red})`, borderRadius: 2 }} />
      {nodes.map(({ cue, I, t: label }, i) => {
        const q = sp(f, r(cue), 12);
        const on = t >= r(cue);
        const pulse = on ? ((t - r(cue)) % 1.6) / 1.6 : 0;
        return (
          <div key={cue} style={{ position: "absolute", left: 90 + i * 330 - 10, top: 690, width: 260, display: "flex", flexDirection: "column", alignItems: "center" }}>
            <div style={{ position: "relative", width: 260, height: 260, display: "flex", alignItems: "center", justifyContent: "center" }}>
              {on && <div style={{ position: "absolute", width: 230, height: 230, borderRadius: "50%", border: `3px solid ${S.red}`, opacity: 1 - pulse, transform: `scale(${1 + pulse * 0.5})` }} />}
              <div style={{ width: 230, height: 230, borderRadius: "50%", background: on ? "#fff" : "rgba(255,255,255,0.5)", boxShadow: on ? "0 30px 70px rgba(255,59,48,0.25)" : "0 10px 30px rgba(60,50,90,0.08)",
                display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${0.7 + 0.3 * q})` }}>
                <I size={96} color={on ? S.red : "#B0B0B5"} strokeWidth={1.7} />
              </div>
            </div>
            <div style={{ marginTop: 26, textAlign: "center", whiteSpace: "pre-line", fontFamily: SANS, fontWeight: 700, fontSize: 40, lineHeight: 1.1, letterSpacing: "-0.02em", color: on ? S.ink : "#B0B0B5", opacity: Math.max(0.4, q) }}>{label}</div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

const E: React.FC<SceneProps> = (p) => {
  const { f, r } = useLocal(p);
  const tiles = [{ cue: "e1", I: FileX2, t: "Don’t open unexpected files", c: S.red }, { cue: "e2", I: PhoneCall, t: "Call the sender to confirm", c: S.blue },
    { cue: "e3", I: Lock, t: "Turn on two-step verification", c: S.green }, { cue: "e4", I: Laptop, t: "Check linked devices", c: S.orange }];
  return (
    <AbsoluteFill>
      <H at={r("e0")} top={260} size={84}>Protect <span style={{ ...grad, background: `linear-gradient(90deg, ${S.green}, ${S.blue})`, WebkitBackgroundClip: "text" }}>yourself.</span></H>
      {tiles.map(({ cue, I, t, c }, i) => {
        const q = sp(f, r(cue), 14);
        const col = i % 2, row = Math.floor(i / 2);
        return (
          <div key={cue} style={{ position: "absolute", left: 90 + col * 460, top: 480 + row * 470, width: 440, opacity: q, transform: `translateY(${(1 - q) * 80}px) scale(${0.85 + 0.15 * q})` }}>
            <Card style={{ height: 440, padding: "44px 40px", display: "flex", flexDirection: "column", justifyContent: "space-between" }}>
              <div style={{ width: 110, height: 110, borderRadius: 30, background: `${c}1A`, display: "flex", alignItems: "center", justifyContent: "center" }}><I size={60} color={c} strokeWidth={1.9} /></div>
              <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 44, lineHeight: 1.1, letterSpacing: "-0.025em", color: S.ink }}>{t}</div>
            </Card>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

const F: React.FC<SceneProps> = (p) => {
  const { f, r } = useLocal(p);
  const pills = [{ I: WifiOff, t: "Disconnect", at: r("f1") + 1.2 }, { I: ScanSearch, t: "Scan your device", at: r("f1") + 1.9 }];
  const card = sp(f, r("f2"), 16);
  return (
    <AbsoluteFill>
      <H at={r("f1")} top={260} size={84}>Already opened it?</H>
      <div style={{ position: "absolute", left: 0, width: 1080, top: 460, display: "flex", justifyContent: "center", gap: 20 }}>
        {pills.map(({ I, t, at }) => {
          const q = sp(f, at, 14);
          return <div key={t} style={{ display: "flex", alignItems: "center", gap: 14, padding: "22px 34px", borderRadius: 999, background: "#fff", boxShadow: "0 16px 40px rgba(60,50,90,0.12)", fontFamily: SANS, fontWeight: 700, fontSize: 38, color: S.ink, opacity: q, transform: `scale(${0.8 + 0.2 * q})` }}><I size={40} color={S.blue} />{t}</div>;
        })}
      </div>
      <div style={{ position: "absolute", left: 90, top: 700, width: 900, opacity: card, transform: `translateY(${(1 - card) * 80}px)` }}>
        <Card style={{ padding: "56px 56px", textAlign: "center" }}>
          <div style={{ fontFamily: SANS, fontWeight: 600, fontSize: 30, color: S.sub }}>Report it to CyberSecurity Malaysia</div>
          <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 130, letterSpacing: "-0.05em", color: S.ink, lineHeight: 1.05, marginTop: 10 }}>Cyber999</div>
          <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 60, letterSpacing: "-0.02em", marginTop: 10, ...grad }}>1-300-88-2999</div>
          <div style={{ height: 1, background: "rgba(0,0,0,0.08)", margin: "36px 0 28px" }} />
          <div style={{ fontFamily: SANS, fontWeight: 600, fontSize: 32, color: S.sub }}>Lost money? Call <span style={{ color: S.ink, fontWeight: 800 }}>NSRC 997</span></div>
        </Card>
      </div>
    </AbsoluteFill>
  );
};

const G: React.FC<SceneProps> = (p) => {
  const { f, r } = useLocal(p);
  const q = sp(f, 0.1, 12);
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 0, width: 1080, top: 470, display: "flex", justifyContent: "center" }}>
        <div style={{ width: 240, height: 240, borderRadius: 64, background: `linear-gradient(135deg, ${S.green}, #0BA5A0)`, display: "flex", alignItems: "center", justifyContent: "center", boxShadow: "0 40px 90px rgba(52,199,89,0.4)", transform: `scale(${q}) rotate(${(1 - q) * -20}deg)` }}>
          <ShieldCheck size={150} color="#fff" strokeWidth={1.7} />
        </div>
      </div>
      <H at={r("g1")} top={800} size={110}>Share this video.</H>
      <H at={r("g1") + 1.4} top={960} size={44} sub>It could protect someone you love.</H>
      <div style={{ position: "absolute", left: 0, width: 1080, top: 1100, display: "flex", justifyContent: "center", opacity: sp(f, r("g1") + 3) }}>
        <div style={{ padding: "18px 36px", borderRadius: 999, background: S.ink, color: "#fff", fontFamily: SANS, fontWeight: 700, fontSize: 38 }}>#DontOpenTheZIP</div>
      </div>
    </AbsoluteFill>
  );
};

const Bg: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  return (
    <AbsoluteFill style={{ background: "linear-gradient(180deg, #F7F6FB 0%, #EEEAF4 100%)", overflow: "hidden" }}>
      <div style={{ position: "absolute", width: 1100, height: 1100, borderRadius: "50%", left: -380 + Math.sin(t * 0.2) * 120, top: -300 + Math.cos(t * 0.17) * 100, background: "radial-gradient(circle, rgba(255,149,0,0.22), transparent 62%)" }} />
      <div style={{ position: "absolute", width: 1200, height: 1200, borderRadius: "50%", right: -460 + Math.cos(t * 0.15) * 120, top: 600 + Math.sin(t * 0.19) * 140, background: "radial-gradient(circle, rgba(120,110,255,0.2), transparent 62%)" }} />
      <div style={{ position: "absolute", width: 900, height: 900, borderRadius: "50%", left: 100 + Math.sin(t * 0.13) * 140, bottom: -420, background: "radial-gradient(circle, rgba(255,59,48,0.12), transparent 62%)" }} />
    </AbsoluteFill>
  );
};

export const V5Soft: React.FC = () => (
  <AbsoluteFill>
    <Bg />
    <Scenes data={D} map={{ A, B, C: Cc, D: Dd, E, F, G }} shell={Shell} />
    <div style={{ position: "absolute", left: 0, width: 1080, top: 90, display: "flex", justifyContent: "center" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10, padding: "10px 22px", borderRadius: 999, background: "rgba(255,255,255,0.7)", fontFamily: SANS, fontWeight: 600, fontSize: 24, color: S.ink, boxShadow: "0 8px 24px rgba(60,50,90,0.1)" }}>
        <span style={{ width: 10, height: 10, borderRadius: "50%", background: S.red }} /> Security Alert
      </div>
    </div>
    <Captions data={D} until={D.cues.G} s={{ top: 1690, size: 44, weight: 600, said: S.ink, unsaid: "rgba(29,29,31,0.3)", activeBg: S.ink, activeColor: "#fff", radius: 999,
      plate: "linear-gradient(180deg, rgba(238,234,244,0) 0%, rgba(238,234,244,0.95) 35%)" }} />
    <Sound style="soft" data={D} music={0.22} sfx={[...stdSfx(D, 0.12, 0.1), ["pop", "a2", 0.15], ["ding", "g1", 0.12]]} />
  </AbsoluteFill>
);
