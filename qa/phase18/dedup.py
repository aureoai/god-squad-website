# -*- coding: utf-8 -*-
"""Phase 18 — collapse 98 audit findings onto the defects that actually exist.

Seven dimensions audited the same theme independently, so one defect can arrive
five times wearing five labels. The chevron rotation is reported by icons,
legacy, buttons and motion-states; the hover-media-query gap by buttons and
motion-states; the inline-link hover by legacy and motion-states. Counting those
as separate findings would overstate the problem and, worse, would have me fix
the same lines four times.

Independent rediscovery is EVIDENCE, though, not noise: four agents reaching the
same file and line by different routes is a much stronger signal than one agent
asserting it once. So this groups by (file, line) and by shared subject, keeps
the highest severity in each group, and reports how many dimensions found it.

Writes a worklist to disk so the fixes can be worked through in order.
"""
import io
import json
import os
import re
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..', '..', 'tasks', 'wtlxbfsav.output'))
SEP = 'god-squad-theme' + os.sep
ORDER = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}


def short(p):
    p = p or ''
    if SEP in p:
        p = p.split(SEP)[-1]
    p = p.replace(os.sep, '/')
    return re.sub(r'^god-squad-theme/', '', p)


# Subjects that are one defect however many dimensions describe it.
SUBJECTS = [
    ('chevron disclosure rotation/size', ['chevron']),
    ('hover outside @media (hover:hover)', ['@media (hover', 'hover: hover', 'hover rules']),
    ('rich-text inline link hover', ['inline-link', 'inline link', 'rich-text']),
    ('empty / zero-result state treatment', ['empty-state', 'empty state', 'zero-result',
                                             'nothing here', 'empty__title', 'empty-title']),
    ('H3/H4 display-vs-body family', ['h3/h4', '--type-h3', '--type-h4', 'font-display']),
]

d = json.load(io.open(OUT, encoding='utf-8', errors='replace'))
rows = []
for dim in d['result']:
    for v in (dim.get('verdicts') or []):
        if v.get('verdict') in ('CONFIRMED', 'PLAUSIBLE'):
            v = dict(v)
            v['dim'] = dim['dimension']
            v['f'] = short(v.get('file'))
            rows.append(v)


def subject_of(v):
    blob = ' '.join([v.get('problem') or '', v.get('why') or '']).lower()
    for name, keys in SUBJECTS:
        if any(k in blob for k in keys):
            return name
    return None


groups = defaultdict(list)
for v in rows:
    s = subject_of(v)
    key = ('subject', s) if s else ('loc', v['f'], v.get('line'))
    groups[key].append(v)

out = []
for key, vs in groups.items():
    vs.sort(key=lambda x: ORDER.get(x.get('severity'), 9))
    top = vs[0]
    out.append({
        'severity': top.get('severity'),
        'sev_rank': ORDER.get(top.get('severity'), 9),
        'title': (top.get('problem') or '')[:200],
        'file': top['f'],
        'line': top.get('line'),
        'dims': sorted({v['dim'] for v in vs}),
        'n': len(vs),
        'fix': top.get('fix'),
        'why': top.get('why'),
        'flag': any(v.get('would_undo_a_deliberate_decision') for v in vs),
        'all_files': sorted({(v['f'], v.get('line')) for v in vs}),
    })

out.sort(key=lambda x: (x['sev_rank'], -x['n']))
io.open(os.path.join(HERE, 'worklist.json'), 'w', encoding='utf-8').write(
    json.dumps(out, indent=2, ensure_ascii=False))

print('=== %d findings -> %d distinct defects ===' % (len(rows), len(out)))
print()
from collections import Counter
print('  severity after dedup: %s' % dict(Counter(x['severity'] for x in out)))
print()
print('=== CORROBORATED BY MORE THAN ONE DIMENSION (strongest signal) ===')
for x in out:
    if x['n'] > 1:
        print('  [%-8s] x%d  %s' % (x['severity'], x['n'], ', '.join(x['dims'])))
        print('      %s' % ' '.join(x['title'].split())[:150])
        print('      %s:%s' % (x['file'], x['line']))
print()
print('=== CRITICAL + HIGH WORKLIST ===')
for i, x in enumerate([y for y in out if y['sev_rank'] <= 1], 1):
    print('%3d. [%-8s] %-13s %s:%s%s'
          % (i, x['severity'], ','.join(x['dims'])[:13], x['file'], x['line'],
             '  !!FLAG' if x['flag'] else ''))
    print('     %s' % ' '.join(x['title'].split())[:165])
print()
print('worklist.json written (%d entries)' % len(out))
