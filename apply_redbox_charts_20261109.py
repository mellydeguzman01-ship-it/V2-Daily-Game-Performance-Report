#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2026-11-09 (Melly): remove the two red-box Key Insights, grow those charts
into the freed space, and make the MTD window explicit (option A).

  1. drop ['.pg-denom', ...] and ['.pp-engage', ...] from the page's `notes` array
  2. vertically stretch the plot area of the denomination + engagement charts
     (bars/rows get taller, type size unchanged -> no distortion)
  3. MTD tile footers say the period they cover: "Nov 1-8 · OCT full month: ..."

Run in the repo root:  python apply_redbox_charts_20261109.py
"""
import re
from pathlib import Path

IDX = Path(__file__).resolve().parent / "index.html"
html = IDX.read_text(encoding="utf-8")
orig = html
NUM = r"(-?\d+(?:\.\d+)?)"


def tidy(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s if s else "0"


# ------------------------------------------------- 1. drop the two notes ----
before = len(html)
html = re.sub(r"\n\s*\['\.pg-denom',\s*'[^']*'\],", "", html)
html = re.sub(r"\n\s*\['\.pp-engage',\s*'[^']*'\],", "", html)
print("notes removed:", before - len(html), "chars")

# ----------------------------------------------------- 2. grow the charts ----
def stretch(svg, a, b, k):
    """Scale every y coordinate inside the plot band [a, b]; push what sits
    below the band down by the same amount the band grew."""
    d = (b - a) * (k - 1.0)

    def yy(v):
        v = float(v)
        if a <= v <= b:
            return tidy(a + (v - a) * k)
        if v > b:
            return tidy(v + d)
        return tidy(v)

    svg = re.sub(r'\b(y|y1|y2)="(' + NUM + r')"',
                 lambda m: f'{m.group(1)}="{yy(m.group(2))}"', svg)
    svg = re.sub(r'\bheight="(' + NUM + r')"',
                 lambda m: f'height="{tidy(float(m.group(1)) * k)}"', svg)

    def vb(m):
        vx, vy, vw, vh = (float(x) for x in m.groups())
        return f'viewBox="{tidy(vx)} {tidy(vy)} {tidy(vw)} {tidy(vh + d)}"'

    return re.sub(r'viewBox="([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+)"', vb, svg, count=1)


m = re.search(r'<svg class="chart denom-svg".*?</svg>', html, re.S)
if m:
    html = html.replace(m.group(0), stretch(m.group(0), 25.0, 190.0, 1.22))
    print("denom chart stretched 1.22x")
else:
    print("WARN: denom svg not found")

m = re.search(r'<svg class="chart eng-svg".*?</svg>', html, re.S)
if m:
    html = html.replace(m.group(0), stretch(m.group(0), 30.0, 150.0, 1.22))
    print("engage chart stretched 1.22x")
else:
    print("WARN: eng svg not found")

# ------------------------------------------------ 3. MTD window on tiles ----
n = html.count("OCT full month:")
html = html.replace(">OCT full month:", ">Nov 1–8 · OCT full month:")
print("mtd footers relabelled:", n)

IDX.write_text(html, encoding="utf-8")
print("done:", f"{len(html) - len(orig):+d} chars")
