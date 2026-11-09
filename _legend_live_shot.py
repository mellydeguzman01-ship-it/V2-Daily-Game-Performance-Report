import asyncio
from playwright.async_api import async_playwright

URL = "https://mellydeguzman01-ship-it.github.io/V2-Daily-Game-Performance-Report/?cb=legend2"
OUT = r"C:/Users/L-User/AppData/Local/hermes/cache/screenshots/heat_legend_live.png"
OUTC = r"C:/Users/L-User/AppData/Local/hermes/cache/screenshots/heat_legend_live_cn.png"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=2)
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(URL, wait_until="load")
        await pg.wait_for_timeout(1800)
        el = await pg.query_selector(".hourly-heat")
        await el.scroll_into_view_if_needed()
        await pg.wait_for_timeout(500)
        await el.screenshot(path=OUT)
        # try CN toggle
        clicked = await pg.evaluate("""() => {
          const els=[...document.querySelectorAll('button,a,span,div')].filter(e=>e.children.length===0 && /中文|CN|Chinese/.test(e.textContent.trim()) && e.textContent.trim().length<10);
          if(els.length){els[0].click();return els[0].textContent.trim();} return null;}""")
        await pg.wait_for_timeout(900)
        await el.screenshot(path=OUTC)
        labels = await pg.evaluate("[...document.querySelectorAll('.heat-scale-labels span')].map(s=>s.textContent)")
        print("clicked:", clicked, "labels:", labels, "errs:", errs[:3])
        await b.close()

asyncio.run(main())
