# -*- coding: utf-8 -*-
"""Phase 11 — the global settings surface and the section settings that depend on it.

Each change traces to a confirmed audit finding, the Phase 11 spec, or Phase 1
section 29.6/29.7. Nothing here redesigns anything.
"""
import collections
import json
import os

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'god-squad-theme')
done = []


def patch(rel, old, new, label):
    p = os.path.join(THEME, rel)
    s = open(p, encoding='utf-8').read()
    assert s.count(old) == 1, 'NOT FOUND or ambiguous in %s: %s' % (rel, label)
    open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new, 1))
    done.append(label)


def od(*pairs):
    return collections.OrderedDict(pairs)


# ====================================================== config/settings_schema
p = os.path.join(THEME, 'config', 'settings_schema.json')
schema = json.load(open(p, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)

# --- 1. The logo becomes a BRAND setting, not a header setting ---------------
brand = next(g for g in schema if g.get('name') == 'Brand')
assert not any(s.get('id') == 'logo' for s in brand['settings']), 'logo already global'
brand['settings'].insert(0, od(
    ('type', 'paragraph'),
    ('content',
     'The wordmark, used by the header and — when you switch it on there — the '
     'footer. It is uploaded once, here, so the two can never drift apart.'),
))
brand['settings'].insert(1, od(
    ('type', 'image_picker'),
    ('id', 'logo'),
    ('label', 'Logo'),
    ('info',
     'A transparent PNG or, better, an SVG. Phase 3 records that the current '
     'wordmark carries heavy transparent padding, so it renders at roughly half '
     'its intended size until a vector master replaces it.'),
))
done.append('settings_schema.json: Brand now owns the logo')

# --- 2. The global palette select stops colliding with the per-section one ----
colours = next(g for g in schema if g.get('name') == 'Colours')
sel = next(s for s in colours['settings'] if s.get('id') == 'color_scheme')
assert sel['label'] == 'Colour scheme'
sel['label'] = 'Brand palette'
sel['info'] = (
    'The whole palette, chosen as one. Each section then picks which side of it '
    'to sit on with its own "Colour scheme" setting. '
    + sel['info']
)
done.append('settings_schema.json: the global select is "Brand palette", so it no longer '
            'collides with every section\'s "Colour scheme"')

# --- 3. A Cart group, which the spec names and the theme never had -----------
assert not any(g.get('name') == 'Cart' for g in schema), 'Cart group already present'
social_at = next(i for i, g in enumerate(schema) if g.get('name') == 'Social')
schema.insert(social_at, od(
    ('name', 'Cart'),
    ('settings', [
        od(('type', 'paragraph'),
           ('content',
            'How the cart opens. The slide-out drawer keeps the customer on the '
            'page they were browsing; the cart page is a full page of its own.')),
        od(('type', 'select'),
           ('id', 'cart_type'),
           ('label', 'Cart style'),
           ('options', [
               od(('value', 'drawer'), ('label', 'Slide-out drawer')),
               od(('value', 'page'), ('label', 'Cart page')),
           ]),
           ('default', 'drawer'),
           ('info',
            'With the cart page selected the drawer is not rendered at all, and '
            'the header cart control becomes an ordinary link to /cart.')),
    ]),
))
done.append('settings_schema.json: a Cart group with a drawer/page choice')

json.dump(schema, open(p, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
open(p, 'a', encoding='utf-8', newline='').write('\n')

# ======================================================== config/settings_data
p = os.path.join(THEME, 'config', 'settings_data.json')
data = json.load(open(p, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
for block in [data['current']] + [data['presets'][k] for k in data.get('presets', {})]:
    block.setdefault('cart_type', 'drawer')
    block.setdefault('logo', '')
json.dump(data, open(p, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
open(p, 'a', encoding='utf-8', newline='').write('\n')
done.append('settings_data.json: defaults for the new settings')

# ============================================================ layout/theme.liquid
patch('layout/theme.liquid',
      """    {%- unless template.name == 'cart' -%}
      {% section 'cart-drawer' %}
    {%- endunless -%}""",
      """    {%- comment -%}
      Phase 11 added the merchant's choice. With "Cart page" selected the drawer
      is not rendered at all — which is the whole switch, because assets/cart.js
      is already written to tolerate its absence: onOpenerClick returns early
      when Drawer.el is null, so the header control stays an ordinary link to
      the cart page, and the add-to-cart path gates auto-open on Drawer.el too.
    {%- endcomment -%}
    {%- if settings.cart_type != 'page' -%}
      {%- unless template.name == 'cart' -%}
        {% section 'cart-drawer' %}
      {%- endunless -%}
    {%- endif -%}""",
      'theme.liquid: the drawer renders only when the merchant wants a drawer')

# ============================================================ sections/header
# The logo comes from the theme setting now.
patch('sections/header.liquid',
      """            assign logo_alt = section.settings.logo.alt | default: shop.name""",
      """            assign logo_alt = settings.logo.alt | default: shop.name""",
      'header.liquid: the logo alt reads the global setting')

patch('sections/header.liquid',
      """          {{
            section.settings.logo
            | image_url: width: 600""",
      """          {{
            settings.logo
            | image_url: width: 600""",
      'header.liquid: the logo image reads the global setting')

hdr = os.path.join(THEME, 'sections', 'header.liquid')
s = open(hdr, encoding='utf-8').read()
s = s.replace('{%- if section.settings.logo != blank -%}', '{%- if settings.logo != blank -%}')
s = s.replace('{% if section.settings.logo != blank %}', '{% if settings.logo != blank %}')
open(hdr, 'w', encoding='utf-8', newline='').write(s)
done.append('header.liquid: the logo guard reads the global setting')

for i, label in enumerate(done, 1):
    print('%d. %s' % (i, label))
