"""Original ambient bed for podcast clips: warm minor pad + soft felt-piano plucks. Usage: music.py dur out.wav seed"""
import numpy as np, wave, sys
from scipy.signal import butter, sosfilt
SR = 44100; DUR = float(sys.argv[1]); N = int(SR * DUR); rng = np.random.default_rng(int(sys.argv[3]))
L = np.zeros(N); R = np.zeros(N)
def tt(d): return np.arange(int(SR * d)) / SR
def lp(x, f): return sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)
def mid(n): return 440 * 2 ** ((n - 69) / 12)
def add(x, t, g, pan=0.0):
    i = int(t * SR)
    if i >= N: return
    x = x[:N - i]; L[i:i + len(x)] += x * g * (1 - max(0, pan)); R[i:i + len(x)] += x * g * (1 + min(0, pan))
BAR = 60 / 72 * 4
prog = [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 60], [55, 59, 62, 67]]  # Am7 Fmaj7 C G
def pad(notes, d):
    t = tt(d); x = np.zeros_like(t)
    for n in notes:
        for det in (-0.08, 0.0, 0.09):
            f = mid(n - 12) * 2 ** (det / 12)
            x += 2 * ((f * t + rng.random()) % 1) - 1
    env = np.minimum(1, t / 1.2) * np.minimum(1, (d - t) / 1.2)
    return lp(x, 900) * env / 12
def pluck(n):
    t = tt(2.5); f = mid(n)
    x = (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t) + 0.1 * np.sin(6 * np.pi * f * t)) * np.exp(-t * 2.2)
    return lp(x, 2500) * np.minimum(1, t / 0.004)
k = 0; t0 = 0.0
while t0 < DUR:
    ch = prog[k % 4]
    add(pad(ch, BAR + 1.2), t0, 0.5, 0)
    add(np.sin(2 * np.pi * mid(ch[0] - 24) * tt(BAR)) * np.minimum(1, tt(BAR) / 0.5) * np.minimum(1, (BAR - tt(BAR)) / 0.5) * 0.18, t0, 1)
    for j, beat in enumerate([0, 1.5, 2.5, 3]):
        n = ch[[3, 1, 2, 0][j]] + 12
        add(pluck(n), t0 + beat * BAR / 4, 0.16, pan=[-0.3, 0.3, -0.15, 0.2][j])
    t0 += BAR; k += 1
# simple room: feedback delay
for d, g in ((0.29, 0.25), (0.43, 0.18)):
    s = int(d * SR); L[s:] += R[:-s] * g; R[s:] += L[:-s] * g
fade = np.ones(N); fl = int(1.5 * SR); fade[:int(0.8 * SR)] = np.linspace(0, 1, int(0.8 * SR)); fade[-fl:] = np.linspace(1, 0, fl)
st = np.stack([L * fade, R * fade], 1); st /= np.abs(st).max() * 1.12
w = wave.open(sys.argv[2], "w"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((st * 32767).astype(np.int16).tobytes()); w.close(); print("ok")
