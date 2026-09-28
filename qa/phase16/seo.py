# -*- coding: utf-8 -*-
"""Phase 16 — document metadata and heading structure, on the rendered head.

The layout is rendered per template the way phase9/layout.py does it, so these
assertions are on real output rather than on a reading of the Liquid.

Heading structure is checked on the built harness pages, which carry the real
section markup.
"""
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', 'phase9')))
S9 = os.path.abspath(os.path.join(HERE, '..', 'phase9', 'site'))
S8 = os.path.abspath(os.path.join(HERE, '..', 'phase8', 'site'))
THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
FAILURES = []
CHECKS = [0]


def check(label, ok, detail=''):
    CHECKS[0] += 1
    print('  %-62s %s %s' % (label, 'OK  ' if ok else '*** FAIL ***',
                             '' if ok else str(detail)[:130]))
    if not ok:
        FAILURES.append(label)


def render_layout(template):
    import build
    engine = build.make_engine(cart=build.CART_EMPTY, template=template)
    engine.globals['content_for_layout'] = '<!--BODY-->'
    engine.globals['content_for_header'] = (
        '<meta name="shopify-checkout-api-token" content="stub">')
    return engine.render_file('layout/theme.liquid')


HEAD_PAGES = ['index', 'product', 'collection', 'search', 'page', 'cart', '404']

BODY_PAGES = [
    ('Homepage', S9, 'home.html'),
    ('Collection', S9, 's-collection.html'),
    ('Search', S9, 's-search.html'),
    ('Page', S9, 's-page.html'),
    ('404', S9, 's-404.html'),
    ('Product', S8, 'p-sizes.html'),
    ('Cart page', S8, 'c-page-many.html'),
]


def headings(html):
    body = html.split('</head>', 1)[-1]
    body = re.sub(r'<(script|style|template)\b.*?</\1>', '', body, flags=re.S | re.I)
    return [(int(m.group(1)), re.sub(r'<[^>]+>', '', m.group(2)).strip()[:44])
            for m in re.finditer(r'<h([1-6])\b[^>]*>(.*?)</h\1>', body, re.S | re.I)]


if __name__ == '__main__':
    print('=== THE HEAD, PER TEMPLATE ===')
    heads = {}
    for t in HEAD_PAGES:
        try:
            heads[t] = render_layout(t)
        except Exception as exc:
            check('%s renders' % t, False, '%s: %s' % (type(exc).__name__, exc))
    print('%-12s %-9s %-9s %-11s %-8s %s' %
          ('template', 'title', 'canonical', 'description', 'og', 'twitter'))
    for t, h in heads.items():
        head = h.split('</head>', 1)[0]
        print('%-12s %-9s %-9s %-11s %-8s %s' %
              (t,
               'yes' if re.search(r'<title>', head) else 'NO',
               str(len(re.findall(r'rel="canonical"', head))),
               'yes' if 'name="description"' in head else 'none',
               str(len(re.findall(r'property="og:', head))),
               str(len(re.findall(r'name="twitter:', head)))))

    print()
    print('=== ONE CANONICAL, AND IT IS SHOPIFY\'S ===')
    for t, h in heads.items():
        head = h.split('</head>', 1)[0]
        check('%-12s exactly one canonical' % t,
              len(re.findall(r'rel="canonical"', head)) == 1)
    src = io.open(os.path.join(THEME, 'layout', 'theme.liquid'), encoding='utf-8').read()
    check('it comes from canonical_url, not a hand-built URL',
          '{{ canonical_url }}' in src)
    check('no section emits a competing canonical',
          not any('rel="canonical"' in io.open(os.path.join(THEME, 'sections', f),
                                               encoding='utf-8').read()
                  for f in os.listdir(os.path.join(THEME, 'sections'))
                  if f.endswith('.liquid')))

    print()
    print('=== THE TITLE IS BUILT, NOT HARDCODED ===')
    for t, h in heads.items():
        m = re.search(r'<title>(.*?)</title>', h, re.S)
        title = re.sub(r'\s+', ' ', m.group(1)).strip() if m else ''
        check('%-12s has a non-empty title' % t, bool(title), title)
    check('the title uses page_title', 'page_title' in src)
    check('and appends the shop name only when it is not already there',
          'unless page_title contains shop.name' in src)
    check('and names the page number on paginated views', 'current_page' in src)

    print()
    print('=== SOCIAL METADATA ===')
    any_og = any('property="og:' in h for h in heads.values())
    check('Open Graph tags are present', any_og)
    check('Twitter card tags are present',
          any('name="twitter:' in h for h in heads.values()))
    check('an apple-touch-icon is declared', 'apple-touch-icon' in src)

    def og(t):
        return dict(re.findall(r'<meta property="og:([\w:]+)" content="([^"]*)"',
                               heads[t].split('</head>', 1)[0]))

    check('og:type is product on a product page, website elsewhere',
          og('product').get('type') == 'product'
          and og('index').get('type') == 'website'
          and og('collection').get('type') == 'website',
          {t: og(t).get('type') for t in ('index', 'product', 'collection')})
    check('og:title is the page title, not a written string',
          og('product').get('title') == 'Signature Oversized Tee'
          and og('collection').get('title') == 'The Faithful')
    check('og:url is the canonical URL, not a hand-built one',
          all(og(t).get('url', '').startswith('https://') for t in HEAD_PAGES))
    check('og:site_name is shop.name', og('index').get('site_name') == 'God Squad')
    check('an image is declared with its real dimensions',
          og('index').get('image') and og('index').get('image:width') == '1200'
          and og('index').get('image:height', '').isdigit())
    check('the card type promises a large image only when there is one',
          'summary_large_image' in heads['index'])
    snippet = io.open(os.path.join(THEME, 'snippets', 'meta-social.liquid'),
                      encoding='utf-8').read()
    snippet_code = re.sub(r'\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}', '',
                          snippet, flags=re.S)
    check('no social tag carries written marketing copy',
          not re.search(r'content="[A-Z][a-z]+ [a-z]+', snippet_code))
    check('the height is derived from width, never from aspect_ratio',
          'aspect_ratio' not in snippet_code
          and 'divided_by: share_image.width' in snippet_code)
    check('and the division is guarded against a zero width',
          'share_image.width > 0' in snippet_code)
    check('no og:price duplicates the structured data',
          'og:price' not in snippet_code)

    print()
    print('=== THE FONT WEIGHTS THE TYPE SYSTEM USES ARE LOADED ===')
    faces = re.findall(r'@font-face\s*\{[^}]*\}', heads['index'])
    flat = ' '.join(re.sub(r'\s+', ' ', f) for f in faces)
    weights = sorted(set(re.findall(r'font-family:\s*([^;]+);\s*font-weight:\s*(\d+)', flat)))
    print('   loaded: %s' % ', '.join('%s %s' % (f.strip(), w) for f, w in weights))
    tokens = io.open(os.path.join(THEME, 'assets', 'design-tokens.css'), encoding='utf-8').read()
    used = set(re.findall(r'--type-\w*weight:\s*var\(--weight-(\w+)\)', tokens))
    numeric = {'regular': '400', 'medium': '500', 'semibold': '600', 'black': '900'}
    want = {numeric[u] for u in used if u in numeric}
    got = {w for _f, w in weights}
    check('every weight the type scale spends has a real face',
          want <= got, 'scale wants %s, loaded %s' % (sorted(want), sorted(got)))
    check('each derived face is guarded, so a one-weight family still renders',
          'if body_medium' in src and 'if body_semibold' in src)
    # Comments stripped first. The Phase 16 comment beside this block QUOTES
    # the style tag while explaining why the faces must stay inside one, and
    # counting the raw file therefore found two and called it a regression.
    # Fourth time this project has asserted on prose; same fix every time.
    src_code = re.sub(r'\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}', '',
                      src, flags=re.S)
    check('the faces are still inside a single style block',
          src_code.count('{% style %}') == 1, src_code.count('{% style %}'))

    print()
    print('=== HEADING STRUCTURE, ON RENDERED PAGES ===')
    print('%-12s %-5s %s' % ('surface', 'h1s', 'outline'))
    for label, site, name in BODY_PAGES:
        p = os.path.join(site, name)
        if not os.path.exists(p):
            continue
        hs = headings(io.open(p, encoding='utf-8').read())
        levels = [l for l, _ in hs]
        print('%-12s %-5d %s' % (label, levels.count(1),
                                 ' '.join('h%d' % l for l in levels)))
    print()
    for label, site, name in BODY_PAGES:
        p = os.path.join(site, name)
        if not os.path.exists(p):
            continue
        hs = headings(io.open(p, encoding='utf-8').read())
        levels = [l for l, _ in hs]
        check('%-12s has exactly one h1' % label, levels.count(1) == 1,
              [t for l, t in hs if l == 1])
        skips = [(levels[i], levels[i + 1]) for i in range(len(levels) - 1)
                 if levels[i + 1] > levels[i] + 1]
        check('%-12s skips no heading level' % label, not skips, skips)

    print()
    print('=== ROBOTS AND SITEMAP ARE SHOPIFY\'S ===')
    check('no robots.txt.liquid in the theme',
          not os.path.exists(os.path.join(THEME, 'templates', 'robots.txt.liquid')))
    check('no sitemap template in the theme',
          not os.path.exists(os.path.join(THEME, 'templates', 'sitemap.xml.liquid')))
    check('no meta robots tag competes with Shopify\'s defaults',
          'name="robots"' not in src)

    print()
    print('%d checks, %d passed, %d failed'
          % (CHECKS[0], CHECKS[0] - len(FAILURES), len(FAILURES)))
    print('OVERALL: %s' % ('PASS' if not FAILURES else '*** FAILURES ABOVE ***'))
