# -*- coding: utf-8 -*-
"""Make every QA suite honour GS_BROWSER instead of hardcoding Edge.

Eight suites pin the browser path in a module-level constant:

    EDGE = r"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"

On 2026-09-26 Edge's --dump-dom began returning zero bytes with exit code 0, so
those eight reported NO READING while the suites that read GS_BROWSER ran fine
against Chrome. A browser that stops working should not be able to take a third
of the test suite down with it.

This rewrites the constant to read the environment first and keep the same Edge
path as the fallback, so nothing changes for anyone who has a working Edge:

    EDGE = os.environ.get('GS_BROWSER') or r"C:\\...\\msedge.exe"

`os` is already imported in every one of them (each builds paths with it), and
that is asserted rather than assumed before the file is touched.
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))

TARGETS = [
    'phase9/cardcascade.py', 'phase9/editor.py', 'phase9/respond.py',
    'phase8/contrast8.py', 'phase8/interact.py', 'phase8/interact_cartpage.py',
    'phase8/interact_product.py', 'phase8/console.py',
]

PAT = re.compile(
    r'^(?P<name>EDGE|CHROME|BROWSER)\s*=\s*r?"(?P<path>[^"]*msedge\.exe)"\s*$',
    re.M)

changed = skipped = 0
for rel in TARGETS:
    p = os.path.join(HERE, rel.replace('/', os.sep))
    if not os.path.exists(p):
        print('  --  %-30s not found' % rel)
        continue
    s = io.open(p, encoding='utf-8').read()

    if 'GS_BROWSER' in s:
        print('  --  %-30s already honours GS_BROWSER' % rel)
        skipped += 1
        continue

    m = PAT.search(s)
    if not m:
        print('  *** %-30s no hardcoded browser constant found' % rel)
        continue

    if not re.search(r'^import os$|^import os\b', s, re.M):
        print('  *** %-30s does not import os — SKIPPED' % rel)
        continue

    new_line = ("%s = os.environ.get('GS_BROWSER') or r\"%s\""
                % (m.group('name'), m.group('path')))
    s = s[:m.start()] + new_line + s[m.end():]
    io.open(p, 'w', encoding='utf-8').write(s)
    changed += 1
    print('  ok  %-30s %s now reads GS_BROWSER' % (rel, m.group('name')))

print()
print('%d patched, %d already fine' % (changed, skipped))
print()
print('Verifying every suite parses:')
import py_compile
bad = 0
for rel in TARGETS:
    p = os.path.join(HERE, rel.replace('/', os.sep))
    if not os.path.exists(p):
        continue
    try:
        py_compile.compile(p, doraise=True)
        print('  ok  %s' % rel)
    except Exception as e:
        bad += 1
        print('  *** %s: %s' % (rel, str(e)[:90]))
raise SystemExit(1 if bad else 0)
