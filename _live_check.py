
import asyncio, json
from playwright.async_api import async_playwright
URL="https://mellydeguzman01-ship-it.github.io/V2-Daily-Game-Performance-Report/?cb=zz1"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={"width":390,"height":1200}, device_scale_factor=3)
        await pg.goto(URL, wait_until="load"); await pg.wait_for_timeout(1500)
        r=await pg.evaluate("""()=>{const g=document.querySelector('.header-metrics');const c=g.querySelector('.card');const m=document.querySelector('.small-grid.mtd-grid');return {cols:getComputedStyle(g).gridTemplateColumns,h:c.getBoundingClientRect().height,val:getComputedStyle(c.querySelector('.metric-value')).fontSize,mtd:getComputedStyle(m).gridTemplateColumns};}""")
        print(json.dumps(r))
        b1=await (await pg.query_selector('.header-metrics')).bounding_box()
        b2=await (await pg.query_selector('.small-grid.mtd-grid')).bounding_box()
        await pg.screenshot(path=r"C:/Users/L-User/Documents/ChatGPT/Daily Report/V2-Daily-Game-Performance-Report/_live390.png",
            clip={"x":0,"y":b1["y"]-30,"width":390,"height":(b2["y"]+b2["height"])-(b1["y"]-30)+12})
        await b.close()
asyncio.run(main())
