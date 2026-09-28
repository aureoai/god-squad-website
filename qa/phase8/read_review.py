# -*- coding: utf-8 -*-
import json, io, sys, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
T = (r"C:\Users\TEST\AppData\Local\Temp\claude"
     r"\C--Users-TEST-OneDrive-Documents-GodSquad-Website"
     r"\de238d03-508d-43ce-a377-210f71ff0033\tasks\wnj31s8r2.output")
doc = json.load(open(T, encoding='utf-8', errors='replace'))
r = doc['result']
print('COUNTS:', r['counts'])
print()
order = {'blocker': 0, 'major': 1, 'minor': 2}
conf = sorted(r['confirmed'], key=lambda f: order.get(f['severity'], 3))
for i, f in enumerate(conf, 1):
    print('%2d. [%-7s] %-48s %-22s refuted %s/%s' % (
        i, f['severity'].upper(), f['id'], f.get('dimension', '?'),
        f.get('refuted_votes'), f.get('total_votes')))
    print('    file : %s | %s' % (os.path.basename(f['file']), (f.get('line_hint') or '')[:66]))
    print('    claim: %s' % ' '.join(f['claim'].split())[:330])
    print('    fix  : %s' % ' '.join(f['fix'].split())[:250])
    print()
print('=' * 80)
print('REFUTED (%d)' % len(r.get('refuted', [])))
for f in r.get('refuted', []):
    print(' - [%s] %s : %s' % (f['severity'], f['id'], ' '.join(f['claim'].split())[:110]))
