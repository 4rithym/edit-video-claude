"""Generate Malay voice-over lines (facebook/mms-tts-zlm) and a cue sheet."""
import sys, json, subprocess, torch, numpy as np, scipy.io.wavfile as wf
from transformers import VitsModel, AutoTokenizer
OUT = sys.argv[1]
SCRIPT = [  # (scene, cue, text)
 ("s1","s1a","Amaran! Jangan buka fail ini."),
 ("s1","s1b","Trojan wassap sedang tersebar."),
 ("s2","s2a","Pada dua puluh tujuh nofember, jam dua tiga puluh lapan petang,"),
 ("s2","s2b","wassap Harith telah digodam."),
 ("s2","s2c","Dalam masa kira-kira empat minit, mesej dan fail yang sama, dihantar kepada ramai kenalannya."),
 ("s3","s3a","Kenal pasti tanda-tandanya."),
 ("s3","sg0","Satu. Arahan formal tentang bahagian kewangan. Ini bukan gaya kawan anda."),
 ("s3","sg1","Dua. Fail zip bernama pelik, tanpa sebarang penjelasan."),
 ("s3","sg2","Tiga. Ia datang dari nombor kawan sendiri, jadi mudah dipercayai."),
 ("s3","sg3","Empat. Balasan automatik masih berjalan. Ini akaun sebenar yang dirampas, bukan nombor palsu."),
 ("s4","s4a","Kenapa ia bahaya?"),
 ("s4","s4b","Fail berbahaya boleh menyamar sebagai dokumen biasa."),
 ("s4","n0","Sekali dibuka,"),
 ("s4","n1","peranti boleh dijangkiti,"),
 ("s4","n2","akaun dirampas,"),
 ("s4","n3","dan mesej ini disebarkan pula kepada kenalan anda."),
 ("s5","s5a","Lindungi diri anda."),
 ("s5","tp0","Jangan buka fail zip atau aplikasi yang tidak dijangka, walaupun dari kawan."),
 ("s5","tp1","Telefon kawan itu dahulu untuk sahkan."),
 ("s5","tp2","Aktifkan pengesahan dua langkah dalam tetapan akaun."),
 ("s5","tp3","Semak peranti dipautkan, dan log keluar peranti yang tidak dikenali."),
 ("s5","tp4","Jangan sekali-kali kongsi kod enam digit wassap anda."),
 ("s6","s6a","Kalau fail itu sudah terbuka,"),
 ("s6","st0","putuskan sambungan internet."),
 ("s6","st1","Imbas peranti dengan antivirus."),
 ("s6","st2","Tukar kata laluan penting, menggunakan peranti lain."),
 ("s6","st3","Dan maklumkan kepada semua kenalan anda."),
 ("s6","rep","Laporkan kepada saiber sembilan sembilan sembilan. Jika kehilangan wang, hubungi Pusat Respons Skem Kebangsaan, di talian sembilan sembilan tujuh."),
 ("s7","s7a","Kongsi video ini, dan selamatkan kawan serta keluarga anda."),
]
m = VitsModel.from_pretrained("facebook/mms-tts-zlm"); tok = AutoTokenizer.from_pretrained("facebook/mms-tts-zlm")
m.config.speaking_rate = 1.08; m.config.noise_scale = 0.6
SR = m.config.sampling_rate
LEAD, GAP, SCENE_GAP, TAIL = 0.35, 0.22, 0.55, 2.6
cues, t, prev_scene, lines = {}, 0.15, None, []
for scene, cue, text in SCRIPT:
    if prev_scene and scene != prev_scene: t += SCENE_GAP
    if scene != prev_scene: cues[scene] = round(max(0, t - LEAD), 3); t = max(t, cues[scene] + LEAD)
    torch.manual_seed(7)
    with torch.no_grad(): w = m(**tok(text, return_tensors="pt")).waveform[0].numpy()
    # trim leading/trailing silence
    a = np.abs(w); thr = 0.02 * a.max(); idx = np.where(a > thr)[0]
    w = w[max(0, idx[0] - 400): idx[-1] + 1600]
    p = f"{OUT}/{cue}.wav"; wf.write(p, SR, (w / np.abs(w).max() * 0.9 * 32767).astype(np.int16))
    d = len(w) / SR
    cues[cue] = round(t, 3); lines.append({"cue": cue, "t": round(t, 3), "d": round(d, 3), "text": text})
    t += d + GAP; prev_scene = scene
cues["end"] = round(t + TAIL, 3)
json.dump({"cues": cues, "lines": lines}, open(f"{OUT}/cues.json", "w"), indent=1)
# mix into one VO track (44.1k stereo) with light EQ/compression
N = int(cues["end"] * SR); mix = np.zeros(N, np.float32)
for l in lines:
    sr, x = wf.read(f"{OUT}/{l['cue']}.wav"); x = x.astype(np.float32) / 32768
    i = int(l["t"] * SR); mix[i:i + len(x)] += x[: N - i]
wf.write(f"{OUT}/vo_raw.wav", SR, (mix * 32767).astype(np.int16))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/vo_raw.wav", "-af",
    "highpass=f=80,equalizer=f=3000:t=q:w=1:g=3,acompressor=threshold=-18dB:ratio=3:attack=5:release=80,aresample=44100,loudnorm=I=-16:TP=-1.5",
    "-ac", "2", "-ar", "44100", f"{OUT}/vo.wav"], check=True)
print(json.dumps(cues))
