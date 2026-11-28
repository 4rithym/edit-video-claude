"""Subtle original underscore for the pro awareness video: tense pulse -> resolve. Follows cues."""
import numpy as np, wave, sys, json
from scipy.signal import butter, sosfilt
CU=json.load(open(sys.argv[2]))["cues"]
SR=44100; DUR=CU["end"]; N=int(SR*DUR); rng=np.random.default_rng(11)
L=np.zeros(N); R=np.zeros(N)
def at(t): return int(round(t*SR))
def add(x,t,g=1.0,pan=0.0):
    i=at(t)
    if i>=N: return
    x=x[:N-i]; L[i:i+len(x)]+=x*g*(1-max(0,pan)); R[i:i+len(x)]+=x*g*(1+min(0,pan))
def tt(d): return np.arange(int(SR*d))/SR
def lp(x,f): return sosfilt(butter(2,f,"low",fs=SR,output="sos"),x)
def hp(x,f): return sosfilt(butter(2,f,"high",fs=SR,output="sos"),x)
def mid(n): return 440*2**((n-69)/12)
def saw(f,t): return 2*((f*t)%1)-1
def pad(notes,d,cut):
    t=tt(d); x=sum(saw(mid(n+det),t+rng.random()) for n in notes for det in (-0.08,0,0.08))
    x=lp(x,cut)/(3*len(notes)); env=np.minimum(1,t/1.2)*np.minimum(1,(d-t)/1.2); return x*env
def pulse(n,d):
    t=tt(d); f=mid(n); return np.sin(2*np.pi*f*t)*np.exp(-t*5)*np.minimum(1,t/0.004)
def tick(): t=tt(0.03); return hp(rng.standard_normal(len(t)),6000)*np.exp(-t*160)
def swell(d):
    t=tt(d); return hp(rng.standard_normal(len(t)),900)*(t/d)**3*0.5
B=60/96
dark=[(38,[57,62,65]),(34,[58,62,65]),(31,[58,62,67]),(33,[57,61,64])]
bright=[(41,[60,65,69]),(36,[60,64,67]),(38,[62,65,69]),(34,[62,65,70])]
F=CU["F"]; H=CU["H"]
t=0.0; bar=0
while t<DUR-0.5:
    sec2=t>=F-0.01
    root,notes=(bright if sec2 else dark)[bar%4]
    d=min(4*B, DUR-t)
    add(pad(notes, d+1.0, 1400 if sec2 else 900), t, 0.5)
    for b in range(8):
        tb=t+b*B/2
        if tb>=DUR-0.3: break
        add(pulse(root-12, B/2*0.95), tb, 0.55 if b%2==0 else 0.3)
        if t>=CU["B"]-0.01 and t<H: add(tick(), tb+B/4, 0.12, 0.3 if b%2 else -0.3)
    t+=4*B; bar+=1
for key in ("B","C","D","E","F","G","H"):
    add(swell(1.2), CU[key]-1.2, 0.35)
fade=np.ones(N); fs=at(DUR-2.5); fade[fs:]=np.linspace(1,0,N-fs); fi=at(1.5); fade[:fi]*=np.linspace(0,1,fi)
L*=fade; R*=fade
m=max(abs(L).max(),abs(R).max()); L=L/m*0.8; R=R/m*0.8
w=wave.open(sys.argv[1],"wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.stack([L,R],1)*32767).astype(np.int16).tobytes()); w.close(); print("ok")
