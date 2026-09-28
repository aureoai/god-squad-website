# -*- coding: utf-8 -*-
"""Phase 18 - pointer-scope the five remaining ungated hover rules.

PHASE-2 22.1 rule 5. Each rule is wrapped verbatim; no declaration changes,
only the media query around it. The header's four were done by hand because one
of them also had to be split from a current-page state.
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ASSETS = os.path.join(
    r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\god-squad-theme", 'assets')

MQ_OPEN = '@media (hover: hover) and (pointer: fine) {\n'

# (file, exact rule text, note placed above the media query)
JOBS = [
    ('section-cart-drawer.css',
     '.cart-drawer__continue:hover {\n  color: inherit;\n}',
     "/* Pointer-scoped in Phase 18. This closes a drawer over the same page --\n"
     "   nothing navigates -- so a tap left it in its hover colour. */"),
    ('section-footer.css',
     '.footer__link:hover {\n  color: var(--accent-current);\n'
     '  text-decoration: underline;\n'
     '  text-underline-offset: var(--link-underline-offset);\n'
     '  text-decoration-thickness: var(--link-underline-thickness);\n}',
     '/* Pointer-scoped in Phase 18 (PHASE-2 22.1 rule 5). */'),
    ('section-footer.css',
     '.footer__text a:hover {\n  color: var(--accent-current);\n}',
     '/* Pointer-scoped in Phase 18 (PHASE-2 22.1 rule 5). */'),
    ('section-main-cart.css',
     '.main-cart__continue:hover {\n  color: inherit;\n}',
     '/* Pointer-scoped in Phase 18 (PHASE-2 22.1 rule 5). */'),
    ('section-main-page.css',
     '.main-page__content a:hover {\n  color: var(--accent-current);\n}',
     '/* Pointer-scoped in Phase 18 (PHASE-2 22.1 rule 5). */'),
]

for fname, rule, note in JOBS:
    p = os.path.join(ASSETS, fname)
    s = io.open(p, encoding='utf-8').read()
    n = s.count(rule)
    if n != 1:
        raise SystemExit('  %-28s *** %d matches, expected 1 ***' % (fname, n))
    indented = '\n'.join(('  ' + ln if ln.strip() else ln) for ln in rule.split('\n'))
    io.open(p, 'w', encoding='utf-8').write(
        s.replace(rule, note + '\n' + MQ_OPEN + indented + '\n}', 1))
    print('  ok  %-28s %s' % (fname, rule.split('{')[0].strip()))
