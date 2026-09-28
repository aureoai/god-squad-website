# -*- coding: utf-8 -*-
"""Phase 15 PART 19 + PART 20 — placeholder, demo and private-data scan.

Run against the SHIPPING theme, not the harness: the harness is allowed fixture
data, the theme is not. Phase 15 asks for exactly this sweep, so it is a
standing test rather than a one-off grep.
"""
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import os as _os
THEME = _os.environ.get('GS_THEME') or _os.path.join(
    _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))),
    'god-squad-theme')

PATTERNS = [
    (r'John Doe|Jane Doe|Juan dela Cruz|Test User|Sample Customer', 'placeholder person'),
    (r'[A-Za-z0-9._%+-]+@(?:example|test|foo|bar|mailinator|sample)\.[a-z]{2,}', 'placeholder email'),
    (r'#(?:1001|1002|1003|12345|1234)\b', 'placeholder order number'),
    (r'\b1Z[0-9A-Z]{16}\b', 'courier tracking literal'),
    (r'\bconsole\.(?:log|info|debug|table|dir)\s*\(', 'console logging'),
    (r'\blocalStorage\b|\bsessionStorage\b|\bindexedDB\b|document\.cookie', 'client-side storage'),
    (r'lorem ipsum', 'lorem'),
    # Customer-identifying values must never reach a URL, a data- attribute or
    # an analytics call. These are the shapes that would.
    (r'data-[\w-]*(?:email|customer|order-id|tracking)[\w-]*=', 'customer data in an attribute'),
    (r'[?&](?:email|customer_id|order_id|token|key)=\{\{', 'customer data in a query string'),
]

# Comments may legitimately DISCUSS these things — the whole project documents
# its reasoning in comments, and three tests have already been fooled by prose.
COMMENT = [
    (r'\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}', re.S),
    (r'/\*.*?\*/', re.S),
    (r'(?m)^\s*//.*$', 0),
]


def strip_comments(text):
    for pat, flags in COMMENT:
        text = re.sub(pat, '', text, flags=flags)
    return text


if __name__ == '__main__':
    hits = []
    scanned = 0
    for root, dirs, files in os.walk(THEME):
        for f in sorted(files):
            p = os.path.join(root, f)
            rel = os.path.relpath(p, THEME).replace(os.sep, '/')
            try:
                raw = io.open(p, encoding='utf-8').read()
            except Exception:
                continue
            scanned += 1
            src = strip_comments(raw)
            for pat, what in PATTERNS:
                for m in re.finditer(pat, src, re.I):
                    line = src[:m.start()].count('\n') + 1
                    ctx = src.splitlines()[line - 1].strip()[:80]
                    hits.append((rel, what, line, ctx))

    print('=== PHASE 15 HYGIENE SWEEP (comments stripped) ===')
    print('scanned %d files' % scanned)
    print()
    if hits:
        for rel, what, line, ctx in hits:
            print('  %-38s %-30s :%-4d %s' % (rel, what, line, ctx))
    else:
        print('  no placeholder, demo or private-data patterns in shipping code')
    print()
    print('%d finding(s)' % len(hits))
    print('OVERALL: %s' % ('PASS' if not hits else '*** REVIEW ABOVE ***'))
