# -*- coding: utf-8 -*-
"""Render layout/theme.liquid — the file nine phases never executed.

Every harness before this one rendered SECTIONS against a hand-written page
template, so the real layout was never run. That is exactly how Phase 10 found
two font_face calls emitting a bare @font-face rule into <head>: no face was
ever registered, and because a non-whitespace character token ends the HTML
"in head" insertion mode, the CSS text rendered as visible page content and
everything after it in source order was parsed in body context.

Nothing in the section harness could have caught that, because the section
harness never opened the file. This closes the gap.

The section bodies are stubbed — their contents are already measured by
respond.py, validate.py and the interaction suites. What is under test here is
the DOCUMENT: what lands in <head>, in what order, and whether the parser keeps
it there.
"""

import os
import sys
from html.parser import HTMLParser

# NB: build.py already wraps sys.stdout. Wrapping it a second time here closes
# build's wrapper and every later print raises on a closed file.
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build  # noqa: E402
import miniliquid  # noqa: E402

THEME = build.THEME

FAILURES = []
CHECKS = [0]


def check(label, ok, detail=''):
    CHECKS[0] += 1
    print('  %-62s %s %s' % (label, 'OK  ' if ok else '*** FAIL ***', '' if ok else detail))
    if not ok:
        FAILURES.append(label)


class HeadAudit(HTMLParser):
    """Where did the parser actually put things?

    The browser decides <head> is over at the first non-whitespace character
    token, so a raw CSS rule printed into the head silently relocates every
    element after it into <body>. This models that rule.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.zone = 'pre'
        self.head_tags = []
        self.body_tags = []
        self.stray_head_text = []
        self.style_depth = 0
        self.script_depth = 0
        # <title> legitimately CONTAINS text in the head. So does <textarea>.
        # Without tracking them the audit reports the page title as stray text.
        self.text_ok_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'head':
            self.zone = 'head'
            return
        if tag == 'body':
            self.zone = 'body'
            return
        if tag == 'style':
            self.style_depth += 1
        if tag == 'script':
            self.script_depth += 1
        if tag in ('title', 'textarea'):
            self.text_ok_depth += 1
        if self.zone == 'head':
            self.head_tags.append(tag)
        elif self.zone == 'body':
            # Only inside <body>. Anything before <head> — <html> itself — is
            # neither, and counting it as body made the skip-link check wrong.
            self.body_tags.append(tag)

    def handle_endtag(self, tag):
        if tag == 'head':
            self.zone = 'between'
        elif tag == 'body':
            self.zone = 'after'
        elif tag == 'style':
            self.style_depth = max(0, self.style_depth - 1)
        elif tag == 'script':
            self.script_depth = max(0, self.script_depth - 1)
        elif tag in ('title', 'textarea'):
            self.text_ok_depth = max(0, self.text_ok_depth - 1)

    def handle_data(self, data):
        if (self.zone == 'head' and self.style_depth == 0
                and self.script_depth == 0 and self.text_ok_depth == 0):
            if data.strip():
                self.stray_head_text.append(data.strip()[:90])


def render_layout(template='index', body='<!--SECTIONS-->'):
    engine = build.make_engine(cart=build.CART_EMPTY, template=template)
    engine.globals['content_for_layout'] = body
    engine.globals['content_for_header'] = (
        '<meta name="shopify-checkout-api-token" content="stub">')
    return engine.render_file('layout/theme.liquid')


if __name__ == '__main__':
    print('=== LAYOUT: layout/theme.liquid renders ===')
    try:
        html = render_layout()
        ok = True
    except Exception as exc:  # noqa: BLE001
        html = ''
        ok = False
        print('  RENDER FAILED: %s: %s' % (type(exc).__name__, exc))
    check('the layout renders without raising', ok)

    if html:
        out = os.path.join(HERE, 'layout-render.html')
        open(out, 'w', encoding='utf-8').write(html)
        print('  (written to %s)' % out)

        a = HeadAudit()
        a.feed(html)

        print()
        print('=== HEAD INTEGRITY ===')
        check('no raw text is emitted directly into <head>', not a.stray_head_text,
              str(a.stray_head_text))
        check('the Shopify head hook is present', 'shopify-checkout-api-token' in html)
        check('the content slot is present', '<!--SECTIONS-->' in html)
        check('no literal "#{" survives into the document', '#{' not in html)

        # Every @font-face rule must be inside a style element.
        outside = []
        pos = 0
        while True:
            k = html.find('@font-face', pos)
            if k < 0:
                break
            before = html[:k]
            if before.count('<style') <= before.count('</style>'):
                outside.append(html[k:k + 70].replace('\n', ' '))
            pos = k + 10
        check('every @font-face sits inside a <style> element', not outside, str(outside))

        print()
        print('=== HEAD CONTENTS (order matters) ===')
        for tag, label in (('title', 'a <title>'), ('meta', 'meta tags'), ('link', 'link tags'),
                           ('style', 'a <style>'), ('script', 'scripts')):
            check('<head> contains %s' % label, tag in a.head_tags,
                  'head=%s' % a.head_tags)

        stylesheets = html.count('rel="stylesheet"')
        # A SECTION legitimately links its own stylesheet from inside <body> —
        # that is how every Shopify theme, Dawn included, scopes section CSS.
        # What must never appear in the body is one of the LAYOUT's stylesheets.
        head_html = html.split('</head>')[0]
        layout_sheets = ['design-tokens.css', 'base.css', 'header.css',
                         'component-button.css', 'component-quantity.css',
                         'component-cart-line.css']
        stranded = [f for f in layout_sheets if f not in head_html]
        check("every layout stylesheet is inside <head>", not stranded, str(stranded))
        check('every stylesheet link resolved (>=6 expected)', stylesheets >= 6,
              'found %d' % stylesheets)

        # Assets referenced must exist on disk.
        import re
        missing = [m for m in re.findall(r'assets/([A-Za-z0-9._-]+\.(?:css|js))', html)
                   if not os.path.exists(os.path.join(THEME, 'assets', m))]
        check('every referenced asset exists in assets/', not missing, str(missing))

        print()
        print('=== BODY LANDMARKS ===')
        check('the skip link is the first thing in <body>',
              a.body_tags[:1] == ['a'], str(a.body_tags[:3]))
        check('<main> is in the body', 'main' in a.body_tags)
        check('the cart live region is present', 'CartStatus' in html)

        print()
        print('=== THE CART-PAGE GUARD ===')
        cart_html = render_layout(template='cart')
        check('the drawer is NOT rendered on the cart template',
              'data-cart-drawer' not in cart_html)
        check('the drawer IS rendered elsewhere', 'data-cart-drawer' in html)

    print()
    print('%d checks, %d passed, %d failed' % (CHECKS[0], CHECKS[0] - len(FAILURES), len(FAILURES)))
    print('OVERALL: %s' % ('PASS' if not FAILURES else '*** FAILURES ABOVE ***'))
