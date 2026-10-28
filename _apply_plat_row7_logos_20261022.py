#!/usr/bin/env python3
"""2026-10-22 (user):
  1) "ILAGAY SA GITNA YUNG LOGO NG PLATFORM."              -> logo centred in each card
  2) "YUNG LOGO NG BINGOPLUS, IPANTAY MO YUNG SIZE SA GAMEZONE AT ARENAPLUS
      KASI SOBRANG LIIT NG SIZE NG SA BP"                   -> BP asset cropped + upscaled
  3) "IBALIK MO NA LANG ULIT YUNG CHANGELOG"               -> back into the platform row
  4) "ONE ROW: BINGOPLUS 10% | GAMEZONE 10% | ARENAPLUS 10% | PLATFORM SHARE 15% |
      TOP 5, 100 ROUNDS 20% | CHANGELOG 25% | COMPLIANCE, ALERTS 10%"

Fail-closed, line-ending safe. The BP logo lives in v2_platform_logos.json (a data
asset the builder loads), so it is fixed there rather than in code.
"""
import base64
import io
import json
import os
import re
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
TPL = HERE / "index.html"
LOGOS = WORK / "v2_platform_logos.json"

CSS_GRID_OLD = "    .platform-layout { display: grid; grid-template-columns: 15fr 15fr 15fr 15fr 25fr 15fr; gap: 10px; align-items: stretch; grid-auto-flow: row; }"
CSS_GRID_NEW = ("    /* 2026-10-22 (user), one row, seven slots:\n"
                "       BingoPlus 10 | GameZone 10 | ArenaPlus 10 | Platform Share 15 |\n"
                "       Top 5 + 100 Rounds 20 | Changelog 25 | Compliance + Alerts 10. */\n"
                "    .platform-layout { display: grid; grid-template-columns: 10fr 10fr 10fr 15fr 20fr 25fr 10fr; gap: 10px; align-items: stretch; grid-auto-flow: row; }")

CSS_PLACE_OLD = """    .platform-layout > .hl-stack { grid-column: 5; grid-row: 1; }
    .platform-layout > .status-stack { grid-column: 6; grid-row: 1; }"""
CSS_PLACE_NEW = """    .platform-layout > .hl-stack { grid-column: 5; grid-row: 1; }
    .platform-layout > .changelog-table { grid-column: 6; grid-row: 1; }
    .platform-layout > .status-stack { grid-column: 7; grid-row: 1; }"""

CSS_BAND_OLD = "    .bottom-band { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; align-items: stretch; }"
CSS_BAND_NEW = ("    /* Changelog moved back into the platform row (2026-10-22), so the bottom\n"
                "       band is the Analysis panel alone. */\n"
                "    .bottom-band { display: grid; grid-template-columns: 1fr; gap: 10px; align-items: stretch; }")

CSS_HEAD_OLD = """    .plat-head { display: grid; grid-template-columns: minmax(0, 1fr) auto;
                 grid-template-rows: auto auto; gap: 4px 6px; align-items: center; }
    .plat-logo { grid-column: 1; grid-row: 1; display: block; height: 24px; width: auto;
                 max-width: 100%; object-fit: contain; object-position: left center; }
    .plat-chip { grid-column: 2; grid-row: 1; margin-left: 0; }
    .plat-id { grid-column: 1 / -1; grid-row: 2; min-width: 0; }"""
CSS_HEAD_NEW = """    /* 2026-10-22 (user): "ILAGAY SA GITNA YUNG LOGO NG PLATFORM." The logo is
       centred on its own row and the code chip floats top-right out of the flow,
       so a wide logo can no longer push the mark off-centre. */
    .plat-head { position: relative; display: grid; grid-template-columns: minmax(0, 1fr);
                 grid-template-rows: auto auto; gap: 4px; align-items: center;
                 justify-items: center; }
    .plat-logo { grid-column: 1; grid-row: 1; display: block; height: 24px; width: auto;
                 max-width: 100%; object-fit: contain; object-position: center; margin: 0 auto; }
    .plat-chip { position: absolute; top: 0; right: 0; grid-column: auto; grid-row: auto;
                 margin-left: 0; }
    .plat-id { grid-column: 1; grid-row: 2; min-width: 0; width: 100%; text-align: center; }"""


def fix_bp_logo():
    with open(LOGOS, encoding="utf-8") as fh:
        data = json.load(fh)
    src = data.get("bp") or ""
    b64 = src.split("base64,", 1)[1] if "base64," in src else ""
    if not b64:
        print("FAIL-CLOSED: bp logo not a data URI")
        return False
    im = Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGBA")
    box = im.getbbox()
    if not box:
        print("FAIL-CLOSED: bp logo is empty")
        return False
    crop = im.crop(box)
    # Render target is height:24px on a 1x screen; ship 3x for crispness and let the
    # browser downscale. Cropping the transparent margin is what actually fixes the
    # size: the canvas was 50x34 with a 37x17 mark inside, so at height:24 the mark
    # drew 12px tall next to GameZone/ArenaPlus marks that filled their 24px.
    scale = 72.0 / crop.height
    new = crop.resize((max(1, round(crop.width * scale)), 72), Image.LANCZOS)
    buf = io.BytesIO()
    new.save(buf, format="PNG")
    data["bp"] = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    with open(LOGOS, "w", encoding="utf-8") as fh:
        json.dump(data, fh)
    print(f"ok bp logo: crop {im.size}->{crop.size}, shipped {new.size}")
    return True


def cut_panel(html, start_marker):
    """Return (block, html_without_block) for a <div ...> block starting at start_marker."""
    i = html.find(start_marker)
    if i < 0:
        return None, html
    depth = 0
    for m in re.finditer(r"<div\b|</div>", html[i:]):
        if m.group(0).startswith("</"):
            depth -= 1
        else:
            depth += 1
        if depth == 0:
            j = i + m.end()
            return html[i:j], html[:i] + html[j:]
    return None, html


def main():
    src = TPL.read_text(encoding="utf-8") if False else open(TPL, encoding="utf-8", newline="").read()
    if "10fr 10fr 10fr 15fr 20fr 25fr 10fr" in src:
        print("already applied")
        return 3

    # 1. move the changelog panel into the platform row, before the status stack
    block, html = cut_panel(src, '<div class="panel pad changelog-table">')
    if not block:
        print("FAIL-CLOSED: changelog panel not found")
        return 1
    anchor = '<div class="status-stack">'
    if html.count(anchor) != 1:
        print(f"FAIL-CLOSED: status-stack anchor count {html.count(anchor)}")
        return 1
    html = html.replace(anchor, block + "\n          " + anchor)

    # 2. CSS
    problems = []
    for old, new in ((CSS_GRID_OLD, CSS_GRID_NEW), (CSS_PLACE_OLD, CSS_PLACE_NEW),
                     (CSS_BAND_OLD, CSS_BAND_NEW), (CSS_HEAD_OLD, CSS_HEAD_NEW)):
        if html.count(old) != 1:
            problems.append(f"anchor {html.count(old)} (want 1): {old.splitlines()[0][:60]}")
            continue
        html = html.replace(old, new)
    if problems:
        print("FAIL-CLOSED, nothing written:")
        for p in problems:
            print("  !", p)
        return 1

    crlf_b, crlf_a = src.count("\r\n"), html.count("\r\n")
    lf_b, lf_a = src.count("\n") - crlf_b, html.count("\n") - crlf_a
    if (lf_a - lf_b) - (0) > 60 or crlf_a != crlf_b:
        print(f"FAIL-CLOSED: endings moved crlf {crlf_b}->{crlf_a}, lf {lf_b}->{lf_a}")
        return 1
    open(TPL, "w", encoding="utf-8", newline="").write(html)
    print(f"ok index.html: {len(src)} -> {len(html)} chars (crlf {crlf_b}->{crlf_a}, lf {lf_b}->{lf_a})")
    return 0 if fix_bp_logo() else 1


if __name__ == "__main__":
    sys.exit(main())
