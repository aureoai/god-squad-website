# -*- coding: utf-8 -*-
"""Give the stacked media a ratio per tier instead of one portrait ratio.

Rendered at 768 the band came out 768 x 960 — a portrait image nearly a
thousand pixels tall on a tablet, which pushed the eyebrow, heading, body and
values entirely below the fold. The ratio came from --hero-aspect-mobile, a
token named for the hero on a phone and borrowed here, which is exactly the
kind of borrowing that produces a number nobody chose.

Phone keeps 4/5: a portrait band beside a thumb is right, and the crop holds
the subject.
Tablet takes 3/2, which is 512px tall at 768 and is also the canonical story
asset's own ratio (images/our-story.webp is 535x348, 1.537:1), so at that tier
the picture is shown essentially uncropped.
"""
p = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\section-our-story.css"
s = open(p, encoding='utf-8').read()

old = """.our-story__media {
  position: relative;
  width: 100%;
  aspect-ratio: var(--hero-aspect-mobile);
  overflow: hidden;
  background-color: var(--color-bg-primary);
}"""
new = """.our-story__media {
  position: relative;
  width: 100%;
  /* Portrait on a phone: the band sits under a thumb, and the taller frame
     holds the subject where a landscape crop would lose it. This is the same
     4/5 the hero uses on a phone, and it is referenced through the token
     rather than written out. */
  aspect-ratio: var(--hero-aspect-mobile);
  overflow: hidden;
  background-color: var(--color-bg-primary);
}

/* Landscape from the tablet tier. 4/5 at 768 is a 960px-tall band that pushes
   every word below the fold — measured, not assumed. 3/2 is 512px there, and
   it is also the canonical story asset's own ratio (images/our-story.webp is
   535x348, 1.537:1), so at this tier the photograph is shown essentially
   uncropped. Phase 2 §14.4 defines no editorial landscape ratio token; this
   is recorded as a token gap rather than as a value chosen here. */
@media (min-width: 768px) {
  .our-story__media {
    aspect-ratio: 3 / 2;
  }
}"""
assert old in s, 'media rule not found'
open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new, 1))
print('section-our-story.css: tablet tier gets a landscape ratio')
