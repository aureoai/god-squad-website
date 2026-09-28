# -*- coding: utf-8 -*-
"""Separate the THEME root from the PROJECT root in the harnesses.

Phase 10 moved the theme into god-squad-theme/. Fixture imagery did NOT move:
Phase 1 section 29.1 is explicit that nothing from images/ or the project root
is copied into the theme, because content images reach the page through
image_picker settings and Shopify Files rather than through assets/.
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OLD_THEME = 'THEME = r"C:\\Users\\TEST\\OneDrive\\Documents\\GodSquad Website\\god-squad-theme"'
NEW_BLOCK = (
    'THEME = r"C:\\Users\\TEST\\OneDrive\\Documents\\GodSquad Website\\god-squad-theme"\n'
    '# Fixture imagery lives OUTSIDE the theme. Phase 1 section 29.1: nothing from\n'
    '# images/ or the project root is copied into the theme, because content images\n'
    '# reach the page through image_picker settings and Shopify Files.\n'
    'PROJECT = r"C:\\Users\\TEST\\OneDrive\\Documents\\GodSquad Website"'
)

for rel in ('phase8/build.py', 'phase9/build.py'):
    p = os.path.join(BASE, rel)
    s = open(p, encoding='utf-8').read()
    assert s.count(OLD_THEME) == 1, 'THEME constant not found in ' + rel
    s = s.replace(OLD_THEME, NEW_BLOCK, 1)
    s = s.replace("os.path.join(THEME, 'images'", "os.path.join(PROJECT, 'brand-assets', 'images'")
    open(p, 'w', encoding='utf-8', newline='').write(s)
    print('patched', rel)

p = os.path.join(BASE, 'phase9/home.py')
s = open(p, encoding='utf-8').read()
s = s.replace("os.path.join(THEME, 'phase-3-assets'",
              "os.path.join(build.PROJECT, 'brand-assets', 'phase-3-assets'")
open(p, 'w', encoding='utf-8', newline='').write(s)
print('patched phase9/home.py')
