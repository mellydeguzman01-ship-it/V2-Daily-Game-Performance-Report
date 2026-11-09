import os
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
URL = "file:///" + os.path.join(BASE, "index.html").replace("\\", "/")
OUT = os.path.join(BASE, "..", "localz")
os.makedirs(OUT, exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (1920, 1440):
        pg = b.new_page(viewport={"width": w, "height": 1080}, device_scale_factor=1.5)
        pg.goto(URL)
        pg.wait_for_timeout(1200)
        el = pg.query_selector(".gp-modes")
        el.screenshot(path=os.path.join(OUT, f"_modes_{w}.png"))
        box = el.bounding_box()
        print(w, "panel box", {k: round(v) for k, v in box.items()})
        print(w, "mode-game count", pg.eval_on_selector_all(".gp-modes .mode-game", "e=>e.length"))
        print(w, "tracks", pg.eval_on_selector_all(".gp-modes .mode-track", "e=>e.length"))
        # overflow check: scrollHeight vs clientHeight of the panel
        print(w, "scrollH/clientH", pg.eval_on_selector(".gp-modes", "e=>[e.scrollHeight,e.clientHeight]"))
        b.close() if False else None
        pg.close()
    b.close()
