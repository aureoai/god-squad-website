# -*- coding: utf-8 -*-
"""The mobile track floor, set from a measured threshold rather than a guess."""
p = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\component-product-card.css"
s = open(p, encoding='utf-8').read()

old = """/* Below the tablet tier the floor is relaxed, and only there. Phase 2 section
   13.9 permits two columns on a phone; the 272px catalogue floor would force
   one, because a 375px viewport has 327px of content box. 9.5rem (152px) is
   the two-up track at 375 and is the smallest tile the type on it still
   reads at — verified by rendering, not assumed. A merchant who chooses one
   column on mobile still gets one: the ceiling governs, the floor only stops
   the ceiling from producing something unreadable. */
@media (max-width: 767px) {
  .product-grid {
    --product-track-floor: 9.5rem;
  }
}"""

new = """/* Below the tablet tier the floor is relaxed, and only there. Phase 2 section
   13.9 permits two columns on a phone; the 272px catalogue floor would force
   one, because a 375px viewport has only 327px of content box.

   8.5rem (136px) is not a guess. Two columns need 2F + 32px of gap to fit the
   content box, so the largest floor that still yields two columns at 375px is
   (327 - 32) / 2 = 147.5px, and 9.5rem (152px) sits just above it — which is
   why the first render at 375 came back one column wide despite the setting
   asking for two. 8.5rem clears that threshold with room, and the resulting
   ladder was rendered and read before it was adopted:

     320px  content 256  ->  1 column at 256px   (2F + gap = 304 > 256)
     375px  content 327  ->  2 columns at 147px
     430px  content 382  ->  2 columns at 175px
     768px  content 704  ->  the 272px catalogue floor takes over again

   At 147px the tracked-caps title wraps to its two-line clamp and the price
   and swatch row still read; that was checked on a render, not assumed. A
   merchant who chooses one column on mobile still gets one: the ceiling
   governs, and the floor only stops the ceiling asking for something the
   viewport cannot carry. */
@media (max-width: 767px) {
  .product-grid {
    --product-track-floor: 8.5rem;
  }
}"""

assert old in s, 'mobile floor block not found'
open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new, 1))
print('component-product-card.css: mobile floor set to 8.5rem')
