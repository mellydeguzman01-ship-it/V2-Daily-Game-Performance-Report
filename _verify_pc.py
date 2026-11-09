import asyncio, json
from playwright.async_api import async_playwright

SRC = "file:///C:/Users/L-User/Documents/ChatGPT/Daily%20Report/V2-Daily-Game-Performance-Report/index.html"
BASE = "C:/Users/L-User/Documents/ChatGPT/Daily Report/V2-Daily-Game-Performance-Report/"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w in (1920, 1440):
            pg = await b.new_page(viewport={"width": w, "height": 1400}, device_scale_factor=2)
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto(SRC); await pg.wait_for_timeout(1000)
            p1 = await pg.query_selector(".player-grid > .panel:nth-child(1)")
            p3 = await pg.query_selector(".player-feature-panel")
            await p1.scroll_into_view_if_needed(); await pg.wait_for_timeout(250)
            await p1.screenshot(path=BASE + f"_after_pie_{w}.png")
            await p3.screenshot(path=BASE + f"_after_gb_{w}.png")
            r = await pg.evaluate("""() => {
              const q=s=>document.querySelector(s);
              const p1=q('.player-grid > .panel:nth-child(1)');
              const pie=p1.querySelector('.compact-pie').getBoundingClientRect();
              const tb=p1.querySelector('.plat-new-table').getBoundingClientRect();
              const p3=q('.player-feature-panel');
              const svg=p3.querySelector('svg.gamebars-svg');
              const vb=svg.getAttribute('viewBox');
              const bars=[...svg.querySelectorAll('rect')].map(r=>r.getAttribute('height'));
              const names=[...svg.querySelectorAll('text[font-size="9.5"]')].map(t=>t.textContent);
              return {panelH:Math.round(p1.getBoundingClientRect().height),
                      pieTop:Math.round(pie.top-p1.getBoundingClientRect().top),
                      pieH:Math.round(pie.height),
                      tableTop:Math.round(tb.top-p1.getBoundingClientRect().top),
                      tableH:Math.round(tb.height),
                      gbW:Math.round(p3.getBoundingClientRect().width),
                      gbH:Math.round(p3.getBoundingClientRect().height),
                      vb, bars: bars.slice(0,4), names};
            }""")
            print(w, json.dumps(r), "errors:", errs[:2])
            await pg.close()
        await b.close()

asyncio.run(main())
