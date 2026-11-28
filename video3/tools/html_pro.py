"""Professional HyperFrames composition: WhatsApp trojan ZIP awareness (neural Malay VO)."""
import sys, json, html as H
S = sys.argv[1]; P = f"{S}/hf/trojan_pro"
D = json.load(open(f"{S}/v4/vo/cues.json")); C = D["cues"]; LINES = D["lines"]
TOTAL = C["end"]
SC = ["A", "B", "C", "D", "E", "F", "G", "H"]
def s_end(k): i = SC.index(k); return C[SC[i + 1]] if i + 1 < len(SC) else TOTAL
parts, tl, SFX = [], [], []
def sfx(n, t, v=0.2, d=1.4): SFX.append((n, max(0, t), v, d))
def clip(id_, s, d, inner, cls="", style=""):
    return f'<div id="{id_}" class="clip {cls}" data-start="{s:.3f}" data-duration="{d:.3f}" style="{style}">{inner}</div>'
def FROM(sel, v, t): tl.append(f'tl.from("{sel}",{{{v}}},{t:.3f});')
def TO(sel, v, t): tl.append(f'tl.to("{sel}",{{{v}}},{t:.3f});')
EO = "ease:'expo.out'"; P3 = "ease:'power3.out'"
def rise(sel, t, d=0.7, y=60): FROM(sel, f"y:{y},opacity:0,duration:{d},{EO}", t)
def mask(sel, t, d=0.8): FROM(sel, f"yPercent:110,duration:{d},{EO}", t)

# ---------- icons (line, 2px) ----------
def ic(path, s=48, col="#F4F5F7", sw=2.2):
    return f'<svg viewBox="0 0 24 24" width="{s}" height="{s}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{path}</svg>'
I = {
 "warn": '<path d="M12 3 2 20h20z"/><path d="M12 10v4"/><path d="M12 17h.01"/>',
 "clip": '<path d="M21 11.5 12.5 20a5 5 0 0 1-7-7L14 4.5a3.3 3.3 0 0 1 4.7 4.7l-8.5 8.5a1.7 1.7 0 0 1-2.4-2.4L15.5 7.6"/>',
 "chat": '<path d="M4 5h16v11H9l-5 4z"/>',
 "x": '<circle cx="12" cy="12" r="9"/><path d="m9 9 6 6M15 9l-6 6"/>',
 "phone": '<path d="M5 3h4l2 5-3 2a11 11 0 0 0 6 6l2-3 5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2z"/>',
 "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
 "laptop": '<rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 19h20"/>',
 "key": '<circle cx="8" cy="15" r="4"/><path d="m11 12 9-9M17 6l3 3M15 8l2 2"/>',
 "wifioff": '<path d="M2 8.5a16 16 0 0 1 4.5-2.8M10 5a16 16 0 0 1 12 3.5M5 12a11 11 0 0 1 5-2.6M14 9.6A11 11 0 0 1 19 12M8.5 15.5a6 6 0 0 1 7 0M12 19h.01M3 3l18 18"/>',
 "bug": '<rect x="7" y="7" width="10" height="13" rx="5"/><path d="M12 7v13M3 13h4M17 13h4M4 7l3 2M20 7l-3 2M4 19l3-2M20 19l-3-2M9 4l1.5 2M15 4l-1.5 2"/>',
 "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
 "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6.5 6.5 0 0 1 3.5 6"/>',
 "shield": '<path d="M12 2.5 20 6v6c0 5-3.4 8.6-8 9.5C7.4 20.6 4 17 4 12V6z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
 "scan": '<path d="M4 8V5a1 1 0 0 1 1-1h3M16 4h3a1 1 0 0 1 1 1v3M20 16v3a1 1 0 0 1-1 1h-3M8 20H5a1 1 0 0 1-1-1v-3M4 12h16"/>',
 "refresh": '<path d="M20 11a8 8 0 0 0-14.3-4.9L4 8M4 4v4h4M4 13a8 8 0 0 0 14.3 4.9L20 16M20 20v-4h-4"/>',
 "mega": '<path d="M3 11v3h3l7 4V7L6 11z"/><path d="M16.5 9a4 4 0 0 1 0 6"/>',
}

MSG = ("Sila forward statement of account di atas kepada bahagian Finance / Cashier syarikat anda.<br><br>"
       "Sila ambil perhatian: Jika anda bukan kakitangan bahagian Finance, sila serahkan dokumen tersebut kepada pihak Finance untuk semakan.<br><br>"
       "Terima kasih atas kerjasama anda.")
FNAME = "20261127134525.CC28C3AC.zip"
def phone(pid, autoreply=False, typing=False):
    ar = ('<div class="bub" id="%s-ar">Hi there! Thank you for messaging&hellip; I have received your message and will respond shortly.'
          '<div class="tm">2:41 PTG</div><div class="ring"></div></div>' % pid) if autoreply else ""
    ty = f'<div class="typing" id="{pid}-ty"><i></i><i></i><i></i></div>' if typing else ""
    return f'''<div class="phone" id="{pid}"><div class="screen"><div class="notch"></div>
  <div class="sbar"><span>2:40</span><span class="mono" style="font-size:20px">5G &#9646;&#9646;&#9646;</span></div>
  <div class="whead" id="{pid}-head"><svg width="22" height="34" viewBox="0 0 12 20"><path d="M10 2 2 10l8 8" stroke="#E9EDEF" stroke-width="2.4" fill="none" stroke-linecap="round"/></svg>
    <div class="ava">K</div><div><div class="wname">Kawan</div><div class="wsub">kenalan anda</div></div><div class="ring"></div></div>
  <div class="chat">{ty}
    <div class="bub" id="{pid}-msg">{MSG}<div class="tm">2:40 PTG</div><div class="ring"></div></div>
    <div class="bub" id="{pid}-file" style="padding:10px 10px 8px"><div class="file"><div class="fic">ZIP</div><div><div class="fname">{FNAME}</div><div class="fmeta">4.0 MB &middot; ZIP</div></div></div><div class="tm" style="padding-right:8px">2:40 PTG</div><div class="ring"></div><div class="ring red" id="{pid}-fred"></div></div>
    {ar}</div></div></div>'''

# ---------- background ----------
parts.append(f'<div id="bg" class="clip" data-start="0" data-duration="{TOTAL}"><div id="dots"></div></div>')
tl.append(f'tl.fromTo("#dots",{{y:0}},{{y:-400,duration:{TOTAL},ease:"none"}},0);')
parts.append(f'<audio id="music" class="clip" data-start="0" data-duration="{TOTAL}" data-volume="0.2" src="assets/music.wav"></audio>')
parts.append(f'<audio id="vo" class="clip" data-start="0" data-duration="{TOTAL}" data-volume="1" src="assets/vo.wav"></audio>')

# ---------- top bar + chapter progress ----------
CH = ["B", "C", "D", "E", "F", "G"]
segs = "".join(f'<div class="seg"><i id="sg{i}"></i></div>' for i in range(len(CH)))
parts.append(clip("topbar", 0, C["H"], f'<div class="tb-l"><span class="rec" id="rec"></span>AMARAN KESELAMATAN SIBER</div><div class="segs">{segs}</div>'))
FROM("#topbar", "opacity:0,y:-20,duration:0.6", 0.1)
tl.append('tl.to("#rec",{opacity:0.25,duration:0.6,yoyo:true,repeat:%d,ease:"sine.inOut"},0);' % int(C["H"] / 0.6))
for i, k in enumerate(CH):
    tl.append(f'tl.fromTo("#sg{i}",{{scaleX:0}},{{scaleX:1,duration:{s_end(k) - C[k]:.3f},ease:"none",immediateRender:false}},{C[k]:.3f});')
    parts.append(clip(f"chno{i}", C[k], s_end(k) - C[k], f'<div class="chno" style="position:absolute;right:0;top:0"><b>{i + 1:02d}</b> / {len(CH):02d}</div>', "", "left:80px;top:78px;width:920px;height:40px"))
    FROM(f"#chno{i} .chno", "y:20,opacity:0,duration:0.5," + EO, C[k] + 0.05)

def chapter(k, num, title):
    return f'<div class="chap"><div class="mask"><span class="k">{num} &mdash; BAB</span></div><h2 class="mask"><span>{title}</span></h2></div>'
def scene(k, inner):
    s, e = C[k], s_end(k)
    parts.append(clip(f"sc{k}", s, e - s, inner, "scene"))
    TO(f"#sc{k} .out", "opacity:0,y:-40,duration:0.35,ease:'power2.in'", e - 0.38)
    sfx("whoosh", s - 0.15, 0.16)
def chap_anim(k):
    mask(f"#sc{k} .chap .k", C[k] + 0.05); mask(f"#sc{k} .chap h2 span", C[k] + 0.15, 0.9)

# ---------- A: hook ----------
pa = phone("pa", typing=True)
scene("A", f'''<div class="out">
  <div class="wrap" style="top:190px"><div class="kick mask"><span>{ic(I["warn"],30,"#E5484D",2.6)}&nbsp;JANGAN BUKA FAIL INI</span></div>
    <div class="hl1 mask" id="hA1"><span>Mesej ini datang daripada</span></div><div class="hl1 mask" id="hA2"><span>nombor <em>kawan anda.</em></span></div></div>
  <div id="pawrap" style="position:absolute;left:220px;top:470px;width:640px;height:1120px;transform-origin:50% 62%">{pa}</div>
  <div class="chip" id="chipA" style="left:560px;top:1265px">{ic(I["warn"],30,"#fff",2.6)}&nbsp;JANGAN BUKA</div></div>''')
FROM("#scA .kick span", "yPercent:110,duration:0.7," + EO, 0.15)
mask("#hA1 span", C["a1"]); mask("#hA2 span", C["a1"] + 0.15)
FROM("#pawrap", "y:300,opacity:0,duration:1.0," + EO, 0.2)
FROM("#pa-ty", "opacity:0,scale:0.6,duration:0.3", 0.9)
TO("#pa-ty", "opacity:0,height:0,padding:0,duration:0.2", 1.75)
FROM("#pa-msg", "opacity:0,y:30,duration:0.5," + EO, 1.8); sfx("pop", 1.8, 0.18)
FROM("#pa-file", "opacity:0,y:30,duration:0.5," + EO, C["a1"] + 2.9); sfx("pop", C["a1"] + 2.9, 0.18)
tA = C["a2"]
TO("#scA .wrap", "opacity:0,y:-30,duration:0.4,ease:'power2.in'", tA - 0.3)
TO("#pawrap", "scale:1.16,y:-170,duration:1.4,ease:'power3.inOut'", tA - 0.2)
TO("#pa-fred", "opacity:1,duration:0.3", tA + 0.9)
TO("#pa-fred", "opacity:0.35,duration:0.45,yoyo:true,repeat:3,ease:'sine.inOut'", tA + 1.2)
FROM("#chipA", "opacity:0,scale:0.8,duration:0.45,ease:'back.out(2)'", tA + 1.0); sfx("ding", tA + 1.0, 0.18)

# ---------- B: incident ----------
times = ["14:38", "14:39", "14:40", "14:40", "14:41", "14:42"]
notifs = "".join(f'''<div class="notif" id="nf{i}" style="top:{i * 132}px"><div class="nicon">{ic(I["chat"],36,"#fff",2.4)}</div>
  <div class="nt"><div class="nt1">Kawan <span>{tm}</span></div><div class="nt2">{ic(I["clip"],24,"#C7CDD6",2.2)}{FNAME}</div></div></div>''' for i, tm in enumerate(times))
scene("B", f'''<div class="out">{chapter("B", "01", "Apa yang berlaku")}
  <div class="wrap" style="top:440px"><div class="datebox"><div class="big-date mask"><span>27.11.2026</span></div><div class="big-time mask"><span>14:38</span></div></div>
    <div class="inc-h" id="incH">Akaun WhatsApp seorang rakan <b>diambil alih</b>.</div></div>
  <div class="wrap" style="top:760px;height:800px">{notifs}
    <div class="tline" style="top:810px"><div class="tl-bar"></div><div class="tl-fill" id="tlf"></div><div class="tl-lab" style="left:0">14:38</div><div class="tl-lab" style="right:0">14:42</div><div class="tl-mid">&asymp; 4 minit</div></div></div></div>''')
chap_anim("B")
mask("#scB .big-date span", C["b1"] + 0.2); mask("#scB .big-time span", C["b1"] + 3.9)
rise("#incH", C["b1"] + 6.3)
for i in range(6):
    t = C["b2"] + 0.4 + i * 0.75
    FROM(f"#nf{i}", f"y:-60,opacity:0,scale:0.96,duration:0.6,{EO}", t); sfx("click", t, 0.16)
tl.append(f'tl.fromTo("#tlf",{{scaleX:0}},{{scaleX:1,duration:{0.75 * 5 + 0.6:.2f},ease:"none",immediateRender:false}},{C["b2"] + 0.4:.3f});')
FROM("#scB .tline", "opacity:0,duration:0.4", C["b2"] + 0.3)

# ---------- C: evidence ----------
ev = [("z5", "14:38", "PENERIMA A"), ("z1", "14:40", "PENERIMA B"), ("z3", "14:40", "PENERIMA C"), ("z2", "14:42", "PENERIMA D"), ("z6", "14:42", "PENERIMA E")]
cards = "".join(f'<div class="evcard" id="ev{i}" style="top:{i * 196}px"><div class="evlab"><span>{lab}</span><b>{tm}</b></div><div class="evimg"><img src="assets/ev/{z}.png"/></div></div>' for i, (z, tm, lab) in enumerate(ev))
scene("C", f'''<div class="out">{chapter("C", "02", "Bukti sebenar")}
  <div class="wrap" style="top:420px;height:1000px">{cards}</div>
  <div class="wrap foot" id="evfoot" style="top:1420px">Tangkapan skrin penerima. Nama &amp; gambar disembunyikan.</div></div>''')
chap_anim("C")
for i in range(5):
    t = C["c1"] + 0.3 + i * 0.55
    FROM(f"#ev{i}", f"x:120,opacity:0,duration:0.7,{EO}", t); sfx("click", t, 0.14)
rise("#evfoot", C["c1"] + 3.5, 0.6, 20)

# ---------- D: red flags ----------
pd = phone("pd", autoreply=True)
flags = [("d1", "Arahan formal tentang &lsquo;Finance&rsquo;", "Bukan gaya penulisan kawan anda.", "msg"),
         ("d2", "Fail ZIP bernama pelik", f"<code>{FNAME}</code><br>Tiada sebarang penjelasan.", "file"),
         ("d3", "Dari nombor yang anda kenali", "Sebab itu ia mudah dipercayai.", "head"),
         ("d4", "Balasan automatik masih berfungsi", "Akaun sebenar telah dirampas &mdash; bukan nombor palsu.", "ar")]
scene("D", f'''<div class="out">{chapter("D", "03", "Tanda amaran")}
  <div id="pdwrap" style="position:absolute;left:220px;top:370px;width:640px;height:1120px;transform:scale(0.68);transform-origin:50% 0">{pd}</div></div>''')
chap_anim("D")
FROM("#pdwrap", "y:120,opacity:0,duration:0.9," + EO, C["D"] + 0.3)
tl.append(f'tl.set("#pd-ar",{{display:"none"}},0);')
tl.append(f'tl.set("#pd-ar",{{display:"block"}},{C["d4"] + 1.2:.3f});')
FROM("#pd-ar", "opacity:0,y:30,duration:0.5," + EO, C["d4"] + 1.2)
for i, (k, h3, p, tgt) in enumerate(flags):
    s = C[k]; e = C[flags[i + 1][0]] if i + 1 < 4 else s_end("D")
    parts.append(clip(f"flag{i}", s, e - s, f'<div class="flag"><div class="n">TANDA {i + 1} / 4</div><h3>{h3}</h3><p>{p}</p></div>'))
    FROM(f"#flag{i} .flag", f"y:50,opacity:0,duration:0.6,{EO}", s)
    if e < s_end("D") - 0.1: TO(f"#flag{i} .flag", "opacity:0,y:-20,duration:0.25", e - 0.27)
    ring = f"#pd-{tgt} > .ring:not(.red)" if tgt != "head" else "#pd-head .ring"
    t_on = s + (1.3 if tgt == "ar" else 0.3)
    TO(ring, "opacity:1,duration:0.35", t_on)
    TO(ring, "opacity:0,duration:0.3", e - 0.3)
    sfx("click", s, 0.16)

# ---------- E: why dangerous ----------
rows = [("e2", I["bug"], "Peranti dijangkiti", "Perisian hasad dipasang"), ("e3", I["user"], "Akaun dirampas", "Penggodam guna akaun anda"),
        ("e4", I["users"], "Disebar kepada kenalan", "Kitaran yang sama berulang")]
srows = "".join(f'<div class="srow" id="sr{i}"><div class="sico">{ic(icn,54,"#F4F5F7",2)}</div><div class="stx">{t}<small>{sub}</small></div></div>' for i, (k, icn, t, sub) in enumerate(rows))
scene("E", f'''<div class="out">{chapter("E", "04", "Kenapa berbahaya")}
  <div class="disg" id="disg"><div class="doc"></div><div><div class="dn">Penyata_Akaun.pdf<span class="ext" id="ext">.exe</span></div><div class="dsub" id="dsub">Contoh: sambungan sebenar disembunyikan</div></div></div>
  <div class="steps"><div class="vline0"></div><div class="vline" id="vl"></div>{srows}</div></div>''')
chap_anim("E")
rise("#disg", C["e1"])
FROM("#ext", "opacity:0,x:-20,duration:0.5," + EO, C["e1"] + 1.4); sfx("ding", C["e1"] + 1.4, 0.15)
FROM("#dsub", "opacity:0,duration:0.4", C["e1"] + 1.7)
FROM("#scE .vline0", "opacity:0,duration:0.4", C["e2"])
tl.append(f'tl.fromTo("#vl",{{scaleY:0}},{{scaleY:1,duration:{C["e4"] - C["e2"]:.2f},ease:"none",immediateRender:false}},{C["e2"]:.3f});')
for i, (k, *_r) in enumerate(rows):
    FROM(f"#sr{i}", f"x:-60,opacity:0,duration:0.6,{EO}", C[k])
    tl.append(f'tl.set("#sr{i} .sico",{{borderColor:"#E5484D",backgroundColor:"#2A1416"}},{C[k] + 0.2:.3f});')
    sfx("click", C[k], 0.16)

# ---------- F: protect ----------
prot = [("f1", I["x"], "Jangan buka fail ZIP / APK yang tidak dijangka", "Walaupun daripada kawan"),
        ("f2", I["phone"], "Hubungi pengirim untuk sahkan", "Melalui panggilan, bukan mesej"),
        ("f3", I["lock"], "Aktifkan pengesahan dua langkah", "Tetapan &rsaquo; Akaun &rsaquo; Pengesahan dua langkah"),
        ("f4", I["laptop"], "Semak peranti dipautkan", "Tetapan &rsaquo; Peranti dipautkan &rsaquo; Log keluar"),
        ("f5", I["key"], "Jangan kongsi kod 6 digit", "Kod pengesahan WhatsApp anda")]
prows = "".join(f'<div class="prow" id="pr{i}" style="top:{420 + i * 214}px"><div class="pi">{ic(icn,46,"#30A46C",2.2)}</div><div><h4>{t}</h4><p>{sub}</p></div></div>' for i, (k, icn, t, sub) in enumerate(prot))
scene("F", f'<div class="out">{chapter("F", "05", "Lindungi diri anda")}{prows}</div>')
chap_anim("F")
for i, (k, *_r) in enumerate(prot):
    FROM(f"#pr{i}", f"y:40,opacity:0,duration:0.6,{EO}", C[k]); sfx("click", C[k], 0.16)
    if i > 0: TO(f"#pr{i - 1}", "opacity:0.45,duration:0.4", C[k])
TO(f"#pr4", "opacity:1,duration:0.1", C["f5"] + 1)
tl.append(f'tl.to("#scF .prow",{{opacity:1,duration:0.5}},{s_end("F") - 1.6:.3f});')

# ---------- G: opened ----------
ops = [("g1", "Putuskan sambungan internet"), ("g2", "Imbas peranti dengan antivirus"), ("g3", "Tukar kata laluan dari peranti lain"), ("g4", "Maklumkan kepada kenalan anda")]
orows = "".join(f'<div class="orow" id="or{i}" style="top:{420 + i * 112}px"><span class="on">{i + 1:02d}</span><div>{t}</div></div>' for i, (k, t) in enumerate(ops))
scene("G", f'''<div class="out">{chapter("G", "06", "Jika sudah terbuka")}{orows}
  <div class="rhead" id="rhead">LAPORKAN INSIDEN</div>
  <div class="report" id="rep"><div class="rcard"><div class="rk">INSIDEN SIBER</div><div class="rn">Cyber999</div><div class="rp">1-300-88-2999</div><div class="rd">CyberSecurity Malaysia</div></div>
    <div class="rcard"><div class="rk">KERUGIAN WANG</div><div class="rn">NSRC</div><div class="rp">997</div><div class="rd">Pusat Respons Scam Kebangsaan</div></div></div></div>''')
chap_anim("G")
for i, (k, _t) in enumerate(ops):
    FROM(f"#or{i}", f"x:-40,opacity:0,duration:0.6,{EO}", C[k]); sfx("click", C[k], 0.16)
FROM("#rhead", "opacity:0,duration:0.4", C["g5"])
FROM("#rep .rcard:nth-child(1)", f"y:60,opacity:0,duration:0.7,{EO}", C["g5"] + 0.6)
FROM("#rep .rcard:nth-child(2)", f"y:60,opacity:0,duration:0.7,{EO}", C["g5"] + 4.2)

# ---------- H: close ----------
parts.append(clip("scH", C["H"], TOTAL - C["H"], f'''<div class="close"><div id="shd">{ic(I["shield"],150,"#30A46C",1.6)}</div>
  <h1 class="mask"><span>Kongsikan</span></h1><h1 class="mask" style="margin-top:0"><span>video ini.</span></h1>
  <p id="hp">Satu perkongsian boleh menyelamatkan<br>kawan dan keluarga anda.</p><div class="tagx" id="htag">#JanganBukaZIP</div></div>
  <div class="disc" id="disc">Maklumat am keselamatan siber. Sahkan nombor talian melalui laman rasmi agensi berkaitan.</div>''', "scene"))
FROM("#shd", "scale:0.6,opacity:0,duration:0.9,ease:'back.out(1.7)'", C["H"] + 0.1)
mask("#scH h1:nth-of-type(1) span", C["h1"]); mask("#scH h1:nth-of-type(2) span", C["h1"] + 0.15)
rise("#hp", C["h1"] + 2.4, 0.7, 20); FROM("#htag", "opacity:0,scale:0.9,duration:0.5," + EO, C["h1"] + 3.4)
FROM("#disc", "opacity:0,duration:0.6", C["h1"] + 4.0)
sfx("whoosh", C["H"] - 0.15, 0.16); sfx("ding", C["h1"] + 3.4, 0.15)

# ---------- captions (chunked, word highlight) ----------
parts.append(f'<div id="capbg" class="clip" data-start="0" data-duration="{C["H"]:.3f}"></div>')
ci = 0
for l in LINES:
    if l["cue"] == "h1": continue
    ws = l["words"]; chunks = []; cur = []
    for w in ws:
        if cur and (len(cur) >= 6 or w["s"] - cur[-1]["e"] > 0.35): chunks.append(cur); cur = []
        cur.append(w)
    if cur: chunks.append(cur)
    for j, ch in enumerate(chunks):
        st = ch[0]["s"] - 0.05
        en = chunks[j + 1][0]["s"] - 0.05 if j + 1 < len(chunks) else ch[-1]["e"] + 0.35
        spans = " ".join(f'<span id="w{ci}_{k}">{H.escape(w["w"])}</span>' for k, w in enumerate(ch))
        parts.append(clip(f"cap{ci}", st, en - st, f'<div class="cap">{spans}</div>', "capw"))
        FROM(f"#cap{ci} .cap", "opacity:0,y:12,duration:0.25,ease:'power2.out'", st)
        for k, w in enumerate(ch): tl.append(f'tl.set("#w{ci}_{k}",{{color:"#F4F5F7"}},{w["s"]:.3f});')
        ci += 1

audio = "\n".join(f'<audio id="sfx{i}" class="clip" data-start="{t:.3f}" data-duration="{d}" data-volume="{v}" src="assets/sfx/{n}.wav"></audio>' for i, (n, t, v, d) in enumerate(SFX))
CSS = open(f"{S}/tools/style_pro.css").read()
doc = f'''<!doctype html>
<html lang="ms" data-resolution="portrait">
<head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script><style>{CSS}</style></head>
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
</body></html>'''
open(f"{P}/index.html", "w").write(doc)
print("ok", ci, "caption chunks", len(SFX), "sfx", TOTAL)
