# -*- coding: utf-8 -*-
"""Tie the copy track's floor to the heading clamp, as Phase 1 STORY-05 asked.

Measured with the real face and tracking, in an unbounded box:

    line                       32px    36px    40px
    REAL PEOPLE.                253     285     316
    BIGGER PURPOSE.             325     366     406

The story scale is --type-display-m-size, clamp(2rem, 4vw, 2.5rem), so it
reaches its 40px cap at a 1000px viewport. The copy track was 397px at 1440 —
nine pixels short of the 406px the second line needs — so even with the break
in the markup the browser broke it again and the lockup came out on three
lines, exactly the defect STORY-05 recorded in the prototype.

26rem (416px) clears 406 with ten pixels to spare. It costs nothing visually:
the track it takes width from is the empty image window, and the photograph is
70% of the band regardless of the inner grid. Checked against the scrim at
both widths — at 1024 the copy now ends at 464 and the scrim holds full
opacity to 551; at 1440 it ends at 464 against 775.
"""
p = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\section-our-story.css"
s = open(p, encoding='utf-8').read()

pairs = [
    ("""  .our-story__inner {
    display: grid;
    grid-template-columns: minmax(20rem, 0.9fr) minmax(0, 1.6fr) minmax(9rem, 0.4fr);""",
     """  .our-story__inner {
    display: grid;
    grid-template-columns: minmax(26rem, 0.9fr) minmax(0, 1.6fr) minmax(9rem, 0.4fr);"""),

    ("""  .our-story--image-left .our-story__inner {
    grid-template-columns: minmax(9rem, 0.4fr) minmax(0, 1.6fr) minmax(20rem, 0.9fr);
  }""",
     """  .our-story--image-left .our-story__inner {
    grid-template-columns: minmax(9rem, 0.4fr) minmax(0, 1.6fr) minmax(26rem, 0.9fr);
  }"""),

    ("""  .our-story__inner {
    grid-template-columns: minmax(24rem, 0.9fr) minmax(0, 1.6fr) minmax(11rem, 0.4fr);
  }""",
     """  .our-story__inner {
    grid-template-columns: minmax(26rem, 0.9fr) minmax(0, 1.6fr) minmax(11rem, 0.4fr);
  }"""),

    ("""  .our-story--image-left .our-story__inner {
    grid-template-columns: minmax(11rem, 0.4fr) minmax(0, 1.6fr) minmax(24rem, 0.9fr);
  }""",
     """  .our-story--image-left .our-story__inner {
    grid-template-columns: minmax(11rem, 0.4fr) minmax(0, 1.6fr) minmax(26rem, 0.9fr);
  }"""),
]
for old, new in pairs:
    assert old in s, 'NOT FOUND:\n' + old[:110]
    s = s.replace(old, new, 1)

# Record the measurement beside the value.
old_c = """     track also needs a minimum: the copy track has to hold the display
     heading's lockup, which Phase 1 STORY-05 recorded wrapping to three lines
     at 1440 and four at 1024 in a track of about 350px and 220px. */"""
new_c = """     track also needs a minimum: the copy track has to hold the display
     heading's lockup, which Phase 1 STORY-05 recorded wrapping to three lines
     at 1440 and four at 1024 in a track of about 350px and 220px.

     26rem is measured, not chosen. With the real face and tracking, the two
     lines of the approved heading set at 253 / 325 (32px), 285 / 366 (36px)
     and 316 / 406 (40px). The scale caps at 40px from a 1000px viewport, so
     the track has to clear 406px or the browser breaks the second line again
     even with the break already in the markup — which is what the first render
     did, at a track of 397px. The width comes out of the empty image window
     track, not out of the photograph, which is 70% of the band either way.

     A longer merchant heading still wraps. That is correct: the floor
     guarantees the approved lockup sets as drawn, not that any text will. */"""
assert old_c in s
s = s.replace(old_c, new_c, 1)

open(p, 'w', encoding='utf-8', newline='').write(s)
print('section-our-story.css: copy track floor set to 26rem from measurement')
