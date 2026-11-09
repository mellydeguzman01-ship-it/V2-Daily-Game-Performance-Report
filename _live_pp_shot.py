import asyncio
from playwright.async_api import async_playwright
URL="https://mellydeguzman01-ship-it.github.io/V2-Daily-Game-Performance-Report/?cb=pp11"
OUT=r"C:/Users/L-User/Documents/ChatGPT/Daily Report/V2-Daily-Game-Performance-Report/_live_pp_pc.png"

async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={"width":1920,"height":1200}, device_scale_factor=1.5)
        try:
            await pg.goto(URL, wait_until="domcontentloaded", timeout=90000)
        except Exception as e:
            print("warn", str(e)[:100])
        await pg.wait_for_timeout(2500)
        p1=await pg.query_selector(".player-grid > .panel:nth-child(1)")
        p3=await pg.query_selector(".player-feature-panel")
        if not p3:
            print("NO PANELS"); await b.close(); return
        await p3.scroll_into_view_if_needed(); await pg.wait_for_timeout(500)
        b1=await p1.bounding_box(); b3=await p3.bounding_box()
        y=min(b1["y"],b3["y"]) - 30
        h=max(b1["y"]+b1["height"], b3["y"]+b3["height"]) - y + 20
        await pg.screenshot(path=OUT, clip={"x":0,"y":y,"width":1920,"height":min(h,1200)})
        print("ok", round(h))
        await b.close()

asyncio.run(main())
