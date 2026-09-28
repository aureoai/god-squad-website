# -*- coding: utf-8 -*-
"""Measure the Our Story band's text contrast the way Phase 5 measured the hero.

Two renders per width: the page as shipped, and the same page with the text
elements set to visibility:hidden. For every pixel a glyph touches, the backdrop
colour is read from the text-hidden capture and measured against the element's
computed colour. Two figures are reported:

  glyph worst  the darkest-contrast pixel under an actual glyph (the WCAG one)
  box worst    the worst pixel anywhere inside the element's box, which is the
               headroom if a merchant types something longer
"""
import json, os, sys, io, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, r"C:\Users\TEST\AppData\Local\Temp\claude"
                   r"\C--Users-TEST-OneDrive-Documents-GodSquad-Website"
                   r"\de238d03-508d-43ce-a377-210f71ff0033\scratchpad")
from pngtool import read_png

HERE = os.path.dirname(os.path.abspath(__file__))
SH = os.path.join(HERE, 'shots')


def lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def L(p):
    return .2126 * lin(p[0]) + .7152 * lin(p[1]) + .0722 * lin(p[2])


def ratio(a, b):
    la, lb = L(a), L(b)
    if la < lb:
        la, lb = lb, la
    return (la + .05) / (lb + .05)


def parse(c):
    m = re.findall(r'[\d.]+', c)
    return (round(float(m[0])), round(float(m[1])), round(float(m[2])))


ROLES = [
    ('eyebrow', '.our-story__eyebrow', 4.5),
    ('heading', '.our-story__heading', 3.0),
    ('body', '.our-story__body', 4.5),
    ('caption', '.our-story__caption', 4.5),
    ('value title', '.our-story__value-title', 4.5),
    ('value body', '.our-story__value-body', 4.5),
]

boxes = json.load(open(os.path.join(HERE, 'roles.json')))
widths = sys.argv[1:] or sorted(boxes, key=int)

print('%6s %-13s %-16s %8s %7s %8s %5s  glyph   box' %
      ('w', 'role', 'fg', 'glyphpx', 'worst', 'boxworst', 'req'))
fails = 0
for wkey in widths:
    r = boxes[wkey]
    txt = read_png(os.path.join(SH, 'os-w%s.png' % wkey))
    bgi = read_png(os.path.join(SH, 'os-bg%s.png' % wkey))
    for name, sel, req in ROLES:
        box = r.get(name)
        col = r.get(name + '_color')
        if not box or not col:
            continue
        fg = parse(col)
        x0, y0 = max(0, box[0]), max(0, box[1])
        x1, y1 = min(txt.w, box[2]), min(txt.h, box[3])
        glyph, allbox = [], []
        for y in range(y0, y1):
            for x in range(x0, x1):
                b = bgi.px(x, y)
                t = txt.px(x, y)
                allbox.append(ratio(fg, b))
                if abs(t[0] - b[0]) + abs(t[1] - b[1]) + abs(t[2] - b[2]) > 8:
                    glyph.append(ratio(fg, b))
        if not glyph:
            continue
        g, a = sorted(glyph), sorted(allbox)
        gv, bv = g[0], a[0]
        ok = gv >= req
        okb = bv >= req
        if not ok:
            fails += 1
        print('%6s %-13s %-16s %8d %7.2f %8.2f %5.1f  %-5s  %s' %
              (wkey, name, '#%02X%02X%02X' % fg, len(g), gv, bv, req,
               'PASS' if ok else 'FAIL', 'PASS' if okb else 'FAIL'))
print()
print('glyph failures:', fails)
