# HyperFrames composition for ClippersFarm "Edit Your Own Version". Usage: cf_comp.py spec.json
import json, sys, os, re, shutil, html as H
B = os.path.dirname(os.path.abspath(__file__)); E = os.path.dirname(B) + "/cf"; REPO = "/home/user/edit-video-claude"
spec = json.load(open(sys.argv[1])); D = f"{E}/work/{spec['id']}"; P = f"{D}/hf"
T = json.load(open(f"{D}/timing.json"))
os.makedirs(f"{P}/assets/sfx", exist_ok=True)
if not os.path.exists(f"{P}/assets/fonts"): shutil.copytree(f"{REPO}/project/assets/fonts", f"{P}/assets/fonts")
for f in os.listdir(f"{REPO}/project/assets/sfx"): shutil.copy(f"{REPO}/project/assets/sfx/{f}", f"{P}/assets/sfx/{f}")
shutil.copy(f"{REPO}/project/assets/gsap.min.js", f"{P}/assets/gsap.min.js"); shutil.copy(f"{D}/cut.mp4", f"{P}/assets/cut.mp4")
VID = T["total"]; END = 3.4; TOTAL = VID + END
KEY = {k.lower() for k in spec.get("keywords", [])}
FIX = {"Creepers": "Clippers", "clipers": "Clippers", "berjadi": "boleh jadi", "bag": "beg", "CDA": "CTA", "Shots": "Shorts",
       "tersimpat": "tersimpan", "books": "hooks", "hoax": "hooks", "hopes": "hooks", **spec.get("fix", {})}
BRAND2 = {"pump", "prom", "spam", "form", "fun", "swamp", "farms", "farm", "pom"}
parts, tl, SFX = [], [], []
def clip(id_, st, dur, inner, cls="", style=""):
    parts.append(f'<div id="{id_}" class="clip {cls}" data-start="{st:.3f}" data-duration="{dur:.3f}" style="{style}">{inner}</div>')
def sfx(name, t, vol=0.4, dur=1.5): SFX.append((name, max(0, t), vol, dur))
parts.append(f'<div id="stage"><video id="vid" class="clip" data-start="0" data-duration="{VID:.3f}" data-has-audio="true" '
             f'data-volume="1" src="assets/cut.mp4" playsinline></video></div>')
for i, b in enumerate(T["bounds"]):
    z = 1.0 if i % 2 == 0 else 1.08
    tl.append(f'tl.fromTo("#stage",{{scale:{z + 0.03:.2f}}},{{scale:{z},duration:0.35,ease:"power3.out",immediateRender:false}},{b["s"]:.3f});')
    if i > 0: sfx("whoosh" if i == 1 else "click", b["s"] - 0.1, 0.32 if i == 1 else 0.18)
# hook panel
hk = spec["hook"]; hd = T["bounds"][0]["e"]
clip("hook", 0, hd + 0.3, f'<div class="hp"><div class="kick">{H.escape(hk["kicker"])}</div><div class="h1">{H.escape(hk["l1"])}</div>'
     f'<div class="h2"><span>{H.escape(hk["l2"])}</span></div></div>', "hookwrap")
tl.append('tl.from("#hook .hp",{yPercent:-100,duration:0.35,ease:"power3.out"},0);')
tl.append('tl.from("#hook .kick",{opacity:0,x:-30,duration:0.25},0.2);')
tl.append('tl.from("#hook .h1",{opacity:0,y:30,duration:0.3,ease:"power3.out"},0.28);')
tl.append('tl.from("#hook .h2 span",{scaleX:0,transformOrigin:"0 50%",duration:0.35,ease:"power3.out"},0.5);')
tl.append(f'tl.to("#hook .hp",{{yPercent:-110,duration:0.3,ease:"power3.in"}},{hd:.3f});')
sfx("pop", 0.5, 0.3)
# persistent tag + progress
clip("tag", hd, VID - hd, '<div class="cf"><i></i>ClippersFarm</div>', "tagwrap")
tl.append(f'tl.from("#tag .cf",{{opacity:0,y:-20,duration:0.3}},{hd + 0.1:.3f});')
# caption band (covers original burned subtitles)
clip("band", 0, VID, '<div id="prog"></div>', "band")
tl.append(f'tl.fromTo("#prog",{{scaleX:0}},{{scaleX:1,duration:{VID:.3f},ease:"none"}},0);')
# words: merge brand phrase + hyphen pieces
ws = []
for w in T["words"]:
    raw = w["w"]; core = re.sub(r"[^\w]", "", raw).lower()
    if ws and core in BRAND2 and re.sub(r"[^\w]", "", ws[-1]["w"]).lower() in ("clippers", "clipper", "creepers", "clipers") and w.get("shot") == ws[-1].get("shot"):
        ws[-1] = {**ws[-1], "w": "Clippers Farm" + re.sub(r"[\w]", "", raw), "e": w["e"]}; continue
    if ws and re.match(r"^[-.,]\w", raw) and w["s"] - ws[-1]["e"] < 0.4: ws[-1] = {**ws[-1], "w": ws[-1]["w"] + raw, "e": w["e"]}; continue
    ws.append(dict(w))
groups, g = [], []
for w in ws:
    if g and (g[-1].get("shot") != w.get("shot") or len(g) >= 4 or sum(len(x["w"]) for x in g) + len(w["w"]) > 22 or w["s"] - g[-1]["e"] > 0.35):
        groups.append(g); g = []
    g.append(w)
    if re.search(r"[.?!]$", w["w"]): groups.append(g); g = []
if g: groups.append(g)
for i, g in enumerate(groups):
    st = g[0]["s"]; en = groups[i + 1][0]["s"] if i + 1 < len(groups) else VID; en = min(en, g[-1]["e"] + 0.6)
    sb = next((b["e"] for b in T["bounds"] if b["s"] <= st < b["e"]), VID); en = min(en, sb)
    sp = []
    for j, w in enumerate(g):
        txt = re.sub(r"[.,]$", "", w["w"]); core = re.sub(r"[^\w'-]", "", txt)
        if core in FIX: txt = txt.replace(core, FIX[core])
        elif core.lower() in FIX: txt = txt.replace(core, FIX[core.lower()])
        cls = "w k" if core.lower() in KEY or "Clippers Farm" in txt else "w"
        sp.append(f'<span id="c{i}_{j}" class="{cls}">{H.escape(txt)}</span>')
        tl.append(f'tl.set("#c{i}_{j}",{{className:"{cls} on"}},{max(w["s"], st):.3f});')
    clip(f"cap{i}", st, max(0.2, en - st), f'<div class="cap">{" ".join(sp)}</div>', "capwrap")
    tl.append(f'tl.from("#cap{i} .cap",{{y:16,opacity:0,duration:0.14,ease:"power2.out"}},{st:.3f});')
# end card CTA
clip("end", VID - 0.3, END + 0.3, '''<div class="end-in"><div class="e-dot"><i></i>ClippersFarm</div>
<div class="e1">Check Clippers Farm<br/>for more details.</div><div class="e2">Link at my bio! &#8593;</div><div class="e3">#CFforBRAND</div></div>''', "endcard")
tl.append(f'tl.from("#end",{{yPercent:100,duration:0.35,ease:"power3.out"}},{VID - 0.3:.3f});')
tl.append(f'tl.from("#end .e1",{{y:40,opacity:0,duration:0.4,ease:"power3.out"}},{VID + 0.1:.3f});')
tl.append(f'tl.from("#end .e2",{{scale:0.6,opacity:0,duration:0.35,ease:"back.out(2)"}},{VID + 0.45:.3f});')
tl.append(f'tl.to("#end .e2",{{y:-12,duration:0.35,yoyo:true,repeat:3,ease:"sine.inOut"}},{VID + 0.9:.3f});')
tl.append(f'tl.from("#end .e3, #end .e-dot",{{opacity:0,duration:0.3}},{VID + 0.7:.3f});')
sfx("whoosh", VID - 0.4, 0.35); sfx("ding", VID + 0.45, 0.3)
audio = "\n".join(f'<audio id="sfx{i}" class="clip" data-start="{t:.3f}" data-duration="{d}" data-volume="{v}" src="assets/sfx/{n}.wav"></audio>'
                  for i, (n, t, v, d) in enumerate(SFX))
CSS = open(f"{B}/cf_style.css").read()
doc = f'''<!doctype html>
<html lang="ms" data-resolution="portrait"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script><style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="1080" data-height="1920">
{chr(10).join(parts)}
{audio}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(tl)}
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl; tl.seek(0);
</script></body></html>'''
open(f"{P}/index.html", "w").write(doc)
json.dump({"name": spec["id"].lower(), "private": True, "type": "module"}, open(f"{P}/package.json", "w"))
shutil.copy(f"{REPO}/project/hyperframes.json", f"{P}/hyperframes.json")
print("ok", spec["id"], "groups", len(groups), "total", round(TOTAL, 2))
