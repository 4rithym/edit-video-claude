# edit-video-claude — Zakat UniKL

**Video siap:** [`output/zakat_unikl_edit.mp4`](output/zakat_unikl_edit.mp4) (1080×1920, 79 s, -14 LUFS)
Kapsyen berasingan: [`output/kapsyen.srt`](output/kapsyen.srt)

Video asal: Release `raw-video` (87 s).

## Apa yang dibuat
- **Transkrip** dengan Whisper large-v3-turbo (Bahasa Melayu), lihat `transcript/`
- **Potong** bahagian senyap / jeda (87 s → 77 s)
- **Hook** pada 0–2.6 s: klip "macam mana hanya tinggal bulu tu?" + tajuk "DUIT TINGGAL 'BULU'?!", lalu "SEBELUM TU…"
- **Motion graphics** (Hyperframes + GSAP): kapsyen karaoke, sticker, kad jenama, senarai ciri, kad website, kalendar "DISEMBER 12", CTA dan end card
- **Sound effects** (dijana sendiri): whoosh, pop, ding, impact, riser, coin, rewind, click

## Render semula
`project/assets/cut.mp4` tidak disimpan (96 MB). Jana semula dari video asal:
```
python3 tools/cut.py <workdir>      # perlukan <workdir>/src/raw.mp4 + audio.wav
cd project && npx hyperframes render -q delivery
```
