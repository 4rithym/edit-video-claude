# Generate a HyperFrames composition for a clip. Usage: comp.py spec.json
import json, sys, os, re, shutil, html as H
B = os.path.dirname(os.path.abspath(__file__)); W = os.path.dirname(B) + "/work"; REPO = "/home/user/edit-video-claude"
spec = json.load(open(sys.argv[1])); cid = spec["id"]; D = f"{W}/{cid}"; P = f"{D}/hf"
T = json.load(open(f"{D}/timing.json")); A = json.load(open(f"{D}/an.json"))
os.makedirs(f"{P}/assets", exist_ok=True)
for f in ("fonts", "gsap.min.js"):
    s, d = f"{REPO}/project/assets/{f}", f"{P}/assets/{f}"
    if not os.path.exists(d): (shutil.copytree if os.path.isdir(s) else shutil.copy)(s, d)
shutil.copy(f"{D}/cut.mp4", f"{P}/assets/cut.mp4")
VID = T["total"]; END = 2.6; TOTAL = VID + END
KEY = {k.lower() for k in spec.get("keywords", [])}
FIX = {"i": "I", **spec.get("fix", {})}
parts, tl = [], []
def clip(id_, st, dur, inner, cls="", style=""):
    parts.append(f'<div id="{id_}" class="clip {cls}" data-start="{st:.3f}" data-duration="{dur:.3f}" style="{style}">{inner}</div>')

parts.append(f'<div id="stage"><video id="vid" class="clip" data-start="0" data-duration="{VID:.3f}" data-has-audio="true" '
             f'data-volume="1" src="assets/cut.mp4" playsinline></video></div>')
clip("shade", 0, VID, "")
# --- jump-cut zoom rhythm: alternate framing on each cut, slow drift inside segments
zooms = spec.get("zooms", {})
for i, (s, e, k) in enumerate(T["bounds"]):
    z = zooms.get(str(i), 1.0 if i % 2 == 0 else 1.09)
    tl.append(f'tl.fromTo("#stage",{{scale:{z}}},{{scale:{z + 0.025:.3f},duration:{e - s:.3f},ease:"none",immediateRender:false}},{s:.3f});')
# --- hook headline
hk = spec["hook"]; hd = spec.get("hook_dur", 3.2)
l2 = H.escape(hk["l2"]).replace(H.escape(hk["mark"]), f'<mark>{H.escape(hk["mark"])}</mark>')
clip("hook", 0.0, hd, f'<div class="kicker">AIDIDITMYWAY PODCAST&ensp;&middot;&ensp;DR. SYAMIR</div>'
     f'<div class="hl"><span class="ln"><span>{H.escape(hk["l1"])}</span></span><span class="ln"><span>{l2}</span></span></div>', "hookwrap")
tl.append('tl.from("#hook .kicker",{opacity:0,y:-16,duration:0.35,ease:"power2.out"},0.05);')
tl.append('tl.from("#hook .ln > span",{yPercent:110,duration:0.55,ease:"power3.out",stagger:0.12},0.1);')
tl.append('tl.from("#hook mark",{"--mk":0,duration:0.45,ease:"power2.out"},0.55);')
tl.append(f'tl.to("#hook",{{opacity:0,y:-20,duration:0.3,ease:"power2.in"}},{hd - 0.3:.3f});')
# --- name tags (first appearance of each speaker in close-up)
def who(x): return "dr" if x < 900 else "aidy"
seen = set()
for s, e, k in T["bounds"]:
    pass
src_bounds = list(zip(T["segs"], T["bounds"]))
tags = {"dr": ("Dr. Syamir", "Pakar Kriminologi"), "aidy": ("Aididitmyway", "Hos Podcast")}
for (a, b, _), (s, e, _) in src_bounds:
    for sh in A["shots"]:
        ss, se = A["start"] + sh["s"], A["start"] + sh["e"]
        if sh["wide"] or se <= a or ss >= b: continue
        p = who(sh["x"]); t0 = s + max(0, ss - a)
        if p in seen or t0 < hd - 0.2 or t0 > VID - 3: continue
        if min(b, se) - max(a, ss) < 1.5: continue
        seen.add(p); n, r = tags[p]; tid = f"tag_{p}"
        clip(tid, t0 + 0.2, 2.8, f'<div class="tag"><i></i><div><b>{n}</b><span>{r}</span></div></div>', "tagwrap")
        tl.append(f'tl.from("#{tid} .tag",{{x:-40,opacity:0,duration:0.45,ease:"power3.out"}},{t0 + 0.2:.3f});')
        tl.append(f'tl.from("#{tid} i",{{scaleY:0,duration:0.4,ease:"power3.out"}},{t0 + 0.25:.3f});')
        tl.append(f'tl.to("#{tid} .tag",{{opacity:0,duration:0.3}},{t0 + 2.7:.3f});')
# --- captions: short phrase groups, active word lights up
ws = []
for w in T["words"]:
    if ws and re.match(r"^[-.]\w", w["w"]) and w["s"] - ws[-1]["e"] < 0.4:
        ws[-1] = {**ws[-1], "w": ws[-1]["w"] + w["w"], "e": w["e"]}
    else: ws.append(dict(w))
groups, g = [], []
for i, w in enumerate(ws):
    txt = w["w"]
    brk = g and (len(g) >= 3 or sum(len(x["w"]) for x in g) + len(txt) > 16 or w["s"] - g[-1]["e"] > 0.28)
    if brk: groups.append(g); g = []
    g.append(w)
    if re.search(r"[.?!,]$", txt): groups.append(g); g = []
if g: groups.append(g)
for i, g in enumerate(groups):
    st = g[0]["s"]; en = groups[i + 1][0]["s"] if i + 1 < len(groups) else VID
    en = min(en, g[-1]["e"] + 0.6)
    spans = []
    for j, w in enumerate(g):
        clean = re.sub(r"[^\w'-]", "", w["w"].lower())
        cls = "w k" if clean in KEY else "w"
        txt = re.sub(r"[.,]$", "", w["w"])
        core = re.sub(r"[^\w'-]", "", txt)
        if core in FIX: txt = txt.replace(core, FIX[core])
        elif core.lower() in FIX: txt = txt.replace(core, FIX[core.lower()])
        spans.append(f'<span id="c{i}_{j}" class="{cls}">{H.escape(txt)}</span>')
        tl.append(f'tl.to("#c{i}_{j}",{{opacity:1,scale:1,duration:0.09,ease:"power2.out"}},{max(w["s"], st):.3f});')
    clip(f"cap{i}", st, max(0.2, en - st), f'<div class="cap">{" ".join(spans)}</div>', "capwrap")
    tl.append(f'tl.from("#cap{i} .cap",{{y:14,opacity:0,duration:0.14,ease:"power2.out"}},{st:.3f});')
# --- end card
clip("end", VID - 0.35, END + 0.35, f'''<div class="end-in"><div class="eline"></div>
<div class="e1">Hentikan buli.</div><div class="e2">Mula peduli.</div>
<div class="eh">#hentibulimulapeduli</div><div class="es">Episod penuh di YouTube &middot; Aididitmyway Podcast</div></div>''', "endcard")
tl.append(f'tl.from("#end",{{opacity:0,duration:0.35,ease:"power1.inOut"}},{VID - 0.35:.3f});')
tl.append(f'tl.from("#end .eline",{{scaleX:0,duration:0.5,ease:"power3.out"}},{VID:.3f});')
tl.append(f'tl.from("#end .e1, #end .e2",{{y:30,opacity:0,duration:0.5,stagger:0.18,ease:"power3.out"}},{VID + 0.1:.3f});')
tl.append(f'tl.from("#end .eh, #end .es",{{opacity:0,duration:0.4,stagger:0.12}},{VID + 0.6:.3f});')
CSS = open(f"{B}/style.css").read()
doc = f'''<!doctype html>
<html lang="ms" data-resolution="portrait">
<head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script><style>{CSS}</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="1080" data-height="1920">
{chr(10).join(parts)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(tl)}
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body></html>'''
open(f"{P}/index.html", "w").write(doc)
json.dump({"name": cid, "private": True, "type": "module"}, open(f"{P}/package.json", "w"))
shutil.copy(f"{REPO}/project/hyperframes.json", f"{P}/hyperframes.json")
json.dump({"groups": [[(w["w"], w["s"]) for w in g] for g in groups]}, open(f"{D}/groups.json", "w"), ensure_ascii=False)
print("ok", cid, "groups", len(groups), "total", round(TOTAL, 2), "tags", sorted(seen))
