#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""VIP Player Performance — full-width band, live Local Z turnover data.

Run from the repo root (V2-Daily-Game-Performance-Report):  python apply_vip_band_20261109.py

  1. CSS  : .pp-vip takes its own band (span 20) and the type scale is retuned.
  2. HTML : row 2 below it reflows to Denomination 8 | Engagement 6 | Spend Tier 6.
  3. HTML : the VIP panel body is rebuilt from ../localz/_vip_final.json.
  4. HTML : CN strings for the new labels are added to the __dynCN map.
Idempotent: safe to run twice.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IDX = ROOT / "index.html"
DATA = ROOT.parent / "localz" / "_vip_final.json"

html = IDX.read_text(encoding="utf-8")
orig = html

# ---------------------------------------------------------------- 1. CSS ----
OLD_CSS_HEAD = """/* =====================================================================
       2026-11-09 (Melly) — PLAYER PERFORMANCE, ONE ROW
       VIP Players 30% | Unique Players by Bet Denomination 30% |
       Player Engagement Distribution 20% | Players by Spend Tier 20%
       (20 tracks: 6 + 6 + 4 + 4; row 1 above is untouched at 4+3+4+9).
       ===================================================================== */
    .player-grid > .pp-vip { grid-column: span 6; display: flex; flex-direction: column;
      gap: 10px; min-width: 0; }"""
NEW_CSS_HEAD = """/* =====================================================================
       2026-11-09 (Melly) — PLAYER PERFORMANCE
       Row 1 (untouched): 4 + 3 + 4 + 9.
       VIP Player Performance owns its own band (span 20) because the eight-column
       account table needs the real width; row 2 below is
       Bet Denomination 40% | Engagement 30% | Spend Tier 30%  (8 + 6 + 6).
       ===================================================================== */
    .player-grid > .pp-vip { grid-column: span 20; display: flex; flex-direction: column;
      gap: 9px; min-width: 0; }"""

if OLD_CSS_HEAD in html:
    html = html.replace(OLD_CSS_HEAD, NEW_CSS_HEAD)
elif ".player-grid > .pp-vip { grid-column: span 20;" not in html:
    sys.exit("CSS head not found — inspect index.html before rerunning")

OLD_KPI = """    .pp-vip .vip-kpis { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr));
      gap: 6px; }
    .pp-vip .vip-k { display: flex; flex-direction: column; justify-content: flex-start;
      gap: 3px; padding: 7px 6px; border: 1px solid var(--line); border-radius: 9px;
      background: var(--panel-2); min-width: 0; }
    .pp-vip .vip-k span { font-size: 7.5px; line-height: 1.15; font-weight: 700;
      letter-spacing: .01em; color: var(--muted); text-transform: uppercase; }
    .pp-vip .vip-k b { font-size: 13px; font-weight: 800; line-height: 1.1; color: var(--text);
      font-variant-numeric: tabular-nums; }
    .pp-vip .vip-k small { font-size: 7px; line-height: 1.2; color: var(--muted);
      font-variant-numeric: tabular-nums; }
    .pp-vip .vip-tbl { flex: 1 1 auto; min-height: 0; }
    .pp-vip .vip-tbl table { width: 100%; table-layout: fixed; border-collapse: collapse;
      font-size: 8.5px; }
    .pp-vip .vip-tbl thead th { font-size: 7.5px; font-weight: 800; letter-spacing: .02em;
      text-transform: uppercase; color: var(--muted); text-align: right; padding: 6px 5px;
      border-bottom: 1px solid var(--line); white-space: normal; line-height: 1.2; }"""
NEW_KPI = """    .pp-vip .vip-kpis { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr));
      gap: 10px; }
    .pp-vip .vip-k { display: flex; flex-direction: column; justify-content: flex-start;
      gap: 2px; padding: 7px 10px; border: 1px solid var(--line); border-radius: 9px;
      background: var(--panel-2); min-width: 0; }
    .pp-vip .vip-k span { font-size: 8px; line-height: 1.15; font-weight: 700;
      letter-spacing: .01em; color: var(--muted); text-transform: uppercase;
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .pp-vip .vip-k b { font-size: 16px; font-weight: 800; line-height: 1.1; color: var(--text);
      font-variant-numeric: tabular-nums; }
    .pp-vip .vip-k small { font-size: 7.5px; line-height: 1.2; color: var(--muted);
      font-variant-numeric: tabular-nums; white-space: nowrap; overflow: hidden;
      text-overflow: ellipsis; }
    .pp-vip .vip-tbl { flex: 1 1 auto; min-height: 0; }
    .pp-vip .vip-tbl table { width: 100%; table-layout: fixed; border-collapse: collapse;
      font-size: 10px; }
    .pp-vip .vip-tbl thead th { font-size: 8px; font-weight: 800; letter-spacing: .02em;
      text-transform: uppercase; color: var(--muted); text-align: right; padding: 6px 8px;
      border-bottom: 1px solid var(--line); white-space: nowrap; line-height: 1.2; }"""

if OLD_KPI in html:
    html = html.replace(OLD_KPI, NEW_KPI)
elif "    .pp-vip .vip-tbl table { width: 100%; table-layout: fixed; border-collapse: collapse;\n      font-size: 10px; }" not in html:
    sys.exit("KPI css block not found")

OLD_TD = "    .pp-vip .vip-tbl tbody td { padding: 6px 5px; text-align: right; color: var(--text);"
NEW_TD = "    .pp-vip .vip-tbl tbody td { padding: 5px 8px; text-align: right; color: var(--text);"
if OLD_TD in html:
    html = html.replace(OLD_TD, NEW_TD)

# tag chips for the classification column
if ".pp-vip .vip-tag {" not in html:
    anchor = "    .pp-vip .vip-tbl td.vip-empty {"
    chips = """    .pp-vip .vip-tag { display: inline-block; margin-left: 7px; padding: 1px 6px;
      border-radius: 999px; font-size: 7px; font-weight: 800; letter-spacing: .04em;
      text-transform: uppercase; border: 1px solid currentColor; vertical-align: 1px; }
    .pp-vip .vip-tag.is-vip { color: #ffca64; }
    .pp-vip .vip-tag.is-pot { color: var(--muted); }
"""
    if anchor in html:
        html = html.replace(anchor, chips + anchor, 1)
    else:
        sys.exit("empty-cell CSS anchor not found")

# ------------------------------------------------------- 2. row-2 reflow ----
if 'class="panel pad chart-box pg-6 pg-denom pg-chart"' in html:
    html = html.replace('class="panel pad chart-box pg-6 pg-denom pg-chart"',
                        'class="panel pad chart-box pg-8 pg-denom pg-chart"')
    html = html.replace('class="panel pad pg-4 chart-box pp-engage"',
                        'class="panel pad pg-6 chart-box pp-engage"')
    html = html.replace('class="panel pad pg-4 pp-tiers"',
                        'class="panel pad pg-6 pp-tiers"')

# --------------------------------------------------------- 3. panel body ----
data = json.loads(DATA.read_text(encoding="utf-8"))
win, th, tot, vip = data["window"], data["thresholds"], data["totals"], data["vip"]
pot = data["potential"]
rows = [(r, "is-vip", "VIP") for r in data["vip_rows"]] + \
       [(r, "is-pot", "Potential") for r in data["potential_rows"]]


def money(v):
    return f"₱{v:,.2f}"


def share(a, b):
    v = 100.0 * a / b if b else 0.0
    if abs(v) < 0.01:
        return f"{v:.4f}%"
    return f"{v:.2f}%"


MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
y, m, d = win["report_to"].split("-")
report_lbl = f"{int(d)} {MON[int(m) - 1]} {y}"
subtitle = f"Lifetime to {report_lbl} · turnover ≥ ₱{th['vip']:,}"

cards = [
    ("Total VIP Players", f"{vip['count']:,}", f"+{pot['count']} potential" if pot["count"] else None),
    ("NEW VIPs", f"{vip['new']:,}", None),
    ("Active VIPs", f"{vip['active']:,}", f"active in {MON[int(win['month_from'][5:7]) - 1]}"),
    ("VIP Player Share", share(vip["count"], tot["players"]), f"of {tot['players']:,} accounts"),
    ("VIP Bet Share", share(vip["bet"], tot["bet"]), f"Total bet {money(tot['bet'])}"),
    ("VIP GGR Share", share(vip["ggr"], tot["ggr"]), f"Total GGR {money(tot['ggr'])}"),
]

kpi_html = "\n".join(
    f'            <div class="vip-k"><span>{lb}</span><b>{val}</b>'
    + (f"<small>{s}</small>" if s else "")
    + "</div>"
    for lb, val, s in cards
)

if rows:
    body = "\n".join(
        '              <tr><td>{login}<span class="vip-tag {cls}">{tag}</span></td>'
        "<td>{bet}</td><td>{payout}</td><td>{ggr}</td><td>{rtp}</td><td>{rounds}</td>"
        "<td>{days}</td><td>{plat}</td></tr>".format(
            login=r["login"], cls=cls, tag=tag, bet=money(r["bet"]),
            payout=money(r["payout"]),
            ggr=("-" if r["ggr"] < 0 else "") + money(abs(r["ggr"])),
            rtp=(f"{r['rtp']:.2f}%" if r["rtp"] is not None else "—"),
            rounds=f"{r['rounds']:,}", days=r["active_days"], plat=r["platform"])
        for r, cls, tag in rows)
else:
    body = ('              <tr><td colspan="8" class="vip-empty">'
            f'No account reached ₱{th["vip"]:,} turnover yet</td></tr>')

panel = f"""        <div class="panel pad pp-vip">
          <div class="side-title"><h3>VIP Player Performance</h3><span>{subtitle}</span></div>
          <div class="vip-kpis">
{kpi_html}
          </div>
          <div class="vip-tbl">
            <table>
              <colgroup><col style="width:22%"><col style="width:15%"><col style="width:15%"><col style="width:14%"><col style="width:7%"><col style="width:11%"><col style="width:8%"><col style="width:8%"></colgroup>
              <thead><tr><th>VIP account</th><th>Total Bet Amount</th><th>Total Payout</th><th>Total GGR</th><th>RTP</th><th>Total Rounds</th><th>Active Days</th><th>Platform</th></tr></thead>
              <tbody>
{body}
              </tbody>
            </table>
          </div>
        </div>"""

pat = re.compile(r'        <div class="panel pad pp-vip">.*?\n        </div>\n', re.S)
if not pat.search(html):
    sys.exit("VIP panel block not found")
html = pat.sub(panel + "\n", html, count=1)

# ------------------------------------------------------------- 4. CN map ----
if f'"{subtitle}"' not in html:
    cn_from = '"No VIP accounts — no VIP level in the Local Z source yet": "暂无 VIP 账号 — 数据源尚无 VIP 等级"'
    if cn_from in html:
        cn_to = (cn_from + ",\n"
                 f'        "{subtitle}": "累计至 {y}年{int(m)}月{int(d)}日 · 流水 ≥ ₱{th["vip"]:,}",\n'
                 '        "potential": "潜在", "VIP": "VIP", "Potential": "潜在",\n'
                 f'        "of {tot["players"]:,} accounts": "{tot["players"]:,} 个账号中",\n'
                 f'        "+{pot["count"]} potential": "+{pot["count"]} 个潜在",\n'
                 f'        "active in {MON[int(win["month_from"][5:7]) - 1]}": "本月活跃",\n'
                 '        "No account reached ₱1,000,000 turnover yet": "暂无账号达到 ₱1,000,000 流水"')
        html = html.replace(cn_from, cn_to, 1)
    else:
        print("WARN: CN anchor missing, skipped CN keys")

IDX.write_text(html, encoding="utf-8")
print(f"written: {len(html) - len(orig):+d} chars | VIP rows {len(data['vip_rows'])} "
      f"+ potential {len(data['potential_rows'])}")
print("cards:", [(c[0], c[1]) for c in cards])
