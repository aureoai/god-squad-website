# -*- coding: utf-8 -*-
"""Phase 16 — page weight and request count, per surface, measured.

WHAT THIS IS AND IS NOT.

It is a real count of what each rendered page asks for and what those bytes
weigh, taken from the actual Liquid output and the actual files on disk. Every
number here is measured.

It is NOT a Core Web Vitals measurement. There is no Shopify server in this
environment, so TTFB, FCP and real LCP timings do not exist to be measured and
are not reported. Image bytes are the harness's placeholder files, not the
merchant's photography, so image weight is reported as COUNT and declared size
rather than as bytes — inventing a kilobyte figure for a photograph nobody has
uploaded would be exactly the fabricated metric the brief forbids.
"""
import gzip
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, '..', 'phase9', 'site'))
SITE8 = os.path.abspath(os.path.join(HERE, '..', 'phase8', 'site'))
THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
# The five surfaces the brief names, plus the two the cart lives on.
PAGES = [
    ('Homepage', SITE, 'home.html'),
    ('Collection', SITE, 's-collection.html'),
    ('Collection + filters', SITE, 's-collection-filters.html'),
    ('Product', SITE8, 'p-sizes.html'),
    ('Cart page', SITE8, 'c-page-many.html'),
    ('Search', SITE, 's-search.html'),
    ('404', SITE, 's-404.html'),
]


def gz(b):
    return len(gzip.compress(b, 9))


def asset_bytes(name):
    p = os.path.join(THEME, 'assets', name)
    if not os.path.exists(p):
        return None
    return io.open(p, 'rb').read()


def measure(path):
    html = io.open(path, encoding='utf-8').read()
    raw_html = html.encode('utf-8')

    css = re.findall(r'<link[^>]+rel="stylesheet"[^>]+href="[^"]*?([\w.-]+\.css)"', html)
    js = re.findall(r'<script[^>]+src="[^"]*?([\w.-]+\.js)"', html)
    imgs = re.findall(r'<img\b', html)
    svgs = re.findall(r'<svg\b', html)
    inline_js = re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', html, re.S)

    css_u = list(dict.fromkeys(css))
    js_u = list(dict.fromkeys(js))

    css_raw = css_gz = 0
    for n in css_u:
        b = asset_bytes(n)
        if b:
            css_raw += len(b)
            css_gz += gz(b)
    js_raw = js_gz = 0
    for n in js_u:
        b = asset_bytes(n)
        if b:
            js_raw += len(b)
            js_gz += gz(b)

    return {
        'html_raw': len(raw_html), 'html_gz': gz(raw_html),
        'css_files': len(css_u), 'css_dupes': len(css) - len(css_u),
        'css_raw': css_raw, 'css_gz': css_gz,
        'js_files': len(js_u), 'js_dupes': len(js) - len(js_u),
        'js_raw': js_raw, 'js_gz': js_gz,
        'imgs': len(imgs), 'svgs': len(svgs),
        'inline_js': len(inline_js),
        'inline_js_bytes': sum(len(s.encode('utf-8')) for s in inline_js),
        'requests': 1 + len(css_u) + len(js_u) + len(imgs),
        'css_list': css_u, 'js_list': js_u,
    }


def strip_js_comments(text):
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    text = re.sub(r'(?m)^\s*//.*$', '', text)
    return '\n'.join(l for l in text.splitlines() if l.strip())


if __name__ == '__main__':
    print('=== PAGE WEIGHT AND REQUEST COUNT (measured) ===')
    print()
    print('%-22s %7s %7s %7s %7s %7s %7s %5s %5s %5s' %
          ('surface', 'reqs', 'htmlGz', 'cssN', 'cssGz', 'jsN', 'jsGz', 'img', 'svg', 'dupe'))
    rows = []
    for label, site, name in PAGES:
        p = os.path.join(site, name)
        if not os.path.exists(p):
            print('%-22s  (not built)' % label)
            continue
        m = measure(p)
        rows.append((label, m))
        print('%-22s %7d %7d %7d %7d %7d %7d %5d %5d %5d' %
              (label, m['requests'], m['html_gz'], m['css_files'], m['css_gz'],
               m['js_files'], m['js_gz'], m['imgs'], m['svgs'],
               m['css_dupes'] + m['js_dupes']))

    print()
    print('  reqs   = 1 document + stylesheets + scripts + <img>. Inline SVG icons cost')
    print('           no request, which is why the icon set is inline snippets.')
    print('  htmlGz = the document itself, gzipped.')
    print('  dupe   = the same URL requested twice on one page. Must be 0.')
    print()
    print('  NOT MEASURED HERE, because this environment has no Shopify server:')
    print('    TTFB, FCP, and real LCP/INP timings. Reported as unavailable rather')
    print('    than estimated. Image BYTES are the merchant photography, which does')
    print('    not exist yet (Phase 3 recorded sourcing as the ceiling).')

    print()
    print('=== WORST-CASE PAGE ===')
    if rows:
        worst = max(rows, key=lambda r: r[1]['css_gz'] + r[1]['js_gz'])
        w = worst[1]
        print('  %s: %d requests, %.1f KB gz of CSS + JS' %
              (worst[0], w['requests'], (w['css_gz'] + w['js_gz']) / 1024.0))
        print('    css:', ', '.join(w['css_list']))
        print('    js: ', ', '.join(w['js_list']))

    print()
    print('=== THE THEME CHECK AssetSizeJavaScript OFFENSE, QUANTIFIED ===')
    print('  Shopify\'s threshold is 10,000 bytes compressed per page-load script.')
    print()
    print('  %-16s %9s %9s %9s %9s' % ('file', 'raw', 'gzip', 'no-comment', 'gz'))
    for n in ('cart.js', 'header.js', 'product.js', 'facets.js'):
        b = asset_bytes(n)
        stripped = strip_js_comments(b.decode('utf-8')).encode('utf-8')
        flag = '  <-- over' if gz(b) > 10000 else ''
        print('  %-16s %9d %9d %9d %9d%s' %
              (n, len(b), gz(b), len(stripped), gz(stripped), flag))
    print()
    print('  The "no-comment" columns are diagnostic only. This theme ships its')
    print('  reasoning in its comments and has no build step, so stripping them is')
    print('  not a change that can be made without losing the thing that makes the')
    print('  code maintainable. The column exists to answer one question: is the')
    print('  threshold reachable by deleting prose alone, or only by restructuring?')
