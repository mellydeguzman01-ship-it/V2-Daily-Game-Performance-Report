"""Brand logos -> transparent PNGs sized for the .plat-logo slot.

The three source files already carry a real alpha channel (their background is
transparent, not white), so the alpha is kept as-is. The only recolour needed is
ArenaPlus: its "PLUS" word is near-black and vanishes on the navy card.
"""
import json, base64, pathlib
from PIL import Image

SRC = pathlib.Path(r"C:\Users\L-User\AppData\Local\hermes\image_cache")
OUT = pathlib.Path(r"C:\Users\L-User\Documents\ChatGPT\Daily Report\V2-Daily-Game-Performance-Report\_logos")
OUT.mkdir(exist_ok=True)

jobs = [
    ("bp", "img_e0455b1a7537.jpg", 34, False),  # BingoPlus
    ("gp", "img_155d03cb2d3b.jpg", 34, False),  # GameZone
    ("ap", "img_99fa121951e8.jpg", 34, True),   # ArenaPlus
]

report, payloads = {}, {}

for key, fn, h, dark_to_light in jobs:
    im = Image.open(SRC / fn).convert("RGBA")
    w, hh = im.size
    pix = im.load()

    if dark_to_light:
        for y in range(hh):
            for x in range(w):
                r, g, b, a = pix[x, y]
                if a > 40 and max(r, g, b) < 90:          # the black "PLUS"
                    lum = (0.2126 * r + 0.7152 * g + 0.0722 * b)
                    f = min(1.0, (90 - max(r, g, b)) / 60)  # keep edge antialiasing soft
                    pix[x, y] = (int(r + (236 - r) * f), int(g + (243 - g) * f),
                                 int(b + (252 - b) * f), a)

    bbox = im.getbbox()
    im = im.crop(bbox)
    cw, ch = im.size
    nw = max(1, round(cw * h / ch))
    im = im.resize((nw, h), Image.LANCZOS)

    p = OUT / f"{key}.png"
    im.save(p, optimize=True)
    payloads[key] = "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()

    data = list(im.getdata())
    op = [(r, g, b) for r, g, b, a in data if a > 40]
    lum = sorted(0.2126 * r + 0.7152 * g + 0.0722 * b for r, g, b in op)
    report[key] = dict(size=im.size, png_kb=round(p.stat().st_size / 1024, 1),
                       transparent_pct=round(100 * (1 - len(op) / len(data)), 1),
                       mean_lum=round(sum(lum) / len(lum)),
                       p10_lum=round(lum[len(lum) // 10]),
                       b64_kb=round(len(payloads[key]) / 1024, 1))

(OUT / "payloads.json").write_text(json.dumps(payloads), encoding="utf-8")
print(json.dumps(report, indent=1))
