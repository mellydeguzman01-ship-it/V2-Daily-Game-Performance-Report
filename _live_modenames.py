import os, sys, time
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "..", "localz")
URL = "https://mellydeguzman01-ship-it.github.io/V2-Daily-Game-Performance-Report/?v=modenamecolors"
TAG = sys.argv[1] if len(sys.argv) > 1 else "1"

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=2)
    page.goto(URL, wait_until="networkidle", timeout=90000)
    page.wait_for_timeout(1500)
    rows = page.eval_on_selector_all(
        ".gp-modes .mode-game",
        """els => els.map(e => { const n = e.querySelector('.mode-game-name');
             return [e.className, n.textContent.trim(), getComputedStyle(n).color]; })""")
    for r in rows:
        print("LIVE", r)
    page.eval_on_selector(".gp-modes", "e=>e.scrollIntoView({block:'center'})")
    page.wait_for_timeout(600)
    page.query_selector(".gp-modes").screenshot(path=os.path.join(OUT, f"_live_modenames_{TAG}.png"))
    page.evaluate("document.documentElement.classList.add('night')")
    page.wait_for_timeout(500)
    page.query_selector(".gp-modes").screenshot(path=os.path.join(OUT, f"_live_modenames_{TAG}_night.png"))
    b.close()
print("shot ok")
