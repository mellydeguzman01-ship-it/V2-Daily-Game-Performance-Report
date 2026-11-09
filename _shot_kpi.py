import asyncio
from playwright.async_api import async_playwright

SRC = "file:///C:/Users/L-User/Documents/ChatGPT/Daily%20Report/V2-Daily-Game-Performance-Report/index.html"
BASE = "C:/Users/L-User/Documents/ChatGPT/Daily Report/V2-Daily-Game-Performance-Report/"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w in (390, 360):
            pg = await b.new_page(viewport={"width": w, "height": 1400}, device_scale_factor=3)
            await pg.goto(SRC)
            await pg.wait_for_timeout(900)
            el = await pg.query_selector(".header-metrics")
            g = await pg.query_selector(".small-grid.mtd-grid")
            b1 = await el.bounding_box(); b2 = await g.bounding_box()
            await pg.screenshot(path=BASE + f"_kpi_{w}.png", clip={
                "x": 0, "y": b1["y"]-26, "width": w,
                "height": (b2["y"]+b2["height"]) - (b1["y"]-26) + 12})
            print(w, b1, b2)
            # night mode too
            await pg.click("#nightModeButton")
            await pg.wait_for_timeout(400)
            await pg.screenshot(path=BASE + f"_kpi_{w}_night.png", clip={
                "x": 0, "y": b1["y"]-26, "width": w,
                "height": (b2["y"]+b2["height"]) - (b1["y"]-26) + 12})
            await pg.close()
        await b.close()

asyncio.run(main())
