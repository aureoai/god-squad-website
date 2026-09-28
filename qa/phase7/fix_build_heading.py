# -*- coding: utf-8 -*-
"""Repair the harness heading literal a heredoc broke, and stop using heredocs."""
p = (r"C:\Users\TEST\AppData\Local\Temp\claude"
     r"\C--Users-TEST-OneDrive-Documents-GodSquad-Website"
     r"\de238d03-508d-43ce-a377-210f71ff0033\scratchpad\phase7\build.py")
lines = open(p, encoding='utf-8').read().split('\n')

start = next(i for i, l in enumerate(lines) if l.strip().startswith("'heading': 'Real People."))
# The broken literal spans two physical lines.
assert lines[start + 1].strip().startswith("Bigger Purpose.'"), lines[start + 1]
lines[start:start + 2] = ["    'heading': 'Real People.' + chr(10) + 'Bigger Purpose.',"]

# The caption literal survived because it was written by the Write tool, but
# normalise it the same way so nothing depends on escape handling.
for i, l in enumerate(lines):
    if "'caption': 'Faith" in l:
        lines[i] = ("    'show_caption': True, 'caption': "
                    "chr(10).join(['Faith', 'Lives', 'Different', 'Here.']),")
        break

open(p, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
print('build.py repaired')

import subprocess, sys, os
r = subprocess.run([sys.executable, 'build.py'], cwd=os.path.dirname(p),
                   capture_output=True, text=True)
print(r.stdout[-900:] or r.stderr[-1500:])
