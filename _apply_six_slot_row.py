import re, pathlib, shutil, datetime

p = pathlib.Path(r"C:\Users\L-User\Documents\ChatGPT\Daily Report\V2-Daily-Game-Performance-Report\index.html")
html = p.read_text(encoding="utf-8")
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
bak = p.with_name(f"_bak_index_before_six_slot_row_{ts}.html")
shutil.copy2(p, bak)

orig_len = len(html)
report = []

# ---------------------------------------------------------------- 1. carve the two panels out of the bottom band
start_marker = '<div class="panel pad compliance-panel">'
start = html.index(start_marker)
end_marker = '</div></div>\n    </section>'
end = html.index(end_marker, start)
moved = html[start:end] + '</div>'          # both panels, incident panel closed
html = html[:start] + html[end + len('</div>'):]   # drop first </div>, keeps bottom-band's own close
report.append(f"carved {len(moved)} chars (compliance + incident) out of .bottom-band")

# ---------------------------------------------------------------- 2. drop them into the row as the 6th slot
insert_at = html.index('\n      </div>\n    </section>\n\n    <section class="section">')
stack = ('<div class="status-stack">' + moved + '</div>')
html = html[:insert_at] + '\n        ' + stack + html[insert_at:]
report.append("inserted .status-stack into .platform-layout as slot 6")

# ---------------------------------------------------------------- 3. grid: six slots, 15/15/15/15/25/15
old_grid = '.platform-layout { display: grid; grid-template-columns: 15fr 15fr 15fr 20fr 35fr; gap: 10px; align-items: stretch; grid-auto-flow: row; }'
new_grid = '.platform-layout { display: grid; grid-template-columns: 15fr 15fr 15fr 15fr 25fr 15fr; gap: 10px; align-items: stretch; grid-auto-flow: row; }'
assert html.count(old_grid) == 1
html = html.replace(old_grid, new_grid)
report.append("platform-layout columns -> 15 15 15 15 25 15")

old_place = """    .platform-layout > .plat-bp { grid-column: 1; grid-row: 1; }
    .platform-layout > .plat-gp { grid-column: 2; grid-row: 1; }
    .platform-layout > .plat-ap { grid-column: 3; grid-row: 1; }
    .platform-layout .platform-charts { grid-column: 4; grid-row: 1; }
    .platform-layout > .hl-stack { grid-column: 5; grid-row: 1; }
    .platform-layout .changelog-table { grid-column: 1 / span 3; grid-row: 2; }
    .platform-layout > .status-stack { grid-column: 4 / span 2; grid-row: 2;
      grid-template-columns: 1fr 1fr; grid-template-rows: auto; }"""
new_place = """    .platform-layout > .plat-bp { grid-column: 1; grid-row: 1; }
    .platform-layout > .plat-gp { grid-column: 2; grid-row: 1; }
    .platform-layout > .plat-ap { grid-column: 3; grid-row: 1; }
    .platform-layout .platform-charts { grid-column: 4; grid-row: 1; }
    .platform-layout > .hl-stack { grid-column: 5; grid-row: 1; }
    .platform-layout > .status-stack { grid-column: 6; grid-row: 1; }"""
assert html.count(old_place) == 1
html = html.replace(old_place, new_place)
report.append("six explicit placements, single row")

# spec comment above .plat-card
old_c = """    /* 2026-10-21 (user): three platform cards replace the 14-row matrix.
       Row: BingoPlus 15 | GameZone 15 | ArenaPlus 15 | Platform Share 20 |
       Top 5 Winning Players + 100 Rounds a Day 35. Changelog and the
       Compliance/Alerts stack move to a second row so nothing is dropped. */"""
new_c = """    /* 2026-10-21 (user, final split): ONE row, six slots, 100% exactly.
         1 BingoPlus 15 | 2 GameZone 15 | 3 ArenaPlus 15 | 4 Platform Share 15
         5 Top 5 Winning Players + 100 Rounds a Day 25
         6 Compliance & PAGCOR Update + Alerts & Incident Report 15
       Changelog is the only card left in .bottom-band (full width). */"""
assert html.count(old_c) == 1
html = html.replace(old_c, new_c)
report.append("spec comment updated")

# ---------------------------------------------------------------- 4. bottom band is now changelog only
old_bb = '.bottom-band { display: grid; grid-template-columns: 36fr 30fr 34fr; gap: 10px; align-items: stretch; }'
new_bb = '.bottom-band { display: grid; grid-template-columns: 1fr; gap: 10px; align-items: stretch; }'
assert html.count(old_bb) == 1
html = html.replace(old_bb, new_bb)
report.append("bottom-band -> single full-width Changelog")

# ---------------------------------------------------------------- 5. narrow-column styling for slot 6
anchor = '    .platform-layout > .status-stack { grid-column: 6; grid-row: 1; }'
addition = anchor + """

    /* 2026-10-21 (user): slot 6 is a 15% column carrying two cards, so the
       tables become label-over-value blocks and every panel divides the
       column's full height instead of pooling blank space at the foot. */
    .platform-layout > .status-stack { grid-template-rows: 1fr 1fr; align-content: stretch; }
    .platform-layout > .status-stack > .panel { display: flex; flex-direction: column;
      justify-content: flex-start; padding: 8px 8px 9px; min-width: 0; gap: 0; }
    .platform-layout > .status-stack > .panel .side-title { margin-bottom: 5px; gap: 4px; align-items: baseline; }
    .platform-layout > .status-stack > .panel .side-title h3 { font-size: 9.5px; line-height: 1.15; letter-spacing: -.01em; }
    .platform-layout > .status-stack > .panel .side-title span { font-size: 7.5px; }
    .platform-layout > .status-stack table,
    .platform-layout > .status-stack tbody,
    .platform-layout > .status-stack tr,
    .platform-layout > .status-stack th,
    .platform-layout > .status-stack td { display: block; width: auto; min-width: 0; }
    .platform-layout > .status-stack > .compliance-panel table { flex: 1 1 auto; }
    .platform-layout > .status-stack > .compliance-panel tbody { display: flex; flex-direction: column;
      height: 100%; justify-content: space-between; }
    .platform-layout > .status-stack tr { padding: 3px 0; border-top: 1px solid var(--line); border-bottom: 0; }
    .platform-layout > .status-stack tr:first-child { border-top: 0; padding-top: 0; }
    .platform-layout > .status-stack th { padding: 0; border: 0; font-size: 7.5px; font-weight: 700;
      letter-spacing: .02em; text-transform: uppercase; color: var(--muted); white-space: normal; text-align: left; }
    .platform-layout > .status-stack td { padding: 1px 0 0; border: 0; font-size: 8.5px; line-height: 1.25;
      white-space: normal; word-break: break-word; }
    .platform-layout > .status-stack .compliance-status { font-size: 8.5px; line-height: 1.25; }
    .platform-layout > .status-stack .alert-row { padding: 5px 0; gap: 4px; align-items: flex-start; }
    .platform-layout > .status-stack .alert-row strong { font-size: 8.5px; line-height: 1.2; }
    .platform-layout > .status-stack .alert-row small { font-size: 7.5px; margin-top: 1px; }
    .platform-layout > .status-stack .status { font-size: 7px; padding: 2px 5px; white-space: normal;
      text-align: center; flex: 0 0 auto; max-width: 46%; }"""
assert html.count(anchor) == 1
html = html.replace(anchor, addition)
report.append("narrow 15% column styles added for slot 6")

# ---------------------------------------------------------------- 6. the old second-row order rules are dead
html = html.replace('    .platform-layout .changelog-table { order: 4; }\n', '')

p.write_text(html, encoding="utf-8")
report.append(f"written: {orig_len} -> {len(html)} chars")
print("\n".join(" - " + r for r in report))
print("backup:", bak.name)
