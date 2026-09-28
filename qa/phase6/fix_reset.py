# -*- coding: utf-8 -*-
"""Add the one missing reset: body margin.

Found by measuring, not by reading. Every band came out 16px narrower than the
viewport at every width, which traced to the user agent's default
`body { margin: 8px }`. Nothing in the theme resets it, so Phase 2 section 8's
full-bleed container model never actually reached the viewport edge: the hero
photograph, the header scrim and both collection bands all carried an 8px strip
of page background down each side.

Phase 5 did not catch it because its harness page set `body{margin:0}` in its
own styles; the Phase 6 harness does not, which is what exposed it.

The rule goes in the GLOBAL BEHAVIOUR block beside the box-sizing reset, in
both the canonical Phase 2 file and its theme copy, so the two stay in step.
"""
files = [
    r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\PHASE-2-DESIGN-TOKENS.css",
    r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\design-tokens.css",
]

old = """*, *::before, *::after { box-sizing: border-box; }"""

new = """*, *::before, *::after { box-sizing: border-box; }

/* The user agent's 8px body margin would inset every full-bleed band, so the
   container model in section 8 — full-bleed section, constrained content —
   could never reach the viewport edge. Measured in Phase 6: every band came
   out 16px narrower than the viewport at every width until this was added. */
body { margin: 0; }"""

for p in files:
    s = open(p, encoding='utf-8').read()
    assert old in s, 'box-sizing reset not found in ' + p
    assert 'body { margin: 0; }' not in s, 'already reset in ' + p
    open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new, 1))
    print('reset added to', p.rsplit('\\', 1)[-1])
