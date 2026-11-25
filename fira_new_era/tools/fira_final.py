# Voice + soft original ambient bed (ducked) to -14 LUFS. Usage: fira_final.py spec.json out.mp4
import json, subprocess, sys, os, re
B = os.path.dirname(os.path.abspath(__file__)); E = os.path.dirname(B) + "/fira"
spec = json.load(open(sys.argv[1])); D = f"{E}/work/{spec['id']}"; out = sys.argv[2]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{D}/overlay.mp4"], capture_output=True, text=True).stdout)
subprocess.run(["python3", "-I", f"{B}/music.py", str(dur + 0.5), f"{D}/music.wav", str(sum(map(ord, spec["id"])))], check=True)
fc = ("[0:a]aresample=48000,asplit=2[v][k];[1:a]aresample=48000,volume=-19dB[bed];"
      "[bed][k]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=600[d];[v][d]amix=inputs=2:normalize=0:duration=first[mix]")
base = ["ffmpeg", "-y", "-i", f"{D}/overlay.mp4", "-i", f"{D}/music.wav", "-filter_complex"]
r = subprocess.run(base + [fc + ";[mix]loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[a]", "-map", "[a]", "-f", "null", "-"], capture_output=True, text=True)
m = json.loads(re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr)[-1])
ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
      f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000")
subprocess.run(base[:1] + ["-v", "error"] + base[1:] + [fc + f";[mix]{ln}[a]", "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "slow",
               "-b:v", "8M", "-maxrate", "10M", "-bufsize", "16M", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
print("done", out)
