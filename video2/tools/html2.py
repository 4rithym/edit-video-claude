"""Hyperframes composition for video 2: osom POV -> zakatUniKL reveal."""
import sys
S = sys.argv[1]; P = f"{S}/hf/zakat2"
VID = 7.6; TOTAL = 10.0
parts, tl, SFX = [], [], []
def sfx(n, t, v=0.45, d=1.4): SFX.append((n, max(0, t), v, d))
def clip(id_, s, d, inner, cls="", style=""):
    return f'<div id="{id_}" class="clip {cls}" data-start="{s:.3f}" data-duration="{d:.3f}" style="{style}">{inner}</div>'
def wm(size): return f'<div class="wm" style="font-size:{size}px"><span class="wm-z">zakat</span><span class="wm-u">UniKL</span></div>'
def flash(id_, t, color, dur=0.3, peak=0.85):
    parts.append(clip(id_, t, dur, "", "flash", f"background:{color}"))
    tl.append(f'tl.fromTo("#{id_}",{{opacity:{peak}}},{{opacity:0,duration:{dur},ease:"power2.out"}},{t:.3f});')
def punch(t, s=1.15, hold=0.5, first=False):
    ir = "" if first else ",immediateRender:false"
    tl.append(f'tl.fromTo("#stage",{{scale:1}},{{scale:{s},duration:0.12,ease:"power3.out"{ir}}},{t:.3f});')
    tl.append(f'tl.to("#stage",{{scale:1,duration:0.35,ease:"power2.inOut"}},{t + hold:.3f});')

parts.append(f'''<div id="stage"><video id="vid" class="clip" data-start="0" data-duration="{VID}" muted src="assets/raw.mp4" playsinline></video></div>
<div id="shade" class="clip" data-start="0" data-duration="{VID}"></div>''')
parts.append(f'<audio id="music" class="clip" data-start="0" data-duration="{TOTAL}" data-volume="0.8" src="assets/music.wav"></audio>')

# Hook 0 - 2.8
parts.append(clip("hook", 0, 2.75, '''<div class="hook-l1">OSOM! YANG KALAH</div>
  <div class="hook-l2 h2b">BELANJA MAKAN!</div>''', "center-top", "top:90px"))
tl.append('tl.from("#hook .hook-l1",{y:-120,opacity:0,duration:0.22,ease:"back.out(2)"},0.0);')
tl.append('tl.from("#hook .hook-l2",{scale:2.4,opacity:0,rotation:-6,duration:0.25,ease:"power4.out"},0.2);')
tl.append('tl.to("#hook",{y:-420,opacity:0,duration:0.2,ease:"power2.in"},2.55);')
sfx("pop", 0.0, 0.4); sfx("impact", 0.2, 0.35)

# counts on the pumps
for i, (t, txt) in enumerate([(0.5, "1"), (1.167, "2"), (1.833, "3")]):
    parts.append(clip(f"cnt{i}", t, 0.62, f'<div class="count">{txt}</div>', "center-top", "top:1060px"))
    tl.append(f'tl.fromTo("#cnt{i} .count",{{scale:2.2,opacity:0}},{{scale:1,opacity:1,duration:0.16,ease:"power3.out"}},{t:.3f});')
    tl.append(f'tl.to("#cnt{i} .count",{{scale:0.6,opacity:0,duration:0.14}},{t + 0.46:.3f});')
parts.append(clip("osom", 2.5, 0.5, '<div class="count osom">OSOM!</div>', "center-top", "top:1030px"))
tl.append('tl.fromTo("#osom .count",{scale:3,opacity:0},{scale:1,opacity:1,duration:0.15,ease:"power4.out"},2.5);')
tl.append('tl.to("#osom .count",{scale:1.3,opacity:0,duration:0.15},2.83);')
punch(2.85, 1.18, 0.4, first=True); flash("fl1", 2.85, "#ffffff", 0.25, 0.7); sfx("impact", 2.85, 0.4)

# "tapi duit tinggal bulu" 3.0 - 3.95
parts.append(clip("bulu", 3.0, 0.95, '''<div class="hook-l1 small">TAPI DUIT TINGGAL</div><div class="hook-l2">&lsquo;BULU&rsquo;&hellip;</div>''', "center-top", "top:170px"))
tl.append('tl.from("#bulu .hook-l1",{y:-80,opacity:0,duration:0.18,ease:"back.out(2)"},3.0);')
tl.append('tl.from("#bulu .hook-l2",{scale:0,rotation:12,duration:0.25,ease:"back.out(2.5)"},3.15);')
tl.append('tl.to("#bulu .hook-l2",{y:30,rotation:-4,duration:0.5,ease:"sine.in"},3.4);')

# whip transition
sfx("whoosh", 3.82, 0.55); flash("fl2", 4.08, "#ffffff", 0.3, 0.8)

# reveal
parts.append(clip("risau", 4.3, 1.25, '<div class="banner"><span>JANGAN RISAU!</span></div>', "center-top", "top:170px"))
tl.append('tl.from("#risau .banner",{scale:0,rotation:-10,duration:0.3,ease:"back.out(2.4)"},4.3);')
tl.append('tl.to("#risau .banner",{scale:0,opacity:0,duration:0.18},5.35);')
sfx("pop", 4.3, 0.45)
parts.append(clip("mohon", 5.4, VID - 5.4, '<div class="sticker" style="background:#22c55e;color:#fff;transform:rotate(-3deg)">MOHON ZAKAT UniKL!</div>', "center-top", "top:190px"))
tl.append('tl.from("#mohon .sticker",{scale:0,duration:0.3,ease:"back.out(2.5)"},5.4);')
sfx("ding", 5.45, 0.4)
ARROW = '<svg viewBox="0 0 120 80" width="190" height="126"><path d="M115 40H30M30 40l26-26M30 40l26 26" stroke="#FFD400" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
parts.append(clip("arrow", 5.0, VID - 5.0, f'<div class="arrow">{ARROW}<div class="arrow-t">WEBSITE<br>ZAKAT UniKL</div></div>', "", "left:640px;top:1020px"))
tl.append('tl.from("#arrow .arrow",{x:300,opacity:0,duration:0.3,ease:"power3.out"},5.0);')
tl.append('tl.to("#arrow svg",{x:-28,duration:0.3,yoyo:true,repeat:7,ease:"sine.inOut"},5.3);')
sfx("pop", 5.0, 0.35)
parts.append(clip("lower", 5.8, VID - 5.8, f'<div class="card brand-card lowcard">{wm(84)}<div class="tagline">Memikul Amanah, Membantu Ummah</div></div>', "center-top", "top:1540px"))
tl.append('tl.from("#lower .card",{y:400,duration:0.4,ease:"power3.out"},5.8);')
sfx("whoosh", 5.65, 0.3)

# end card
parts.append(clip("end", VID, TOTAL - VID, f'''<div class="end-in">{wm(150)}
  <div class="tagline big">Memikul Amanah, Membantu Ummah</div>
  <div class="pill">Dibuka Disember ini &middot; Semua student UniKL</div>
  <div class="end-s">Menang atau kalah osom &mdash; jangan risau!</div></div>''', "endcard"))
tl.append(f'tl.from("#end .wm",{{scale:0.4,opacity:0,duration:0.45,ease:"back.out(1.8)"}},{VID + 0.05});')
tl.append(f'tl.from("#end .tagline",{{y:40,opacity:0,duration:0.3}},{VID + 0.35});')
tl.append(f'tl.from("#end .pill",{{scale:0,duration:0.3,ease:"back.out(2)"}},{VID + 0.6});')
tl.append(f'tl.from("#end .end-s",{{opacity:0,y:20,duration:0.3}},{VID + 0.9});')
sfx("whoosh", VID - 0.25, 0.4); sfx("ding", VID + 0.1, 0.35)

parts.append(f'<div id="prog" class="clip" data-start="0" data-duration="{VID}"><div id="progfill"></div></div>')
tl.append(f'tl.fromTo("#progfill",{{scaleX:0}},{{scaleX:1,duration:{VID},ease:"none"}},0);')

audio = "\n".join(f'<audio id="sfx{i}" class="clip" data-start="{t:.3f}" data-duration="{d}" data-volume="{v}" src="assets/sfx/{n}.wav"></audio>' for i, (n, t, v, d) in enumerate(SFX))
CSS = open(f"{S}/tools/style.css").read() + """
.count{font-weight:900;font-size:260px;line-height:1;color:#FFD400;-webkit-text-stroke:18px #000;paint-order:stroke fill;text-shadow:0 14px 40px rgba(0,0,0,.6)}
.count.osom{font-size:230px;color:#fff;-webkit-text-stroke:20px #ff3b30}
.h2b{font-size:128px;color:#FFD400;-webkit-text-stroke:16px #000}
.hook-l1.small{font-size:80px}
.lowcard{padding:30px 54px}
.arrow{display:flex;flex-direction:column;align-items:flex-start;gap:8px}
.arrow-t{font-weight:900;font-size:50px;line-height:1.02;color:#fff;-webkit-text-stroke:10px #000;paint-order:stroke fill}
.end-s{margin-top:34px;font-weight:700;font-size:40px;color:#dbe4f3}
"""
doc = f'''<!doctype html>
<html lang="ms" data-resolution="portrait">
<head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script><style>{CSS}</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{chr(10).join(parts)}
{audio}
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
print("ok", len(SFX), "sfx")
