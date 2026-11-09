import asyncio, json
from playwright.async_api import async_playwright

SRC = "file:///C:/Users/L-User/Documents/ChatGPT/Daily%20Report/V2-Daily-Game-Performance-Report/index.html"
OUT = "C:/Users/L-User/Documents/ChatGPT/Daily Report/V2-Daily-Game-Performance-Report/live_kpi4_onerow_{w}.png"

JS = r"""
() => {
  const rep = [];
  const check = (el, tag) => {
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    rep.push({tag, w: Math.round(r.width), h: Math.round(r.height),
      sw: el.scrollWidth, cw: el.clientWidth,
      over: el.scrollWidth - el.clientWidth,
      fs: cs.fontSize, txt: (el.textContent||'').trim().slice(0,28)});
  };
  document.querySelectorAll('.header-metrics > .card').forEach((c,i)=>{
    check(c, 'card'+i);
    check(c.querySelector('.metric-value'), 'val'+i);
    const l = c.querySelector('.metric-label'); if (l) check(l,'lab'+i);
    const f = c.querySelector('.metric-foot'); if (f) check(f,'foot'+i);
  });
  document.querySelectorAll('.small-grid.mtd-grid > .card').forEach((c,i)=>{
    check(c, 'mtd'+i);
    check(c.querySelector('.metric-value'), 'mtdval'+i);
    const p = c.querySelector('.mtd-prev'); if (p) check(p,'mtdprev'+i);
    const l = c.querySelector('.mtd-label'); if (l) check(l,'mtdlab'+i);
  });
  const g1 = document.querySelector('.header-metrics');
  const g2 = document.querySelector('.small-grid.mtd-grid');
  rep.push({tag:'grid-header', cols: getComputedStyle(g1).gridTemplateColumns, h: Math.round(g1.getBoundingClientRect().height)});
  rep.push({tag:'grid-mtd', cols: getComputedStyle(g2).gridTemplateColumns, h: Math.round(g2.getBoundingClientRect().height)});
  // overlap check: label rect vs foot rect
  const ov = [];
  document.querySelectorAll('.header-metrics > .card').forEach((c,i)=>{
    const a = c.querySelector('.metric-label'), b = c.querySelector('.metric-foot');
    if (!a||!b) return;
    const ra=a.getBoundingClientRect(), rb=b.getBoundingClientRect();
    const inter = !(ra.right<=rb.left||rb.right<=ra.left||ra.bottom<=rb.top||rb.bottom<=ra.top);
    ov.push({i, overlap:inter});
  });
  rep.push({tag:'label_foot_overlap', v: ov});
  rep.push({tag:'doc_scrollW', v: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth});
  return rep;
}
"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w in (390, 360, 430, 768):
            pg = await b.new_page(viewport={"width": w, "height": 900}, device_scale_factor=2)
            await pg.goto(SRC)
            await pg.wait_for_timeout(900)
            rep = await pg.evaluate(JS)
            print("=== width", w)
            for r in rep:
                print(json.dumps(r, ensure_ascii=False))
            el = await pg.query_selector(".topbar")
            box = await el.bounding_box()
            await pg.screenshot(path=OUT.format(w=w),
                                clip={"x":0,"y":0,"width":w,"height":min(760, box["height"]+30)})
            await pg.close()
        await b.close()

asyncio.run(main())
