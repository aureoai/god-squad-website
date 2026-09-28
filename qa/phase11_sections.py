# -*- coding: utf-8 -*-
"""Phase 11 — the section settings the spec names and the theme lacked."""
import collections
import json
import os
import re

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'god-squad-theme')
done = []


def patch(rel, old, new, label):
    p = os.path.join(THEME, rel)
    s = open(p, encoding='utf-8').read()
    assert s.count(old) == 1, 'NOT FOUND or ambiguous in %s: %s' % (rel, label)
    open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new, 1))
    done.append(label)


# ================================================== 1. announcement alignment
patch('sections/announcement-bar.liquid',
      """  assign bar_class = 'announcement-bar surface-dark'""",
      """  comment
    Phase 11. The desktop distribution was hardcoded: one message centred, two
    or more pushed to the outer edges. Both states already existed in
    assets/header.css; neither was reachable from the editor. The spec names
    alignment as one of the announcement bar's four merchant controls.

    Below --bp-md the bar always stacks and centres, because a phone has no
    width to distribute across — so this setting is honestly labelled as a
    desktop one rather than pretending to apply everywhere.
  endcomment
  assign bar_class = 'announcement-bar surface-dark'""",
      'announcement-bar.liquid: alignment reasoning recorded')

patch('sections/announcement-bar.liquid',
      """  <div class="{{ bar_class }}" data-announcement-bar>""",
      """  {%- liquid
    assign align = section.settings.alignment | default: 'edges'
    assign bar_class = bar_class | append: ' announcement-bar--align-' | append: align
  -%}
  <div class="{{ bar_class }}" data-announcement-bar>""",
      'announcement-bar.liquid: the alignment modifier reaches the root')

# The schema: alignment + a label that matches every other section.
p = os.path.join(THEME, 'sections', 'announcement-bar.liquid')
s = open(p, encoding='utf-8').read()
m = re.search(r'\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}', s, re.S)
doc = json.loads(m.group(1), object_pairs_hook=collections.OrderedDict)

surface = next(x for x in doc['settings'] if x.get('id') == 'surface')
assert surface['label'] == 'Surface'
surface['label'] = 'Colour scheme'
surface['options'] = [
    collections.OrderedDict([('value', 'dark'), ('label', 'Ink')]),
    collections.OrderedDict([('value', 'light'), ('label', 'Cream')]),
]

doc['settings'].append(collections.OrderedDict([
    ('type', 'select'),
    ('id', 'alignment'),
    ('label', 'Alignment on desktop'),
    ('options', [
        collections.OrderedDict([('value', 'edges'), ('label', 'Spread to the edges')]),
        collections.OrderedDict([('value', 'centre'), ('label', 'Centred together')]),
    ]),
    ('default', 'edges'),
    ('info', 'On a phone the messages always stack and centre — there is no width to spread across.'),
]))

new_schema = json.dumps(doc, indent=2, ensure_ascii=False)
s = s[:m.start(1)] + '\n' + new_schema + '\n' + s[m.end(1):]
open(p, 'w', encoding='utf-8', newline='').write(s)
done.append('announcement-bar.liquid: "Colour scheme" wording now matches the other seven '
            'sections, and an alignment setting exists')

# The CSS the modifier drives.
patch('assets/header.css',
      """@media (min-width: 768px) {
  .announcement-bar__inner {
    flex-direction: row;
    justify-content: space-between;
    min-height: var(--announcement-height);
    padding-block: 0;
    text-align: left;
  }
}""",
      """@media (min-width: 768px) {
  .announcement-bar__inner {
    flex-direction: row;
    justify-content: space-between;
    min-height: var(--announcement-height);
    padding-block: 0;
    text-align: left;
  }

  /* Phase 11. The merchant's choice, and only on desktop: below --bp-md the bar
     stacks and centres because there is no width to distribute. "Spread to the
     edges" is the shipped composition and stays the default. */
  .announcement-bar--align-centre .announcement-bar__inner {
    justify-content: center;
    gap: var(--space-6);
    text-align: center;
  }
}""",
      'header.css: the centred alignment the setting selects')

# ========================================================== 2. header show_cart
p = os.path.join(THEME, 'sections', 'header.liquid')
s = open(p, encoding='utf-8').read()
doc = json.loads(re.search(r'\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}', s, re.S).group(1),
                 object_pairs_hook=collections.OrderedDict)
idx = next(i for i, x in enumerate(doc['settings']) if x.get('id') == 'show_account')
doc['settings'].insert(idx + 1, collections.OrderedDict([
    ('type', 'checkbox'),
    ('id', 'show_cart'),
    ('label', 'Show cart'),
    ('default', True),
    ('info',
     'Leave this on unless you have another route to the cart. With it off the '
     'header has no cart control at all, and a customer who has added something '
     'can only reach the cart by typing the address.'),
]))
m = re.search(r'\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}', s, re.S)
s = s[:m.start(1)] + '\n' + json.dumps(doc, indent=2, ensure_ascii=False) + '\n' + s[m.end(1):]
open(p, 'w', encoding='utf-8', newline='').write(s)
done.append('header.liquid: a "Show cart" setting, with the consequence spelled out')

# ============================================== 3. the hero focal point, honestly
patch('sections/hero.liquid',
      '''      "info": "Where the crop centres when the image is narrower than the frame. Centre-left keeps both chest logos legible on a phone.",''',
      '''      "info": "Where the crop centres when the image is narrower than the frame. Centre-left keeps both chest logos legible on a phone. If you set a focal point on the image itself in Shopify admin, that focal point is used instead and this setting has no effect.",''',
      'hero.liquid: the focal point setting states when Shopify admin overrides it')

for i, label in enumerate(done, 1):
    print('%d. %s' % (i, label))
