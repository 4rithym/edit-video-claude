import React from "react";
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, Easing } from "remotion";
import { Ban, Bug, FileX2, KeyRound, Laptop, Lock, MessageCircle, Paperclip, PhoneCall, ScanSearch, ShieldCheck, TriangleAlert, UserX, Users, WifiOff } from "lucide-react";
import { Background, Glass, Kicker, Phone, Reveal } from "../components";
import { C } from "../theme";
import { Captions, DATA, FILE_NAME, FPS, KEYS, MONO, SANS, SceneProps, Scenes, Sound, sceneEnd, sp, ramp, stdSfx, useLocal, Key } from "./shared";

const D = DATA.noir;

const Shell: React.FC<{ dur: number; k: Key; children: React.ReactNode }> = ({ dur, children }) => {
  const f = useCurrentFrame();
  const i = interpolate(f, [0, 16], [0, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const o = interpolate(f, [dur * FPS - 13, dur * FPS], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.in(Easing.cubic) });
  return <AbsoluteFill style={{ opacity: i * (1 - o), transform: `translateY(${(1 - i) * 40 - o * 40}px)`, filter: `blur(${(1 - i) * 10 + o * 10}px)` }}>{children}</AbsoluteFill>;
};
const Title: React.FC<{ k: string; t: string }> = ({ k, t }) => (
  <div style={{ position: "absolute", left: 80, top: 200, width: 920 }}>
    <Kicker at={0.05}><span style={{ width: 40, height: 3, background: C.red, display: "inline-block" }} />{k}</Kicker>
    <Reveal text={t} at={0.12} size={80} style={{ marginTop: 16 }} />
  </div>
);

const A: React.FC<SceneProps> = (p) => {
  const { f, t, r } = useLocal(p);
  const a2 = r("a2");
  const enter = sp(f, 0.1, 18);
  const zoom = sp(f, a2 - 0.3, 200, 30);
  const chip = sp(f, a2 + 0.1, 13);
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 60%, rgba(255,77,87,${0.2 * ramp(t, a2, a2 + 0.3)}) 0%, transparent 60%)` }} />
      <div style={{ position: "absolute", left: 80, top: 200, width: 920, opacity: 1 - zoom }}>
        <Kicker at={0.1}><TriangleAlert size={30} strokeWidth={2.6} /> SECURITY ALERT</Kicker>
        <Reveal text="This file is spreading on WhatsApp." at={r("a1")} size={76} accent={["spreading"]} style={{ marginTop: 18 }} />
      </div>
      <div style={{ position: "absolute", left: 220, top: 560, perspective: 2200 }}>
        <div style={{ transformOrigin: "50% 62%", transform: `translateY(${(1 - enter) * 700 - zoom * 330}px) rotateY(${-22 * (1 - enter) - 8 * (1 - zoom)}deg) rotateX(${4 * (1 - zoom)}deg) scale(${1 + zoom * 0.22})` }}>
          <Phone showMsgAt={0.6} showFileAt={1.2} dangerAt={a2} />
        </div>
      </div>
      <div style={{ position: "absolute", left: 460, top: 1200, opacity: chip, transform: `scale(${0.6 + 0.4 * chip})`, transformOrigin: "0 50%", display: "flex", alignItems: "center", gap: 12, padding: "18px 28px",
        borderRadius: 18, background: C.red, color: "#fff", fontFamily: MONO, fontWeight: 700, fontSize: 34, letterSpacing: "0.08em", boxShadow: "0 24px 60px rgba(255,77,87,0.55)" }}>
        <Ban size={36} strokeWidth={2.6} /> DON'T OPEN IT
      </div>
    </AbsoluteFill>
  );
};

const TIMES = ["14:38", "14:39", "14:40", "14:40", "14:41", "14:42"];
const B: React.FC<SceneProps> = (p) => {
  const { f, t, r } = useLocal(p);
  const at = TIMES.map((_, i) => r("b2") + 0.3 + i * 0.6);
  const n = at.filter((x) => t >= x).length;
  return (
    <AbsoluteFill>
      <Title k="WHAT HAPPENED" t="27.11.2026" />
      <div style={{ position: "absolute", left: 80, top: 400, fontFamily: MONO, fontWeight: 700, fontSize: 64, color: C.red, opacity: sp(f, r("b1") + 1.2), textShadow: "0 0 30px rgba(255,77,87,0.5)" }}>{n ? TIMES[n - 1] : "14:38"}</div>
      <Reveal text="Harith's WhatsApp account was hijacked." at={r("b1") + 2.2} size={52} weight={700} accent={["hijacked"]} style={{ position: "absolute", left: 80, top: 510, width: 920, lineHeight: 1.15 }} />
      <div style={{ position: "absolute", left: 80, top: 700, width: 920 }}>
        {TIMES.map((tm, i) => {
          if (t < at[i] - 0.05) return null;
          const q = sp(f, at[i], 16);
          let y = 0;
          for (let j = i + 1; j < at.length; j++) y += sp(f, at[j], 18) * 128;
          return (
            <div key={i} style={{ position: "absolute", width: 920, transform: `translateY(${y + (1 - q) * -80}px) scale(${0.94 + 0.06 * q})`, opacity: Math.min(1, q * 1.4) }}>
              <Glass style={{ height: 112, display: "flex", alignItems: "center", gap: 22, padding: "0 28px" }}>
                <div style={{ width: 62, height: 62, borderRadius: 16, background: "linear-gradient(135deg,#3DD68C,#1F9D63)", display: "flex", alignItems: "center", justifyContent: "center" }}><MessageCircle size={34} color="#fff" /></div>
                <div style={{ flex: 1 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", fontFamily: SANS, fontWeight: 700, fontSize: 28, color: C.text }}><span>Harith</span><span style={{ fontFamily: MONO, fontSize: 24, color: C.muted }}>{tm}</span></div>
                  <div style={{ display: "flex", alignItems: "center", gap: 8, marginTop: 6, fontFamily: MONO, fontSize: 23, color: "#C8CED8" }}><Paperclip size={22} />{FILE_NAME}</div>
                </div>
              </Glass>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const SIGNS = [
  { cue: "c1", t: "A formal “Finance” request", target: "msg" as const },
  { cue: "c2", t: "A strangely named ZIP file", target: "file" as const },
  { cue: "c3", t: "From someone you trust", target: "head" as const },
];
const Cc: React.FC<SceneProps> = (p) => {
  const { f, t, r } = useLocal(p);
  const ends = SIGNS.map((s, i) => (i < 2 ? r(SIGNS[i + 1].cue) : 99));
  return (
    <AbsoluteFill>
      <Title k="WARNING SIGNS" t="Spot the trap" />
      <div style={{ position: "absolute", left: 220, top: 400, transform: `scale(0.66) translateY(${(1 - sp(f, 0.2, 20)) * 200}px)`, transformOrigin: "50% 0", opacity: sp(f, 0.2) }}>
        <Phone showMsgAt={-1} showFileAt={-1} highlight={SIGNS.map((s, i) => ({ target: s.target, from: r(s.cue) + 0.1, to: ends[i] }))} />
      </div>
      {SIGNS.map((s, i) => {
        const st = r(s.cue);
        if (t < st - 0.05 || t > ends[i]) return null;
        const q = sp(f, st, 18);
        return (
          <div key={i} style={{ position: "absolute", left: 80, top: 1230, width: 920, opacity: q, transform: `translateY(${(1 - q) * 50}px)` }}>
            <Glass accent={C.amber} style={{ padding: "30px 38px" }}>
              <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: "0.14em", color: C.amber }}>SIGN {i + 1} / 3</div>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 52, letterSpacing: "-0.02em", color: C.text, marginTop: 10 }}>{s.t}</div>
            </Glass>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

const CHAIN = [{ cue: "d1", I: Bug, t: "Device infected" }, { cue: "d2", I: UserX, t: "Account taken over" }, { cue: "d3", I: Users, t: "It spreads again" }];
const Dd: React.FC<SceneProps> = (p) => {
  const { f, t, r } = useLocal(p);
  const lineP = ramp(t, r("d1"), r("d3") + 0.3);
  return (
    <AbsoluteFill>
      <Title k="IF YOU OPEN IT" t="What happens next" />
      <div style={{ position: "absolute", left: 80, top: 520, width: 920 }}>
        <div style={{ position: "absolute", left: 68, top: 130, width: 4, height: 520, background: "rgba(255,255,255,0.08)" }} />
        <div style={{ position: "absolute", left: 68, top: 130, width: 4, height: 520 * lineP, background: C.red, boxShadow: "0 0 14px rgba(255,77,87,0.8)" }} />
        {CHAIN.map(({ cue, I, t: label }, i) => {
          const q = sp(f, r(cue), 16);
          const lit = t >= r(cue) + 0.15;
          return (
            <div key={cue} style={{ position: "absolute", top: i * 260, display: "flex", alignItems: "center", gap: 36, opacity: Math.max(0.2, q), transform: `translateX(${(1 - q) * -40}px)` }}>
              <div style={{ width: 140, height: 140, borderRadius: 36, background: lit ? "rgba(255,77,87,0.16)" : C.panelSolid, border: `2px solid ${lit ? C.red : C.line}`, display: "flex", alignItems: "center", justifyContent: "center", boxShadow: lit ? "0 0 50px rgba(255,77,87,0.35)" : "none" }}>
                <I size={64} color={lit ? C.red : C.muted} strokeWidth={1.8} />
              </div>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 58, letterSpacing: "-0.02em", color: C.text }}>{label}</div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const TIPS = [{ cue: "e1", I: FileX2, t: "Don't open unexpected files" }, { cue: "e2", I: PhoneCall, t: "Call the sender to confirm" }, { cue: "e3", I: Lock, t: "Turn on two-step verification" }, { cue: "e4", I: Laptop, t: "Check your linked devices" }];
const E: React.FC<SceneProps> = (p) => {
  const { f, t, r } = useLocal(p);
  return (
    <AbsoluteFill>
      <Title k="PROTECT YOURSELF" t="Four simple habits" />
      {TIPS.map(({ cue, I, t: label }, i) => {
        const q = sp(f, r(cue), 18);
        const nxt = i < 3 ? r(TIPS[i + 1].cue) : 99;
        const active = t >= r(cue) && t < nxt;
        return (
          <div key={cue} style={{ position: "absolute", left: 80, top: 450 + i * 200, width: 920, opacity: q * (t >= nxt && t < p.dur - 1.2 ? 0.45 : 1), transform: `translateY(${(1 - q) * 50}px)` }}>
            <Glass style={{ padding: "30px 34px", display: "flex", alignItems: "center", gap: 28, borderColor: active ? "rgba(61,214,140,0.55)" : C.line, boxShadow: active ? "0 0 50px rgba(61,214,140,0.15)" : undefined }}>
              <div style={{ width: 92, height: 92, borderRadius: 24, background: "rgba(61,214,140,0.12)", display: "flex", alignItems: "center", justifyContent: "center" }}><I size={48} color={C.green} /></div>
              <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 44, letterSpacing: "-0.01em", color: C.text }}>{label}</div>
            </Glass>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

const F: React.FC<SceneProps> = (p) => {
  const { f, r } = useLocal(p);
  const rows = [{ I: WifiOff, t: "Disconnect", at: r("f1") + 1.3 }, { I: ScanSearch, t: "Scan your device", at: r("f1") + 2.0 }];
  const card = sp(f, r("f2"), 16);
  return (
    <AbsoluteFill>
      <Title k="ALREADY OPENED IT?" t="Act fast" />
      {rows.map(({ I, t: label, at }, i) => {
        const q = sp(f, at, 18);
        return (
          <div key={i} style={{ position: "absolute", left: 80, top: 470 + i * 130, width: 920, display: "flex", alignItems: "center", gap: 28, padding: "24px 0", borderBottom: `1px solid ${C.line}`, opacity: q, transform: `translateX(${(1 - q) * -40}px)` }}>
            <span style={{ fontFamily: MONO, fontWeight: 700, fontSize: 30, color: C.red }}>0{i + 1}</span><I size={44} color={C.text} /><span style={{ fontFamily: SANS, fontWeight: 600, fontSize: 48, color: C.text }}>{label}</span>
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 80, top: 800, width: 920, background: C.text, color: "#0B0D10", borderRadius: 34, padding: "40px 44px", opacity: card, transform: `translateY(${(1 - card) * 60}px)`, boxShadow: "0 30px 70px rgba(0,0,0,0.45)" }}>
        <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: "0.16em", color: "#5A6270" }}>REPORT IT</div>
        <div style={{ fontFamily: SANS, fontWeight: 900, fontSize: 96, letterSpacing: "-0.03em", marginTop: 8 }}>Cyber999</div>
        <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 50, color: "#D92D37", marginTop: 4 }}>1-300-88-2999</div>
        <div style={{ fontFamily: SANS, fontWeight: 500, fontSize: 28, color: "#5A6270", marginTop: 10 }}>CyberSecurity Malaysia · Lost money? NSRC 997</div>
      </div>
    </AbsoluteFill>
  );
};

const G: React.FC<SceneProps> = (p) => {
  const { f, t, r } = useLocal(p);
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", top: 520, left: 0, width: 1080, display: "flex", justifyContent: "center" }}>
        <div style={{ position: "relative", width: 200, height: 200, display: "flex", alignItems: "center", justifyContent: "center" }}>
          {[0, 1, 2].map((i) => { const ph = ((t + i * 0.8) % 2.4) / 2.4; return <div key={i} style={{ position: "absolute", width: 200, height: 200, borderRadius: "50%", border: `2px solid ${C.green}`, opacity: (1 - ph) * 0.5, transform: `scale(${1 + ph * 1.4})` }} />; })}
          <div style={{ transform: `scale(${sp(f, 0.05, 12)})` }}><ShieldCheck size={170} color={C.green} strokeWidth={1.5} /></div>
        </div>
      </div>
      <div style={{ position: "absolute", top: 830, left: 80, width: 920, textAlign: "center" }}>
        <Reveal text="Share this video." at={r("g1")} size={112} weight={900} />
        <Reveal text="It could protect someone you love." at={r("g1") + 1.4} size={44} weight={500} color="#C8CED8" stagger={0.05} style={{ marginTop: 26 }} />
        <div style={{ display: "inline-block", marginTop: 50, padding: "16px 32px", borderRadius: 16, border: `2px solid ${C.red}`, color: C.red, fontFamily: MONO, fontWeight: 700, fontSize: 38, opacity: sp(f, r("g1") + 3) }}>#DontOpenTheZIP</div>
      </div>
    </AbsoluteFill>
  );
};

const Header: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  return (
    <div style={{ position: "absolute", left: 80, top: 80, width: 920, opacity: sp(f, 0.1) * (t > D.cues.G ? 0 : 1) }}>
      <div style={{ display: "flex", gap: 8 }}>
        {KEYS.slice(0, 6).map((k) => (
          <div key={k} style={{ flex: 1, height: 4, borderRadius: 2, background: "rgba(255,255,255,0.1)" }}>
            <div style={{ width: `${ramp(t, D.cues[k], sceneEnd(D.cues, k), Easing.linear) * 100}%`, height: "100%", background: C.text, borderRadius: 2 }} />
          </div>
        ))}
      </div>
    </div>
  );
};

export const V1Noir: React.FC = () => (
  <AbsoluteFill style={{ background: C.bg }}>
    <Background />
    <Scenes data={D} map={{ A, B, C: Cc, D: Dd, E, F, G }} shell={Shell} />
    <Header />
    <Captions data={D} until={D.cues.G} s={{ top: 1660, size: 48, said: C.text, unsaid: "rgba(255,255,255,0.32)", activeBg: C.red, activeColor: "#fff", plate: "linear-gradient(180deg, rgba(6,7,10,0) 0%, rgba(6,7,10,0.92) 40%, #06070A 100%)" }} />
    <Sound style="noir" data={D} music={0.2} sfx={[...stdSfx(D), ["ding", "a2", 0.16], ["pop", 0.6, 0.15], ["pop", 1.2, 0.15]]} />
  </AbsoluteFill>
);
