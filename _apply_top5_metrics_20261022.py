#!/usr/bin/env python3
"""2026-10-22 (user, red box on the Top 5 panel): "ang laki ng space, magdagdag ka
pa ng metrics. idagdag mo yung bet amount, payout, ggr, rtp, rounds, multi, new or
old player."

One row per player, eight columns, all from the player's own day totals:
    PLAYER (site chip + short login) | BET | PAYOUT | GGR | RTP | ROUNDS | MULT | NEW/RET
The ranking round's own payout/multiplier, the stake range, IP and first day move
into the row title so nothing is lost.

Touches: builder markup (`_pp_top5`), template CSS, and the extraction
(`bp1_dashboard_data.top_players` gains first_day/is_new so future days carry the
NEW-vs-RETURNING flag). Fail-closed, line-ending safe.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TPL = HERE / "index.html"
BUILDER = HERE.parent / "build_v2_dashboard.py"
DATA = HERE.parent / "bp1_dashboard_data.py"

CSS_OLD = """    .pp-top5 .top5-head-row,
    .pp-top5 .top5-item { display: grid; align-items: center; min-width: 0;
                          grid-template-columns: minmax(0, 1fr) 52px 42px 34px 26px;
                          column-gap: 6px; }"""

CSS_NEW = """    /* 2026-10-22 (user): "ang laki ng space, magdagdag ka pa ng metrics ...
       bet amount, payout, ggr, rtp, rounds, multi, new or old player." Eight
       columns, one row per player; the wide name column that used to eat the
       middle of the panel now holds the day's numbers. */
    .pp-top5 .top5-head-row,
    .pp-top5 .top5-item { display: grid; align-items: center; min-width: 0;
                          grid-template-columns: minmax(0, 1fr) 32px 33px 31px 31px 25px 23px 21px;
                          column-gap: 3px; }"""

CSS_VALS_OLD = """    .pp-top5 .top5-pay, .pp-top5 .top5-rtp, .pp-top5 .top5-rnd, .pp-top5 .top5-mult {
      font-size: 8px; font-weight: 800; text-align: right; white-space: nowrap;
      font-variant-numeric: tabular-nums; color: var(--text); }
    .pp-top5 .top5-pay { color: var(--cyan); }
    .pp-top5 .top5-rtp { font-weight: 700; }
    .pp-top5 .top5-rnd { color: var(--muted); font-weight: 700; }
    .pp-top5 .top5-mult { font-size: 7.5px; color: var(--cyan); }"""

CSS_VALS_NEW = """    .pp-top5 .top5-bet, .pp-top5 .top5-pay, .pp-top5 .top5-ggr,
    .pp-top5 .top5-rtp, .pp-top5 .top5-rnd, .pp-top5 .top5-mult, .pp-top5 .top5-age {
      font-size: 7.5px; font-weight: 800; text-align: right; white-space: nowrap;
      font-variant-numeric: tabular-nums; color: var(--text); }
    .pp-top5 .top5-bet { color: var(--muted); font-weight: 700; }
    .pp-top5 .top5-pay { color: var(--cyan); }
    .pp-top5 .top5-ggr.positive { color: #0e7d45; }
    .pp-top5 .top5-ggr.negative { color: #b3122b; }
    html.night .pp-top5 .top5-ggr.positive { color: var(--green); }
    html.night .pp-top5 .top5-ggr.negative { color: var(--red); }
    .pp-top5 .top5-rtp { font-weight: 700; }
    .pp-top5 .top5-rnd { color: var(--muted); font-weight: 700; }
    .pp-top5 .top5-mult { color: var(--cyan); }
    .pp-top5 .top5-age { font-size: 6.5px; color: var(--muted); letter-spacing: .02em; }
    .pp-top5 .top5-age.new { color: #0e7d45; }
    html.night .pp-top5 .top5-age.new { color: var(--green); }"""

PY_HELPERS_OLD = """    @staticmethod
    def _alert_row(head, sub, cls, badge, tight=False, live=False) -> str:"""

PY_HELPERS_NEW = """    @staticmethod
    def _pes_k(v) -> str:
        \"\"\"Space-constrained day totals: \\u20b1108.2k / \\u20b1980 / \\u20b1-18.7k.\"\"\"
        d = D(v or 0)
        sign = "-" if d < 0 else ""
        a = abs(d)
        if a >= 1000:
            return "\\u20b1" + sign + f"{a / 1000:.1f}k"
        return "\\u20b1" + sign + f"{a:,.0f}"

    @staticmethod
    def _short_login(name) -> str:
        \"\"\"Cut the leaderboard login to its distinguishing tail: the site chip
        already says BP1/GP/AP, so 'bingoplus' is 9 wasted characters in a 60px
        column. Anything without that prefix renders untouched.\"\"\"
        s = str(name or "")
        if "_" in s:
            s = s.split("_", 1)[1]
        if s.lower().startswith("bingoplus") and len(s) > 9:
            return s[9:]
        return s

    @staticmethod
    def _alert_row(head, sub, cls, badge, tight=False, live=False) -> str:"""

PY_ROWS_OLD = """            # 2026-10-22 (user): "isang row dapat lahat ng details kada players."
            # One row per player: site + name, payout, RTP, rounds, multiplier.
            # Stake range and IP ride along in the row's title so nothing is lost.
            rows.append(
                f'<div class="top5-item" title="{site} \\u00b7 {rng} \\u00b7 IP {ip}">'
                f'<div class="top5-name"><span class="top5-site">{site}</span>'
                f'<b class="top5-player" title="{head}">{head}</b></div>'
                f'<b class="top5-pay">{pay}</b>'
                f'<span class="top5-rtp">{rtp_txt}</span>'
                f'<span class="top5-rnd">{rnd_txt}</span>'
                f'<span class="top5-mult">{self._mult_txt(p.get("mult"))}</span>'
                '</div>')"""

PY_ROWS_NEW = """            # 2026-10-22 (user): "ang laki ng space, magdagdag ka pa ng metrics.
            # idagdag mo yung bet amount, payout, ggr, rtp, rounds, multi, new or
            # old player." One row per player, day totals: bet / payout / GGR
            # (bet - payout) / RTP / rounds, plus the day's best multiplier and
            # NEW-vs-RETURNING. The ranking round's payout + multiplier, the stake
            # range, the IP and the first-seen day ride in the row title.
            day_bet = D(p.get("day_bet") or 0)
            day_pay = D(p.get("day_payout") or 0)
            day_ggr = day_bet - day_pay
            if p.get("is_new") is True:
                age_txt, age_cls = "NEW", " new"
            elif p.get("is_new") is False:
                age_txt, age_cls = "RET", ""
            else:
                age_txt, age_cls = "\\u2014", ""
            best = (f"best round {pay} at {self._mult_txt(p.get('mult'))}")
            tip = (f"{site} \\u00b7 {best} \\u00b7 range {rng} \\u00b7 "
                   f"first day {p.get('first_day') or '\\u2014'} \\u00b7 IP {ip}")
            rows.append(
                f'<div class="top5-item" title="{tip}">'
                f'<div class="top5-name"><span class="top5-site">{site}</span>'
                f'<b class="top5-player" title="{head}">{self._short_login(head)}</b></div>'
                f'<b class="top5-bet">{self._pes_k(day_bet)}</b>'
                f'<b class="top5-pay">{self._pes_k(day_pay)}</b>'
                f'<b class="top5-ggr{" positive" if day_ggr >= 0 else " negative"}">'
                f'{self._pes_k(day_ggr)}</b>'
                f'<span class="top5-rtp">{rtp_txt}</span>'
                f'<span class="top5-rnd">{rnd_txt}</span>'
                f'<span class="top5-mult">'
                f'{self._mult_txt(p.get("day_max_mult") or p.get("mult"))}</span>'
                f'<span class="top5-age{age_cls}">{age_txt}</span>'
                '</div>')"""

PY_RTP_OLD = """            rtp_txt = f"{num(rtp, 2)}%" if rtp not in (None, "") else "\\u2014\""""
PY_RTP_NEW = """            rtp_txt = f"{num(rtp, 1)}%" if rtp not in (None, "") else "\\u2014\""""

PY_HEAD_OLD = """                '<div class="top5-head-row"><span></span><span>Payout</span>'
                '<span>RTP</span><span>Rounds</span><span>Mult.</span></div>'"""
PY_HEAD_NEW = """                '<div class="top5-head-row"><span></span><span>Bet</span>'
                '<span>Payout</span><span>GGR</span><span>RTP</span>'
                '<span>Rounds</span><span>Mult.</span><span>New</span></div>'"""

DATA_OLD = '    out = []\n    for name, site, bet, pay, mult, ts in rows:\n        agg = a.execute('
DATA_NEW = (
    '    out = []\n'
    '    for name, site, bet, pay, mult, ts in rows:\n'
    '        # 2026-10-22 (user): "new or old player" on the Top 5 row. Same\n'
    "        # definition as the page's TRUE-NEW count: first-ever day in the archive.\n"
    '        first_day = a.execute(\n'
    '            "select min(day) from orders_flat where login_name=?", (name,)).fetchone()\n'
    '        first_day = first_day[0] if first_day else None\n'
    '        agg = a.execute('
)

DATA_ROW_OLD = """            "day_rtp": (str(pct(D(agg[2]), D(agg[1]))) if agg and agg[1] else None),
        })"""
DATA_ROW_NEW = """            "day_rtp": (str(pct(D(agg[2]), D(agg[1]))) if agg and agg[1] else None),
            "first_day": first_day,
            "is_new": (first_day == day) if first_day else None,
        })"""


def edit(path, pairs):
    with open(path, encoding="utf-8", newline="") as fh:
        src = fh.read()
    out, problems, lf_expect = src, [], 0
    crlf_file = src.count("\r\n") > 0
    for old, new in pairs:
        if crlf_file and "\r\n" not in old and out.count(old) == 0:
            old = old.replace("\n", "\r\n")
            new = new.replace("\n", "\r\n")
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
    print(f"ok {path.name}: {len(src)} -> {len(out)} chars (crlf {crlf_b}->{crlf_a}, lf {lf_b}->{lf_a})")
    return True


def main():
    src = TPL.read_text(encoding="utf-8")
    if "top5-bet" in src:
        print("already applied")
        return 3
    ok = edit(TPL, [(CSS_OLD, CSS_NEW), (CSS_VALS_OLD, CSS_VALS_NEW)])
    ok = edit(BUILDER, [(PY_HELPERS_OLD, PY_HELPERS_NEW), (PY_ROWS_OLD, PY_ROWS_NEW),
                        (PY_RTP_OLD, PY_RTP_NEW), (PY_HEAD_OLD, PY_HEAD_NEW)]) and ok
    ok = edit(DATA, [(DATA_OLD, DATA_NEW), (DATA_ROW_OLD, DATA_ROW_NEW)]) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
