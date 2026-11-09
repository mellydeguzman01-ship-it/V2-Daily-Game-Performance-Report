import os
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
URL = "file:///" + os.path.join(BASE, "index.html").replace("\\", "/")
OUT = os.path.join(BASE, "..", "localz")
os.makedirs(OUT, exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch()
    for night in (False, True):
        page = b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=2)
        page.goto(URL)
        page.wait_for_timeout(900)
        if night:
            page.evaluate("document.documentElement.classList.add('night')")
            page.wait_for_timeout(400)
        el = page.query_selector(".gp-modes")
        tag = "night" if night else "light"
        el.screenshot(path=os.path.join(OUT, f"_modesnames_{tag}_1920.png"))
        # report computed colours of the four game names
        rows = page.eval_on_selector_all(
            ".gp-modes .mode-game",
            """els => els.map(e => {
                 const n = e.querySelector('.mode-game-name');
                 return [e.className, n.textContent.trim(),
                         getComputedStyle(n).color,
                         getComputedStyle(n).fontWeight];
               })""")
        for r in rows:
            print(tag, r)
        # clipping check inside the panel
        print(tag, "panel scroll/client",
              page.eval_on_selector(".gp-modes", "e=>[e.scrollHeight,e.clientHeight,e.scrollWidth,e.clientWidth]"))
        page.close()
    b.close()
print("done")
