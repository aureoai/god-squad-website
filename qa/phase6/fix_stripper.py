# -*- coding: utf-8 -*-
"""Repair the stripper regex.

A bash heredoc turned the \\b in the pattern into a literal backspace byte
(0x08), so the expression could never match and the prohibition checks kept
firing on the code's own documentation. Written through a file this time.
"""
p = r"C:\Users\TEST\AppData\Local\Temp\claude\C--Users-TEST-OneDrive-Documents-GodSquad-Website\de238d03-508d-43ce-a377-210f71ff0033\scratchpad\phase6\validate.py"
lines = open(p, encoding='utf-8').read().split('\n')
for i, l in enumerate(lines):
    if 'endcomment' in l and 're.M' in l:
        lines[i] = (r"    s = re.sub(r'^[ \t]*comment[ \t]*$.*?^[ \t]*endcomment[ \t]*$', "
                    r"'', s, flags=re.S | re.M)")
        print('line %d replaced' % (i + 1))
        break
else:
    raise SystemExit('target line not found')
open(p, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
print(repr(lines[i]))
