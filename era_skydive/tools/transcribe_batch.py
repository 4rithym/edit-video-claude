import json, sys, subprocess, numpy as np, os
from faster_whisper import WhisperModel
m = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8", cpu_threads=4)
out = {}
for f in sys.argv[2:]:
    n = os.path.basename(f).rsplit(".", 1)[0]
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    segs, info = m.transcribe(a, word_timestamps=True, vad_filter=True, beam_size=5, language="ms")
    out[n] = [{"start": s.start, "end": s.end, "text": s.text, "words": [{"w": w.word, "s": w.start, "e": w.end} for w in s.words]} for s in segs]
    print(f"== {n}", file=sys.stderr)
    for s in out[n]: print(f'[{s["start"]:6.2f}-{s["end"]:6.2f}] {s["text"]}', file=sys.stderr)
    json.dump(out, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
