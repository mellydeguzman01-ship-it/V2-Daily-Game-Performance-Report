#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2026-10-23 (Melly): headline cards = day figures, submetrics = the month.

MAIN ROW      Bet Amount | Payout | GGR | Players          (day figures)
SUBMETRIC     Monthly Bet Amount | Monthly Payout | Monthly GGR | Monthly Total Players

So the fourth headline card stops being "MTD GGR" and becomes "Players" (promoted
out of the small tile row, which keeps its other eight tiles). The monthly figure
moves into each card's subtext line, labelled in words instead of "October MTD".

Run from the repo root; it asserts before it writes. Pair it with the matching edit
in build_v2_dashboard.py, or the next 04:15 rebuild will restore the old row.
"""
import io
import os
import re
import shutil
import sys
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(HERE, "index.html")
sys.path.insert(0, os.path.dirname(HERE))

from build_v2_dashboard import delta, delta_wow  # noqa: E402  (same maths as the build)

DAY_PLAYERS = 665
PRIOR_PLAYERS = 800
WOW_PLAYERS = 716

png = os.path.join(HERE, "_bak_index_before_kpi_monthly_20261023.html")
if not os.path.exists(png):
    shutil.copy2(HTML, png)
    print("backup ->", os.path.basename(png))

s = io.open(HTML, encoding="utf-8", newline="").read()
real = s.replace("\r\n", "\n")
orig = real

fail = []


def sub_once(old, new, label, count=1):
    global real
    n = real.count(old)
    if n != count:
        fail.append(f"{label}: expected {count} match(es), found {n}")
        return
    real = real.replace(old, new)
    print(f"  ok  {label}")


dod_cls, dod_txt = delta(DAY_PLAYERS, PRIOR_PLAYERS)
wow_cls, wow_txt = delta_wow(DAY_PLAYERS, WOW_PLAYERS)
print(f"players DoD={dod_txt!r} ({dod_cls})  WoW={wow_txt!r} ({wow_cls})")

# ---------------------------------------------------------------- 1. fourth card
i = real.find('<article class="panel pad card accent-cyan">')
if i < 0:
    fail.append("fourth headline card not found")
    old_card = new_card = ""
else:
    j = real.index("</article>", i) + len("</article>")
    old_card = real[i:j]
    if "MTD GGR" not in old_card:
        fail.append("fourth headline card is not the MTD GGR card any more")
    people_icon = (
        '<svg viewBox="0 0 24 24">'
        '<circle cx="9" cy="8" r="3.2" stroke="currentColor" fill="none" stroke-width="1.7" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M3.4 19.4c0-3 2.5-5 5.6-5s5.6 2 5.6 5" stroke="currentColor" fill="none" '
        'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M15.9 7.2a3 3 0 0 1 0 5.6" stroke="currentColor" fill="none" stroke-width="1.7" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M17.2 14.9c2 .6 3.4 2.3 3.4 4.5" stroke="currentColor" fill="none" '
        'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
        "</svg>"
    )
    new_card = (
        '<article class="panel pad card accent-cyan">'
        '<div class="metric-label"><span class="kpi-ico people c-cyan" aria-hidden="true">'
        + people_icon
        + "</span>Players</div>"
        f'<div class="metric-value">{DAY_PLAYERS:,}</div>'
        '<div class="metric-subtext">Monthly Total Players 19,463</div>'
        '<div class="metric-foot">'
        f'<span class="{dod_cls}">{dod_txt}</span><span class="{wow_cls}">{wow_txt}</span>'
        "</div></article>"
    )
    sub_once(old_card, new_card, "headline card 4: MTD GGR -> Players")

# ---------------------------------------------------------------- 2. subtexts
sub_once('<div class="metric-subtext">October MTD ₱10,941,268.00</div>',
         '<div class="metric-subtext">Monthly Bet Amount ₱10,941,268.00</div>',
         "subtext: Bet Amount -> Monthly Bet Amount")
sub_once('<div class="metric-subtext">October MTD ₱10,736,253.40</div>',
         '<div class="metric-subtext">Monthly Payout ₱10,736,253.40</div>',
         "subtext: Payout -> Monthly Payout")
sub_once('<div class="metric-subtext">October MTD ₱205,014.60</div>',
         '<div class="metric-subtext">Monthly GGR ₱205,014.60</div>',
         "subtext: GGR -> Monthly GGR")

# ---------------------------------------------------------------- 3. small tile row
tiles = list(re.finditer(r'<article class="panel pad card">.*?</article>', real, re.S))
target = [t for t in tiles if '<span class="label-text">Players</span>' in t.group(0)]
if len(target) != 1:
    fail.append(f"Players tile: expected 1 match, found {len(target)}")
else:
    real = real[:target[0].start()] + real[target[0].end():]
    print("  ok  small tile row: Players tile removed (8 tiles left)")

# ---------------------------------------------------------------- 4. Chinese labels
sub_once("'Bet Amount': '投注金额',",
         "'Bet Amount': '投注金额', 'Monthly Bet Amount': '月度投注金额', "
         "'Monthly Payout': '月度派彩', 'Monthly GGR': '月度游戏总收入', "
         "'Monthly Total Players': '月度玩家总数',",
         "i18n: four monthly labels")

if fail:
    print("\nABORTED - nothing written:")
    for f in fail:
        print("  !!", f)
    sys.exit(1)

out = real.replace("\n", "\r\n")
io.open(HTML, "w", encoding="utf-8", newline="").write(out)
print(f"\nwritten: {len(orig)} -> {len(real)} chars")
