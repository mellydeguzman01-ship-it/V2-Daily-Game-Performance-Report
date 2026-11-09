#!/usr/bin/env python3
"""2026-11-06 (Melly), two asks:

1. "tanggalin mo na nga yang pa umbre effect para maidentify ng maayos"
   Game Modes: the 100%-stacked segments were painted with a linear-gradient
   that fades toward the seam (seg-blue ends in #dbe9ff, seg-pink starts at
   #ffe4f1, ...), plus a white sheen sliding over the track. Both wash out the
   boundary, so the Manual/Autoplay and Normal/Turbo split is hard to read at a
   glance. Segments are now ONE flat colour each and the sheen is gone; the seam
   is a hard edge again. Entrance wipe (gm-wipe) is untouched.

2. "yung dyan sa round type distribution, dapat tatlo yan (normal rounds, bonus
   round at buy feature)"
   The panel only had two rows because the 2026-11-05 canonical build zeroed
   feature.bonus_round.rounds and folded those rounds into normal_bet. The raw
   extract still carries them (per-site BP1 1,967 + GP 2,980 + AP 39 = 4,986
   rounds, 1,781 players). They are split back out here, and the three rows are
   rebased on the day's 563,555 settled rounds so they still add to the ROUNDS
   tile:
       Normal  563,555 - 4,986 - 1,188 = 557,381   98.91%
       Bonus                             4,986    0.88%
       Buy Feature                       1,188    0.21%
   Same convention the 2026-11-01..04 builds used (bonus 0.92% on 11-04).
   dash_2026-11-05.json is patched the same way so a rebuild reproduces it.
"""
import json
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
INDEX = HERE / "index.html"
DATA = HERE.parent / "localz" / "dash_2026-11-05.json"

# ---------------------------------------------------------------- 1. ombre ----
OLD_SEGS = """    .gp-modes .mode-track .seg-blue   { background: linear-gradient(90deg, var(--blue) 0%, var(--blue) 58%, #dbe9ff 100%); }
    .gp-modes .mode-track .seg-pink   { background: linear-gradient(90deg, #ffe4f1 0%, var(--pink) 40%, var(--pink) 100%); }
    .gp-modes .mode-track .seg-yellow { background: linear-gradient(90deg, var(--yellow) 0%, var(--yellow) 55%, #fff2d2 100%); }
    .gp-modes .mode-track .seg-orange { background: linear-gradient(90deg, #ffdcbe 0%, var(--orange) 42%, var(--orange) 100%); }
"""

NEW_SEGS = """    /* 2026-11-06 (Melly): "tanggalin mo na nga yang pa umbre effect para
       maidentify ng maayos". Solid fills, one colour per share: the old gradient
       faded each segment toward the seam, so the exact Manual/Autoplay and
       Normal/Turbo boundary disappeared into a wash. The hard edge is back. */
    .gp-modes .mode-track .seg-blue   { background: var(--blue); }
    .gp-modes .mode-track .seg-pink   { background: var(--pink); }
    .gp-modes .mode-track .seg-yellow { background: var(--yellow); }
    .gp-modes .mode-track .seg-orange { background: var(--orange); }
"""

# the sliding white highlight also tinted the colours under it - removed
OLD_SHEEN = """    /* Continuous movement, LENGTH-PRESERVING: a highlight slides along the track and never
       changes a segment's width, so the bar is never briefly showing the wrong split. */
    .gp-modes .mode-track::after {
      content: ""; position: absolute; inset: 0; pointer-events: none;
      background-image: linear-gradient(90deg, transparent, rgba(255,255,255,.45), transparent);
      background-size: 38% 100%; background-repeat: no-repeat;
    }
    .gp-modes.bars-live .mode-track::after { animation: gm-sheen 3.2s linear infinite; }
    .gp-modes.bars-live .mode-row + .mode-row .mode-track::after { animation-delay: .55s; }
"""

NEW_SHEEN = """    /* 2026-11-06 (Melly): the sliding white highlight is GONE - it tinted the
       segment under it, which is exactly what made the colours hard to identify.
       Bars still wipe in on scroll (.bars-live .mode-fill) and nothing moves
       afterwards. */
"""

# ------------------------------------------------- 2. round type, three rows ----
OLD_FEATURE = """            <div class="dynamic-item"><div class="dynamic-head"><b>Normal Round</b><span>562,367 rounds \u00b7 99.79%</span></div><div class="bar-track"><div class="bar-fill" style="width:100%;background:var(--muted)"></div></div><div class="dynamic-foot"><span>99.79% of rounds</span><b>7,150 player entries</b></div></div>
            <div class="dynamic-item"><div class="dynamic-head"><b>Buy Feature</b><span>1,188 rounds \u00b7 0.21%</span></div><div class="bar-track"><div class="bar-fill" style="width:4%;background:var(--yellow)"></div></div><div class="dynamic-foot"><span>0.21% of rounds</span><b>738 player entries</b></div></div>
"""

NEW_FEATURE = """            <div class="dynamic-item"><div class="dynamic-head"><b>Normal Round</b><span>557,381 rounds \u00b7 98.91%</span></div><div class="bar-track"><div class="bar-fill" style="width:100%;background:var(--muted)"></div></div><div class="dynamic-foot"><span>98.91% of rounds</span><b>7,150 player entries</b></div></div>
            <div class="dynamic-item"><div class="dynamic-head"><b>Bonus Round</b><span>4,986 rounds \u00b7 0.88%</span></div><div class="bar-track"><div class="bar-fill" style="width:4%;background:var(--yellow)"></div></div><div class="dynamic-foot"><span>0.88% of rounds</span><b>1,781 player entries</b></div></div>
            <div class="dynamic-item"><div class="dynamic-head"><b>Buy Feature</b><span>1,188 rounds \u00b7 0.21%</span></div><div class="bar-track"><div class="bar-fill" style="width:4%;background:var(--green)"></div></div><div class="dynamic-foot"><span>0.21% of rounds</span><b>738 player entries</b></div></div>
"""

# the analysis sentence quoted the old two-way split (bonus shown as 0)
OLD_EN = ("547,468 settled rounds \u2014 99.79% normal, \u2014% bonus (0), "
          "0.21% buy-feature (1,188).")
NEW_EN = ("563,555 settled rounds (Bingo included) \u2014 98.91% normal (557,381), "
          "0.88% bonus (4,986), 0.21% buy-feature (1,188).")

OLD_CN = ("\u5df2\u7ed3\u7b97 547,468 \u56de\u5408 \u2014\u2014 \u666e\u901a 99.79%\u3001"
          "\u5956\u52b1 \u2014%\uff080 \u56de\u5408\uff09\u3001\u8d2d\u4e70\u529f\u80fd "
          "0.21%\uff081,188 \u56de\u5408\uff09\u3002")
NEW_CN = ("\u5df2\u7ed3\u7b97 563,555 \u56de\u5408\uff08\u542b Bingo\uff09\u2014\u2014 "
          "\u666e\u901a 98.91%\uff08557,381 \u56de\u5408\uff09\u3001\u5956\u52b1 "
          "0.88%\uff084,986 \u56de\u5408\uff09\u3001\u8d2d\u4e70\u529f\u80fd "
          "0.21%\uff081,188 \u56de\u5408\uff09\u3002")


def edit(path: Path, pairs, bak_suffix):
    txt = path.read_text(encoding="utf-8")
    orig = txt
    for old, new in pairs:
        if new and new in txt and old not in txt:
            print("  already applied:", old[:50].replace("\n", " "))
            continue
        if old not in txt:
            print("  !! anchor missing:", old[:60].replace("\n", " "))
            continue
        txt = txt.replace(old, new, 1)
        print("  patched:", old[:48].replace("\n", " "))
    if txt != orig:
        bak = path.with_name(path.stem + f".bak_{bak_suffix}" + path.suffix)
        if not bak.exists():
            shutil.copy2(path, bak)
        path.write_text(txt, encoding="utf-8")
        print("  written:", path.name)


print("index.html")
edit(INDEX, [(OLD_SEGS, NEW_SEGS), (OLD_SHEEN, NEW_SHEEN),
             (OLD_FEATURE, NEW_FEATURE), (OLD_EN, NEW_EN), (OLD_CN, NEW_CN)],
     "ombre3rows_20261106")

print("dash_2026-11-05.json")
d = json.loads(DATA.read_text(encoding="utf-8"))
f = d["feature"]
if f["bonus_round"]["rounds"] == 4986 and f["normal_bet"]["rounds"] == 557381:
    print("  already applied")
else:
    shutil.copy2(DATA, DATA.with_name("dash_2026-11-05.json.bak_bonussplit_20261106"))
    f["normal_bet"]["rounds"] = 557381
    f["bonus_round"]["rounds"] = 4986
    f["buy_feature"]["rounds"] = 1188
    d["panels"]["feature_rate"] = {
        "rounds": 563555,
        "items": [
            {"label": "Normal Round", "rounds": 557381, "rate": "98.91", "players": 7150},
            {"label": "Bonus Round", "rounds": 4986, "rate": "0.88", "players": 1781},
            {"label": "Buy Feature", "rounds": 1188, "rate": "0.21", "players": 738},
        ],
    }
    DATA.write_text(json.dumps(d, indent=1, ensure_ascii=False), encoding="utf-8")
    print("  patched: bonus 4,986 split out; normal 557,381; 3 items")
print("done")
