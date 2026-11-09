import asyncio, json
from playwright.async_api import async_playwright

SRC = "file:///C:/Users/L-User/Documents/ChatGPT/Daily%20Report/V2-Daily-Game-Performance-Report/index.html"

JS = r"""
() => {
  const out = [];
  const c = document.querySelector('.header-metrics > .card');
  const cr = c.getBoundingClientRect();
  out.push({card:[Math.round(cr.left),Math.round(cr.right)], sw:c.scrollWidth, cw:c.clientWidth});
  c.querySelectorAll('*').forEach(el=>{
    const r = el.getBoundingClientRect();
    if (r.width && (r.right > cr.right + 0.5 || r.left < cr.left - 0.5))
      out.push({el: el.className || el.tagName, l: Math.round(r.left), r: Math.round(r.right)});
  });
  // pseudo elements
  for (const pe of ['::before','::after']) {
    const cs = getComputedStyle(c, pe);
    out.push({pe, content: cs.content, w: cs.width, pos: cs.position,
              l: cs.left, r: cs.right, tr: cs.transform});
  }
  return out;
}
"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 390, "height": 900}, device_scale_factor=2)
        await pg.goto(SRC)
        await pg.wait_for_timeout(700)
        for r in await pg.evaluate(JS):
            print(json.dumps(r, ensure_ascii=False))
        await b.close()

asyncio.run(main())
