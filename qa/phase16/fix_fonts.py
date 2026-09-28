# -*- coding: utf-8 -*-
"""Phase 16 — load the font weights the type system actually uses.

MEASURED: design-tokens.css defines four weights (400/500/600/900) and the type
scale spends three of them on the BODY family — --type-eyebrow-weight is 500,
--type-label-weight and --type-price-weight are 600 — across nineteen-plus rules
covering every label, price and eyebrow in the store.

layout/theme.liquid called font_face exactly twice, once per family, and each
call emits a face for the ONE variant in the setting: jost_n4 (400) and
playfair_display_n9 (900). So 500 and 600 had no @font-face at all and the
browser synthesised them from Jost 400 — faux bold, which is thicker, wider and
differently spaced than the real cut. On a brand whose whole type system is
labels in tracked caps, that is visible on every surface.

font_modify returns nil when a family has no such variant, so every call is
guarded: a merchant who picks a single-weight font gets the same rendering as
before rather than a broken @font-face.
"""
import io
import os

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
p = os.path.join(THEME, 'layout', 'theme.liquid')
s = io.open(p, encoding='utf-8').read()
n0 = len(s)

old = """    {% style %}
      {{ settings.type_display_font | font_face: font_display: 'swap' }}
      {{ settings.type_body_font | font_face: font_display: 'swap' }}
    {% endstyle %}"""

new = """    {%- comment -%}
      PHASE 16: THE WEIGHTS THE TYPE SYSTEM USES, NOT JUST THE ONES IT PICKS.

      These two calls emit a face for the ONE variant in each setting — jost_n4
      and playfair_display_n9. But design-tokens.css spends three weights on the
      body family: --type-eyebrow-weight is 500, and --type-label-weight and
      --type-price-weight are 600, between them covering every label, price and
      eyebrow in the theme. Neither had a face, so the browser synthesised them
      from Jost 400. Faux bold is thicker and wider than a real cut and tracks
      differently, which on a type system built out of tracked caps is visible
      on every surface.

      font_modify returns nil when the family has no such variant, so each is
      guarded: a merchant who picks a single-weight font gets exactly what they
      got before rather than a broken rule.

      Still inside one {% style %} — font_face returns a bare @font-face RULE,
      and the Phase 10 note below is the reason that matters.
    {%- endcomment -%}
    {%- liquid
      assign body_medium = settings.type_body_font | font_modify: 'weight', '500'
      assign body_semibold = settings.type_body_font | font_modify: 'weight', '600'
    -%}
    {% style %}
      {{ settings.type_display_font | font_face: font_display: 'swap' }}
      {{ settings.type_body_font | font_face: font_display: 'swap' }}
      {%- if body_medium %}
        {{ body_medium | font_face: font_display: 'swap' }}
      {%- endif %}
      {%- if body_semibold %}
        {{ body_semibold | font_face: font_display: 'swap' }}
      {%- endif %}
    {% endstyle %}"""

assert s.count(old) == 1
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new, 1))
print('layout/theme.liquid  %d -> %d bytes' % (n0, n0 - len(old) + len(new)))

# The harness fixture has to declare which variants exist, or font_modify cannot
# model the nil case that every guard above depends on.
for d in ('phase8', 'phase9'):
    bp = os.path.join(
        r"C:\Users\TEST\AppData\Local\Temp\claude\C--Users-TEST-OneDrive-Documents-GodSquad-Website\de238d03-508d-43ce-a377-210f71ff0033\scratchpad",
        d, 'build.py')
    b = io.open(bp, encoding='utf-8').read()
    old_f = """                          'type_body_font': wrap({
                              'family': 'Jost', 'weight': '400',
                              'fallback_families': 'sans-serif'})}),"""
    new_f = """                          'type_body_font': wrap({
                              'family': 'Jost', 'weight': '400',
                              # Phase 16: which cuts this family actually has,
                              # so font_modify can return nil for the ones it
                              # does not and the layout's guards are exercised.
                              'variants': ['400', '500', '600', '700'],
                              'fallback_families': 'sans-serif'})}),"""
    if old_f in b:
        io.open(bp, 'w', encoding='utf-8').write(b.replace(old_f, new_f, 1))
        print('%s/build.py: body font declares its variants' % d)
