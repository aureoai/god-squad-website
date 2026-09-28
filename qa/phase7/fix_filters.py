# -*- coding: utf-8 -*-
"""Repair the newline_to_br filter.

A bash heredoc turned the escaped newlines in the pattern into real ones, so
the file no longer parsed. Written through a file this time — the third time
this session that a heredoc has mangled a backslash escape.
"""
p = (r"C:\Users\TEST\AppData\Local\Temp\claude"
     r"\C--Users-TEST-OneDrive-Documents-GodSquad-Website"
     r"\de238d03-508d-43ce-a377-210f71ff0033\scratchpad\phase7\miniliquid.py")
lines = open(p, encoding='utf-8').read().split('\n')

start = next(i for i, l in enumerate(lines) if "if name == 'newline_to_br':" in l)
end = next(i for i, l in enumerate(lines) if "if name == 'strip_html':" in l)

repl = [
    "    if name == 'newline_to_br':",
    "        return _s(val).replace(chr(13) + chr(10), '<br />').replace(chr(10), '<br />')",
]
lines[start:end] = repl
open(p, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
print('newline_to_br repaired')
import subprocess, sys
subprocess.run([sys.executable, '-c', 'import sys; sys.path.insert(0, r"%s"); import miniliquid; print("imports ok")'
                % p.rsplit('\\', 1)[0]], check=True)
