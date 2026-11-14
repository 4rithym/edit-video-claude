"""Original background track for video 2 (osom -> zakatUniKL reveal). Deterministic synth."""
import numpy as np, wave, sys
from scipy.signal import butter, sosfilt

SR = 44100
DUR = 10.0
N = int(SR * DUR)
rng = np.random.default_rng(42)
L = np.zeros(N); R = np.zeros(N)

def at(t): return int(round(t * SR))
def add(x, t, gain=1.0, pan=0.0):
    i = at(t)
    if i >= N: return
    x = x[: N - i]
    L[i:i + len(x)] += x * gain * (1 - max(0, pan))
    R[i:i + len(x)] += x * gain * (1 + min(0, pan))
def tt(d): return np.arange(int(SR * d)) / SR
def lp(x, f, o=2): return sosfilt(butter(o, f, "low", fs=SR, output="sos"), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, "high", fs=SR, output="sos"), x)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], "band", fs=SR, output="sos"), x)
def mid(n): return 440 * 2 ** ((n - 69) / 12)
def saw(f, t): return 2 * ((f * t) % 1) - 1

def kick(h=1.0):
    t = tt(0.45); f = 50 + 110 * np.exp(-t * 28)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
    x[:200] += rng.standard_normal(200) * 0.3 * np.linspace(1, 0, 200)
    return np.tanh(x * 1.6) * h
def clap():
    t = tt(0.25); n = rng.standard_normal(len(t))
    env = np.zeros(len(t))
    for o in (0, 0.011, 0.022): env += (t >= o) * np.exp(-np.maximum(t - o, 0) * 60)
    env += np.exp(-t * 18) * 0.5
    return bp(n, 900, 5000) * env
def hat(open_=False):
    t = tt(0.25 if open_ else 0.06); n = rng.standard_normal(len(t))
    return hp(n, 7000) * np.exp(-t * (14 if open_ else 70))
def tick():
    t = tt(0.04); return np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 160)

def pad(notes, d, cutoff=1800):
    t = tt(d); x = np.zeros(len(t))
    for n in notes:
        for det in (-0.12, 0, 0.12):
            x += saw(mid(n + det), t + rng.random())
    x = lp(x, cutoff, 2) / (len(notes) * 3)
    env = np.minimum(1, t / 0.05) * np.minimum(1, (d - t) / 0.08)
    return x * env
def bass(n, d):
    t = tt(d); f = mid(n)
    x = np.sin(2 * np.pi * f * t) + 0.35 * lp(saw(f, t), 600)
    return np.tanh(1.4 * x) * np.minimum(1, t / 0.005) * np.minimum(1, (d - t) / 0.03) * np.exp(-t * 1.2)
def pluck(n, d=0.35):
    t = tt(d); f = mid(n)
    x = 0.6 * np.sin(2 * np.pi * f * t) + 0.4 * np.sign(np.sin(2 * np.pi * f * t)) * np.exp(-t * 25)
    return lp(x, 4000) * np.exp(-t * 9)

# ---------- Part A: tension, kicks on the hand pumps (0.5, 1.17, 1.83, 2.5) ----------
B = 0.6667
pumps = [0.5, 1.167, 1.833, 2.5]
for i, p in enumerate(pumps):
    add(kick(0.9), p, 0.9)
    add(tick(), p + B / 2, 0.25, 0.3)
    add(tick(), p + B / 4, 0.12, -0.3); add(tick(), p + 3 * B / 4, 0.12, -0.3)
# low drone that rises a semitone each pump
for i, p in enumerate([0.0] + pumps[:-1]):
    d = (pumps[i] if i < len(pumps) else 2.85) - p
    add(pad([45 + i, 52 + i], max(d, 0.4) + 0.05, 900), p, 0.35)
add(pad([48, 55], 0.4, 900), 2.5, 0.35)
# OSOM hit at 2.85
add(kick(1.0), 2.85, 1.0)
t = tt(1.0); add(lp(rng.standard_normal(len(t)), 3000) * np.exp(-t * 6), 2.85, 0.35)
add(pad([57, 61, 64, 69], 0.5, 3000), 2.85, 0.5)

# ---------- "sad trombone" 3.0 - 3.9 (duit tinggal bulu) ----------
for k, (n, d) in enumerate([(55, 0.2), (54, 0.2), (53, 0.2), (52, 0.45)]):
    t = tt(d); vib = 1 + (0.012 * np.sin(2 * np.pi * 6 * t) if k == 3 else 0)
    f = mid(n) * vib
    x = lp(saw(f, t) + 0.5 * saw(f * 2, t), 1400) * np.minimum(1, t / 0.02) * np.minimum(1, (d - t) / 0.04)
    add(x, 3.0 + 0.2 * k, 0.32)
# riser into drop
t = tt(0.6); f = 300 + 2500 * (t / 0.6) ** 2
add(hp(rng.standard_normal(len(t)), 2000) * (t / 0.6) ** 2 * 0.5 + 0.15 * np.sin(2 * np.pi * np.cumsum(f) / SR) * (t / 0.6), 3.35, 0.5)

# ---------- Part B: drop at 3.95 — bright groove, C G Am F ----------
D0 = 3.95
add(kick(1.0), D0, 1.0)
t = tt(1.4); add(lp(rng.standard_normal(len(t)), 6000) * np.exp(-t * 3), D0, 0.25)  # crash
prog = [(60, [60, 64, 67, 72]), (55, [59, 62, 67, 71]), (57, [60, 64, 69, 72]), (53, [60, 65, 69, 72]), (60, [60, 64, 67, 72])]
CH = 2 * B
mel = [72, 76, 79, 76, 74, 79, 74, 71, 72, 76, 81, 76, 77, 72, 69, 72, 79, 76, 72, 76]
duck = np.ones(N)
beat = 0
tb = D0
while tb < DUR - 0.05:
    add(kick(0.95), tb, 0.95)
    i = at(tb); k = np.minimum(1, np.arange(int(0.25 * SR)) / (0.25 * SR)) ** 0.7
    duck[i:i + len(k)] = np.minimum(duck[i:i + len(k)], 0.35 + 0.65 * k[: N - i] if i < N else 1)
    if beat % 2 == 1: add(clap(), tb, 0.55)
    for s in range(4):
        add(hat(open_=(s == 2)), tb + s * B / 4, 0.18 if s != 2 else 0.12, 0.25)
    beat += 1; tb += B
# chords + bass (bass bounces on 8ths)
for c in range(int((DUR - D0) / CH) + 1):
    t0 = D0 + c * CH
    if t0 >= DUR: break
    root, notes = prog[c % len(prog)]
    pd = pad(notes, CH, 2600)
    i = at(t0); seg = duck[i:i + len(pd)]
    add(pd * np.pad(seg, (0, len(pd) - len(seg)), constant_values=1), t0, 0.55)
    for e in range(4):
        add(bass(root - 24 + (12 if e == 3 else 0), B / 2 * 0.9), t0 + e * B / 2, 0.55)
# pluck melody on 8ths
for j, n in enumerate(mel):
    t0 = D0 + j * B / 2
    if t0 < DUR - 0.3: add(pluck(n), t0, 0.22, 0.2 if j % 2 else -0.2)

# ---------- master ----------
fade = np.ones(N); fs = at(DUR - 1.0); fade[fs:] = np.linspace(1, 0, N - fs)
L *= fade; R *= fade
m = max(np.abs(L).max(), np.abs(R).max())
L = np.tanh(L / m * 1.2) * 0.85; R = np.tanh(R / m * 1.2) * 0.85
st = np.stack([L, R], 1)
w = wave.open(sys.argv[1], "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((st * 32767).astype(np.int16).tobytes()); w.close()
print("ok", sys.argv[1])
