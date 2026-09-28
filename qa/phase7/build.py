# -*- coding: utf-8 -*-
"""
Phase 7 render harness.

Renders the REAL sections/*.liquid and snippets/*.liquid through miniliquid
against mock Shopify data, and writes one static page per test case. The mock
data exists only here, in the scratchpad; nothing in the theme knows about it.

The story image used is the CANONICAL one the Phase 3 manifest identifies —
images/our-story.webp, the three-model composition — not the wrong hero crop
the prototype had in the slot.
"""
import os, sys, json, io, shutil

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from miniliquid import Engine, wrap, Env

THEME = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website"
OUT = os.path.join(HERE, 'site')
os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
os.makedirs(os.path.join(OUT, 'img'), exist_ok=True)

for f in ('design-tokens.css', 'header.css', 'section-hero.css',
          'component-button.css', 'component-product-card.css',
          'section-featured-collection.css', 'section-our-story.css'):
    shutil.copy(os.path.join(THEME, 'assets', f), os.path.join(OUT, 'assets', f))
shutil.copy(os.path.join(THEME, 'images', 'logo.png'), os.path.join(OUT, 'img', 'logo.png'))
shutil.copy(os.path.join(THEME, 'phase-3-assets', 'hero', 'hero-walk-by-faith-desktop-1672w.webp'),
            os.path.join(OUT, 'img', 'hero.webp'))
# The canonical story asset (PHASE-3-ASSET-MANIFEST.csv: images/our-story.webp,
# 535x348, the three-model composition). Deliberately NOT the hero crop the
# prototype used, which has headline fragments baked into its pixels.
shutil.copy(os.path.join(THEME, 'images', 'our-story.webp'), os.path.join(OUT, 'img', 'story.webp'))
# The wrong asset, kept only so the documentation can show what was replaced.
shutil.copy(os.path.join(THEME, '01-hero-model-mu98p88t-7jig.webp'),
            os.path.join(OUT, 'img', 'story-wrong.webp'))
for src, dst in (('product-tee.webp', 'tee.webp'),
                 ('product-hoodie.webp', 'hoodie.webp'),
                 ('product-cap.webp', 'cap.webp')):
    shutil.copy(os.path.join(THEME, 'images', src), os.path.join(OUT, 'img', dst))

TRANSLATIONS = json.load(open(os.path.join(THEME, 'locales', 'en.default.json'), encoding='utf-8'))


def img(src, alt, w, h):
    return wrap({'src': 'img/' + src, 'alt': alt, 'width': w, 'height': h})


STORY_IMG = img('story.webp', 'God Squad community wearing faith-inspired streetwear', 535, 348)
STORY_IMG_NOALT = img('story.webp', '', 535, 348)
STORY_MOBILE = img('hero.webp', 'God Squad community', 1672, 941)


def product(handle, title, price, **kw):
    images = kw.get('images', [img('tee.webp', title, 900, 900)])
    return wrap({
        'title': title, 'url': '/products/' + handle, 'handle': handle,
        'price': price, 'price_min': kw.get('price_min', price),
        'price_max': kw.get('price_max', price),
        'price_varies': kw.get('price_varies', False),
        'compare_at_price_max': kw.get('compare_at', 0),
        'available': kw.get('available', True),
        'featured_image': images[0] if images else None, 'images': images,
        'variants': kw.get('variants', [{'id': 1}]),
        'selected_or_first_available_variant': {'id': 1},
        'options_with_values': kw.get('options', []),
    })


def swatch_option(name, values):
    return wrap({'name': name,
                 'values': [{'name': v, 'swatch': ({'color': c} if c else None)} for v, c in values]})


COLOURS = swatch_option('Colour', [('Ink', '#0D0C0A'), ('Cream', '#F3EFE6'), ('Olive', '#4B5443')])
P1 = product('tee', 'Signature Oversized Tee', 129000,
             images=[img('tee.webp', 'Signature Oversized Tee', 900, 900)], options=[COLOURS])
P2 = product('hoodie', 'Heavyweight Hoodie', 249000,
             images=[img('hoodie.webp', 'Heavyweight Hoodie', 900, 900)], compare_at=299000)
P3 = product('cap', 'Utility Cap', 89000,
             images=[img('cap.webp', 'Utility Cap', 900, 900)], available=False)
P4 = product('crew', 'Faith Crew', 169000, images=[img('tee.webp', 'Faith Crew', 900, 900)])


def collection(handle, products, title='The Faithful'):
    return wrap({'handle': handle, 'title': title, 'url': '/collections/' + handle,
                 'products': products, 'products_count': len(products)})


def make_engine(design_mode=False):
    g = {
        'settings': wrap({'container_width': 1440, 'radius_sm': 2,
                          'product_image_ratio': 'square'}),
        'request': wrap({'design_mode': design_mode, 'locale': {'iso_code': 'en'}}),
        'routes': wrap({'root_url': '/', 'cart_url': '/cart', 'cart_add_url': '/cart/add',
                        'search_url': '/search', 'account_url': '/account'}),
        'shop': wrap({'name': 'God Squad', 'customer_accounts_enabled': True}),
        'cart': wrap({'item_count': 0}),
        'template': wrap({'name': 'index'}),
    }
    return Engine(THEME, globals_=g, translations=TRANSLATIONS, asset_base='assets/')


HERO = {
    'image': img('hero.webp', '', 1672, 941), 'mobile_image': None,
    'focal_point': 'centre-left', 'overlay': 'medium',
    'eyebrow': 'Streetwear With A Purpose.', 'heading': 'Walk By',
    'heading_accent': 'Faith.', 'scripture': '2 Corinthians 5:7',
    'description': 'Different People. Same Purpose.',
    'button_label': 'Shop The Collection', 'button_link': '',
    'height': 'medium', 'text_position': 'centre', 'text_alignment': 'left',
}

FC = {
    'collection': None, 'products_to_show': 3,
    'eyebrow': 'New Drop /', 'heading': 'The Faithful',
    'description': 'Premium Essentials for a Higher Purpose.',
    'show_view_all': True, 'view_all_label': 'View All Products', 'view_all_url': '',
    'surface': 'light', 'layout': 'with-copy-column',
    'columns_desktop': 3, 'columns_tablet': 2, 'columns_mobile': 2,
    'show_price': True, 'show_compare_at_price': True, 'show_swatches': True,
    'spacing_top': 'standard', 'spacing_bottom': 'standard', 'anchor_id': 'shop',
}

BODY = ('<p>God Squad is a Philippine streetwear brand built on faith, creativity, '
        'and community. We create pieces that inspire a generation to live different '
        '\u2014 with purpose.</p>')

OS = {
    'eyebrow': 'Our Story',
    'heading': 'Real People.' + chr(10) + 'Bigger Purpose.',
    'body': BODY,
    'image': STORY_IMG, 'mobile_image': None,
    'image_side': 'right',
    'button_label': 'Discover Our Story', 'button_url': '',
    'show_caption': True, 'caption': chr(10).join(['Faith', 'Lives', 'Different', 'Here.']),
    'surface': 'dark', 'spacing_top': 'standard', 'spacing_bottom': 'standard',
    'anchor_id': 'story',
}

# The prototype's own value copy (God Squad Website.html lines 180-183), minus
# "Worldwide / Shipping Available", which Phase 1 VAL-04 holds as an unverified
# commercial promise. This is what templates/index.json ships.
VALUES = [
    {'id': 'faith', 'type': 'value',
     'settings': {'title': 'Faith Driven', 'body': 'More Than Clothing'}},
    {'id': 'community', 'type': 'value',
     'settings': {'title': 'Community', 'body': 'People With Purpose'}},
    {'id': 'quality', 'type': 'value',
     'settings': {'title': 'Premium Quality', 'body': 'Crafted To Inspire'}},
]


def blocks(items):
    return [wrap({'id': b['id'], 'type': b['type'], 'settings': b['settings'],
                  'shopify_attributes': ''}) for b in items]


def render_section(engine, relpath, sid, settings, blks=None):
    scope = {'section': wrap({'id': sid, 'settings': wrap(settings),
                              'blocks': blocks(blks or []),
                              'shopify_attributes': ''})}
    src = open(os.path.join(THEME, relpath), encoding='utf-8').read()
    return engine.render(src, scope)


HEADER = open(os.path.join(HERE, 'header.html'), encoding='utf-8').read()

PAGE = """<!doctype html>
<html lang="en" class="no-js"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>God Squad — Phase 7 harness</title>
<link rel="stylesheet" href="assets/design-tokens.css">
<link rel="stylesheet" href="assets/header.css">
<link rel="stylesheet" href="assets/component-button.css">
<style>:root{--header-overlay-offset:var(--header-height-mobile)}@media(min-width:1024px){:root{--header-overlay-offset:var(--header-height-desktop)}}:root{%(extra_root)s}</style>
<script>document.documentElement.classList.replace('no-js','js');</script>
</head><body class="template-index">
<a class="skip-link" href="#MainContent">Skip to content</a>
%(header)s
<main id="MainContent" tabindex="-1">
%(body)s
</main></body></html>
"""


def write(name, parts, extra_root='', header=True):
    body = '\n'.join(
        '<section id="shopify-section-%s" class="shopify-section">%s</section>' % (sid, html)
        for sid, html in parts)
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(
        PAGE % {'body': body, 'header': HEADER if header else '', 'extra_root': extra_root})
    return name


def main():
    results = []

    def case(label, specs, design_mode=False, fname=None, extra_root='', header=True):
        e = make_engine(design_mode)
        parts = []
        for relpath, sid, settings, blks in specs:
            parts.append((sid, render_section(e, relpath, sid, settings, blks)))
        fn = fname or (label.replace(' ', '-').lower() + '.html')
        write(fn, parts, extra_root=extra_root, header=header)
        results.append((label, fn, sorted(set(e.missing_translations))))
        return fn

    HERO_S = ('sections/hero.liquid', 'hero', HERO, None)
    FCL = 'sections/featured-collection.liquid'
    OSL = 'sections/our-story.liquid'

    def os_case(**over):
        s = dict(OS)
        s.update(over)
        return s

    # The shipped home page, end to end.
    case('home', [
        HERO_S,
        (FCL, 'newdrop', dict(FC, collection=collection('the-faithful', [P1, P2, P3])), None),
        (FCL, 'best', dict(FC, collection=collection('best', [P1, P2, P3, P4], 'Best Sellers'),
                           eyebrow='Best Sellers /',
                           heading='The Pieces That Define The Movement',
                           description='Chosen by the community.',
                           view_all_label='Shop All Best Sellers',
                           surface='dark', layout='full-width',
                           products_to_show=4, columns_desktop=4, anchor_id=''), None),
        (OSL, 'story', OS, VALUES),
    ], fname='index.html')

    # The section alone, so its own geometry can be measured without the rest.
    case('story only', [(OSL, 'story', OS, VALUES)], fname='case-story.html')

    # 5. Desktop image only (the shipped default) is covered above.
    # 6. Desktop + mobile image.
    case('mobile image', [(OSL, 'story', os_case(mobile_image=STORY_MOBILE), VALUES)],
         fname='case-mobile-image.html')

    # Image on the left.
    case('image left', [(OSL, 'story', os_case(image_side='left'), VALUES)],
         fname='case-image-left.html')

    # 4. No image, live store -> renders nothing. In the editor -> a note.
    case('no image live', [(OSL, 'story', os_case(image=None), VALUES)],
         fname='case-noimage-live.html')
    case('no image editor', [(OSL, 'story', os_case(image=None), VALUES)],
         design_mode=True, fname='case-noimage-editor.html')

    # Image with no alt text, in the editor.
    case('no alt editor', [(OSL, 'story', os_case(image=STORY_IMG_NOALT), VALUES)],
         design_mode=True, fname='case-noalt-editor.html')

    # 10 / 11. CTA absent (no url) and present.
    case('cta present', [(OSL, 'story', os_case(button_url='/pages/our-story'), VALUES)],
         fname='case-cta.html')
    case('cta label no url editor', [(OSL, 'story', OS, VALUES)],
         design_mode=True, fname='case-cta-nourl-editor.html')

    # 7 / 8. Long and short heading.
    case('long heading', [(OSL, 'story', os_case(
        heading='Different People Walking Forward With The Same Higher Purpose And Conviction'), VALUES)],
        fname='case-long-heading.html')
    case('short heading', [(OSL, 'story', os_case(heading='Faith.'), VALUES)],
         fname='case-short-heading.html')

    # 8a. Six value blocks, the schema's limit. The row must not leave one tile
    # alone on a second line at any width.
    six = VALUES + [
        {'id': 'v4', 'type': 'value', 'settings': {'title': 'Four', 'body': 'Fourth line.'}},
        {'id': 'v5', 'type': 'value', 'settings': {'title': 'Five', 'body': 'Fifth line.'}},
        {'id': 'v6', 'type': 'value', 'settings': {'title': 'Six', 'body': 'Sixth line.'}},
    ]
    case('six values', [(OSL, 'story', os_case(), six)], fname='case-values6.html')

    # 8b. Heading cleared, values kept. The tiles must not hang off the hero's
    # h1 as h3s with the h2 gone, so their level follows the heading.
    case('no heading with values', [(OSL, 'story', os_case(heading=''), VALUES)],
         fname='case-no-heading.html')

    # 9. Long body copy — four paragraphs, the brief's stated maximum.
    long_body = BODY + (
        '<p>The clothing is part of the expression. The purpose comes first.</p>'
        '<p>Every piece is made to be worn by people who have decided what they stand for '
        'and are not quiet about it.</p>'
        '<p>Different people. Same purpose.</p>')
    case('long body', [(OSL, 'story', os_case(body=long_body), VALUES)],
         fname='case-long-body.html')

    # Caption off, and no value blocks.
    case('no caption', [(OSL, 'story', os_case(show_caption=False), VALUES)],
         fname='case-no-caption.html')
    case('no values', [(OSL, 'story', OS, [])], fname='case-no-values.html')

    # The cream scheme, where gold must not be the button fill.
    case('cream surface', [(OSL, 'story', os_case(surface='light'), VALUES)],
         fname='case-cream.html')

    # 16 / 17. Section reordered to first (header clearance) and removed.
    case('story first', [(OSL, 'story', OS, VALUES)], fname='case-story-first.html')
    case('story removed', [
        HERO_S,
        (FCL, 'newdrop', dict(FC, collection=collection('the-faithful', [P1, P2, P3])), None),
    ], fname='case-story-removed.html')

    print('%-26s %-34s %s' % ('CASE', 'FILE', 'MISSING TRANSLATIONS'))
    bad = 0
    for label, fn, miss in results:
        if miss:
            bad += 1
        print('%-26s %-34s %s' % (label, fn, miss or 'none'))
    print()
    print('pages written:', len(results), ' with missing translations:', bad)


if __name__ == '__main__':
    main()
