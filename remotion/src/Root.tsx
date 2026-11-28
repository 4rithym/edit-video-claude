import React from "react";
import { Composition } from "remotion";
import { FPS, H, TOTAL_SEC, W } from "./theme";
import { TrojanVideo } from "./Video";
import { DURATION } from "./v6/shared";
import { V1Noir } from "./v6/V1Noir";
import { V2Swiss } from "./v6/V2Swiss";
import { V3Kinetic } from "./v6/V3Kinetic";
import { V4Terminal } from "./v6/V4Terminal";
import { V5Soft } from "./v6/V5Soft";
import { loadFonts } from "./theme";

loadFonts();

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="TrojanAwareness" component={TrojanVideo} durationInFrames={Math.ceil(TOTAL_SEC * FPS)} fps={FPS} width={W} height={H} />
    <Composition id="V1-Noir" component={V1Noir} durationInFrames={DURATION} fps={FPS} width={W} height={H} />
    <Composition id="V2-Swiss" component={V2Swiss} durationInFrames={DURATION} fps={FPS} width={W} height={H} />
    <Composition id="V3-Kinetic" component={V3Kinetic} durationInFrames={DURATION} fps={FPS} width={W} height={H} />
    <Composition id="V4-Terminal" component={V4Terminal} durationInFrames={DURATION} fps={FPS} width={W} height={H} />
    <Composition id="V5-Soft" component={V5Soft} durationInFrames={DURATION} fps={FPS} width={W} height={H} />
  </>
);
