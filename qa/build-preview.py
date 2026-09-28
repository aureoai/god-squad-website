# -*- coding: utf-8 -*-
"""Build preview-site/ — the whole website as files you can double-click.

    python build-preview.py

The QA harness renders each surface to its own page, but those pages link to
each other with REAL SHOPIFY ROUTES — /products/signature-tee, /collections/all,
/cart — because that is what the theme emits. Opened from disk, every one of
those is a dead link, so the site looks right and cannot be walked.

This copies the pages into preview-site/ and rewrites those routes to point at
the local files, so the result needs no server, no Python and no terminal: open
preview-site/index.html and click.

WHAT IS REAL: every page is the theme's own Liquid, rendered, with the theme's
own CSS and JavaScript. Layout, typography, colour, spacing, responsive
behaviour, the drawer, the filter UI, the variant picker and focus order are all
the real thing and worth judging.

WHAT IS NOT: the routing. Shopify decides which product a URL resolves to; this
maps each handle to whichever fixture best demonstrates that kind of product, so
the price on a card may not match the page it opens. The fixtures exercise the
theme; they are not a consistent catalogue.

WHAT WILL FAIL: anything needing Shopify — add to cart, quantity changes, search,
filtering, checkout. Watch HOW they fail; a readable message and no stuck spinner
is the thing being tested.

Re-run this after changing the theme. It rebuilds the harness first.
"""
import io
import os
import re
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
QA = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(QA)
SRC = os.path.join(QA, 'phase9', 'site')
OUT = os.path.join(PROJECT, 'preview-site')

# fixture in phase9/site  ->  (output filename, label for the nav bar)
PAGES = [
    ('home.html',                 'index.html',             'Home'),
    ('s-collection.html',         'collection.html',        'Collection'),
    ('s-collection-filters.html', 'collection-filters.html', 'Collection + filters'),
    ('s-collection-empty.html',   'collection-empty.html',  'Collection, empty'),
    ('p-sizes.html',              'product.html',           'Product'),
    ('p-multi.html',              'product-variants.html',  'Product, colour + size'),
    ('p-details.html',            'product-details.html',   'Product, description'),
    ('p-soldout.html',            'product-soldout.html',   'Product, sold out'),
    ('p-long.html',               'product-long.html',      'Product, long copy'),
    ('p-single.html',             'product-one-image.html', 'Product, one image'),
    ('c-page-many.html',          'cart.html',              'Cart'),
    ('c-page-empty.html',         'cart-empty.html',        'Cart, empty'),
    ('c-page-note.html',          'cart-note.html',         'Cart + order note'),
    ('c-many.html',               'cart-drawer.html',       'Cart drawer'),
    ('s-search.html',             'search.html',            'Search'),
    ('s-search-none.html',        'search-none.html',       'Search, no results'),
    ('s-page.html',               'page.html',              'Content page'),
    ('s-404.html',                '404.html',               '404'),
]

# Shopify route -> local file. Longest keys are replaced first.
ROUTES = {
    '/products/signature-tee': 'product.html',
    '/products/heavyweight-hoodie': 'product-variants.html',
    '/products/sold-out-crew': 'product-soldout.html',
    '/products/utility-cap': 'product-one-image.html',
    '/products/bundle': 'product-details.html',
    '/products/long': 'product-long.html',
    '/collections/the-faithful': 'collection.html',
    '/collections/all': 'collection.html',
    # '/collections' IS DELIBERATELY ABSENT. It is Shopify's collection LIST
    # page and needs templates/list-collections.json, which this theme does not
    # ship. Mapping it here to the collection grid made a route that leads to an
    # error page on a live store look like a working one, and that is precisely
    # why Shop and Collections appeared identical in the preview. Anything still
    # pointing at it now falls through to 404.html, which is the truth.
    '/policies/refund-policy': 'page.html',
    '/policies/privacy-policy': 'page.html',
    '/pages/our-story': 'page.html',
    '/pages/size-guide': 'page.html',
    '/search': 'search.html',
    '/account': '404.html',
    '/cart': 'cart.html',
    '/': 'index.html',
}

# THE PREVIEW HAD NO FONTS AT ALL, AND NOBODY NOTICED FOR NINETEEN PHASES.
#
# On a real store, layout/theme.liquid calls `font_face` and Shopify serves
# Playfair Display and Jost from its own CDN. The harness does not run Liquid's
# font_face, so the rendered pages loaded ZERO webfaces and silently fell back
# to Georgia and Helvetica.
#
# It hid because getComputedStyle().fontFamily reports the DECLARED stack, not
# the family actually drawn — it says "Playfair Display" whether or not Playfair
# exists. document.fonts.check() also returns true. The only reliable test is to
# measure the width of identical text in the named font and in its fallback: on
# this machine both came out at exactly 845.6px and 850px, so neither font was
# present and every screenshot taken all project was Georgia and Arial.
#
# Both faces are Google Fonts under the SIL Open Font Licence, so the preview
# can load the real ones. The weights match what the theme registers: Playfair
# 900, and Jost 400/500/600 (theme.liquid registers 500 and 600 via font_modify).
FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    'family=Jost:wght@400;500;600&family=Playfair+Display:wght@900&display=swap">'
)

BAR = """
<nav id="gs-nav" aria-label="Preview navigation" style="position:fixed;left:0;right:0;bottom:0;
 z-index:2147483647;background:#141310;border-top:1px solid rgba(243,239,230,.18);
 font:11.5px/1.5 ui-monospace,Menlo,Consolas,monospace;padding:6px 10px;display:flex;
 gap:9px;align-items:center;flex-wrap:wrap;color:#F3EFE6">
<b style="color:#D8C08A;letter-spacing:.07em;white-space:nowrap">PREVIEW</b>
%(links)s
<a href="#" onclick="document.getElementById('gs-nav').remove();return false"
   style="color:#D8C08A;margin-left:auto">hide</a>
</nav>
"""


def retitle(html, label):
    """Give the page the title the THEME would give it.

    layout/theme.liquid builds `<title>` from `page_title`, plus the tag, the
    page number and the shop name. The harness does not run that layout — it
    hardcodes "God Squad — Phase 8 harness" into every fixture, so all eighteen
    preview pages carried the same developer-facing string. Harmless in a test
    rig; wrong in anything anyone looks at, and every browser tab said "Phase 8
    harness".

    The page's own <h1> is the closest thing the fixture has to `page_title`, so
    the title is derived from it and falls back to the page's label. The en dash
    and the trailing shop name match what theme.liquid emits.
    """
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    name = re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else label
    name = re.sub(r'\s+', ' ', name)
    title = 'GOD SQUAD – Faith-Driven Philippine Streetwear' \
        if label == 'Home' else '%s – GOD SQUAD' % name
    return re.sub(r'<title>.*?</title>', '<title>%s</title>' % title, html,
                  count=1, flags=re.S)


def rewrite(html, here):
    """Point every internal Shopify route at its local file."""
    for route in sorted(ROUTES, key=len, reverse=True):
        target = ROUTES[route]
        # href="/cart"  href="/cart?x=1"  href="/products/foo?variant=1"
        html = re.sub(r'href="%s(\?[^"]*)?"' % re.escape(route),
                      'href="%s"' % target, html)
    # "/#story" and "/#verse" are the nav's links to sections OF THE HOMEPAGE.
    # They are not routes and must keep their fragment, or Our Story and Verse
    # stop being reachable from anywhere but the homepage itself.
    html = re.sub(r'href="/#([\w-]+)"', r'href="index.html#\1"', html)
    # /cart/change?id=… and anything else left over: neutralise rather than 404.
    html = re.sub(r'href="/cart/[^"]*"', 'href="cart.html"', html)
    html = re.sub(r'href="/[^"#][^"]*"', 'href="404.html"', html)
    # action="/…" would navigate away from the folder on submit.
    html = re.sub(r'action="/[^"]*"', 'action="#"', html)
    return html


if __name__ == '__main__':
    print('[1/3] Rebuilding the harness from the theme ...')
    for s in ('phase9/build.py', 'phase9/surfacepages.py', 'phase9/home.py'):
        d, f = s.split('/')
        r = subprocess.run([sys.executable, f], cwd=os.path.join(QA, d),
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print('      %-26s %s' % (s, 'ok' if r.returncode == 0 else '*** FAILED ***'))
        if r.returncode:
            print(r.stdout.decode('utf-8', 'replace')[-500:])
            raise SystemExit(1)

    print()
    print('[2/3] Writing preview-site/ ...')
    # Clear the CONTENTS rather than the directory. OneDrive holds a handle on
    # the folder while it syncs, so rmtree on preview-site/ itself fails with
    # WinError 32 — and a build step that dies because a cloud client happened
    # to be looking at the folder is a build step nobody will trust.
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    for e in os.listdir(OUT):
        p = os.path.join(OUT, e)
        try:
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
        except OSError as exc:
            print('      (could not remove %s: %s)' % (e, exc))
    for sub in ('assets', 'img'):
        s = os.path.join(SRC, sub)
        if os.path.isdir(s):
            shutil.copytree(s, os.path.join(OUT, sub))

    links = ' '.join(
        '<a href="%s" style="color:#F3EFE6;white-space:nowrap">%s</a>' % (out, label)
        for _src, out, label in PAGES)
    bar = BAR % {'links': links}

    written = missing = 0
    for src, out, label in PAGES:
        p = os.path.join(SRC, src)
        if not os.path.isfile(p):
            print('      --  %-26s source missing (%s)' % (out, src))
            missing += 1
            continue
        html = io.open(p, encoding='utf-8', errors='replace').read()
        html = rewrite(html, out)
        html = retitle(html, label)
        # The real typefaces, into <head> before the theme's own stylesheets so
        # the faces are being fetched while the CSS parses.
        if '</head>' in html:
            html = html.replace('</head>', FONTS + '</head>', 1)
        else:
            html = FONTS + html
        if '</body>' in html:
            html = html.replace('</body>', bar + '</body>', 1)
        else:
            html += bar
        io.open(os.path.join(OUT, out), 'w', encoding='utf-8').write(html)
        written += 1
        print('      ok  %-26s <- %s' % (out, src))

    print()
    print('[3/3] Verifying every link resolves ...')
    broken = []
    files = {f for f in os.listdir(OUT)}
    for f in sorted(files):
        if not f.endswith('.html'):
            continue
        t = io.open(os.path.join(OUT, f), encoding='utf-8', errors='replace').read()
        for m in re.finditer(r'href="([^"#][^"]*)"', t):
            h = m.group(1).split('?')[0].split('#')[0]
            if h.startswith(('http:', 'https:', 'mailto:', 'tel:', 'data:')):
                continue
            if h.startswith('assets/') or h.startswith('img/'):
                if not os.path.exists(os.path.join(OUT, h.replace('/', os.sep))):
                    broken.append((f, h))
            elif h and h not in files:
                broken.append((f, h))
    if broken:
        print('      *** %d broken link(s):' % len(broken))
        seen = set()
        for f, h in broken:
            if h in seen:
                continue
            seen.add(h)
            print('          %-24s -> %s' % (f, h))
    else:
        print('      every internal link resolves.')

    print()
    print('=' * 68)
    print('  %d pages written, %d missing' % (written, missing))
    print('  OPEN: %s' % os.path.join(OUT, 'index.html'))
    print('  No server, no Python, nothing to start — just double-click it.')
    print('=' * 68)
