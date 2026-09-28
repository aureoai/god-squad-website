# -*- coding: utf-8 -*-
"""Final mobile track floor, from a measured threshold in both scrollbar regimes."""
p = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\component-product-card.css"
s = open(p, encoding='utf-8').read()

start = s.index("/* Below the tablet tier the floor is relaxed")
end = s.index("/* ------------------------------------------------------------------- card */")

new = """/* Below the tablet tier the floor is relaxed, and only there. Phase 2 section
   13.9 permits two columns on a phone; the 272px catalogue floor would force
   one, because a 375px viewport has only 327px of content box.

   8rem (128px) is not a guess. Two columns need 2F + 32px of gap to fit the
   grid's own width, so the floor decides the 1 -> 2 threshold exactly. It was
   measured in both scrollbar regimes, because a phone has overlay scrollbars
   that take no layout width while a desktop window narrowed to the same size
   has a classic one that takes about 15px:

     window  layout  grid   columns at 8.5rem   columns at 8rem
       320     320    272        1                  1
       344     344    280        1                  1
       375     360    296        1  <- classic       2
       375     375    311        2  <- overlay       2
       390     375    311        2                   2
       430     415    351        2                   2

   8.5rem put the threshold between those two 375 rows, so the same phone width
   gave two columns on a device and one in a desktop window. 8rem puts the
   threshold at a layout width of 352 instead, below both, so a merchant who
   asks for two columns on mobile gets two wherever they look. The cost is a
   132px track instead of 147px at the narrowest two-up, which was rendered and
   read before it was adopted: the tracked-caps title still wraps inside its
   two-line clamp and the price and swatch row still read.

   320px still gets one column, which is correct: two 128px tracks plus the gap
   do not fit 272px of content box.

   A merchant who chooses one column on mobile still gets one. The ceiling
   governs; the floor only stops the ceiling asking for something the viewport
   cannot carry. */
@media (max-width: 767px) {
  .product-grid {
    --product-track-floor: 8rem;
  }
}

"""
s = s[:start] + new + s[end:]
open(p, 'w', encoding='utf-8', newline='').write(s)
print('component-product-card.css: mobile floor set to 8rem')
