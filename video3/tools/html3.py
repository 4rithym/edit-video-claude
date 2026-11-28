"""Hyperframes composition: WhatsApp trojan ZIP awareness video (9:16, 48 s)."""
import sys
S = sys.argv[1]; P = f"{S}/hf/trojan"
TOTAL = 48.0
parts, tl, SFX = [], [], []
def sfx(n, t, v=0.4, d=1.4): SFX.append((n, max(0, t), v, d))
def clip(id_, s, d, inner, cls="", style=""):
    return f'<div id="{id_}" class="clip {cls}" data-start="{s:.3f}" data-duration="{d:.3f}" style="{style}">{inner}</div>'
def flash(id_, t, color, dur=0.3, peak=0.8):
    parts.append(clip(id_, t, dur, "", "flash", f"background:{color}"))
    tl.append(f'tl.fromTo("#{id_}",{{opacity:{peak}}},{{opacity:0,duration:{dur},ease:"power2.out"}},{t:.3f});')
def A(sel, vars_, t): tl.append(f'tl.from("{sel}",{{{vars_}}},{t:.3f});')
def TO(sel, vars_, t): tl.append(f'tl.to("{sel}",{{{vars_}}},{t:.3f});')
def scene(id_, s, e, inner):
    parts.append(clip(id_, s, e - s, inner, "scene"))
    TO(f"#{id_} .sc", "opacity:0,y:-60,duration:0.25,ease:'power2.in'", e - 0.27)

WARN = '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path d="M12 2L1 21h22z" fill="#FFD400" stroke="#000" stroke-width="1.2" stroke-linejoin="round"/><path d="M12 9v5" stroke="#000" stroke-width="2.4" stroke-linecap="round"/><circle cx="12" cy="17.3" r="1.4" fill="#000"/></svg>'
SHIELD = '<svg viewBox="0 0 24 24" width="220" height="220"><path d="M12 1.5l8.5 3.2v6.6c0 5.3-3.6 9.7-8.5 11.2-4.9-1.5-8.5-5.9-8.5-11.2V4.7z" fill="#22c55e"/><path d="M7.6 12.2l3.1 3.1 5.9-6.4" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ZIPI = '<svg viewBox="0 0 64 80" width="150" height="188"><path d="M4 4h38l18 18v54H4z" fill="#e8ecf3"/><path d="M42 4v18h18" fill="#b9c3d4"/><rect x="26" y="4" width="8" height="40" fill="#8492a8"/><g fill="#e8ecf3"><rect x="26" y="8" width="4" height="4"/><rect x="30" y="14" width="4" height="4"/><rect x="26" y="20" width="4" height="4"/><rect x="30" y="26" width="4" height="4"/></g><rect x="22" y="44" width="16" height="12" rx="2" fill="#5b6b85"/><text x="32" y="72" font-size="13" font-weight="900" text-anchor="middle" fill="#12233f" font-family="sans-serif">ZIP</text></svg>'

# global background + moving grid
parts.append(f'<div id="bg" class="clip" data-start="0" data-duration="{TOTAL}"><div id="grid"></div><div id="vign"></div></div>')
tl.append(f'tl.fromTo("#grid",{{y:0}},{{y:-480,duration:{TOTAL},ease:"none"}},0);')
parts.append(f'<audio id="music" class="clip" data-start="0" data-duration="{TOTAL}" data-volume="0.75" src="assets/music.wav"></audio>')

# ---------- S1 HOOK 0-4 ----------
scene("s1", 0, 4.0, f'''<div class="sc s1">
  <div class="alert">{WARN.format(s=88)}<span>AMARAN</span></div>
  <div class="big red">JANGAN<br>BUKA FAIL NI!</div>
  <div class="evi"><img src="assets/ev/z1.png" /></div>
  <div class="sub">Trojan WhatsApp sedang tersebar</div></div>''')
flash("f0", 0, "#ff1f1f", 0.5, 0.75)
A("#s1 .alert", "y:-200,opacity:0,duration:0.3,ease:'back.out(2)'", 0.05)
A("#s1 .big", "scale:2.5,opacity:0,duration:0.3,ease:'power4.out'", 0.25)
TO("#s1 .big", "x:10,duration:0.05,yoyo:true,repeat:7,ease:'none'", 0.6)
A("#s1 .evi", "y:500,rotation:8,opacity:0,duration:0.45,ease:'back.out(1.6)'", 0.9)
TO("#s1 .evi", "scale:1.05,duration:0.4,yoyo:true,repeat:3,ease:'sine.inOut'", 1.4)
A("#s1 .sub", "opacity:0,y:30,duration:0.3", 1.6)
sfx("impact", 0, 0.5); sfx("pop", 0.25, 0.4); sfx("whoosh", 0.85, 0.35); sfx("click", 1.6, 0.4)

# ---------- S2 TIMELINE 4-11 ----------
cards = [("z5", "2:38"), ("z1", "2:40"), ("z3", "2:40"), ("z2", "2:42"), ("z6", "2:42")]
cardhtml = "".join(f'<div class="ev ev{i}"><div class="tm">{tm} PTG</div><img src="assets/ev/{z}.png" /></div>' for i, (z, tm) in enumerate(cards))
scene("s2", 4.0, 11.0, f'''<div class="sc s2">
  <div class="date">27 NOV 2026 &middot; 2:38 PTG</div>
  <div class="h1">WhatsApp <span class="y">Harith</span><br><span class="red">DIGODAM</span></div>
  <div class="stack">{cardhtml}</div>
  <div class="note">Dalam <b>~4 minit</b>, mesej &amp; fail yang sama<br>dihantar kepada <b>ramai kenalan</b></div></div>''')
A("#s2 .date", "x:-700,duration:0.35,ease:'power3.out'", 4.05)
A("#s2 .h1", "scale:0.5,opacity:0,duration:0.35,ease:'back.out(2)'", 4.3)
for i in range(len(cards)):
    t = 5.0 + i * 0.55
    A(f"#s2 .ev{i}", "x:900,rotation:10,opacity:0,duration:0.35,ease:'power3.out'", t)
    sfx("pop", t, 0.35)
A("#s2 .note", "opacity:0,y:40,duration:0.35", 8.0)
sfx("whoosh", 3.9, 0.4); sfx("ding", 8.0, 0.25)

# ---------- S3 TANDA-TANDA 11-21 ----------
signs = [
    ("1", "Arahan formal tentang <b>&lsquo;Finance&rsquo;</b> &mdash; bukan gaya kawan anda"),
    ("2", "Fail <b>.ZIP</b> bernama pelik (4 MB) &mdash; tiada penjelasan"),
    ("3", "Datang dari nombor <b>kawan sendiri</b>, jadi mudah dipercayai"),
    ("4", "Auto-reply masih berjalan &rarr; ini <b>akaun sebenar</b> yang dirampas, bukan nombor palsu"),
]
signhtml = "".join(f'<div class="sign sg{i}"><div class="num">{n}</div><div>{t}</div></div>' for i, (n, t) in enumerate(signs))
scene("s3", 11.0, 21.0, f'''<div class="sc s3">
  <div class="tag2">KENAL PASTI TANDA-TANDANYA</div>
  <div class="msg"><img src="assets/ev/msg.png" /><img src="assets/ev/z3.png" /></div>
  <div class="signs">{signhtml}</div></div>''')
A("#s3 .tag2", "y:-120,opacity:0,duration:0.3,ease:'back.out(2)'", 11.05)
A("#s3 .msg", "scale:0.7,opacity:0,duration:0.4,ease:'power3.out'", 11.3)
for i in range(4):
    t = 12.4 + i * 2.0
    A(f"#s3 .sg{i}", "x:-80,opacity:0,duration:0.3,ease:'back.out(2)'", t)
    sfx("pop", t, 0.4)
sfx("whoosh", 10.9, 0.4)

# ---------- S4 KENAPA BAHAYA 21-27 ----------
scene("s4", 21.0, 27.0, f'''<div class="sc s4">
  <div class="h1"><span class="red">KENAPA</span> BAHAYA?</div>
  <div class="zipbox"><div class="zipi">{ZIPI}</div>
    <div class="inside"><div class="f">statement.pdf<span class="red">.exe</span></div><div class="f">dokumen<span class="red">.apk</span></div><div class="f">invois<span class="red">.scr</span></div></div></div>
  <div class="hint">Fail berbahaya boleh <b>menyamar</b> sebagai dokumen</div>
  <div class="chain">
    <div class="node n0">Buka fail</div><div class="arr a0">&darr;</div>
    <div class="node n1">Peranti dijangkiti</div><div class="arr a1">&darr;</div>
    <div class="node n2">Akaun dirampas</div><div class="arr a2">&darr;</div>
    <div class="node n3 redn">Disebar ke kenalan <b>ANDA</b></div></div></div>''')
A("#s4 .h1", "scale:0.5,opacity:0,duration:0.3,ease:'back.out(2)'", 21.05)
A("#s4 .zipi", "y:-300,rotation:-20,duration:0.45,ease:'bounce.out'", 21.3)
for i in range(3): A(f"#s4 .inside .f:nth-child({i + 1})", "x:120,opacity:0,duration:0.25,ease:'power3.out'", 21.9 + i * 0.25)
A("#s4 .hint", "opacity:0,duration:0.3", 22.7)
for i in range(4):
    t = 23.3 + i * 0.7
    A(f"#s4 .n{i}", "scale:0,duration:0.28,ease:'back.out(2.5)'", t); sfx("click", t, 0.4)
    if i < 3: A(f"#s4 .a{i}", "opacity:0,y:-20,duration:0.2", t + 0.3)
sfx("whoosh", 20.9, 0.4); sfx("impact", 25.4, 0.35)

# ---------- S5 LINDUNGI 27-37 ----------
tips = [
    ("&#10060;", "<b>Jangan buka</b> fail .ZIP / .APK yang tak dijangka, walaupun dari kawan"),
    ("&#128222;", "<b>Call</b> kawan tu dulu untuk sahkan"),
    ("&#128274;", "Aktifkan <b>Pengesahan Dua Langkah</b><small>Tetapan &rsaquo; Akaun &rsaquo; Pengesahan dua langkah</small>"),
    ("&#128187;", "Semak <b>Peranti Dipautkan</b>, log keluar yang tak dikenali<small>Tetapan &rsaquo; Peranti dipautkan</small>"),
    ("&#128273;", "<b>Jangan kongsi</b> kod 6-digit WhatsApp kepada sesiapa"),
]
tiphtml = "".join(f'<div class="tip tp{i}"><div class="ico">{ic}</div><div>{t}</div></div>' for i, (ic, t) in enumerate(tips))
scene("s5", 27.0, 37.0, f'''<div class="sc s5"><div class="tag2 green">LINDUNGI DIRI ANDA</div>{tiphtml}</div>''')
A("#s5 .tag2", "scale:0,duration:0.3,ease:'back.out(2.5)'", 27.05)
for i in range(5):
    t = 27.6 + i * 1.75
    A(f"#s5 .tp{i}", "x:-900,duration:0.35,ease:'power3.out'", t); sfx("pop", t, 0.4)
flash("f5", 27.0, "#22c55e", 0.4, 0.5); sfx("ding", 27.05, 0.35)

# ---------- S6 DAH TERBUKA 37-44 ----------
steps = ["Putuskan internet (Wi-Fi &amp; data)", "Imbas peranti dengan antivirus", "Tukar kata laluan penting dari <b>peranti lain</b>", "Maklumkan kenalan: <b>&ldquo;Jangan buka fail dari saya&rdquo;</b>"]
sthtml = "".join(f'<div class="step st{i}"><div class="num">{i + 1}</div><div>{s}</div></div>' for i, s in enumerate(steps))
scene("s6", 37.0, 44.0, f'''<div class="sc s6"><div class="h1">DAH <span class="red">TERBUKA?</span></div>{sthtml}
  <div class="report"><div class="rh">LAPORKAN</div>
    <div class="rl"><b>Cyber999</b> (CyberSecurity Malaysia)<br><span class="y">1-300-88-2999</span></div>
    <div class="rl">Hilang wang? <b>NSRC</b> <span class="y">997</span></div></div></div>''')
A("#s6 .h1", "scale:0.5,opacity:0,duration:0.3,ease:'back.out(2)'", 37.05)
for i in range(4):
    t = 37.5 + i * 0.9
    A(f"#s6 .st{i}", "x:-80,opacity:0,duration:0.3,ease:'back.out(2)'", t); sfx("click", t, 0.4)
A("#s6 .report", "y:400,duration:0.45,ease:'power3.out'", 41.3)
flash("f6", 37.0, "#ff1f1f", 0.35, 0.45); sfx("whoosh", 36.9, 0.4); sfx("ding", 41.4, 0.3)

# ---------- S7 CTA 44-48 ----------
parts.append(clip("s7", 44.0, TOTAL - 44.0, f'''<div class="sc s7">{SHIELD}
  <div class="big">KONGSI<br>VIDEO INI</div>
  <div class="sub">Selamatkan kawan &amp; keluarga anda</div>
  <div class="hash">#JanganBukaZIP</div></div>''', "scene"))
A("#s7 svg", "scale:0,rotation:-30,duration:0.5,ease:'back.out(2)'", 44.05)
A("#s7 .big", "y:60,opacity:0,duration:0.35", 44.4)
A("#s7 .sub", "opacity:0,duration:0.3", 44.8)
A("#s7 .hash", "scale:0,duration:0.35,ease:'back.out(2.5)'", 45.2)
sfx("whoosh", 43.9, 0.4); sfx("impact", 44.05, 0.35); sfx("ding", 45.2, 0.35)

# progress bar
parts.append(f'<div id="prog" class="clip" data-start="0" data-duration="{TOTAL}"><div id="progfill"></div></div>')
tl.append(f'tl.fromTo("#progfill",{{scaleX:0}},{{scaleX:1,duration:{TOTAL},ease:"none"}},0);')

audio = "\n".join(f'<audio id="sfx{i}" class="clip" data-start="{t:.3f}" data-duration="{d}" data-volume="{v}" src="assets/sfx/{n}.wav"></audio>' for i, (n, t, v, d) in enumerate(SFX))
CSS = open(f"{S}/tools/style3.css").read()
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
