import json, os, time
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
URL = "file:///" + os.path.join(BASE, "index.html").replace("\\", "/")
OUT = os.path.join(BASE, "_rd_probe")
os.makedirs(OUT, exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1900, "height": 1000}, device_scale_factor=2)
    pg.goto(URL)
    pg.wait_for_timeout(300)

    # sample the typed length over 1.6s to prove it animates
    lens = []
    for _ in range(9):
        lens.append(pg.eval_on_selector("#reportDateValue", "e => e.textContent.length"))
        pg.wait_for_timeout(200)
    print("typed length samples:", lens)

    info = pg.evaluate("""() => {
      const v = document.getElementById('reportDateValue');
      const chip = document.querySelector('.rd-chip');
      const wrap = v.parentNode;
      const ghost = document.querySelector('.rd-ghost');
      const caret = document.querySelector('.rd-caret');
      const cs = getComputedStyle(v);
      return {
        text: v.textContent,
        full: ghost.textContent,
        wrapW: wrap.getBoundingClientRect().width,
        ghostW: ghost.getBoundingClientRect().width,
        chipW: chip.getBoundingClientRect().width,
        chipH: chip.getBoundingClientRect().height,
        fontSize: cs.fontSize, color: cs.color, weight: cs.fontWeight,
        caretBg: getComputedStyle(caret).backgroundColor,
        overflowX: document.documentElement.scrollWidth - window.innerWidth,
        label: document.getElementById('reportDateLabel').textContent.trim(),
      };
    }""")
    print(json.dumps(info, indent=1))

    # wait for one full cycle to finish, then shoot the header
    pg.wait_for_timeout(2200)
    rect = pg.evaluate("""() => { const r = document.querySelector('.report-date').getBoundingClientRect();
        return {x: r.x, y: r.y, w: r.width, h: r.height}; }""")
    clip = {"x": max(0, rect["x"] - 24), "y": max(0, rect["y"] - 26),
            "width": min(760, rect["w"] + 60), "height": rect["h"] + 46}
    pg.screenshot(path=os.path.join(OUT, "rd_light.png"), clip=clip)

    # night mode
    pg.click("#nightModeButton")
    pg.wait_for_timeout(2600)
    pg.screenshot(path=os.path.join(OUT, "rd_night.png"), clip=clip)
    night = pg.evaluate("""() => { const v = document.getElementById('reportDateValue');
        return {cls: document.documentElement.className, color: getComputedStyle(v).color,
                chipBg: getComputedStyle(document.querySelector('.rd-chip')).backgroundColor}; }""")
    print("night:", json.dumps(night))

    # CN label + chinese date
    pg.click("button[data-lang='cn']")
    pg.wait_for_timeout(2600)
    cn = pg.evaluate("""() => {
      const v = document.getElementById('reportDateValue');
      return {lang: document.documentElement.lang, label: document.getElementById('reportDateLabel').textContent.trim(),
              text: v.textContent, wrapW: v.parentNode.getBoundingClientRect().width,
              ghostW: document.querySelector('.rd-ghost').getBoundingClientRect().width,
              overflowX: document.documentElement.scrollWidth - window.innerWidth};
    }""")
    print("cn:", json.dumps(cn, ensure_ascii=False))
    rect2 = pg.evaluate("""() => { const r = document.querySelector('.report-date').getBoundingClientRect();
        return {x: r.x, y: r.y, w: r.width, h: r.height}; }""")
    pg.screenshot(path=os.path.join(OUT, "rd_cn_night.png"),
                  clip={"x": max(0, rect2["x"] - 24), "y": max(0, rect2["y"] - 26),
                        "width": min(760, rect2["w"] + 60), "height": rect2["h"] + 46})

    # 1366 check for clipping
    pg2 = b.new_page(viewport={"width": 1366, "height": 800})
    pg2.goto(URL)
    pg2.wait_for_timeout(1200)
    print("1366:", pg2.evaluate("""() => ({overflowX: document.documentElement.scrollWidth - window.innerWidth,
        chipW: document.querySelector('.rd-chip').getBoundingClientRect().width})"""))
    b.close()
print("shots in", OUT)
