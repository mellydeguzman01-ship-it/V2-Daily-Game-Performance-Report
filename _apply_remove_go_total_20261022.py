#!/usr/bin/env python3
"""2026-10-22 (user, screenshot of Game Overview + TOTAL bar):
    "tanggalin an tong total dito."  -> drop the TOTAL bar under the two Game
    Overview cards (Total GGR / Total Bet Amount / Total Payout).

The bar is builder-owned markup (`_gp_by_game()` writes it between the GP:BYGAME
markers on every run), so the builder AND the template CSS both change; a CSS-only
or markup-only edit reverts at the next daily build. Fail-closed, CRLF/LF safe.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # .../V2-Daily-Game-Performance-Report
TPL = HERE / "index.html"
BUILDER = HERE.parent / "build_v2_dashboard.py"

CSS_OLD = """    .go-total { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); align-items: center;
      gap: 4px 5px; padding: 7px 8px 8px; border: 1px solid var(--line);
      border-radius: 12px; background: var(--panel-2); }
    .go-total-tag { grid-column: 1 / -1; font-size: 7px; font-weight: 800; letter-spacing: .14em;
      color: #0d7a74; padding: 0 0 4px; border-bottom: 1px solid var(--line); }
    html.night .go-total-tag { color: var(--cyan); }
    .go-total-col { min-width: 0; }
    .go-total-col span { display: block; font-size: 7px; font-weight: 800; letter-spacing: 0;
      text-transform: uppercase; color: var(--muted); }
    .go-total-col b { display: block; margin-top: 2px; font-size: 11.5px; font-weight: 800; color: var(--text);
      font-variant-numeric: tabular-nums; }
    .go-total-col b.positive { color: #0e7d45; }
    .go-total-col b.negative { color: #b3122b; }
    html.night .go-total-col b.positive { color: var(--green); }
    html.night .go-total-col b.negative { color: var(--red); }
"""

CSS_NEW = """    /* 2026-10-22 (user): "tanggalin an tong total dito" -- the TOTAL bar under the
       two Game Overview cards is gone, so its rules are gone with it. The cards
       already fill the panel (`.gp-overview > .go-band { flex: 1 1 auto }`). */
"""

PY_TB_OLD = """        tb = ('<div class="go-total"><div class="go-total-tag">TOTAL</div>'
              '<div class="go-total-col"><span>Total GGR</span><b class="'
              + ggr_cls(t_ggr) + '">' + jsmoney(t_ggr) + "</b></div>"
              '<div class="go-total-col"><span>Total Bet Amount</span><b>'
              + jsmoney(t_bet) + "</b></div>"
              '<div class="go-total-col"><span>Total Payout</span><b>'
              + jsmoney(t_pay) + "</b></div></div>")
"""

PY_TB_NEW = """        # 2026-10-22 (user): "tanggalin an tong total dito." The TOTAL bar under the
        # two Game Overview cards is NO LONGER EMITTED. The sums stay derived because
        # the share / note strings below still quote them for the CN dictionary.
"""

PY_BODY_OLD = """        # TOTAL bar ship. The strings are still computed below for the CN dictionary
        # and for anyone reading this code, but they are no longer emitted.
        body = (self.NL
                + "          " + '<div class="go-band">' + bc + lc + "</div>"
                + self.NL + "          " + tb
                + self.NL + "          ")"""

PY_BODY_NEW = """        # TOTAL bar ship (and the bar itself left on 2026-10-22). The strings are
        # still computed below for the CN dictionary and for anyone reading this
        # code, but they are no longer emitted.
        body = (self.NL
                + "          " + '<div class="go-band">' + bc + lc + "</div>"
                + self.NL + "          ")"""


def edit(path, pairs):
    with open(path, encoding="utf-8", newline="") as fh:
        src = fh.read()
    out, problems, lf_expect = src, [], 0
    for old, new in pairs:
        lf_expect += new.count("\n") - old.count("\n")
        n = out.count(old)
        if n != 1:
            problems.append(f"{path.name}: anchor count {n} (want 1): {old.splitlines()[0][:70]!r}")
            continue
        out = out.replace(old, new)
    if problems:
        print("FAIL-CLOSED, nothing written:")
        for p in problems:
            print("  !", p)
        return False
    crlf_b, crlf_a = src.count("\r\n"), out.count("\r\n")
    lf_b, lf_a = src.count("\n") - crlf_b, out.count("\n") - crlf_a
    if crlf_a != crlf_b:
        print(f"FAIL-CLOSED: CRLF changed {crlf_b} -> {crlf_a}")
        return False
    if lf_a - lf_b != lf_expect:
        print(f"FAIL-CLOSED: bare-LF {lf_b} -> {lf_a}, expected +{lf_expect}")
        return False
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(out)
    print(f"ok {path.name}: {len(src)} -> {len(out)} chars "
          f"(crlf {crlf_b}->{crlf_a}, lf {lf_b}->{lf_a})")
    return True


def main():
    src = TPL.read_text(encoding="utf-8")
    if "go-total" not in src:
        print("already applied")
        return 3
    ok = edit(TPL, [(CSS_OLD, CSS_NEW)])
    ok = edit(BUILDER, [(PY_TB_OLD, PY_TB_NEW), (PY_BODY_OLD, PY_BODY_NEW)]) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
