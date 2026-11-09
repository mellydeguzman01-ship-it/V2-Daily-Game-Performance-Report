import re, shutil, datetime, sys, os

P = r"C:\Users\L-User\Documents\ChatGPT\Daily Report\V2-Daily-Game-Performance-Report\index.html"
bak = P.replace("index.html", f"_bak_index_before_ppfill_{datetime.datetime.now():%Y%m%d_%H%M%S}.html")
shutil.copyfile(P, bak)
d = open(P, "rb").read()
crlf0 = d.count(b"\r\n")

edits = [
    # 1. donut smaller (user: "liitan mo ng kaunti yung pie chart")
    (b".player-grid > .panel:first-child .donut-wrap svg { width: 100%; max-width: 280px; max-height: 280px; height: auto; }",
     b".player-grid > .panel:first-child .donut-wrap svg { width: 100%; max-width: 196px; max-height: 196px; height: auto; }"),
    # 2. donut block must not re-grow into the leftover height (that void is what she boxed)
    (b".player-grid > .panel:first-child .compact-pie { flex: 1 1 auto; align-content: center; }",
     b".player-grid > .panel:first-child .compact-pie { flex: 0 0 auto; align-content: start; }\r\n"
     b"    .player-grid > .panel:first-child .legend-list { align-content: stretch; grid-auto-rows: minmax(0, 1fr); }\r\n"
     b"    .player-grid > .panel:first-child .legend-list div { justify-content: center; }"),
    # 3. retention rows absorb the card height instead of pooling it above the keynote
    (b".pg-retention .retention-row { padding: 6px 0; }",
     b".pg-retention .retention-row { padding: 7px 0; }"),
    (b".pg-retention .retention-row .spark { height: 20px; margin-top: 3px; }",
     b".pg-retention .retention-row .spark { height: 36px; margin-top: 3px; }"),
]

for old, new in edits:
    n = d.count(old)
    if n != 1:
        print("FAIL count", n, old[:70]); sys.exit(1)
    d = d.replace(old, new)

crlf1 = d.count(b"\r\n")
open(P, "wb").write(d)
print("backup", os.path.basename(bak))
print("crlf", crlf0, "->", crlf1, "bytes", len(d))
