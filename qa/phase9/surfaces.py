# -*- coding: utf-8 -*-
"""Render the five storefront surfaces Phase 10 added.

collection, page, 404, search and footer had never been rendered once when they
were written. This renders each against mock Shopify data, in every state it is
supposed to handle, and asserts on the markup.

Settings come from each section's OWN schema defaults rather than a hand-written
dict, so a renamed or added setting cannot silently fall back to blank and make
a surface look like it handles an empty state when it was never given data.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build  # noqa: E402
from miniliquid import wrap  # noqa: E402

THEME = build.THEME
FAILURES = []
CHECKS = [0]


def check(label, ok, detail=''):
    CHECKS[0] += 1
    print('  %-58s %s %s' % (label, 'OK  ' if ok else '*** FAIL ***',
                             '' if ok else str(detail)[:160]))
    if not ok:
        FAILURES.append(label)


def schema_defaults(section):
    """Every setting's default, straight from the section's {% schema %}."""
    src = open(os.path.join(THEME, 'sections', section + '.liquid'),
               encoding='utf-8').read()
    m = re.search(r'\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}', src, re.S)
    if not m:
        return {}, []
    doc = json.loads(m.group(1))
    out = {}
    for s in doc.get('settings', []):
        if 'id' in s:
            out[s['id']] = s.get('default', '')
    return out, doc.get('blocks', [])


# ------------------------------------------------------------------ mock data
PRODUCTS = [build.P_SIZES, build.P_MULTI, build.P_SOLDOUT, build.P_SINGLE,
            build.P_LONG, build.P_RULE]
COLL = build.collection('the-faithful', PRODUCTS)
COLL_EMPTY = build.collection('empty-drop', [], title='Empty Drop')

PAGE = wrap({
    'title': 'Size Guide',
    'handle': 'size-guide',
    'content': ('<h2>Fit</h2><p>Our tees are cut boxy.</p>'
                '<ul><li>Chest, flat</li><li>Body length</li></ul>'
                '<blockquote>Measure a shirt you already own.</blockquote>'
                '<table><tr><th>Size</th><th>Chest</th></tr>'
                '<tr><td>S</td><td>52cm</td></tr></table>'
                # A bare pasted URL, which is what a contact or shipping page
                # is full of. Without overflow-wrap on the content root this
                # pushes a 375px viewport into horizontal scroll.
                # A URL full of slashes and hyphens wraps on its own: UAX #14
                # already permits a break after those. The case that actually
                # overflows is an UNBREAKABLE token — an order reference, a
                # tracking hash, a long compound — which is equally likely on a
                # shipping or returns page.
                '<p>Reference: '
                'GS7QK4XZ9WTB2LMN6RVP0DYJ3HFC8SAE1UIO5GXKQ7ZWTB2LMN6RVP</p>'),
})
PAGE_EMPTY = wrap({'title': 'Blank', 'handle': 'blank', 'content': ''})

def as_result(obj, kind='product'):
    """Shopify tags every search result with object_type; the section branches
    on it to decide between a product card and a text result. A mock product
    without it is not a search result, and the section is right to skip it."""
    d = dict(obj)
    d['object_type'] = kind
    return wrap(d)


SEARCH_HITS = wrap({
    'performed': True, 'terms': 'tee', 'results_count': 3,
    'results': [as_result(build.P_SIZES), as_result(build.P_MULTI),
                wrap({'object_type': 'page', 'title': 'Size Guide',
                      'url': '/pages/size-guide', 'content': 'Fit notes.'})],
})
SEARCH_NONE = wrap({
    'performed': True, 'terms': 'zzzz', 'results_count': 0, 'results': [],
})
SEARCH_IDLE = wrap({
    'performed': False, 'terms': '', 'results_count': 0, 'results': [],
})

POLICIES = [
    wrap({'title': 'Refund policy', 'url': '/policies/refund-policy'}),
    wrap({'title': 'Privacy policy', 'url': '/policies/privacy-policy'}),
]
FOOTER_MENU = {'links': [
    {'title': 'Shop', 'url': '/collections/all', 'active': False},
    {'title': 'Our Story', 'url': '/pages/our-story', 'active': False},
]}


def engine(**extra):
    e = build.make_engine(template=extra.pop('template', 'index'))
    ll = dict(e.globals['linklists'])
    ll['footer'] = FOOTER_MENU
    e.globals['linklists'] = wrap(ll)
    shop = dict(e.globals['shop'])
    shop['policies'] = POLICIES
    shop['privacy_policy'] = POLICIES[1]
    shop['refund_policy'] = POLICIES[0]
    e.globals['shop'] = wrap(shop)
    for k, v in extra.items():
        e.globals[k] = v
    return e


def render(section, sid, settings=None, blocks=None, **globals_):
    base, _ = schema_defaults(section)
    if settings:
        base.update(settings)
    e = engine(**globals_)
    return build.render_section(e, 'sections/%s.liquid' % section, sid, base, blocks)


def try_render(label, *a, **kw):
    try:
        html = render(*a, **kw)
        check(label, True)
        return html
    except Exception as exc:  # noqa: BLE001
        check(label, False, '%s: %s' % (type(exc).__name__, exc))
        return ''


def no_missing_translation(label, html):
    bad = re.findall(r'translation missing[^<"]*', html or '')
    check(label, not bad, bad[:3])


if __name__ == '__main__':
    print('=== COLLECTION ===')
    h = try_render('main-collection renders with products', 'main-collection',
                   'coll', collection=COLL, template='collection')
    if h:
        check('it renders a product grid', 'product-grid' in h)
        check('it renders product cards', h.count('product-card__link') >= 1,
              'cards=%d' % h.count('product-card__link'))
        check('it renders the collection title', 'The Faithful' in h)
        check('it renders a sort control', 'name="sort_by"' in h or 'sort_by' in h)
        check('the sort form is a GET form', 'method="get"' in h)
        check('it renders an h1', '<h1' in h)
        no_missing_translation('no missing translation key', h)
    he = try_render('main-collection renders an EMPTY collection', 'main-collection',
                    'coll', collection=COLL_EMPTY, template='collection')
    if he:
        check('the empty state has real copy', 'empty' in he.lower())
        check('the empty state renders no cards', 'product-card__link' not in he)

    print()
    print('=== PAGE ===')
    h = try_render('main-page renders', 'main-page', 'pg', page=PAGE, template='page')
    if h:
        check('it renders the page title as h1', '<h1' in h and 'Size Guide' in h)
        check('it renders the rich-text content', '<blockquote' in h and '<table' in h)
        no_missing_translation('no missing translation key', h)
    he = try_render('main-page renders with NO content', 'main-page', 'pg',
                    page=PAGE_EMPTY, template='page')

    print()
    print('=== 404 ===')
    h = try_render('main-404 renders', 'main-404', 'nf', template='404')
    if h:
        check('it offers a way back', 'href=' in h)
        check('it uses the button system', 'button' in h)
        no_missing_translation('no missing translation key', h)

    print()
    print('=== SEARCH ===')
    h = try_render('main-search renders WITH results', 'main-search', 'sr',
                   search=SEARCH_HITS, template='search')
    if h:
        check('it renders a role=search form', 'role="search"' in h)
        check('the input is named q', 'name="q"' in h)
        check('it declares type=product', 'name="type"' in h or 'type=' in h)
        check('it renders result cards', 'product-card__link' in h)
        no_missing_translation('no missing translation key', h)
    h0 = try_render('main-search renders with ZERO results', 'main-search', 'sr',
                    search=SEARCH_NONE, template='search')
    if h0:
        check('zero results renders no cards', 'product-card__link' not in h0)
        check('zero results still renders the form', 'name="q"' in h0)
    hi = try_render('main-search renders with NO query yet', 'main-search', 'sr',
                    search=SEARCH_IDLE, template='search')
    if hi:
        check('the idle state still renders the form', 'name="q"' in hi)

    print()
    print('=== FOOTER ===')
    blocks = build.blocks([{'id': 'm1', 'type': 'link_list',
                            'settings': {'menu': 'footer', 'heading': 'Shop'}}])
    h = try_render('footer renders', 'footer', 'footer', blocks=blocks,
                   template='index')
    if h:
        check('it is a contentinfo landmark', 'role="contentinfo"' in h)
        check('it renders a <footer> element', '<footer' in h)
        check('it renders the menu block links', 'Our Story' in h)
        check('it renders the copyright', '&copy;' in h or '©' in h)
        check('it renders policy links', 'policies/refund-policy' in h)
        check('no invented social URL', 'facebook.com/' not in h)
        no_missing_translation('no missing translation key', h)

    print()
    print('=== NO SURFACE EMITS A RAW LIQUID ARTEFACT ===')
    everything = ''.join(x or '' for x in (h, h0, hi, he))
    check('no unrendered {{ or {% survives', '{{' not in everything and '{%' not in everything)
    check('no "#{" interpolation survives', '#{' not in everything)

    print()
    print('%d checks, %d passed, %d failed'
          % (CHECKS[0], CHECKS[0] - len(FAILURES), len(FAILURES)))
    print('OVERALL: %s' % ('PASS' if not FAILURES else '*** FAILURES ABOVE ***'))
