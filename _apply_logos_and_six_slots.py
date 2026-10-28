"""Platform row -> six slots (15/15/15/15/25/15) + real brand logos in the head.

Runs on whatever index.html is on disk (keeps the Top 5 stacked-block re-cut from
the parallel pass) and is idempotent for the logo swap.
"""
import json, pathlib, re, shutil, datetime

REPO = pathlib.Path(r"C:\Users\L-User\Documents\ChatGPT\Daily Report\V2-Daily-Game-Performance-Report")
LOGOS = REPO / "_logos" / "payloads.json"
p = REPO / "index.html"
html = p.read_text(encoding="utf-8")
log = []

shutil.copy2(p, p.with_name(f"_bak_index_before_logos_{datetime.datetime.now():%Y%m%d_%H%M%S}.html"))

# ---------------------------------------------------------------- 1. six-slot grid
m = re.search(r'\.platform-layout \{ display: grid; grid-template-columns: [^;]+;', html)
assert m, "platform-layout rule not found"
html = html[:m.start()] + '.platform-layout { display: grid; grid-template-columns: 15fr 15fr 15fr 15fr 25fr 15fr;' + html[m.end():]
log.append("grid -> 15/15/15/15/25/15")

# ---------------------------------------------------------------- 2. explicit placements
old_place = re.search(
    r'\.platform-layout > \.plat-bp \{ grid-column: 1; grid-row: 1; \}.*?\.platform-layout > \.status-stack \{[^}]*\}',
    html, re.S)
assert old_place, "placement block not found"
new_place = """.platform-layout > .plat-bp { grid-column: 1; grid-row: 1; }
    .platform-layout > .plat-gp { grid-column: 2; grid-row: 1; }
    .platform-layout > .plat-ap { grid-column: 3; grid-row: 1; }
    .platform-layout .platform-charts { grid-column: 4; grid-row: 1; }
    .platform-layout > .hl-stack { grid-column: 5; grid-row: 1; }
    .platform-layout > .status-stack { grid-column: 6; grid-row: 1; }"""
html = html[:old_place.start()] + new_place + html[old_place.end():]
log.append("placements -> slots 1-6 in row 1")

# ---------------------------------------------------------------- 3. status stack back in the row
start = html.index('<div class="status-stack">')
end_marker = '</div></div>\n</div>\n    </section>'
end = html.index(end_marker, start)
block = html[start:end] + '</div></div>'
html = html[:start] + html[end + len('</div></div>'):]
log.append(f"extracted .status-stack ({len(block)} chars)")

anchor = '\n      </div>\n    </section>\n\n    <section class="section">'
pos = html.index(anchor)
html = html[:pos] + '\n        ' + block + html[pos:]
log.append("status-stack dropped in as slot 6")

# ---------------------------------------------------------------- 4. bottom band = Changelog only
m = re.search(r'\.bottom-band \{ display: grid; grid-template-columns: [^;]+;', html)
assert m
html = html[:m.start()] + '.bottom-band { display: grid; grid-template-columns: 1fr;' + html[m.end():]
log.append("bottom-band -> single full-width Changelog")

# ---------------------------------------------------------------- 5. logos replace the letter chips
payloads = json.loads(LOGOS.read_text(encoding="utf-8"))
names = {"BP1": ("bp", "BingoPlus"), "GP": ("gp", "GameZone"), "AP": ("ap", "ArenaPlus")}
for code, (key, brand) in names.items():
    old = f'<div class="plat-emblem">{code}</div><div><div class="plat-name">'
    new = (f'<img class="plat-logo" alt="{brand} logo" src="{payloads[key]}">'
           f'<div class="plat-id"><div class="plat-name">')
    if old in html:
        html = html.replace(old, new)
        log.append(f"{code} emblem -> {brand} logo")

# ---------------------------------------------------------------- 6. logo CSS
emblem_rule_end = html.index('.plat-gp .plat-emblem { background: var(--blue); }')
emblem_tail = '.plat-ap .plat-emblem { background: var(--violet); }'
i = html.index(emblem_tail) + len(emblem_tail)
logo_css = """

    /* 2026-10-21 (user): "palitan mo yan ng logo mismo ng platform" - the letter
       chips are gone, the real brand logos sit in their place. The head is a
       2-row grid so a wide logo never squeezes the platform name: row 1 is
       logo + code chip, row 2 is the name and its game list at full width. */
    .plat-head { display: grid; grid-template-columns: minmax(0, 1fr) auto;
                 grid-template-rows: auto auto; gap: 4px 6px; align-items: center; }
    .plat-logo { grid-column: 1; grid-row: 1; display: block; height: 24px; width: auto;
                 max-width: 100%; object-fit: contain; object-position: left center; }
    .plat-chip { grid-column: 2; grid-row: 1; margin-left: 0; }
    .plat-id { grid-column: 1 / -1; grid-row: 2; min-width: 0; }
    .plat-id .plat-name { font-size: 11px; }"""
html = html[:i] + logo_css + html[i:]
log.append("logo CSS added")

p.write_text(html, encoding="utf-8")
print("\n".join(" - " + l for l in log))
print("sixcol:", html.count("15fr 15fr 15fr 15fr 25fr 15fr"),
      "| fivecol:", html.count("repeat(5, minmax(0, 1fr))"),
      "| logo imgs:", html.count('class="plat-logo"'),
      "| status-stacks:", html.count('class="status-stack"'))
