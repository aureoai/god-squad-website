# -*- coding: utf-8 -*-
"""Teach the validator the post-review contract.

Three checks described the old code and now describe nothing; ten new ones lock
in what the review changed, so a later edit cannot quietly put any of it back.
"""
p = (r"C:\Users\TEST\AppData\Local\Temp\claude"
     r"\C--Users-TEST-OneDrive-Documents-GodSquad-Website"
     r"\de238d03-508d-43ce-a377-210f71ff0033\scratchpad\phase7\validate.py")
s = open(p, encoding='utf-8').read()


def sub(old, new, label):
    global s
    assert old in s, 'NOT FOUND: ' + label
    s = s.replace(old, new, 1)
    print('  ', label)


sub("""check("value titles are h3", '<h3 class="our-story__value-title">' in storyc)""",
    """check("value titles take a level derived from the heading",
      '<h{{ value_level }} class="our-story__value-title">' in storyc
      and 'assign value_level = 3' in story and 'assign value_level = 2' in story)""",
    'value heading level')

sub("""local = {'--os-space-top', '--os-space-bottom', '--os-header-clearance', '--os-focal-y',
         '--os-wash-hold', '--os-wash-end', '--os-scrim-rgb', '--header-overlay-offset'}""",
    """local = {'--os-space-top', '--os-space-bottom', '--os-header-clearance',
         '--os-scrim-rgb', '--header-overlay-offset'}""",
    'local property list trimmed to what exists')

sub("""print("\\n=== TOKEN FIDELITY ===")""",
    """print("\\n=== REVIEW CONTRACT ===")
# The photograph is 70% of a band with no max-width, so its slot is 70vw at
# every width from the split up. Capping it at a share of container_width told
# the browser 1008px for a 1344px slot above 1440.
check("the image slot is declared in viewport units",
      "assign img_sizes = '(min-width: 1024px) 70vw, 100vw'" in story)
check("the image slot is not capped at the container width",
      'container_width' not in storybody and 'capped' not in storybody)

# image_tag writes an inline object-position for an admin focal point, which no
# stylesheet can override, so the theme must not offer a competing control.
check("no theme-side focal point setting",
      not [f for f in schema['settings'] if f.get('id') == 'focal_point'])
check("no focal point modifier class", 'our-story--focal-' not in story
      and 'our-story--focal-' not in css)
check("the stylesheet sets only a default crop centre",
      '--os-focal-y' not in css and 'object-position: center 33%' in css)

# The media wrapper carries an aspect ratio and an ink fill, so it must not be
# emitted without an image.
mi = storyc.index('<div class="our-story__media">')
gi = storyc.index('{%- if img != blank -%}')
check("the media wrapper is inside the image guard", gi < mi)

# Phase 2 26.5: at most two accent marks in a band. The eyebrow is one.
check("gold is spent once in the band",
      css.count('color: var(--accent-current)') == 1)

# Phase 2 26.2: the editorial cap belongs to the rail, the reading cap to the
# stacked column.
check("the stacked body takes the reading measure",
      'max-width: var(--measure-body);' in css)
check("the body takes the editorial measure at the split",
      'max-width: var(--measure-narrow);' in css)

# A 14rem floor fits five tracks at 1440 and orphans a sixth block.
check("the values row fits four tracks, not five",
      'minmax(min(17rem, 100%), 1fr)' in css)

# The mobile source covers up to 1023 CSS px, which is 3069 device px at DPR 3.
check("the mobile source reaches beyond 1200w",
      'width: 2048 }} 2048w' in storyc)

print("\\n=== APPROVED COPY ===")
proto = R('God Squad Website.html')
approved = [('Faith Driven', 'More Than Clothing'),
            ('Community', 'People With Purpose'),
            ('Premium Quality', 'Crafted To Inspire')]
for title, line in approved:
    check("value '%s' is the prototype's own copy" % title,
          title in proto and line in proto and title in story and line in story)
check("the unverified shipping claim is not shipped",
      'Shipping Available' not in story and 'Shipping Available' not in json.dumps(entry))
check("no value line duplicates the hero's copy",
      'Different People. Same Purpose.' not in story
      and 'Different people. Same purpose.' not in story)

print("\\n=== TOKEN FIDELITY ===")""",
    'review contract block')

open(p, 'w', encoding='utf-8', newline='').write(s)
print('validate.py updated')
