# -*- coding: utf-8 -*-
"""Phase 18 — read the design-audit workflow's verdicts into a triage list.

Fourteen agents across seven dimensions, each finding adversarially verified by
a second agent. This prints them ranked so every one can be decided on
individually against my own measurements, rather than accepted wholesale.

A CONFIRMED verdict from a verifier is a claim with evidence attached, not a
fact. Several of these touch code earlier phases chose deliberately, and the
`would_undo_a_deliberate_decision` flag is the audit's own warning about that.
Anything that contradicts a measurement I hold gets re-measured before it is
written down as a defect.
"""
import io
import json
import os
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
OUT = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tasks', 'wtlxbfsav.output'))

SEP = 'god-squad-theme' + os.sep


def short(p):
    p = p or ''
    if SEP in p:
        p = p.split(SEP)[-1]
    return p.replace(os.sep, '/')


d = json.load(io.open(OUT, encoding='utf-8', errors='replace'))
res = d['result']
print('workflow logs: %s' % d.get('logs'))
print()

tot, sev = Counter(), Counter()
print('=== BY DIMENSION ===')
for dim in res:
    vs = dim.get('verdicts') or []
    c = Counter(v.get('verdict', '?') for v in vs)
    print('  %-14s %2d verdicts   %s' % (dim.get('dimension', '?'), len(vs), dict(c)))
    for v in vs:
        tot[v.get('verdict', '?')] += 1
        if v.get('verdict') in ('CONFIRMED', 'PLAUSIBLE'):
            sev[v.get('severity', '?')] += 1
print()
print('  totals:   %s' % dict(tot))
print('  severity: %s' % dict(sev))

ORDER = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
rows = []
for dim in res:
    for v in (dim.get('verdicts') or []):
        if v.get('verdict') in ('CONFIRMED', 'PLAUSIBLE'):
            rows.append((ORDER.get(v.get('severity'), 9), dim['dimension'], v))
rows.sort(key=lambda x: (x[0], x[1]))

print()
print('=== FINDINGS, RANKED ===')
for i, (_, dn, v) in enumerate(rows, 1):
    flag = '  !! CLAIMS TO UNDO A DELIBERATE DECISION' \
        if v.get('would_undo_a_deliberate_decision') else ''
    print('%3d. [%-8s %-9s] %-13s %s:%s%s'
          % (i, v.get('severity'), v.get('verdict'), dn,
             short(v.get('file')), v.get('line'), flag))
    print('     %s' % ' '.join((v.get('problem') or '').split())[:190])

print()
print('=== THE ONES THAT TOUCH WHAT I ALREADY MEASURED ===')
KEYS = ['pagination', 'container', 'product-card__error', 'line-height',
        'cart-line__title', 'label-lh']
for _, dn, v in rows:
    blob = ' '.join([(v.get('problem') or ''), (v.get('why') or ''),
                     (v.get('file') or '')]).lower()
    hit = [k for k in KEYS if k.lower() in blob]
    if hit:
        print('  %-13s %-8s %s   <- %s'
              % (dn, v.get('severity'), short(v.get('file')), ', '.join(hit)))
        print('      %s' % ' '.join((v.get('problem') or '').split())[:170])
