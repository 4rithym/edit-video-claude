# HyperFrames composition for Fira Worldwide THE NEW ERA. Usage: fira_comp.py spec.json
import json, sys, os, re, shutil, html as H
B = os.path.dirname(os.path.abspath(__file__)); E = os.path.dirname(B) + "/fira"; REPO = "/home/user/edit-video-claude"
spec = json.load(open(sys.argv[1])); D = f"{E}/work/{spec['id']}"; P = f"{D}/hf"
T = json.load(open(f"{D}/timing.json"))
os.makedirs(f"{P}/assets/sfx", exist_ok=True)
if not os.path.exists(f"{P}/assets/fonts"): shutil.copytree(f"{REPO}/project/assets/fonts", f"{P}/assets/fonts")
shutil.copy(f"{E}/fonts/PlayfairDisplay-Italic.ttf", f"{P}/assets/fonts/")
for f in ("whoosh", "pop", "ding", "riser"): shutil.copy(f"{REPO}/project/assets/sfx/{f}.wav", f"{P}/assets/sfx/{f}.wav")
for f in ("logo.png", "poster_1920.jpg", "poster_bg.jpg", spec["banner"]): shutil.copy(f"{E}/assets/{f}", f"{P}/assets/{f}")
shutil.copy(f"{REPO}/project/assets/gsap.min.js", f"{P}/assets/gsap.min.js"); shutil.copy(f"{D}/cut.mp4", f"{P}/assets/cut.mp4")
VID = T["total"]; END = 4.5; TOTAL = VID + END; BAN = VID - 4.5
KEY = {k.lower() for k in spec.get("keywords", [])}
FIX = {"Fila": "Fira", "revestrate": "frustrate", "goal": "gold", "committee": "community", "SL": "SL", **spec.get("fix", {})}
parts, tl, SFX = [], [], []
def clip(id_, st, dur, inner, cls="", style=""):
    parts.append(f'<div id="{id_}" class="clip {cls}" data-start="{st:.3f}" data-duration="{dur:.3f}" style="{style}">{inner}</div>')
def sfx(name, t, vol=0.3, dur=1.5): SFX.append((name, max(0, t), vol, dur))
parts.append(f'<div id="stage"><video id="vid" class="clip" data-start="0" data-duration="{VID:.3f}" data-has-audio="true" '
             f'data-volume="1" src="assets/cut.mp4" playsinline></video></div>')
clip("shade", 0, VID, "")
# gentle push-ins, alternating framing on each cut
for i, b in enumerate(T["bounds"]):
    z = [1.0, 1.1, 1.04][i % 3]
    tl.append(f'tl.fromTo("#stage",{{scale:{z}}},{{scale:{z + 0.03:.3f},duration:{b["e"] - b["s"]:.3f},ease:"none",immediateRender:false}},{b["s"]:.3f});')
# hook title
hk = spec["hook"]
clip("hook", 0.15, 3.3, f'<div class="hk1">{H.escape(hk["l1"])}</div><div class="hk2">{H.escape(hk["l2"])}</div>', "hookwrap")
tl.append('tl.from("#hook .hk1",{opacity:0,y:30,duration:0.45,ease:"power3.out"},0.2);')
tl.append('tl.from("#hook .hk2",{opacity:0,y:30,duration:0.45,ease:"power3.out"},0.45);')
tl.append('tl.to("#hook",{opacity:0,duration:0.3},3.15);')
sfx("pop", 0.2, 0.22)
# brand marks
clip("logo", 0, VID, '<img src="assets/logo.png" alt="Fira Worldwide"/>', "logowrap")
clip("ne", 0, VID, '<div class="nepill"><b>THE NEW ERA</b><span>28 NOV &middot; KUALA LUMPUR</span></div>', "newrap")
tl.append('tl.from("#logo img, #ne .nepill",{opacity:0,y:-20,duration:0.5,stagger:0.1},0.1);')
# official banner over the last seconds of talk
clip("ban", BAN, VID - BAN, f'<img src="assets/{spec["banner"]}" alt="banner"/>', "banwrap")
tl.append(f'tl.from("#ban img",{{yPercent:30,opacity:0,duration:0.5,ease:"power3.out"}},{BAN:.3f});')
sfx("whoosh", BAN - 0.1, 0.25)
# captions
ws = []
for w in T["words"]:
    if ws and re.match(r"^[-.,]\w", w["w"]) and w["s"] - ws[-1]["e"] < 0.4: ws[-1] = {**ws[-1], "w": ws[-1]["w"] + w["w"], "e": w["e"]}
    else: ws.append(dict(w))
groups, g = [], []
for w in ws:
    if g and (len(g) >= 3 or sum(len(x["w"]) for x in g) + len(w["w"]) > 18 or w["s"] - g[-1]["e"] > 0.35): groups.append(g); g = []
    g.append(w)
    if re.search(r"[.?!,]$", w["w"]): groups.append(g); g = []
if g: groups.append(g)
for i, g in enumerate(groups):
    st = g[0]["s"]; en = groups[i + 1][0]["s"] if i + 1 < len(groups) else VID; en = min(en, g[-1]["e"] + 0.6, VID)
    sp = []
    for j, w in enumerate(g):
        txt = re.sub(r"[.,]$", "", w["w"]); core = re.sub(r"[^\w'$-]", "", txt)
        if core in FIX: txt = txt.replace(core, FIX[core])
        cls = "w k" if core.lower() in KEY else "w"
        sp.append(f'<span id="c{i}_{j}" class="{cls}">{H.escape(txt)}</span>')
        tl.append(f'tl.set("#c{i}_{j}",{{className:"{cls} on"}},{max(w["s"], st):.3f});')
    hi = " hi" if st >= BAN - 0.05 else ""
    clip(f"cap{i}", st, max(0.2, en - st), f'<div class="cap">{" ".join(sp)}</div>', "capwrap" + hi)
    tl.append(f'tl.from("#cap{i} .cap",{{y:14,opacity:0,duration:0.16,ease:"power2.out"}},{st:.3f});')
# closing card: date, location, CTA, official accounts
clip("end", VID - 0.3, END + 0.3, '''<img class="e-bg" src="assets/poster_bg.jpg" alt=""/>
<div class="end-in"><img class="e-poster" src="assets/poster_1920.jpg" alt="THE NEW ERA"/>
<div class="e-date">28 November 2026 &middot; Kuala Lumpur</div>
<div class="e-cta">DM Fira &ldquo;NEW ERA&rdquo;</div><div class="e-sub">untuk dapatkan seat</div>
<div class="e-acc"><span>IG @firaworldwide</span><span>TikTok @firaindicator</span></div></div>''', "endcard")
tl.append(f'tl.from("#end",{{opacity:0,duration:0.35}},{VID - 0.3:.3f});')
tl.append(f'tl.from("#end .e-poster",{{scale:0.85,opacity:0,duration:0.6,ease:"power3.out"}},{VID:.3f});')
tl.append(f'tl.from("#end .e-date, #end .e-cta, #end .e-sub, #end .e-acc",{{y:30,opacity:0,duration:0.4,stagger:0.15,ease:"power3.out"}},{VID + 0.35:.3f});')
sfx("ding", VID + 0.5, 0.25)
audio = "\n".join(f'<audio id="sfx{i}" class="clip" data-start="{t:.3f}" data-duration="{d}" data-volume="{v}" src="assets/sfx/{n}.wav"></audio>'
                  for i, (n, t, v, d) in enumerate(SFX))
CSS = open(f"{B}/fira_style.css").read()
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
