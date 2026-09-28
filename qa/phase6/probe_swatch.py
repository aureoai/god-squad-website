# -*- coding: utf-8 -*-
import os, sys, json, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = r"C:\Users\TEST\AppData\Local\Temp\claude\C--Users-TEST-OneDrive-Documents-GodSquad-Website\de238d03-508d-43ce-a377-210f71ff0033\scratchpad\phase6"
sys.path.insert(0, HERE)
from miniliquid import Engine, wrap

THEME = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website"
TRANSLATIONS = json.load(open(os.path.join(THEME, 'locales', 'en.default.json'), encoding='utf-8'))

def swatch_option(name, values):
    return wrap({'name': name,
                 'values': [{'name': v, 'swatch': ({'color': c} if c else None)} for v, c in values]})

MIXED = swatch_option('Colour', [('Ink', '#0D0C0A'), ('Cream', '#F3EFE6'), ('Custom', None)])
MIXED_MID = swatch_option('Colour', [('Ink', '#0D0C0A'), ('Custom', None), ('Cream', '#F3EFE6')])
ALLSW = swatch_option('Colour', [('Ink', '#0D0C0A'), ('Cream', '#F3EFE6')])

def product(opts):
    return wrap({'title': 'Probe Tee', 'url': '/products/probe', 'handle': 'probe',
                 'price': 1000, 'price_min': 1000, 'price_max': 1000, 'price_varies': False,
                 'compare_at_price_max': 0, 'available': True,
                 'featured_image': wrap({'src': 'img/tee.webp', 'alt': 'x', 'width': 9, 'height': 9}),
                 'images': [], 'variants': [{'id': 1}],
                 'selected_or_first_available_variant': {'id': 1},
                 'options_with_values': [opts]})

g = {'settings': wrap({'product_image_ratio': 'square'}),
     'request': wrap({'design_mode': False, 'locale': {'iso_code': 'en'}}),
     'routes': wrap({'root_url': '/', 'cart_url': '/cart', 'cart_add_url': '/cart/add'}),
     'shop': wrap({'name': 'God Squad'}), 'cart': wrap({'item_count': 0}),
     'template': wrap({'name': 'index'})}

src = open(os.path.join(THEME, 'snippets', 'product-card.liquid'), encoding='utf-8').read()

for label, opt in (('ALL SWATCHED', ALLSW), ('TRAILING UNSWATCHED', MIXED), ('MIDDLE UNSWATCHED', MIXED_MID)):
    e = Engine(THEME, globals_=g, translations=TRANSLATIONS, asset_base='assets/')
    out = e.render(src, {'product': product(opt)})
    i = out.find('product-card__swatches')
    print('=== %s ===' % label)
    print(repr(out[i-20:i+420]))
    print()
