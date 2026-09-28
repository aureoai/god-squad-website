# -*- coding: utf-8 -*-
"""Apply the Phase 7 adversarial-review findings that survive against the
current files.

Thirty findings were confirmed against a snapshot. Nine of them (the cream
surface, the scrim base colour and the call-to-action variant) were already
closed by fix_cream.py before the review returned, and the verifiers said so.
What follows is everything else that is still true of the code on disk.

  A. image_tag writes an inline object-position for admin focal points, which
     outranks this theme's focal_point select. The select is removed.
  B. sizes capped the slot at 70% of the container; the photograph is 70% of a
     full-bleed band. Above 1440 the browser was told 1008px for a 1344px slot.
  C. The media wrapper rendered with an aspect ratio and an ink fill even with
     no image, which is the state templates/index.json actually ships.
  D. Four gold marks in one band against Phase 2 §26.5's budget of two.
  E. The body cap was the 40ch editorial measure at every width, including the
     768-1023 tier where the copy runs full width and wants a reading measure.
  F. The value blocks shipped copy I wrote over approved copy the project has.
  G. Dead knobs, a dead override, a mis-stated comment and a wrapping ceiling.
"""
import json, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SECT = ROOT + r"\sections\our-story.liquid"
CSS = ROOT + r"\assets\section-our-story.css"
TPL = ROOT + r"\templates\index.json"

done = []


def sub(text, old, new, label):
    assert old in text, 'NOT FOUND: ' + label
    assert text.count(old) == 1, 'AMBIGUOUS: ' + label
    done.append(label)
    return text.replace(old, new, 1)


# =====================================================================  LIQUID
t = open(SECT, encoding='utf-8').read()

# --- B. the slot is 70vw, not 70% of the container ------------------------
t = sub(t, """  comment
    The image sits in the larger track and bleeds to the band's edge, so its
    slot is 70% of the row from the split up and the full width below it.
  endcomment
  assign container = settings.container_width | default: 1440
  assign capped = container | times: 70 | divided_by: 100
  capture img_sizes
    echo '(min-width: '
    echo container
    echo 'px) '
    echo capped
    echo 'px, (min-width: 1024px) 70vw, 100vw'
  endcapture
""", """  comment
    The image's slot, stated in viewport terms because that is what it is.
    .our-story__media is width:70% of a band that is width:100% with no
    max-width — only the copy container and the values row are capped at
    --container-standard, never the photograph. So the slot is 70vw from the
    split up and the full width below it, at every viewport.

    An earlier version also capped this at 70% of settings.container_width,
    which on a 1920 screen declared 1008px for a slot that renders 1344px and
    let the browser settle for a candidate a quarter too small. The cap was the
    mistake, not the value: there is nothing above --container-standard for the
    photograph to stop at.
  endcomment
  assign img_sizes = '(min-width: 1024px) 70vw, 100vw'
""", 'B sizes is 70vw')

# --- A. the crop centre is Shopify's focal point, not a theme select -------
t = sub(t, """  assign classes = classes | append: ' our-story--focal-' | append: section.settings.focal_point
""", """""", 'A focal class removed')

t = sub(t, """    {
      "type": "select",
      "id": "focal_point",
      "label": "Focal point",
      "info": "Where the crop centres when the frame is shorter than the photograph. The prototype cropped about a fifth of the picture's height away and lost the subject's hands and chest.",
      "options": [
        { "value": "top", "label": "Top" },
        { "value": "upper", "label": "Upper third" },
        { "value": "centre", "label": "Centre" },
        { "value": "lower", "label": "Lower third" }
      ],
      "default": "upper"
    },
""", """""", 'A focal setting removed')

t = sub(t, """        "focal_point": "upper",
""", """""", 'A focal preset value removed')

t = sub(t, """      "info": "Optional. Below 1024px the image runs full width in a shorter band, so a portrait or squarer crop holds the subject better. Leave empty and the desktop image is used with the focal point below applied."
""", """      "info": "Optional. Below 1024px the image runs full width in a shorter band, so a portrait or squarer crop holds the subject better. Leave empty and the desktop image is used with its own focal point applied."
""", 'A mobile info reworded')

t = sub(t, """Set the image's alt text in Shopify admin: the theme never writes it for you."
""", """Set the image's alt text and its focal point in Shopify admin. The theme never writes alt text for you, and the focal point you set there is what decides the crop centre when the frame is shorter than the photograph — this section deliberately does not add a second, competing control, because Shopify writes the admin focal point onto the image as an inline style that a stylesheet cannot override."
""", 'A image info records the focal point')

# --- G. the mobile source stopped at 1200w (before the re-indent below) ---
t = sub(t, """              {{ img_mobile | image_url: width: 1200 }} 1200w
            \"""", """              {{ img_mobile | image_url: width: 1200 }} 1200w,
              {{ img_mobile | image_url: width: 1500 }} 1500w,
              {{ img_mobile | image_url: width: 2048 }} 2048w
            \"""", 'G mobile srcset reaches 2048w')

# --- C. no image, no media block ------------------------------------------
t = sub(t, """<div class="{{ classes }}" {% if section.settings.anchor_id != blank %}id="{{ section.settings.anchor_id | handle }}"{% endif %}>
  <div class="our-story__media">
    {%- if img != blank -%}
""", """<div class="{{ classes }}" {% if section.settings.anchor_id != blank %}id="{{ section.settings.anchor_id | handle }}"{% endif %}>
  {%- comment -%}
    The media block is inside the guard, not around it. The wrapper carries an
    aspect ratio and an ink fill, so emitting it without an image ships a tall
    empty rectangle above the copy — and that is the state a merchant is in the
    moment they add the section, because an image_picker cannot have a default.
    It is also the state templates/index.json ships, since the canonical master
    does not exist yet. The Theme Editor notice at the foot of the band is the
    merchant's cue instead.
  {%- endcomment -%}
  {%- if img != blank -%}
    <div class="our-story__media">
""", 'C media wrapper inside the guard')

t = sub(t, """      <div class="our-story__scrim" aria-hidden="true"></div>
    {%- endif -%}
  </div>
""", """      <div class="our-story__scrim" aria-hidden="true"></div>
    </div>
  {%- endif -%}
""", 'C media wrapper closed inside the guard')

# The markup between the two edits above is now one level shallower than its
# braces suggest; re-indent the picture/img/scrim block so the file still reads.
old_body_start = t.index('  {%- if img != blank -%}\n    <div class="our-story__media">\n')
old_body_end = t.index('      <div class="our-story__scrim" aria-hidden="true"></div>\n    </div>\n  {%- endif -%}\n')
head = t[:old_body_start]
mid = t[old_body_start:old_body_end]
tail = t[old_body_end:]
lines = mid.split('\n')
out = [lines[0], lines[1]]
for ln in lines[2:]:
    out.append(('  ' + ln) if ln.strip() else ln)
t = head + '\n'.join(out) + tail
done.append('C media block re-indented')

# --- G. an h3 with no h2 above it -----------------------------------------
t = sub(t, """  assign show_caption = false
""", """  comment
    The value tiles are h3s under this band's h2. If the merchant clears the
    heading the h2 goes with it, and three h3s would then hang directly off the
    hero's h1 with a level skipped. The level follows the heading instead, the
    same way the Phase 6 rows derive theirs.
  endcomment
  assign value_level = 3
  if heading == blank
    assign value_level = 2
  endif

  assign show_caption = false
""", 'G value heading level derived')

t = sub(t, """              <h3 class="our-story__value-title">{{ block.settings.title }}</h3>
""", """              <h{{ value_level }} class="our-story__value-title">{{ block.settings.title }}</h{{ value_level }}>
""", 'G value title uses the derived level')

# --- F. the approved value copy -------------------------------------------
t = sub(t, """      numbers. Every line is brand messaging, never a measurable claim.
""", """      numbers. Every line is brand messaging, never a measurable claim.

      The copy is the prototype's own, not new copy. Three of the four approved
      tiles ship as the preset. The fourth — "Worldwide / Shipping Available" —
      does not, because Phase 1 VAL-04 and UX-05 recorded it as the one value
      that is a checkable commercial promise with no policy, destination list or
      rate table behind it anywhere in the project. It is BUSINESS INFORMATION
      REQUIRED, and a merchant who can stand behind it can add it as a fourth
      block in one edit.
""", 'F values comment records VAL-04')

t = sub(t, """        {
          "type": "text",
          "id": "title",
          "label": "Title",
          "default": "Faith"
        },
        {
          "type": "text",
          "id": "body",
          "label": "Line",
          "default": "Walking by faith.",
""", """        {
          "type": "text",
          "id": "title",
          "label": "Title",
          "default": "Faith Driven"
        },
        {
          "type": "text",
          "id": "body",
          "label": "Line",
          "default": "More Than Clothing",
""", 'F block defaults are approved copy')

t = sub(t, """        { "type": "value", "settings": { "title": "Faith", "body": "Walking by faith." } },
        { "type": "value", "settings": { "title": "Purpose", "body": "Created with intention." } },
        { "type": "value", "settings": { "title": "Community", "body": "Different people. Same purpose." } }
""", """        { "type": "value", "settings": { "title": "Faith Driven", "body": "More Than Clothing" } },
        { "type": "value", "settings": { "title": "Community", "body": "People With Purpose" } },
        { "type": "value", "settings": { "title": "Premium Quality", "body": "Crafted To Inspire" } }
""", 'F preset blocks are approved copy')

# --- G. the body field's paragraph count -----------------------------------
t = sub(t, """      "info": "Two to four short paragraphs at most. The column is capped at a reading measure, so longer copy makes the band taller rather than the lines wider."
""", """      "info": "One paragraph is the house default: Phase 2 §26.1 gives this band a single body paragraph. The Phase 7 brief allows up to four short ones, so the field accepts them, and the column is capped at a reading measure — longer copy makes the band taller rather than the lines wider."
""", 'G body info records the 1-vs-4 departure')

open(SECT, 'w', encoding='utf-8', newline='').write(t)
print('sections/our-story.liquid rewritten')


# ========================================================================  CSS
c = open(CSS, encoding='utf-8').read()

# --- G. the header comment blamed the Liquid for a CSS rule ---------------
c = sub(c, """   Below --bp-lg the rail collapses: the photograph takes a defined band of its
   own and the copy sits beneath it on flat ink. The caption rail is not
   rendered at all down there (see the section's Liquid), because Phase 1
   STORY-04 recorded it stacking as an orphan after the button.
""", """   Below --bp-lg the rail collapses: the photograph takes a defined band of its
   own and the copy sits beneath it on flat ink. The caption rail is not
   rendered at all down there — display:none on .our-story__caption in this
   file, lifted at the split — because Phase 1 STORY-04 recorded it stacking as
   an orphan after the button.
""", 'G header comment points at the right file')

# --- G. the header-clearance comment asserted a position -------------------
c = sub(c, """/* The Phase 4 header overlays the FIRST section of the home page. This band is
   sixth, but a merchant can reorder, and a section that finds itself first
   would otherwise sit under the navigation. Same mechanism the collection row
   uses; the property resolves to 0 when the header is not overlaying. */
""", """/* The Phase 4 header overlays the FIRST section of the home page. This band is
   not first as shipped, but a merchant can reorder, and a section that finds
   itself first would otherwise sit under the navigation. Same mechanism the
   collection row uses; the property resolves to 0 when the header is not
   overlaying. */
""", 'G clearance comment drops the stale ordinal')

# --- A. the focal point is Shopify's -------------------------------------
c = sub(c, """.our-story__image {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center var(--os-focal-y, 33%);
}

/* Four named vertical crops. The prototype's object-position was `center top`,
   which discarded about a fifth of the picture's height at 1440 — the hands and
   chest that carry the composition's gesture. */
.our-story--focal-top    { --os-focal-y: 0%; }
.our-story--focal-upper  { --os-focal-y: 33%; }
.our-story--focal-centre { --os-focal-y: 50%; }
.our-story--focal-lower  { --os-focal-y: 67%; }
""", """/* The crop centre is Shopify's own focal point, not a second control here.

   image_tag writes style="object-position:X% Y%" straight onto the <img>
   whenever the image carries a focal point set in admin, and an inline style
   outranks every rule in this file. A theme-side focal select would therefore
   have moved nothing on exactly the images a merchant had bothered to position
   — a control that silently did nothing. It was removed, and admin is the
   single source of truth, which is what Phase 1 STORY-02 asked for.

   The value below is the default for an image with no focal point set. The
   prototype used `center top`, which discarded about a fifth of the picture's
   height at 1440 — the hands and chest that carry the composition's gesture. */
.our-story__image {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 33%;
}
""", 'A focal rules replaced by the admin focal point')

# --- G. the scrim comment claimed two tokens where there is one ------------
c = sub(c, """/* The photograph dissolves into the band rather than ending on a hard edge.
   Below the split that is a bottom fade; above it, a horizontal one toward the
   copy. Both are Phase 2 tokens. */
""", """/* The photograph dissolves into the band rather than ending on a hard edge.
   Below the split that is --scrim-bottom, a Phase 2 token, used as it stands.

   Above the split it is a horizontal wash written out at the breakpoint rather
   than taken from --scrim-story-horizontal. Two reasons, both measured: the
   token's stops (ink to 30%, 0.55 at 42%, clear at 56%) are the prototype's,
   and the caption rail over them measured 1.69-2.14:1 against the 4.5:1 a
   tracked 12px line needs; and the token is a fixed ink, while this band has to
   fade into cream as well. The stops below are the measured ones and their base
   colour follows the surface. Recorded as a token the band cannot use, not as a
   token overlooked. */
""", 'G scrim comment states what is and is not a token')

# --- G. two knobs that exist nowhere --------------------------------------
n = c.count('var(--os-wash-hold, 34%)') + c.count('var(--os-wash-end, 62%)')
assert n == 4, 'expected 4 wash var() reads, found %d' % n
c = c.replace('var(--os-wash-hold, 34%)', '34%').replace('var(--os-wash-end, 62%)', '62%')
done.append('G dead wash knobs inlined (%d reads)' % n)

# --- E. the body cap follows the composition ------------------------------
c = sub(c, """/* Phase 2 §26.2: the prototype capped this paragraph at 320px, about 40
   characters, which is an editorial caption measure rather than a reading
   measure. --measure-narrow is that value named. Phase 1 recorded the cap as
   correct for a three-sentence brand statement and wrong for anything longer,
   so the cap widens with the copy rather than the copy widening the column. */
.our-story__body {
  margin: var(--space-6) 0 0;
  max-width: var(--measure-narrow);
""", """/* The cap follows the composition, which is what Phase 2 §26.2 actually says:
   the prototype's 320px is "an editorial caption measure, not a reading
   measure", correct for a three-sentence brand statement and wrong for
   anything longer.

   Stacked, the copy is a full-width reading column and takes the reading
   measure --measure-body (68ch), inside §14.4's 60-75 target. At 375 the column
   is narrower than the cap anyway and nothing changes; at 768-1023 it is the
   difference between a 324px ribbon in a 640px column and a paragraph.

   At the split the copy moves into the rail's 0.9fr track beside the
   photograph, where it is editorial copy over an image again, and takes
   --measure-narrow. The track is about 416px there, so the narrow cap is what
   draws and the reading cap would never bind. See the breakpoint block. */
.our-story__body {
  margin: var(--space-6) 0 0;
  max-width: var(--measure-body);
""", 'E body cap is the reading measure when stacked')

c = sub(c, """  .our-story__content { grid-column: 1; }
  .our-story__caption { grid-column: 3; }
""", """  .our-story__content { grid-column: 1; }
  .our-story__caption { grid-column: 3; }

  /* Editorial measure again, for the reason given on the base rule. */
  .our-story__body { max-width: var(--measure-narrow); }
""", 'E narrow measure restored at the split')

# --- D. the gold budget ---------------------------------------------------
c = sub(c, """.our-story__value-title {
  margin: 0;
  color: var(--accent-current);
""", """/* Not gold. Phase 2 §26.5 allows a band two accent marks and the eyebrow is
   one; three gold value titles would make four, and the prototype's own tiles
   set their titles in cream, not gold. The weight, tracking and caps carry the
   hierarchy, and inheriting puts the title at 16.9:1 on ink and 16.7:1 on
   cream instead of the accent's 11.01 and 4.66. */
.our-story__value-title {
  margin: 0;
  color: inherit;
""", 'D value titles are not gold')

# --- G. the values row orphaned a sixth tile ------------------------------
c = sub(c, """  grid-template-columns: repeat(auto-fit, minmax(min(14rem, 100%), 1fr));
""", """  /* 17rem, not 14. The row is capped at --container-standard, so at 1440 it is
     1344px wide: a 14rem floor fits five tracks there, and the schema's sixth
     permitted block then sits alone on a second row. A 17rem floor fits four,
     so six tiles read 4 + 2 and four tiles read as one row. auto-fit collapses
     the tracks nobody fills, so the shipped three still span the full width. */
  grid-template-columns: repeat(auto-fit, minmax(min(17rem, 100%), 1fr));
""", 'G values row fits four, not five')

# --- G. an override that overrode nothing ---------------------------------
c = sub(c, """  /* The rail's hairline sits on the wash, so it takes the wash's edge colour
     rather than the band's border token, which would disappear on it. */
  .our-story__caption::after {
    background-color: var(--color-border-current);
  }

""", """""", 'G dead caption::after override removed')

open(CSS, 'w', encoding='utf-8', newline='').write(c)
print('assets/section-our-story.css rewritten')


# ===================================================================  TEMPLATE
d = json.load(open(TPL, encoding='utf-8'))
s = d['sections']['our-story']
s['settings'].pop('focal_point', None)
s['blocks'] = {
    'faith': {'type': 'value',
              'settings': {'title': 'Faith Driven', 'body': 'More Than Clothing'}},
    'community': {'type': 'value',
                  'settings': {'title': 'Community', 'body': 'People With Purpose'}},
    'quality': {'type': 'value',
                'settings': {'title': 'Premium Quality', 'body': 'Crafted To Inspire'}},
}
s['block_order'] = ['faith', 'community', 'quality']
json.dump(d, open(TPL, 'w', encoding='utf-8', newline=''),
          indent=2, ensure_ascii=False)
open(TPL, 'a', encoding='utf-8', newline='').write('\n')
done.append('templates/index.json: focal setting dropped, approved value copy')
print('templates/index.json rewritten')

print()
for i, label in enumerate(done, 1):
    print('%2d. %s' % (i, label))
