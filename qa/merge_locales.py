# -*- coding: utf-8 -*-
"""Merge the five surfaces' locale keys into locales/en.default.json.

The builders were forbidden from touching shared files, so each returned the
keys it needs and this merges them in one place. Dotted paths become nested
objects, which is also how Shopify's plural objects (.one / .other) fall out
naturally.

Namespacing follows what the file already does: storefront strings sit in a
top-level namespace per surface (header.*, cart.*, products.* — now collection.*
and footer.*), while Theme-Editor notices sit under sections.<name>.*.
"""
import collections
import json
import os

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'god-squad-theme')
TASK = (r"C:\Users\TEST\AppData\Local\Temp\claude"
        r"\C--Users-TEST-OneDrive-Documents-GodSquad-Website"
        r"\de238d03-508d-43ce-a377-210f71ff0033\tasks\wvm4y60sv.output")

keys = json.load(open(TASK, encoding='utf-8'))['result']['all_locale_keys']

p = os.path.join(THEME, 'locales', 'en.default.json')
doc = json.load(open(p, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)


def flatten(o, prefix=''):
    for k, v in o.items():
        if isinstance(v, dict):
            for r in flatten(v, prefix + k + '.'):
                yield r
        else:
            yield prefix + k, v


before = dict(flatten(doc))

added, conflicts, identical = [], [], []
for entry in keys:
    path = entry['key'].split('.')
    value = entry['value']
    node = doc
    for part in path[:-1]:
        if part not in node:
            node[part] = collections.OrderedDict()
        elif not isinstance(node[part], dict):
            conflicts.append((entry['key'], 'ancestor %r is a string' % part))
            node = None
            break
        node = node[part]
    if node is None:
        continue
    leaf = path[-1]
    if leaf in node:
        if node[leaf] == value:
            identical.append(entry['key'])
        else:
            conflicts.append((entry['key'], 'exists as %r' % node[leaf]))
        continue
    node[leaf] = value
    added.append(entry['key'])

if conflicts:
    print('CONFLICTS — nothing written:')
    for k, why in conflicts:
        print('  %-44s %s' % (k, why))
    raise SystemExit(1)

# Sort keys within each namespace so the file stays readable, but keep the
# top-level namespace order the file already established.
json.dump(doc, open(p, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
open(p, 'a', encoding='utf-8', newline='').write('\n')

after = dict(flatten(doc))
print('locale keys before: %d' % len(before))
print('locale keys after:  %d' % len(after))
print('added: %d, already identical: %d, conflicts: %d'
      % (len(added), len(identical), len(conflicts)))
print()
for k in added:
    print('  + %s' % k)
