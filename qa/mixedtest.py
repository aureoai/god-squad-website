# -*- coding: utf-8 -*-
import sys, os
H = r"C:\Users\TEST\AppData\Local\Temp\claude\C--Users-TEST-OneDrive-Documents-GodSquad-Website\de238d03-508d-43ce-a377-210f71ff0033\scratchpad\phase6"
sys.path.insert(0, H)
os.chdir(H)
import build

MIXED = build.swatch_option('Colour', [('Ink', '#0D0C0A'), ('Cream', '#F3EFE6'), ('Custom', None)])
MIXED_MID = build.swatch_option('Colour', [('Ink', '#0D0C0A'), ('Custom', None), ('Cream', '#F3EFE6')])
ALLSW = build.swatch_option('Colour', [('Ink', '#0D0C0A'), ('Cream', '#F3EFE6')])

e = build.make_engine()
buf = []
for label, opt in (('LAST VALUE NO SWATCH', MIXED), ('MIDDLE VALUE NO SWATCH', MIXED_MID), ('ALL SWATCHES', ALLSW)):
    p = build.product('mixed', 'Mixed Option Piece', 129000,
                      images=[build.img('tee.webp', 'Mixed Option Piece', 900, 900)],
                      options=[opt], variants=[{'id': 1}, {'id': 2}, {'id': 3}])
    out = e.render("{% render 'product-card', product: prod %}", {'prod': p})
    i = out.find('product-card__swatches')
    buf.append('=== ' + label + ' ===')
    buf.append(out[i-30:i+800] if i >= 0 else '(no swatch block rendered)')
    buf.append('')
open(os.path.join(H, '..', 'mixedout.txt'), 'w', encoding='utf-8').write('\n'.join(buf))
