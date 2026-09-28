# -*- coding: utf-8 -*-
"""Phase 17 — negative control for tracking.py.

The whole Phase 17 audit reports an ABSENCE: no pixel, no ID, no third-party
host, no PII path. An absence report that has never been seen to fail is
worthless, so this seeds each class of violation into a throwaway copy of the
theme and requires the auditor to catch it.

The seeds are deliberately realistic — the snippets a developer actually pastes
in — rather than strings chosen to match the regex.
"""
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
def append(root, rel, text):
    p = os.path.join(root, rel.replace('/', os.sep))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with io.open(p, 'a', encoding='utf-8') as fh:
        fh.write(text)


VIOLATIONS = [
    ('GA4 pasted into the layout', 'layout/theme.liquid',
     '\n<script async src="https://www.googletagmanager.com/gtag/js?id=G-ABC1234567"></script>\n'
     '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}\n'
     'gtag(\'js\', new Date()); gtag(\'config\', \'G-ABC1234567\');</script>\n',
     ['no tracking platform', 'GA4 measurement ID literal', 'reaches no third-party host']),

    ('Meta Pixel pasted into the layout', 'layout/theme.liquid',
     "\n<script>!function(f,b,e,v,n,t,s){}(window,document,'script',"
     "'https://connect.facebook.net/en_US/fbevents.js');fbq('init','1234567890123456');"
     "fbq('track','PageView');</script>\n",
     ['no tracking platform', 'Meta Pixel ID shape literal', 'reaches no third-party host']),

    ('TikTok pixel in a section', 'sections/main-product.liquid',
     "\n<script>ttq.load('CABCDEFGHIJKLMNOPQRS');ttq.page();</script>\n",
     ['no tracking platform']),

    ('a dataLayer push from cart.js', 'assets/cart.js',
     "\nwindow.dataLayer = window.dataLayer || [];\n"
     "window.dataLayer.push({event: 'add_to_cart'});\n",
     ['no tracking platform']),

    ('customer email written into the page', 'sections/footer.liquid',
     '\n<span data-email="{{ customer.email }}"></span>\n',
     ['no customer field is read']),

    ('an analytics id stashed in localStorage', 'assets/header.js',
     "\nlocalStorage.setItem('_ga_cid', Math.random());\n",
     ['no localStorage']),

    ('a tracking pixel built with new Image()', 'assets/product.js',
     "\nvar px = new Image(1,1); px.src = 'https://t.example.com/p?e=view';\n",
     ['no new Image(']),

    ('a beacon to an off-origin collector', 'assets/facets.js',
     "\nnavigator.sendBeacon('https://collect.example.com/e', '{}');\n",
     ['no navigator.sendBeacon']),

    ('console logging of a tracking payload', 'assets/cart.js',
     "\nconsole.log('track', {event: 'purchase'});\n",
     ['no console logging']),

    ('customer data written into a cart attribute', 'snippets/cart-note.liquid',
     '\n<input type="hidden" name="attributes[email]" value="x">\n',
     ['nothing is written into a cart attribute']),

    ('Hotjar in the layout', 'layout/theme.liquid',
     "\n<script>window._hjSettings={hjid:123};</script>\n"
     '<script src="https://static.hotjar.com/c/hotjar.js"></script>\n',
     ['no tracking platform', 'reaches no third-party host']),

    ('a GTM container', 'layout/theme.liquid',
     "\n<script>(function(w,d,s,l,i){})(window,document,'script','dataLayer','GTM-ABC1234');</script>\n",
     ['no tracking platform', 'GTM container ID literal']),
]


def run(root):
    env = dict(os.environ, GS_THEME=root, PYTHONIOENCODING='utf-8')
    out = subprocess.run([sys.executable, os.path.join(HERE, 'tracking.py')],
                         capture_output=True, text=True, encoding='utf-8',
                         errors='replace', env=env).stdout
    return [re.sub(r'\s+', ' ', l.split('*** FOUND ***')[0]).strip()
            for l in out.splitlines() if '*** FOUND ***' in l]


if __name__ == '__main__':
    print('=== EVERY ABSENCE CLAIM, SEEN TO FAIL ===')
    print()
    gaps = []
    for name, rel, text, expect_any in VIOLATIONS:
        root = tempfile.mkdtemp(prefix='gs17-')
        shutil.rmtree(root)
        shutil.copytree(THEME, root)
        try:
            append(root, rel, text)
            found = run(root)
            caught = [e for e in expect_any
                      if any(e.lower() in f.lower() for f in found)]
            ok = len(caught) == len(expect_any)
            print('  %-42s %s' % (name, 'CAUGHT' if ok else '*** MISSED ***'))
            if not ok:
                missed = [e for e in expect_any if e not in caught]
                gaps.append((name, missed, found))
        finally:
            shutil.rmtree(root, ignore_errors=True)

    print()
    for name, missed, found in gaps:
        print('  MISSED: %s' % name)
        print('    expected findings containing: %s' % missed)
        print('    actual findings: %s' % (found or 'NONE — a seeded theme passed clean'))
    print('%d violations seeded, %d fully caught, %d with gaps'
          % (len(VIOLATIONS), len(VIOLATIONS) - len(gaps), len(gaps)))
    print('OVERALL: %s' % ('PASS' if not gaps else '*** GAPS ABOVE ***'))
