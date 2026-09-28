# -*- coding: utf-8 -*-
"""GOD SQUAD — run the whole site locally and click through it.

    python serve-site.py            then open http://127.0.0.1:8000

The QA harness renders each surface to its own file — home.html, s-collection.html,
p-sizes.html — but the pages link to each other with REAL SHOPIFY ROUTES, because
that is what the theme emits: /products/signature-tee, /collections/all, /cart,
/search. On a plain static server every one of those 404s, so the site looks
right and cannot be walked.

This maps those routes onto the fixtures, so the site behaves like a site: click
a product card and you land on a product page, click the cart and you get the
cart, use the nav and it goes somewhere.

WHAT IS REAL HERE AND WHAT IS NOT.

Real: every page is the theme's own Liquid, rendered. The CSS and JavaScript are
the theme's. Layout, typography, colour, spacing, responsive behaviour, the
drawer, the filter UI, the variant picker, focus order — all real, all worth
judging.

Not real: the ROUTING. Shopify decides which product a URL resolves to; this maps
each handle to whichever fixture best demonstrates that kind of product. So
`/products/signature-tee` always shows the size-variant fixture, and the price on
the card you clicked may not match the price on the page you land on. The
fixtures were built to exercise the theme, not to be a consistent catalogue.

Not real either: anything needing Shopify. Add-to-cart, quantity changes, search
queries and filtering all post to endpoints that do not exist. They will fail —
and how they fail is worth watching, because failing gracefully is a feature.

Unmapped routes fall through to the theme's own 404 page, which is correct
behaviour and also worth a look.
"""
import io
import os
import posixpath
import re
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, 'phase9', 'site')
PORT = int(os.environ.get('GS_PORT', '8000'))

# Shopify route -> the fixture that best demonstrates it.
ROUTES = {
    '/': 'home.html',
    # '/collections' omitted on purpose -- no list-collections.json in the theme,
    # so on a live store this route serves an error page. See build-preview.py.
    '/collections/all': 's-collection.html',
    '/collections/the-faithful': 's-collection.html',
    '/collections/new-drop': 's-collection.html',
    '/collections/best-sellers': 's-collection.html',
    '/collections/empty': 's-collection-empty.html',
    '/search': 's-search.html',
    '/cart': 'c-page-many.html',
    '/account': 's-404.html',          # accounts are Shopify-hosted; no template ships
    '/pages/our-story': 's-page.html',
    '/pages/size-guide': 's-page.html',
    '/policies/refund-policy': 's-page.html',
    '/policies/privacy-policy': 's-page.html',
    '/policies/terms-of-service': 's-page.html',
    '/policies/shipping-policy': 's-page.html',
    # Each handle goes to the fixture that shows that KIND of product.
    '/products/signature-tee': 'p-sizes.html',        # size variants
    '/products/heavyweight-hoodie': 'p-multi.html',   # colour + size
    '/products/sold-out-crew': 'p-soldout.html',      # unavailable
    '/products/utility-cap': 'p-single.html',         # one image
    '/products/bundle': 'p-details.html',             # description disclosure
    '/products/long': 'p-long.html',                  # long copy
    '/products/faith-crew': 'p-soldout.html',
    '/products/three-pack': 'p-details.html',
}

# Extra surfaces reachable only by typing the URL, listed on the index banner.
EXTRA = [
    ('/collections/all?filters=1', 's-collection-filters.html', 'collection with filters'),
    ('/search?empty=1', 's-search-none.html', 'search, no results'),
    ('/cart?empty=1', 'c-page-empty.html', 'empty cart'),
    ('/cart?note=1', 'c-page-note.html', 'cart with an order note'),
    ('/404', 's-404.html', 'the 404 page'),
]

QUERY_OVERRIDES = {
    ('/collections/all', 'filters'): 's-collection-filters.html',
    ('/search', 'empty'): 's-search-none.html',
    ('/cart', 'empty'): 'c-page-empty.html',
    ('/cart', 'note'): 'c-page-note.html',
}

BANNER = """
<div id="gs-devbar" style="position:fixed;left:0;right:0;bottom:0;z-index:2147483647;
  background:#141310;color:#F3EFE6;border-top:1px solid rgba(243,239,230,.18);
  font:12px/1.5 ui-monospace,Menlo,Consolas,monospace;padding:7px 12px;
  display:flex;gap:14px;align-items:center;flex-wrap:wrap">
  <b style="color:#D8C08A;letter-spacing:.08em">LOCAL PREVIEW</b>
  <span style="opacity:.62">%(route)s &rarr; %(file)s</span>
  <span style="margin-left:auto;display:flex;gap:10px;flex-wrap:wrap">
    <a href="/" style="color:#F3EFE6">home</a>
    <a href="/collections/all" style="color:#F3EFE6">collection</a>
    <a href="/collections/all?filters=1" style="color:#F3EFE6">+filters</a>
    <a href="/products/signature-tee" style="color:#F3EFE6">product</a>
    <a href="/products/heavyweight-hoodie" style="color:#F3EFE6">variants</a>
    <a href="/products/sold-out-crew" style="color:#F3EFE6">sold out</a>
    <a href="/cart" style="color:#F3EFE6">cart</a>
    <a href="/cart?empty=1" style="color:#F3EFE6">empty cart</a>
    <a href="/search" style="color:#F3EFE6">search</a>
    <a href="/search?empty=1" style="color:#F3EFE6">no results</a>
    <a href="/pages/our-story" style="color:#F3EFE6">page</a>
    <a href="/404" style="color:#F3EFE6">404</a>
    <a href="#" onclick="document.getElementById('gs-devbar').remove();return false"
       style="color:#D8C08A">hide</a>
  </span>
</div>
"""


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=SITE, **kw)

    def log_message(self, fmt, *args):
        code = args[1] if len(args) > 1 else ''
        path = getattr(self, '_gs_route', self.path)
        target = getattr(self, '_gs_file', '')
        if target:
            print('  %-34s -> %-28s %s' % (path[:34], target, code))
        elif not path.startswith(('/assets', '/img')):
            print('  %-34s    %s' % (path[:34], code))

    def resolve(self, path, qs):
        clean = posixpath.normpath(path)
        if clean in ROUTES or clean == '/':
            base = ROUTES.get(clean, 'home.html')
            for (p, key), f in QUERY_OVERRIDES.items():
                if p == clean and key in qs:
                    return f
            return base
        # /products/<anything-else> still shows a product rather than a 404.
        if clean.startswith('/products/'):
            return 'p-sizes.html'
        if clean.startswith('/collections/'):
            return 's-collection.html'
        if clean.startswith('/pages/') or clean.startswith('/policies/'):
            return 's-page.html'
        return None

    def do_GET(self):
        u = urlparse(self.path)
        qs = parse_qs(u.query)
        self._gs_route = self.path

        # Real files (assets, img, and the fixture pages themselves) pass through.
        candidate = os.path.join(SITE, u.path.lstrip('/').replace('/', os.sep))
        if u.path != '/' and os.path.isfile(candidate):
            self._gs_file = ''
            return super().do_GET()

        target = self.resolve(u.path, qs)
        # An unmapped route serves the theme's 404 page AND answers 404. Serving
        # a not-found page with a 200 is the mistake that makes every soft-404
        # bug invisible, and Phase 16's SEO work would not forgive it here.
        status = 200
        if target is None:
            target, status = 's-404.html', 404
        self._gs_file = target

        full = os.path.join(SITE, target)
        if not os.path.isfile(full):
            self.send_error(404, 'fixture missing: %s' % target)
            return

        html = io.open(full, encoding='utf-8', errors='replace').read()
        banner = BANNER % {'route': u.path + (('?' + u.query) if u.query else ''),
                           'file': target}
        if '</body>' in html:
            html = html.replace('</body>', banner + '</body>', 1)
        else:
            html += banner
        body = html.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        """Shopify's endpoints. Answer honestly instead of hanging."""
        self.send_response(404)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"description":"No Shopify backend in local preview.",'
                         b'"message":"Not Found","status":404}')


if __name__ == '__main__':
    if not os.path.isdir(SITE):
        raise SystemExit('harness not built: %s\nRun: cd phase9 && python home.py' % SITE)
    missing = sorted({f for f in list(ROUTES.values()) + [e[1] for e in EXTRA]
                      if not os.path.isfile(os.path.join(SITE, f))})
    print('=' * 72)
    print('GOD SQUAD — local site preview')
    print('=' * 72)
    print('  serving : %s' % SITE)
    print('  open    : http://127.0.0.1:%d' % PORT)
    if missing:
        print('  MISSING FIXTURES (those routes will 404): %s' % ', '.join(missing))
    print()
    print('  Routes you can click or type:')
    seen = set()
    for route, f in ROUTES.items():
        if f in seen and route != '/':
            continue
        seen.add(f)
        print('    %-32s -> %s' % (route, f))
    for route, f, desc in EXTRA:
        print('    %-32s -> %-22s %s' % (route, f, desc))
    print()
    print('  Add-to-cart and friends will FAIL: there is no Shopify here. Watch')
    print('  HOW they fail — a readable message and no stuck spinner is the test.')
    print('  Unmapped routes show the theme\'s own 404 page.')
    print()
    print('  Ctrl+C to stop.')
    print('=' * 72)
    print()
    ThreadingHTTPServer(('127.0.0.1', PORT), Handler).serve_forever()
