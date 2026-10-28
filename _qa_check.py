from playwright.sync_api import sync_playwright
import pathlib, json

p = pathlib.Path('index.html').resolve().as_uri()
js = """() => [...document.querySelectorAll('.platform-charts .platform-chart')].map(c => {
  const cr = c.getBoundingClientRect();
  const s = c.querySelector('svg').getBoundingClientRect();
  const d = c.querySelector(':scope>div').getBoundingClientRect();
  const labs = [...c.querySelectorAll('.ring-lbl')].map(l => {
    const r = l.getBoundingClientRect();
    return { t: l.textContent, x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width),
             inside: r.left >= cr.left && r.right <= cr.right && r.top >= cr.top && r.bottom <= cr.bottom };
  });
  return { card: [Math.round(cr.x), Math.round(cr.right), Math.round(cr.width)],
           copy: [Math.round(d.x), Math.round(d.right)],
           svg: [Math.round(s.x), Math.round(s.right)],
           overflowX: c.scrollWidth > c.clientWidth, labels: labs };
})"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    for w in (1920, 1366):
        pg = b.new_page(viewport={'width': w, 'height': 1100})
        pg.goto(p, wait_until='networkidle')
        pg.wait_for_timeout(900)
        print(w, json.dumps(pg.evaluate(js), indent=1))
        pg.close()
    b.close()
