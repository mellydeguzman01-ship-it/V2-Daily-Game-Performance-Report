#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2026-10-23 (Melly): the tile row under the headline cards becomes MONTH-TO-DATE.

She crossed out all eight day-tiles (Total Rounds .. D1 Retention) and said:

    "TANGALIN NA YANG SUBMETRICS NA YAN. TAPOS TANGGALIN NA DIN YUNG MALIIT NA TEXT
     SA MAIN CARD FOR MONTHLY KASI AYUN ANG MAGIGING SUBMETRICS"

So:
  * headline cards  = day figures only (label, value, DoD/WoW) - no monthly small print
  * tile row        = the four monthly figures that used to be that small print:
                      Monthly Bet Amount / Monthly Payout / Monthly GGR / Monthly Total Players

One tile per headline card, same order, same accent colour, so the two rows read
straight down. The eight day tiles are deleted outright.

Run from the repo root; asserts before writing. Pair with the matching edit in
build_v2_dashboard.py or the 04:15 rebuild puts the old row back.
"""
import io
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(HERE, "index.html")

BAK = os.path.join(HERE, "_bak_index_before_mtd_row_20261023.html")
if not os.path.exists(BAK):
    shutil.copy2(HTML, BAK)
    print("backup ->", os.path.basename(BAK))

s = io.open(HTML, encoding="utf-8", newline="").read()
real = s.replace("\r\n", "\n")
orig = real
fail = []


def once(old, new, label, count=1):
    global real
    n = real.count(old)
    if n != count:
        fail.append(f"{label}: expected {count} match(es), found {n}")
        return
    real = real.replace(old, new)
    print(f"  ok  {label}")


# ------------------------------------------------------------------ 1. icons
def card_block(accent):
    i = real.find(f'<article class="panel pad card {accent}">')
    if i < 0:
        return ""
    j = real.index("</article>", i) + len("</article>")
    return real[i:j]


def icon_of(accent):
    blk = card_block(accent)
    m = re.search(r'<span class="kpi-ico[^"]*"[^>]*>(<svg.*?</svg>)</span>', blk, re.S)
    return m.group(1) if m else ""


ICONS = {
    "blue": icon_of("accent-blue"),
    "green": icon_of("accent-green"),
    "orange": icon_of("accent-orange"),
    "cyan": icon_of("accent-cyan"),
}
for k, v in ICONS.items():
    if not v:
        fail.append(f"icon for {k} not found")

# ------------------------------------------------------------------ 2. CSS
CSS_ANCHOR = "    .small-grid .submetric-monthly { margin-top: auto;"
i = real.find(CSS_ANCHOR)
if i < 0:
    fail.append("CSS anchor .submetric-monthly not found")
else:
    j = real.index("\n", i) + 1
    css = """    /* 2026-10-23 (Melly): the eight day-tiles are gone. This row is now the
       MONTH-TO-DATE reading of the four headline measures, so the month no longer has
       to live as 10px small print inside the headline card. One tile per headline
       card, same order, same accent colour -> the two rows read straight down. */
    .small-grid.mtd-grid { margin-top: 10px; }
    .small-grid.mtd-grid .card { min-height: 86px; justify-content: center; }
    .small-grid.mtd-grid .mtd-label { display: flex; align-items: center; gap: 6px;
                                      color: #5b7189; font-size: 10px; font-weight: 800;
                                      letter-spacing: .05em; text-transform: uppercase;
                                      white-space: nowrap; }
    html.night .small-grid.mtd-grid .mtd-label { color: #9fb4cc; }
    .small-grid.mtd-grid .mtd-ico { display: block; flex: 0 0 13px; width: 13px;
                                    height: 13px; }
    .small-grid.mtd-grid .mtd-ico svg { width: 100%; height: 100%; display: block;
                                        overflow: visible; }
    .small-grid.mtd-grid .metric-value { margin-top: 7px; font-size: 19px;
                                         line-height: 1.15; white-space: nowrap; }
    .small-grid.mtd-grid .card.mtd-blue   { border-top-color: #6ea8ff; }
    .small-grid.mtd-grid .card.mtd-green  { border-top-color: #5fd88a; }
    .small-grid.mtd-grid .card.mtd-orange { border-top-color: #ffb347; }
    .small-grid.mtd-grid .card.mtd-cyan   { border-top-color: #40d9d0; }
    .small-grid.mtd-grid .mtd-blue   .mtd-ico { color: #2f6fd0; }
    .small-grid.mtd-grid .mtd-green  .mtd-ico { color: #248a4a; }
    .small-grid.mtd-grid .mtd-orange .mtd-ico { color: #b4620f; }
    .small-grid.mtd-grid .mtd-cyan   .mtd-ico { color: #0e8b9c; }
    html.night .small-grid.mtd-grid .mtd-blue   .mtd-ico { color: #6ea8ff; }
    html.night .small-grid.mtd-grid .mtd-green  .mtd-ico { color: #5fd88a; }
    html.night .small-grid.mtd-grid .mtd-orange .mtd-ico { color: #ffb347; }
    html.night .small-grid.mtd-grid .mtd-cyan   .mtd-ico { color: #40d9d0; }
"""
    real = real[:j] + css + real[j:]
    print("  ok  CSS: mtd-grid rules")

# ------------------------------------------------------------------ 3. small tile row
start = real.find('<div class="grid small-grid">')
if start < 0:
    fail.append("small-grid block not found")
    old_block = ""
else:
    depth = 0
    old_block = ""
    for m in re.finditer(r'<div\b[^>]*>|</div>', real[start:]):
        if m.group(0).startswith("</"):
            depth -= 1
            if depth == 0:
                end = start + m.end()
                break
        else:
            depth += 1
    old_block = real[start:end]
    if old_block.count("<article") != 8:
        fail.append(f"small-grid: expected 8 tiles, found {old_block.count('<article')}")
    for lbl in ("Total Rounds", "New Players", "ABPU", "ARPP",
                "Max Payout", "Max Multiplier", "Max Bet", "D1 Retention"):
        if lbl not in old_block:
            fail.append(f"small-grid: {lbl} tile missing")


def tile(colour, label, value, icon):
    return (
        f'<article class="panel pad card mtd-{colour}">'
        f'<div class="mtd-label"><span class="mtd-ico" aria-hidden="true">{icon}</span>'
        f'<span class="label-text">{label}</span></div>'
        f'<div class="metric-value">{value}</div></article>'
    )


TILES = [
    ("blue", "Monthly Bet Amount", "\u20b110,941,268.00"),
    ("green", "Monthly Payout", "\u20b110,736,253.40"),
    ("orange", "Monthly GGR", "\u20b1205,014.60"),
    ("cyan", "Monthly Total Players", "19,463"),
]
new_block = (
    '<div class="grid small-grid mtd-grid">\n'
    + "".join("              " + tile(c, l, v, ICONS[c]) + "\n" for c, l, v in TILES)
    + "            </div>"
)
if not fail:
    once(old_block, new_block, "tile row: 8 day tiles -> 4 monthly tiles")
else:
    print("  !! tile row not rewritten (earlier failures)")

# ------------------------------------------------------------------ 4. headline cards
for txt in ("Monthly Bet Amount \u20b110,941,268.00",
            "Monthly Payout \u20b110,736,253.40",
            "Monthly GGR \u20b1205,014.60",
            "Monthly Total Players 19,463"):
    once(f'<div class="metric-subtext">{txt}</div>', "",
         f"headline card subtext removed: {txt.split(' ')[1]}")

if fail:
    print("\nABORTED - nothing written:")
    for f in fail:
        print("  !!", f)
    sys.exit(1)

out = real.replace("\n", "\r\n")
io.open(HTML, "w", encoding="utf-8", newline="").write(out)
print(f"\nwritten: {len(orig)} -> {len(real)} chars")
