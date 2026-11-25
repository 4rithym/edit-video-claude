# Multi-source vertical montage: each shot cropped/graded to 1080x1920@30, concatenated, words remapped.
# Usage: montage.py spec.json
import json, subprocess, sys, os, re
B = os.path.dirname(os.path.abspath(__file__)); E = os.path.dirname(B) + "/era"
spec = json.load(open(sys.argv[1])); D = f"{E}/work/{spec['id']}"; os.makedirs(D, exist_ok=True)
T = json.load(open(f"{E}/transcripts.json"))
GRADE = "eq=contrast=1.06:saturation=1.14:gamma=0.98,colorbalance=bs=0.02:bm=0.01"
def probe(f):
    o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:stream_side_data=rotation",
                        "-of", "json", f], capture_output=True, text=True).stdout
    s = json.loads(o)["streams"][0]; w, h = s["width"], s["height"]
    rot = next((abs(int(d.get("rotation", 0))) for d in s.get("side_data_list", []) if "rotation" in d), 0)
    return (h, w) if rot in (90, 270) else (w, h)
parts, words, bounds, t = [], [], [], 0.0
for i, sh in enumerate(spec["shots"]):
    src = f"{E}/src/{sh['src']}.mp4"; a, b = sh["a"], sh["b"]; d = b - a
    vs = sh.get("vsrc"); vfile = f"{E}/src/{vs['src']}.mp4" if vs else src
    w, h = probe(vfile)
    if vs: sh = {**sh, **{k: v for k, v in vs.items() if k in ("x", "y", "zoom")}}
    z = sh.get("zoom", 1.0)
    if w > h:  # landscape -> 9:16 window at horizontal position x (0..1)
        cw = int(h * 9 / 16 / z) // 2 * 2; ch = int(h / z) // 2 * 2; x = sh.get("x", 0.5)
        y = sh.get("y", 0.5)
        vf = f"crop={cw}:{ch}:{int((w - cw) * x)}:{int((h - ch) * y)}"
    else:
        cw = int(w / z) // 2 * 2; ch = int(h / z) // 2 * 2
        vf = f"crop={cw}:{ch}:{int((w - cw) * sh.get('x', 0.5))}:{int((h - ch) * sh.get('y', 0.5))}"
    vf += f",scale=1080:1920:flags=lanczos,fps=30,{GRADE},format=yuv420p"
    vol = sh.get("vol", 1.0)
    af = (f"highpass=f=80,volume={vol},aresample=48000,aformat=channel_layouts=stereo,"
          f"afade=t=in:d=0.02,afade=t=out:st={d - 0.03:.3f}:d=0.03")
    out = f"{D}/s{i:02d}.mp4"
    vin = ["-ss", str(vs["a"]), "-t", f"{d:.3f}", "-i", vfile] if vs else []
    maps = ["-map", "1:v:0", "-map", "0:a:0"] if vs else []
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", f"{d:.3f}", "-i", src] + vin + maps + ["-vf", vf, "-af", af,
                    "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-shortest", out], check=True)
    parts.append(out)
    if sh.get("cap", True):
        for s in T.get(sh["src"], []):
            for wd in s["words"]:
                if wd["s"] >= a - 0.05 and wd["e"] <= b + 0.1 and re.sub(r"[^\w]", "", wd["w"]).lower() not in sh.get("drop", []):
                    words.append({"w": wd["w"].strip(), "shot": i, "s": round(t + max(0, wd["s"] - a), 3), "e": round(t + min(b, wd["e"]) - a, 3)})
    bounds.append({"s": round(t, 3), "e": round(t + d, 3), **{k: sh[k] for k in ("chapter", "tag", "sfx", "src") if k in sh}})
    t += d
open(f"{D}/list.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{D}/list.txt",
                "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-c:a", "aac", "-b:a", "256k", f"{D}/cut.mp4"], check=True)
json.dump({"words": words, "bounds": bounds, "total": round(t, 3)}, open(f"{D}/timing.json", "w"), ensure_ascii=False, indent=1)
print(spec["id"], "shots", len(parts), "duration", round(t, 2), "words", len(words))
