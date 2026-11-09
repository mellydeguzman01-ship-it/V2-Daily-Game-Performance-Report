#!/usr/bin/env python
"""Apply REPORT DATE style 04 (typewriter + caret) to the canonical V2 dashboard.

Byte-level edit: the file is all-CRLF (4125 lines) and `patch`/text-mode reads
would rewrite every line ending.
"""
import shutil, sys, os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
shutil.copyfile(P, P.replace("index.html", "_bak_index_20261106_pre_datetypewriter.html"))

raw = open(P, "rb").read()
crlf_before = raw.count(b"\r\n")
s = raw.decode("utf-8")

OLD_CSS = (
    "    .report-date { display: flex; gap: 8px; align-items: baseline; margin-top: 10px; color: var(--text); font-size: 13px; font-weight: 700; }\r\n"
    "    .report-date span { color: var(--muted); font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; }\r\n"
)

NEW_CSS = """    /* 2026-11-06 (Melly): "REPORT DATE" badge -- style 04 of the ten samples she picked:
       label chip + the date typing itself out behind a blinking caret, then it re-types.
       The reveal runs in JS (the rdTypewriter block at the end of the document) because renderReportDate()
       rewrites this text on EN/CN and archive-date changes, and a fixed steps(27) CSS
       reveal clipped longer dates. Light is the default theme; html.night carries the
       bright set. */
    .report-date { display: flex; gap: 10px; align-items: center; margin-top: 11px; color: var(--text); font-size: 13px; font-weight: 700; }
    .rd-chip { display: inline-flex; align-items: center; gap: 10px; padding: 6px 13px 6px 11px; border-radius: 999px;
      background: linear-gradient(180deg, #f4f9ff, #e8f1fc); border: 1px solid #a6c1df;
      box-shadow: 0 2px 8px rgba(38, 62, 88, .07), inset 0 1px 0 rgba(255, 255, 255, .9); }
    .report-date .rd-label { color: #2d527b; font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: .18em; white-space: nowrap; }
    .rd-type { position: relative; display: inline-flex; align-items: center; }
    .rd-ghost { position: absolute; left: 0; top: 0; visibility: hidden; pointer-events: none; white-space: nowrap;
      font-size: 15px; font-weight: 800; letter-spacing: .01em; font-variant-numeric: tabular-nums; }
    .report-date #reportDateValue { color: var(--text); font-size: 15px; font-weight: 800; letter-spacing: .01em;
      text-transform: none; white-space: nowrap; font-variant-numeric: tabular-nums; }
    .report-date .rd-caret { display: inline-block; width: 2.5px; height: 16px; margin-left: 3px; border-radius: 2px;
      background: #2e74c8; box-shadow: 0 0 7px rgba(46, 116, 200, .6); animation: rdCaret 1s steps(1, end) infinite; }
    @keyframes rdCaret { 0%, 49% { opacity: 1; } 50%, 100% { opacity: 0; } }
    @media (prefers-reduced-motion: reduce) { .report-date .rd-caret { animation: none; } }
    html.night .rd-chip { background: linear-gradient(180deg, rgba(110, 168, 255, .17), rgba(13, 26, 42, .60));
      border-color: rgba(110, 168, 255, .38);
      box-shadow: 0 6px 18px rgba(0, 0, 0, .38), inset 0 1px 0 rgba(255, 255, 255, .06); }
    html.night .report-date .rd-label { color: #a9cbf7; }
    html.night .report-date .rd-caret { background: #6ea8ff; box-shadow: 0 0 10px rgba(110, 168, 255, .85); }
""".replace("\n", "\r\n")

OLD_MARKUP = '        <p class="report-date"><span id="reportDateLabel">Report Date</span><span id="reportDateValue" data-report-date="2026-11-05">November 5, 2026</span></p>\r\n'

NEW_MARKUP = (
    '        <p class="report-date"><span class="rd-chip"><span class="rd-label" id="reportDateLabel">Report Date</span>'
    '<span class="rd-type"><span class="rd-ghost" aria-hidden="true">November 5, 2026</span>'
    '<span id="reportDateValue" data-report-date="2026-11-05">November 5, 2026</span>'
    '<span class="rd-caret" aria-hidden="true"></span></span></span></p>\r\n'
)

JS = """
<script>
  /* 2026-11-06 (Melly): REPORT DATE typewriter (style 04). Types the date behind a caret,
     holds, clears and re-types. The full string is the one renderReportDate() writes, so
     EN/CN switches and archive-date picks restart it with the right text. The ghost span
     reserves the finished width, so the badge never jitters while it types. */
  (function () {
    var el = document.getElementById('reportDateValue');
    if (!el) return;
    var wrap = el.parentNode;
    var ghost = wrap.querySelector('.rd-ghost');
    var caret = wrap.querySelector('.rd-caret');
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var full = '', lastWritten = null, timer = null, typing = false;

    function measure(text) {
      if (!ghost) return;
      ghost.textContent = text;
      var w = ghost.getBoundingClientRect().width;
      if (w > 0) wrap.style.width = Math.ceil(w + 1) + 'px';
    }

    function hold() {
      setTimeout(function () {
        if (document.body.contains(el)) start(full);
      }, 1600);
    }

    function typeOnce() {
      var i = 0;
      typing = true;
      timer = setInterval(function () {
        i += 1;
        lastWritten = full.slice(0, i);
        el.textContent = lastWritten;
        if (i >= full.length) {
          clearInterval(timer); timer = null; typing = false;
          hold();
        }
      }, 55);
    }

    function start(text) {
      var next = (text || '').replace(/\\s+/g, ' ').trim();
      if (!next) return;
      full = next;
      measure(full);
      if (timer) { clearInterval(timer); timer = null; }
      if (reduce) { typing = false; lastWritten = full; el.textContent = full; return; }
      lastWritten = '';
      el.textContent = '';
      typeOnce();
    }

    if (window.MutationObserver) {
      new MutationObserver(function () {
        var txt = el.textContent;
        if (txt === lastWritten) return;              /* my own keystroke */
        if (typing && full.indexOf(txt) === 0) return;
        start(txt);                                   /* renderReportDate() wrote a new date */
      }).observe(el, { childList: true, characterData: true, subtree: true });
    }

    start(el.textContent);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { measure(full); });
    window.addEventListener('resize', function () { measure(full); });
  })();
</script>
""".replace("\n", "\r\n")

assert s.count(OLD_CSS) == 1, "css anchor hits: %d" % s.count(OLD_CSS)
assert s.count(OLD_MARKUP) == 1, "markup anchor hits: %d" % s.count(OLD_MARKUP)
assert s.count("\r\n</body>") == 1, "body anchor"
assert JS.count("</body>") == 0 and NEW_CSS.count("</body>") == 0
assert s.count("</script>") == 3

s = s.replace(OLD_CSS, NEW_CSS)
s = s.replace(OLD_MARKUP, NEW_MARKUP)
head, tail = s.split("\r\n</body>")
assert head.count("</script>") == 3, "tail anchor must be after every script block"
s = head + JS + "\r\n</body>" + tail
assert s.count("</script>") == 4 and s.count("<script>") == 4

open(P, "wb").write(s.encode("utf-8"))
crlf_after = open(P, "rb").read().count(b"\r\n")
print("crlf %d -> %d (+%d)" % (crlf_before, crlf_after, crlf_after - crlf_before))
print("bytes", len(open(P, "rb").read()))
print("tokens:", s.count('class="rd-chip"'), s.count("rdTypewriter"), s.count(".rd-caret"), s.count("#reportDateValue"))
