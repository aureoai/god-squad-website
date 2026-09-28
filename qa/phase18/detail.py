# -*- coding: utf-8 -*-
"""Phase 18 — print one deduplicated defect in full, fix text included.

Usage: python detail.py <index>            (indexes from the CRITICAL+HIGH list)
       python detail.py <index> --all      (index into every severity)
"""
import io
import json
import os
import sys
import textwrap

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
work = json.load(io.open(os.path.join(HERE, 'worklist.json'), encoding='utf-8'))

args = [a for a in sys.argv[1:] if not a.startswith('--')]
rows = work if '--all' in sys.argv else [w for w in work if w['sev_rank'] <= 1]


def show(x, i):
    print('=' * 78)
    print('[%s] %s:%s   (found by %d agent(s): %s)'
          % (x['severity'], x['file'], x['line'], x['n'], ', '.join(x['dims'])))
    if x['flag']:
        print('!! the audit flags this as possibly undoing a deliberate decision')
    print('=' * 78)
    for label, key in (('PROBLEM', 'title'), ('WHY', 'why'), ('FIX', 'fix')):
        v = x.get(key)
        if not v:
            continue
        print('%s:' % label)
        for para in str(v).split('\n'):
            print(textwrap.fill(para, 76, initial_indent='  ', subsequent_indent='  '))
        print()
    if len(x['all_files']) > 1:
        print('ALL SITES:')
        for f, l in x['all_files']:
            print('  %s:%s' % (f, l))
        print()


if args:
    for a in args:
        n = int(a)
        if 1 <= n <= len(rows):
            show(rows[n - 1], n)
else:
    for i, x in enumerate(rows, 1):
        print('%3d. [%-8s] %-30s %s'
              % (i, x['severity'], '%s:%s' % (x['file'], x['line']),
                 ' '.join(x['title'].split())[:90]))
