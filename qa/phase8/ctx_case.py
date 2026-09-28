# -*- coding: utf-8 -*-
"""Render one extra product case: the CONTEXTUAL-availability scenario that
Shopify's own product_option_value.available docs describe ("in the context of
the selected values for previous options").

Colour: Ink (selected), Olive     -- both have a purchaseable combination
Size:   S, L                      -- in the context of Ink, L is NOT purchaseable

Variants: Ink/S ok, Ink/L sold out, Olive/S ok, Olive/L ok

So Liquid marks Size L unavailable on load, and choosing Olive makes it
purchaseable again. Nothing here is hand-written markup: the real
sections/main-product.liquid and snippets/product-variant-picker.liquid render it.
"""
import build
from build import option, option_value, variant, product, media, case, PRODUCT_DEFAULTS

COLOURS = [option_value('Ink', colour='#0D0C0A', selected=True),
           option_value('Olive', colour='#4B5443')]
# In the context of Ink, L has no purchaseable combination -> available False.
SIZES = [option_value('S', selected=True), option_value('L', available=False)]

VARIANTS = [
    variant(9401, 'Ink / S',   ['Ink', 'S'],   249000, available=True,  handle='ctx-hoodie', sku='GS-CTX-IN-S'),
    variant(9402, 'Ink / L',   ['Ink', 'L'],   249000, available=False, handle='ctx-hoodie', sku='GS-CTX-IN-L'),
    variant(9403, 'Olive / S', ['Olive', 'S'], 249000, available=True,  handle='ctx-hoodie', sku='GS-CTX-OL-S'),
    variant(9404, 'Olive / L', ['Olive', 'L'], 249000, available=True,  handle='ctx-hoodie', sku='GS-CTX-OL-L'),
]

P_CTX = product(
    'ctx-hoodie', 'Contextual Availability Hoodie', VARIANTS,
    media=[media(401, 'hoodie.webp', 'Contextual Hoodie', 900, 900)],
    description='<p>Scenario fixture.</p>', type='Hoodie',
    options=[option('Colour', 1, COLOURS, 'Ink'),
             option('Size', 2, SIZES, 'S')],
    selected=VARIANTS[0])

case('contextual availability', 'p-ctx.html', P_CTX)
print('wrote site/p-ctx.html')
