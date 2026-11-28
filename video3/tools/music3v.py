"""Original tense background track for the WhatsApp trojan awareness video (48 s, 100 BPM)."""
import numpy as np, wave, sys
from scipy.signal import butter, sosfilt
import json
CU=json.load(open(sys.argv[2]))["cues"]
SR=44100; DUR=CU["end"]; N=int(SR*DUR); rng=np.random.default_rng(3)
L=np.zeros(N); R=np.zeros(N)
def at(t): return int(round(t*SR))
def add(x,t,g=1.0,pan=0.0):
    i=at(t)
    if i>=N: return
    x=x[:N-i]; L[i:i+len(x)]+=x*g*(1-max(0,pan)); R[i:i+len(x)]+=x*g*(1+min(0,pan))
def tt(d): return np.arange(int(SR*d))/SR
def lp(x,f): return sosfilt(butter(2,f,"low",fs=SR,output="sos"),x)
def hp(x,f): return sosfilt(butter(2,f,"high",fs=SR,output="sos"),x)
def bp(x,a,b): return sosfilt(butter(2,[a,b],"band",fs=SR,output="sos"),x)
def mid(n): return 440*2**((n-69)/12)
def saw(f,t): return 2*((f*t)%1)-1
def kick(): t=tt(0.4); f=45+100*np.exp(-t*30); return np.tanh(1.5*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*8))
def snare(): t=tt(0.3); return bp(rng.standard_normal(len(t)),1200,6000)*np.exp(-t*22)+0.3*np.sin(2*np.pi*190*t)*np.exp(-t*30)
def hat(): t=tt(0.05); return hp(rng.standard_normal(len(t)),7500)*np.exp(-t*90)
def tick(): t=tt(0.03); return np.sin(2*np.pi*2800*t)*np.exp(-t*200)
def pad(notes,d,cut=1200):
    t=tt(d); x=sum(saw(mid(n+det),t+rng.random()) for n in notes for det in (-0.1,0,0.1))
    return lp(x,cut)/(3*len(notes))*np.minimum(1,t/0.3)*np.minimum(1,(d-t)/0.3)
def bass(n,d):
    t=tt(d); f=mid(n); return np.tanh(1.6*(np.sin(2*np.pi*f*t)+0.3*lp(saw(f,t),500)))*np.exp(-t*3)*np.minimum(1,(d-t)/0.02)
def glitch(d=0.25):
    t=tt(d); x=np.sign(np.sin(2*np.pi*(80+rng.random()*400)*t))*rng.standard_normal(len(t))*0.6
    return bp(x,300,5000)*np.exp(-t*8)
def hitimpact():
    t=tt(1.5); f=40+90*np.exp(-t*10)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*2.5)+0.4*lp(rng.standard_normal(len(t)),2000)*np.exp(-t*5)
def pluck(n,d=0.3):
    t=tt(d); f=mid(n); return lp(np.sin(2*np.pi*f*t)+0.4*np.sign(np.sin(2*np.pi*f*t))*np.exp(-t*30),3500)*np.exp(-t*10)

B=0.6; BAR=4*B
# Dm Bb Gm A  (dark), then F C Dm Bb (determined) from 27s
dark=[(38,[62,65,69]),(34,[62,65,70]),(31,[62,67,70]),(33,[61,64,69])]
bright=[(41,[65,69,72]),(36,[64,67,72]),(38,[65,69,74]),(34,[65,70,74])]
# intro 0-4: alarm-ish pulse + ticking
for k in range(int(CU['s2']/B*2)): add(tick(),k*B/2,0.35,0.2 if k%2 else -0.2)
add(pad([50,53,57],CU['s2']+0.2,700),0,0.6)
for t0 in (0.0,1.2,2.4,3.0,3.3): add(glitch(),t0,0.25)
add(hitimpact(),0.0,0.8); add(hitimpact(),CU['s2'],0.9)
# main groove 4 - 46
t=CU['s2']; bar=0
OUT0=CU['s7']
while t<OUT0:
    sec2 = t>=CU['s5']
    root,notes=(bright if sec2 else dark)[bar%4]
    add(pad(notes,BAR+0.3,1600 if sec2 else 1000),t,0.55)
    for b in range(4):
        tb=t+b*B
        if tb>=OUT0: break
        add(kick(),tb,0.75 if (b%2==0 or sec2) else 0.0)
        if b%2==1: add(snare(),tb,0.35 if sec2 else 0.22)
        for s in range(2 if not sec2 else 4):
            add(hat(),tb+s*B/(2 if not sec2 else 4),0.12)
        add(bass(root-12+(0 if b%2==0 else 12 if sec2 else 0),B*0.9),tb,0.5)
    if sec2:
        mel=[notes[0]+12,notes[1]+12,notes[2]+12,notes[1]+12]
        for j in range(8): add(pluck(mel[j%4]),t+j*B/2,0.12,0.3 if j%2 else -0.3)
    else:
        for j in (0,3,5): add(tick(),t+j*B/2+B/4,0.2)
    t+=BAR; bar+=1
# transitions
for tx in (CU['s2'],CU['s3'],CU['s4'],CU['s6'],CU['s7']): add(glitch(0.3),tx-0.1,0.3)
# riser into section 2
tr=tt(1.8); fr=200+1800*(tr/1.8)**2
add(hp(rng.standard_normal(len(tr)),1500)*(tr/1.8)**2*0.4+0.15*np.sin(2*np.pi*np.cumsum(fr)/SR)*(tr/1.8),CU['s5']-1.8,0.6)
add(hitimpact(),CU['s5'],0.7)
# outro sustain
add(pad([53,57,60,65],DUR-OUT0,1400),OUT0,0.6); add(hitimpact(),OUT0,0.6)
fade=np.ones(N); fs=at(DUR-1.8); fade[fs:]=np.linspace(1,0,N-fs); L*=fade; R*=fade
m=max(abs(L).max(),abs(R).max()); L=np.tanh(L/m*1.3)*0.85; R=np.tanh(R/m*1.3)*0.85
w=wave.open(sys.argv[1],"wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.stack([L,R],1)*32767).astype(np.int16).tobytes()); w.close(); print("ok")
