# -*- coding: utf-8 -*-
import os, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
from miniliquid import wrap

def run(label, values):
    opt = B.swatch_option('Colour', values)
    p = B.product('mix', 'Mixed Swatch Piece', 129000, options=[opt])
    coll = B.collection('mix', [p])
    e = B.make_engine(False)
    s = dict(B.SECTION_DEFAULTS); s['collection'] = coll; s['products_to_show'] = 1
    out = B.render_section(e, 'sections/featured-collection.liquid', 'mix', wrap(s))
    m = re.search(r'<div class="product-card__swatches">.*?</div>', out, re.S)
    print('=== ' + label)
    print(m.group(0) if m else 'NO SWATCH BLOCK')
    if m:
        hid = re.search(r'<span class="visually-hidden">(.*?)</span>', m.group(0), re.S)
        print('HIDDEN TEXT REPR:', repr(' '.join(hid.group(1).split())) if hid else None)
        print('DOT COUNT:', m.group(0).count('product-card__swatch"') + m.group(0).count('product-card__swatch '))
    print()

run('last value unswatched', [('Ink','#0D0C0A'), ('Cream','#F3EFE6'), ('Custom', None)])
run('middle value unswatched', [('Ink','#0D0C0A'), ('Custom', None), ('Cream','#F3EFE6')])
run('all swatched (control)', [('Ink','#0D0C0A'), ('Cream','#F3EFE6'), ('Olive','#4B5443')])
run('two swatched last unswatched x2', [('Ink','#0D0C0A'), ('Cream','#F3EFE6'), ('Custom', None), ('Other', None)])
