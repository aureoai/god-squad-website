# -*- coding: utf-8 -*-
"""Soften the rail backing's horizontal edges.

Rendered, the backing read as a rectangular panel: the horizontal fade worked
but the top and bottom were hard cuts across the photograph. A linear gradient
can only fade on one axis, and layering a second one does not help — the
opaque middle of a vertical layer would paint over the horizontal fade rather
than multiply with it.

A mask fades the second axis. The panel is extended 8rem beyond the text on
each side and the mask fades its outer thirds, so the text still sits in the
fully opaque middle and the wash has no visible edge anywhere. Where masks are
unsupported the panel simply keeps its hard edges — the words stay legible,
which is the property that matters.
"""
p = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\section-our-story.css"
s = open(p, encoding='utf-8').read()

old = """  .our-story__caption::before {
    content: "";
    position: absolute;
    z-index: -1;
    inset-block: calc(var(--space-7) * -1);
    inset-inline-start: -10rem;
    inset-inline-end: calc(var(--gutter) * -1);
    background: linear-gradient(90deg,
      rgba(13, 12, 10, 0) 0%,
      rgba(13, 12, 10, 0.9) 62%,
      rgba(13, 12, 10, 0.92) 100%);
    pointer-events: none;
  }"""
new = """  .our-story__caption::before {
    content: "";
    position: absolute;
    z-index: -1;
    inset-block: -8rem;
    inset-inline-start: -10rem;
    inset-inline-end: calc(var(--gutter) * -1);
    background: linear-gradient(90deg,
      rgba(13, 12, 10, 0) 0%,
      rgba(13, 12, 10, 0.9) 62%,
      rgba(13, 12, 10, 0.92) 100%);
    /* The second axis. Without it the wash is a rectangle with two hard cuts
       across the photograph. The 8rem of extra height above and below puts the
       words inside the mask's opaque middle, so softening the edges costs them
       no contrast. */
    -webkit-mask-image: linear-gradient(180deg,
      transparent 0%, #000 30%, #000 70%, transparent 100%);
    mask-image: linear-gradient(180deg,
      transparent 0%, #000 30%, #000 70%, transparent 100%);
    pointer-events: none;
  }"""
assert old in s, 'caption backing not found'
s = s.replace(old, new, 1)

old2 = """  .our-story--image-left .our-story__caption::before {
    inset-inline-start: calc(var(--gutter) * -1);
    inset-inline-end: -10rem;
    background: linear-gradient(270deg,
      rgba(13, 12, 10, 0) 0%,
      rgba(13, 12, 10, 0.9) 62%,
      rgba(13, 12, 10, 0.92) 100%);
  }"""
new2 = """  .our-story--image-left .our-story__caption::before {
    inset-inline-start: calc(var(--gutter) * -1);
    inset-inline-end: -10rem;
    background: linear-gradient(270deg,
      rgba(13, 12, 10, 0) 0%,
      rgba(13, 12, 10, 0.9) 62%,
      rgba(13, 12, 10, 0.92) 100%);
  }

  /* The rail's hairline sits on the wash, so it takes the wash's edge colour
     rather than the band's border token, which would disappear on it. */
  .our-story__caption::after {
    background-color: var(--color-border-current);
  }"""
assert old2 in s, 'mirrored caption backing not found'
s = s.replace(old2, new2, 1)
open(p, 'w', encoding='utf-8', newline='').write(s)
print('section-our-story.css: rail backing edges softened')
