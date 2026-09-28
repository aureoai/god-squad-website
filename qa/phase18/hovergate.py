# -*- coding: utf-8 -*-
"""Phase 18 — every :hover rule, and whether it is pointer-scoped.

PHASE-2-DESIGN-SYSTEM.md §22.1 rule 5: "Hover is pointer-scoped. Hover rules sit
inside @media (hover: hover) so a touch tap never leaves an element stuck in a
hover state."

That matters most for controls that do NOT navigate away. Tapping a link is
forgiven because the page changes; tapping the header's menu toggle or the cart
drawer's "continue shopping" leaves the element sitting in its hover state on a
touch screen, because nothing reloads to clear it.

This tracks brace depth so it knows which @media block a rule is inside, rather
than matching text near it. It is also the regression test for the fix: run it
again afterwards and the ungated list should be empty.
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
THEME = os.environ.get('GS_THEME') or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
ASSETS = os.path.join(THEME, 'assets')

HOVER_MQ = re.compile(r'@media[^{]*hover:\s*hover', re.I)


def scan(path):
    """Yield (line_no, selector, inside_hover_media) for every :hover rule."""
    src = io.open(path, encoding='utf-8').read()
    # Blank out comments but keep newlines so line numbers survive.
    src = re.sub(r'/\*.*?\*/', lambda m: re.sub(r'[^\n]', ' ', m.group(0)), src, flags=re.S)
    depth = 0
    hover_depths = []          # depths at which a hover media query opened
    buf = ''
    line = 1
    out = []
    for ch in src:
        if ch == '\n':
            line += 1
        if ch == '{':
            head = ' '.join(buf.split())
            if head.startswith('@media'):
                depth += 1
                if HOVER_MQ.search(head):
                    hover_depths.append(depth)
            else:
                depth += 1
                if ':hover' in head:
                    out.append((line, head, bool(hover_depths)))
            buf = ''
        elif ch == '}':
            if hover_depths and hover_depths[-1] == depth:
                hover_depths.pop()
            depth -= 1
            buf = ''
        else:
            buf += ch
    return out


if __name__ == '__main__':
    gated, ungated = [], []
    for f in sorted(os.listdir(ASSETS)):
        if not f.endswith('.css'):
            continue
        for line, sel, inside in scan(os.path.join(ASSETS, f)):
            (gated if inside else ungated).append((f, line, sel))

    print('=== HOVER RULES OUTSIDE @media (hover: hover) ===')
    if not ungated:
        print('  none')
    for f, line, sel in ungated:
        print('  %-30s :%-5d %s' % (f, line, sel[:90]))

    print()
    print('=== CORRECTLY POINTER-SCOPED ===')
    from collections import Counter
    for f, n in sorted(Counter(x[0] for x in gated).items()):
        print('  %-30s %d rule(s)' % (f, n))

    print()
    print('%d hover rule(s) total: %d gated, %d ungated'
          % (len(gated) + len(ungated), len(gated), len(ungated)))
    print('OVERALL: %s' % ('PASS' if not ungated
                           else '*** %d UNGATED ***' % len(ungated)))
