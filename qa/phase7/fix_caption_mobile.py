# -*- coding: utf-8 -*-
"""The caption rail was claimed to be absent below the split. It was not.

The Liquid comment said the rail "is not rendered at all down there", but
nothing implemented that — Liquid cannot know the viewport, and no CSS rule
hid it. Rendered at 375 the rail duly stacked after the body copy as a
four-line orphan, which is precisely the defect Phase 1 STORY-04 recorded in
the prototype and asked this phase to decide.

The decision stands; only the mechanism was missing. display:none below the
split removes it from the layout AND from the accessibility tree, so it is not
read out either. The comment is corrected to say what the code does.
"""
css = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\section-our-story.css"
sect = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\sections\our-story.liquid"

s = open(css, encoding='utf-8').read()
old = """.our-story__caption {
  margin: var(--space-8) 0 0;"""
new = """/* Below the split the rail is not shown at all. Phase 1 STORY-04 recorded it
   stacking as a four-line orphan after the button on the prototype's small
   screens, and asked Phase 7 to decide its behaviour and expose the choice.
   The decision is that it belongs to the wide composition: it is editorial
   texture at the band's edge, and there is no band edge once the composition
   stacks. display:none rather than visibility or opacity, so it leaves the
   accessibility tree too and is not read out on a phone either. The setting
   turns it off everywhere. */
.our-story__caption {
  display: none;
  margin: var(--space-8) 0 0;"""
assert old in s, 'caption rule not found'
s = s.replace(old, new, 1)

old2 = """  .our-story__caption {
    position: relative;
    margin-block-start: 0;
    align-self: start;
  }"""
new2 = """  .our-story__caption {
    display: block;
    position: relative;
    margin-block-start: 0;
    align-self: start;
  }"""
assert old2 in s, 'wide caption rule not found'
s = s.replace(old2, new2, 1)
open(css, 'w', encoding='utf-8', newline='').write(s)
print('section-our-story.css: rail hidden below the split')

t = open(sect, encoding='utf-8').read()
oldc = """    The caption rail. Phase 1 STORY-04 recorded it stacking as a 145px orphan
    after the CTA below 900px, and asked Phase 7 to decide its small-screen
    behaviour and expose the choice. The decision: it belongs to the wide
    composition only. Below the split it is not rendered at all rather than
    hidden with CSS, so it costs nothing on the viewport that can least afford
    it. The setting turns it off everywhere."""
newc = """    The caption rail. Phase 1 STORY-04 recorded it stacking as a 145px orphan
    after the CTA below 900px, and asked Phase 7 to decide its small-screen
    behaviour and expose the choice. The decision: it belongs to the wide
    composition only, and the stylesheet hides it below the split with
    display:none so it leaves the accessibility tree as well as the layout.
    This setting turns it off at every width."""
assert oldc in t, 'caption comment not found'
open(sect, 'w', encoding='utf-8', newline='').write(t.replace(oldc, newc, 1))
print('our-story.liquid: comment now describes what the code does')
