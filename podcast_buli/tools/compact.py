import re, sys
lines = open(sys.argv[1]).read().splitlines(); lo, hi = float(sys.argv[2]), float(sys.argv[3])
cur, buf = None, []
for l in lines:
    m = re.match(r'\[\s*([\d.]+)-\s*([\d.]+)\]\s*(.*)', l)
    if not m: continue
    s = float(m[1])
    if s < lo or s >= hi: continue
    if cur is None or s - cur >= 20:
        if buf: print(f"[{int(cur//60)}:{int(cur%60):02d} {cur:.0f}] " + " ".join(buf))
        cur, buf = s, []
    buf.append(m[3].strip())
if buf: print(f"[{int(cur//60)}:{int(cur%60):02d} {cur:.0f}] " + " ".join(buf))
