# -*- coding: utf-8 -*-
"""Sample the rendered pixels of every text role in the two new bands."""
import sys, os, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, r"C:\Users\TEST\AppData\Local\Temp\claude\C--Users-TEST-OneDrive-Documents-GodSquad-Website\de238d03-508d-43ce-a377-210f71ff0033\scratchpad")
from pngtool import read_png

def lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def L(p): return .2126*lin(p[0]) + .7152*lin(p[1]) + .0722*lin(p[2])
def ratio(a, b):
    la, lb = L(a), L(b)
    if la < lb: la, lb = lb, la
    return (la + .05) / (lb + .05)

SH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shots')
boxes = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'roles.json')))
im = read_png(os.path.join(SH, sys.argv[1]))

print(f"{'role':<28} {'fg':<16} {'bg':<16} {'px':>6} {'worst':>7} {'req':>5}  verdict")
for r in boxes:
    x0, y0, x1, y1 = r['box']
    x1 = min(x1, im.w); y1 = min(y1, im.h)
    px = [im.px(x, y) for y in range(y0, y1) for x in range(x0, x1)]
    if not px:
        print(f"{r['role']:<28} EMPTY BOX"); continue
    # Text pixels are the ones closest to the declared foreground; background
    # pixels are the ones closest to the declared background. Everything in
    # between is antialiasing and is excluded.
    fg = tuple(r['fg']); bg = tuple(r['bg'])
    def near(p, c, tol): return all(abs(p[i]-c[i]) <= tol for i in range(3))
    core = [p for p in px if near(p, fg, 20)]
    ground = [p for p in px if near(p, bg, 12)]
    if not core or not ground:
        print(f"{r['role']:<28} {str(fg):<16} {str(bg):<16} {len(px):>6}  core={len(core)} ground={len(ground)}  NOT FOUND")
        continue
    worst = min(ratio(c, g) for c in core[:400] for g in ground[:400])
    req = r['req']
    print(f"{r['role']:<28} {str(fg):<16} {str(bg):<16} {len(core):>6} {worst:>7.2f} {req:>5}  {'PASS' if worst >= req else '*** FAIL ***'}")
