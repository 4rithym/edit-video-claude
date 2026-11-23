import json, sys
T = json.load(open(sys.argv[1])); a, b = float(sys.argv[2]), float(sys.argv[3])
for s in T["segments"]:
    if s["end"] < a or s["start"] > b: continue
    print(f'[{s["start"]:.2f}-{s["end"]:.2f}] ' + " ".join(f'{w["w"].strip()}@{w["s"]:.2f}' for w in s["words"]))
