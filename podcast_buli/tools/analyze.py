# Shot + face analysis for a source range. Usage: analyze.py src start end out.json
import cv2, json, subprocess, sys, numpy as np
src, a, b, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
W, H, FPS = 640, 360, 10
CUT = 18
p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(a), "-t", str(b - a), "-i", src, "-an",
                      "-vf", f"fps={FPS},scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
cc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
frames, prev = [], None
i = 0
while True:
    buf = p.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    im = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    sm = cv2.resize(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY), (64, 36)).astype(np.float32)
    d = 0 if prev is None else float(np.mean(np.abs(sm - prev)))
    prev = sm
    faces = cc.detectMultiScale(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY), 1.1, 5, minSize=(45, 45))
    fx = [(int((x + w / 2) * 3), int(w * 3)) for x, y, w, h in faces]
    frames.append({"t": i / FPS, "d": round(float(d), 3), "faces": fx}); i += 1
# shots: cut where hist distance spikes
cuts = [0.0] + [f["t"] for f in frames if f["d"] > CUT] + [frames[-1]["t"] + 1 / FPS]
shots = []
for s, e in zip(cuts, cuts[1:]):
    fs = [max(f["faces"], key=lambda z: z[1]) for f in frames if s <= f["t"] < e and f["faces"]]
    tot = max(1, sum(1 for f in frames if s <= f["t"] < e))
    xs = [z[0] for z in fs]; ws = [z[1] for z in fs]
    wide = (not fs) or len(fs) < 0.3 * tot or np.median(ws) < 150
    shots.append({"s": s, "e": e, "x": int(np.median(xs)) if xs else None, "n": len(xs),
                  "fw": int(np.median(ws)) if ws else 0, "wide": bool(wide)})
# fill missing x: nearest shot with similar look -> fallback to neighbour
for k, sh in enumerate(shots):
    if sh["wide"]: sh["x"] = 960
    elif sh["x"] is None:
        cand = [o["x"] for o in shots[max(0, k - 2):k + 3] if o["x"] is not None and o is not sh]
        sh["x"] = cand[-1] if cand else 960
json.dump({"start": a, "end": b, "shots": shots}, open(out, "w"), indent=1)
for sh in shots: print(f'{sh["s"]:7.1f}-{sh["e"]:7.1f}  x={sh["x"]}  n={sh["n"]} fw={sh["fw"]} wide={sh["wide"]}')

import collections

