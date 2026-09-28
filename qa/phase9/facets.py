# -*- coding: utf-8 -*-
"""Phase 13 — collection filtering, rendered against every filter state.

The fixtures cover what Shopify actually returns:
  FILTERS_NONE        no filters configured in the admin app at all
  FILTERS_ALL         list x2, boolean, price_range — every type the API has
  FILTERS_ACTIVE      the same, with values applied and a price floor set
  FILTERS_DEGENERATE  a one-value group, which is not a choice
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build  # noqa: E402
import surfaces  # noqa: E402
from miniliquid import wrap  # noqa: E402

THEME = build.THEME
FAILURES = []
CHECKS = [0]


def check(label, ok, detail=''):
    CHECKS[0] += 1
    print('  %-62s %s %s' % (label, 'OK  ' if ok else '*** FAIL ***',
                             '' if ok else str(detail)[:150]))
    if not ok:
        FAILURES.append(label)


def render(filters, settings=None, products=None, design_mode=False):
    coll = dict(surfaces.COLL)
    coll['filters'] = filters
    if products is not None:
        coll['products'] = products
        coll['products_count'] = len(products)
    e = surfaces.engine(template='collection', collection=wrap(coll))
    e.globals['request'] = wrap({'design_mode': design_mode,
                                 'locale': {'iso_code': 'en'}, 'path': '/collections/the-faithful'})
    base, _ = surfaces.schema_defaults('main-collection')
    if settings:
        base.update(settings)
    return build.render_section(e, 'sections/main-collection.liquid', 'coll', base)


def groups(html):
    """Real <details> groups, not the .facets__groups wrapper."""
    return len(re.findall(r'class="facets__group"', html))


if __name__ == '__main__':
    print('=== NOTHING RENDERS UNTIL A MERCHANT CONFIGURES FILTERS ===')
    none = render(build.FILTERS_NONE)
    check('no filter panel at all', 'class="facets"' not in none)
    check('no Filter button', 'data-facets-toggle' not in none)
    check('no active-filter row', 'facets-active' not in none)
    check('the sort control is untouched', 'data-collection-sort' in none)
    ed = render(build.FILTERS_NONE, design_mode=True)
    check('the Theme Editor explains why it is empty',
          'Search &amp; Discovery' in ed or 'Search & Discovery' in ed)
    check('the live storefront says nothing',
          'Search &amp; Discovery' not in none and 'Search & Discovery' not in none)

    print()
    print('=== EVERY FILTER TYPE RENDERS ITS OWN CONTROL ===')
    h = render(build.FILTERS_ALL)
    check('a filter panel renders', 'class="facets"' in h)
    check('four groups, one per filter', groups(h) == 4, 'got %d' % groups(h))
    check('list values are checkboxes', 'type="checkbox"' in h)
    check('a swatch filter renders its swatch', 'facets__swatch' in h)
    check('price renders two number inputs',
          h.count('facets__price-input') == 2)
    check('price uses Shopify\'s own parameters',
          'filter.v.price.gte' in h and 'filter.v.price.lte' in h)
    check('availability uses Shopify\'s own parameter', 'filter.v.availability' in h)
    check('option filters use Shopify\'s own parameters',
          'filter.v.option.size' in h and 'filter.v.option.color' in h)
    check('counts come from Shopify, not from counting', 'facets__count' in h)

    print()
    print('=== A ONE-VALUE GROUP IS NOT A CHOICE ===')
    d = render(build.FILTERS_DEGENERATE)
    check('the single-value group is dropped', groups(d) == 1, 'got %d' % groups(d))
    check('and it is the Vendor group that went', 'Vendor' not in d)
    check('the real group stayed', 'Size' in d)

    print()
    print('=== ONE FORM: SORT AND FILTERS SUBMIT TOGETHER ===')
    form_ids = re.findall(r'<form[^>]*id="([^"]+)"', h)
    check('exactly one form on the surface', len(form_ids) == 1, 'forms=%s' % form_ids)
    fid = form_ids[0] if form_ids else ''
    bound = len(re.findall(r'form="%s"' % re.escape(fid), h))
    check('every facet control is bound to it by the form attribute',
          bound >= 10, 'bound=%d' % bound)
    check('the sort select is inside that same form', 'name="sort_by"' in h)
    # The decisive one: filters must survive when sorting is switched OFF.
    nosort = render(build.FILTERS_ALL, {'show_sorting': False})
    check('the form still exists when sorting is off', '<form' in nosort)
    check('and the facets are still bound to it',
          re.search(r'form="[^"]+"', nosort) is not None)
    check('with no sort control inside it', 'name="sort_by"' not in nosort)
    # And no page parameter, so any submission returns to page 1.
    check('the form carries no page parameter', 'name="page"' not in h)

    print()
    print('=== ACTIVE FILTERS ARE REMOVABLE LINKS ===')
    a = render(build.FILTERS_ACTIVE)
    chips = re.findall(r'<a class="facets-active__chip" href="([^"]+)"', a)
    check('one chip per applied value', len(chips) == 4, 'chips=%d' % len(chips))
    check('each chip is Shopify\'s own url_to_remove',
          all(c.startswith('/collections/') for c in chips), chips[:2])
    check('Clear all is a link, not a form control',
          'facets-active__clear' in a and 'href=' in a)
    check('the applied set is named for a screen reader',
          'Applied filters' in a)
    check('an applied group is open so what is applied is visible',
          '<details class="facets__group" open' in a or 'facets__group"\n            open' in a
          or re.search(r'class="facets__group"\s+open', a) is not None)
    check('the Filter button shows how many are applied',
          'main-collection__filter-count' in a)

    print()
    print('=== NO JAVASCRIPT IS REQUIRED ===')
    check('the drawer trigger ships hidden, for script to reveal',
          re.search(r'data-facets-toggle[^>]*hidden', a) is not None
          or re.search(r'hidden[^>]*data-facets-toggle', a) is not None)
    check('the panel itself is not hidden', not re.search(r'class="facets"[^>]*hidden', a))
    check('every value is a real form control or a real link',
          'role="button"' not in a and 'javascript:' not in a)

    print()
    print('=== A FILTERED COLLECTION THAT MATCHES NOTHING ===')
    empty_filtered = render(build.FILTERS_ACTIVE, products=[])
    empty_plain = render(build.FILTERS_NONE, products=[])
    check('filtered-empty says the FILTERS matched nothing',
          'No pieces match these filters' in empty_filtered)
    check('and offers to clear them', 'collection.filters.clear_all' not in empty_filtered
          and 'Clear all' in empty_filtered)
    check('an unfiltered empty collection keeps its own words',
          'This collection is empty' in empty_plain
          and 'No pieces match' not in empty_plain)
    check('neither invents a product', 'product-card__link' not in empty_filtered
          and 'product-card__link' not in empty_plain)

    print()
    print('=== NOTHING IS HARDCODED ===')
    raw = open(os.path.join(THEME, 'snippets', 'facets.liquid'), encoding='utf-8').read()
    # Comments explain the mechanism and quote parameter names to do it. Strip
    # them: what matters is what the CODE emits, not what the prose describes.
    src = re.sub(r'\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}', '', raw, flags=re.S)
    for bad, what in ((r'>\s*(XS|XXL|Small|Medium|Large)\s*<', 'hardcoded sizes'),
                      (r'>\s*(Black|White|Gold)\s*<', 'hardcoded colours'),
                      ('₱', 'a hardcoded currency symbol'),
                      ('filter.v.option', 'a hardcoded option parameter')):
        check('the code contains no %s' % what,
              re.search(bad, src) is None if bad.startswith('>') else bad not in src)
    # The two price fallbacks ARE literal, and legitimately so: they are the
    # parameter names Shopify documents, used only when min_value/max_value is
    # nil because the customer has set no bound yet.
    check('the only literal parameters are the documented price bounds',
          src.count('filter.v.price.gte') == 1 and src.count('filter.v.price.lte') == 1)
    check('every label comes from Shopify or the locale file',
          'f.label' in src and "| t" in src)

    print()
    print('=== HEADER SEARCH: an upgrade of a working link ===')
    e = surfaces.engine(template='index')
    hdr = build.render_section(e, 'sections/header.liquid', 'header',
                               dict(build.HEADER_SETTINGS))
    check('the trigger is still a link to the search route',
          re.search(r'<a[^>]*href="/search"[^>]*data-search-trigger', hdr) is not None)
    check('it is not a button, which would do nothing without script',
          re.search(r'<button[^>]*data-search-trigger', hdr) is None)
    check('a real search form is present', 'role="search"' in hdr)
    check('with a real input named q', re.search(r'<input[^>]*name="q"', hdr) is not None)
    check('the input has a label', 'for="HeaderSearchInput"' in hdr)
    check('the panel ships hidden', re.search(r'data-search-panel[^>]*hidden', hdr) is not None)
    check('no ARIA claim is printed before script can honour it',
          'aria-haspopup' not in hdr and 'aria-expanded="false" aria-controls="HeaderSearch"' not in hdr)
    js = open(os.path.join(THEME, 'assets', 'header.js'), encoding='utf-8').read()
    check('script applies the disclosure ARIA at upgrade', 'aria-haspopup' in js)
    check('Escape closes it', 'Escape' in js and 'closeSearch' in js)
    check('a modified click still opens the search page',
          'metaKey' in js and js.count('metaKey') >= 1)
    check('its bindings are released by the header teardown',
          'activeSearchTrap' in js and 'activeSearchClose' in js)
    check('the search type matches what the search template configures',
          'name="type" value="product"' in hdr)

    print()
    print('=== THE DRAWER FOLLOWS THE MENU, NOT THE CART ===')
    fjs_raw = open(os.path.join(THEME, 'assets', 'facets.js'), encoding='utf-8').read()
    # Comments describe what the cart does differently, quoting its API to do
    # it. Strip them: the claim is about what this file EXECUTES.
    fjs = re.sub(r'/\*.*?\*/', '', fjs_raw, flags=re.S)
    fjs = re.sub(r'(?m)//.*$', '', fjs)
    check('it locks with a class, which composes',
          "classList.add('facets-open')" in fjs)
    check("it does NOT take the cart inline fixed-position lock",
          'body.style.position' not in fjs)
    fcss = open(os.path.join(THEME, 'assets', 'component-facets.css'), encoding='utf-8').read()
    check('and the class is what hides the overflow', '.facets-open body' in fcss)
    check('the drawer positioning is opt-in, applied by script',
          '.facets--drawer' in fcss and "classList.add('facets--drawer')" in fjs)
    check('init is idempotent per element', '__gsFacetsInit' in fjs)
    check('it releases on section unload', 'shopify:section:unload' in fjs)

    print()
    print('%d checks, %d passed, %d failed'
          % (CHECKS[0], CHECKS[0] - len(FAILURES), len(FAILURES)))
    print('OVERALL: %s' % ('PASS' if not FAILURES else '*** FAILURES ABOVE ***'))
