# -*- coding: utf-8 -*-
"""The display heading must be hard-broken, not left to wrap.

Measured: "Real People. Bigger Purpose." came out on THREE lines at every width
from 320 to 1920 — the copy track is 397px at 1440 and "BIGGER PURPOSE." needs
about 420px at the 40px story scale, so the browser broke it after "BIGGER".
Phase 1 STORY-05 recorded exactly this in the prototype (three lines at 1440,
four at 1024, against the mockup's two) and asked Phase 7 to keep the explicit
break after "Real People." as the only break.

Phase 2 §26.1 already specifies the display headline as "2-4 words, hard-broken
with <br>". The fix is therefore to give the merchant the break rather than a
wider column: the field becomes a textarea and its newlines become breaks, the
same pattern the caption rail already uses. Widening the column instead would
have pushed the photograph out of the composition to solve a typesetting
problem.
"""
sect = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\sections\our-story.liquid"
css = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\section-our-story.css"

s = open(sect, encoding='utf-8').read()

# Render the break.
old = """        <h2 class="our-story__heading">{{ heading }}</h2>"""
new = """        {%- comment -%}
          The break is the merchant's, not the browser's. Phase 2 §26.1 defines
          the display headline as hard-broken; left to wrap, "Real People.
          Bigger Purpose." came out on three lines at every width measured,
          which is the defect Phase 1 STORY-05 recorded.
        {%- endcomment -%}
        <h2 class="our-story__heading">{{ heading | newline_to_br }}</h2>"""
assert old in s, 'heading markup not found'
s = s.replace(old, new, 1)

# The setting becomes a textarea so the editor can hold the break.
old2 = """    {
      "type": "text",
      "id": "heading",
      "label": "Heading",
      "default": "Real People. Bigger Purpose.",
      "info": "Renders as a level-2 heading. The page's only level-1 heading belongs to the hero."
    },"""
new2 = """    {
      "type": "textarea",
      "id": "heading",
      "label": "Heading",
      "default": "Real People.\\nBigger Purpose.",
      "info": "Renders as a level-2 heading. The page's only level-1 heading belongs to the hero. Each line you type becomes a line of the heading, so the break is yours rather than the browser's."
    },"""
assert old2 in s, 'heading setting not found'
s = s.replace(old2, new2, 1)

s = s.replace('"heading": "Real People. Bigger Purpose.",',
              '"heading": "Real People.\\nBigger Purpose.",', 1)
open(sect, 'w', encoding='utf-8', newline='').write(s)
print('our-story.liquid: heading is hard-broken')

# The 14ch cap was there to force a break the markup now carries.
c = open(css, encoding='utf-8').read()
old3 = """.our-story__heading {
  margin: var(--space-5) 0 0;
  max-width: 14ch;"""
new3 = """.our-story__heading {
  margin: var(--space-5) 0 0;
  /* No character cap: the break is in the markup now, so a cap here would only
     introduce a second, accidental one. */"""
assert old3 in c, 'heading rule not found'
open(css, 'w', encoding='utf-8', newline='').write(c.replace(old3, new3, 1))
print('section-our-story.css: character cap removed from the heading')
