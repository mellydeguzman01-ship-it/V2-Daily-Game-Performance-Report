import asyncio, json
from playwright.async_api import async_playwright

SRC = "file:///C:/Users/L-User/Documents/ChatGPT/Daily%20Report/V2-Daily-Game-Performance-Report/index.html"
BASE = "C:/Users/L-User/Documents/ChatGPT/Daily Report/V2-Daily-Game-Performance-Report/"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
        await pg.goto(SRC); await pg.wait_for_timeout(800)
        r = await pg.evaluate("""() => {
          const g=document.querySelector('.header-metrics');
          const c=g.querySelector('.card');
          const m=document.querySelector('.small-grid.mtd-grid');
          return {cols:getComputedStyle(g).gridTemplateColumns,
                  h:c.getBoundingClientRect().height,
                  val:getComputedStyle(c.querySelector('.metric-value')).fontSize,
                  foot:getComputedStyle(c.querySelector('.metric-foot')).position,
                  mtdCols:getComputedStyle(m).gridTemplateColumns,
                  mtdH:m.querySelector('.card').getBoundingClientRect().height};
        }""")
        print(json.dumps(r))
        el = await pg.query_selector(".topbar")
        bb = await el.bounding_box()
        await pg.screenshot(path=BASE+"_desk1440.png", clip={"x":0,"y":bb["y"],"width":1440,"height":min(700,bb["height"])})
        await b.close()

asyncio.run(main())
