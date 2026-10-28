from playwright.sync_api import sync_playwright
import pathlib, json

paths = {
    'template': pathlib.Path('index.html').resolve().as_uri(),
    'built': pathlib.Path('D:/UserData/Temp/test_share_align.html').as_uri(),
}
js = """() => {
  const cards = [...document.querySelectorAll('.plat-card')].map(c => {
    const r = c.getBoundingClientRect(); return {x: Math.round(r.x), w: Math.round(r.width), right: Math.round(r.right)};
  });
  const charts = [...document.querySelectorAll('.platform-charts .platform-chart')].map(c => {
    const r = c.getBoundingClientRect(); return {x: Math.round(r.x), w: Math.round(r.width), right: Math.round(r.right)};
  });
  const pc = document.querySelector('.platform-charts');
  const ss = pc ? pc.closest('.side-stack') : null;
  return {cards, charts, pc: pc ? {x: Math.round(pc.getBoundingClientRect().x), w: Math.round(pc.getBoundingClientRect().width), cols: getComputedStyle(pc).gridTemplateColumns} : null, sideStack: ss ? {x: Math.round(ss.getBoundingClientRect().x), w: Math.round(ss.getBoundingClientRect().width), col: getComputedStyle(ss).gridColumn, row: getComputedStyle(ss).gridRow} : null};
}"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    for name, url in paths.items():
        pg = b.new_page(viewport={'width': 1920, 'height': 1100})
        pg.goto(url, wait_until='networkidle')
        pg.wait_for_timeout(900)
        print(name, json.dumps(pg.evaluate(js), indent=1))
        pg.close()
    b.close()
