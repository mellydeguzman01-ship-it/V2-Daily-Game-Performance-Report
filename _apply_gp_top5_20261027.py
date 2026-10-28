#!/usr/bin/env python3
"""2026-10-27 (Melly): put Top 5 Winning Players inside the Game Performance
section, in the 310px dead band under the Game Performance table.

Adds a `.gp-side` flex wrapper around the table + new card so the column keeps
its current height; the table/keynote stops at content height and the Top 5
card absorbs the leftover. Idempotent: refuses to run twice.
"""
import json
import os
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(HERE, "index.html")
DATA = os.path.join(os.path.dirname(HERE), "localz", "dash_2026-10-26.json")

CSS_OLD = """    .gp-row-1 > .gp-passline { grid-column: 3; grid-row: 1 / span 2; }
    .gp-row-1 > .game-summary { grid-column: 4; grid-row: 1 / span 2; }
"""
CSS_NEW = """    .gp-row-1 > .gp-passline { grid-column: 3; grid-row: 1 / span 2; }
    .gp-row-1 > .gp-side { grid-column: 4; grid-row: 1 / span 2;
      display: flex; flex-direction: column; gap: 10px; min-width: 0; }
    .gp-row-1 > .game-summary { grid-column: 4; grid-row: 1 / span 2; }
"""

TOP5_CSS = """    /* 2026-10-27 (user): "dyan mo ilagay yung top 5 winning players, ilagay mo
       siya sa game performance na section" - the dead band under the Game
       Performance table now carries a compact Top 5. Two lines per player: name
       + payout on line 1, the day's metrics on line 2, so all eight fields stay
       readable in the 20% column instead of squeezing eight columns into 370px. */
    .gp-top5 { display: flex; flex-direction: column; min-height: 0; }
    .gp-top5 .side-title { margin-bottom: 2px; }
    .gp-top5 .side-title h3 { font-size: 12px; }
    .gp-top5 .side-title span { font-size: 8px; }
    .gp-top5-list { flex: 1 1 auto; display: grid; grid-auto-rows: minmax(0, 1fr); margin-top: 2px; }
    .gp-top5-item { display: flex; flex-direction: column; justify-content: center; gap: 2px;
                    padding: 6px 0; border-top: 1px solid var(--line); min-width: 0; }
    .gp-top5-item:first-child { border-top: 0; padding-top: 2px; }
    .gp-top5-top { display: flex; align-items: baseline; gap: 5px; min-width: 0; }
    .gp-rank { flex: 0 0 auto; width: 10px; font-size: 8px; font-weight: 900; color: var(--muted); }
    .gp-site { flex: 0 0 auto; font-size: 6.2px; font-weight: 800; letter-spacing: .02em; color: var(--muted); }
    .gp-player { flex: 1 1 auto; min-width: 0; font-size: 8.4px; font-weight: 800; color: var(--text);
                 white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .gp-pay { flex: 0 0 auto; font-size: 10px; font-weight: 800; color: var(--cyan);
              font-variant-numeric: tabular-nums; }
    .gp-top5-meta { display: flex; flex-wrap: wrap; gap: 0 7px; font-size: 6.4px;
                    line-height: 1.35; color: var(--muted); font-variant-numeric: tabular-nums; }
    .gp-top5-meta b { color: var(--text); font-weight: 800; }
    .gp-top5-meta .positive, .gp-top5-meta .positive b { color: var(--pos-text); }
    .gp-top5-meta .negative, .gp-top5-meta .negative b { color: var(--neg-text); }
    .gp-top5-meta .gp-mult, .gp-top5-meta .gp-mult b { color: var(--cyan); }
    .gp-top5-meta .gp-age { font-weight: 800; letter-spacing: .02em; }
    .gp-top5-meta .gp-age.new { color: var(--pos-text); }
"""

CSS_ANCHOR = "    .gp-overview { min-width: 0; }\n"


def money(v):
    d = Decimal(str(v or 0))
    return "\u20b1" + f"{d:,.2f}"


def signed_money(v):
    d = Decimal(str(v or 0))
    sign = "+" if d >= 0 else "-"
    return sign + "\u20b1" + f"{abs(d):,.2f}"


def num1(v):
    return f"{float(v):,.1f}"


def num(v):
    d = Decimal(str(v or 0))
    return f"{d:,.0f}" if d == d.to_integral_value() else f"{d.normalize():f}"


def mult(v):
    d = Decimal(str(v or 0))
    core = f"{d:,.0f}" if d == d.to_integral_value() else f"{d.normalize():f}".rstrip("0").rstrip(".")
    return core + "\u00d7"


def build_card(players):
    rows = []
    for i, p in enumerate(players[:5], 1):
        head = str(p.get("player") or "").replace("BP1_", "")
        site = p.get("site") or "\u2014"
        day_bet = Decimal(str(p.get("day_bet") or 0))
        day_pay = Decimal(str(p.get("day_payout") or 0))
        day_ggr = day_bet - day_pay
        ggr_cls = "positive" if day_ggr >= 0 else "negative"
        age = "NEW" if p.get("is_new") is True else ("RET" if p.get("is_new") is False else "\u2014")
        age_cls = " new" if p.get("is_new") is True else ""
        first_day = p.get("first_day") or "\u2014"
        tip = (f"{site} \u00b7 best round {money(p.get('payout'))} at {mult(p.get('mult'))} \u00b7 "
               f"first day {first_day}")
        rows.append(
            f'            <div class="gp-top5-item" title="{tip}">'
            f'<div class="gp-top5-top"><span class="gp-rank">{i}</span>'
            f'<span class="gp-site">{site}</span>'
            f'<b class="gp-player" title="{head}">{head}</b>'
            f'<b class="gp-pay">{money(day_pay)}</b></div>'
            f'<div class="gp-top5-meta"><span>BET <b>{money(day_bet)}</b></span>'
            f'<span class="{ggr_cls}">GGR <b>{signed_money(day_ggr)}</b></span>'
            f'<span>RTP <b>{num1(p.get("day_rtp"))}%</b></span>'
            f'<span><b>{num(p.get("day_rounds"))}</b> rounds</span>'
            f'<span class="gp-mult">{mult(p.get("day_max_mult") or p.get("mult"))}</span>'
            f'<span class="gp-age{age_cls}">{age}</span></div></div>'
        )
    return (
        '          <div class="panel pad gp-top5">\n'
        '          <div class="side-title"><h3>Top 5 Winning Players</h3>'
        '<span>Biggest single-bet payout</span></div>\n'
        '          <!--GP:TOP5:START-->\n'
        '          <div class="gp-top5-list">\n'
        + "\n".join(rows) + "\n"
        '          </div>\n'
        '          <!--GP:TOP5:END-->\n'
        '          </div>'
    )


def main():
    html = open(INDEX, encoding="utf-8", newline="").read()
    if "gp-top5-list" in html:
        raise SystemExit("already applied - refusing to double-wrap")

    assert CSS_OLD in html, "gp-row-1 CSS anchor missing"
    html = html.replace(CSS_OLD, CSS_NEW, 1)
    assert CSS_ANCHOR in html, "gp-overview CSS anchor missing"
    html = html.replace(CSS_ANCHOR, TOP5_CSS + CSS_ANCHOR, 1)

    start = html.index('          <div class="panel table-scroll game-summary">')
    end_marker = '  </div>\n        </div>\n        <div class="gp-row-2">'
    end = html.index(end_marker, start)
    table_block = html[start:end + len('  </div>')]

    players = json.load(open(DATA, encoding="utf-8"))["incidents"]["top_players"]
    card = build_card(players)
    wrapped = ('          <div class="gp-side">\n'
               + table_block + "\n"
               + card + "\n"
               + '          </div>')
    html = html[:start] + wrapped + html[end + len('  </div>'):]
    open(INDEX, "w", encoding="utf-8", newline="").write(html)
    print("applied: GP side wrapper + top5 card")


if __name__ == "__main__":
    main()
