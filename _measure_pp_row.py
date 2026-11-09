import json, sys
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8971/index.html"
W = int(sys.argv[1]) if len(sys.argv) > 1 else 1909

JS = r"""
() => {
  const out = {};
  const row = document.querySelector('.player-grid');
  const panels = [...row.children];
  out.row = row.getBoundingClientRect().toJSON();
  out.rowStyle = getComputedStyle(row).gridTemplateColumns;
  out.panels = panels.map(p => {
    const r = p.getBoundingClientRect();
    const cs = getComputedStyle(p);
    const kids = [...p.children].map(c => {
      const cr = c.getBoundingClientRect();
      return {cls: c.className && c.className.toString().slice(0,60), top: +cr.top.toFixed(1), bottom: +cr.bottom.toFixed(1), h: +cr.height.toFixed(1)};
    });
    const last = p.lastElementChild ? p.lastElementChild.getBoundingClientRect() : null;
    return {
      cls: p.className.slice(0,70), h: +r.height.toFixed(1), top:+r.top.toFixed(1), bottom:+r.bottom.toFixed(1),
      padB: cs.paddingBottom, slack: last ? +(r.bottom - parseFloat(cs.paddingBottom) - last.bottom).toFixed(1) : null,
      kids
    };
  });
  const q = s => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect(); return {w:+r.width.toFixed(1), h:+r.height.toFixed(1), top:+r.top.toFixed(1), bottom:+r.bottom.toFixed(1), left:+r.left.toFixed(1), right:+r.right.toFixed(1)}; };
  out.pie = q('.player-grid > .panel:first-child .compact-pie');
  out.donut = q('.player-grid > .panel:first-child .donut-wrap');
  out.donutSvg = q('.player-grid > .panel:first-child .donut-wrap svg');
  out.legend = q('.player-grid > .panel:first-child .legend-list');
  out.table = q('.player-grid > .panel:first-child .plat-new-table');
  out.heatSvg = q('.hourly-heat-svg');
  out.heatPanel = q('.hourly-heat');
  out.barsSvg = q('.gamebars-svg');
  out.barsPanel = q('.panel.pg-chart');
  out.retention = [...document.querySelectorAll('.pg-retention .retention-row')].map(e=>{const r=e.getBoundingClientRect();return {h:+r.height.toFixed(1), top:+r.top.toFixed(1), bottom:+r.bottom.toFixed(1)}});
  out.doc = {sw: document.documentElement.scrollWidth, iw: innerWidth, sh: document.documentElement.scrollHeight};
  out.viewBoxes = {
    heat: document.querySelector('.hourly-heat-svg')?.getAttribute('viewBox'),
    bars: document.querySelector('.gamebars-svg')?.getAttribute('viewBox'),
  };
  return out;
}
"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": W, "height": 1200})
    pg.goto(URL, wait_until="load")
    pg.wait_for_timeout(1200)
    data = pg.evaluate(JS)
    print(json.dumps(data, indent=1))
    row = data["row"]
    pg.screenshot(path=f"_pp_before_{W}.png", clip={"x":0,"y":max(0,row["y"]-10),"width":W,"height":min(700,row["height"]+30)}, full_page=True)
    b.close()
