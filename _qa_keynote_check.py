from playwright.sync_api import sync_playwright
import pathlib, json

p = pathlib.Path('index.html').resolve().as_uri()
js = """() => {
  const kn = document.querySelector('.platform-charts > .keynote');
  const pc = document.querySelector('.platform-charts');
  const r = kn.getBoundingClientRect();
  const s = kn.querySelector('span');
  return {pc: [Math.round(pc.getBoundingClientRect().x), Math.round(pc.getBoundingClientRect().width)],
          kn: [Math.round(r.x), Math.round(r.width), Math.round(r.height)],
          scrollH: kn.scrollHeight, clientH: kn.clientHeight,
          spanH: s ? Math.round(s.getBoundingClientRect().height) : null,
          overflowY: kn.scrollHeight > kn.clientHeight + 1,
          heightDelta: Math.round(pc.getBoundingClientRect().height - (document.querySelector('.platform-chart').getBoundingClientRect().height + 40))};
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
