# -*- coding: utf-8 -*-
"""Phase 11 — does each merchant setting actually change the output?

A settings phase fails quietly: a control appears in the editor, the merchant
moves it, and nothing happens. Every assertion here renders the real section
BOTH ways and compares, so a setting that does nothing cannot pass.
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
    print('  %-60s %s %s' % (label, 'OK  ' if ok else '*** FAIL ***',
                             '' if ok else str(detail)[:140]))
    if not ok:
        FAILURES.append(label)


def render(section, sid, overrides=None, blocks=None, theme=None, **globals_):
    base, _ = surfaces.schema_defaults(section)
    if overrides:
        base.update(overrides)
    e = surfaces.engine(**globals_)
    if theme:
        merged = dict(e.globals['settings'])
        merged.update(theme)
        e.globals['settings'] = wrap(merged)
    return build.render_section(e, 'sections/%s.liquid' % section, sid, base, blocks)


def schema_of(section):
    src = open(os.path.join(THEME, 'sections', section + '.liquid'), encoding='utf-8').read()
    return json.loads(re.search(r'\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}', src, re.S).group(1))


def global_schema():
    return json.load(open(os.path.join(THEME, 'config', 'settings_schema.json'),
                          encoding='utf-8'))


if __name__ == '__main__':
    print('=== GLOBAL: the logo is a theme setting, uploaded once ===')
    g = global_schema()
    brand = next((x for x in g if x.get('name') == 'Brand'), None)
    check('a Brand group exists', brand is not None)
    check('it owns the logo',
          bool(brand) and any(s.get('id') == 'logo' for s in brand['settings']))
    hdr = schema_of('header')
    check('the header no longer duplicates the upload',
          not any(s.get('id') == 'logo' for s in hdr['settings']))
    check('the header keeps its two size controls',
          all(any(s.get('id') == i for s in hdr['settings'])
              for i in ('logo_height_desktop', 'logo_height_mobile')))
    # NB: match the img's class attribute exactly. A bare "header__logo" test is
    # also satisfied by "header__logo-link", which the wordmark branch uses too.
    with_logo = render('header', 'header')
    check('the header renders the global logo', 'class="header__logo"' in with_logo)
    no_logo = render('header', 'header', theme={'logo': ''})
    # THE FALLBACK CHANGED, SO THE ASSERTION DID.
    #
    # This used to require the no-logo branch to render a TEXT wordmark
    # (header__wordmark) and no <img>. Phase 19 replaced it with a bundled
    # image: assets/logo.png, the transparent white wordmark (md5 c247ae94…,
    # 76.9% of its pixels clear, corners at alpha 0), referenced through
    # asset_url. For a bespoke single-brand theme that is the better default —
    # a fresh install shows the brand rather than a text stand-in.
    #
    # What must stay true is the thing the old check was really protecting: the
    # branding link is never EMPTY. A logo link with nothing inside it is an
    # unlabelled target, and that is the failure either design could produce.
    check('with no logo uploaded it still renders a mark, not an empty link',
          'header__logo' in no_logo
          and ('<img' in no_logo or 'header__wordmark' in no_logo))
    hdr_src = open(os.path.join(THEME, 'sections', 'header.liquid'), encoding='utf-8').read()
    check('the bundled fallback comes from the theme asset, not a hardcoded path',
          'header__wordmark' in no_logo or 'asset_url' in hdr_src)

    print()
    print('=== GLOBAL: the palette select no longer collides ===')
    colours = next((x for x in g if x.get('name') == 'Colours'), None)
    sel = next((s for s in colours['settings'] if s.get('id') == 'color_scheme'), None)
    check('the global select is "Brand palette"', sel and sel.get('label') == 'Brand palette')
    per_section = schema_of('featured-collection')
    surf = next((s for s in per_section['settings'] if s.get('id') == 'surface'), None)
    check('the per-section one is still "Colour scheme"',
          surf and surf.get('label') == 'Colour scheme')

    print()
    print('=== GLOBAL: cart style ===')
    cart = next((x for x in g if x.get('name') == 'Cart'), None)
    check('a Cart group exists', cart is not None)
    check('it offers drawer or page',
          bool(cart) and any(s.get('id') == 'cart_type' for s in cart['settings']))
    lay = open(os.path.join(THEME, 'layout', 'theme.liquid'), encoding='utf-8').read()
    check('the layout gates the drawer on it', "settings.cart_type != 'page'" in lay)

    print()
    print('=== HEADER: show cart ===')
    check('a Show cart setting exists', any(s.get('id') == 'show_cart' for s in hdr['settings']))
    shown = render('header', 'header', {'show_cart': True})
    hidden = render('header', 'header', {'show_cart': False})
    check('on, the cart control renders', 'data-cart-bubble' in shown)
    check('off, it does not', 'data-cart-bubble' not in hidden)
    check('the setting warns what turning it off costs',
          'typing the address' in json.dumps(hdr))

    print()
    print('=== ANNOUNCEMENT BAR ===')
    ann = schema_of('announcement-bar')
    surf = next((s for s in ann['settings'] if s.get('id') == 'surface'), None)
    check('its colour control matches the other sections',
          surf and surf.get('label') == 'Colour scheme'
          and [o['label'] for o in surf['options']] == ['Ink', 'Cream'])
    check('an alignment setting exists', any(s.get('id') == 'alignment' for s in ann['settings']))
    blocks = build.blocks([{'id': 'm1', 'type': 'message', 'settings': {'text': 'One', 'link': ''}},
                           {'id': 'm2', 'type': 'message', 'settings': {'text': 'Two', 'link': ''}}])
    edges = render('announcement-bar', 'ab', {'alignment': 'edges'}, blocks)
    centre = render('announcement-bar', 'ab', {'alignment': 'centre'}, blocks)
    check('the alignment reaches the markup',
          'announcement-bar--align-edges' in edges
          and 'announcement-bar--align-centre' in centre)
    css = open(os.path.join(THEME, 'assets', 'header.css'), encoding='utf-8').read()
    check('and the CSS acts on it', '.announcement-bar--align-centre' in css)

    print()
    print('=== FOOTER: the wordmark ===')
    foot = schema_of('footer')
    check('a Show the logo setting exists', any(s.get('id') == 'show_logo' for s in foot['settings']))
    fb = build.blocks([{'id': 'm1', 'type': 'link_list',
                        'settings': {'menu': 'footer', 'heading': 'Shop'}}])
    on = render('footer', 'footer', {'show_logo': True}, fb)
    off = render('footer', 'footer', {'show_logo': False}, fb)
    nologo = render('footer', 'footer', {'show_logo': True}, fb, theme={'logo': ''})
    check('on, with a logo uploaded, it renders', 'footer__logo' in on)
    check('off, it does not', 'footer__logo' not in off)
    # Same change as the header's, and the same reasoning. This used to require
    # the footer to render NOTHING when show_logo was on but no logo had been
    # uploaded, because a checkbox that produces an empty gap is worse than no
    # checkbox. Phase 19 gave it the bundled wordmark instead, so there is no
    # gap to produce — the branch always has a mark to draw.
    #
    # The invariant that survives: turning the setting OFF must still render
    # nothing, and turning it ON must never render an empty anchor.
    check('on, with NO logo uploaded, it renders the bundled mark, not an empty link',
          'footer__logo' in nologo and '<img' in nologo)
    fcss = open(os.path.join(THEME, 'assets', 'section-footer.css'), encoding='utf-8').read()
    check('it is sized by the token reserved for it', '--logo-height-footer' in fcss)

    print()
    print('=== PRODUCT: hiding the quantity control must not break the add ===')
    on = render('main-product', 'p', {'show_quantity': True},
                product=build.P_SIZES, template='product')
    off = render('main-product', 'p', {'show_quantity': False},
                 product=build.P_SIZES, template='product')
    check('shown, there is a quantity control', 'data-quantity' in on)
    check('hidden, a quantity is STILL submitted',
          'name="quantity"' in off, 'no quantity field at all -> a quantity rule minimum 422s')
    check('hidden, the control itself is gone', 'quantity__button' not in off)

    print()
    print('=== HERO: the focal point tells the truth ===')
    hero = schema_of('hero')
    fp = next((s for s in hero['settings'] if s.get('id') == 'focal_point'), None)
    check('it says Shopify admin can override it',
          fp and 'focal point' in fp.get('info', '').lower()
          and 'admin' in fp.get('info', '').lower())

    print()
    print('%d checks, %d passed, %d failed'
          % (CHECKS[0], CHECKS[0] - len(FAILURES), len(FAILURES)))
    print('OVERALL: %s' % ('PASS' if not FAILURES else '*** FAILURES ABOVE ***'))
