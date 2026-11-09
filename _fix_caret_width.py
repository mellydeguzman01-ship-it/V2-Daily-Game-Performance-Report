import os, sys
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
s = open(P, "rb").read().decode("utf-8")
crlf_before = s.count("\r\n")

OLD = """      var w = ghost.getBoundingClientRect().width;\r
      if (w > 0) wrap.style.width = Math.ceil(w + 1) + 'px';\r
"""
NEW = """      var w = ghost.getBoundingClientRect().width;\r
      var cw = caret ? caret.getBoundingClientRect().width + 3 : 0;\r
      if (w > 0) wrap.style.width = Math.ceil(w + cw + 1) + 'px';\r
"""
assert s.count(OLD) == 1, s.count(OLD)
s = s.replace(OLD, NEW)
assert s.count("\r\n") == crlf_before + 1, (crlf_before, s.count("\r\n"))
open(P, "wb").write(s.encode("utf-8"))
print("ok crlf", s.count("\r\n"))
