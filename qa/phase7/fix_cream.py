# -*- coding: utf-8 -*-
"""Make the band work on the cream scheme, not only on ink.

Rendered with surface: light the band was broken three ways, all from one
cause: every scrim stop was the ink literal regardless of which surface the
band was on.

  1. The photograph faded into INK while the band around it was CREAM, so the
     picture ended on a hard dark rectangle instead of dissolving.
  2. That rectangle cut through the heading — the copy column reaches 464 and
     the photograph starts at 432, so "BIGGER PURPOSE." ran into an opaque
     dark edge and its last characters disappeared.
  3. The caption rail inherits the band's text colour, which on cream is ink.
     Ink text on the ink scrim is invisible.

The scrim's base colour now comes from a custom property the surface sets, so
it always fades into the band it is actually in.

Separately, the call to action cannot be the accent variant on cream. Phase 2
§10.1: gold on cream is 1.55:1, so the accent variant has no .surface-light
rule at all and the button would have rendered with no fill and no visible
border. §10.1 says the light-surface expression of the accent is a text link,
not a gold fill; the band's single CTA therefore becomes the primary variant
there, which §10.2 allows as the band's one primary.
"""
css = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\section-our-story.css"
sect = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\sections\our-story.liquid"

s = open(css, encoding='utf-8').read()

# 1. The scrim base colour follows the surface.
old = """.our-story {
  position: relative;
  width: 100%;
  isolation: isolate;
}"""
new = """.our-story {
  position: relative;
  width: 100%;
  isolation: isolate;
  /* The scrim's base colour. Every wash in this file fades into the band's own
     background, so the photograph dissolves into the band rather than into a
     colour the band is not. Written as channels because rgba() needs them
     separately; the two values are --gs-ink and --gs-cream, reached through
     the surface rather than through the palette. */
  --os-scrim-rgb: 13, 12, 10;
}

.our-story.surface-light {
  --os-scrim-rgb: 243, 239, 230;
}"""
assert old in s, 'band rule not found'
s = s.replace(old, new, 1)

# 2. Every ink literal becomes the property.
s = re._sre if False else s
import re as _re
count = len(_re.findall(r'rgba\(13, 12, 10,', s))
s = _re.sub(r'rgba\(13, 12, 10,', 'rgba(var(--os-scrim-rgb),', s)
print('scrim stops rebased:', count)

open(css, 'w', encoding='utf-8', newline='').write(s)
print('section-our-story.css: scrim follows the surface')

# 3. The CTA variant follows the surface.
t = open(sect, encoding='utf-8').read()
old_t = """  assign surface_class = 'surface-dark'
  if section.settings.surface == 'light'
    assign surface_class = 'surface-light'
  endif"""
new_t = """  assign surface_class = 'surface-dark'
  assign cta_variant = 'button--accent'
  if section.settings.surface == 'light'
    assign surface_class = 'surface-light'
    comment
      Gold on cream is 1.55:1, so Phase 2 §10.1 gives the accent variant no
      light-surface rule at all — used there it would render with no fill and
      no visible border. On cream the band's single call to action is the
      primary variant, which §10.2 permits as the band's one primary.
    endcomment
    assign cta_variant = 'button--primary'
  endif"""
assert old_t in t, 'surface assign not found'
t = t.replace(old_t, new_t, 1)

old_b = """        <a class="our-story__cta button button--accent" href="{{ btn_url }}">"""
new_b = """        <a class="our-story__cta button {{ cta_variant }}" href="{{ btn_url }}">"""
assert old_b in t, 'cta markup not found'
t = t.replace(old_b, new_b, 1)

old_c = """        {%- comment -%}
          The page's one gold call to action. Phase 2 §10.1 permits the accent
          variant on a dark surface only, where ink on gold is 11.01:1. The
          component has no light-surface rule, so choosing the cream scheme
          leaves the button transparent-bordered rather than illegible.
        {%- endcomment -%}"""
if old_c not in t:
    old_c = """        {%- comment -%}
          The page's one gold call to action. Phase 2 §10.1 permits the accent
          variant on a dark surface only, where ink on gold is 11.01:1; the
          component has no light-surface rule, so choosing the cream scheme
          leaves the button transparent-bordered rather than illegible.
        {%- endcomment -%}"""
new_c = """        {%- comment -%}
          On ink this is the page's one gold call to action, which Phase 2
          §10.1 permits on a dark surface only — ink on gold is 11.01:1 there.
          On cream the variant switches, for the reason recorded above.
        {%- endcomment -%}"""
assert old_c in t, 'cta comment not found'
t = t.replace(old_c, new_c, 1)
open(sect, 'w', encoding='utf-8', newline='').write(t)
print('our-story.liquid: CTA variant follows the surface')
