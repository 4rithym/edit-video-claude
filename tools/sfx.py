import numpy as np, wave, sys
SR=44100; out=sys.argv[1]
rng=np.random.default_rng(7)
def save(name,x):
    x=x/ (np.max(np.abs(x))+1e-9)*0.9
    st=np.stack([x,x],1)
    w=wave.open(f"{out}/{name}.wav","wb");w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR)
    w.writeframes((st*32767).astype(np.int16).tobytes());w.close()
def t(d): return np.arange(int(SR*d))/SR
def lp(x,a):  # one-pole lowpass, a per-sample array or scalar
    y=np.zeros_like(x);p=0.0
    a=np.broadcast_to(a,x.shape)
    for i in range(len(x)): p+=a[i]*(x[i]-p); y[i]=p
    return y
# whoosh: noise with sweeping lowpass, bell envelope
d=0.55;tt=t(d);n=rng.standard_normal(len(tt))
sweep=0.02+0.35*np.sin(np.pi*tt/d)**2
env=np.sin(np.pi*tt/d)**3
save("whoosh",lp(lp(n,sweep),sweep)*env)
# pop: sine with fast pitch drop
d=0.14;tt=t(d);f=900*np.exp(-tt*30)+300
save("pop",np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*35))
# ding: bell partials
d=1.4;tt=t(d);x=sum(a*np.sin(2*np.pi*fr*tt)*np.exp(-tt*k) for fr,a,k in [(1318,1,3.5),(2637,.5,5),(3956,.25,7),(1976,.3,4)])
x*=np.minimum(1,tt/0.003);save("ding",x)
# impact/boom: low sine drop + noise burst
d=1.0;tt=t(d);f=120*np.exp(-tt*6)+40
x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*4)+0.6*lp(rng.standard_normal(len(tt)),0.08)*np.exp(-tt*14)
save("impact",x)
# riser: rising noise+tone
d=1.2;tt=t(d);f=200+1200*(tt/d)**2
x=0.5*np.sin(2*np.pi*np.cumsum(f)/SR)+lp(rng.standard_normal(len(tt)),0.05+0.4*tt/d)
x*=(tt/d)**2;save("riser",x)
# click/tick
d=0.05;tt=t(d);save("click",rng.standard_normal(len(tt))*np.exp(-tt*150)+np.sin(2*np.pi*2500*tt)*np.exp(-tt*120))
# record scratch / rewind-ish: fast down-pitched saw glitch
d=0.45;tt=t(d);f=1400*np.exp(-tt*7)+120
ph=np.cumsum(f)/SR;x=(2*(ph%1)-1)*np.exp(-tt*3)
save("rewind",lp(x,0.3))
# cash register / coin-ish: two quick high dings
d=0.6;tt=t(d);x=np.sin(2*np.pi*2093*tt)*np.exp(-tt*9);x2=np.zeros_like(x);o=int(0.08*SR);x2[o:]=np.sin(2*np.pi*2637*tt[:-o])*np.exp(-tt[:-o]*8)
save("coin",x+x2)
