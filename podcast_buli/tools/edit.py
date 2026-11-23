# Build a clip: tighten segments by word timing, render vertical base, cut, write timing data.
# Usage: edit.py spec.json   (spec: id, segments[[s,e]...], gap, hook_end_idx)
import json, subprocess, sys, os
B = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(B) + "/work"; SRC = os.path.dirname(B) + "/dl/source.mp4"
spec = json.load(open(sys.argv[1])); cid = spec["id"]; D = f"{W}/{cid}"; os.makedirs(D, exist_ok=True)
T = json.load(open(f"{W}/transcript.json"))
words = [w for s in T["segments"] for w in s["words"]]
GAP, PRE, POST = spec.get("gap", 0.32), 0.07, 0.12
# 1) tighten: split each requested segment into speech runs
segs = []
for k, (a, b) in enumerate(spec["segments"]):
    ws = [w for w in words if w["s"] >= a - 0.05 and w["e"] <= b + 0.05]
    drop = [x.lower() for x in spec.get("drop_words", [])]
    run = []
    for w in ws:
        if run and w["s"] - run[-1]["e"] > GAP:
            segs.append([max(a, run[0]["s"] - PRE), min(b, run[-1]["e"] + POST), k]); run = []
        run.append(w)
    if run: segs.append([max(a, run[0]["s"] - PRE), min(b, run[-1]["e"] + POST), k])
# merge overlapping
m = []
for s in segs:
    if m and s[2] == m[-1][2] and s[0] <= m[-1][1]: m[-1][1] = max(m[-1][1], s[1])
    else: m.append(s)
segs = [s for s in m if s[1] - s[0] > 0.2]
# 2) cluster nearby segments; one analysed vertical base per cluster
order = sorted(range(len(segs)), key=lambda i: segs[i][0])
clusters = []
for i in order:
    a, b, _ = segs[i]
    if clusters and a - clusters[-1][1] < 40: clusters[-1][1] = max(clusters[-1][1], b)
    else: clusters.append([a, b])
clusters = [[a - 0.5, b + 0.5] for a, b in clusters]
shots_abs = []
for ci, (lo, hi) in enumerate(clusters):
    an, base = f"{D}/an_{ci}.json", f"{D}/base_{ci}.mp4"
    if not os.path.exists(base) or spec.get("rebase"):
        subprocess.run(["python3", "-I", f"{B}/analyze.py", SRC, str(lo), str(hi), an], check=True)
        subprocess.run(["python3", "-I", f"{B}/base.py", SRC, an, base], check=True)
    for sh in json.load(open(an))["shots"]:
        shots_abs.append({**sh, "s": lo + sh["s"], "e": lo + sh["e"]})
json.dump({"start": 0, "shots": shots_abs}, open(f"{D}/an.json", "w"), indent=1)
def cl(a): return next(i for i, (lo, hi) in enumerate(clusters) if lo <= a <= hi)
# 3) cut + concat (short audio fades at joins)
fc = []
for i, (a, b, _) in enumerate(segs):
    ci = cl(a); lo = clusters[ci][0]
    a0, b0, d = a - lo, b - lo, b - a
    fc.append(f"[{ci}:v]trim={a0:.3f}:{b0:.3f},setpts=PTS-STARTPTS[v{i}];[{ci}:a]atrim={a0:.3f}:{b0:.3f},asetpts=PTS-STARTPTS,"
              f"afade=t=in:d=0.015,afade=t=out:st={d - 0.025:.3f}:d=0.025[a{i}]")
n = len(segs)
fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a]")
open(f"{D}/fc.txt", "w").write(";".join(fc))
ins = sum([["-i", f"{D}/base_{ci}.mp4"] for ci in range(len(clusters))], [])
subprocess.run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex_script", f"{D}/fc.txt", "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "256k",
                f"{D}/cut.mp4"], check=True)
# 4) remap words to new timeline
out, t = [], 0.0; bounds = []
for a, b, k in segs:
    for w in words:
        if w["s"] >= a - 0.02 and w["e"] <= b + 0.05:
            out.append({"w": w["w"].strip(), "s": round(t + max(0, w["s"] - a), 3), "e": round(t + min(b, w["e"]) - a, 3), "seg": k})
    bounds.append([round(t, 3), round(t + b - a, 3), k]); t += b - a
json.dump({"segs": segs, "bounds": bounds, "words": out, "total": round(t, 3)}, open(f"{D}/timing.json", "w"), ensure_ascii=False, indent=1)
print(cid, "segments", n, "duration", round(t, 2))
