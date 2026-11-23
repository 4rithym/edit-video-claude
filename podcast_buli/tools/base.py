# Render a vertical, graded base video for a source range using analysis json.
# Usage: base.py src analysis.json out.mp4
import json, subprocess, sys
src, an, out = sys.argv[1], json.load(open(sys.argv[2])), sys.argv[3]
a, b, shots = an["start"], an["end"], an["shots"]
CW = 608  # 9:16 crop width from 1080p
def cx(x): return max(0, min(1920 - CW, int(x - CW / 2)))
# piecewise crop x by time (t relative to range start)
expr = str(cx(shots[-1]["x"]))
for sh in reversed(shots[:-1]):
    expr = f"if(lt(t,{sh['e']:.2f}),{cx(sh['x'])},{expr})"
wide = "+".join(f"between(t,{sh['s']:.2f},{sh['e'] - 0.01:.2f})" for sh in shots if sh["wide"]) or "0"
grade = ("eq=contrast=1.07:saturation=1.06:gamma=0.98,"
         "colorbalance=rs=0.03:gs=0.0:bs=-0.03:rm=0.02:bm=-0.02,"
         "vignette=angle=PI/5")
fc = (f"[0:v]fps=30,split=3[v1][v2][v3];"
      f"[v1]crop={CW}:1080:'{expr}':0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.6[crop];"
      f"[v2]scale=-2:1920,crop=1080:1920,boxblur=40:2,eq=brightness=-0.18:saturation=0.8[bg];"
      f"[v3]scale=1080:608:flags=lanczos[fg];"
      f"[bg][fg]overlay=0:(H-h)/2-80[wide];"
      f"[crop][wide]overlay=0:0:enable='{wide}'[m];[m]{grade},format=yuv420p[v];"
      f"[0:a]highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=10:release=200:makeup=2,"
      f"aresample=48000[a]")
cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", str(b - a), "-i", src, "-filter_complex", fc,
       "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
       "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out]
subprocess.run(cmd, check=True)
print("ok", out)
