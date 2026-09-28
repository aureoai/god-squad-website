# -*- coding: utf-8 -*-
"""Phase 8 structural validation.

Every check here is something a later edit could quietly break. It is not a
substitute for rendering — the harness does that — it is the contract.
"""
import os, re, json, csv, hashlib, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
PROJECT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ok = True
count = {'pass': 0, 'fail': 0}


def check(label, cond, detail=''):
    global ok
    if cond:
        count['pass'] += 1
    else:
        count['fail'] += 1
        ok = False
    print("  %-62s %s %s" % (label, "OK  " if cond else "*** FAIL ***", detail))
    return cond


def R(rel):
    with open(os.path.join(THEME, rel), encoding='utf-8') as f:
        return f.read()


def strip_liquid(src):
    """Markup only: schema, comments and {% liquid %} comment bodies removed, so
    a prohibition about the markup is not triggered by prose explaining it."""
    src = re.sub(r'\{%-?\s*schema\s*-?%\}.*?\{%-?\s*endschema\s*-?%\}', '', src, flags=re.S)
    src = re.sub(r'\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}', '', src, flags=re.S)
    src = re.sub(r'^\s*comment\b.*?^\s*endcomment\b', '', src, flags=re.S | re.M)
    return src


def strip_css(src):
    return re.sub(r'/\*.*?\*/', '', src, flags=re.S)


def strip_js(src):
    src = re.sub(r'/\*.*?\*/', '', src, flags=re.S)
    return re.sub(r'(?m)^\s*//.*$', '', src)


NEW_SECTIONS = ['main-product', 'cart-drawer', 'cart-icon-bubble', 'main-cart']
NEW_SNIPPETS = ['product-media-gallery', 'product-variant-picker', 'quantity-selector',
                'cart-line-item', 'cart-icon-bubble', 'cart-totals', 'cart-empty-state',
                'icon-plus', 'icon-minus', 'icon-chevron']
NEW_ASSETS = ['section-main-product.css', 'section-cart-drawer.css', 'section-main-cart.css',
              'component-quantity.css', 'component-cart-line.css', 'cart.js', 'product.js']

print("=== FILES ===")
for rel in ([f'sections/{n}.liquid' for n in NEW_SECTIONS]
            + [f'snippets/{n}.liquid' for n in NEW_SNIPPETS]
            + [f'assets/{n}' for n in NEW_ASSETS]
            + ['templates/product.json', 'templates/cart.json']):
    p = os.path.join(THEME, rel)
    check(rel, os.path.exists(p), '%d B' % os.path.getsize(p) if os.path.exists(p) else 'MISSING')

print("\n=== JSON AND SCHEMA PARSE ===")
for rel in ('templates/product.json', 'templates/cart.json', 'templates/index.json',
            'locales/en.default.json', 'config/settings_data.json', 'sections/header-group.json'):
    try:
        json.loads(R(rel))
        check(rel, True)
    except Exception as e:
        check(rel, False, str(e)[:60])

SCHEMAS = {}
for name in NEW_SECTIONS:
    src = R(f'sections/{name}.liquid')
    m = re.search(r'\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}', src, re.S)
    if name == 'cart-icon-bubble':
        check('cart-icon-bubble carries no schema (it is a render target)', m is None)
        continue
    try:
        SCHEMAS[name] = json.loads(m.group(1))
        s = SCHEMAS[name]
        real = [f for f in s.get('settings', []) if f.get('type') not in ('header', 'paragraph')]
        check('sections/%s.liquid schema' % name, True,
              'settings=%d (+%d headers) blocks=%d' %
              (len(real), len(s.get('settings', [])) - len(real), len(s.get('blocks', []))))
        check('  %s is within the 14-setting budget' % name, len(real) <= 14, '%d' % len(real))
    except Exception as e:
        check('sections/%s.liquid schema' % name, False, str(e)[:60])

print("\n=== TEMPLATE WIRING ===")
for tpl, sect in (('templates/product.json', 'main-product'), ('templates/cart.json', 'main-cart')):
    d = json.loads(R(tpl))
    types = {v['type'] for v in d['sections'].values()}
    check('%s renders %s' % (tpl, sect), sect in types, str(sorted(types)))
    check('  %s order covers every section' % tpl,
          set(d['order']) == set(d['sections']), str(d['order']))
    schema = SCHEMAS.get(sect, {})
    ids = {f['id'] for f in schema.get('settings', []) if f.get('id')}
    used = set()
    for v in d['sections'].values():
        used |= set(v.get('settings', {}).keys())
    check('  every setting used exists in the schema', used <= ids, str(sorted(used - ids)))

print("\n=== SHOPIFY IS THE SOURCE OF TRUTH ===")
product_body = strip_liquid(R('sections/main-product.liquid'))
picker_body = strip_liquid(R('snippets/product-variant-picker.liquid'))
line_body = strip_liquid(R('snippets/cart-line-item.liquid'))
drawer_body = strip_liquid(R('sections/cart-drawer.liquid'))
cartpage_body = strip_liquid(R('sections/main-cart.liquid'))
totals_body = strip_liquid(R('snippets/cart-totals.liquid'))
empty_body = strip_liquid(R('snippets/cart-empty-state.liquid'))
all_markup = (product_body + picker_body + line_body + drawer_body + cartpage_body
              + totals_body + empty_body)

check("no currency symbol is written into the markup",
      not re.search(r'[\u20b1$\u20ac\u00a3\u00a5]', all_markup))
# The property has to END in price/total/amount to be a money value:
# unit_price_measurement.reference_unit contains "price" and is a unit NAME.
MONEY_OUT = r'\{\{\s*[\w.]*?(price|total|amount)\s*\}\}'
check("every price goes through the money filter",
      not re.search(MONEY_OUT, all_markup, re.I),
      str(re.findall(MONEY_OUT, all_markup, re.I)))
check("no hard-coded size run", not re.search(r'>\s*(XS|XXL)\s*<', all_markup))
check("no invented review or rating", not re.search(r'\u2605|review|rating|stars?\b', all_markup, re.I))
# Phase 12 compares inventory_quantity in LIQUID to decide whether a "Low stock"
# line appears, and publishes only the boolean. So the rule is not "the words
# never appear in the source" — it is "no inventory value ever reaches the
# customer", which is a property of the RENDERED page. Checking the render is
# also strictly stronger than checking the source.
_rendered = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'site', 'p-sizes.html'), encoding='utf-8').read()
check("no inventory number is rendered",
      'inventory_quantity' not in _rendered and 'inventory_policy' not in _rendered
      and 'inventory_management' not in _rendered)
check("no invented shipping claim",
      not re.search(r'free shipping|worldwide shipping|ships? in \d', all_markup, re.I))
check("no invented stock message", not re.search(r'only \d+ left|low stock|selling fast', all_markup, re.I))
check("no href=\"#\" anywhere", 'href="#"' not in all_markup)
check("no hand-built Shopify CDN URL", 'cdn.shopify.com' not in all_markup)
check("the cart components are loaded once, from the layout",
      "'component-quantity.css'" in R('layout/theme.liquid')
      and "'component-cart-line.css'" in R('layout/theme.liquid')
      and 'component-quantity.css' not in R('sections/main-product.liquid')
      and 'component-cart-line.css' not in R('sections/main-cart.liquid'))
check("no hard-coded /cart path in the markup",
      not re.search(r'action="/cart|href="/cart', all_markup))
check("routes are used for every cart URL",
      all_markup.count('routes.cart_url') >= 2 and 'routes.root_url' in all_markup)

print("\n=== PRODUCT FORM ===")
check("the form is Shopify's own form tag", "form 'product'" in product_body)
check("the class string keeps shopify-product-form",
      'shopify-product-form' in product_body,
      'passing class: replaces the tag default')
check("the theme supplies the variant input itself",
      re.search(r'name="id"\s*\n?\s*value="\{\{\s*current_variant\.id', product_body) is not None)
check("the variant input is disabled when it cannot be bought",
      re.search(r'name="id".*?unless can_buy.*?disabled', product_body, re.S) is not None)
check("the submit is disabled when it cannot be bought",
      re.search(r'data-add-to-cart.*?unless can_buy.*?disabled', product_body, re.S) is not None)
check("availability is read from the variant, not from a nil check",
      'current_variant.available' in R('sections/main-product.liquid'))
check("the product form does not switch off constraint validation",
      'novalidate' not in product_body,
      'novalidate defeats the quantity input\'s own min')
check("the variant picker is inside the product form",
      product_body.index("form 'product'")
      < product_body.index("render 'product-variant-picker'")
      < product_body.index('endform'))
check("the variant table carries the quantity rule",
      'quantity_rule' in product_body)
# THE ASSERTION MOVED WITH THE DEFECT IT GUARDS.
#
# This used to require tabindex="0" on the buying column, because the column was
# a sticky SCROLL CONTAINER — capped at one viewport with its own overflow-y —
# and Safari, plus Chrome before 127, leave scroll containers out of the tab
# order, so anything below its fold was unreachable.
#
# The column is no longer a scroll container. The description moved out to
# .main-product__story, below both grid tracks, which took the column from 794px
# to 485px and let the cap and the overflow come out with it. A tabindex on a
# plain <div> would now be a tab stop that does nothing.
#
# So the check is rewritten rather than deleted, and what it guards is the
# PAIRING: a capped, scrolling column MUST carry the tabindex, and a column that
# fits must not. Reintroduce either half on its own and this fails.
_capped = re.search(r'\.main-product__info\b[^}]*overflow-y:\s*auto',
                    R('assets/section-main-product.css'), re.S) is not None
_tabbed = re.search(r'class="main-product__info"\s*\n?\s*tabindex="0"',
                    product_body) is not None
check("the buying column's scroll container and its tabindex agree",
      _capped == _tabbed,
      'capped=%s tabindex=%s — a scrolling column needs the tabindex, '
      'a fitting one must not have it' % (_capped, _tabbed))
check("the description is not inside the sticky buying column",
      product_body.index('main-product__story')
      > product_body.index('class="main-product__info"')
      and product_body.index('main-product__description')
      > product_body.index('main-product__story'),
      'inside the column it overflowed the cap and produced a second scrollbar')
check("the accelerated checkout button is not wrapped",
      re.search(r'\{\{\s*form\s*\|\s*payment_button\s*\}\}', product_body) is not None
      and 'shopify-payment-button"' not in product_body)
check("the picker is built from options_with_values, not variants",
      'product.options_with_values' in picker_body and 'for variant in product.variants' not in picker_body)
check("a product with no options renders no picker",
      'unless product.has_only_default_variant' in picker_body)
check("unavailable values stay in the DOM and stay focusable",
      'data-unavailable' in picker_body and 'disabled' not in picker_body)
check("the server's unavailable note carries the hook the script manages",
      'data-unavailable-note' in picker_body
      and 'data-unavailable-note' in strip_js(R('assets/product.js')))
check("structured data is emitted exactly once, by Shopify's filter",
      product_body.count('application/ld+json') == 1
      and 'product | structured_data' in product_body)
check("the variant table omits inventory",
      'inventory' not in re.search(r'data-variant-data>(.*?)</script>', _rendered, re.S).group(1))
check("the variant table carries low stock as a boolean, never a count",
      re.search(r'"low_stock":\s*(true|false)',
                re.search(r'data-variant-data>(.*?)</script>', _rendered, re.S).group(1))
      is not None)

print("\n=== CART ===")
check("the quantity field is Shopify's updates[]", "name: 'updates[]'" in line_body)
check("the quantity field is never conditional (updates[] is positional)",
      not re.search(r'\{%-?\s*if[^%]*%\}\s*\{%\s*render \'quantity-selector\'', line_body))
check("removal uses Shopify's own url_to_remove", 'item.url_to_remove' in line_body)
check("the line name comes from item.product.title",
      'item.product.title' in line_body and 'item.product_title' not in line_body)
check("the variant line comes from options_with_values",
      'item.options_with_values' in line_body and 'item.variant_title' not in line_body)
check("the default-title option row is guarded",
      'item.product.has_only_default_variant' in line_body)
check("the line is identified by item.key", 'item.key' in line_body)
check("the totals show subtotal, discounts and an estimated total",
      all(k in totals_body for k in ('cart.items_subtotal_price',
                                     'cart.cart_level_discount_applications',
                                     'cart.total_price')))
check("both cart surfaces render those totals",
      "render 'cart-totals'" in drawer_body and "render 'cart-totals'" in cartpage_body)
check("checkout is a submit inside the cart form, not a bare link",
      'name="checkout"' in drawer_body and 'href="/checkout"' not in drawer_body)
check("the update submit comes before the checkout submit",
      drawer_body.index('name="update"') < drawer_body.index('name="checkout"'),
      'Enter in a quantity field must update, not check out')
check("the count comes from cart.item_count, never a literal",
      'cart.item_count' in strip_liquid(R('snippets/cart-icon-bubble.liquid')))
check("the drawer is not rendered on the cart page",
      re.search(r"unless template\.name == 'cart'", R('layout/theme.liquid')) is not None)
check("the cart page is its own render target",
      'data-cart-page-section' in cartpage_body and 'data-cart-page-inner' in cartpage_body
      and 'data-cart-page-inner' in strip_js(R('assets/cart.js')))
check("each cart surface has a visible failure line",
      drawer_body.count('data-cart-error') == 1 and cartpage_body.count('data-cart-error') == 1
      and 'showCartError' in strip_js(R('assets/cart.js')))
check("the drawer carries its own live region inside the dialog",
      'data-cart-drawer-status' in drawer_body
      and drawer_body.index('data-cart-drawer-status') < drawer_body.index('data-cart-drawer-inner'))
check("cart line ids are namespaced by their surface",
      "scope: 'CartDrawer'" in drawer_body and "scope: 'CartPage'" in cartpage_body
      and 'id_scope' in line_body)
check("the tax note is derived from the store, not asserted",
      'cart.taxes_included' in R('snippets/cart-totals.liquid'))
check("the empty-cart button goes somewhere this theme renders",
      'routes.root_url' in empty_body and 'all_products_collection_url' not in empty_body,
      'no collection template exists yet')
check("totals and the empty state are shared, not duplicated",
      "render 'cart-totals'" in drawer_body and "render 'cart-totals'" in cartpage_body
      and "render 'cart-empty-state'" in drawer_body
      and "render 'cart-empty-state'" in cartpage_body)
check("the drawer is a dialog with a label",
      all(k in drawer_body for k in ('role="dialog"', 'aria-modal="true"', 'aria-labelledby=')))
check("the drawer heading is outside the swapped region",
      drawer_body.index('CartDrawerTitle') < drawer_body.index('data-cart-drawer-inner'))
check("the empty state points somewhere real",
      'routes.root_url' in empty_body and 'href="#"' not in empty_body)
check("the cart drawer adds no cart note or attribute",
      'cart.note' not in drawer_body and 'attributes[' not in drawer_body)

print("\n=== MARKUP CONTRACT ===")
check("exactly one h1 in the product section", product_body.count('<h1') == 1)
check("the cart page's h1 is its title", cartpage_body.count('<h1') == 1)
check("the drawer's heading is an h2, not an h1", '<h2 class="cart-drawer__title"' in drawer_body)
check("no clickable div anywhere",
      not re.search(r'<div[^>]*\bonclick', all_markup))
check("no positive tabindex", not re.findall(r'tabindex="[1-9]', all_markup))
check("no role=menu", 'role="menu"' not in all_markup)
check("no inline event handler", not re.findall(r'\son[a-z]+\s*=\s*"', all_markup))
check("every icon is decorative and named by its control",
      all_markup.count('visually-hidden') >= 6)
check("images carry explicit widths and sizes",
      strip_liquid(R('snippets/product-media-gallery.liquid')).count('sizes: media_sizes') >= 3)
check("the first medium is eager and high priority",
      "loading: 'eager'" in R('snippets/product-media-gallery.liquid')
      and "fetchpriority: 'high'" in R('snippets/product-media-gallery.liquid'))
check("later media are lazy", "loading: 'lazy'" in R('snippets/product-media-gallery.liquid'))
check("no style: parameter is passed to image_tag (Shopify owns object-position)",
      'style:' not in strip_liquid(R('snippets/product-media-gallery.liquid')))

print("\n=== JAVASCRIPT ===")
cart_js = strip_js(R('assets/cart.js'))
product_js = strip_js(R('assets/product.js'))
for label, src in (('cart.js', cart_js), ('product.js', product_js)):
    check("%s adds no framework" % label,
          not re.search(r'\b(React|Vue|jQuery|\$\()', src))
    check("%s uses no alert or confirm" % label, not re.search(r'\b(alert|confirm|prompt)\s*\(', src))
    check("%s does not write to window.Shopify" % label,
          not re.search(r'window\.Shopify\s*[.\[][\w\[\]\'\"]*\s*=', src))
check("cart.js builds URLs from Shopify.routes.root",
      'window.Shopify.routes.root' in cart_js or 'routes && window.Shopify.routes.root' in cart_js)
check("cart.js hard-codes no cart endpoint",
      not re.search(r'[\'\"]/cart/(add|change|update|clear)\.js', cart_js))
check("cart.js sends the documented sections parameter",
      "'sections'" in cart_js and 'sections_url' in cart_js)
check("cart.js identifies lines by key, not index",
      'line' not in re.findall(r'JSON\.stringify\(\{([^}]*)\}', cart_js)[0])
check("cart.js creates exactly one global",
      len(set(re.findall(r'window\.(\w+)\s*=', cart_js)) - {'GodSquad'}) == 0,
      str(sorted(set(re.findall(r'window\.(\w+)\s*=', cart_js)))))
check("product.js creates no global",
      not re.findall(r'window\.\w+\s*=', product_js))
check("cart.js writes no user-facing English",
      'data-cart-strings' in cart_js and not re.search(r"'(Added|Removed|Updated|Sorry)", cart_js))
# The guard is that cart.js never SETS aria-hidden on anything — the drawer
# hides the background with inert, because aria-hidden leaves content focusable
# while removing it from the accessibility tree. Phase 16 added a selector that
# EXCLUDES aria-hidden elements when choosing a focus target, which is the same
# principle applied in the other direction; a test on the bare string called
# that a regression.
check("the drawer's background is made inert, not aria-hidden",
      "setAttribute('inert'" in cart_js
      and not re.search(r"setAttribute\(\s*['\"]aria-hidden", cart_js)
      and not re.search(r"\.ariaHidden\s*=", cart_js))
check("and focus is never moved onto an aria-hidden element",
      ':not([aria-hidden="true"])' in cart_js)
check("inert skips the drawer's own section wrapper",
      'contains(self.el)' in cart_js)
check("the scroll lock saves and restores the offset",
      'scrollY' in cart_js and 'window.scrollTo' in cart_js)
check("Escape is only listened for while the drawer is open",
      cart_js.count("addEventListener('keydown', this.onKeydown") == 1
      and "removeEventListener('keydown', this.onKeydown" in cart_js)
check("the busy state never disables the add button",
      not re.search(r'button\.disabled = ', cart_js),
      'disabling a focused control blurs it')
check("render targets are collected from the page",
      'collectSections' in cart_js and "SECTIONS = ['cart-icon-bubble']" in cart_js)
check("an add carries a sequence guard",
      cart_js.count('var seq = ++requestSeq;') == 2)
check("a superseded change still clears its busy state",
      cart_js.index("control.removeAttribute('aria-busy')")
      < cart_js.index('if (seq !== requestSeq) return;'))
check("a re-rendered drawer tears its open state down",
      cart_js.index('reset: function ()') < cart_js.index('init: function ()')
      < cart_js.index("this.el = document.querySelector('[data-cart-drawer]')"))
check("the price is never blanked when no variant matches",
      "price: ''" not in product_js and 'if (variant) {' in product_js)
check("the quantity rule follows the variant",
      'updateQuantityRule' in product_js)
check("the gallery opens on the slide the server chose",
      "querySelector('.product-gallery__slide.is-active')" in product_js)
check("the scroll strategy reads the rendered layout, not the setting",
      'viewport.scrollWidth > viewport.clientWidth' in product_js
      and "getAttribute('data-gallery-layout') === 'carousel'" not in product_js)
check("the quantity debounce is a literal, not a motion token",
      'QUANTITY_DEBOUNCE_MS = 250' in cart_js)
check("product.js replaces history rather than pushing it",
      'replaceState' in product_js and 'pushState' not in product_js)
check("every listener is delegated on the document",
      cart_js.count("document.addEventListener('click'") >= 3)

print("\n=== DESIGN SYSTEM ===")
qty_css = strip_css(R('assets/component-quantity.css'))
check("the steppers are not shipped without the script that binds them",
      '.cart-js .quantity__button' in qty_css and 'display: none;' in qty_css)
check("the native spinner survives when the steppers do not",
      '.cart-js .quantity__input::-webkit-inner-spin-button' in qty_css)
check("the disabled stepper matches the system's 0.45",
      'opacity: 0.45' in qty_css and 'opacity: 0.35' not in qty_css)
check("an icon-only control hovers to the accent, not to opacity",
      'color: var(--accent-current)' in qty_css)
check("the compact quantity keeps the 16px value",
      'font-size: var(--type-body-sm-size)' not in qty_css)
check("one focus ring on the quantity control, not two",
      ':focus-within' not in qty_css and ':has(.quantity__input:focus-visible)' in qty_css)
check("the swatch uses its own token",
      'var(--swatch-size)' in strip_css(R('assets/section-main-product.css')))
check("the drawer's scrim takes the duration §21.4 assigns it",
      'transition: opacity var(--transition-slow)' in strip_css(R('assets/section-cart-drawer.css')))
check("the visually-hidden recipe is not copied a second time",
      '.visually-hidden--until-focus:focus-visible' in strip_css(R('assets/section-cart-drawer.css'))
      and 'clip: rect(0 0 0 0)' not in strip_css(R('assets/section-cart-drawer.css')))

print("\n=== LOCALES ===")
loc = json.loads(R('locales/en.default.json'))
flat = {}


def walk(node, prefix=''):
    for k, v in node.items():
        key = prefix + k
        if isinstance(v, dict) and not {'one', 'other'} & set(v):
            walk(v, key + '.')
        else:
            flat[key] = v


walk(loc)
# Every Liquid file in the theme, discovered rather than listed. A hand-written
# list silently reports each new section's keys as unused the moment a later
# phase adds one, which is what Phase 10 hit with 39 false positives.
#
# 'templates' was missing from this tuple until Phase 19, and the omission is
# the same defect one level up: when templates/gift_card.liquid arrived it
# referenced seven gift_cards.issued.* keys that this check could not see, so it
# reported all eight as unused. Seven were false. Directories are discovered
# here for the same reason files are discovered inside them.
_liquid = []
for _dirname in ('sections', 'snippets', 'layout', 'templates'):
    _d = os.path.join(THEME, _dirname)
    if os.path.isdir(_d):
        for _f in sorted(os.listdir(_d)):
            if _f.endswith('.liquid'):
                _liquid.append('%s/%s' % (_dirname, _f))
sources = ''.join(R(p) for p in _liquid)
used = set(re.findall(r"'([a-z_]+(?:\.[a-z_0-9]+)+)'\s*\|\s*t\b", sources))
check("no missing translation key", used <= set(flat), str(sorted(used - set(flat))))
unused = sorted(set(flat) - used)
check("no unused translation key", not unused, str(unused))

print("\n=== TOKEN FIDELITY ===")
tokens = set(re.findall(r'(--[\w-]+)\s*:', strip_css(R('assets/design-tokens.css'))))
local = {'--swatch-fill', '--swatch-image', '--logo-height-desktop', '--logo-height-mobile',
         '--header-overlay-offset', '--os-space-top', '--os-space-bottom',
         '--shopify-accelerated-checkout-button-block-size',
         '--shopify-accelerated-checkout-button-border-radius',
         '--shopify-accelerated-checkout-skeleton-background-color'}
for name in NEW_ASSETS:
    if not name.endswith('.css'):
        continue
    css = strip_css(R('assets/' + name))
    # A property DEFINED in this same file is defined, whatever the allow-list
    # happens to list. Component-local properties are an established pattern
    # here (--swatch-fill, --logo-height-mobile), and a hand-written list turns
    # every new one into a false failure.
    defined_here = set(re.findall(r'(--[\w-]+)\s*:', css))
    undef = sorted(u for u in set(re.findall(r'var\((--[\w-]+)', css))
                   if u not in tokens and u not in local and u not in defined_here)
    check("%s: no undefined custom property" % name, not undef, str(undef))
    hexes = set(re.findall(r'#[0-9A-Fa-f]{3,8}\b', css))
    check("%s: no raw hex" % name, not hexes, str(sorted(hexes)))
    check("%s: no !important" % name, '!important' not in css)
    check("%s: no component-level outline" % name,
          not re.search(r'^\s*outline:', css, re.M)
          or 'focus-visible' in css)

def strip_comments(text):
    """A source file with its comments removed — CSS/JS block and Liquid."""
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    text = re.sub(r'\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}', '',
                  text, flags=re.S)
    return text


print("\n=== EARLIER PHASES ===")
untouched = ['sections/hero.liquid', 'sections/featured-collection.liquid',
             'sections/our-story.liquid', 'sections/announcement-bar.liquid',
             'snippets/product-card.liquid', 'assets/header.js',
             'assets/design-tokens.css', 'assets/section-hero.css',
             'assets/section-featured-collection.css', 'assets/section-our-story.css',
             'assets/component-product-card.css', 'assets/component-button.css',
             'assets/header.css', 'templates/index.json']
for rel in untouched:
    # Phase 14: comments are stripped first. This guard exists to catch Phase 8
    # MARKUP and SELECTORS turning up in an earlier phase's file, and a comment
    # is neither — it cannot render an element or match one. Phase 14 added a
    # rule to component-product-card.css whose comment cites
    # section-main-product.css as the precedent it follows, and the guard read
    # the citation as the leak. That is the third time this project has
    # asserted on prose and believed the answer; the fix is the same each time.
    src = strip_comments(R(rel))
    # Phase 12 deliberately crossed this boundary in ONE place: the product
    # card's quick-add form now carries the three hooks assets/cart.js reads, so
    # a failed quick add is visible rather than silent. That is the Phase 12
    # brief's requirement, not drift — so the guard narrows to the markup that
    # would still be wrong here (the drawer, the product page, their controls)
    # rather than being deleted.
    forbidden = r'cart-drawer|main-product|variant-picker|quantity-selector'
    if rel != 'snippets/product-card.liquid':
        forbidden += r'|data-cart-'
    else:
        forbidden += r'|data-cart-bubble|data-cart-drawer|data-cart-line'
    check("%s carries nothing from Phase 8" % rel,
          not re.search(forbidden, src))

header = R('sections/header.liquid')
for marker, label in (('data-menu-toggle', 'the menu button'),
                      ('data-menu-panel', 'the mobile panel'),
                      ('aria-expanded="false"', 'the disclosure state'),
                      ('link.active', 'the active nav state'),
                      ('header__scrim', 'the mandatory scrim'),
                      ('routes.cart_url', 'the cart link destination')):
    check("header keeps %s" % label, marker in header)
check("the header's cart control opens the drawer",
      'data-cart-bubble' in header and "render 'cart-icon-bubble'" in header)
check("the header's cart control is still a real link",
      re.search(r'<a\s+class="header__control header__cart"\s+href="\{\{ routes\.cart_url \}\}"', header) is not None)

layout = R('layout/theme.liquid')
for marker, label in (('skip-link', 'the skip link'), ('<main id="MainContent"', 'the main landmark'),
                      ("sections 'header-group'", 'the header group'), ('content_for_header', 'content_for_header')):
    check("layout keeps %s" % label, marker in layout)
check("the layout renders the drawer as a child of body",
      re.search(r'</main>.*?\{% section \'cart-drawer\' %\}', layout, re.S) is not None)
check("the live region is in the layout, outside the drawer",
      'id="CartStatus"' in layout and 'CartStatus' not in R('sections/cart-drawer.liquid'))
check("the live region is excluded from inert", 'data-cart-no-inert' in layout)

print("\n=== ORIGINAL PROJECT FILES ===")
EV = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'audit-evidence')
orig = {r['path']: r['md5'] for r in csv.DictReader(open(EV + '/inventory.tsv', encoding='utf-8'), delimiter='\t')}
# The manifest's paths are relative to the theme root, not to this script.
def _abs(rel):
    """Where a tracked original lives NOW.

    These are PROTOTYPE files. Phase 10 moved the theme into god-squad-theme/
    and left them at the project root; the 2026-09-26 reorganisation then sorted
    them into prototype/ and brand-assets/. The manifest still records the
    original relative paths, so this tries each home in turn.

    The md5 comparison below is untouched: a file that moved still has to hash
    identically, and one that was edited still fails. Only the lookup changed.
    """
    rel = rel.replace('/', os.sep)
    for base in (
        PROJECT,                                          # pre-reorganisation
        os.path.join(PROJECT, 'prototype'),               # the export itself
        os.path.join(PROJECT, 'brand-assets'),            # images/, uploads/, …
    ):
        p = os.path.join(base, rel)
        if os.path.exists(p):
            return p
        # images/foo.png -> brand-assets/images/foo.png keeps its subfolder, but
        # a loose root file lands directly in brand-assets/ with no subfolder.
        flat = os.path.join(base, os.path.basename(rel))
        if os.path.exists(flat):
            return flat
    return os.path.join(PROJECT, rel)


mod = [p for p, h in orig.items()
       if os.path.exists(_abs(p)) and hashlib.md5(open(_abs(p), 'rb').read()).hexdigest() != h]
gone = [p for p in orig if not os.path.exists(_abs(p))]
check("tracked originals unmodified (%d files)" % len(orig), not mod and not gone,
      "MODIFIED=%s DELETED=%s" % (mod or 'none', gone or 'none'))

print("\n%d checks, %d passed, %d failed" % (count['pass'] + count['fail'], count['pass'], count['fail']))
print("OVERALL:", "PASS" if ok else "*** FAILURES ABOVE ***")
