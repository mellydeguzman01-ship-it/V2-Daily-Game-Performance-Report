import os
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "..", "localz")
URL = "https://mellydeguzman01-ship-it.github.io/V2-Daily-Game-Performance-Report/?v=flat3rows2"

with sync_playwright() as p:
    b = p.chromium.launch()
    for night in (False, True):
        page = b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=2)
        page.goto(URL, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_selector(".gp-modes .seg-blue", timeout=60000)
        page.wait_for_timeout(2500)
        if night:
            page.evaluate("document.documentElement.classList.add('night')")
            page.wait_for_timeout(500)
        tag = "night" if night else "light"
        bg = page.eval_on_selector(".gp-modes .seg-blue", "e=>getComputedStyle(e).backgroundImage")
        print(tag, "seg backgroundImage:", bg)
        rows = page.eval_on_selector_all(
            ".gp-feature .dynamic-item",
            "els => els.map(e => e.querySelector('.dynamic-head').textContent)")
        for r in rows:
            print("   LIVE feature:", r)
        page.eval_on_selector(".gp-modes", "e=>e.scrollIntoView({block:'center'})")
        page.wait_for_timeout(800)
        page.query_selector(".gp-modes").screenshot(path=os.path.join(OUT, f"_live_flat_{tag}.png"))
        page.query_selector(".gp-feature").screenshot(path=os.path.join(OUT, f"_live_feature3_{tag}.png"))
        page.close()
    b.close()
print("ok")
