"""Neural Malay voice-over (Microsoft ms-MY) with word timings -> cues.json + vo.wav."""
import asyncio, os, sys, json, subprocess
import edge_tts
OUT = sys.argv[1]; VOICE = sys.argv[2] if len(sys.argv) > 2 else "ms-MY-OsmanNeural"
SCRIPT = [
 ("A","a1","Mesej ini kelihatan biasa. Ia datang daripada nombor kawan anda sendiri."),
 ("A","a2","Tetapi, jangan sesekali buka fail ini."),
 ("B","b1","Pada 27 November 2026, sekitar jam 2:38 petang, akaun WhatsApp milik Harith telah diambil alih."),
 ("B","b2","Dalam masa kira-kira empat minit, mesej yang sama, bersama sebuah fail ZIP, dihantar kepada ramai kenalannya."),
 ("C","c1","Ini bukti sebenar daripada penerima. Nama fail, saiz, dan masanya hampir serentak."),
 ("D","d0","Kenal pasti tanda-tandanya."),
 ("D","d1","Pertama, arahan formal tentang bahagian Finance, yang bukan gaya penulisan kawan anda."),
 ("D","d2","Kedua, fail ZIP bernama pelik, tanpa sebarang penjelasan."),
 ("D","d3","Ketiga, ia dihantar daripada nombor yang anda kenali, jadi mudah dipercayai."),
 ("D","d4","Keempat, balasan automatik masih berfungsi. Ini menunjukkan akaun sebenar telah dirampas, bukan nombor palsu."),
 ("E","e1","Fail berbahaya boleh disamarkan sebagai dokumen biasa."),
 ("E","e2","Sebaik sahaja dibuka, peranti boleh dijangkiti,"),
 ("E","e3","akaun boleh dirampas,"),
 ("E","e4","dan mesej yang sama akan disebarkan kepada kenalan anda pula."),
 ("F","f0","Lindungi diri anda."),
 ("F","f1","Jangan buka fail ZIP atau APK yang tidak dijangka, walaupun daripada kawan."),
 ("F","f2","Hubungi pengirim melalui panggilan untuk mengesahkannya."),
 ("F","f3","Aktifkan pengesahan dua langkah di WhatsApp."),
 ("F","f4","Semak peranti dipautkan, dan log keluar peranti yang tidak dikenali."),
 ("F","f5","Jangan sesekali kongsi kod enam digit WhatsApp anda."),
 ("G","g0","Jika fail itu telah dibuka,"),
 ("G","g1","putuskan sambungan internet,"),
 ("G","g2","imbas peranti dengan antivirus,"),
 ("G","g3","tukar kata laluan menggunakan peranti lain,"),
 ("G","g4","dan maklumkan kepada kenalan anda."),
 ("G","g5","Laporkan insiden kepada Cyber999. Jika melibatkan kerugian wang, hubungi NSRC di talian 997."),
 ("H","h1","Kongsikan video ini. Satu perkongsian boleh menyelamatkan kawan dan keluarga anda."),
]
async def synth(cue, text):
    c = edge_tts.Communicate(text, VOICE, rate="-4%", boundary="WordBoundary", proxy=os.environ.get("HTTPS_PROXY"))
    audio = bytearray(); words = []
    async for ch in c.stream():
        if ch["type"] == "audio": audio += ch["data"]
        elif ch["type"] == "WordBoundary":
            words.append({"w": ch["text"], "s": ch["offset"] / 1e7, "e": (ch["offset"] + ch["duration"]) / 1e7})
    open(f"{OUT}/{cue}.mp3", "wb").write(audio)
    return words
def dur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],capture_output=True,text=True).stdout)
async def main():
    LEAD, GAP, SCENE_GAP, TAIL = 0.5, 0.28, 0.7, 3.2
    cues, lines, t, prev = {}, [], 0.3, None
    for scene, cue, text in SCRIPT:
        if prev and scene != prev: t += SCENE_GAP
        if scene != prev: cues[scene] = round(max(0, t - LEAD), 3)
        words = await synth(cue, text)
        # trim leading silence using first word offset
        lead = words[0]["s"] if words else 0
        subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{max(0,lead-0.05):.3f}","-i",f"{OUT}/{cue}.mp3","-ar","44100","-ac","1",f"{OUT}/{cue}.wav"],check=True)
        d = words[-1]["e"] - lead + 0.15 if words else dur(f"{OUT}/{cue}.wav")
        off = t - max(0, lead - 0.05)
        cues[cue] = round(t, 3)
        lines.append({"cue": cue, "t": round(t, 3), "d": round(d, 3), "text": text,
                      "words": [{"w": w["w"], "s": round(w["s"] + off, 3), "e": round(w["e"] + off, 3)} for w in words]})
        t += d + GAP; prev = scene
    cues["end"] = round(t + TAIL, 3)
    json.dump({"cues": cues, "lines": lines}, open(f"{OUT}/cues.json", "w"), indent=1, ensure_ascii=False)
    # mix
    inputs, filt = [], []
    for i, l in enumerate(lines):
        inputs += ["-i", f"{OUT}/{l['cue']}.wav"]; filt.append(f"[{i}:a]adelay={int(l['t']*1000)}|{int(l['t']*1000)}[a{i}]")
    filt.append("".join(f"[a{i}]" for i in range(len(lines))) + f"amix=inputs={len(lines)}:normalize=0,apad=whole_dur={cues['end']},highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=100,loudnorm=I=-16:TP=-1.5[out]")
    subprocess.run(["ffmpeg","-v","error","-y",*inputs,"-filter_complex",";".join(filt),"-map","[out]","-ac","2","-ar","44100","-t",str(cues["end"]),f"{OUT}/vo.wav"],check=True)
    print(json.dumps(cues))
asyncio.run(main())
