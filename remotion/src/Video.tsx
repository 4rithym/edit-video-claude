import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile } from "remotion";
import { CUES, FPS, SCENES, SceneKey, sceneEnd, loadFonts } from "./theme";
import { Background, Captions, Header, SceneShell } from "./components";
import { SceneA, SceneB, SceneC, SceneD, SceneE, SceneF, SceneG, SceneH } from "./scenes";

loadFonts();

const MAP: Record<SceneKey, React.FC> = { A: SceneA, B: SceneB, C: SceneC, D: SceneD, E: SceneE, F: SceneF, G: SceneG, H: SceneH };
const fr = (s: number) => Math.round(s * FPS);

const SFX: [string, number, number][] = [
  ["pop", 1.9, 0.18],
  ["pop", CUES.a1 + 2.9, 0.18],
  ["ding", CUES.a2 + 0.9, 0.16],
  ...(["B", "C", "D", "E", "F", "G", "H"] as SceneKey[]).map((k) => ["whoosh", CUES[k] - 0.2, 0.14] as [string, number, number]),
  ...[0, 1, 2, 3, 4, 5].map((i) => ["click", CUES.b2 + 0.35 + i * 0.72, 0.14] as [string, number, number]),
  ...["d1", "d2", "d3", "d4", "e2", "e3", "e4", "f1", "f2", "f3", "f4", "f5", "g1", "g2", "g3", "g4"].map((c) => ["click", CUES[c], 0.12] as [string, number, number]),
  ["ding", CUES.g5 + 0.3, 0.12],
  ["ding", CUES.h1 + 3.2, 0.14],
];

export const TrojanVideo: React.FC = () => (
  <AbsoluteFill>
    <Background />
    {SCENES.map((k) => {
      const Comp = MAP[k];
      const dur = sceneEnd(k) - CUES[k];
      return (
        <Sequence key={k} from={fr(CUES[k])} durationInFrames={fr(dur)} name={`Scene ${k}`}>
          <SceneShell dur={dur}><Comp /></SceneShell>
        </Sequence>
      );
    })}
    <Header />
    <Captions />
    <Audio src={staticFile("vo.wav")} />
    <Audio src={staticFile("music.wav")} volume={0.2} />
    {SFX.map(([n, t, v], i) => (
      <Sequence key={`sfx${i}`} from={fr(Math.max(0, t))} durationInFrames={fr(1.4)} name={`sfx-${n}`}>
        <Audio src={staticFile(`${n}.wav`)} volume={v} />
      </Sequence>
    ))}
  </AbsoluteFill>
);
