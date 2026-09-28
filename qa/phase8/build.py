# -*- coding: utf-8 -*-
"""
Phase 8 render harness.

Renders the REAL sections/*.liquid and snippets/*.liquid through miniliquid
against mock Shopify data, and writes one static page per test state. The mock
data lives only here, in the scratchpad; nothing in the theme knows about it.

It covers the states the Phase 8 brief lists: one variant, several variants,
several option types, a sold-out variant, a sold-out product, a sale price, no
compare-at price, a long title, a long description, one image, several images,
a video, an empty cart, one cart item, several cart items, two lines of the
same product, and the drawer on both surfaces.
"""
import os, re, sys, json, io, shutil

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from miniliquid import Engine, wrap, Env  # noqa: E402

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
# Fixture imagery lives OUTSIDE the theme. Phase 1 section 29.1: nothing from
# images/ or the project root is copied into the theme, because content images
# reach the page through image_picker settings and Shopify Files.
PROJECT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(HERE, 'site')
os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
os.makedirs(os.path.join(OUT, 'img'), exist_ok=True)

# Every asset in the theme, DISCOVERED rather than listed. A hand-written list
# silently stops copying the moment a phase adds a stylesheet: Phase 10's five
# new surfaces linked their CSS, the files were never copied, the links 404'd,
# and the responsive sweep measured unstyled browser defaults -- reporting 17px
# footer links and a 19px select as real defects. The harness must serve what
# the theme references.
ASSETS = tuple(sorted(
    f for f in os.listdir(os.path.join(THEME, 'assets'))
    if f.endswith('.css') or f.endswith('.js')))
for f in ASSETS:
    shutil.copy(os.path.join(THEME, 'assets', f), os.path.join(OUT, 'assets', f))
# The TRANSPARENT wordmark, not images/logo.png. That file is the same
# artwork flattened onto a dark square: 0% of its pixels are transparent and
# all four corners are alpha 255, which is the black box that sat behind the
# logo in every screenshot. This one is 76.9% clear with white ink. The
# original is a tracked audit original and is deliberately left untouched.
shutil.copy(os.path.join(PROJECT, 'brand-assets', 'images', 'WHITE FONT LOGO.png'),
            os.path.join(OUT, 'img', 'logo.png'))
for src, dst in (('product-tee.webp', 'tee.webp'),
                 ('product-hoodie.webp', 'hoodie.webp'),
                 ('product-cap.webp', 'cap.webp'),
                 ('our-story.webp', 'story.webp')):
    shutil.copy(os.path.join(PROJECT, 'brand-assets', 'images', src), os.path.join(OUT, 'img', dst))

TRANSLATIONS = json.load(open(os.path.join(THEME, 'locales', 'en.default.json'), encoding='utf-8'))


# --------------------------------------------------------------------- data

def img(src, alt, w, h):
    return wrap({'src': 'img/' + src, 'alt': alt, 'width': w, 'height': h})


def media(mid, src, alt, w, h, kind='image', host=None):
    """A Shopify media object. preview_image is present on every type, which is
    what lets the thumbnail rail draw a video's poster frame."""
    return wrap({
        'id': mid, 'media_type': kind, 'alt': alt, 'position': None,
        'preview_image': {'src': 'img/' + src, 'alt': alt, 'width': w, 'height': h},
        'src': 'img/' + src, 'width': w, 'height': h, 'host': host,
    })


def option_value(name, available=True, selected=False, colour=None, vid=None):
    return {'name': name, 'available': available, 'selected': selected,
            'id': vid or abs(hash(name)) % 100000,
            'swatch': ({'color': colour} if colour else None),
            'product_url': None, 'variant': None}


def option(name, position, values, selected_value=None):
    return {'name': name, 'position': position, 'values': values,
            'selected_value': selected_value or values[0]['name']}


def variant(vid, title, options, price, **kw):
    return {
        'id': vid, 'title': title, 'options': options, 'price': price,
        'compare_at_price': kw.get('compare_at', 0),
        'available': kw.get('available', True),
        'sku': kw.get('sku', ''),
        'featured_media': kw.get('featured_media'),
        'quantity_rule': kw.get('quantity_rule'),
        'unit_price_measurement': kw.get('unit_price_measurement'),
        'unit_price': kw.get('unit_price'),
        'url': '/products/' + kw.get('handle', 'p') + '?variant=' + str(vid),
    }


def product(handle, title, variants, **kw):
    med = kw.get('media', [])
    images = [m['preview_image'] for m in med if m['media_type'] == 'image']
    prices = [v['price'] for v in variants] or [0]
    first_available = None
    for v in variants:
        if v['available']:
            first_available = v
            break
    selected = kw.get('selected')
    if selected is None and kw.get('select_option'):
        want = kw['select_option']
        for v in variants:
            if want in v['options']:
                selected = v
                break
    if selected is None:
        selected = first_available or (variants[0] if variants else None)
    return wrap({
        'id': kw.get('id', abs(hash(handle)) % 1000000),
        'title': title, 'handle': handle, 'url': '/products/' + handle,
        'vendor': kw.get('vendor', 'God Squad'),
        'type': kw.get('type', ''),
        'description': kw.get('description', ''),
        'available': any(v['available'] for v in variants),
        'price': selected['price'] if selected else 0,
        'price_min': min(prices), 'price_max': max(prices),
        'price_varies': min(prices) != max(prices),
        'compare_at_price_max': max([v['compare_at_price'] for v in variants] or [0]),
        'featured_image': images[0] if images else None,
        'images': images,
        'media': med,
        'featured_media': med[0] if med else None,
        'variants': variants,
        'selected_variant': kw.get('selected'),
        'selected_or_first_available_variant': selected,
        'options_with_values': kw.get('options', []),
        'has_only_default_variant': kw.get('default_only', False),
    })


SHORT_DESC = ('<p>Heavyweight cotton, cut boxy and built to last. Printed in small runs.</p>')
LONG_DESC = SHORT_DESC + (
    '<p>Every piece is produced in limited quantity so the people wearing it are not '
    'wearing what everyone else is wearing.</p>'
    '<p>Fit is oversized. Take your usual size for the intended drape, or one down '
    'for a regular fit.</p>'
    '<ul><li>Ribbed collar</li><li>Double-stitched hems</li><li>Machine wash cold</li></ul>')

TEE_MEDIA = [media(101, 'tee.webp', 'Signature Oversized Tee, front', 900, 900),
             media(102, 'hoodie.webp', 'Signature Oversized Tee, back', 900, 900),
             media(103, 'cap.webp', 'Signature Oversized Tee, detail', 900, 900),
             media(104, 'story.webp', 'Signature Oversized Tee, worn', 535, 348)]

# 1. One variant, no options. The state every merchant starts in.
P_SINGLE = product(
    'utility-cap', 'Utility Cap',
    [variant(9001, 'Default Title', ['Default Title'], 89000, sku='GS-CAP-001', handle='utility-cap')],
    media=[media(201, 'cap.webp', 'Utility Cap', 900, 900)],
    description=SHORT_DESC, type='Headwear', default_only=True)

# 2. One option, one value sold out.
SIZES = [option_value('XS'), option_value('S', selected=True), option_value('M'),
         option_value('L', available=False), option_value('XL')]
P_SIZES = product(
    'signature-tee', 'Signature Oversized Tee',
    [variant(9101, 'XS', ['XS'], 129000, handle='signature-tee', featured_media=TEE_MEDIA[0]),
     variant(9102, 'S', ['S'], 129000, handle='signature-tee', sku='GS-TEE-S',
             featured_media=TEE_MEDIA[1]),
     variant(9103, 'M', ['M'], 129000, handle='signature-tee'),
     variant(9104, 'L', ['L'], 129000, available=False, handle='signature-tee'),
     variant(9105, 'XL', ['XL'], 129000, handle='signature-tee')],
    media=TEE_MEDIA, description=LONG_DESC, type='T-shirt',
    options=[option('Size', 1, SIZES, 'S')],
    # Shopify keeps options_with_values[].selected and
    # selected_or_first_available_variant in step; the fixture must too, or the
    # harness reports a mismatch the platform cannot produce.
    selected=None, select_option='S')

# 3. Two option types, swatches, and a sale price on every variant.
COLOURS = [option_value('Ink', colour='#0D0C0A', selected=True),
           option_value('Cream', colour='#F3EFE6'),
           option_value('Olive', colour='#4B5443', available=False)]
SIZES2 = [option_value('S', selected=True), option_value('M'), option_value('L')]


def hoodie_variants():
    out = []
    vid = 9200
    for colour in ('Ink', 'Cream', 'Olive'):
        for size in ('S', 'M', 'L'):
            vid += 1
            avail = not (colour == 'Olive' or (colour == 'Cream' and size == 'L'))
            out.append(variant(vid, colour + ' / ' + size, [colour, size], 249000,
                               compare_at=299000, available=avail, handle='heavyweight-hoodie',
                               sku='GS-HD-' + colour[:2].upper() + '-' + size))
    return out


P_MULTI = product(
    'heavyweight-hoodie', 'Heavyweight Hoodie', hoodie_variants(),
    media=[media(301, 'hoodie.webp', 'Heavyweight Hoodie', 900, 900),
           media(302, 'tee.webp', 'Heavyweight Hoodie, back', 900, 900),
           media(303, 'story.webp', 'Heavyweight Hoodie, worn', 535, 348, kind='video')],
    description=SHORT_DESC, type='Hoodie',
    options=[option('Colour', 1, COLOURS, 'Ink'), option('Size', 2, SIZES2, 'S')])

# 4. Every variant sold out.
P_SOLDOUT = product(
    'sold-out-crew', 'Faith Crew',
    [variant(9301, 'S', ['S'], 169000, available=False, handle='sold-out-crew'),
     variant(9302, 'M', ['M'], 169000, available=False, handle='sold-out-crew')],
    media=[media(401, 'tee.webp', 'Faith Crew', 900, 900)],
    description=SHORT_DESC,
    options=[option('Size', 1, [option_value('S', available=False, selected=True),
                                option_value('M', available=False)], 'S')])

# 5. A very long title, a long description, and no media at all.
P_LONG = product(
    'long', 'Limited Edition Heavyweight Oversized Hooded Sweatshirt In Washed Ink',
    [variant(9401, 'Default Title', ['Default Title'], 349000, handle='long')],
    media=[], description=LONG_DESC, default_only=True, vendor='God Squad', type='Hoodie')

# 6. A variant carrying a quantity rule and a unit price.
P_RULE = product(
    'bundle', 'Three Pack',
    [variant(9501, 'Default Title', ['Default Title'], 300000, handle='bundle',
             quantity_rule={'min': 2, 'max': 6, 'increment': 2},
             unit_price=100000,
             unit_price_measurement={'reference_value': 1, 'reference_unit': 'item'})],
    media=[media(501, 'tee.webp', 'Three Pack', 900, 900)],
    description=SHORT_DESC, default_only=True)


# ---------------------------------------------------------------- cart data

def line(key, prod, var, qty, price, **kw):
    return wrap({
        'key': key, 'id': var['id'], 'quantity': qty,
        'product': prod, 'variant': var,
        'title': prod['title'] + ' - ' + var['title'],
        'url': prod['url'] + '?variant=' + str(var['id']),
        'url_to_remove': '/cart/change?id=' + key + '&quantity=0',
        'image': kw.get('image'),
        'final_line_price': price * qty,
        'original_line_price': kw.get('original', price) * qty,
        'final_price': price, 'original_price': kw.get('original', price),
        'options_with_values': kw.get('options', []),
        'properties': kw.get('properties'),
        'line_level_discount_allocations': kw.get('discounts', []),
        'error_message': kw.get('error'),
        'selling_plan_allocation': None,
        'unit_price_measurement': None,
    })


CART_EMPTY = wrap({'item_count': 0, 'items': [], 'items_subtotal_price': 0,
                   'total_price': 0, 'cart_level_discount_applications': [],
                   'taxes_included': False, 'note': ''})


def build_cart(items, discounts=None, note=''):
    subtotal = sum(i['final_line_price'] for i in items)
    disc = discounts or []
    total = subtotal - sum(d['total_allocated_amount'] for d in disc)
    return wrap({
        'item_count': sum(i['quantity'] for i in items),
        'items': items,
        'items_subtotal_price': subtotal,
        'total_price': total,
        'original_total_price': sum(i['original_line_price'] for i in items),
        'cart_level_discount_applications': disc,
        'taxes_included': False,
        # Phase 14. Shopify's own single free-text cart note.
        'note': note,
        'empty?': len(items) == 0,
    })


L1 = line('k1:aaa', P_SIZES, P_SIZES['variants'][1], 1, 129000,
          image=img('tee.webp', 'Signature Oversized Tee', 900, 900),
          options=[{'name': 'Size', 'value': 'S'}])
L2 = line('k2:bbb', P_SIZES, P_SIZES['variants'][2], 2, 129000,
          image=img('tee.webp', 'Signature Oversized Tee', 900, 900),
          options=[{'name': 'Size', 'value': 'M'}])
L3 = line('k3:ccc', P_MULTI, P_MULTI['variants'][0], 1, 224100, original=249000,
          image=img('hoodie.webp', 'Heavyweight Hoodie', 900, 900),
          options=[{'name': 'Colour', 'value': 'Ink'}, {'name': 'Size', 'value': 'S'}],
          discounts=[{'amount': 24900,
                      'discount_application': {'title': 'Launch 10%'}}])
L4 = line('k4:ddd', P_SINGLE, P_SINGLE['variants'][0], 1, 89000,
          image=img('cap.webp', 'Utility Cap', 900, 900),
          error='All 3 Utility Cap are in your cart.')

CART_ONE = build_cart([L1])
# Phase 14. A cart that already carries a note, so the disclosure has to render
# open — a note hidden behind a control the customer must find is a note they
# will not know is attached to their order.
CART_NOTED = build_cart([L1, L2], note='Please leave it with the guard at Gate 2.')
CART_MANY = build_cart([L1, L2, L3, L4],
                       discounts=[{'title': 'Welcome', 'total_allocated_amount': 5000}])


# ------------------------------------------------------------------- engine

PAGE_TYPES = {'index': 'index', 'product': 'product', 'collection': 'collection',
              'search': 'search', 'page': 'page', 'cart': 'cart', '404': '404',
              'list-collections': 'list-collections'}

PAGE_TITLES = {'index': 'God Squad', 'product': 'Signature Oversized Tee',
               'collection': 'The Faithful', 'search': 'Search',
               'page': 'Size Guide', 'cart': 'Your cart', '404': 'Page not found'}


def make_engine(cart=CART_EMPTY, design_mode=False, template='product'):
    g = {
        'settings': wrap({'container_width': 1440, 'radius_sm': 2,
                          'product_image_ratio': 'square',
                          'logo': img('logo.png', 'God Squad', 500, 500),
                          'logo_height_desktop': 78, 'logo_height_mobile': 56}),
        # Phase 16. page_type, canonical_url, page_title and page_description
        # were all absent, so every head tag built from them rendered empty and
        # the Open Graph branches were never exercised. request.page_type in
        # particular decides og:type.
        'request': wrap({'design_mode': design_mode, 'locale': {'iso_code': 'en'},
                         'page_type': PAGE_TYPES.get(template, template)}),
        'canonical_url': 'https://godsquad.example/' + template,
        'page_title': PAGE_TITLES.get(template, 'God Squad'),
        'page_description': 'Faith-driven premium streetwear from the Philippines.',
        'routes': wrap({'root_url': '/', 'cart_url': '/cart',
                        'cart_add_url': '/cart/add', 'cart_change_url': '/cart/change',
                        'cart_update_url': '/cart/update',
                        'all_products_collection_url': '/collections/all',
                        'search_url': '/search', 'account_url': '/account'}),
        'shop': wrap({'name': 'God Squad', 'customer_accounts_enabled': True}),
        'cart': cart,
        'template': wrap({'name': template}),
        'additional_checkout_buttons': True,
        'content_for_additional_checkout_buttons':
            '<div data-harness-stub="additional-checkout">Shop Pay</div>',
        'linklists': wrap({'main-menu': {'links': [
            {'title': 'Home', 'url': '/', 'active': False},
            {'title': 'Shop', 'url': '/collections/all', 'active': False},
            # COLLECTIONS REMOVED. It pointed at /collections, which is Shopify's
            # collection LIST page and needs templates/list-collections.json.
            # This theme ships seven templates and that is not one of them, so on a
            # live store the item led to an error page. Phase 1 recorded it at the
            # outset -- PHASE-1-WEBSITE-AUDIT.md:1249, "ADD LATER, REQUIRED if
            # COLLECTIONS stays in the menu" -- and it was never built. The owner
            # asked to merge Shop and Collections; Shop (/collections/all) is the
            # one with a working destination, so Collections is the one that goes.
            # The live menu is merchant data in Shopify admin; this mock only makes
            # the preview show what the live menu is meant to be.
            {'title': 'Our Story', 'url': '/#story', 'active': False},
            {'title': 'Verse', 'url': '/#verse', 'active': False},
        ]}}),
    }
    return Engine(THEME, globals_=g, translations=TRANSLATIONS, asset_base='assets/')


def blocks(items):
    return [wrap({'id': b['id'], 'type': b['type'], 'settings': wrap(b['settings']),
                  'shopify_attributes': ''}) for b in items]


def render_section(engine, relpath, sid, settings, blks=None, extra=None):
    scope = {'section': wrap({'id': sid, 'settings': wrap(settings),
                              'blocks': blocks(blks or []),
                              'shopify_attributes': ''})}
    if extra:
        scope.update(extra)
    src = open(os.path.join(THEME, relpath), encoding='utf-8').read()
    return engine.render(src, scope)


HEADER_SETTINGS = {
    'logo': img('logo.png', 'God Squad', 500, 500),
    'logo_height_desktop': 78, 'logo_height_mobile': 56,
    'menu': 'main-menu', 'show_search': True, 'show_account': True,
    'show_cart': True,
    'sticky': False, 'overlay_first_section': False,
}

PRODUCT_DEFAULTS = {
    'media_layout': 'stacked', 'show_quantity': True,
    'show_accelerated_checkout': True, 'description_layout': 'open',
    'show_vendor': False, 'show_product_type': False, 'show_sku': False,
    'sticky_info': True, 'surface': 'light',
}

DRAWER_DEFAULTS = {
    'auto_open': True, 'show_view_cart': True, 'show_note': False,
    'empty_link': '', 'empty_link_label': 'Shop the collection',
}

CART_DEFAULTS = {'empty_link': '', 'empty_link_label': 'Shop the collection',
                 'show_note': False}

PAGE = """<!doctype html>
<html lang="en" class="no-js"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>God Squad — Phase 8 harness</title>
%(headcss)s
<script>document.documentElement.classList.replace('no-js','js');</script>
<script>window.Shopify = window.Shopify || {routes: {root: '/'}};</script>
<script src="assets/header.js" defer></script>
<script src="assets/cart.js" defer></script>
</head><body class="template-%(template)s">
<a class="skip-link" href="#MainContent">Skip to content</a>
%(header)s
<main id="MainContent" tabindex="-1">
%(body)s
</main>
%(drawer)s
<div id="CartStatus" class="visually-hidden" role="status" aria-live="polite" data-cart-no-inert></div>
<div hidden data-cart-no-inert data-cart-strings
  data-added="Added to your cart."
  data-updated="Cart updated."
  data-removed="Removed from your cart."
  data-note-saved="Order note saved."
  data-quantity-announce="Quantity: [count]"
  data-error-generic="Unable to update your cart. Please try again."
  data-error-network="We could not reach the store. Check your connection and try again."></div>
</body></html>
"""


def layout_stylesheets():
    """The stylesheets layout/theme.liquid actually loads, in its order.

    Phase 18: this list used to be hardcoded in PAGE. Two components were
    promoted to the layout — component-container.css and
    component-pagination.css — and the harness kept rendering pages without
    them, which showed up as a fake layout regression: cards 24px too wide and
    the homepage overflowing, because .container had no stylesheet. The theme
    was correct and the harness was a page from a different theme.

    Reading the layout means a stylesheet promoted in a later phase is picked
    up automatically instead of silently missing.
    """
    src = open(os.path.join(THEME, 'layout', 'theme.liquid'), encoding='utf-8').read()
    src = re.sub(r'\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}', '', src, flags=re.S)
    names = re.findall(r"'([\w.-]+\.css)'\s*\|\s*asset_url\s*\|\s*stylesheet_tag", src)
    seen, out = set(), []
    for n in names:
        if n not in seen:
            seen.add(n)
            out.append('<link rel="stylesheet" href="assets/%s">' % n)
    return '\n'.join(out)


def write(name, parts, header_html, drawer_html, template='product'):
    # The layout does not render the drawer on the cart template: two views of
    # one cart on one page can disagree, and they collided on every line's ids.
    if template == 'cart':
        drawer_html = ''
    body = '\n'.join(
        '<div id="shopify-section-%s" class="shopify-section">%s</div>' % (sid, html)
        for sid, html in parts)
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(
        PAGE % {'body': body, 'header': header_html, 'drawer': drawer_html,
                'template': template, 'headcss': layout_stylesheets()})
    return name


CASES = []


def case(label, fname, prod=None, cart=CART_EMPTY, product_settings=None,
         drawer_settings=None, template='product', cart_page=False,
         cart_settings=None, no_drawer=False):
    engine = make_engine(cart=cart, template=template)
    header = '<div id="shopify-section-header" class="shopify-section">%s</div>' % (
        render_section(engine, 'sections/header.liquid', 'header', HEADER_SETTINGS))
    drawer = '<div id="shopify-section-cart-drawer" class="shopify-section">%s</div>' % (
        render_section(engine, 'sections/cart-drawer.liquid', 'cart-drawer',
                       dict(DRAWER_DEFAULTS, **(drawer_settings or {}))))

    # Phase 14. settings.cart_type == 'page' means the layout renders no drawer
    # at all, which is the case where an add has nothing to confirm it.
    if no_drawer:
        drawer = ''

    parts = []
    if cart_page:
        parts.append(('main', render_section(engine, 'sections/main-cart.liquid', 'main',
                                             dict(CART_DEFAULTS, **(cart_settings or {})))))
    elif prod is not None:
        settings = dict(PRODUCT_DEFAULTS, **(product_settings or {}))
        parts.append(('main', render_section(engine, 'sections/main-product.liquid', 'main',
                                             settings, extra={'product': prod})))

    write(fname, parts, header, drawer, template=template)
    missing = list(engine.missing_translations)
    CASES.append((label, fname, missing))
    return fname


def main():
    # -------------------------------------------------------- product states
    case('one variant, no options', 'p-single.html', P_SINGLE)
    case('several variants, one sold out', 'p-sizes.html', P_SIZES)
    case('two option types, swatches, on sale', 'p-multi.html', P_MULTI)
    case('product entirely sold out', 'p-soldout.html', P_SOLDOUT)
    case('long title, long description, no media', 'p-long.html', P_LONG)
    case('quantity rule and unit price', 'p-rule.html', P_RULE)
    case('carousel media layout', 'p-carousel.html', P_SIZES,
         product_settings={'media_layout': 'carousel'})
    case('ink surface', 'p-ink.html', P_SIZES, product_settings={'surface': 'dark'})
    case('all details shown', 'p-details.html', P_SIZES,
         product_settings={'show_vendor': True, 'show_sku': True,
                           'show_product_type': True,
                           'description_layout': 'collapsible'})
    case('no quantity, no accelerated checkout', 'p-minimal.html', P_SINGLE,
         product_settings={'show_quantity': False,
                           'show_accelerated_checkout': False})
    case('sticky info off', 'p-nosticky.html', P_SIZES,
         product_settings={'sticky_info': False})

    # ----------------------------------------------------------- cart states
    case('drawer, empty cart', 'c-empty.html', P_SIZES, cart=CART_EMPTY)
    case('drawer, one item', 'c-one.html', P_SIZES, cart=CART_ONE)
    case('drawer, four items with a discount and an error', 'c-many.html', P_SIZES,
         cart=CART_MANY)
    case('drawer, view cart link off', 'c-noview.html', P_SIZES, cart=CART_MANY,
         drawer_settings={'show_view_cart': False})
    case('cart page, empty', 'c-page-empty.html', cart=CART_EMPTY,
         template='cart', cart_page=True)
    case('cart page, four items', 'c-page-many.html', cart=CART_MANY,
         template='cart', cart_page=True)

    # ------------------------------------------------- Phase 14: the note
    case('drawer, order note on, empty note', 'c-note.html', P_SIZES, cart=CART_ONE,
         drawer_settings={'show_note': True})
    case('drawer, order note on, note already written', 'c-noted.html', P_SIZES,
         cart=CART_NOTED, drawer_settings={'show_note': True})
    case('cart page, order note on', 'c-page-note.html', cart=CART_NOTED,
         template='cart', cart_page=True, cart_settings={'show_note': True})
    case('product page, no drawer (cart style: page)', 'p-nodrawer.html', P_SIZES,
         no_drawer=True)

    print('%-46s %-24s %s' % ('CASE', 'FILE', 'MISSING TRANSLATIONS'))
    bad = 0
    for label, fname, missing in CASES:
        if missing:
            bad += 1
        print('%-46s %-24s %s' % (label, fname, ', '.join(sorted(missing)) or 'none'))
    print()
    print('pages written: %d  with missing translations: %d' % (len(CASES), bad))


if __name__ == '__main__':
    main()
