# -*- coding: utf-8 -*-
"""The HOME page, added to the Phase 8 harness.

Phase 8's harness rendered the product page and the cart. Phase 9 has to
measure the whole storefront at ten widths, so the hero, both collection rows
and the story band have to render too — from the same real .liquid files and
the same engine, not from a second set of fixtures.

The settings below are exactly what templates/index.json ships.
"""
import json, os, io, sys

# stdout is wrapped by build.py on import; wrapping it twice closes the first.
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build  # noqa: E402  the Phase 8 harness, reused whole
from miniliquid import wrap  # noqa: E402

THEME = build.THEME
INDEX = json.load(open(os.path.join(THEME, 'templates', 'index.json'), encoding='utf-8'))


def hero_image():
    return build.img('hero.webp', '', 1672, 941)


def story_image():
    return build.img('story.webp',
                     'God Squad community wearing faith-inspired streetwear', 535, 348)


def section_settings(key):
    """The shipped settings, with the two image pickers filled in — a merchant
    cannot ship an image_picker default, so index.json has none, and a harness
    that measured the empty state would measure the wrong page."""
    s = dict(INDEX['sections'][key].get('settings', {}))
    if key == 'hero':
        s.setdefault('image', None)
        s['image'] = hero_image()
        s['mobile_image'] = None
    if key == 'our-story':
        s['image'] = story_image()
        s['mobile_image'] = None
    if key == 'verse-feature':
        s['image'] = standin(0)
        s['mobile_image'] = None
    return s


def section_blocks(key):
    entry = INDEX['sections'][key]
    order = entry.get('block_order', [])
    blocks = entry.get('blocks', {})
    out = []
    for i, bid in enumerate(order):
        if bid not in blocks:
            continue
        settings = dict(blocks[bid].get('settings', {}))
        # Same reason as the section-level pickers above: an image_picker cannot
        # carry a default, so index.json ships none and a harness measuring the
        # empty state would measure the wrong page.
        if key in ('verse-index', 'words-we-wear'):
            settings['image'] = standin(i + 1)
        out.append({'id': bid, 'type': blocks[bid]['type'], 'settings': settings})
    return out


SECTION_FILE = {
    'hero': 'sections/hero.liquid',
    'new-drop': 'sections/featured-collection.liquid',
    'best-sellers': 'sections/featured-collection.liquid',
    'our-story': 'sections/our-story.liquid',
    'verse-feature': 'sections/verse-feature.liquid',
    'verse-index': 'sections/verse-index.liquid',
    'words-we-wear': 'sections/words-we-wear.liquid',
}

# THE VERSE BANDS' PHOTOGRAPHS ARE STAND-INS, AND DELIBERATELY NOT THE FILES IN
# brand-assets/verse images/. Those ten JPEGs are crops of a flattened mockup
# screenshot -- their own README says any typography baked into the screenshot
# survives the crop, and it does: 03_verse_faith_card.jpg already carries its
# own category, quote, reference and READ VERSE painted into the pixels, so
# using it behind the real markup would render every line twice. The harness
# reuses the clean product and lifestyle photographs it already has, cycling
# them, because what this preview is for is the LAYOUT. On a live store every
# one of these is an image_picker the merchant fills.
VERSE_STANDINS = ['hero.webp', 'story.webp', 'tee.webp', 'hoodie.webp', 'cap.webp']


def standin(i, alt=''):
    return build.img(VERSE_STANDINS[i % len(VERSE_STANDINS)], alt, 1200, 1600)


def render_home(collection, drawer_settings=None, cart=None, hero_overrides=None, order=None):
    """Every band templates/index.json lists, in its own order."""
    engine = build.make_engine(cart=cart or build.CART_EMPTY, template='index')
    # A `collection` setting arrives as the collection OBJECT, not a handle —
    # Shopify resolves the picker for the section. The fixture has to hand the
    # object over the same way, or the section's has_products guard sees blank
    # and renders nothing, which is what a first run of this harness measured.
    engine.globals['collections'] = wrap({collection['handle']: collection})

    header = '<div id="shopify-section-header" class="shopify-section">%s</div>' % (
        build.render_section(engine, 'sections/header.liquid', 'header',
                             dict(build.HEADER_SETTINGS, overlay_first_section=True)))
    drawer = '<div id="shopify-section-cart-drawer" class="shopify-section">%s</div>' % (
        build.render_section(engine, 'sections/cart-drawer.liquid', 'cart-drawer',
                             dict(build.DRAWER_DEFAULTS, **(drawer_settings or {}))))

    parts = []
    # Phase 11 made the home page reorderable in the Theme Editor, so the
    # harness has to be able to render it in an order other than the shipped one.
    for key in (order or INDEX['order']):
        settings = section_settings(key)
        # templates/index.json ships button_label with NO button_link, because a
        # merchant has to choose the collection — so has_cta is false and the
        # hero renders no button at all. Production WILL have one, and the
        # landscape hero has to be measured with it present rather than with the
        # shorter lockup the default fixture happens to produce.
        if key == 'hero' and hero_overrides:
            settings = dict(settings, **hero_overrides)
        if key in ('new-drop', 'best-sellers'):
            settings = dict(settings)
            settings['collection'] = collection
        parts.append((key, build.render_section(
            engine, SECTION_FILE[key], key, settings, section_blocks(key))))
    return header, drawer, parts, engine


# The header overlays the first section on the home page, so the harness page
# has to publish the same custom property the header's own <style> block does.
OVERLAY_STYLE = (
    '<style>:root{--header-overlay-offset:var(--header-height-mobile)}'
    '@media(min-width:1024px){:root{--header-overlay-offset:var(--header-height-desktop)}}</style>')


def write_home(name, collection, drawer_settings=None, cart=None, hero_overrides=None, order=None):
    header, drawer, parts, engine = render_home(collection, drawer_settings, cart, hero_overrides, order)
    body = '\n'.join(
        '<div id="shopify-section-%s" class="shopify-section">%s</div>' % (sid, html)
        for sid, html in parts)
    page = build.PAGE % {'body': body, 'header': header, 'drawer': drawer,
                         'footer': build.footer_group_html(engine, 'index'),
                         'headcss': build.layout_stylesheets(),
                         'template': 'index'}
    page = page.replace('</head>', OVERLAY_STYLE + '</head>', 1)
    open(os.path.join(build.OUT, name), 'w', encoding='utf-8').write(page)
    return list(engine.missing_translations)


if __name__ == '__main__':
    import shutil
    for f in ('section-hero.css', 'section-featured-collection.css',
              'section-our-story.css'):
        shutil.copy(os.path.join(THEME, 'assets', f),
                    os.path.join(build.OUT, 'assets', f))
    shutil.copy(os.path.join(build.PROJECT, 'brand-assets', 'phase-3-assets', 'hero',
                             'hero-walk-by-faith-desktop-1672w.webp'),
                os.path.join(build.OUT, 'img', 'hero.webp'))

    full = build.collection('the-faithful', [build.P_SIZES, build.P_MULTI,
                                             build.P_SINGLE, build.P_SOLDOUT])
    one = build.collection('one', [build.P_SIZES])
    three = build.collection('three', [build.P_SIZES, build.P_MULTI, build.P_SINGLE])
    eight = build.collection('eight', [build.P_SIZES, build.P_MULTI, build.P_SINGLE,
                                       build.P_SOLDOUT, build.P_LONG, build.P_RULE,
                                       build.P_SIZES, build.P_MULTI])

    cases = [
        ('home.html', full, None, None),
        ('home-one.html', one, None, None),
        ('home-three.html', three, None, None),
        ('home-eight.html', eight, None, None),
        ('home-cart.html', full, None, build.CART_MANY),
    ]
    cases.append(('home-cta.html', full, None, None))
    # The hero demoted out of first position: what a merchant sees after
    # dragging another section above it.
    cases.append(('home-reordered.html', full, None, None))
    print('%-22s %s' % ('FILE', 'MISSING TRANSLATIONS'))
    bad = 0
    for name, coll, drawer, cart in cases:
        hero_ov = {'button_link': '/collections/all'} if name in ('home-cta.html', 'home-reordered.html') else None
        order = None
        if name == 'home-reordered.html':
            order = [k for k in INDEX['order'] if k != 'hero']
            order.insert(1, 'hero')
        missing = write_home(name, coll, drawer, cart, hero_ov, order)
        if missing:
            bad += 1
        print('%-22s %s' % (name, ', '.join(sorted(set(missing))) or 'none'))
    print()
    print('home pages written: %d  with missing translations: %d' % (len(cases), bad))
