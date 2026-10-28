from playwright.sync_api import sync_playwright
import pathlib, json

p = pathlib.Path('index.html').resolve().as_uri()
js = """() => {
  const cards = [...document.querySelectorAll('.plat-card')].map(c => {
    const r = c.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.right), Math.round(r.width)];
  });
  const charts = [...document.querySelectorAll('.platform-charts .platform-chart')].map(c => {
    const r = c.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.right), Math.round(r.width)];
  });
  return {cards, charts};
}"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    for w in (1920, 1366, 1280):
        pg = b.new_page(viewport={'width': w, 'height': 1100})
        pg.goto(p, wait_until='networkidle')
        pg.wait_for_timeout(700)
        print(w, json.dumps(pg.evaluate(js)))
        pg.close()
    b.close()
