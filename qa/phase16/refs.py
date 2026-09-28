# -*- coding: utf-8 -*-
"""Phase 16 — every reference the theme makes, resolved.

PARTS 42 and 43: broken assets and broken links. A reference that does not
resolve is a 404 in production, and the only way to be sure is to check all of
them rather than the ones someone thought to look at.

Covers: asset_url, render, section, JSON template "type", section-group "type",
translation keys used and translation keys defined, and literal internal hrefs.
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
THEME = os.environ.get('GS_THEME') or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')

FAILURES = []
CHECKS = [0]


def check(label, ok, detail=''):
    CHECKS[0] += 1
    print('  %-58s %s %s' % (label, 'OK  ' if ok else '*** FAIL ***',
                             '' if ok else str(detail)[:150]))
    if not ok:
        FAILURES.append(label)


def files(*exts):
    for root, _d, fs in os.walk(THEME):
        for f in sorted(fs):
            if f.endswith(exts):
                p = os.path.join(root, f)
                yield (os.path.relpath(p, THEME).replace(os.sep, '/'),
                       io.open(p, encoding='utf-8').read())


def strip_comments(t):
    t = re.sub(r'\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}', '', t, flags=re.S)
    # Inside a {% liquid %} block, `comment` is a bare statement with no
    # {% %} around it. Missing that form read a prose example of a filter
    # chain, inside a comment, as a real translation key. Phase 17 fixed the
    # same gap in its own scanner; this is the third one to need it.
    t = re.sub(r'(?m)^\s*comment\b.*?^\s*endcomment\b', '', t, flags=re.S)
    return re.sub(r'/\*.*?\*/', '', t, flags=re.S)


def flatten(d, prefix=''):
    out = set()
    for k, v in d.items():
        key = '%s.%s' % (prefix, k) if prefix else k
        if isinstance(v, dict):
            # A pluralisation group counts as its parent key.
            if set(v) & {'one', 'other', 'zero', 'few', 'many', 'two'}:
                out.add(key)
            out |= flatten(v, key)
        else:
            out.add(key)
    return out


if __name__ == '__main__':
    src = {rel: strip_comments(s) for rel, s in files('.liquid')}
    alljson = {rel: s for rel, s in files('.json')}
    everything = '\n'.join(src.values())

    print('=== ASSETS ===')
    refs = set()
    for rel, s in src.items():
        for m in re.finditer(r"'([\w.-]+\.(?:css|js|svg|png|jpg|webp|woff2?))'\s*\|\s*asset_url", s):
            refs.add(m.group(1))
        # AN ASSET NAME CAN REACH asset_url AS A PARAMETER, NOT ONLY AS A LITERAL.
        #
        # snippets/image-fallback.liquid renders `{{ file | asset_url }}`, and
        # its seven call sites pass the filename in: `{% render 'image-fallback',
        # file: 'hero.webp', ... %}`. The literal never sits beside asset_url, so
        # the pattern above could not see it and this check reported five
        # genuinely-used photographs as orphans.
        #
        # This is the third time in this project a scanner has been wrong by
        # assuming a name is written where it is used — the dead-code scan hit it
        # twice with Liquid-concatenated class names.
        #
        # And a parameter is not the only indirection. verse-index.liquid:211 and
        # words-we-wear.liquid:81 both build a LIST:
        #   assign fb_files = 'story.webp,tee.webp,hoodie.webp,cap.webp' | split: ','
        # so the name never appears next to a colon either. The reliable rule is
        # simpler than chasing each shape: any asset-shaped filename written
        # inside a quoted string in the theme's Liquid is a reference. It can
        # over-count — a filename mentioned only in prose would pass — but this
        # check exists to catch a file nothing uses, and the cost of a false
        # ORPHAN (deleting a photograph the theme draws) is far higher than the
        # cost of a false reference.
        # The lookbehind excludes a PATH. 'vendor/qrcode.js' in
        # templates/gift_card.liquid goes through shopify_asset_url — it is
        # Shopify's own copy of the QR generator and is not, and must not be, a
        # file in this theme's assets folder. Without this the broadened scan
        # reported qrcode.js as a missing asset_url target.
        for q in re.finditer(r"'([^']*)'", s):
            for m in re.finditer(r"(?<![\w/.-])([\w.-]+\.(?:css|js|svg|png|jpg|webp|woff2?))\b",
                                 q.group(1)):
                refs.add(m.group(1))
    missing = sorted(a for a in refs
                     if not os.path.exists(os.path.join(THEME, 'assets', a)))
    check('every asset_url reference exists (%d referenced)' % len(refs), not missing, missing)

    on_disk = {f for f in os.listdir(os.path.join(THEME, 'assets'))}
    orphans = sorted(f for f in on_disk if f not in refs)
    check('no asset file is shipped that nothing references', not orphans, orphans)

    print()
    print('=== SNIPPETS ===')
    # Two call forms, and missing the second reported a live snippet as an
    # orphan: inside a {% liquid %} block `render` is a bare STATEMENT with no
    # {% %} around it, which is how main-collection and main-search call
    # grid-sizes. Phase 13 learned the same thing about liquid-block lines.
    rendered = set(re.findall(r"\{%-?\s*(?:render|include)\s+'([\w.-]+)'", everything))
    rendered |= set(re.findall(r"(?m)^\s*(?:render|include)\s+'([\w.-]+)'", everything))
    snip_dir = os.path.join(THEME, 'snippets')
    missing = sorted(n for n in rendered
                     if not os.path.exists(os.path.join(snip_dir, n + '.liquid')))
    check('every rendered snippet exists (%d rendered)' % len(rendered), not missing, missing)
    have = {f[:-7] for f in os.listdir(snip_dir) if f.endswith('.liquid')}
    unused = sorted(have - rendered)
    check('no snippet is shipped that nothing renders', not unused, unused)

    print()
    print('=== SECTIONS ===')
    sec_dir = os.path.join(THEME, 'sections')
    wanted = set(re.findall(r"\{%-?\s*section\s+'([\w.-]+)'", everything))
    for rel, s in alljson.items():
        if rel.startswith('templates/') or rel.startswith('sections/'):
            try:
                doc = json.loads(s)
            except ValueError:
                continue
            for v in (doc.get('sections') or {}).values():
                if isinstance(v, dict) and 'type' in v:
                    wanted.add(v['type'])
    for rel, s in src.items():
        wanted |= set(re.findall(r"\{%-?\s*sections\s+'([\w.-]+)'", s))
    missing = sorted(n for n in wanted
                     if not (os.path.exists(os.path.join(sec_dir, n + '.liquid'))
                             or os.path.exists(os.path.join(sec_dir, n + '.json'))))
    check('every referenced section exists (%d referenced)' % len(wanted), not missing, missing)
    have = {f.rsplit('.', 1)[0] for f in os.listdir(sec_dir)}
    # cart-icon-bubble is a Section Rendering API target, reached by name at
    # runtime rather than by a template reference. Phase 8 documents this.
    unused = sorted(have - wanted - {'cart-icon-bubble'})
    check('no section is shipped that nothing references', not unused, unused)

    print()
    print('=== TRANSLATIONS ===')
    locale = json.load(io.open(os.path.join(THEME, 'locales', 'en.default.json'),
                               encoding='utf-8'))
    defined = flatten(locale)
    used = set(re.findall(r"'([a-z][\w.]*)'\s*\|\s*t\b", everything))
    used |= set(re.findall(r'"([a-z][\w.]*)"\s*\|\s*t\b', everything))
    missing = sorted(k for k in used if k not in defined)
    check('every translation key used is defined (%d used)' % len(used), not missing, missing)
    unused_keys = sorted(k for k in defined
                         if k not in used and not any(k.startswith(u + '.') for u in used))
    check('no translation key is defined that nothing uses', not unused_keys, unused_keys)

    print()
    print('=== INTERNAL LINKS ===')
    literal = set()
    for rel, s in src.items():
        for m in re.finditer(r'href="(/[\w/-]*)"', s):
            literal.add((rel, m.group(1)))
    # Only routes Shopify guarantees, or a path this theme has a template for.
    known = {'/', '/cart', '/search', '/account', '/collections/all'}
    unknown = sorted('%s -> %s' % (r, h) for r, h in literal if h not in known)
    check('every literal internal href is a route Shopify serves', not unknown, unknown)
    check('navigation destinations come from the merchant menu, not the theme',
          'linklists[' in everything)

    print()
    print('=== TEMPLATES SHOPIFY CAN ROUTE TO ===')
    tpl_dir = os.path.join(THEME, 'templates')
    have = {f.rsplit('.', 1)[0] for f in os.listdir(tpl_dir)}
    # Every storefront route Shopify serves. A missing one is an error page.
    expected = {'index', 'product', 'collection', 'search', 'page', 'cart', '404',
                'list-collections', 'blog', 'article', 'password', 'gift_card'}
    print('  present: %s' % ', '.join(sorted(have)))
    print('  missing: %s' % (', '.join(sorted(expected - have)) or 'none'))
    print('  Each missing one serves Shopify\'s error page to anyone who reaches')
    print('  its URL. Phase 1 SHOP-09 tracks the same list.')

    print()
    print('%d checks, %d passed, %d failed'
          % (CHECKS[0], CHECKS[0] - len(FAILURES), len(FAILURES)))
    print('OVERALL: %s' % ('PASS' if not FAILURES else '*** REVIEW ABOVE ***'))
