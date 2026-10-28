import subprocess, pathlib

repo = pathlib.Path(r"C:\Users\L-User\Documents\ChatGPT\Daily Report\V2-Daily-Game-Performance-Report")
base = subprocess.run(["git", "show", "HEAD:index.html"], cwd=repo, capture_output=True).stdout.decode("utf-8")
assert "15fr 15fr 15fr 15fr 25fr 15fr" in base, "HEAD is not the six-slot version"

anchor = """    .platform-layout > .status-stack .status { font-size: 7px; padding: 2px 5px; white-space: normal;
      text-align: center; flex: 0 0 auto; max-width: 46%; }"""
assert base.count(anchor) == 1

add = anchor + """

    /* 2026-10-21 (user): Platform Share is now a 15% column, so its rings scale to
       the column (32% of the card, capped at 96px) instead of a fixed 110px that
       pushed the copy out of the card, and the three charts spread over the full
       height so no blank pocket is left at the foot. */
    .platform-layout .platform-charts { align-content: space-between; gap: 2px; }
    .platform-layout .platform-charts .platform-chart { grid-template-columns: minmax(44px, 32%) minmax(0, 1fr);
      gap: 7px; padding: 6px 0; align-items: center; }
    .platform-layout .platform-charts .mini-donut { width: 100%; max-width: 96px; height: auto;
      aspect-ratio: 1 / 1; display: block; }
    .platform-layout .platform-charts .platform-chart > div { min-width: 0; }
    .platform-layout .platform-charts .platform-chart strong { display: block; font-size: 9.5px; }
    .platform-layout .platform-charts .platform-chart small { display: block; font-size: 8px;
      line-height: 1.22; overflow-wrap: anywhere; }
    .platform-layout .platform-charts .share-values { font-size: 8px; gap: 2px; margin-top: 4px; }
    .platform-layout .platform-charts .share-values span { white-space: normal; }"""

out = base.replace(anchor, add)
(repo / "index.html").write_text(out, encoding="utf-8", newline="")
print("written", len(out), "chars; sixcol:", out.count("15fr 15fr 15fr 15fr 25fr 15fr"), "; fivecol:", out.count("repeat(5, minmax(0, 1fr))"))
