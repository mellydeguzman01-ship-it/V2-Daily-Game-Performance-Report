import asyncio, json
from playwright.async_api import async_playwright

SRC = "file:///C:/Users/L-User/Documents/ChatGPT/Daily%20Report/V2-Daily-Game-Performance-Report/index.html"
BASE = "C:/Users/L-User/Documents/ChatGPT/Daily Report/V2-Daily-Game-Performance-Report/"

TABLE = """
<table>
 <colgroup><col style="width:31%"><col style="width:23%"><col style="width:23%"><col style="width:23%"></colgroup>
 <thead><tr><th>Platform</th><th>Players</th><th>New</th><th>New share</th></tr></thead>
 <tbody>
  <tr><th scope="row">BingoPlus</th><td>3,030</td><td>1,176</td><td>38.8%</td></tr>
  <tr><th scope="row">GameZone</th><td>2,460</td><td>963</td><td>39.1%</td></tr>
  <tr><th scope="row">ArenaPlus</th><td>24</td><td>10</td><td>41.7%</td></tr>
 </tbody>
</table>
"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w in (1920, 1440):
            pg = await b.new_page(viewport={"width": w, "height": 1400}, device_scale_factor=2)
            await pg.goto(SRC); await pg.wait_for_timeout(900)
            await pg.evaluate("(t)=>{const d=document.querySelector('.plat-new-table'); if(d) d.innerHTML=t;}", TABLE)
            await pg.wait_for_timeout(300)
            p1 = await pg.query_selector(".player-grid > .panel:nth-child(1)")
            await p1.scroll_into_view_if_needed(); await pg.wait_for_timeout(200)
            await p1.screenshot(path=BASE + f"_mock_pie_{w}.png")
            r = await pg.evaluate("""() => {
              const p=document.querySelector('.player-grid > .panel:nth-child(1)');
              const pie=p.querySelector('.compact-pie').getBoundingClientRect();
              const pr=p.getBoundingClientRect();
              const tb=p.querySelector('.plat-new-table').getBoundingClientRect();
              const svg=p.querySelector('.donut-wrap svg').getBoundingClientRect();
              const t=p.querySelector('.plat-new-table table').getBoundingClientRect();
              return {panelH:Math.round(pr.height), pieTop:Math.round(pie.top-pr.top),
                      pieH:Math.round(pie.height), svgTop:Math.round(svg.top-pr.top),
                      tableTop:Math.round(tb.top-pr.top), tableH:Math.round(tb.height),
                      tableInnerH:Math.round(t.height)};
            }""")
            print(w, json.dumps(r))
            await pg.close()
        await b.close()

asyncio.run(main())
