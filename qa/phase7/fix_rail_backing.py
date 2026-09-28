# -*- coding: utf-8 -*-
"""Tie the caption rail's backing to the rail, not to the photograph's width.

Strengthening the media scrim's right tail fixed 1024, 1280 and 1440 but left
1920 at 1.67:1. The reason is arithmetic, not tuning: the photograph is 70% of
the FULL-BLEED band while the caption sits inside a container capped at 1440,
so the rail's position as a fraction of the photograph moves with the viewport.
Measured, the rail's left edge falls at:

    1024  73.2%      1280  78.6%      1440  77.8%      1920  65.5%

and above 1440 it keeps drifting left — (0.2V + 496) / 0.7V, which tends to
28.6% as V grows. No fixed percentage stop can cover that.

So the backing moves onto the rail itself: a pseudo-element that starts
transparent 10rem to the rail's left and reaches full strength behind it, at
every viewport by construction. The media scrim's right tail goes back to a
light edge vignette, which is all it was ever for, so the photograph keeps its
right third.
"""
p = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\section-our-story.css"
s = open(p, encoding='utf-8').read()

# 1. Media scrim: back to a light edge vignette.
for direction in ('90deg', '270deg'):
    old = """      rgba(13, 12, 10, 0.12) 68%,
      rgba(13, 12, 10, 0.88) var(--os-rail-hold, 77%),
      rgba(13, 12, 10, 0.9) 100%);"""
    new = """      rgba(13, 12, 10, 0.1) 82%,
      rgba(13, 12, 10, 0.45) 100%);"""
    assert old in s
    s = s.replace(old, new, 1)

old_c = """  /* The scrim turns horizontal and always fades toward the copy, then darkens
     again under the caption rail.

     Both ends are measured, not styled. The copy end holds 0.96 to 34% because
     the copy column overlaps the photograph's inner edge. The rail end holds
     0.88 from 77% because the rail occupies 78% to 95% of the media and, left
     on open photograph, its cream 12px measured 1.69 to 2.14 against a 4.5:1
     requirement at every width tested. The 68% to 77% ramp is deliberately
     wide so the darkening reads as the picture fading out rather than as a
     panel dropped behind the text. */"""
new_c = """  /* The scrim turns horizontal and always fades toward the copy, then lifts
     slightly again at the trailing edge so the photograph ends on a vignette
     rather than a cut.

     The copy end is measured: it holds 0.96 to 34% because the copy column
     overlaps the photograph's inner edge, and with it the heading measures
     16.5-16.9 and the body 9.56-9.70 at every width tested. The trailing 0.45
     is aesthetic only — the caption rail carries its own backing, for the
     reason given on that rule. */"""
assert old_c in s
s = s.replace(old_c, new_c, 1)

# 2. The rail's own backing.
old_cap = """  .our-story__caption {
    margin-block-start: 0;
    align-self: start;
  }"""
new_cap = """  .our-story__caption {
    position: relative;
    margin-block-start: 0;
    align-self: start;
  }

  /* The rail's backing, tied to the rail rather than to the photograph.

     Left on open photograph the rail's cream 12px measured 1.69, 2.07, 2.14
     and 1.86 to one at 1024, 1280, 1440 and 1920 — against the 4.5:1 a tracked
     12px line needs. A stop in the photograph's own gradient cannot fix it,
     because the photograph is 70% of a full-bleed band while the rail sits in
     a container capped at --container-standard, so the rail's position across
     the picture moves with the viewport: 73.2% at 1024, 78.6% at 1280, 77.8%
     at 1440, 65.5% at 1920, and further left as the screen grows.

     Anchoring the wash to the rail is exact at every width. It starts fully
     transparent 10rem to the rail's left, so it reads as the picture fading
     out behind the words rather than as a panel dropped on top of them, and it
     darkens nothing the words do not need. */
  .our-story__caption::before {
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
  }

  .our-story--image-left .our-story__caption::before {
    inset-inline-start: calc(var(--gutter) * -1);
    inset-inline-end: -10rem;
    background: linear-gradient(270deg,
      rgba(13, 12, 10, 0) 0%,
      rgba(13, 12, 10, 0.9) 62%,
      rgba(13, 12, 10, 0.92) 100%);
  }"""
assert old_cap in s, 'caption rule not found'
s = s.replace(old_cap, new_cap, 1)
open(p, 'w', encoding='utf-8', newline='').write(s)
print('section-our-story.css: rail backing anchored to the rail')
