import io, os, time
from PIL import Image
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
URL = "file:///" + os.path.abspath("index.html").replace("\\", "/")
OUT = os.path.join(BASE, "_rd_probe")
os.makedirs(OUT, exist_ok=True)

shot_frames = []


def grab(pg, clip, theme, frames, step, n):
    for i in range(n):
        buf = pg.screenshot(clip=clip)
        im = Image.open(io.BytesIO(buf)).convert("RGB")
        # label the theme on the frame
        frames.append(im)
        pg.wait_for_timeout(step)


with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1900, "height": 900}, device_scale_factor=2)
    pg.goto(URL)
    pg.wait_for_timeout(300)
    rect = pg.evaluate("""() => { const r = document.querySelector('.rd-chip').getBoundingClientRect();
        return {x: r.x, y: r.y, w: r.width, h: r.height}; }""")
    clip = {"x": rect["x"] - 10, "y": rect["y"] - 10, "width": rect["w"] + 20, "height": rect["h"] + 20}

    frames = []
    grab(pg, clip, "light", frames, 70, 46)          # ~3.2s, one full cycle
    pg.click("#nightModeButton"); pg.wait_for_timeout(300)
    grab(pg, clip, "night", frames, 70, 46)
    b.close()

# 2x downscale so the GIF stays small
w, h = frames[0].size
frames = [f.resize((w // 2, h // 2), Image.LANCZOS).convert("P", palette=Image.ADAPTIVE, colors=128) for f in frames]
gif = os.path.join(OUT, "report_date_style04_live.gif")
frames[0].save(gif, save_all=True, append_images=frames[1:], duration=70, loop=0, optimize=True, disposal=2)
print(gif, frames[0].size, os.path.getsize(gif))
