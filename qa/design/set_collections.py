# -*- coding: utf-8 -*-
"""Set the collection handle on both homepage product bands to `all`.

Phase 6 shipped `templates/index.json` with no collection handle on either
featured-collection section, deliberately: Phase 1 COLL-03 recorded the
collection taxonomy as BUSINESS INFORMATION REQUIRED, and until a merchant picks
one the section's own schema says it "does not render on the live store".

FIRST ATTEMPT WAS WRONG, AND THIS IS THE CORRECTION.

`all` was written here on the belief that Shopify generates a collection with
that handle on every store, so both bands would render with no admin setup.
Shopify's own documentation for the `collection` input setting says otherwise: it
returns "a collection object... blank, if no selection has been made, the
selection isn't visible, or the selection no longer exists", the picker is
populated with "the available collections for the store", and NO reserved handle
such as `all` is documented for it.

`collections.all` is a Liquid ACCESSOR and `/collections/all` is a virtual route.
Neither is a collection record, so nothing stores the handle `all` unless a
merchant creates a collection that happens to be handled that way. A setting of
`all` therefore resolves to blank, the section's `has_products` stays false, and
the band renders nothing — the exact state this change was meant to fix.

So: the semantic handles instead. They match the section presets and the design's
own band names, they document intent in the file, and they work the moment the
merchant creates two collections with these handles. Nothing renders until then,
because on Shopify nothing can.

Key order is preserved so the diff is one added line per section rather than a
reshuffled file.
"""
import io
import json
import os
import sys
from collections import OrderedDict

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
p = os.path.join(THEME, 'templates', 'index.json')

doc = json.load(io.open(p, encoding='utf-8'), object_pairs_hook=OrderedDict)

# Section key -> the handle the merchant must create in Shopify admin.
HANDLES = {
    'new-drop': 'new-drop',
    'best-sellers': 'best-sellers',
}

changed = []
for key, sec in doc.get('sections', OrderedDict()).items():
    if sec.get('type') != 'featured-collection':
        continue
    want = HANDLES.get(key)
    if not want:
        print('  --  %-14s no handle mapped, left alone' % key)
        continue
    settings = sec.setdefault('settings', OrderedDict())
    before = settings.get('collection', '(absent)')
    if before == want:
        print('  --  %-14s already %r' % (key, want))
        continue
    # Put `collection` first in the settings block: it is the setting the whole
    # section depends on, and a reader should meet it before the cosmetics.
    new_settings = OrderedDict()
    new_settings['collection'] = want
    for k, v in settings.items():
        if k != 'collection':
            new_settings[k] = v
    sec['settings'] = new_settings
    changed.append((key, before))
    print('  ok  %-14s collection: %s -> %r' % (key, before, want))

if changed:
    io.open(p, 'w', encoding='utf-8').write(
        json.dumps(doc, indent=2, ensure_ascii=False) + '\n')

print()
print('=== VERIFY ===')
back = json.load(io.open(p, encoding='utf-8'))
print('  templates/index.json parses OK')
for key, sec in back['sections'].items():
    if sec['type'] == 'featured-collection':
        print('  %-14s type=%-22s collection=%r products_to_show=%s'
              % (key, sec['type'], sec['settings'].get('collection'),
                 sec['settings'].get('products_to_show')))
print('  section order unchanged: %s' % ' -> '.join(back.get('order', [])))
