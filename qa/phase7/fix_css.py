# -*- coding: utf-8 -*-
"""Remove the dead --split-rail / --split-rail-mirror declarations.

The explicit minmax() track lists below them supersede both, and
--split-rail-mirror does not exist as a token at all.
"""
p = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\section-our-story.css"
s = open(p, encoding='utf-8').read()

old = """  .our-story__inner {
    display: grid;
    grid-template-columns: var(--split-rail);
    gap: var(--grid-gap-large);
    align-items: center;
    padding-block-start: 0;
  }

  /* Image on the left mirrors the tracks so the copy stays on the clear side. */
  .our-story--image-left .our-story__inner {
    grid-template-columns: var(--split-rail-mirror);
  }

  .our-story--image-left .our-story__content { grid-column: 3; }"""

new = """  /* --split-rail is 0.9fr 1.6fr 0.4fr — copy / image window / caption rail.
     The track list is written out rather than using the token because each
     track also needs a minimum: see the floors below. */
  .our-story__inner {
    display: grid;
    gap: var(--grid-gap-large);
    align-items: center;
    padding-block-start: 0;
  }

  /* Image on the left mirrors the tracks so the copy stays on the clear side. */
  .our-story--image-left .our-story__content { grid-column: 3; }"""

assert old in s, 'inner grid block not found'
open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new, 1))
print('section-our-story.css: dead --split-rail references removed')
