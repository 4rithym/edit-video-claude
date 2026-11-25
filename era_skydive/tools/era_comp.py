# HyperFrames composition in ERA campaign style. Usage: era_comp.py spec.json
import json, sys, os, re, shutil, html as H
B = os.path.dirname(os.path.abspath(__file__)); E = os.path.dirname(B) + "/era"; REPO = "/home/user/edit-video-claude"
spec = json.load(open(sys.argv[1])); D = f"{E}/work/{spec['id']}"; P = f"{D}/hf"
T = json.load(open(f"{D}/timing.json"))
os.makedirs(f"{P}/assets/fonts", exist_ok=True); os.makedirs(f"{P}/assets/sfx", exist_ok=True)
for f in os.listdir(f"{E}/fonts"): shutil.copy(f"{E}/fonts/{f}", f"{P}/assets/fonts/{f}")
for f in os.listdir(f"{REPO}/project/assets/sfx"): shutil.copy(f"{REPO}/project/assets/sfx/{f}", f"{P}/assets/sfx/{f}")
shutil.copy(f"{REPO}/project/assets/gsap.min.js", f"{P}/assets/gsap.min.js")
shutil.copy(f"{E}/dl/w_1uXtyJadhZdz6eUfCh_bFD4S4AHlqvKHO.img", f"{P}/assets/era.png")
shutil.copy(f"{E}/era_logo.svg", f"{P}/assets/mbsb.svg")
shutil.copy(f"{D}/cut.mp4", f"{P}/assets/cut.mp4")
VID = T["total"]; END = 3.2; TOTAL = VID + END
KEY = {k.lower() for k in spec.get("keywords", [])}; FIX = spec.get("fix", {})
parts, tl, SFX = [], [], []
def clip(id_, st, dur, inner, cls="", style=""):
    parts.append(f'<div id="{id_}" class="clip {cls}" data-start="{st:.3f}" data-duration="{dur:.3f}" style="{style}">{inner}</div>')
def sfx(name, t, vol=0.5, dur=1.5): SFX.append((name, max(0, t), vol, dur))
parts.append(f'<div id="stage"><video id="vid" class="clip" data-start="0" data-duration="{VID:.3f}" data-has-audio="true" '
             f'data-volume="1" src="assets/cut.mp4" playsinline></video></div>')
clip("shade", 0, VID, "")
# punch-in on every cut, a touch of drift
for i, b in enumerate(T["bounds"]):
    z0 = 1.12 if (i == 0 or "chapter" in b) else 1.04
    tl.append(f'tl.fromTo("#stage",{{scale:{z0}}},{{scale:1,duration:0.45,ease:"power3.out",immediateRender:false}},{b["s"]:.3f});')
    if "sfx" in b:
        n = b["sfx"]; at = b["s"] - (1.0 if n == "riser" else 0.12 if n == "whoosh" else 0)
        sfx(n, at, {"impact": 0.55, "whoosh": 0.4, "riser": 0.35}.get(n, 0.4))
    if "chapter" in b and i > 0:
        cid = f"ch{i}"; d = min(1.9, b["e"] - b["s"])
        clip(cid, b["s"], d, f'<div class="chap"><span>{H.escape(b["chapter"])}</span></div>', "chapwrap")
        tl.append(f'tl.from("#{cid} .chap",{{xPercent:-120,duration:0.32,ease:"power4.out"}},{b["s"]:.3f});')
        tl.append(f'tl.to("#{cid} .chap",{{xPercent:-130,duration:0.25,ease:"power3.in"}},{b["s"] + d - 0.26:.3f});')
# white flash on first frame
clip("flash", 0, 0.4, "", "flash"); tl.append('tl.fromTo("#flash",{opacity:0.9},{opacity:0,duration:0.38,ease:"power2.out"},0);')
# hook
hk = spec["hook"]; hd = T["bounds"][0]["e"] + (0.6 if len(T["bounds"]) < 2 or "chapter" not in T["bounds"][1] else 0.0); hd = max(hd, 1.6)
clip("hook", 0, hd, f'<div class="kick">{H.escape(hk["kicker"])}</div><div class="h1">{H.escape(hk["l1"])}</div><div class="h2">{H.escape(hk["l2"])}</div>', "hookwrap")
tl.append('tl.from("#hook .kick",{scaleX:0,transformOrigin:"0 50%",duration:0.3,ease:"power3.out"},0.05);')
tl.append('tl.from("#hook .h1",{scale:2.2,opacity:0,duration:0.32,ease:"power4.out"},0.12);')
tl.append('tl.from("#hook .h2",{scale:2.2,opacity:0,duration:0.32,ease:"power4.out"},0.42);')
tl.append('tl.to("#hook .h2",{x:6,duration:0.05,yoyo:true,repeat:5,ease:"none"},0.74);')
tl.append(f'tl.to("#hook",{{opacity:0,scale:0.9,duration:0.25,ease:"power2.in"}},{hd - 0.25:.3f});')
sfx("pop", 0.42, 0.35)
# ERA logo always on screen (brand visibility)
clip("logo", 0, VID, '<img src="assets/era.png" alt="ERA" />', "logowrap")
tl.append('tl.from("#logo img",{scale:0,duration:0.4,ease:"back.out(2)"},0.2);')
# name tags
for nt in spec.get("names", []):
    b = T["bounds"][nt["t_shot"]]; t0 = b["s"] + nt.get("at", 0.3); nid = "nm" + re.sub(r"\W", "", nt["name"])
    clip(nid, t0, 2.6, f'<div class="name"><b>{H.escape(nt["name"])}</b><span>{H.escape(nt["role"])}</span></div>', "namewrap")
    tl.append(f'tl.from("#{nid} b",{{xPercent:-110,duration:0.3,ease:"power4.out"}},{t0:.3f});')
    tl.append(f'tl.from("#{nid} span",{{xPercent:-110,duration:0.3,ease:"power4.out"}},{t0 + 0.1:.3f});')
    tl.append(f'tl.to("#{nid}",{{opacity:0,duration:0.25}},{t0 + 2.35:.3f});')
# captions
ws = []
for w in T["words"]:
    if ws and re.match(r"^[-.,]\w", w["w"]) and w["s"] - ws[-1]["e"] < 0.4: ws[-1] = {**ws[-1], "w": ws[-1]["w"] + w["w"], "e": w["e"]}
    else: ws.append(dict(w))
groups, g = [], []
for w in ws:
    if g and (g[-1].get("shot") != w.get("shot") or len(g) >= 3 or sum(len(x["w"]) for x in g) + len(w["w"]) > 15 or w["s"] - g[-1]["e"] > 0.3): groups.append(g); g = []
    g.append(w)
    if re.search(r"[.?!,]$", w["w"]): groups.append(g); g = []
if g: groups.append(g)
for i, g in enumerate(groups):
    st = g[0]["s"]; en = groups[i + 1][0]["s"] if i + 1 < len(groups) else VID; en = min(en, g[-1]["e"] + 0.5)
    sb = next((b["e"] for b in T["bounds"] if b["s"] <= st < b["e"]), VID); en = min(en, sb)
    sp = []
    for j, w in enumerate(g):
        txt = re.sub(r"[.,]$", "", w["w"]); core = re.sub(r"[^\w'-]", "", txt)
        if core in FIX: txt = txt.replace(core, FIX[core])
        cls = "w k" if core.lower() in KEY else "w"
        sp.append(f'<span id="c{i}_{j}" class="{cls}">{H.escape(txt)}</span>')
        tl.append(f'tl.fromTo("#c{i}_{j}",{{scale:1}},{{scale:1.14,duration:0.08,yoyo:true,repeat:1,ease:"power2.out",immediateRender:false}},{max(w["s"], st):.3f});')
        tl.append(f'tl.set("#c{i}_{j}",{{className:"{cls} on"}},{max(w["s"], st):.3f});')
    clip(f"cap{i}", st, max(0.2, en - st), f'<div class="cap">{" ".join(sp)}</div>', "capwrap")
    tl.append(f'tl.from("#cap{i} .cap",{{scale:0.6,opacity:0,duration:0.16,ease:"back.out(2.4)"}},{st:.3f});')
# end card
clip("end", VID - 0.25, END + 0.25, f'''<div class="end-in">
<img class="e-logo" src="assets/era.png" alt="ERA"/>
<div class="e-k">DARI UDARA KE UDARA</div><div class="e-big">14,000 KAKI</div>
<div class="e-tag">#ERARadioNo1PalingLegit</div>
<div class="e-sp"><span>CABARAN BE BOLD</span><i></i><img src="assets/mbsb.svg" alt="MBSB Bank"/><b>&times;</b><em>ERA</em></div></div>''', "endcard")
tl.append(f'tl.from("#end",{{clipPath:"inset(0 0 100% 0)",duration:0.35,ease:"power3.inOut"}},{VID - 0.25:.3f});')
tl.append(f'tl.from("#end .e-logo",{{scale:0,duration:0.45,ease:"back.out(2)"}},{VID + 0.1:.3f});')
tl.append(f'tl.from("#end .e-k, #end .e-big",{{y:60,opacity:0,duration:0.35,stagger:0.12,ease:"power3.out"}},{VID + 0.3:.3f});')
tl.append(f'tl.from("#end .e-tag, #end .e-sp",{{opacity:0,y:20,duration:0.35,stagger:0.15}},{VID + 0.8:.3f});')
sfx("whoosh", VID - 0.35, 0.45); sfx("impact", VID + 0.3, 0.45)
audio = "\n".join(f'<audio id="sfx{i}" class="clip" data-start="{t:.3f}" data-duration="{d}" data-volume="{v}" src="assets/sfx/{n}.wav"></audio>'
                  for i, (n, t, v, d) in enumerate(SFX))
CSS = open(f"{B}/era_style.css").read()
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
