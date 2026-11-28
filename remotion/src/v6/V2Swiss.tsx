import React from "react";
import { AbsoluteFill, useCurrentFrame, Easing, interpolate } from "remotion";
import { Captions, DATA, FILE_NAME, FPS, KEYS, MONO, SANS, SceneProps, Scenes, Sound, sp, ramp, stdSfx, useLocal, Key } from "./shared";

const D = DATA.swiss;
const P = { paper: "#EEEBE5", ink: "#111111", red: "#E3341F", rule: "#CFCAC0", mute: "#6E6A63" };

const Shell: React.FC<{ dur: number; k: Key; children: React.ReactNode }> = ({ k, children }) => {
  const f = useCurrentFrame();
  const t = f / FPS;
  if (k === "A") return <AbsoluteFill>{children}</AbsoluteFill>;
  const cover = ramp(t, 0, 0.28, Easing.in(Easing.cubic));
  const uncover = ramp(t, 0.3, 0.62, Easing.out(Easing.cubic));
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ opacity: t < 0.3 ? 0 : 1 }}>{children}</AbsoluteFill>
      <AbsoluteFill style={{ background: P.red, transform: `scaleX(${cover - uncover})`, transformOrigin: t < 0.3 ? "0% 50%" : "100% 50%" }} />
    </AbsoluteFill>
  );
};

const Mask: React.FC<{ at: number; children: React.ReactNode; style?: React.CSSProperties }> = ({ at, children, style }) => {
  const f = useCurrentFrame();
  const q = sp(f, at, 200, 22);
  return <div style={{ overflow: "hidden", ...style }}><div style={{ transform: `translateY(${(1 - q) * 110}%)` }}>{children}</div></div>;
};
const Big: React.FC<{ s?: number; c?: string; children: React.ReactNode }> = ({ s = 210, c = P.ink, children }) => (
  <div style={{ fontFamily: SANS, fontWeight: 900, fontSize: s, lineHeight: 0.9, letterSpacing: "-0.055em", color: c }}>{children}</div>
);
const Label: React.FC<{ at: number; children: React.ReactNode; c?: string }> = ({ at, children, c = P.ink }) => (
  <Mask at={at}><div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 26, letterSpacing: "0.16em", color: c }}>{children}</div></Mask>
);
const Rule: React.FC<{ at: number; top: number; w?: number; c?: string; h?: number }> = ({ at, top, w = 920, c = P.ink, h = 3 }) => {
  const f = useCurrentFrame();
  return <div style={{ position: "absolute", left: 80, top, width: w, height: h, background: c, transformOrigin: "0 50%", transform: `scaleX(${sp(f, at, 200, 24)})` }} />;
};

const A: React.FC<SceneProps> = (p) => {
  const { f, r } = useLocal(p);
  const a2 = r("a2");
  const box = sp(f, r("a1") + 0.8, 200, 24);
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 80, top: 260 }}><Label at={r("a1")} c={P.red}>● SPREADING ON WHATSAPP</Label></div>
      <div style={{ position: "absolute", left: 80, top: 340, width: 920, border: `3px solid ${P.ink}`, padding: "28px 30px", display: "flex", gap: 24, alignItems: "center",
        clipPath: `inset(0 ${(1 - box) * 100}% 0 0)` }}>
        <div style={{ background: P.ink, color: P.paper, fontFamily: MONO, fontWeight: 700, fontSize: 26, padding: "16px 14px" }}>ZIP</div>
        <div><div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 34, color: P.ink }}>{FILE_NAME}</div><div style={{ fontFamily: MONO, fontSize: 24, color: P.mute, marginTop: 6 }}>4.0 MB · RECEIVED 14:38–14:42</div></div>
      </div>
      <div style={{ position: "absolute", left: 70, top: 640 }}>
        <Mask at={a2 - 0.05}><Big>DON’T</Big></Mask>
        <Mask at={a2 + 0.08}><Big>OPEN</Big></Mask>
        <Mask at={a2 + 0.21}><Big c={P.red}>IT.</Big></Mask>
      </div>
    </AbsoluteFill>
  );
};

const TIMES = ["14:38", "14:39", "14:40", "14:40", "14:41", "14:42"];
const B: React.FC<SceneProps> = (p) => {
  const { r } = useLocal(p);
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 70, top: 230 }}>
        <Mask at={r("b1")}><Big s={190}>27.11</Big></Mask>
        <Mask at={r("b1") + 0.12}><Big s={190} c={P.red}>14:38</Big></Mask>
      </div>
      <div style={{ position: "absolute", left: 80, top: 640, width: 920 }}>
        <Mask at={r("b1") + 2.0}><div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 56, lineHeight: 1.08, letterSpacing: "-0.03em", color: P.ink }}>Harith’s WhatsApp account</div></Mask>
        <Mask at={r("b1") + 2.15}><div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 56, lineHeight: 1.08, letterSpacing: "-0.03em", color: P.red }}>was hijacked.</div></Mask>
      </div>
      <Rule at={r("b2")} top={830} />
      {TIMES.map((tm, i) => (
        <React.Fragment key={i}>
          <div style={{ position: "absolute", left: 80, top: 850 + i * 100, width: 920 }}>
            <Mask at={r("b2") + 0.3 + i * 0.55}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", height: 80 }}>
                <span style={{ fontFamily: MONO, fontWeight: 700, fontSize: 38, color: P.red }}>{tm}</span>
                <span style={{ fontFamily: SANS, fontWeight: 600, fontSize: 36, color: P.ink }}>ZIP sent to contact</span>
                <span style={{ fontFamily: MONO, fontWeight: 700, fontSize: 30, color: P.mute }}>#{String(i + 1).padStart(2, "0")}</span>
              </div>
            </Mask>
          </div>
          <Rule at={r("b2") + 0.35 + i * 0.55} top={940 + i * 100} c={P.rule} h={2} />
        </React.Fragment>
      ))}
    </AbsoluteFill>
  );
};

const Cc: React.FC<SceneProps> = (p) => {
  const { r } = useLocal(p);
  const rows = [["c1", "A formal request", "about “Finance”."], ["c2", "A ZIP file with", "a strange name."], ["c3", "From someone", "you trust."]];
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 80, top: 240 }}><Label at={0.4}>WARNING SIGNS</Label></div>
      <div style={{ position: "absolute", left: 70, top: 300 }}><Mask at={r("c0")}><Big s={150}>Watch for</Big></Mask><Mask at={r("c0") + 0.1}><Big s={150} c={P.red}>these.</Big></Mask></div>
      {rows.map(([cue, a, b], i) => (
        <React.Fragment key={cue}>
          <Rule at={r(cue)} top={680 + i * 300} />
          <div style={{ position: "absolute", left: 80, top: 710 + i * 300, width: 920, display: "flex", gap: 40 }}>
            <Mask at={r(cue) + 0.05}><div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 90, color: P.red, lineHeight: 1 }}>0{i + 1}</div></Mask>
            <div>
              <Mask at={r(cue) + 0.12}><div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 62, letterSpacing: "-0.03em", color: P.ink, lineHeight: 1.05 }}>{a}</div></Mask>
              <Mask at={r(cue) + 0.22}><div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 62, letterSpacing: "-0.03em", color: P.ink, lineHeight: 1.05 }}>{b}</div></Mask>
            </div>
          </div>
        </React.Fragment>
      ))}
    </AbsoluteFill>
  );
};

const Dd: React.FC<SceneProps> = (p) => {
  const { f, r } = useLocal(p);
  const items = [["d1", "INFECTED"], ["d2", "HIJACKED"], ["d3", "SPREADS"]];
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 80, top: 240 }}><Label at={0.3}>IF YOU OPEN IT</Label></div>
      {items.map(([cue, w], i) => {
        const on = sp(f, r(cue) + 0.2, 200, 14);
        return (
          <div key={cue} style={{ position: "absolute", left: 70, top: 330 + i * 400 }}>
            <Mask at={r(cue)}>
              <div style={{ position: "relative", display: "inline-block" }}>
                <div style={{ position: "absolute", inset: "-6px -20px", background: P.red, transformOrigin: "0 50%", transform: `scaleX(${i === 2 ? on : 0})` }} />
                <div style={{ position: "relative" }}><Big s={170} c={i === 2 ? (on > 0.5 ? P.paper : P.ink) : P.ink}>{w}</Big></div>
              </div>
            </Mask>
            {i < 2 && <Mask at={r(items[i + 1][0]) - 0.15}><div style={{ fontFamily: SANS, fontWeight: 900, fontSize: 120, color: P.red, lineHeight: 1.3, marginLeft: 10 }}>↓</div></Mask>}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

const E: React.FC<SceneProps> = (p) => {
  const { f, r } = useLocal(p);
  const tips = [["e1", "Don’t open unexpected files"], ["e2", "Call the sender to confirm"], ["e3", "Turn on two-step verification"], ["e4", "Check your linked devices"]];
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 80, top: 240 }}><Label at={0.3} c={P.red}>PROTECT YOURSELF</Label></div>
      <div style={{ position: "absolute", left: 70, top: 300 }}><Mask at={r("e0")}><Big s={150}>Four</Big></Mask><Mask at={r("e0") + 0.1}><Big s={150}>habits.</Big></Mask></div>
      {tips.map(([cue, txt], i) => {
        const chk = sp(f, r(cue) + 0.25, 200, 14);
        return (
          <React.Fragment key={cue}>
            <Rule at={r(cue)} top={690 + i * 190} c={P.rule} h={2} />
            <div style={{ position: "absolute", left: 80, top: 730 + i * 190, width: 920, display: "flex", alignItems: "center", gap: 34 }}>
              <div style={{ width: 84, height: 84, border: `4px solid ${P.ink}`, background: chk > 0.5 ? P.ink : "transparent", display: "flex", alignItems: "center", justifyContent: "center", opacity: sp(f, r(cue)) }}>
                <svg width="56" height="56" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke={P.paper} strokeWidth="3" strokeLinecap="square" strokeDasharray="22" strokeDashoffset={22 * (1 - chk)} /></svg>
              </div>
              <Mask at={r(cue) + 0.05}><div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 50, letterSpacing: "-0.025em", color: P.ink }}>{txt}</div></Mask>
            </div>
          </React.Fragment>
        );
      })}
    </AbsoluteFill>
  );
};

const F: React.FC<SceneProps> = (p) => {
  const { f, r } = useLocal(p);
  const blk = sp(f, r("f2"), 200, 22);
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 80, top: 240 }}><Label at={0.3}>ALREADY OPENED IT?</Label></div>
      <div style={{ position: "absolute", left: 70, top: 300 }}>
        <Mask at={r("f1") + 1.2}><Big s={150}>Disconnect.</Big></Mask>
        <Mask at={r("f1") + 2.0}><Big s={150}>Scan.</Big></Mask>
        <Mask at={r("f2") - 0.1}><Big s={150} c={P.red}>Report.</Big></Mask>
      </div>
      <div style={{ position: "absolute", left: 80, top: 900, width: 920, background: P.ink, color: P.paper, padding: "48px 50px", clipPath: `inset(0 ${(1 - blk) * 100}% 0 0)` }}>
        <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: "0.18em", color: "#A9A49A" }}>CYBERSECURITY MALAYSIA</div>
        <div style={{ fontFamily: SANS, fontWeight: 900, fontSize: 120, letterSpacing: "-0.05em", lineHeight: 1, marginTop: 14 }}>Cyber999</div>
        <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 58, color: P.red, marginTop: 14 }}>1-300-88-2999</div>
        <div style={{ height: 2, background: "#333", margin: "30px 0 22px" }} />
        <div style={{ fontFamily: SANS, fontWeight: 600, fontSize: 32 }}>Lost money? <span style={{ fontFamily: MONO, color: P.red }}>NSRC 997</span></div>
      </div>
    </AbsoluteFill>
  );
};

const G: React.FC<SceneProps> = (p) => {
  const { f, r } = useLocal(p);
  return (
    <AbsoluteFill style={{ background: P.red }}>
      <div style={{ position: "absolute", left: 70, top: 520 }}>
        <Mask at={r("g1")}><Big s={260} c={P.paper}>Share</Big></Mask>
        <Mask at={r("g1") + 0.12}><Big s={260} c={P.ink}>this.</Big></Mask>
      </div>
      <div style={{ position: "absolute", left: 80, top: 1060, width: 920 }}>
        <Mask at={r("g1") + 1.4}><div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 50, color: P.paper, letterSpacing: "-0.02em" }}>It could protect someone you love.</div></Mask>
        <div style={{ height: 3, background: P.paper, marginTop: 40, transformOrigin: "0 50%", transform: `scaleX(${sp(f, r("g1") + 2.2)})` }} />
        <Mask at={r("g1") + 2.6} style={{ marginTop: 26 }}><div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 38, color: P.ink }}>#DONTOPENTHEZIP</div></Mask>
      </div>
    </AbsoluteFill>
  );
};

const Frame: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const idx = KEYS.filter((k) => t >= D.cues[k]).length;
  const top = sp(f, 0.05, 200, 24);
  return (
    <>
      {[1, 2, 3, 4, 5].map((i) => <div key={i} style={{ position: "absolute", left: 80 + (920 / 6) * i, top: 0, width: 1, height: 1920, background: P.rule, opacity: 0.45 }} />)}
      <div style={{ position: "absolute", left: 80, top: 90, width: 920, display: "flex", justifyContent: "space-between", fontFamily: MONO, fontWeight: 700, fontSize: 22, letterSpacing: "0.16em", color: t >= D.cues.G ? P.paper : P.ink, opacity: top }}>
        <span>PUBLIC NOTICE — CYBER SAFETY</span><span>Nº {String(idx).padStart(2, "0")} / 07</span>
      </div>
      <div style={{ position: "absolute", left: 80, top: 136, width: 920, height: 3, background: t >= D.cues.G ? P.paper : P.ink, transformOrigin: "0 50%", transform: `scaleX(${top})` }} />
      <div style={{ position: "absolute", left: 80, top: 136, width: 920 * (t / 60), height: 3, background: P.red }} />
    </>
  );
};

export const V2Swiss: React.FC = () => (
  <AbsoluteFill style={{ background: P.paper }}>
    <Scenes data={D} map={{ A, B, C: Cc, D: Dd, E, F, G }} shell={Shell} />
    <Frame />
    <Captions data={D} until={D.cues.G} s={{ top: 1700, size: 44, weight: 700, said: P.ink, unsaid: "rgba(17,17,17,0.3)", activeBg: P.ink, activeColor: P.paper, radius: 0,
      plate: `linear-gradient(180deg, rgba(238,235,229,0) 0%, ${P.paper} 30%)` }} />
    <Sound style="swiss" data={D} music={0.24} sfx={[...stdSfx(D, 0.16, 0.1), ["ding", "g1", 0.12]]} />
  </AbsoluteFill>
);
