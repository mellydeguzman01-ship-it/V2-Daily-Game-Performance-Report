import asyncio, sys
from playwright.async_api import async_playwright

URL = "file:///C:/Users/L-User/Documents/ChatGPT/Daily%20Report/V2-Daily-Game-Performance-Report/index.html"
OUT = r"C:/Users/L-User/AppData/Local/hermes/cache/screenshots/heat_legend_new.png"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w, name, out in ((1440, "desk", OUT), (390, "mobile", OUT.replace(".png", "_m.png"))):
            pg = await b.new_page(viewport={"width": w, "height": 1200}, device_scale_factor=2)
            await pg.goto(URL, wait_until="load")
            await pg.wait_for_timeout(1200)
            el = await pg.query_selector(".hourly-heat")
            await el.scroll_into_view_if_needed()
            await pg.wait_for_timeout(300)
            await el.screenshot(path=out)
            info = await pg.evaluate("""() => {
              const r = document.querySelector('.hourly-heat .heat-ramp');
              const lb = [...document.querySelectorAll('.hourly-heat .heat-scale-labels span')].map(s=>s.textContent);
              const cs = r ? getComputedStyle(r) : null;
              const box = r ? r.getBoundingClientRect() : null;
              const card = document.querySelector('.hourly-heat').getBoundingClientRect();
              return {labels: lb, w: box&&Math.round(box.width), h: box&&Math.round(box.height),
                      right: box&&Math.round(card.right - box.right), radius: cs&&cs.borderRadius,
                      radiusTop: cs&&cs.borderTopLeftRadius, bg: cs&&cs.backgroundImage.slice(0,120),
                      overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth};
            }""")
            print(name, info)
            await pg.close()
        await b.close()

asyncio.run(main())
