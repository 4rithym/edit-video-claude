# Mix clip audio + upbeat bed (ducked under speech) to -14 LUFS. Usage: era_final.py spec.json out.mp4
import json, subprocess, sys, os, re
B = os.path.dirname(os.path.abspath(__file__)); E = os.path.dirname(B) + "/era"
spec = json.load(open(sys.argv[1])); D = f"{E}/work/{spec['id']}"; out = sys.argv[2]
T = json.load(open(f"{D}/timing.json")); TOTAL = T["total"] + 3.2
subprocess.run(["python3", "-I", f"{B}/music_up.py", str(TOTAL + 0.3), f"{D}/music.wav", str(sum(map(ord, spec["id"])))], check=True)
fc = ("[0:a]aresample=48000,asplit=2[voice][key];[1:a]aresample=48000,volume=-9dB[bed];"
      "[bed][key]sidechaincompress=threshold=0.04:ratio=5:attack=30:release=500[duck];"
      "[voice][duck]amix=inputs=2:normalize=0:duration=first[mix]")
base = ["ffmpeg", "-y", "-i", f"{D}/overlay.mp4", "-i", f"{D}/music.wav", "-filter_complex"]
r = subprocess.run(base + [fc + ";[mix]loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[a]", "-map", "[a]", "-f", "null", "-"], capture_output=True, text=True)
m = json.loads(re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr)[-1])
ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
      f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000")
subprocess.run(base[:1] + ["-v", "error"] + base[1:] + [fc + f";[mix]{ln}[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy",
               "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out], check=True)
r = subprocess.run(["ffmpeg", "-i", out, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
print("done", out, re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1], "LUFS")
