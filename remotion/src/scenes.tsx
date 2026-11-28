import React from "react";
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, Easing } from "remotion";
import { Ban, Bug, FileText, FileX2, KeyRound, Laptop, Lock, Megaphone, PhoneCall, ScanSearch, ShieldCheck, TriangleAlert, UserX, Users, WifiOff, MessageCircle, Paperclip } from "lucide-react";
import { C, CUES, FILE_NAME, FPS, MONO, SANS, sp } from "./theme";
import { Chapter, Glass, Kicker, Phone, Reveal, rel } from "./components";

const T = (f: number) => f / FPS;

/* ================= A — Hook ================= */
export const SceneA: React.FC = () => {
  const f = useCurrentFrame();
  const a1 = rel("a1", "A"), a2 = rel("a2", "A");
  const enter = sp(f, 0.15, 18);
  const zoom = sp(f, a2 - 0.1, 200, 40);
  const headOut = sp(f, a2 - 0.25, 200, 10);
  const rotY = interpolate(enter, [0, 1], [-28, -10]) * (1 - zoom);
  const chip = sp(f, a2 + 0.9, 13);
  const redWash = interpolate(T(f), [a2 + 0.8, a2 + 1.0, a2 + 1.6], [0, 0.22, 0.08], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 55%, rgba(255,77,87,${redWash}) 0%, transparent 60%)` }} />
      <div style={{ position: "absolute", left: 80, top: 210, width: 920, opacity: 1 - headOut, transform: `translateY(${-headOut * 40}px)` }}>
        <Kicker at={0.2}><TriangleAlert size={30} strokeWidth={2.6} /> DON'T OPEN THIS FILE</Kicker>
        <Reveal text="It looks like a normal message." at={a1 + 0.1} size={74} accent={["normal"]} style={{ marginTop: 18 }} />
        <Reveal text="From a friend's number." at={a1 + 2.4} size={44} weight={600} color={C.muted} style={{ marginTop: 16 }} />
      </div>
      <div style={{ position: "absolute", left: 220, top: 520, perspective: 2200 }}>
        <div style={{ transformOrigin: "50% 66%", transform: `translateY(${(1 - enter) * 700 - zoom * 290}px) rotateY(${rotY}deg) rotateX(${4 * (1 - zoom)}deg) scale(${1 + zoom * 0.2})` }}>
          <Phone showTypingFrom={0.9} showMsgAt={1.9} showFileAt={a1 + 2.9} dangerAt={a2 + 0.85} />
        </div>
      </div>
      <div style={{ position: "absolute", left: 470, top: 1235, opacity: chip, transform: `scale(${0.6 + 0.4 * chip}) rotate(${(1 - chip) * -8}deg)`, transformOrigin: "0 50%",
        display: "flex", alignItems: "center", gap: 12, padding: "18px 28px", borderRadius: 18, background: C.red, color: "#fff", fontFamily: MONO, fontWeight: 700, fontSize: 32, letterSpacing: "0.08em",
        boxShadow: "0 24px 60px rgba(255,77,87,0.55)" }}>
        <Ban size={34} strokeWidth={2.6} /> DO NOT OPEN
      </div>
    </AbsoluteFill>
  );
};

/* ================= B — What happened ================= */
const ARRIVALS = ["14:38", "14:39", "14:40", "14:40", "14:41", "14:42"];
export const SceneB: React.FC = () => {
  const f = useCurrentFrame();
  const b1 = rel("b1", "B"), b2 = rel("b2", "B");
  const at = ARRIVALS.map((_, i) => b2 + 0.35 + i * 0.72);
  const arrived = at.filter((x) => T(f) >= x).length;
  const clock = arrived ? ARRIVALS[arrived - 1] : "14:38";
  const dateP = sp(f, b1 + 0.2);
  const fill = interpolate(T(f), [at[0], at[5]], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill>
      <Chapter num="01" title="What happened" />
      <div style={{ position: "absolute", left: 80, top: 440, width: 920, opacity: dateP, transform: `translateY(${(1 - dateP) * 30}px)` }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: 26 }}>
          <span style={{ fontFamily: MONO, fontWeight: 700, fontSize: 92, letterSpacing: "-0.03em", color: C.text }}>27.11.2026</span>
          <span style={{ fontFamily: MONO, fontWeight: 700, fontSize: 58, color: C.red, textShadow: "0 0 30px rgba(255,77,87,0.5)" }}>{clock}</span>
        </div>
      </div>
      <Reveal text="Harith's WhatsApp account was taken over." at={b1 + 4.2} size={52} weight={700} accent={["taken", "over"]} style={{ position: "absolute", left: 80, top: 575, width: 920, lineHeight: 1.15 }} />
      <div style={{ position: "absolute", left: 80, top: 760, width: 920, height: 820 }}>
        {ARRIVALS.map((tm, i) => {
          if (T(f) < at[i] - 0.05) return null;
          const p = sp(f, at[i], 16);
          let y = 0;
          for (let j = i + 1; j < at.length; j++) y += sp(f, at[j], 18) * 128;
          return (
            <div key={i} style={{ position: "absolute", left: 0, top: 0, width: 920, transform: `translateY(${y + (1 - p) * -80}px) scale(${0.94 + 0.06 * p})`, opacity: Math.min(1, p * 1.4) * (y > 640 ? 0 : 1) }}>
              <Glass style={{ height: 112, borderRadius: 30, display: "flex", alignItems: "center", gap: 22, padding: "0 28px" }}>
                <div style={{ width: 62, height: 62, borderRadius: 16, background: "linear-gradient(135deg,#3DD68C,#1F9D63)", display: "flex", alignItems: "center", justifyContent: "center" }}>
                  <MessageCircle size={34} color="#fff" strokeWidth={2.4} />
                </div>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", fontFamily: SANS, fontWeight: 700, fontSize: 28, color: C.text }}>
                    <span>Harith</span><span style={{ fontFamily: MONO, fontWeight: 500, fontSize: 24, color: C.muted }}>{tm}</span>
                  </div>
                  <div style={{ display: "flex", alignItems: "center", gap: 8, marginTop: 6, fontFamily: MONO, fontSize: 23, color: "#C8CED8" }}>
                    <Paperclip size={22} /> {FILE_NAME}
                  </div>
                </div>
              </Glass>
            </div>
          );
        })}
      </div>
      <div style={{ position: "absolute", left: 80, top: 1560, width: 920, opacity: sp(f, b2 + 0.2) }}>
        <div style={{ height: 6, borderRadius: 3, background: "rgba(255,255,255,0.1)" }}>
          <div style={{ width: `${fill * 100}%`, height: "100%", borderRadius: 3, background: C.red, boxShadow: "0 0 16px rgba(255,77,87,0.7)" }} />
        </div>
        <div style={{ display: "flex", justifyContent: "space-between", marginTop: 14, fontFamily: MONO, fontWeight: 700, fontSize: 24, color: C.muted }}>
          <span>14:38</span><span style={{ color: C.text, fontFamily: SANS, fontSize: 28 }}>≈ 4 minutes · {arrived} recipients shown</span><span>14:42</span>
        </div>
      </div>
    </AbsoluteFill>
  );
};

/* ================= C — Evidence ================= */
const EV = [["z5", "14:38", "A"], ["z1", "14:40", "B"], ["z3", "14:40", "C"], ["z2", "14:42", "D"], ["z6", "14:42", "E"]];
export const SceneC: React.FC = () => {
  const f = useCurrentFrame();
  const c1 = rel("c1", "C");
  return (
    <AbsoluteFill>
      <Chapter num="02" title="Real evidence" />
      <div style={{ position: "absolute", left: 80, top: 430, width: 920 }}>
        {EV.map(([z, tm, who], i) => {
          const p = sp(f, c1 + 0.2 + i * 0.45, 16);
          const drift = T(f) * 3;
          return (
            <div key={z} style={{ position: "absolute", left: 0, top: i * 200, width: 920, opacity: Math.min(1, p * 1.3),
              transform: `translateX(${(1 - p) * 300}px) rotate(${(i % 2 ? 1 : -1) * (1.2 + (1 - p) * 4)}deg) translateY(${-drift}px)` }}>
              <Glass style={{ padding: "14px 18px 16px", borderRadius: 24 }}>
                <div style={{ display: "flex", justifyContent: "space-between", fontFamily: MONO, fontWeight: 700, fontSize: 22, letterSpacing: "0.08em", color: C.muted, marginBottom: 10 }}>
                  <span>RECIPIENT {who}</span><span style={{ color: C.red }}>{tm}</span>
                </div>
                <div style={{ height: 118, display: "flex", alignItems: "center" }}>
                  <Img src={staticFile(`ev/${z}.png`)} style={{ maxHeight: 118, maxWidth: 884, borderRadius: 10 }} />
                </div>
              </Glass>
            </div>
          );
        })}
      </div>
      <div style={{ position: "absolute", left: 80, top: 1450, width: 920, fontFamily: SANS, fontWeight: 500, fontSize: 28, color: C.muted, opacity: sp(f, c1 + 3.2) }}>
        Recipients' screenshots. Names and photos hidden for privacy.
      </div>
    </AbsoluteFill>
  );
};

/* ================= D — Warning signs ================= */
const FLAGS: { cue: string; title: string; body: React.ReactNode; target: "msg" | "file" | "head" | "ar" }[] = [
  { cue: "d1", title: "A formal “Finance” request", body: "Doesn't sound like your friend at all.", target: "msg" },
  { cue: "d2", title: "A strangely named ZIP file", body: <><span style={{ fontFamily: MONO, fontSize: 27, color: C.text }}>{FILE_NAME}</span><br />No explanation given.</>, target: "file" },
  { cue: "d3", title: "From a number you trust", body: "That's exactly why it works.", target: "head" },
  { cue: "d4", title: "The auto-reply still works", body: "The real account was hijacked — it's not a fake number.", target: "ar" },
];
export const SceneD: React.FC = () => {
  const f = useCurrentFrame();
  const t = T(f);
  const ends = FLAGS.map((x, i) => (i + 1 < FLAGS.length ? rel(FLAGS[i + 1].cue, "D") : 99));
  const highlight = FLAGS.map((x, i) => ({ target: x.target, from: rel(x.cue, "D") + (x.target === "ar" ? 1.1 : 0.3), to: ends[i] }));
  const ph = sp(f, 0.3, 20);
  return (
    <AbsoluteFill>
      <Chapter num="03" title="Warning signs" />
      <div style={{ position: "absolute", left: 220, top: 380, transform: `translateY(${(1 - ph) * 200}px) scale(0.64)`, transformOrigin: "50% 0", opacity: ph }}>
        <Phone showMsgAt={-1} showFileAt={-1} showAutoReplyAt={rel("d4", "D") + 1.0} highlight={highlight} />
      </div>
      {FLAGS.map((x, i) => {
        const s = rel(x.cue, "D");
        if (t < s - 0.05 || t > ends[i]) return null;
        const p = sp(f, s, 18);
        const out = ends[i] < 90 ? interpolate(t, [ends[i] - 0.3, ends[i]], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 0;
        return (
          <div key={i} style={{ position: "absolute", left: 80, top: 1150, width: 920, opacity: p * (1 - out), transform: `translateY(${(1 - p) * 60 - out * 30}px)` }}>
            <Glass accent={C.amber} style={{ padding: "34px 40px" }}>
              <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: "0.14em", color: C.amber }}>SIGN {i + 1} / 4</div>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 54, lineHeight: 1.08, letterSpacing: "-0.02em", color: C.text, marginTop: 12 }}>{x.title}</div>
              <div style={{ fontFamily: SANS, fontWeight: 500, fontSize: 32, lineHeight: 1.35, color: "#C8CED8", marginTop: 14 }}>{x.body}</div>
            </Glass>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

/* ================= E — Why dangerous ================= */
const CHAIN = [
  { cue: "e2", Icon: Bug, title: "Device infected", sub: "Malware gets installed" },
  { cue: "e3", Icon: UserX, title: "Account taken over", sub: "Attackers use your account" },
  { cue: "e4", Icon: Users, title: "Spreads to your contacts", sub: "And the cycle repeats" },
];
export const SceneE: React.FC = () => {
  const f = useCurrentFrame();
  const t = T(f);
  const e1 = rel("e1", "E");
  const card = sp(f, e1, 18);
  const ext = ".exe";
  const typed = Math.floor(interpolate(t, [e1 + 1.6, e1 + 2.1], [0, ext.length], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  const lineP = interpolate(t, [rel("e2", "E"), rel("e4", "E") + 0.3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) });
  return (
    <AbsoluteFill>
      <Chapter num="04" title="Why it's dangerous" />
      <div style={{ position: "absolute", left: 80, top: 430, width: 920, opacity: card, transform: `translateY(${(1 - card) * 40}px)` }}>
        <Glass style={{ padding: "34px 38px", display: "flex", alignItems: "center", gap: 30 }}>
          <div style={{ width: 100, height: 100, borderRadius: 24, background: typed ? "rgba(255,77,87,0.16)" : "rgba(255,255,255,0.06)", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <FileText size={56} color={typed ? C.red : C.text} strokeWidth={1.8} />
          </div>
          <div>
            <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 40, color: C.text }}>
              Statement_of_Account.pdf<span style={{ color: C.red }}>{ext.slice(0, typed)}</span>
            </div>
            <div style={{ fontFamily: SANS, fontWeight: 500, fontSize: 27, color: C.muted, marginTop: 10, opacity: sp(f, e1 + 2.0) }}>Example: the real file type can be hidden</div>
          </div>
        </Glass>
      </div>
      <div style={{ position: "absolute", left: 80, top: 760, width: 920, height: 700 }}>
        <div style={{ position: "absolute", left: 58, top: 110, width: 4, height: 420, background: "rgba(255,255,255,0.08)" }} />
        <div style={{ position: "absolute", left: 58, top: 110, width: 4, height: 420 * lineP, background: C.red, boxShadow: "0 0 14px rgba(255,77,87,0.8)" }} />
        {CHAIN.map(({ cue, Icon, title, sub }, i) => {
          const s = rel(cue, "E");
          const p = sp(f, s, 16);
          const lit = t >= s + 0.15;
          return (
            <div key={cue} style={{ position: "absolute", left: 0, top: i * 210, display: "flex", alignItems: "center", gap: 34, opacity: Math.max(0.25, p), transform: `translateX(${(1 - p) * -40}px)` }}>
              <div style={{ width: 120, height: 120, borderRadius: 32, background: lit ? "rgba(255,77,87,0.16)" : C.panelSolid, border: `2px solid ${lit ? C.red : C.line}`,
                display: "flex", alignItems: "center", justifyContent: "center", boxShadow: lit ? "0 0 40px rgba(255,77,87,0.35)" : "none" }}>
                <Icon size={56} color={lit ? C.red : C.muted} strokeWidth={1.9} />
              </div>
              <div>
                <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 50, letterSpacing: "-0.02em", color: C.text }}>{title}</div>
                <div style={{ fontFamily: SANS, fontWeight: 500, fontSize: 28, color: C.muted, marginTop: 6 }}>{sub}</div>
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

/* ================= F — Protect yourself ================= */
const TIPS = [
  { cue: "f1", Icon: FileX2, title: "Never open unexpected ZIP / APK files", sub: "Even if they come from friends" },
  { cue: "f2", Icon: PhoneCall, title: "Call the sender to confirm", sub: "Use a phone call, not a message" },
  { cue: "f3", Icon: Lock, title: "Turn on two-step verification", sub: "Settings › Account › Two-step verification" },
  { cue: "f4", Icon: Laptop, title: "Check your linked devices", sub: "Settings › Linked devices › Log out" },
  { cue: "f5", Icon: KeyRound, title: "Never share your 6-digit code", sub: "Your WhatsApp verification code" },
];
export const SceneF: React.FC = () => {
  const f = useCurrentFrame();
  const t = T(f);
  const endAll = CUES.G - CUES.F - 1.6;
  return (
    <AbsoluteFill>
      <Chapter num="05" title="Protect yourself" />
      {TIPS.map(({ cue, Icon, title, sub }, i) => {
        const s = rel(cue, "F");
        const p = sp(f, s, 18);
        const next = i + 1 < TIPS.length ? rel(TIPS[i + 1].cue, "F") : 99;
        const active = t >= s && (t < next || t >= endAll);
        const dimmed = t >= next && t < endAll;
        return (
          <div key={cue} style={{ position: "absolute", left: 80, top: 430 + i * 214, width: 920, opacity: p * (dimmed ? 0.42 : 1), transform: `translateY(${(1 - p) * 50}px) scale(${active ? 1 : 0.985})` }}>
            <Glass style={{ padding: "26px 32px", display: "flex", alignItems: "center", gap: 28, borderColor: active ? "rgba(61,214,140,0.55)" : C.line,
              boxShadow: active ? "0 0 50px rgba(61,214,140,0.14), 0 30px 60px rgba(0,0,0,0.35)" : undefined }}>
              <div style={{ width: 88, height: 88, borderRadius: 24, background: "rgba(61,214,140,0.12)", display: "flex", alignItems: "center", justifyContent: "center", flex: "none" }}>
                <Icon size={46} color={C.green} strokeWidth={2} />
              </div>
              <div>
                <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 38, lineHeight: 1.15, letterSpacing: "-0.01em", color: C.text }}>{title}</div>
                <div style={{ fontFamily: MONO, fontWeight: 500, fontSize: 23, color: C.muted, marginTop: 8 }}>{sub}</div>
              </div>
            </Glass>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

/* ================= G — Already opened ================= */
const STEPS = [
  { cue: "g1", Icon: WifiOff, text: "Disconnect from the internet" },
  { cue: "g2", Icon: ScanSearch, text: "Scan your device with antivirus" },
  { cue: "g3", Icon: KeyRound, text: "Change passwords from another device" },
  { cue: "g4", Icon: Megaphone, text: "Warn your contacts" },
];
export const SceneG: React.FC = () => {
  const f = useCurrentFrame();
  const g5 = rel("g5", "G");
  const cards = [
    { at: g5 + 0.3, k: "CYBER INCIDENT", n: "Cyber999", p: "1-300-88-2999", d: "CyberSecurity Malaysia" },
    { at: g5 + 3.1, k: "LOST MONEY", n: "NSRC", p: "997", d: "National Scam Response Centre" },
  ];
  return (
    <AbsoluteFill>
      <Chapter num="06" title="Already opened it?" />
      {STEPS.map(({ cue, Icon, text }, i) => {
        const p = sp(f, rel(cue, "G"), 18);
        return (
          <div key={cue} style={{ position: "absolute", left: 80, top: 430 + i * 118, width: 920, display: "flex", alignItems: "center", gap: 26, padding: "20px 0",
            borderBottom: `1px solid ${C.line}`, opacity: p, transform: `translateX(${(1 - p) * -40}px)` }}>
            <span style={{ fontFamily: MONO, fontWeight: 700, fontSize: 28, color: C.red, width: 50 }}>{String(i + 1).padStart(2, "0")}</span>
            <Icon size={40} color={C.text} strokeWidth={1.9} />
            <span style={{ fontFamily: SANS, fontWeight: 600, fontSize: 40, letterSpacing: "-0.01em", color: C.text }}>{text}</span>
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 80, top: 960, fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: "0.18em", color: C.muted, opacity: sp(f, g5) }}>REPORT IT</div>
      <div style={{ position: "absolute", left: 80, top: 1020, width: 920, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
        {cards.map((c) => {
          const p = sp(f, c.at, 16);
          return (
            <div key={c.n} style={{ background: C.text, color: "#0B0D10", borderRadius: 30, padding: "30px 32px", opacity: p, transform: `translateY(${(1 - p) * 60}px)`, boxShadow: "0 30px 60px rgba(0,0,0,0.4)" }}>
              <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 20, letterSpacing: "0.14em", color: "#5A6270" }}>{c.k}</div>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 46, letterSpacing: "-0.02em", marginTop: 10 }}>{c.n}</div>
              <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 38, color: "#D92D37", marginTop: 6 }}>{c.p}</div>
              <div style={{ fontFamily: SANS, fontWeight: 500, fontSize: 23, color: "#5A6270", marginTop: 8 }}>{c.d}</div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

/* ================= H — Close ================= */
export const SceneH: React.FC = () => {
  const f = useCurrentFrame();
  const t = T(f);
  const h1 = rel("h1", "H");
  const sh = sp(f, 0.1, 12);
  return (
    <AbsoluteFill style={{ alignItems: "center" }}>
      <div style={{ position: "absolute", top: 470, left: 0, width: 1080, display: "flex", justifyContent: "center" }}>
        <div style={{ position: "relative", width: 200, height: 200, display: "flex", alignItems: "center", justifyContent: "center" }}>
          {[0, 1, 2].map((i) => {
            const ph = ((t - 0.3 + i * 0.8) % 2.4) / 2.4;
            return t > 0.3 ? <div key={i} style={{ position: "absolute", width: 200, height: 200, borderRadius: "50%", border: `2px solid ${C.green}`, opacity: (1 - ph) * 0.5, transform: `scale(${1 + ph * 1.4})` }} /> : null;
          })}
          <div style={{ transform: `scale(${sh})` }}><ShieldCheck size={170} color={C.green} strokeWidth={1.5} /></div>
        </div>
      </div>
      <div style={{ position: "absolute", top: 780, left: 80, width: 920, textAlign: "center" }}>
        <Reveal text="Share this video." at={h1} size={110} weight={900} style={{ textAlign: "center" }} />
        <Reveal text="One share could protect your friends and family." at={h1 + 1.6} size={40} weight={500} color="#C8CED8" stagger={0.04} style={{ textAlign: "center", marginTop: 30, lineHeight: 1.3 }} />
        <div style={{ display: "inline-block", marginTop: 50, padding: "16px 32px", borderRadius: 16, border: `2px solid ${C.red}`, color: C.red, fontFamily: MONO, fontWeight: 700, fontSize: 38,
          opacity: sp(f, h1 + 3.2), transform: `scale(${0.9 + 0.1 * sp(f, h1 + 3.2, 12)})` }}>#DontOpenTheZIP</div>
      </div>
      <div style={{ position: "absolute", top: 1560, left: 80, width: 920, textAlign: "center", fontFamily: SANS, fontWeight: 500, fontSize: 24, color: C.dim, opacity: sp(f, h1 + 4) }}>
        General cyber-safety information. Verify hotline numbers on official agency websites.
      </div>
    </AbsoluteFill>
  );
};
