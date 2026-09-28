# -*- coding: utf-8 -*-
"""Phase 16 — wire the social metadata and the apple-touch-icon into the head."""
import io
import json
import os
from collections import OrderedDict

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
def sub(rel, old, new, label):
    p = os.path.join(THEME, rel)
    s = io.open(p, encoding='utf-8').read()
    if old not in s:
        raise SystemExit('NOT FOUND in %s: %s' % (rel, label))
    if s.count(old) != 1:
        raise SystemExit('AMBIGUOUS (%d) in %s: %s' % (s.count(old), rel, label))
    n0 = len(s)
    s = s.replace(old, new, 1)
    io.open(p, 'w', encoding='utf-8').write(s)
    print('  ok  %-28s %-46s %d -> %d' % (rel, label, n0, len(s)))


# ---------------------------------------------------- the favicon block
# Phase 16 measured the head and found no apple-touch-icon. Shopify's own
# favicon setting supplies it; iOS wants 180x180 and ignores the <link rel=icon>
# that is already there.
sub('layout/theme.liquid',
    """    {%- if settings.favicon != blank -%}
      <link rel="icon" type="image/png" href="{{ settings.favicon | image_url: width: 32, height: 32 }}">
    {%- endif -%}""",
    """    {%- comment -%}
      The favicon, at the three sizes that are actually asked for. Phase 16
      added the second and third: iOS ignores rel="icon" entirely and looks for
      apple-touch-icon at 180x180, and without it a customer who adds the store
      to their home screen gets a screenshot of the page instead of the mark.

      All three come from one Shopify setting, resized by Shopify, so there is
      one file to upload and no second asset to keep in step.
    {%- endcomment -%}
    {%- if settings.favicon != blank -%}
      <link rel="icon" type="image/png" href="{{ settings.favicon | image_url: width: 32, height: 32 }}">
      <link rel="icon" type="image/png" sizes="192x192" href="{{ settings.favicon | image_url: width: 192, height: 192 }}">
      <link rel="apple-touch-icon" sizes="180x180" href="{{ settings.favicon | image_url: width: 180, height: 180 }}">
    {%- endif -%}""",
    'apple-touch-icon and 192px icon')

# ------------------------------------------------- the social metadata
# Placed immediately after the description, so everything describing the
# document to another machine sits in one block.
sub('layout/theme.liquid',
    """    {%- if page_description -%}
      <meta name="description" content="{{ page_description | escape }}">
    {%- endif -%}""",
    """    {%- if page_description -%}
      <meta name="description" content="{{ page_description | escape }}">
    {%- endif -%}

    {%- comment -%}
      Phase 16. Open Graph and Twitter card tags. Rendered from a snippet rather
      than written here because the image chain is four branches deep and the
      head should stay readable. Every value is a Shopify object; nothing in it
      is written copy. See snippets/meta-social.liquid.
    {%- endcomment -%}
    {% render 'meta-social' %}""",
    'Open Graph + Twitter card')


# ------------------------------------------------------ the share image
sp = os.path.join(THEME, 'config', 'settings_schema.json')
schema = json.load(io.open(sp, encoding='utf-8'), object_pairs_hook=OrderedDict)
brand = next(g for g in schema if g.get('name') == 'Brand')
if not any(s.get('id') == 'share_image' for s in brand['settings']):
    brand['settings'].append(OrderedDict([
        ('type', 'image_picker'),
        ('id', 'share_image'),
        ('label', 'Social sharing image'),
        ('info',
         'Shown when someone shares a link to this store on Facebook, Viber, X '
         'or Instagram. Product and collection pages use their own image; this '
         'covers everything else. Around 1200 x 630 works best \u2014 a logo on '
         'its own tends to be cropped badly. Leave it empty and the logo is '
         'used instead.'),
    ]))
    io.open(sp, 'w', encoding='utf-8').write(
        json.dumps(schema, indent=2, ensure_ascii=False) + '\n')
    print('  ok  %-28s %s' % ('config/settings_schema.json', 'share_image setting (Brand)'))

dp = os.path.join(THEME, 'config', 'settings_data.json')
data = json.load(io.open(dp, encoding='utf-8'), object_pairs_hook=OrderedDict)
for block in (data['current'], data['presets']['God Squad']):
    block.setdefault('share_image', '')
io.open(dp, 'w', encoding='utf-8').write(
    json.dumps(data, indent=2, ensure_ascii=False) + '\n')
print('  ok  %-28s %s' % ('config/settings_data.json', 'share_image in current + preset'))
