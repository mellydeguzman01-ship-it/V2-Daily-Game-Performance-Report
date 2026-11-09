import asyncio, json
from playwright.async_api import async_playwright

SRC = "file:///C:/Users/L-User/Documents/ChatGPT/Daily%20Report/V2-Daily-Game-Performance-Report/index.html"
BASE = "C:/Users/L-User/Documents/ChatGPT/Daily Report/V2-Daily-Game-Performance-Report/"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1440, "height": 1400}, device_scale_factor=2)
        await pg.goto(SRC); await pg.wait_for_timeout(1000)
        # find the Player Performance section
        sec = await pg.query_selector("section.section:has(h2:text-is('Player Performance'))")
        if not sec:
            print("section not found"); await b.close(); return
        await sec.scroll_into_view_if_needed(); await pg.wait_for_timeout(300)
        # first two panels only
        p1 = await pg.query_selector(".player-grid > .panel:nth-child(1)")
        p3 = await pg.query_selector(".player-feature-panel")
        b1 = await p1.bounding_box(); b2 = await p3.bounding_box()
        print(json.dumps({"p1": b1, "p3": b2}))
        await pg.screenshot(path=BASE + "_pc_before.png",
                            clip={"x": 0, "y": b1["y"]-40, "width": 1440,
                                  "height": (b1["height"]+80)})
        await p3.screenshot(path=BASE + "_pc_before_gamebars.png")
        await p1.screenshot(path=BASE + "_pc_before_pie.png")
        await b.close()

asyncio.run(main())
