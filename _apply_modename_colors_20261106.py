#!/usr/bin/env python3
"""2026-11-06 (Melly): "yung color ng text ng sa game dapat iba ibang color din
para mabilis maidentify".

Game Modes panel: each game's NAME text gets that game's own accent so the four
blocks are identifiable at a glance. Palette is the SAME one already used by the
Game Overview cards (go-a..go-d), so the legend stays consistent:
  Banana Craze -> green   (#0e7d45 light / #55d68b night)
  Lucky Color  -> purple  (#6b3fbf light / #b78cff night)
  Blazing 7S   -> orange  (#c2571a light / #ff9f45 night)
  Ginto Match  -> yellow  (#8a6a00 light / #ffca64 night)
Light values are dark enough to clear 4.5:1 on the white panel.

Also patches build_v2_dashboard.py so tonight's regeneration keeps the classes.
"""
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INDEX = HERE / "index.html"
BUILDER = HERE.parent / "build_v2_dashboard.py"

SLUG = {
    "Banana Craze": "mg-banana",
    "Lucky Color": "mg-lucky",
    "Blazing 7S": "mg-blazing",
    "Blazing 7's": "mg-blazing",
    "Ginto Match": "mg-ginto",
}

CSS_ANCHOR = """    .gp-modes .mode-game-name { font-size: 10.5px; font-weight: 800; color: var(--text);
                                letter-spacing: .1px; margin-bottom: 6px; }
"""

CSS_NEW = """    /* 2026-11-06 (Melly): "yung color ng text ng sa game dapat iba ibang color
       din para mabilis maidentify". Every game name carries that game's own
       accent, so the four blocks read by colour instead of by position. The
       palette is the one the Game Overview cards already use (go-a..go-d):
       Banana green, Lucky purple, Blazing orange, Ginto yellow - light values
       are dark enough to clear 4.5:1 on the white panel, night values are the
       bright twins. --gm-acc is the only thing that changes per game; the base
       rule above falls back to --text when no slug is present. */
    .gp-modes .mode-game.mg-banana  { --gm-acc: #0e7d45; }
    .gp-modes .mode-game.mg-lucky   { --gm-acc: #6b3fbf; }
    .gp-modes .mode-game.mg-blazing { --gm-acc: #c2571a; }
    .gp-modes .mode-game.mg-ginto   { --gm-acc: #8a6a00; }
    html.night .gp-modes .mode-game.mg-banana  { --gm-acc: #55d68b; }
    html.night .gp-modes .mode-game.mg-lucky   { --gm-acc: #b78cff; }
    html.night .gp-modes .mode-game.mg-blazing { --gm-acc: #ff9f45; }
    html.night .gp-modes .mode-game.mg-ginto   { --gm-acc: #ffca64; }
    .gp-modes .mode-game-name { color: var(--gm-acc, var(--text)); }
"""


def main():
    html = INDEX.read_text(encoding="utf-8")
    orig = html

    # 1. CSS: insert the per-game accent block right after the base name rule.
    if "mg-banana" in html:
        print("CSS already applied")
    else:
        if CSS_ANCHOR not in html:
            sys.exit("CSS anchor not found")
        html = html.replace(CSS_ANCHOR, CSS_ANCHOR + CSS_NEW, 1)

    # 2. Markup: add the slug class to every mode-game block inside GP:MODES.
    def add_slug(m):
        name = m.group(1)
        slug = SLUG.get(name)
        if not slug:
            return m.group(0)
        return ('<div class="mode-game ' + slug
                + '"><div class="mode-game-name">' + name + "</div>")

    pat = re.compile(r'<div class="mode-game"><div class="mode-game-name">([^<]+)</div>')
    html, n = pat.subn(add_slug, html)
    print("markup blocks tagged:", n)

    if html != orig:
        bak = HERE / "_bak_index_before_modenamecolor_20261106.html"
        if not bak.exists():
            shutil.copy2(INDEX, bak)
        INDEX.write_text(html, encoding="utf-8")
        print("index.html written")
    else:
        print("index.html unchanged")

    # 3. Builder: emit the slug so regeneration keeps it.
    if BUILDER.exists():
        b = BUILDER.read_text(encoding="utf-8")
        old = ("                gblocks.append('<div class=\"mode-game\">"
               "<div class=\"mode-game-name\">' + gname")
        if "mg-banana" in b:
            print("builder already patched")
        elif old in b:
            new = ("                gblocks.append('<div class=\"mode-game"
                   " ' + MG_SLUG.get(gname, \"\") + '\">"
                   "<div class=\"mode-game-name\">' + gname")
            b = b.replace(old, new, 1)
            anchor = "            order = (\"Banana Craze\", \"Ginto Match\", \"Lucky Color\", \"Blazing 7S\")\n"
            decl = ('            # 2026-11-06 (Melly): per-game accent class on the name row\n'
                    '            # (mg-banana/lucky/blazing/ginto) - same palette as the\n'
                    '            # Game Overview cards, so the blocks read by colour.\n'
                    '            MG_SLUG = {"Banana Craze": "mg-banana", "Ginto Match": "mg-ginto",\n'
                    '                       "Lucky Color": "mg-lucky", "Blazing 7S": "mg-blazing",\n'
                    '                       "Blazing 7\'s": "mg-blazing"}\n')
            if anchor in b:
                b = b.replace(anchor, anchor + decl, 1)
            else:
                sys.exit("builder anchor not found")
            BUILDER.write_text(b, encoding="utf-8")
            print("builder patched")
        else:
            sys.exit("builder target not found")


if __name__ == "__main__":
    main()
