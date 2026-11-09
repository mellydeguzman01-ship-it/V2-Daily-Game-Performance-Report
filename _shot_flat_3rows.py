import os
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
URL = "file:///" + os.path.join(BASE, "index.html").replace("\\", "/")
OUT = os.path.join(BASE, "..", "localz")

with sync_playwright() as p:
    b = p.chromium.launch()
    for night in (False, True):
        page = b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=2)
        page.goto(URL)
        page.wait_for_timeout(900)
        if night:
            page.evaluate("document.documentElement.classList.add('night')")
            page.wait_for_timeout(400)
        tag = "night" if night else "light"
        page.query_selector(".gp-modes").screenshot(path=os.path.join(OUT, f"_modes_flat_{tag}.png"))
        page.query_selector(".gp-feature").screenshot(path=os.path.join(OUT, f"_feature3_{tag}.png"))
        segs = page.eval_on_selector_all(
            ".gp-modes .mode-track .seg",
            "els => els.map(e => [e.className, getComputedStyle(e).backgroundImage, getComputedStyle(e).backgroundColor])")
        print(tag, "segments:", len(segs))
        for s in segs[:2]:
            print("   ", s)
        rows = page.eval_on_selector_all(
            ".gp-feature .dynamic-item",
            """els => els.map(e => [e.querySelector('.dynamic-head b').textContent,
                                   e.querySelector('.dynamic-head span').textContent,
                                   e.querySelector('.dynamic-foot b').textContent])""")
        for r in rows:
            print("   feature:", r)
        print(tag, "feature panel box", page.eval_on_selector(
            ".gp-feature", "e=>{const r=e.getBoundingClientRect();return [Math.round(r.width),Math.round(r.height),e.scrollHeight,e.clientHeight]}"))
        print(tag, "modes panel box", page.eval_on_selector(
            ".gp-modes", "e=>{const r=e.getBoundingClientRect();return [Math.round(r.width),Math.round(r.height),e.scrollHeight,e.clientHeight]}"))
        page.close()
    b.close()
print("done")
