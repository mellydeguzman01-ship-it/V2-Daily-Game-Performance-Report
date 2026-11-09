import os
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
URL = "file:///" + os.path.join(BASE, "index.html").replace("\\", "/")
JS = """()=>{
  const row=document.querySelector('.gp-row-2');
  const kids=[...row.children];
  return {row:Math.round(row.getBoundingClientRect().height),
    kids:kids.map(k=>{const r=k.getBoundingClientRect();
      return {cls:k.className.split(' ').slice(0,3).join(' '),h:Math.round(r.height),bot:Math.round(r.bottom)};})};
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (1440, 1920, 2560):
        pg = b.new_page(viewport={"width": w, "height": 1200}, device_scale_factor=1)
        pg.goto(URL)
        pg.wait_for_timeout(1500)
        info = pg.evaluate(JS)
        bots = [k["bot"] for k in info["kids"]]
        print(w, "row", info["row"], "bottoms", bots, "LEVEL" if len(set(bots)) == 1 else "MISMATCH")
        for k in info["kids"]:
            print("    ", k)
        if w == 1920:
            pg.query_selector(".gp-row-2").screenshot(path=os.path.join(BASE, "..", "localz", "_row2_aligned_1920.png"))
        pg.close()
    b.close()
