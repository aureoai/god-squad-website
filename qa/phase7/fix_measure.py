# -*- coding: utf-8 -*-
"""The backdrop capture must keep the caption's backing.

visibility:hidden is inherited by pseudo-elements, so hiding the caption also
hid the ::before that carries its wash. The backdrop then had no wash while the
text capture did, every changed pixel looked like a glyph, and the measurement
reported 14,000 "glyph" pixels at 1.4:1 — an artifact of the harness, not the
page. visibility is re-asserted on the pseudo-element so only the words go.
"""
p = (r"C:\Users\TEST\AppData\Local\Temp\claude"
     r"\C--Users-TEST-OneDrive-Documents-GodSquad-Website"
     r"\de238d03-508d-43ce-a377-210f71ff0033\scratchpad\phase7\measure_contrast.py")
s = open(p, encoding='utf-8').read()

old = """HIDE = ('<style>.our-story__eyebrow,.our-story__heading,.our-story__body,'
        '.our-story__caption,.our-story__value-title,.our-story__value-body'
        '{visibility:hidden}</style>')"""
new = """HIDE = ('<style>.our-story__eyebrow,.our-story__heading,.our-story__body,'
        '.our-story__caption,.our-story__value-title,.our-story__value-body'
        '{visibility:hidden}'
        # visibility is inherited by pseudo-elements, and the caption's wash
        # lives on one. Without this the backdrop loses the wash the real page
        # has and every washed pixel counts as a glyph.
        '.our-story__caption::before,.our-story__caption::after'
        '{visibility:visible}</style>')"""
assert old in s, 'HIDE block not found'
open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new, 1))
print('measure_contrast.py: backdrop keeps the rail wash')
