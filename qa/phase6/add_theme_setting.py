# -*- coding: utf-8 -*-
"""Phase 6: add the one theme-level product setting Phase 2 section 27.6.5 requires."""
import json, collections, io, os

root = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website"

# --- settings_schema.json -------------------------------------------------
p = os.path.join(root, 'config', 'settings_schema.json')
schema = json.load(open(p, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)

assert not any(
    s.get('id') == 'product_image_ratio'
    for group in schema if isinstance(group, dict)
    for s in group.get('settings', [])
), "product_image_ratio already present"

group = collections.OrderedDict()
group['name'] = 'Products'
group['settings'] = [
    collections.OrderedDict([
        ('type', 'paragraph'),
        ('content',
         'One image shape for the whole catalogue. It is set here rather than on each '
         'section because a ratio that differs between two rows of the same shop is a '
         'bug, not a choice: mixed shapes break the grid rhythm and force product '
         'photographs to be letterboxed onto the tile ground.'),
    ]),
    collections.OrderedDict([
        ('type', 'select'),
        ('id', 'product_image_ratio'),
        ('label', 'Product image shape'),
        ('options', [
            collections.OrderedDict([('value', 'square'), ('label', 'Square (1:1)')]),
            collections.OrderedDict([('value', 'portrait'), ('label', 'Portrait (4:5)')]),
        ]),
        ('default', 'square'),
    ]),
]

# Insert before the Brand group so Colours / Typography / Layout / Products / Brand.
idx = next(i for i, g in enumerate(schema) if isinstance(g, dict) and g.get('name') == 'Brand')
schema.insert(idx, group)
open(p, 'w', encoding='utf-8', newline='').write(json.dumps(schema, indent=2, ensure_ascii=False) + '\n')
print('settings_schema.json: Products group added')

# --- settings_data.json ---------------------------------------------------
p2 = os.path.join(root, 'config', 'settings_data.json')
data = json.load(open(p2, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
data['current']['product_image_ratio'] = 'square'
data['presets']['God Squad']['product_image_ratio'] = 'square'
open(p2, 'w', encoding='utf-8', newline='').write(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
print('settings_data.json: default written')

# --- layout/theme.liquid --------------------------------------------------
p3 = os.path.join(root, 'layout', 'theme.liquid')
t = open(p3, encoding='utf-8').read()
old = """        --radius-sm: {{ settings.radius_sm | default: 2 }}px;"""
new = """        --radius-sm: {{ settings.radius_sm | default: 2 }}px;
        {%- comment -%}
          One ratio for the whole catalogue (Phase 2 section 27.6.5). The token
          already exists in both shapes; this picks which one every product
          card in the theme reads.
        {%- endcomment -%}
        {%- if settings.product_image_ratio == 'portrait' -%}
          --product-aspect: var(--product-aspect-wide);
        {%- endif -%}"""
assert old in t, 'radius line not found'
open(p3, 'w', encoding='utf-8', newline='').write(t.replace(old, new, 1))
print('theme.liquid: product ratio wired')
