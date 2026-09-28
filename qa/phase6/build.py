# -*- coding: utf-8 -*-
"""
Phase 6 render harness.

Renders the REAL sections/*.liquid and snippets/*.liquid through miniliquid
against mock Shopify data, and writes one static page per test case. The mock
data exists only here, in the scratchpad; nothing in the theme knows about it.
"""
import os, sys, json, io, shutil, html

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from miniliquid import Engine, Drop, wrap, LiquidError, Env

THEME = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website"
OUT = os.path.join(HERE, 'site')
os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
os.makedirs(os.path.join(OUT, 'img'), exist_ok=True)

for f in ('design-tokens.css', 'header.css', 'section-hero.css',
          'component-button.css', 'component-product-card.css',
          'section-featured-collection.css'):
    shutil.copy(os.path.join(THEME, 'assets', f), os.path.join(OUT, 'assets', f))
shutil.copy(os.path.join(THEME, 'images', 'logo.png'), os.path.join(OUT, 'img', 'logo.png'))
shutil.copy(os.path.join(THEME, 'phase-3-assets', 'hero', 'hero-walk-by-faith-desktop-1672w.webp'),
            os.path.join(OUT, 'img', 'hero.webp'))
for src, dst in (('product-tee.webp', 'tee.webp'),
                 ('product-hoodie.webp', 'hoodie.webp'),
                 ('product-cap.webp', 'cap.webp')):
    shutil.copy(os.path.join(THEME, 'images', src), os.path.join(OUT, 'img', dst))

TRANSLATIONS = json.load(open(os.path.join(THEME, 'locales', 'en.default.json'), encoding='utf-8'))


# --------------------------------------------------------------------- mock data
def img(src, alt, w, h):
    return wrap({'src': 'img/' + src, 'alt': alt, 'width': w, 'height': h})


def swatch_option(name, values):
    """values: [(label, hex|None)]"""
    return wrap({
        'name': name,
        'values': [
            {'name': v, 'swatch': ({'color': c} if c else None)}
            for v, c in values
        ],
    })


def product(handle, title, price, **kw):
    images = kw.get('images', [img('tee.webp', title, 900, 900)])
    p = {
        'title': title,
        'url': '/products/' + handle,
        'handle': handle,
        'price': price,
        'price_min': kw.get('price_min', price),
        'price_max': kw.get('price_max', price),
        'price_varies': kw.get('price_varies', False),
        'compare_at_price_max': kw.get('compare_at', 0),
        'available': kw.get('available', True),
        'featured_image': images[0] if images else None,
        'images': images,
        'variants': kw.get('variants', [{'id': 111, 'available': True}]),
        'selected_or_first_available_variant': {'id': 111},
        'options_with_values': kw.get('options', []),
    }
    return wrap(p)


COLOURS = swatch_option('Colour', [('Ink', '#0D0C0A'), ('Cream', '#F3EFE6'), ('Olive', '#4B5443')])
TWO_COLOURS = swatch_option('Colour', [('Ink', '#0D0C0A'), ('Cream', '#F3EFE6')])
SIZES_OPT = swatch_option('Size', [('S', None), ('M', None), ('L', None)])

P_TEE = product('signature-oversized-tee', 'Signature Oversized Tee', 129000,
                images=[img('tee.webp', 'Signature Oversized Tee', 900, 900),
                        img('hoodie.webp', 'Signature Oversized Tee, back', 900, 900)],
                options=[SIZES_OPT, COLOURS],
                variants=[{'id': 1}, {'id': 2}, {'id': 3}])
P_HOODIE = product('heavyweight-hoodie', 'Heavyweight Hoodie', 249000,
                   images=[img('hoodie.webp', 'Heavyweight Hoodie', 900, 900)],
                   options=[TWO_COLOURS], compare_at=299000,
                   variants=[{'id': 4}, {'id': 5}])
P_CAP = product('utility-cap', 'Utility Cap', 89000,
                images=[img('cap.webp', 'Utility Cap', 900, 900)],
                available=False, options=[])
P_LONG = product('long', 'The Built Different For A Higher Purpose Heavyweight Embroidered Oversized Crewneck Sweatshirt',
                 189000, images=[img('tee.webp', None, 900, 900)], options=[COLOURS])
P_NOIMG = product('no-image', 'Piece Without A Photograph', 99000, images=[], options=[])
P_VARIES = product('varies', 'Essentials Set', 159000, price_min=159000, price_max=289000,
                   price_varies=True, compare_at=349000,
                   images=[img('cap.webp', 'Essentials Set', 900, 900)],
                   variants=[{'id': 9}, {'id': 10}])
P_SINGLE = product('single-variant', 'One Variant Piece', 109000,
                   images=[img('hoodie.webp', 'One Variant Piece', 900, 900)],
                   variants=[{'id': 12}], options=[])

ALL = [P_TEE, P_HOODIE, P_CAP, P_LONG, P_NOIMG, P_VARIES, P_SINGLE,
       product('x1', 'Cross Tee', 119000, images=[img('tee.webp', 'Cross Tee', 900, 900)]),
       product('x2', 'Purpose Hoodie', 259000, images=[img('hoodie.webp', 'Purpose Hoodie', 900, 900)]),
       product('x3', 'Movement Cap', 79000, images=[img('cap.webp', 'Movement Cap', 900, 900)]),
       product('x4', 'Faith Crew', 169000, images=[img('tee.webp', 'Faith Crew', 900, 900)]),
       product('x5', 'Higher Tee', 139000, images=[img('tee.webp', 'Higher Tee', 900, 900)])]


def collection(handle, products, title='The Faithful'):
    return wrap({'handle': handle, 'title': title, 'url': '/collections/' + handle,
                 'products': products, 'products_count': len(products),
                 'image': None, 'description': ''})


# --------------------------------------------------------------------- engine
def make_engine(design_mode=False):
    g = {
        'settings': wrap({'container_width': 1440, 'radius_sm': 2, 'product_image_ratio': 'square',
                          'color_ink': '#0D0C0A', 'color_cream': '#F3EFE6', 'color_gold': '#D8C08A'}),
        'request': wrap({'design_mode': design_mode, 'locale': {'iso_code': 'en'}}),
        'routes': wrap({'root_url': '/', 'cart_url': '/cart', 'cart_add_url': '/cart/add',
                        'search_url': '/search', 'account_url': '/account'}),
        'shop': wrap({'name': 'God Squad', 'customer_accounts_enabled': True}),
        'cart': wrap({'item_count': 0}),
        'template': wrap({'name': 'index'}),
    }
    e = Engine(THEME, globals_=g, translations=TRANSLATIONS, asset_base='assets/')
    return e


SECTION_DEFAULTS = {
    'collection': None, 'products_to_show': 3,
    'eyebrow': 'New Drop /', 'heading': 'The Faithful',
    'description': 'Premium Essentials for a Higher Purpose.',
    'show_view_all': True, 'view_all_label': 'View All Products', 'view_all_url': '',
    'surface': 'light', 'layout': 'with-copy-column',
    'columns_desktop': 3, 'columns_tablet': 2, 'columns_mobile': 2,
    'show_price': True, 'show_compare_at_price': True, 'show_swatches': True,
    'spacing_top': 'standard', 'spacing_bottom': 'standard', 'anchor_id': 'shop',
}

HERO_SETTINGS = {
    'image': img('hero.webp', '', 1672, 941), 'mobile_image': None,
    'focal_point': 'centre-left', 'overlay': 'medium',
    'eyebrow': 'Streetwear With A Purpose.', 'heading': 'Walk By',
    'heading_accent': 'Faith.', 'scripture': '2 Corinthians 5:7',
    'description': 'Different People. Same Purpose.',
    'button_label': 'Shop The Collection', 'button_link': '',
    'height': 'medium', 'text_position': 'centre', 'text_alignment': 'left',
}


def render_section(engine, relpath, sid, settings):
    scope = {'section': wrap({'id': sid, 'settings': settings, 'shopify_attributes': ''})}
    src = open(os.path.join(THEME, relpath), encoding='utf-8').read()
    return engine.render(src, scope)


HEADER = open(os.path.join(HERE, 'header.html'), encoding='utf-8').read() if os.path.exists(
    os.path.join(HERE, 'header.html')) else ''

PAGE = """<!doctype html>
<html lang="en" class="no-js"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>God Squad — Phase 6 harness</title>
<link rel="stylesheet" href="assets/design-tokens.css">
<link rel="stylesheet" href="assets/header.css">
<link rel="stylesheet" href="assets/component-button.css">
<style>:root{--header-overlay-offset:var(--header-height-mobile)}@media(min-width:1024px){:root{--header-overlay-offset:var(--header-height-desktop)}}:root{%(extra_root)s}</style>
%(headcss)s
<script>document.documentElement.classList.replace('no-js','js');</script>
</head><body class="template-index">
<a class="skip-link" href="#MainContent">Skip to content</a>
%(header)s
<main id="MainContent" tabindex="-1">
%(body)s
</main></body></html>
"""


def page(body, extra_root='', header=True, headcss=''):
    return PAGE % {'body': body, 'header': HEADER if header else '',
                   'extra_root': extra_root, 'headcss': headcss}


def write(name, body, **kw):
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(page(body, **kw))
    return name


# --------------------------------------------------------------------- cases
def main():
    results = []

    def case(label, sections, design_mode=False, extra_root='', fname=None):
        e = make_engine(design_mode)
        parts = []
        for relpath, sid, settings in sections:
            merged = dict(SECTION_DEFAULTS)
            merged.update(settings)
            html_out = render_section(e, relpath, sid, wrap(merged))
            parts.append('<section id="shopify-section-%s" class="shopify-section">%s</section>' % (sid, html_out))
        fn = fname or (label.replace(' ', '-').lower() + '.html')
        write(fn, '\n'.join(parts), extra_root=extra_root)
        results.append((label, fn, e.missing_translations))
        return fn

    hero = ('sections/hero.liquid', 'hero', HERO_SETTINGS)
    FC = 'sections/featured-collection.liquid'

    # The shipped home page: hero + New Drop + Best Sellers, with real collections.
    case('home', [
        hero,
        (FC, 'newdrop', {'collection': collection('the-faithful', [P_TEE, P_HOODIE, P_CAP])}),
        (FC, 'best', {'collection': collection('best-sellers', ALL[:4], 'Best Sellers'),
                      'eyebrow': 'Best Sellers /',
                      'heading': 'The Pieces That Define The Movement',
                      'description': 'Chosen by the community.',
                      'view_all_label': 'Shop All Best Sellers',
                      'surface': 'dark', 'layout': 'full-width',
                      'products_to_show': 4, 'columns_desktop': 4, 'anchor_id': ''}),
    ], fname='index.html')

    # Case 1 — nothing selected, live store: renders nothing at all.
    case('no collection live', [(FC, 'a', {'collection': None})], fname='case-nocollection-live.html')
    # Case 19 — nothing selected, Theme Editor: renders with a note.
    case('no collection editor', [(FC, 'a', {'collection': None})], design_mode=True,
         fname='case-nocollection-editor.html')
    # Collection selected but empty, in the editor.
    case('empty collection editor', [(FC, 'a', {'collection': collection('empty', [])})],
         design_mode=True, fname='case-emptycollection-editor.html')

    # Cases 3, 4, 5 — product counts.
    for n in (1, 2, 5, 12):
        case('count %d' % n, [(FC, 'c%d' % n, {
            'collection': collection('c', ALL[:n]), 'products_to_show': 12,
            'columns_desktop': 4, 'layout': 'full-width'})],
            fname='case-count-%d.html' % n)

    # Cases 6-14 — the hard product states, all in one grid so they can be compared.
    case('product states', [(FC, 'states', {
        'collection': collection('states', [P_TEE, P_HOODIE, P_CAP, P_LONG, P_NOIMG, P_VARIES, P_SINGLE, P_TEE]),
        'products_to_show': 8, 'columns_desktop': 4, 'layout': 'full-width',
        'heading': 'Every Card State'})], fname='case-states.html')

    # The same grid on the dark band.
    case('product states dark', [(FC, 'statesdark', {
        'collection': collection('states', [P_TEE, P_HOODIE, P_CAP, P_LONG, P_NOIMG, P_VARIES, P_SINGLE, P_TEE]),
        'products_to_show': 8, 'columns_desktop': 4, 'layout': 'full-width',
        'surface': 'dark', 'heading': 'Every Card State'})], fname='case-states-dark.html')

    # Column ceilings.
    for cd, ct, cm in ((4, 3, 2), (2, 2, 1), (3, 2, 2)):
        case('cols %d-%d-%d' % (cd, ct, cm), [(FC, 'g%d%d%d' % (cd, ct, cm), {
            'collection': collection('c', ALL), 'products_to_show': 8,
            'columns_desktop': cd, 'columns_tablet': ct, 'columns_mobile': cm,
            'layout': 'full-width'})], fname='case-cols-%d%d%d.html' % (cd, ct, cm))

    # Portrait ratio (the theme setting).
    case('portrait', [(FC, 'por', {
        'collection': collection('c', ALL[:4]), 'products_to_show': 4,
        'columns_desktop': 4, 'layout': 'full-width'})],
        extra_root='--product-aspect: var(--product-aspect-wide);',
        fname='case-portrait.html')

    # Quick add, which no shipped configuration turns on.
    e = make_engine()
    cards = []
    for p in (P_TEE, P_SINGLE, P_CAP):
        scope = {'product': p, 'quick_add': True, 'heading_level': 3,
                 'sizes': '(min-width: 1024px) 25vw, 50vw'}
        cards.append('<li class="product-grid__item">%s</li>' % e._render_with(
            Env([dict(e.globals), scope], e), 'snippets/product-card.liquid'))
    write('case-quickadd.html',
          '<div class="featured-collection surface-light featured-collection--pt-standard '
          'featured-collection--pb-standard"><div class="featured-collection__inner">'
          '<div class="featured-collection__products"><ul class="product-grid" role="list" '
          'style="--product-cols:3">%s</ul></div></div></div>' % ''.join(cards))
    results.append(('quick add', 'case-quickadd.html', e.missing_translations))

    print('%-28s %-34s %s' % ('CASE', 'FILE', 'MISSING TRANSLATIONS'))
    bad = 0
    for label, fn, miss in results:
        if miss:
            bad += 1
        print('%-28s %-34s %s' % (label, fn, sorted(set(miss)) or 'none'))
    print()
    print('pages written:', len(results), ' with missing translations:', bad)


if __name__ == '__main__':
    main()
