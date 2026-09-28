# -*- coding: utf-8 -*-
"""The caption rail's backing, from measurement.

Measured with the text hidden and the backdrop sampled under every glyph, the
caption rail came out at 1.69 / 2.07 / 2.14 / 1.86 to one at 1024 / 1280 / 1440
/ 1920, against the 4.5:1 a 12px tracked line needs. Every other role on the
band passed comfortably — eyebrow 11.01, heading 16.5-16.9, body 9.56-9.70,
values 9.70-11.01 — because they sit on flat ink or on the scrim's opaque end.
The rail is the one part of the composition that sits on open photograph.

The rail occupies 78% to 95% of the media's width, so the wash has to be dark
from about 77% rather than the 0.12 it held there. The ramp starts at 68% so
the change reads as the photograph fading out rather than as a panel behind
text.

This is the same decision Phase 4 took for the header: the contrast failure was
not optional, so the scrim is not optional either.
"""
p = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\section-our-story.css"
s = open(p, encoding='utf-8').read()

old_right = """  .our-story--image-right .our-story__scrim {
    background: linear-gradient(90deg,
      rgba(13, 12, 10, 1) 0%,
      rgba(13, 12, 10, 0.96) var(--os-wash-hold, 34%),
      rgba(13, 12, 10, 0.2) var(--os-wash-end, 62%),
      rgba(13, 12, 10, 0.12) 88%,
      rgba(13, 12, 10, 0.55) 100%);
  }"""
new_right = """  .our-story--image-right .our-story__scrim {
    background: linear-gradient(90deg,
      rgba(13, 12, 10, 1) 0%,
      rgba(13, 12, 10, 0.96) var(--os-wash-hold, 34%),
      rgba(13, 12, 10, 0.2) var(--os-wash-end, 62%),
      rgba(13, 12, 10, 0.12) 68%,
      rgba(13, 12, 10, 0.88) var(--os-rail-hold, 77%),
      rgba(13, 12, 10, 0.9) 100%);
  }"""

old_left = """  .our-story--image-left .our-story__scrim {
    background: linear-gradient(270deg,
      rgba(13, 12, 10, 1) 0%,
      rgba(13, 12, 10, 0.96) var(--os-wash-hold, 34%),
      rgba(13, 12, 10, 0.2) var(--os-wash-end, 62%),
      rgba(13, 12, 10, 0.12) 88%,
      rgba(13, 12, 10, 0.55) 100%);
  }"""
new_left = """  .our-story--image-left .our-story__scrim {
    background: linear-gradient(270deg,
      rgba(13, 12, 10, 1) 0%,
      rgba(13, 12, 10, 0.96) var(--os-wash-hold, 34%),
      rgba(13, 12, 10, 0.2) var(--os-wash-end, 62%),
      rgba(13, 12, 10, 0.12) 68%,
      rgba(13, 12, 10, 0.88) var(--os-rail-hold, 77%),
      rgba(13, 12, 10, 0.9) 100%);
  }"""

assert old_right in s and old_left in s, 'scrim rules not found'
s = s.replace(old_right, new_right, 1).replace(old_left, new_left, 1)

old_c = """  /* The scrim turns horizontal and always fades toward the copy. */"""
new_c = """  /* The scrim turns horizontal and always fades toward the copy, then darkens
     again under the caption rail.

     Both ends are measured, not styled. The copy end holds 0.96 to 34% because
     the copy column overlaps the photograph's inner edge. The rail end holds
     0.88 from 77% because the rail occupies 78% to 95% of the media and, left
     on open photograph, its cream 12px measured 1.69 to 2.14 against a 4.5:1
     requirement at every width tested. The 68% to 77% ramp is deliberately
     wide so the darkening reads as the picture fading out rather than as a
     panel dropped behind the text. */"""
assert old_c in s
s = s.replace(old_c, new_c, 1)
open(p, 'w', encoding='utf-8', newline='').write(s)
print('section-our-story.css: caption rail now has a measured backing')
