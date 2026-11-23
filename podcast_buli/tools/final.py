# Mix voice + ambient bed (ducked) + minimal SFX, loudness -14 LUFS. Usage: final.py spec.json out.mp4
import json, subprocess, sys, os, re
B = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(B) + "/work"
spec = json.load(open(sys.argv[1])); D = f"{W}/{spec['id']}"; out = sys.argv[2]
T = json.load(open(f"{D}/timing.json")); VID = T["total"]; TOTAL = VID + 2.6; hd = spec.get("hook_dur", 3.2)
seed = sum(map(ord, spec["id"]))
subprocess.run(["python3", "-I", f"{B}/music.py", str(TOTAL + 0.5), f"{D}/music.wav", str(seed)], check=True)
SFX = "/home/user/edit-video-claude/project/assets/sfx"
hook_end = T["bounds"][0][1]
fc = (f"[0:a]aresample=48000,asplit=2[voice][key];"
      f"[1:a]aresample=48000,volume=-17dB[bed];"
      f"[bed][key]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=600[duck];"
      f"[2:a]aresample=48000,volume=-16dB,adelay={int((hook_end - 0.25) * 1000)}|{int((hook_end - 0.25) * 1000)}[sw];"
      f"[voice][duck][sw]amix=inputs=3:normalize=0:duration=first[mix]")
def run(extra_af, fmt_null=False):
    args = ["ffmpeg", "-v", "info" if fmt_null else "error", "-y", "-i", f"{D}/overlay.mp4", "-i", f"{D}/music.wav",
            "-i", f"{SFX}/whoosh.wav", "-filter_complex", fc + f";[mix]{extra_af}[a]", "-map", "0:v", "-map", "[a]"]
    return args
# pass 1: measure
r = subprocess.run(run("loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", True) + ["-f", "null", "-"], capture_output=True, text=True)
m = json.loads(re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr)[-1])
ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
      f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000")
subprocess.run(run(ln) + ["-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out], check=True)
r = subprocess.run(["ffmpeg", "-i", out, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
print("done", out, re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1], "LUFS")
