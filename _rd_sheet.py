import os
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
URL = "file:///" + os.path.join(BASE, "index.html").replace("\\", "/")
OUT = os.path.join(BASE, "_rd_probe")
os.makedirs(OUT, exist_ok=True)


def wait_full(pg, timeout=6000):
    """Wait until the typewriter is showing the whole date (and holding)."""
    import time
    t0 = time.time()
    while time.time() - t0 < timeout:
        done = pg.evaluate("""() => { const v = document.getElementById('reportDateValue');
            const g = document.querySelector('.rd-ghost');
            return v.textContent === g.textContent; }""")
        if done:
            pg.wait_for_timeout(120)
            return True
        pg.wait_for_timeout(80)
    return False


with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1900, "height": 900}, device_scale_factor=2)
    pg.goto(URL)
    pg.wait_for_timeout(400)

    rect = pg.evaluate("""() => { const r = document.querySelector('.report-date').getBoundingClientRect();
        return {x: r.x, y: r.y, w: r.width, h: r.height}; }""")
    clip = {"x": max(0, rect["x"] - 18), "y": max(0, rect["y"] - 18),
            "width": min(780, rect["w"] + 40), "height": rect["h"] + 36}

    wait_full(pg)
    pg.screenshot(path=os.path.join(OUT, "s_light.png"), clip=clip)
    pg.click("#nightModeButton")
    pg.wait_for_timeout(700)
    wait_full(pg)
    pg.screenshot(path=os.path.join(OUT, "s_night.png"), clip=clip)
    pg.click("button[data-lang='cn']")
    pg.wait_for_timeout(700)
    wait_full(pg)
    pg.screenshot(path=os.path.join(OUT, "s_cn.png"), clip=clip)
    b.close()

shots = [("LIGHT MODE (default)  ·  EN", "s_light.png", (239, 242, 246)),
         ("NIGHT MODE  ·  EN", "s_night.png", (9, 19, 33)),
         ("NIGHT MODE  ·  CN (报告日期)", "s_cn.png", (9, 19, 33))]

imgs = [Image.open(os.path.join(OUT, f)).convert("RGB") for _, f, _ in shots]
pad, labelh, gap = 18, 30, 12
W = max(i.width for i in imgs) + pad * 2
H = sum(i.height + labelh for i in imgs) + gap * (len(imgs) - 1) + pad * 2
sheet = Image.new("RGB", (W, H), (7, 15, 26))
d = ImageDraw.Draw(sheet)
try:
    f = ImageFont.truetype("C:/Windows/Fonts/seguisb.ttf", 19)
except Exception:
    f = ImageFont.load_default()

y = pad
for (label, _, _), im in zip(shots, imgs):
    d.text((pad, y), label, font=f, fill=(122, 176, 235))
    y += labelh
    sheet.paste(im, (pad, y))
    y += im.height + gap

out = os.path.join(OUT, "report_date_style04_preview.png")
sheet.save(out, quality=95)
print(out, sheet.size, os.path.getsize(out))
