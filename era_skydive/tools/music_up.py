"""Original upbeat track (124 bpm) for ERA clips. Usage: music_up.py dur out.wav seed"""
import numpy as np, wave, sys
from scipy.signal import butter, sosfilt
SR = 44100; DUR = float(sys.argv[1]); N = int(SR * DUR); rng = np.random.default_rng(int(sys.argv[3]))
L = np.zeros(N); R = np.zeros(N)
def tt(d): return np.arange(int(SR * d)) / SR
def lp(x, f, o=2): return sosfilt(butter(o, f, "low", fs=SR, output="sos"), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, "high", fs=SR, output="sos"), x)
def mid(n): return 440 * 2 ** ((n - 69) / 12)
def add(x, t, g, pan=0.0):
    i = int(t * SR)
    if i >= N or i < 0: return
    x = x[:N - i]; L[i:i + len(x)] += x * g * (1 - max(0, pan)); R[i:i + len(x)] += x * g * (1 + min(0, pan))
BPM = 124; BEAT = 60 / BPM; BAR = BEAT * 4
def kick():
    t = tt(0.4); f = 48 + 120 * np.exp(-t * 30); x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 8)
    return np.tanh(x * 1.8)
def clap():
    t = tt(0.25); n = rng.standard_normal(len(t)); env = np.exp(-t * 22)
    for d in (0.0, 0.011, 0.022): env += np.where(t > d, np.exp(-(t - d) * 60), 0) * 0.5
    return hp(lp(n, 6000), 900) * env * 0.6
def hat(o=False):
    t = tt(0.25 if o else 0.06); return hp(rng.standard_normal(len(t)), 7000) * np.exp(-t * (14 if o else 70)) * 0.5
def saw(f, t): return 2 * ((f * t) % 1) - 1
def bass(n, d):
    t = tt(d); x = saw(mid(n), t) + 0.5 * np.sin(2 * np.pi * mid(n - 12) * t)
    return lp(x, 380) * np.minimum(1, t / 0.005) * np.exp(-t * 3) * 0.7
def stab(ch, d):
    t = tt(d); x = sum(saw(mid(n) * 2 ** (dt / 1200), t) for n in ch for dt in (-8, 8))
    return lp(x, 2400) * np.exp(-t * 6) / len(ch) * 0.6
prog = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]  # Am F C G
bars = int(DUR / BAR) + 1
for b in range(bars):
    t0 = b * BAR; ch = prog[b % 4]; intro = b < 1
    for k in range(4):
        tb = t0 + k * BEAT
        if not intro: add(kick(), tb, 0.9)
        add(hat(), tb + BEAT / 2, 0.35, pan=0.3)
        if k in (1, 3) and not intro: add(clap(), tb, 0.55, pan=-0.1)
    for s in range(8):
        n = ch[0] - 12 + (12 if s in (3, 7) else 0)
        if not intro: add(bass(n, BEAT / 2), t0 + s * BEAT / 2, 0.8)
    for s in (0, 3, 6):
        add(stab([n + 12 for n in ch], 0.35), t0 + s * BEAT / 2, 0.35, pan=[-0.4, 0.4, 0][s // 3])
    if b % 8 == 7:  # riser into next phrase
        t = tt(BAR); add(hp(rng.standard_normal(len(t)), 2000) * (t / BAR) ** 2 * 0.25, t0, 1)
for d, g in ((0.36, 0.18),):
    s = int(d * SR); L[s:] += R[:-s] * g; R[s:] += L[:-s] * g
fade = np.ones(N); fl = int(1.2 * SR); fade[-fl:] = np.linspace(1, 0, fl); fade[:int(0.05 * SR)] = np.linspace(0, 1, int(0.05 * SR))
st = np.tanh(np.stack([L * fade, R * fade], 1) * 0.9); st /= np.abs(st).max() * 1.1
w = wave.open(sys.argv[2], "w"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((st * 32767).astype(np.int16).tobytes()); w.close(); print("ok")
