import React from "react";
import { AbsoluteFill, random, useCurrentFrame, Easing, interpolate } from "remotion";
import { Captions, DATA, FILE_NAME, FPS, KEYS, MONO, SceneProps, Scenes, Sound, sp, ramp, stdSfx, useLocal, Key } from "./shared";

const D = DATA.terminal;
const T = { bg: "#040705", g: "#3DFF8F", gd: "rgba(61,255,143,0.55)", gl: "rgba(61,255,143,0.12)", a: "#FFB000", r: "#FF4545", w: "#DFFFEA" };
const glow = (c: string) => `0 0 10px ${c}, 0 0 24px ${c}55`;

const Type: React.FC<{ text: string; at: number; cps?: number; color?: string; size?: number; cursor?: boolean; weight?: number }> = ({ text, at, cps = 45, color = T.g, size = 34, cursor = false, weight = 500 }) => {
  const f = useCurrentFrame();
  const t = f / FPS;
  if (t < at) return <div style={{ height: size * 1.4 }} />;
  const n = Math.min(text.length, Math.floor((t - at) * cps));
  const done = n >= text.length;
  return (
    <div style={{ fontFamily: MONO, fontWeight: weight, fontSize: size, lineHeight: 1.4, color, textShadow: glow(color), whiteSpace: "pre-wrap" }}>
      {text.slice(0, n)}
      {(!done || cursor) && <span style={{ opacity: Math.floor(t * 2.5) % 2 ? 1 : 0, background: color, color: T.bg }}>&nbsp;</span>}
    </div>
  );
};
const Panel: React.FC<{ title: string; at?: number; top: number; h?: number; color?: string; children: React.ReactNode }> = ({ title, at = 0, top, h, color = T.g, children }) => {
  const f = useCurrentFrame();
  const q = sp(f, at, 200, 14);
  return (
    <div style={{ position: "absolute", left: 70, top, width: 940, height: h, border: `2px solid ${color}`, boxShadow: `0 0 30px ${color}33, inset 0 0 40px ${color}14`, background: "rgba(4,10,6,0.75)",
      clipPath: `inset(0 0 ${(1 - q) * 100}% 0)` }}>
      <div style={{ display: "flex", justifyContent: "space-between", padding: "10px 20px", background: `${color}22`, borderBottom: `2px solid ${color}`, fontFamily: MONO, fontWeight: 700, fontSize: 22, letterSpacing: "0.14em", color, textShadow: glow(color) }}>
        <span>{title}</span><span>■ ■ ■</span>
      </div>
      <div style={{ padding: "22px 26px" }}>{children}</div>
    </div>
  );
};
const Glitch: React.FC<{ text: string; size: number; color: string; at: number }> = ({ text, size, color, at }) => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const burst = t >= at && t < at + 0.5 ? 1 : random(`g${Math.floor(f / 3)}`) > 0.97 ? 0.5 : 0;
  const dx = burst ? (random(`x${f}`) - 0.5) * 30 * burst : 0;
  const vis = t >= at;
  return (
    <div style={{ position: "relative", fontFamily: MONO, fontWeight: 700, fontSize: size, letterSpacing: "0.02em", lineHeight: 1, color, opacity: vis ? 1 : 0, textShadow: `${dx}px 0 #FF3D6E, ${-dx}px 0 #3DD9FF, ${glow(color)}`,
      transform: `translateX(${dx * 0.3}px)`, clipPath: burst ? `inset(${random(`c${f}`) * 12}% 0 ${random(`d${f}`) * 12}% 0)` : undefined }}>
      {text}
    </div>
  );
};

const Shell: React.FC<{ dur: number; k: Key; children: React.ReactNode }> = ({ dur, children }) => {
  const f = useCurrentFrame();
  const i = interpolate(f, [0, 8], [0, 1], { extrapolateRight: "clamp" });
  const o = interpolate(f, [dur * FPS - 8, dur * FPS], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const sq = 1 - o;
  return <AbsoluteFill style={{ opacity: i, transform: `scaleY(${Math.max(0.01, sq)})`, filter: `brightness(${1 + o * 2})` }}>{children}</AbsoluteFill>;
};

const A: React.FC<SceneProps> = (p) => {
  const { f, t, r } = useLocal(p);
  const blink = Math.floor(t * 3) % 2;
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 70, top: 260 }}>
        <Type text="> scanning whatsapp traffic..." at={0.1} size={30} />
        <Type text="> match found." at={0.9} size={30} color={T.a} />
      </div>
      <div style={{ position: "absolute", left: 70, top: 440, width: 940 }}>
        <Glitch text="THREAT" size={190} color={T.r} at={r("a1")} />
        <Glitch text="DETECTED" size={150} color={T.r} at={r("a1") + 0.3} />
      </div>
      <Panel title="PAYLOAD" at={r("a1") + 1.0} top={820} color={T.a}>
        <Type text={`file   : ${FILE_NAME}`} at={r("a1") + 1.2} size={30} color={T.w} cps={60} />
        <Type text="size   : 4.0 MB" at={r("a1") + 1.9} size={30} color={T.w} cps={60} />
        <Type text="vector : whatsapp / trusted contact" at={r("a1") + 2.3} size={30} color={T.w} cps={60} />
      </Panel>
      <div style={{ position: "absolute", left: 70, top: 1180, width: 940, padding: "30px 0", textAlign: "center", border: `4px solid ${T.r}`, background: blink && t > r("a2") ? T.r : "transparent",
        fontFamily: MONO, fontWeight: 700, fontSize: 64, letterSpacing: "0.12em", color: blink && t > r("a2") ? T.bg : T.r, textShadow: blink ? "none" : glow(T.r), opacity: sp(f, r("a2")) }}>
        ⛔ DO NOT OPEN
      </div>
    </AbsoluteFill>
  );
};

const B: React.FC<SceneProps> = (p) => {
  const { r } = useLocal(p);
  const logs = ["[14:38:04] tx -> contact_01   delivered", "[14:38:51] tx -> contact_02   delivered", "[14:39:37] tx -> contact_03   delivered", "[14:40:12] tx -> contact_04   delivered", "[14:41:08] tx -> contact_05   delivered", "[14:42:20] tx -> contact_06   delivered"];
  return (
    <AbsoluteFill>
      <Panel title="INCIDENT REPORT // 2026-11-27" top={250} color={T.g}>
        <Type text="time    : 14:38 MYT" at={r("b1") + 0.2} size={32} />
        <Type text="account : Harith (WhatsApp)" at={r("b1") + 1.2} size={32} />
        <Type text="status  : HIJACKED" at={r("b1") + 2.4} size={32} color={T.r} weight={700} />
      </Panel>
      <Panel title="OUTBOUND BROADCAST" at={r("b2")} top={640} color={T.a}>
        {logs.map((l, i) => <Type key={i} text={l} at={r("b2") + 0.3 + i * 0.6} size={27} color={T.w} cps={80} />)}
        <Type text="duration: ~4 min   target: entire contact list" at={r("b2") + 4.2} size={27} color={T.a} cps={70} weight={700} />
      </Panel>
    </AbsoluteFill>
  );
};

const Cc: React.FC<SceneProps> = (p) => {
  const { f, r } = useLocal(p);
  const sig = [["c1", "formal_finance_request", "tone mismatch"], ["c2", "zip_strange_filename", "no explanation"], ["c3", "trusted_sender", "social engineering"]];
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 70, top: 250 }}><Glitch text="SIGNATURES" size={110} color={T.g} at={r("c0")} /></div>
      {sig.map(([cue, id, note], i) => {
        const q = sp(f, r(cue), 200, 12);
        return (
          <div key={cue} style={{ position: "absolute", left: 70, top: 460 + i * 300, width: 940, height: 250, border: `2px solid ${T.a}`, background: `rgba(255,176,0,${0.06 + 0.06 * q})`, clipPath: `inset(0 ${(1 - q) * 100}% 0 0)`, padding: "28px 30px", boxShadow: `0 0 30px rgba(255,176,0,0.18)` }}>
            <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 26, color: T.a, letterSpacing: "0.12em", textShadow: glow(T.a) }}>[!] SIGNAL 0{i + 1}</div>
            <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 52, color: T.w, marginTop: 18, textShadow: glow(T.g) }}>{id}</div>
            <div style={{ fontFamily: MONO, fontSize: 28, color: T.gd, marginTop: 12 }}>// {note}</div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

const Dd: React.FC<SceneProps> = (p) => {
  const { t, r } = useLocal(p);
  const nodes = [["d1", "DEVICE", "infected"], ["d2", "ACCOUNT", "taken over"], ["d3", "CONTACTS", "infected next"]];
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 70, top: 250 }}><Glitch text="INFECTION CHAIN" size={84} color={T.r} at={0.1} /></div>
      {nodes.map(([cue, a, b], i) => {
        const on = t >= r(cue);
        const lineP = i < 2 ? ramp(t, r(cue) + 0.2, r(nodes[i + 1][0])) : 0;
        return (
          <React.Fragment key={cue}>
            <div style={{ position: "absolute", left: 220, top: 450 + i * 380, width: 640, height: 220, border: `3px solid ${on ? T.r : "rgba(255,69,69,0.25)"}`, background: on ? "rgba(255,69,69,0.1)" : "transparent",
              boxShadow: on ? `0 0 40px rgba(255,69,69,0.35)` : "none", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
              <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 70, color: on ? T.r : "rgba(255,69,69,0.3)", textShadow: on ? glow(T.r) : "none" }}>[ {a} ]</div>
              <div style={{ fontFamily: MONO, fontSize: 30, color: on ? T.w : "rgba(223,255,234,0.25)", marginTop: 10 }}>status: {on ? b : "..."}</div>
            </div>
            {i < 2 && <div style={{ position: "absolute", left: 538, top: 670 + i * 380, width: 4, height: 160 * lineP, background: T.r, boxShadow: glow(T.r) }} />}
          </React.Fragment>
        );
      })}
    </AbsoluteFill>
  );
};

const E: React.FC<SceneProps> = (p) => {
  const { r } = useLocal(p);
  const cm = [["e1", "block    unexpected_files"], ["e2", "verify   sender --by-call"], ["e3", "enable   two_step_verification"], ["e4", "audit    linked_devices --logout-unknown"]];
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 70, top: 250 }}><Glitch text="COUNTERMEASURES" size={84} color={T.g} at={r("e0")} /></div>
      <Panel title="HARDENING CHECKLIST" at={r("e0") + 0.3} top={420} color={T.g}>
        {cm.map(([cue, txt]) => (
          <div key={cue} style={{ marginBottom: 26 }}>
            <Type text={`[✓] ${txt}`} at={r(cue)} size={34} color={T.g} cps={70} weight={700} />
          </div>
        ))}
      </Panel>
    </AbsoluteFill>
  );
};

const F: React.FC<SceneProps> = (p) => {
  const { r } = useLocal(p);
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 70, top: 250 }}><Glitch text="ALREADY OPENED?" size={84} color={T.a} at={0.1} /></div>
      <Panel title="INCIDENT RESPONSE" at={0.3} top={420} color={T.a}>
        <Type text="$ network --disconnect" at={r("f1") + 1.2} size={34} color={T.w} cps={60} />
        <Type text="$ device --scan --antivirus" at={r("f1") + 2.0} size={34} color={T.w} cps={60} />
        <Type text="$ report --to Cyber999" at={r("f2")} size={34} color={T.w} cps={60} />
      </Panel>
      <div style={{ position: "absolute", left: 70, top: 900, width: 940, border: `3px solid ${T.g}`, padding: "36px 40px", boxShadow: `0 0 40px ${T.g}33` }}>
        <Type text="CYBER999 HOTLINE" at={r("f2") + 0.8} size={30} color={T.gd} cps={60} />
        <Type text="1-300-88-2999" at={r("f2") + 1.1} size={92} color={T.g} cps={30} weight={700} />
        <Type text="lost money? -> NSRC 997" at={r("f2") + 1.8} size={32} color={T.a} cps={60} />
      </div>
    </AbsoluteFill>
  );
};

const G: React.FC<SceneProps> = (p) => {
  const { r } = useLocal(p);
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 70, top: 620, width: 940 }}>
        <Glitch text="SHARE" size={230} color={T.g} at={r("g1")} />
        <Glitch text="TO PROTECT." size={110} color={T.w} at={r("g1") + 0.4} />
        <div style={{ marginTop: 50 }}><Type text="> someone you love is one tap away from that file." at={r("g1") + 1.4} size={32} color={T.gd} cps={50} /></div>
        <div style={{ marginTop: 30 }}><Type text="#DontOpenTheZIP" at={r("g1") + 3.0} size={46} color={T.a} cps={30} weight={700} cursor /></div>
      </div>
    </AbsoluteFill>
  );
};

const Overlay: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const sec = 38 * 60 + Math.floor(t * 4);
  const clock = `14:${String(Math.floor(sec / 60) % 60).padStart(2, "0")}:${String(sec % 60).padStart(2, "0")}`;
  return (
    <>
      <div style={{ position: "absolute", left: 70, top: 90, width: 940, display: "flex", justifyContent: "space-between", fontFamily: MONO, fontWeight: 700, fontSize: 22, letterSpacing: "0.14em", color: T.g, textShadow: glow(T.g) }}>
        <span>SOC // INCIDENT 2026-11-27</span><span style={{ color: T.r }}>● LIVE {clock}</span>
      </div>
      <div style={{ position: "absolute", left: 70, top: 136, width: 940, height: 2, background: T.gd }} />
      <div style={{ position: "absolute", left: 70, top: 136, width: 940 * (t / 60), height: 2, background: T.g, boxShadow: glow(T.g) }} />
      <AbsoluteFill style={{ background: "repeating-linear-gradient(180deg, rgba(0,0,0,0) 0px, rgba(0,0,0,0) 2px, rgba(0,0,0,0.28) 3px, rgba(0,0,0,0) 4px)", pointerEvents: "none" }} />
      <div style={{ position: "absolute", left: 0, width: 1080, height: 220, top: ((t * 260) % 2300) - 220, background: "linear-gradient(180deg, transparent, rgba(61,255,143,0.05), transparent)" }} />
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 50%, transparent 55%, rgba(0,0,0,0.75) 100%)", opacity: 0.95 + 0.05 * random(`fl${f}`) }} />
    </>
  );
};

export const V4Terminal: React.FC = () => (
  <AbsoluteFill style={{ background: T.bg }}>
    <AbsoluteFill style={{ backgroundImage: `linear-gradient(${T.gl} 1px, transparent 1px), linear-gradient(90deg, ${T.gl} 1px, transparent 1px)`, backgroundSize: "60px 60px", opacity: 0.35 }} />
    <Scenes data={D} map={{ A, B, C: Cc, D: Dd, E, F, G }} shell={Shell} />
    <Captions data={D} until={D.cues.G} s={{ top: 1680, size: 40, font: MONO, weight: 700, said: T.g, unsaid: "rgba(61,255,143,0.3)", activeBg: T.a, activeColor: T.bg, radius: 2, upper: true,
      plate: "linear-gradient(180deg, rgba(4,7,5,0) 0%, rgba(4,7,5,0.95) 35%)" }} />
    <Overlay />
    <Sound style="terminal" data={D} music={0.2} sfx={[...stdSfx(D, 0.12, 0.12), ["ding", "a2", 0.14]]} />
  </AbsoluteFill>
);
