# -*- coding: utf-8 -*-
"""The hero in landscape.

Measured at 812x375 and 932x430 — a phone turned sideways — the hero renders
545 and 563px tall inside a 375 and 430px viewport, and the call to action ends
at y=497. It is below the fold, on a band whose whole job is to carry it.

The cause is the clamp FLOOR, not the svh: --h-medium is
clamp(32rem, 68svh, 45rem), and 32rem is 512px, which is larger than a
landscape phone's entire viewport. The floors are right for portrait, where
they stop the hero collapsing on a short-but-wide desktop window; they are
simply not reachable on a screen 375px tall.

The block below is additive and bounded to phones and small tablets turned
sideways: max-height 540px AND max-width 1023px, so a resized desktop window
keeps the composition it was designed with.
"""
p = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\section-hero.css"
s = open(p, encoding='utf-8').read()

anchor = "/* ---------------------------------------------------------- reduced motion"
if anchor not in s:
    anchor = "@media (prefers-reduced-motion: reduce)"
assert anchor in s, 'anchor not found'

block = """/* ------------------------------------------------------------- landscape
   A phone turned sideways. Measured before this block: the medium hero was
   545px tall in a 375px viewport and its call to action ended at y=497 —
   below the fold, on the one band whose purpose is to carry it.

   The cause is the clamp FLOOR rather than the svh. 32rem is 512px, which is
   more than a landscape phone's whole viewport, so the hero could never be
   shorter than the screen. The floors are correct in portrait and are left
   alone there.

   Bounded to max-width 1023px as well as max-height 540px, so a desktop
   window someone has made short keeps the composition it was designed with.

   Everything here is a token. Nothing about the content, the order or the
   messaging changes; the band is re-proportioned for a screen 375px tall. */

@media (max-height: 540px) and (max-width: 1023px) {
  .hero--h-small,
  .hero--h-medium,
  .hero--h-large,
  .hero--h-full {
    /* The viewport, and no floor above it. */
    min-height: calc(100svh - var(--header-overlay-offset, 0px));
  }

  .hero__inner {
    padding-block: calc(var(--header-overlay-offset, 0px) + var(--space-4)) var(--space-5);
  }

  /* The display scale is set from the viewport's WIDTH, which in landscape is
     the dimension that is not scarce. Re-clamped against height so the lockup
     keeps its two lines without taking a third of the screen: 9svh is 34px on
     a 375px-tall phone and 39px on a 430px one. */
  .hero__heading {
    font-size: clamp(1.75rem, 9svh, 3rem);
  }

  .hero__eyebrow {
    margin-block-end: var(--space-3);
  }

  .hero__scripture {
    margin-block-start: var(--space-3);
  }

  .hero__description {
    margin-block-start: var(--space-4);
  }

  .hero__description::before {
    margin-block-end: var(--space-3);
  }

  .hero__cta {
    margin-block-start: var(--space-5);
  }
}

"""
s = s.replace(anchor, block + anchor, 1)
open(p, 'w', encoding='utf-8', newline='').write(s)
print('section-hero.css: landscape block added')
