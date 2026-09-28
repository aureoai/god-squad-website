# -*- coding: utf-8 -*-
"""Rebuild the wide composition after rendering it.

Three defects the first render showed:

1. The caption rail landed in track 2, the image window, because it is the
   second child of a three-track grid and nothing placed it. It belongs in
   track 3, at the band's edge.
2. The brand values row sat ON the photograph. The media was absolutely
   positioned across the whole band, so the values inherited whatever was left
   of the scrim — which by 88% of the width is 0.12 alpha. Gold value titles on
   an unscrimmed photograph is exactly the failure Phase 1 A11Y-03 recorded for
   the nav.
3. Absolute positioning made the band's height independent of its content, so
   the composition and the values could not be given separate rows.

All three are the same fix: make the band a two-row grid, let the media and the
copy share row one, and give the values row two on flat ink.
"""
p = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\section-our-story.css"
s = open(p, encoding='utf-8').read()

start = s.index("@media (min-width: 1024px) {")
end = s.index("/* ---------------------------------------------------------- reduced motion")

new = """@media (min-width: 1024px) {
  /* Two rows: the composition, then the values. The media and the copy share
     row one by both being placed in the same cell, which is what lets the
     photograph sit behind the copy without absolute positioning — and what
     keeps the values row out of the photograph entirely. */
  .our-story {
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    grid-template-rows: auto auto;
  }

  .our-story__media,
  .our-story__inner {
    grid-row: 1;
    grid-column: 1;
  }

  .our-story__values {
    grid-row: 2;
    grid-column: 1;
  }

  /* The photograph is offset, never centred behind the copy (Phase 2 §26.3
     rule 3): it takes 70% of the band and bleeds to one edge. */
  .our-story__media {
    position: relative;
    width: 70%;
    min-height: var(--band-min-height-story);
    aspect-ratio: auto;
    z-index: var(--z-base);
  }

  .our-story--image-right .our-story__media { justify-self: end; }
  .our-story--image-left  .our-story__media { justify-self: start; }

  /* The scrim turns horizontal and always fades toward the copy. */
  .our-story--image-right .our-story__scrim {
    background: linear-gradient(90deg,
      rgba(13, 12, 10, 1) 0%,
      rgba(13, 12, 10, 0.96) var(--os-wash-hold, 34%),
      rgba(13, 12, 10, 0.2) var(--os-wash-end, 62%),
      rgba(13, 12, 10, 0.12) 88%,
      rgba(13, 12, 10, 0.55) 100%);
  }

  .our-story--image-left .our-story__scrim {
    background: linear-gradient(270deg,
      rgba(13, 12, 10, 1) 0%,
      rgba(13, 12, 10, 0.96) var(--os-wash-hold, 34%),
      rgba(13, 12, 10, 0.2) var(--os-wash-end, 62%),
      rgba(13, 12, 10, 0.12) 88%,
      rgba(13, 12, 10, 0.55) 100%);
  }

  /* --split-rail is 0.9fr 1.6fr 0.4fr — copy / image window / caption rail.
     The track list is written out rather than using the token because each
     track also needs a minimum: the copy track has to hold the display
     heading's lockup, which Phase 1 STORY-05 recorded wrapping to three lines
     at 1440 and four at 1024 in a track of about 350px and 220px. */
  .our-story__inner {
    display: grid;
    grid-template-columns: minmax(20rem, 0.9fr) minmax(0, 1.6fr) minmax(9rem, 0.4fr);
    gap: var(--grid-gap-large);
    align-items: center;
    align-content: center;
    padding-block: var(--space-9);
  }

  .our-story__content { grid-column: 1; }
  .our-story__caption { grid-column: 3; }

  /* Image on the left mirrors the tracks so the copy stays on the clear side. */
  .our-story--image-left .our-story__inner {
    grid-template-columns: minmax(9rem, 0.4fr) minmax(0, 1.6fr) minmax(20rem, 0.9fr);
  }

  .our-story--image-left .our-story__content { grid-column: 3; }
  .our-story--image-left .our-story__caption { grid-column: 1; }

  .our-story__caption {
    margin-block-start: 0;
    align-self: start;
  }

  .our-story--image-left .our-story__caption { text-align: right; }
  .our-story--image-left .our-story__caption::after { margin-inline-start: auto; }

  .our-story__values {
    margin-block-start: 0;
    padding-block-start: var(--space-8);
  }
}

@media (min-width: 1440px) {
  .our-story__inner {
    grid-template-columns: minmax(24rem, 0.9fr) minmax(0, 1.6fr) minmax(11rem, 0.4fr);
  }

  .our-story--image-left .our-story__inner {
    grid-template-columns: minmax(11rem, 0.4fr) minmax(0, 1.6fr) minmax(24rem, 0.9fr);
  }
}

"""
s = s[:start] + new + s[end:]
open(p, 'w', encoding='utf-8', newline='').write(s)
print('section-our-story.css: wide composition rebuilt as a two-row grid')
