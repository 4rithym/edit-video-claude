import json, sys, html
S=sys.argv[1]; P=f"{S}/hf/zakat"
segs=json.load(open(f"{S}/src/cuts.json"))["segments"]
VID=sum(b-a for a,b in segs)
END_CARD=2.2
TOTAL=round(VID+END_CARD,2)
# cumulative offsets
offs=[];c=0
for a,b in segs: offs.append(c); c+=b-a
def m(t, hook=False):
    rng=range(0,1) if hook else range(1,len(segs))
    best=None
    for i in rng:
        a,b=segs[i]
        if a<=t<=b: return offs[i]+t-a
        # nearest
        d=min(abs(t-a),abs(t-b)); 
        if best is None or d<best[0]: best=(d, offs[i]+(0 if t<a else b-a))
    return best[1]
tr=json.load(open(f"{S}/src/transcript.json"))
W=[]
for s in tr["segments"]:
    for j,w in enumerate(s["words"]): W.append({"w":w["w"].strip(),"s":w["s"],"e":w["e"],"f":j==0})
# fixes keyed by rounded start
fix={38.46:"log in,",37.54:"zakat,",40.16:"pengguna",40.90:"daftar",43.92:"bayar",26.94:"bayar",49.44:"lain-lain"}
drop={38.78,37.84,48.86,49.06,49.68,86.36,86.66}
words=[]
for w in W:
    k=round(w["s"],2)
    if k in drop: continue
    t=fix.get(k,w["w"])
    if t.startswith("KL") and words and words[-1]["w"]=="Uni":
        words[-1]["w"]="UniKL"+t[2:]; words[-1]["e"]=w["e"]; continue
    words.append({"w":t,"s":w["s"],"e":w["e"],"f":w["f"]})
# Whisper stretches first word of a segment; clamp word length
for w in words:
    if w["e"]-w["s"]>0.6: w["s"]=w["e"]-0.45
KEY={"zakat","unikl","mohon","bantuan","bayar","daftar","bertuah","12","student","website","platform","bulu","mampu"}
def chunks(ws, hook):
    out=[];cur=[]
    for w in ws:
        s=m(w["s"],hook); e=m(w["e"],hook)
        if e<=s: e=s+0.12
        item={"w":w["w"],"s":round(s,3),"e":round(e,3)}
        if cur and (len(cur)>=3 or s-cur[-1]["e"]>0.35 or cur[-1]["w"][-1] in ",.?!" or w["f"]):
            out.append(cur);cur=[]
        cur.append(item)
    if cur: out.append(cur)
    return out
hookw=[w for w in words if 12.7<=w["s"]<15.4]
story=[w for w in words if w["s"]>=0.6]
C=chunks(hookw,True)+chunks(story,False)
# chunk display windows
for i,ch in enumerate(C):
    st=ch[0]["s"]; en=ch[-1]["e"]+0.25
    if i+1<len(C): en=min(en, C[i+1][0]["s"])
    if i>0: st=max(st, C[i-1]["en"])
    if i<3: en=min(en, segs[0][1]-segs[0][0]-0.02)
    ch_meta=(round(st,3),round(max(en,st+0.3),3))
    C[i]={"st":ch_meta[0],"en":ch_meta[1],"w":ch}
json.dump(C,open(f"{S}/src/captions.json","w"),ensure_ascii=False,indent=0)
H=segs[0][1]-segs[0][0]
def T(src): return round(m(src),3)
ev={k:T(v) for k,v in dict(failexam=5.36,allah=12.86,platform=19.06,mohon=27.94,login=36.44,daftar=40.9,bayar=43.92,isi=47.56,
    scene=51.60,assalam=52.04,website=57.72,tidak=69.36,bulan=75.9,nanti=82.86).items()}
ev["scene"]=round(offs[[i for i,(a,b) in enumerate(segs) if a>=51.5][0]],3)
ev["hookend"]=round(H,3); ev["vid"]=round(VID,3); ev["total"]=TOTAL
json.dump(ev,open(f"{S}/src/events.json","w"),indent=1)
print(ev, len(C))
