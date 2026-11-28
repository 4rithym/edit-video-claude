import { continueRender, delayRender, spring, staticFile } from "remotion";
import cuesJson from "./cues.json";

export const FPS = 30;
export const W = 1080;
export const H = 1920;

type Word = { w: string; s: number; e: number };
type Line = { cue: string; t: number; d: number; text: string; words: Word[] };
export const CUES = cuesJson.cues as Record<string, number>;
export const LINES = cuesJson.lines as Line[];
export const TOTAL_SEC = CUES.end;
export const SCENES = ["A", "B", "C", "D", "E", "F", "G", "H"] as const;
export type SceneKey = (typeof SCENES)[number];
export const sceneEnd = (k: SceneKey) => {
  const i = SCENES.indexOf(k);
  return i + 1 < SCENES.length ? CUES[SCENES[i + 1]] : TOTAL_SEC;
};
export const CHAPTERS: SceneKey[] = ["B", "C", "D", "E", "F", "G"];

export const C = {
  bg: "#06070A",
  panel: "rgba(22,25,31,0.78)",
  panelSolid: "#15181E",
  line: "rgba(255,255,255,0.09)",
  text: "#F5F6F8",
  muted: "#8E97A6",
  dim: "#5A6270",
  red: "#FF4D57",
  redSoft: "rgba(255,77,87,0.14)",
  amber: "#FFB224",
  green: "#3DD68C",
  waBg: "#0B141A",
  waHead: "#1F2C34",
  waIn: "#1F2C34",
  waFile: "#16232B",
};
export const SANS = "'Inter Display', sans-serif";
export const MONO = "'JetBrains Mono', monospace";

export const FILE_NAME = "20261127134525.CC28C3AC.zip";
export const SCAM_MSG = [
  "Sila forward statement of account di atas kepada bahagian Finance / Cashier syarikat anda.",
  "Sila ambil perhatian: Jika anda bukan kakitangan bahagian Finance, sila serahkan dokumen tersebut kepada pihak Finance untuk semakan.",
  "Terima kasih atas kerjasama anda.",
];

/** spring that starts at `atSec` (relative to the current Sequence) */
export const sp = (frame: number, atSec: number, damping = 200, durationInFrames?: number) =>
  spring({ frame: frame - atSec * FPS, fps: FPS, config: { damping, mass: 0.9 }, durationInFrames });

const FONTS: [string, string, string][] = [
  ["Inter Display", "InterDisplay-Medium.otf", "500"],
  ["Inter Display", "InterDisplay-SemiBold.otf", "600"],
  ["Inter Display", "InterDisplay-Bold.otf", "700"],
  ["Inter Display", "InterDisplay-ExtraBold.otf", "800"],
  ["Inter Display", "InterDisplay-Black.otf", "900"],
  ["JetBrains Mono", "JetBrainsMono-Medium.ttf", "500"],
  ["JetBrains Mono", "JetBrainsMono-Bold.ttf", "700"],
];
let fontsRequested = false;
export const loadFonts = () => {
  if (fontsRequested || typeof document === "undefined") return;
  fontsRequested = true;
  const handle = delayRender("Loading fonts");
  Promise.all(
    FONTS.map(([family, file, weight]) =>
      new FontFace(family, `url(${staticFile(`fonts/${file}`)})`, { weight }).load().then((f) => {
        document.fonts.add(f);
      }),
    ),
  )
    .then(() => continueRender(handle))
    .catch((e) => {
      console.error(e);
      continueRender(handle);
    });
};
