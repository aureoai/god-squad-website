# -*- coding: utf-8 -*-
"""Phase 12 — the catalog surfaces, rendered against every product shape.

The fixture set covers the whole matrix without inventing anything:
  P_SIZES   4 images, 4 media, size options
  P_MULTI   2 images, 3 media, colour swatches
  P_SOLDOUT 1 image,  unavailable
  P_SINGLE  1 image,  one variant
  P_RULE    1 image,  a quantity rule
  P_LONG    0 images, a long title
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
                             '' if ok else str(detail)[:140]))
    if not ok:
        FAILURES.append(label)


def card(product, theme=None, **kw):
    """Render product-card.liquid on its own, as every grid does."""
    e = surfaces.engine(template='collection')
    if theme:
        merged = dict(e.globals['settings'])
        merged.update(theme)
        e.globals['settings'] = wrap(merged)
    scope = {'product': product}
    scope.update(kw)
    src = open(os.path.join(THEME, 'snippets', 'product-card.liquid'), encoding='utf-8').read()
    return e.render(src, scope)


def render_section(section, overrides=None, **globals_):
    base, _ = surfaces.schema_defaults(section)
    if overrides:
        base.update(overrides)
    e = surfaces.engine(template='product', **globals_)
    return build.render_section(e, 'sections/%s.liquid' % section, 'x', base)


def secondaries(html):
    return html.count('product-card__image--secondary')


if __name__ == '__main__':
    ON = {'card_hover_secondary_image': True}
    OFF = {'card_hover_secondary_image': False}

    print('=== SECONDARY IMAGE: only where one genuinely exists ===')
    cases = [
        ('P_SIZES   (4 images)', build.P_SIZES, 1),
        ('P_MULTI   (2 images)', build.P_MULTI, 1),
        ('P_SOLDOUT (1 image)', build.P_SOLDOUT, 0),
        ('P_SINGLE  (1 image)', build.P_SINGLE, 0),
        ('P_RULE    (1 image)', build.P_RULE, 0),
        ('P_LONG    (0 images)', build.P_LONG, 0),
    ]
    for label, prod, expected in cases:
        n = secondaries(card(prod, theme=ON))
        check('%s -> %d secondary' % (label, expected), n == expected, 'got %d' % n)

    print()
    print('=== IT IS NOT THE SAME PICTURE AS THE PRIMARY ===')
    h = card(build.P_MULTI, theme=ON)
    # No escape hatch: a regex that matches nothing must FAIL, not pass. The
    # point of this assertion is that the secondary is a different picture from
    # the primary — if it silently re-rendered the featured image the swap would
    # look like a no-op and every other check here would still be green.
    imgs = re.findall(r'<img[^>]*class="(product-card__image[^"]*)"[^>]*src="([^"]+)"', h)
    srcs = [src for _cls, src in imgs]
    check('both card images were found in the markup', len(imgs) == 2, 'found %d' % len(imgs))
    check('the secondary is a DIFFERENT picture from the primary',
          len(set(srcs)) == 2, 'srcs=%s' % srcs)
    check('the secondary is lazy, never an LCP candidate',
          re.search(r'product-card__image--secondary[^>]*loading="lazy"', h)
          or re.search(r'loading="lazy"[^>]*product-card__image--secondary', h))
    check('the secondary is decorative (empty alt)', 'alt=""' in h)

    print()
    print('=== OFF BY DEFAULT: the approved Phase 2 hover is unchanged ===')
    for label, prod, _ in cases:
        n = secondaries(card(prod, theme=OFF))
        check('%s renders none when off' % label, n == 0, 'got %d' % n)
    g = json.load(open(os.path.join(THEME, 'config', 'settings_schema.json'), encoding='utf-8'))
    prods = next(x for x in g if x.get('name') == 'Products')
    setting = next((s for s in prods['settings'] if s.get('id') == 'card_hover_secondary_image'), None)
    check('the setting exists and defaults to off',
          setting is not None and setting.get('default') is False)

    print()
    print('=== NO HOVER DEPENDENCY ON TOUCH ===')
    css = open(os.path.join(THEME, 'assets', 'component-product-card.css'), encoding='utf-8').read()
    m = re.search(r'\.product-card__image--secondary \{(.*?)\}', css, re.S)
    check('it is hidden in the base (non-hover) rules', m and 'opacity: 0' in m.group(1))
    reveal = re.search(r'@media \(hover: hover\) and \(pointer: fine\) \{[^@]*?opacity: 1;', css, re.S)
    check('it is revealed only inside a hover-capable query', bool(reveal))
    check('it is laid over the primary, so nothing shifts',
          m and 'position: absolute' in m.group(1) and 'inset: 0' in m.group(1))

    print()
    print('=== THE CARD STILL ANSWERS THE OTHER PHASE 12 ITEMS ===')
    sold = card(build.P_SOLDOUT, theme=OFF)
    check('a sold-out card still links to the product', 'product-card__link' in sold)
    check('a sold-out card is marked, in text not colour alone',
          'product-card__badge' in sold and 'visually-hidden' in sold)
    check('a sold-out card offers no add-to-cart', 'cart/add' not in sold)
    sale = card(build.P_MULTI, theme=OFF)
    check('a compare-at price renders when one exists',
          'compare' in sale.lower() or '<s' in sale)
    check('no hardcoded currency symbol in the card source',
          '₱' not in open(os.path.join(THEME, 'snippets', 'product-card.liquid'),
                               encoding='utf-8').read())
    check('the title is a real heading', re.search(r'<h[1-6][^>]*product-card__title', sale) is not None)
    check('one anchor per card, no nested link',
          sale.count('<a ') == sale.count('product-card__link'),
          'anchors=%d links=%d' % (sale.count('<a '), sale.count('product-card__link')))

    print()
    print('=== SKU: the row must be reachable for a LATER variant ===')
    # P_SIZES' first variant has no SKU; its second does. Gated on the
    # render-time variant, the markup was absent and product.js's
    # [data-variant-sku] hook could never be filled.
    pp = render_section('main-product', {'show_sku': True}, product=build.P_SIZES)
    check('the row renders even though the FIRST variant has no SKU',
          'data-variant-sku' in pp)
    check('it starts hidden, so no labelled row stands over an empty value',
          'data-variant-sku-row' in pp and 'hidden' in pp)
    js = open(os.path.join(THEME, 'assets', 'product.js'), encoding='utf-8').read()
    check('product.js shows and hides it on variant change',
          'updateSkuRow' in js and js.count('updateSkuRow') >= 2)
    none_sku = render_section('main-product', {'show_sku': True}, product=build.P_LONG)
    check('a product where NO variant has a SKU renders no row',
          'data-variant-sku' not in none_sku)

    print()
    print('=== ADD TO CART: Unavailable is not Sold out ===')
    check('the button carries a third, Unavailable label',
          'data-label-unavailable' in pp)
    check('product.js distinguishes a missing variant from a sold-out one',
          'data-label-unavailable' in js)

    print()
    print('=== QUICK ADD: the cart script can see it ===')
    qa = card(build.P_SINGLE, theme=OFF, quick_add=True)
    check('the form marks its button for the cart script', 'data-add-to-cart' in qa)
    check('it has a label node for the busy state', 'data-add-to-cart-label' in qa)
    # Phase 14 corrected the attribute. This test passed on the NAME being
    # present and never on the name being one assets/cart.js reads: the card
    # carried data-cart-error, which showFormError does not look for and
    # showCartError wrote unrelated cart failures into. So the box existed, the
    # test was green, and a failed quick add still showed the customer nothing.
    # The assertion now names the function that has to find it.
    check('it has somewhere to show a failure', 'data-product-error' in qa)
    js_cart = open(os.path.join(THEME, 'assets', 'cart.js'), encoding='utf-8').read()
    check('and that is the attribute the add path actually reads',
          "form.querySelector('[data-product-error]" in js_cart)
    cart_js = open(os.path.join(THEME, 'assets', 'cart.js'), encoding='utf-8').read()
    check('those are the hooks cart.js actually reads',
          'data-label-busy' in cart_js and 'data-cart-error' in cart_js)
    qa_multi = card(build.P_MULTI, theme=OFF, quick_add=True)
    check('a multi-variant product still gets a LINK, never a silent add',
          'cart/add' not in qa_multi and 'product-card__link' in qa_multi)

    print()
    print('=== COLLECTION: empty means the SET is empty, not the page ===')
    src = open(os.path.join(THEME, 'sections', 'main-collection.liquid'),
               encoding='utf-8').read()
    check('the empty branch tests paginate.items',
          'if paginate.items > 0' in src)
    check('it no longer tests the page slice',
          'if collection.products.size > 0' not in src)

    print()
    print('=== LOW STOCK: only where the data actually supports it ===')

    def stocked(mgmt, policy, qty, available=True):
        """P_SINGLE with one variant's inventory fields set, as Shopify sets them."""
        p = dict(build.P_SINGLE)
        v = dict(p['variants'][0])
        v.update({'inventory_management': mgmt, 'inventory_policy': policy,
                  'inventory_quantity': qty, 'available': available})
        p['variants'] = [wrap(v)]
        p['selected_or_first_available_variant'] = wrap(v)
        p['available'] = available
        return wrap(p)

    def low_shown(product, threshold):
        html = render_section('main-product', {'low_stock_threshold': threshold},
                              product=product)
        m = re.search(r'<p[^>]*data-low-stock[^>]*>', html)
        if not m:
            return None
        return 'hidden' not in m.group(0)

    matrix = [
        ('tracked, cannot oversell, 2 left, threshold 3', stocked('shopify', 'deny', 2), 3, True),
        ('tracked, cannot oversell, 10 left, threshold 3', stocked('shopify', 'deny', 10), 3, False),
        ('NOT tracked by Shopify, 2 left', stocked('', 'deny', 2), 3, False),
        ('continue-selling (never runs out), 2 left', stocked('shopify', 'continue', 2), 3, False),
        ('tracked, 2 left, but threshold 0', stocked('shopify', 'deny', 2), 0, False),
        ('tracked, 0 left and unavailable', stocked('shopify', 'deny', 0, False), 3, False),
    ]
    for label, product, threshold, expected in matrix:
        got = low_shown(product, threshold)
        check('%-46s -> %s' % (label, 'LOW' if expected else 'silent'),
              got is expected, 'got %r' % got)

    pl = render_section('main-product', {'low_stock_threshold': 3},
                        product=stocked('shopify', 'deny', 2))
    check('the line says Low stock, never a number',
          'Low stock' in pl and not re.search(r'data-low-stock[^>]*>[^<]*\d', pl))
    check('no inventory figure reaches the page at all',
          'inventory_quantity' not in pl and '"low_stock"' in pl)
    check('the variant table carries a boolean, not a count',
          re.search(r'"low_stock":\s*(true|false)', pl) is not None)
    js = open(os.path.join(THEME, 'assets', 'product.js'), encoding='utf-8').read()
    check('product.js updates it on variant change',
          'updateLowStock' in js and js.count('updateLowStock') >= 2)

    # The owner set this to 3. Asserted in BOTH places it can come from: the
    # schema default governs a section added fresh in the Theme Editor, the
    # template governs the shipped product page.
    mp = json.loads(re.search(
        r'\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}',
        open(os.path.join(THEME, 'sections', 'main-product.liquid'),
             encoding='utf-8').read(), re.S).group(1))
    thr = next((x for x in mp['settings'] if x.get('id') == 'low_stock_threshold'), None)
    check('the schema default threshold is 3', thr and thr.get('default') == 3,
          'default=%r' % (thr or {}).get('default'))
    tmpl = json.load(open(os.path.join(THEME, 'templates', 'product.json'), encoding='utf-8'))
    check('the shipped product template sets it to 3',
          tmpl['sections']['main']['settings'].get('low_stock_threshold') == 3)
    # And it must actually fire at 3 without being passed explicitly.
    shipped = render_section('main-product', None, product=stocked('shopify', 'deny', 3))
    mline = re.search(r'<p[^>]*data-low-stock[^>]*>', shipped)
    check('a tracked variant with 3 left shows the line on defaults alone',
          mline and 'hidden' not in mline.group(0))
    above = render_section('main-product', None, product=stocked('shopify', 'deny', 4))
    mline2 = re.search(r'<p[^>]*data-low-stock[^>]*>', above)
    check('with 4 left it stays silent', mline2 and 'hidden' in mline2.group(0))

    print()
    print('%d checks, %d passed, %d failed'
          % (CHECKS[0], CHECKS[0] - len(FAILURES), len(FAILURES)))
    print('OVERALL: %s' % ('PASS' if not FAILURES else '*** FAILURES ABOVE ***'))
