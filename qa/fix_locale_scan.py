# -*- coding: utf-8 -*-
"""Scan EVERY Liquid file for translation usage, not a hand-written list.

Phase 8 enumerated the files it had just written. Phase 10 added five sections
and a snippet, so a fixed list reported all 39 new keys as unused — a false
failure of exactly the kind this project keeps hitting whenever a check names
files instead of discovering them.
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(BASE, 'phase8', 'validate.py')
s = open(p, encoding='utf-8').read()

OLD = """sources = ''.join(R(p) for p in
                  [f'sections/{n}.liquid' for n in NEW_SECTIONS]
                  + [f'snippets/{n}.liquid' for n in NEW_SNIPPETS]
                  + ['sections/header.liquid', 'sections/featured-collection.liquid',
                     'sections/our-story.liquid', 'sections/hero.liquid',
                     'sections/announcement-bar.liquid', 'snippets/product-card.liquid',
                     'layout/theme.liquid'])"""

NEW = """# Every Liquid file in the theme, discovered rather than listed. A hand-written
# list silently reports each new section's keys as unused the moment a later
# phase adds one, which is what Phase 10 hit with 39 false positives.
_liquid = []
for _dirname in ('sections', 'snippets', 'layout'):
    _d = os.path.join(THEME, _dirname)
    if os.path.isdir(_d):
        for _f in sorted(os.listdir(_d)):
            if _f.endswith('.liquid'):
                _liquid.append('%s/%s' % (_dirname, _f))
sources = ''.join(R(p) for p in _liquid)"""

assert s.count(OLD) == 1, 'translation source list not found verbatim'
open(p, 'w', encoding='utf-8', newline='').write(s.replace(OLD, NEW, 1))
print('validate.py: translation scan now discovers all %s Liquid files' % 'theme')
