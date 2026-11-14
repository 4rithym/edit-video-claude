import json, re, subprocess, sys
S=sys.argv[1]
log=subprocess.run(["ffmpeg","-i",f"{S}/src/audio.wav","-af","silencedetect=n=-35dB:d=0.35","-f","null","-"],capture_output=True,text=True).stderr
sil=[(float(a),float(b)) for a,b in re.findall(r"silence_start: ([\d.]+).*?silence_end: ([\d.]+)",log,re.S)]
DUR=86.45; PAD=0.12
# speech = complement of silences
keep=[]; t=0.6
for a,b in sil:
    if b<=0.6: continue
    if a>t: keep.append([t,min(a+PAD,DUR)])
    t=max(t,b-PAD)
if t<DUR: keep.append([t,DUR])
# merge tiny gaps
m=[]
for k in keep:
    if m and k[0]-m[-1][1]<0.08: m[-1][1]=k[1]
    else: m.append(k)
keep=[k for k in m if k[1]-k[0]>0.15]
hook=[[12.78,15.40]]
keep=[k for k in keep if not (1.9<k[0]<3.7)]
keep.insert(1,[3.05,7.39])
segs=hook+keep
json.dump({"segments":segs},open(f"{S}/src/cuts.json","w"),indent=1)
fc=[];n=len(segs)
for i,(a,b) in enumerate(segs):
    d=b-a
    fc.append(f"[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS,fps=30[v{i}];[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={d-0.03:.3f}:d=0.03[a{i}]")
fc.append("".join(f"[v{i}][a{i}]" for i in range(n))+f"concat=n={n}:v=1:a=1[v][a]")
subprocess.run(["ffmpeg","-v","error","-y","-i",f"{S}/src/raw.mp4","-filter_complex",";".join(fc),"-map","[v]","-map","[a]","-c:v","libx264","-crf","16","-preset","fast","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",f"{S}/src/cut.mp4"],check=True)
tot=sum(b-a for a,b in segs)
for a,b in segs: print(f"{a:6.2f}-{b:6.2f}")
print("total",round(tot,2))
