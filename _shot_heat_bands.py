import asyncio, json
from playwright.async_api import async_playwright

SRC = "file:///C:/Users/L-User/Documents/ChatGPT/Daily%20Report/V2-Daily-Game-Performance-Report/index.html"
BASE = "C:/Users/L-User/Documents/ChatGPT/Daily Report/V2-Daily-Game-Performance-Report/"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w, tag in ((1440, "desk"), (390, "mob")):
            pg = await b.new_page(viewport={"width": w, "height": 1200}, device_scale_factor=2)
            await pg.goto(SRC); await pg.wait_for_timeout(900)
            el = await pg.query_selector(".hourly-heat")
            await el.scroll_into_view_if_needed()
            await pg.wait_for_timeout(300)
            await el.screenshot(path=BASE + f"_heat_{tag}.png")
            r = await pg.evaluate("""() => {
              const p=document.querySelector('.hourly-heat');
              const lg=p.querySelector('.heat-legend');
              const lr=lg.getBoundingClientRect(), pr=p.getBoundingClientRect();
              return {legendW: Math.round(lr.width), panelW: Math.round(pr.width),
                      legendH: Math.round(lr.height),
                      overflowX: lg.scrollWidth - lg.clientWidth,
                      chips: lg.querySelectorAll('span').length,
                      svgW: Math.round(p.querySelector('svg').getBoundingClientRect().width),
                      panelH: Math.round(pr.height)};
            }""")
            print(tag, json.dumps(r))
            await pg.close()
        await b.close()

asyncio.run(main())
