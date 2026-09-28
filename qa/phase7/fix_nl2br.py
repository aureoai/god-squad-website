# -*- coding: utf-8 -*-
"""Match Shopify's newline_to_br exactly.

Shopify's implementation is gsub(/\\r?\\n/, "<br />\\n") — it INSERTS the tag and
keeps the newline. The harness replaced the newline instead, so the rendered
text node lost its whitespace and the probe reported the heading's accessible
name as "Real People.Bigger Purpose." with no separator. That was the harness
misreporting, not the theme, and it would have sent me chasing a defect that
does not exist.
"""
p = (r"C:\Users\TEST\AppData\Local\Temp\claude"
     r"\C--Users-TEST-OneDrive-Documents-GodSquad-Website"
     r"\de238d03-508d-43ce-a377-210f71ff0033\scratchpad\phase7\miniliquid.py")
lines = open(p, encoding='utf-8').read().split('\n')
i = next(k for k, l in enumerate(lines) if "if name == 'newline_to_br':" in l)
assert 'replace' in lines[i + 1], lines[i + 1]
lines[i + 1] = ("        return re.sub(r'\\r?\\n', '<br />' + chr(10), _s(val))")
open(p, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
print('miniliquid: newline_to_br now matches Shopify')

import subprocess, sys, os
HERE = os.path.dirname(p)
r = subprocess.run([sys.executable, 'build.py'], cwd=HERE, capture_output=True, text=True)
print((r.stdout or r.stderr)[-300:])
