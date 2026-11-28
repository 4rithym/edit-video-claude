import React from "react";
import { Composition } from "remotion";
import { FPS, H, TOTAL_SEC, W } from "./theme";
import { TrojanVideo } from "./Video";

export const RemotionRoot: React.FC = () => (
  <Composition id="TrojanAwareness" component={TrojanVideo} durationInFrames={Math.ceil(TOTAL_SEC * FPS)} fps={FPS} width={W} height={H} />
);
