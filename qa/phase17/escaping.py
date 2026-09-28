# -*- coding: utf-8 -*-
"""Phase 17 — untrusted input is never rendered as markup.

Shopify Liquid does NOT escape output. Anything a customer or an anonymous
poster controls and the theme prints is a markup-injection vector unless it goes
through | escape.

This is its own negative control: it renders the real snippets with real
payloads and fails if the payload comes back as live markup. It cannot pass
vacuously, because a missing filter produces the payload verbatim.
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', 'phase9')))
THEME = os.environ.get('GS_THEME') or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')

FAILURES = []
CHECKS = [0]


def check(label, ok, detail=''):
    CHECKS[0] += 1
    print('  %-58s %s %s' % (label, 'OK  ' if ok else '*** UNESCAPED ***',
                             '' if ok else str(detail)[:120]))
    if not ok:
        FAILURES.append(label)


BREAKOUT = '</p></textarea></title><img src=x onerror=alert(1)><b foo="'
ATTR = '" onmouseover="alert(2)'


if __name__ == '__main__':
    import build
    build.THEME = THEME

    print('=== RENDERED WITH A PAYLOAD, NOT GREPPED ===')
    line = build.line('k9:zzz', build.P_SIZES, build.P_SIZES['variants'][1], 1, 129000,
                      image=build.img('tee.webp', 'Tee', 900, 900),
                      options=[{'name': 'Size', 'value': 'S'}],
                      properties=[[BREAKOUT, BREAKOUT]])
    cart = build.build_cart([line], note=BREAKOUT)
    e = build.make_engine(cart=cart, template='cart')
    e.root = THEME

    def render(rel, scope):
        src = io.open(os.path.join(THEME, rel), encoding='utf-8').read()
        return e.render(src, scope)

    out = render('snippets/cart-line-item.liquid',
                 {'item': line, 'index': 1, 'form_id': 'F', 'scope': 'S'})
    check('a cart line property does not break out of its element',
          BREAKOUT not in out)
    check('and it is present, escaped, rather than dropped',
          '&lt;/p&gt;' in out or '&lt;' in out)

    note = render('snippets/cart-note.liquid', {'id': 'N'})
    check('the cart note does not close its textarea', BREAKOUT not in note)
    check('and it is present, escaped', '&lt;/textarea&gt;' in note)

    # A payload aimed at an attribute rather than at element content.
    line2 = build.line('k' + ATTR, build.P_SIZES, build.P_SIZES['variants'][1], 1, 129000,
                       image=build.img('tee.webp', 'Tee', 900, 900),
                       options=[{'name': 'Size', 'value': 'S'}])
    out2 = render('snippets/cart-line-item.liquid',
                  {'item': line2, 'index': 1, 'form_id': 'F', 'scope': 'S'})
    check('a line key cannot escape the attribute it is written into',
          'onmouseover="alert(2)"' not in out2)

    print()
    print('=== EVERY CUSTOMER-CONTROLLED VALUE THE THEME PRINTS ===')
    # The fields Shopify documents as untrusted: anything a shopper supplies.
    UNTRUSTED = [
        (r'\{\{-?\s*property\.(?:first|last)\s*\}\}', 'cart line property'),
        (r'\{\{-?\s*cart\.note\s*\}\}', 'cart note'),
        (r'\{\{-?\s*search\.terms\s*\}\}', 'search terms'),
        (r'\{\{-?\s*item\.key\s*\}\}', 'cart line key'),
        (r'\{\{-?\s*customer\.[\w.]+\s*\}\}', 'customer field'),
        (r'\{\{-?\s*[\w.]*attributes\[', 'cart attribute'),
    ]
    for root, _d, files in os.walk(THEME):
        for f in sorted(files):
            if not f.endswith('.liquid'):
                continue
            rel = os.path.relpath(os.path.join(root, f), THEME).replace(os.sep, '/')
            src = io.open(os.path.join(root, f), encoding='utf-8').read()
            src = re.sub(r'\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}', '',
                         src, flags=re.S)
            for pat, what in UNTRUSTED:
                for m in re.finditer(pat, src):
                    line_no = src[:m.start()].count('\n') + 1
                    check('%s:%d %s is escaped' % (rel, line_no, what), False,
                          m.group(0))

    if CHECKS[0] == 5:
        print('  no unescaped customer-controlled output anywhere in the theme')

    print()
    print('=== AND THE FILTER IS ACTUALLY THERE ===')
    li = io.open(os.path.join(THEME, 'snippets', 'cart-line-item.liquid'),
                 encoding='utf-8').read()
    nt = io.open(os.path.join(THEME, 'snippets', 'cart-note.liquid'),
                 encoding='utf-8').read()
    check('cart-line-item escapes both halves of the property',
          li.count('property.first | escape') == 1 and li.count('property.last | escape') == 1)
    check('cart-note escapes the note', 'cart.note | escape' in nt)

    print()
    print('%d checks, %d passed, %d failed'
          % (CHECKS[0], CHECKS[0] - len(FAILURES), len(FAILURES)))
    print('OVERALL: %s' % ('PASS' if not FAILURES else '*** FAILURES ABOVE ***'))
