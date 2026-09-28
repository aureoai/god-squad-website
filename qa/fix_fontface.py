# -*- coding: utf-8 -*-
"""Repair the font_face filter body mangled by shell heredoc escaping."""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
NL = chr(10)

BROKEN_START = "    if name == 'font_face':"
NEXT_FILTER = "    if name == 'newline_to_br':"

GOOD = (
    "    if name == 'font_face':" + NL +
    "        # Shopify's font_face returns a BARE @font-face rule with no style" + NL +
    "        # element around it. Stubbing it to '' meant the harness could never" + NL +
    "        # see what happens when that text lands somewhere it must not, which" + NL +
    "        # is exactly the production bug Phase 10 found in the layout." + NL +
    "        if val is None or val is BLANK or val == '':" + NL +
    "            return ''" + NL +
    "        fam = ''" + NL +
    "        wt = ''" + NL +
    "        if hasattr(val, 'get'):" + NL +
    "            fam = _s(val.get('family') or '')" + NL +
    "            wt = _s(val.get('weight') or '')" + NL +
    "        fam = fam or 'Stub Family'" + NL +
    "        wt = wt or '400'" + NL +
    "        disp = ''" + NL +
    "        for _k, _v in (kw or {}).items():" + NL +
    "            if _k == 'font_display':" + NL +
    "                disp = '  font-display: ' + _s(_v) + ';'" + NL +
    "        parts = ['@font-face {', '  font-family: ' + fam + ';'," + NL +
    "                 '  font-weight: ' + wt + ';']" + NL +
    "        if disp:" + NL +
    "            parts.append(disp)" + NL +
    "        parts.append(\"  src: url('stub.woff2') format('woff2');\")" + NL +
    "        parts.append('}')" + NL +
    "        return chr(10).join(parts)" + NL
)

for rel in ('phase9/miniliquid.py', 'phase8/miniliquid.py'):
    p = os.path.join(BASE, rel)
    s = open(p, encoding='utf-8').read()
    i = s.find(BROKEN_START)
    if i < 0:
        print('skip (no font_face block):', rel)
        continue
    j = s.find(NEXT_FILTER, i)
    assert j > i, 'could not find the following filter in ' + rel
    s = s[:i] + GOOD + s[j:]
    open(p, 'w', encoding='utf-8', newline='').write(s)
    print('repaired', rel)
