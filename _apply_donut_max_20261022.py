import io, sys

p = r"C:\Users\L-User\Documents\ChatGPT\Daily Report\V2-Daily-Game-Performance-Report\index.html"
with open(p, "rb") as f:
    raw = f.read()

text = raw.decode("utf-8")
lines = text.splitlines(keepends=True)

start = None
for i, ln in enumerate(lines):
    if ".player-grid > .panel:first-child .compact-pie {" in ln and "grid-template-columns: 1fr" in ln:
        start = i
        break
assert start is not None, "start not found"
# The block ends at the legend-list div line
end = None
for j in range(start, start + 15):
    if ".player-grid > .panel:first-child .legend-list div {" in lines[j]:
        end = j
        break
assert end is not None, "end not found"

new = [
    "    .player-grid > .panel:first-child .compact-pie { grid-template-columns: minmax(0, 1fr) 92px; gap: 10px; min-height: 0; }\n",
    "    /* 2026-10-22 (user: \"masyadong maliit yung pie chart dito at ang laki pa ng\n",
    "       unused space, i-maximize mo yung space\"). The card is a 20% track now, not\n",
    "       the old 15% one, so the 126px cap left ~180px of dead width either side of\n",
    "       the ring. The legend moves into that dead width instead of sitting under\n",
    "       the ring: the donut takes the whole remaining column (up to 250px) and\n",
    "       grows with the card. Nothing is added, cut or reworded. */\n",
    "    .player-grid > .panel:first-child .donut-wrap { min-height: 0; min-width: 0; }\n",
    "    .player-grid > .panel:first-child .donut-wrap svg { width: 100%; max-width: 250px; max-height: 250px; height: auto; }\n",
    "    .player-grid > .panel:first-child .donut-center strong { font-size: 30px; }\n",
    "    .player-grid > .panel:first-child .donut-center span { font-size: 11px; }\n",
    "    .player-grid > .panel:first-child .legend-list { min-width: 0; }\n",
    "    .player-grid > .panel:first-child .legend-list div { font-size: 10.5px; gap: 1px; flex-direction: column; align-items: flex-start; line-height: 1.3; }\n",
    "    .player-grid > .panel:first-child .legend-list b { font-size: 12px; white-space: nowrap; }\n",
    "    /* Below ~1500px the 92px legend rail squeezes the ring too far; stack it back\n",
    "       under the donut, which is still well above the old 126px cap. */\n",
    "    @media (max-width: 1500px) {\n",
    "      .player-grid > .panel:first-child .compact-pie { grid-template-columns: 1fr; gap: 6px; }\n",
    "      .player-grid > .panel:first-child .donut-wrap svg { width: min(210px, 100%); }\n",
    "      .player-grid > .panel:first-child .legend-list div { flex-direction: row; align-items: center; justify-content: space-between; }\n",
    "    }\n",
]

# preserve the original line ending style of the block
crlf = lines[start].endswith("\r\n")
if crlf:
    new = [x.replace("\n", "\r\n") for x in new]

out = lines[:start] + new + lines[end + 1:]
data = "".join(out).encode("utf-8")
with open(p, "wb") as f:
    f.write(data)
print("replaced lines", start + 1, "to", end + 1, "crlf", crlf, "bytes", len(raw), "->", len(data))
