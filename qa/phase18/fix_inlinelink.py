# -*- coding: utf-8 -*-
"""Phase 18 - the merchant rich-text link, hovering on all five surfaces.

Five stylesheets declare the same three-declaration rest rule for a link inside
merchant rich text. Two of them follow it with a hover; three do not. So the
same <a> a merchant types into a description responds in the footer and on a
page, and sits inert in a collection description, a product description and the
Our Story body.

The hover added here is the one the other two already use - the accent colour,
pointer-scoped per PHASE-2 22.1 rule 5, which Phase 18 has just made true of
every hover rule in the theme.
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ASSETS = os.path.join(
    r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\god-squad-theme", 'assets')

REST = ('  color: inherit;\n'
        '  text-underline-offset: var(--link-underline-offset);\n'
        '  text-decoration-thickness: var(--link-underline-thickness);\n}')

NOTE = ('\n\n/* Phase 18. The other four surfaces that style a merchant rich-text link\n'
        '   declare this same rest rule; two of them had a hover and three did not, so\n'
        '   the identical link responded on some pages and not others. Pointer-scoped\n'
        '   per PHASE-2 22.1 rule 5. */\n'
        '@media (hover: hover) and (pointer: fine) {\n'
        '  %s:hover {\n'
        '    color: var(--accent-current);\n'
        '  }\n}')

JOBS = [
    ('section-main-collection.css', '.main-collection__description a'),
    ('section-main-product.css', '.main-product__description a'),
    ('section-our-story.css', '.our-story__body a'),
]

for fname, sel in JOBS:
    p = os.path.join(ASSETS, fname)
    s = io.open(p, encoding='utf-8').read()
    anchor = sel + ' {\n' + REST
    if s.count(anchor) != 1:
        print('  *** %-30s anchor not unique (%d)' % (fname, s.count(anchor)))
        continue
    io.open(p, 'w', encoding='utf-8').write(
        s.replace(anchor, anchor + (NOTE % sel), 1))
    print('  ok  %-30s %s:hover added' % (fname, sel))
