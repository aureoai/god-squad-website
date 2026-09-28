# -*- coding: utf-8 -*-
import json, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
T = (r"C:\Users\TEST\AppData\Local\Temp\claude"
     r"\C--Users-TEST-OneDrive-Documents-GodSquad-Website"
     r"\de238d03-508d-43ce-a377-210f71ff0033\tasks\w8znmmgry.output")
doc = json.load(open(T, encoding='utf-8', errors='replace'))
payload = doc['result']

print('LOGS:', doc.get('logs'))
print('COUNTS:', payload.get('counts'))
print()
order = {'blocker': 0, 'major': 1, 'minor': 2}
conf = sorted(payload['confirmed'], key=lambda f: order.get(f['severity'], 3))
print('=' * 78)
print('CONFIRMED FINDINGS (%d)' % len(conf))
print('=' * 78)
for i, f in enumerate(conf, 1):
    print()
    print('%2d. [%s] %s   (%s)  refuted %s/%s' %
          (i, f['severity'].upper(), f['id'], f.get('dimension', '?'),
           f.get('refuted_votes'), f.get('total_votes')))
    print('    file : %s | %s' % (f['file'], f.get('line_hint', '')))
    print('    claim: %s' % f['claim'])
    print('    fail : %s' % f['failure'][:400])
    print('    fix  : %s' % f['fix'][:400])
print()
print('=' * 78)
print('REFUTED (%d) — not acted on' % len(payload.get('refuted', [])))
print('=' * 78)
for f in payload.get('refuted', []):
    print(' -', f['id'], ':', f['claim'][:130])
