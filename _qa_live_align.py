from playwright.sync_api import sync_playwright
import json, time

url = "https://mellydeguzman01-ship-it.github.io/V2-Daily-Game-Performance-Report/?v=" + str(int(time.time()))
js = """() => {
  const cards = [...document.querySelectorAll('.plat-card')].map(c => {
    const r = c.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.right)];
  });
  const charts = [...document.querySelectorAll('.platform-charts .platform-chart')].map(c => {
    const r = c.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.right), Math.round(r.width)];
  });
  const kn = document.querySelector('.platform-charts > .keynote');
  return {
    width: innerWidth,
    cards, charts,
    note: kn ? kn.innerText.replace(/\\s+/g, ' ').slice(0, 90) : null,
    keynoteH: kn ? Math.round(kn.getBoundingClientRect().height) : null,
    gpTop5: document.querySelectorAll('.gp-top5-item').length,
    bodyOver: document.documentElement.scrollWidth > innerWidth,
    cols: getComputedStyle(document.querySelector('.platform-charts')).gridTemplateColumns,
  };
}"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    for w in (1920, 1366):
        pg = b.new_page(viewport={'width': w, 'height': 1200})
        pg.goto(url, wait_until='networkidle')
        pg.wait_for_timeout(1200)
        print(w, json.dumps(pg.evaluate(js), indent=1))
        pg.close()
    b.close()
