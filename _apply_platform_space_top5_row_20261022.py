#!/usr/bin/env python3
"""2026-10-22 (user, Tagalog):
  (1) "masyadong maraming spaces sa mga platforms, dapat alisin yan."
      -> the platform metric grid stops parking leftover height as blank bands
         between rows; rows become equal-height table rows with continuous rules.
  (2) "yung sa top 5 winning players, isang row dapat lahat ng details kada players."
      -> each player is ONE row (site + name | payout | RTP | rounds | mult) with a
         single caption row above, instead of a 3-line stacked block.

Edits BOTH the template CSS (index.html) and the generator that owns the Top 5
markup (build_v2_dashboard.py), because the generator re-writes that block on every
daily rebuild. Fail-closed: every anchor must appear exactly once and CRLF must be
preserved, or nothing is written.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TPL = HERE / "index.html"
BUILDER = HERE.parent / "build_v2_dashboard.py"

CSS_PLAT_OLD = """    .plat-metrics { display: grid; grid-template-columns: 1fr 1fr; gap: 0 7px; flex: 1 1 auto;
                    align-content: space-between; }
    .plat-m { min-width: 0; padding: 3px 0; border-top: 1px solid var(--line); }
    .plat-m span { display: block; font-size: 6.5px; font-weight: 700; letter-spacing: .02em;
                   text-transform: uppercase; color: var(--muted); white-space: nowrap;
                   overflow: hidden; text-overflow: ellipsis; }
    .plat-m b { display: block; font-size: 8.5px; font-weight: 800; color: var(--text);
                white-space: nowrap; font-variant-numeric: tabular-nums; }"""

CSS_PLAT_NEW = """    /* 2026-10-22 (user): "masyadong maraming spaces sa mga platforms, dapat alisin
       yan." align-content:space-between parked the card's leftover height as a
       ~27px blank band between every metric row, which is what read as "daming
       spaces". The grid is a table now: seven equal 1fr rows, one continuous
       hairline per row, label over value centred inside its own row. The card
       reads edge to edge - no blank bands, nothing floating. */
    .plat-metrics { display: grid; grid-template-columns: 1fr 1fr; gap: 0 8px; flex: 1 1 auto;
                    align-content: stretch; grid-auto-rows: minmax(0, 1fr); }
    .plat-m { min-width: 0; padding: 2px 0; border-top: 1px solid var(--line);
              display: flex; flex-direction: column; justify-content: center; min-height: 0; }
    .plat-m span { display: block; font-size: 6.8px; font-weight: 700; letter-spacing: .02em;
                   text-transform: uppercase; color: var(--muted); white-space: nowrap;
                   overflow: hidden; text-overflow: ellipsis; }
    .plat-m b { display: block; font-size: 9.5px; font-weight: 800; color: var(--text);
                white-space: nowrap; font-variant-numeric: tabular-nums; }"""

CSS_TOP5_OLD = """    .pp-top5 tbody td:first-child { font-weight: 700; }
    /* 2026-10-21 (user): five equal 20% columns. The Top 5 panel is ~300px wide
       and an 8-column table broke words mid-word there, so each player is one
       stacked block: name + multiplier, then Payout / RTP / Rounds, then site,
       stake range and IP. All eight fields survive, nothing wraps mid-word. */
    .pp-top5 .top5-list { display: grid; align-content: start; min-width: 0; }
    .pp-top5 .top5-item { padding: 5px 0; border-top: 1px solid var(--line); min-width: 0; }
    .pp-top5 .top5-item:first-child { border-top: 0; padding-top: 1px; }
    .pp-top5 .top5-head { display: flex; align-items: baseline; gap: 6px; min-width: 0; }
    .pp-top5 .top5-player { flex: 1 1 auto; min-width: 0; font-size: 8.5px; font-weight: 800;
                            color: var(--text); white-space: nowrap; overflow: hidden;
                            text-overflow: ellipsis; }
    .pp-top5 .top5-mult { flex: 0 0 auto; font-size: 7.5px; font-weight: 800; color: var(--cyan);
                          font-variant-numeric: tabular-nums; }
    .pp-top5 .top5-vals { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr));
                          gap: 0 6px; margin-top: 3px; }
    .pp-top5 .top5-vals div { min-width: 0; }
    .pp-top5 .top5-vals span { display: block; font-size: 6px; font-weight: 700; letter-spacing: .03em;
                               text-transform: uppercase; color: var(--muted); white-space: nowrap; }
    .pp-top5 .top5-vals b { display: block; font-size: 8px; font-weight: 800; color: var(--text);
                            white-space: nowrap; font-variant-numeric: tabular-nums; }
    .pp-top5 .top5-meta { display: flex; gap: 6px; margin-top: 2px; font-size: 6.5px;
                          color: var(--muted); min-width: 0; }
    .pp-top5 .top5-meta span { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .pp-top5 .top5-site { flex: 0 0 auto; font-weight: 800; color: var(--text); }
    .pp-top5 .top5-ip { margin-left: auto; flex: 0 0 auto; }"""

CSS_TOP5_NEW = """    .pp-top5 tbody td:first-child { font-weight: 700; }
    /* 2026-10-22 (user): "yung sa top 5 winning players, isang row dapat lahat ng
       details kada players." Each player is ONE row now - site + name, payout,
       RTP, rounds, multiplier - instead of a three-line stacked block, with the
       column captions printed once above the list. Site / stake range / IP move
       into the row's title tooltip so no field is lost. */
    .pp-top5 .top5-list { display: grid; align-content: start; min-width: 0; }
    .pp-top5 .top5-head-row,
    .pp-top5 .top5-item { display: grid; align-items: center; min-width: 0;
                          grid-template-columns: minmax(0, 1fr) 52px 42px 34px 26px;
                          column-gap: 6px; }
    .pp-top5 .top5-head-row { padding: 0 0 4px; }
    .pp-top5 .top5-head-row span { font-size: 6px; font-weight: 700; letter-spacing: .04em;
                                   text-transform: uppercase; color: var(--muted);
                                   white-space: nowrap; overflow: hidden; }
    .pp-top5 .top5-head-row span:not(:first-child) { text-align: right; }
    .pp-top5 .top5-item { padding: 7px 0; border-top: 1px solid var(--line); }
    .pp-top5 .top5-item:first-child { border-top: 0; padding-top: 2px; }
    .pp-top5 .top5-name { display: flex; align-items: baseline; gap: 4px; min-width: 0; }
    .pp-top5 .top5-site { flex: 0 0 auto; font-size: 6.2px; font-weight: 800; color: var(--muted);
                          letter-spacing: .02em; }
    .pp-top5 .top5-player { flex: 1 1 auto; min-width: 0; font-size: 8.5px; font-weight: 800;
                            color: var(--text); white-space: nowrap; overflow: hidden;
                            text-overflow: ellipsis; }
    .pp-top5 .top5-pay, .pp-top5 .top5-rtp, .pp-top5 .top5-rnd, .pp-top5 .top5-mult {
      font-size: 8px; font-weight: 800; text-align: right; white-space: nowrap;
      font-variant-numeric: tabular-nums; color: var(--text); }
    .pp-top5 .top5-pay { color: var(--cyan); }
    .pp-top5 .top5-rtp { font-weight: 700; }
    .pp-top5 .top5-rnd { color: var(--muted); font-weight: 700; }
    .pp-top5 .top5-mult { font-size: 7.5px; color: var(--cyan); }"""

PY_OLD = """            rows.append(
                '<div class="top5-item"><div class="top5-head">'
                f'<b class="top5-player" title="{head}">{head}</b>'
                f'<span class="top5-mult">{self._mult_txt(p.get("mult"))}</span></div>'
                '<div class="top5-vals">'
                f'<div><span>Payout</span><b>{pay}</b></div>'
                f'<div><span>RTP</span><b>{rtp_txt}</b></div>'
                f'<div><span>Rounds</span><b>{rnd_txt}</b></div>'
                '</div>'
                f'<div class="top5-meta"><span class="top5-site">{site}</span>'
                f'<span class="top5-range">{rng}</span>'
                f'<span class="top5-ip">IP {ip}</span></div></div>')"""

PY_NEW = """            # 2026-10-22 (user): "isang row dapat lahat ng details kada players."
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

PY_BODY_OLD = """        body = (self.NL + "          "
                '<div class="top5-list">' + "".join(rows) + '</div>'
                + self.NL + "          ")"""

PY_BODY_NEW = """        body = (self.NL + "          "
                '<div class="top5-head-row"><span></span><span>Payout</span>'
                '<span>RTP</span><span>Rounds</span><span>Mult.</span></div>'
                + self.NL + "          "
                '<div class="top5-list">' + "".join(rows) + '</div>'
                + self.NL + "          ")"""


def edit(path, pairs, expect_crlf):
    with open(path, encoding="utf-8", newline="") as fh:
        src = fh.read()
    problems = []
    out = src
    lf_expect = 0
    for old, new in pairs:
        lf_expect += new.count("\n") - old.count("\n")
        n = out.count(old)
        if n != 1:
            problems.append(f"{path.name}: anchor count {n} (want 1) for {old.splitlines()[0][:70]!r}")
            continue
        out = out.replace(old, new)
    if problems:
        print("FAIL-CLOSED, nothing written:")
        for p in problems:
            print("  !", p)
        return False
    crlf_before, crlf_after = src.count("\r\n"), out.count("\r\n")
    lf_before = src.count("\n") - crlf_before
    lf_after = out.count("\n") - crlf_after
    if lf_after - lf_before != lf_expect:
        print(f"FAIL-CLOSED: bare-LF moved {lf_before} -> {lf_after}, expected +{lf_expect}")
        return False
    if crlf_after != crlf_before:
        print(f"FAIL-CLOSED: CRLF count changed {crlf_before} -> {crlf_after}")
        return False
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(out)
    print(f"ok {path.name}: {len(src)} -> {len(out)} bytes "
          f"(crlf {crlf_before}->{crlf_after}, bare-lf {lf_before}->{lf_after})")
    return True


def main():
    tpl_src = TPL.read_text(encoding="utf-8")
    if "top5-head-row" in tpl_src and "align-content: stretch; grid-auto-rows" in tpl_src:
        print("already applied")
        return 3
    ok = edit(TPL, [(CSS_PLAT_OLD, CSS_PLAT_NEW), (CSS_TOP5_OLD, CSS_TOP5_NEW)], True)
    ok = edit(BUILDER, [(PY_OLD, PY_NEW), (PY_BODY_OLD, PY_BODY_NEW)], False) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
