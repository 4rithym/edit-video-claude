import json, sys, html as H
S = sys.argv[1]; P = f"{S}/hf/zakat"
C = json.load(open(f"{S}/src/captions.json"))
E = json.load(open(f"{S}/src/events.json"))
VID, TOTAL = E["vid"], E["total"]
KEY = {"zakat", "unikl", "mohon", "bantuan", "bayar", "daftar", "bertuah", "12", "student",
       "website", "platform", "bulu", "mampu", "akaun"}

def clip(id_, start, dur, inner, cls="", style=""):
    return (f'<div id="{id_}" class="clip {cls}" data-start="{start:.3f}" data-duration="{dur:.3f}" '
            f'style="{style}">{inner}</div>')

SFX = []
def sfx(name, t, vol=0.45, dur=1.2):
    SFX.append((name, max(0, t), vol, dur))

ICON = {
 "check": '<svg viewBox="0 0 24 24" width="44" height="44"><circle cx="12" cy="12" r="12" fill="#22c55e"/><path d="M6.5 12.5l3.5 3.5 7.5-8" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "rewind": '<svg viewBox="0 0 24 24" width="46" height="46"><path d="M11 6v12L2 12zM21 6v12l-9-6z" fill="#FFD400"/></svg>',
 "bell": '<svg viewBox="0 0 24 24" width="120" height="120"><path d="M12 2a1.5 1.5 0 0 1 1.5 1.5v.6A6.5 6.5 0 0 1 18.5 10.5v4.2l2 2.3v1H3.5v-1l2-2.3v-4.2a6.5 6.5 0 0 1 5-6.4v-.6A1.5 1.5 0 0 1 12 2zm-2.2 18h4.4a2.2 2.2 0 0 1-4.4 0z" fill="#FFD400"/></svg>',
 "mega": '<svg viewBox="0 0 24 24" width="64" height="64"><path d="M3 10v4h3l6 4V6L6 10zM15 8.5v7a4 4 0 0 0 0-7zM15 4.6v2.1a6.5 6.5 0 0 1 0 10.6v2.1a8.5 8.5 0 0 0 0-14.8z" fill="#12233f"/></svg>',
}

def wordmark(size):
    return (f'<div class="wm" style="font-size:{size}px"><span class="wm-z">zakat</span>'
            f'<span class="wm-u">UniKL</span></div>')

parts = []
tl = []  # js lines

# ---------- video ----------
parts.append(f'''<div id="stage">
  <video id="vid" class="clip" data-start="0" data-duration="{VID:.3f}" data-has-audio="true" data-volume="1" src="assets/cut.mp4" playsinline></video>
</div>
<div id="shade" class="clip" data-start="0" data-duration="{VID:.3f}"></div>''')

# zoom punches on the stage (scale only, seek-safe)
def punch(t, s=1.14, hold=0.9):
    tl.append(f'tl.fromTo("#stage",{{scale:1}},{{scale:{s},duration:0.18,ease:"power3.out",immediateRender:false}},{t:.3f});')
    tl.append(f'tl.to("#stage",{{scale:1,duration:0.5,ease:"power2.inOut"}},{t+hold:.3f});')

def flash(id_, t, color, dur=0.35, peak=0.85):
    parts.append(clip(id_, t, dur, "", "flash", f"background:{color}"))
    tl.append(f'tl.fromTo("#{id_}",{{opacity:{peak}}},{{opacity:0,duration:{dur:.2f},ease:"power2.out"}},{t:.3f});')

# ---------- HOOK (0 - hookend) ----------
he = E["hookend"]
tl.append(f'tl.fromTo("#stage",{{scale:1.0}},{{scale:1.22,duration:{he:.2f},ease:"none"}},0);')
tl.append(f'tl.set("#stage",{{scale:1}},{he:.3f});')
flash("fl0", 0, "#ff2d2d", 0.45, 0.7)
parts.append(clip("hook", 0, he, '''
  <div class="hook-l1">DUIT TINGGAL</div>
  <div class="hook-l2">&lsquo;BULU&rsquo;?!</div>
  <div class="hook-l3">Ini penyelesaian untuk student UniKL</div>''', "center-top", "top:210px"))
tl.append('tl.from("#hook .hook-l1",{y:-120,opacity:0,duration:0.25,ease:"back.out(2)"},0.02);')
tl.append('tl.from("#hook .hook-l2",{scale:2.6,opacity:0,rotation:-8,duration:0.28,ease:"power4.out"},0.18);')
tl.append('tl.to("#hook .hook-l2",{rotation:3,duration:0.06,yoyo:true,repeat:5,ease:"none"},0.46);')
tl.append('tl.from("#hook .hook-l3",{y:40,opacity:0,duration:0.3,ease:"power2.out"},0.9);')
sfx("impact", 0.0, 0.55); sfx("coin", 0.25, 0.3); sfx("whoosh", 0.88, 0.25)
# transition out of hook
sfx("rewind", he - 0.32, 0.4); sfx("whoosh", he - 0.15, 0.4)
flash("fl1", he, "#ffffff", 0.3, 0.9)
parts.append(clip("rew", he, 2.2, f'<div class="tag">{ICON["rewind"]}<span>SEBELUM TU&hellip;</span></div>', "", "left:60px;top:140px"))
tl.append(f'tl.from("#rew .tag",{{x:-500,duration:0.35,ease:"power3.out"}},{he+0.05:.3f});')
tl.append(f'tl.to("#rew .tag",{{x:-600,opacity:0,duration:0.3,ease:"power2.in"}},{he+1.85:.3f});')

# ---------- sticker helper ----------
def sticker(id_, t, dur, text, bg, fg, pos, rot=-6, snd="pop"):
    parts.append(clip(id_, t, dur, f'<div class="sticker" style="background:{bg};color:{fg};transform:rotate({rot}deg)">{text}</div>', "", pos))
    tl.append(f'tl.from("#{id_} .sticker",{{scale:0,duration:0.3,ease:"back.out(2.5)"}},{t:.3f});')
    tl.append(f'tl.to("#{id_} .sticker",{{scale:0,opacity:0,duration:0.2,ease:"power2.in"}},{t+dur-0.22:.3f});')
    if snd: sfx(snd, t, 0.45)

sticker("st_fail", E["failexam"] - 0.1, 1.9, "FAIL EXAM?", "#ff3b30", "#fff", "right:70px;top:300px", 7)

# Allahuakbar moment
ta = E["allah"]
punch(ta, 1.2, 0.8); sfx("impact", ta - 0.02, 0.5); flash("fl2", ta, "#ff2d2d", 0.3, 0.45)
sticker("st_bulu", ta + 0.35, 2.6, "BAKI: TINGGAL &lsquo;BULU&rsquo;!", "#FFD400", "#111", "left:60px;top:260px", -5, "coin")

# ---------- brand card ----------
tp = E["platform"]
parts.append(clip("brand", tp - 0.1, 3.5, f'''<div class="card brand-card">{wordmark(118)}
  <div class="tagline">Memikul Amanah, Membantu Ummah</div></div>''', "center-top", "top:330px"))
tl.append(f'tl.from("#brand .card",{{y:-260,scale:0.6,opacity:0,duration:0.45,ease:"back.out(1.8)"}},{tp - 0.08:.3f});')
tl.append(f'tl.from("#brand .tagline",{{opacity:0,y:20,duration:0.3}},{tp + 0.4:.3f});')
tl.append(f'tl.to("#brand .card",{{y:-300,opacity:0,duration:0.3,ease:"power2.in"}},{tp + 3.1:.3f});')
sfx("whoosh", tp - 0.25, 0.4); sfx("ding", tp + 0.2, 0.35)

# ---------- feature checklist ----------
items = [("mohon", "Mohon Bantuan"), ("login", "Log In Akaun"), ("daftar", "Daftar Akaun Baharu"),
         ("bayar", "Bayar Zakat"), ("isi", "Isi Maklumat Diri")]
c0 = E["mohon"] - 0.25; c1 = E["scene"] - 0.05
lis = "".join(f'<div class="li" id="li{i}">{ICON["check"]}<span>{t}</span></div>' for i, (_, t) in enumerate(items))
parts.append(clip("list", c0, c1 - c0, f'<div class="card list-card"><div class="list-h">DALAM {wordmark(46)} BOLEH:</div>{lis}</div>', "", "left:50px;top:150px"))
tl.append(f'tl.from("#list .card",{{x:-700,duration:0.4,ease:"power3.out"}},{c0:.3f});')
for i, (k, _) in enumerate(items):
    t = E[k]
    tl.append(f'tl.from("#li{i}",{{x:-60,opacity:0,scale:0.7,duration:0.28,ease:"back.out(2)"}},{t:.3f});')
    sfx("pop", t, 0.4)
tl.append(f'tl.to("#list .card",{{x:-760,duration:0.3,ease:"power2.in"}},{c1 - 0.32:.3f});')
sfx("whoosh", c0 - 0.15, 0.3)

# ---------- scene change ----------
ts = E["scene"]
flash("fl3", ts, "#ffffff", 0.35, 0.95); sfx("whoosh", ts - 0.2, 0.45)
tb = E["assalam"] + 0.2
parts.append(clip("annc", tb, 3.6, f'<div class="banner">{ICON["mega"]}<span>WARGA UniKL,<br>DENGAR SINI!</span></div>', "center-top", "top:230px"))
tl.append(f'tl.from("#annc .banner",{{scale:0,rotation:-10,duration:0.35,ease:"back.out(2.2)"}},{tb:.3f});')
tl.append(f'tl.to("#annc .banner",{{rotation:2,duration:0.08,yoyo:true,repeat:3}},{tb + 0.4:.3f});')
tl.append(f'tl.to("#annc .banner",{{scale:0,opacity:0,duration:0.22}},{tb + 3.35:.3f});')
sfx("pop", tb, 0.45)

# ---------- website card ----------
tw = E["website"] - 0.15
parts.append(clip("web", tw, 5.0, f'''<div class="browser">
  <div class="bar"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i><i style="background:#28c840"></i><div class="url">Website Zakat UniKL</div></div>
  <div class="bbody">{wordmark(96)}<div class="b-h">Memikul Amanah,<br>Membantu Ummah</div><div class="btn">MOHON SEKARANG</div></div></div>''', "center-top", "top:200px"))
tl.append(f'tl.from("#web .browser",{{y:500,opacity:0,scale:0.8,duration:0.5,ease:"power3.out"}},{tw:.3f});')
tl.append(f'tl.from("#web .btn",{{scale:0,duration:0.35,ease:"back.out(3)"}},{tw + 0.9:.3f});')
tl.append(f'tl.to("#web .btn",{{scale:1.08,duration:0.35,yoyo:true,repeat:5,ease:"sine.inOut"}},{tw + 1.3:.3f});')
tl.append(f'tl.to("#web .browser",{{y:-700,opacity:0,duration:0.35,ease:"power2.in"}},{tw + 4.6:.3f});')
sfx("whoosh", tw - 0.1, 0.35); sfx("ding", tw + 0.35, 0.35); sfx("click", tw + 0.9, 0.5)

# ---------- tak mampu ----------
tm = E["tidak"]
sticker("st_mampu", tm - 0.1, 1.6, "TAK MAMPU?", "#ff3b30", "#fff", "right:70px;top:300px", 6)
sticker("st_mohon", tm + 1.0, 2.5, "MOHON ZAKAT UniKL!", "#22c55e", "#fff", "left:60px;top:470px", -4, "ding")

# ---------- bulan 12 ----------
tc = E["bulan"]
parts.append(clip("cal", tc - 0.1, 5.9, '''<div class="cal"><div class="cal-top">DISEMBER</div><div class="cal-num">12</div></div>
  <div class="cal-cap">DIBUKA KEPADA<br><b>SELURUH STUDENT!</b></div>''', "center-top", "top:180px"))
tl.append(f'tl.from("#cal .cal",{{y:-600,rotation:-20,duration:0.5,ease:"bounce.out"}},{tc - 0.1:.3f});')
tl.append(f'tl.from("#cal .cal-cap",{{scale:0,opacity:0,duration:0.35,ease:"back.out(2)"}},{tc + 2.5:.3f});')
tl.append(f'tl.to("#cal",{{y:-900,duration:0.35,ease:"power2.in"}},{tc + 5.45:.3f});')
sfx("riser", tc - 1.25, 0.3); sfx("impact", tc + 0.15, 0.45); sfx("ding", tc + 2.5, 0.35)
punch(tc + 0.15, 1.12, 1.2)

# ---------- CTA + end card ----------
tn = E["nanti"] - 0.2
parts.append(clip("cta", tn, VID - tn, f'<div class="cta">{ICON["bell"]}<div>NANTIKAN!</div></div>', "center-top", "top:330px"))
tl.append(f'tl.from("#cta .cta",{{scale:0,duration:0.4,ease:"back.out(2.5)"}},{tn:.3f});')
tl.append(f'tl.to("#cta svg",{{rotation:18,duration:0.1,yoyo:true,repeat:7,transformOrigin:"50% 10%"}},{tn + 0.4:.3f});')
sfx("pop", tn, 0.45); sfx("ding", tn + 0.4, 0.3)
parts.append(clip("end", VID, TOTAL - VID, f'''<div class="end-in">{wordmark(150)}
  <div class="tagline big">Memikul Amanah, Membantu Ummah</div>
  <div class="pill">Dibuka Disember ini &middot; Semua student UniKL</div></div>''', "endcard"))
tl.append(f'tl.from("#end .wm",{{scale:0.4,opacity:0,duration:0.5,ease:"back.out(1.8)"}},{VID + 0.05:.3f});')
tl.append(f'tl.from("#end .tagline",{{y:40,opacity:0,duration:0.35}},{VID + 0.4:.3f});')
tl.append(f'tl.from("#end .pill",{{scale:0,duration:0.35,ease:"back.out(2)"}},{VID + 0.7:.3f});')
sfx("whoosh", VID - 0.25, 0.45); sfx("ding", VID + 0.1, 0.4)

# ---------- captions ----------
for i, ch in enumerate(C):
    st, en = ch["st"], ch["en"]
    spans = []
    for j, w in enumerate(ch["w"]):
        k = w["w"].lower().strip(",.?!")
        cls = "w key" if k in KEY else "w"
        spans.append(f'<span id="c{i}w{j}" class="{cls}">{H.escape(w["w"])}</span>')
        tl.append(f'tl.fromTo("#c{i}w{j}",{{scale:1}},{{scale:1.08,duration:0.08}},{max(w["s"], st):.3f});')
        tl.append(f'tl.set("#c{i}w{j}",{{color:"#FFD400"}},{max(w["s"], st):.3f});')
    parts.append(clip(f"cap{i}", st, en - st, f'<div class="cap">{" ".join(spans)}</div>', "capwrap"))
    tl.append(f'tl.from("#cap{i} .cap",{{scale:0.75,y:24,opacity:0,duration:0.12,ease:"back.out(2)"}},{st:.3f});')

# progress bar
parts.append(f'<div id="prog" class="clip" data-start="0" data-duration="{VID:.3f}"><div id="progfill"></div></div>')
tl.append(f'tl.fromTo("#progfill",{{scaleX:0}},{{scaleX:1,duration:{VID:.3f},ease:"none"}},0);')

audio = "\n".join(
    f'<audio id="sfx{i}" class="clip" data-start="{t:.3f}" data-duration="{d}" data-volume="{v}" src="assets/sfx/{n}.wav"></audio>'
    for i, (n, t, v, d) in enumerate(SFX))

CSS = open(f"{S}/tools/style.css").read()
doc = f'''<!doctype html>
<html lang="ms" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL:.3f}" data-width="1080" data-height="1920">
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
</body>
</html>'''
open(f"{P}/index.html", "w").write(doc)
print("ok", len(parts), "parts", len(SFX), "sfx", TOTAL)
