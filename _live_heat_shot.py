
import asyncio
from playwright.async_api import async_playwright
URL="https://mellydeguzman01-ship-it.github.io/V2-Daily-Game-Performance-Report/?cb=hb9"
OUT=r"C:/Users/L-User/Documents/ChatGPT/Daily Report/V2-Daily-Game-Performance-Report/_live_heat_bands.png"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={"width":1380,"height":1200}, device_scale_factor=2)
        try:
            await pg.goto(URL, wait_until="domcontentloaded", timeout=90000)
        except Exception as e:
            print("goto warn:", str(e)[:120])
        await pg.wait_for_timeout(3000)
        el=await pg.query_selector(".hourly-heat")
        if not el:
            print("NO PANEL"); await b.close(); return
        await el.scroll_into_view_if_needed(); await pg.wait_for_timeout(600)
        await el.screenshot(path=OUT)
        n=await pg.evaluate("document.querySelectorAll('.heat-legend span').length")
        print("chips", n, "saved")
        await b.close()
asyncio.run(main())
