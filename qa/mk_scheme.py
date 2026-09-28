# -*- coding: utf-8 -*-
"""Phase 2 guardrails G1 and G2, in config/.

Replaces the three unconstrained `color` pickers with one verified scheme
select. Every ratio below was recomputed in Phase 10 from WCAG 2.2 relative
luminance and matches Phase 2 section 3 exactly.
"""
import json, os, collections

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'god-squad-theme')
# ----------------------------------------------------------- settings_schema
p = os.path.join(THEME, 'config', 'settings_schema.json')
schema = json.load(open(p, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)

colours = next(g for g in schema if g.get('name') == 'Colours')
ids = [s.get('id') for s in colours['settings'] if s.get('id')]
assert ids == ['color_ink', 'color_cream', 'color_gold'], ids

colours['settings'] = [
    collections.OrderedDict([
        ('type', 'paragraph'),
        ('content',
         'The brand palette is chosen as a whole rather than as three separate '
         'colours. Each scheme ships its dark-surface gold and its light-surface '
         'partner together and carries measured contrast for every pairing in the '
         'system, so no combination here can fall below WCAG AA.'),
    ]),
    collections.OrderedDict([
        ('type', 'select'),
        ('id', 'color_scheme'),
        ('label', 'Colour scheme'),
        ('options', [
            collections.OrderedDict([
                ('value', 'godsquad'),
                ('label', 'God Squad (approved palette)'),
            ]),
        ]),
        ('default', 'godsquad'),
        ('info',
         'Measured: cream on near black 17.04:1, near black on cream 17.04:1, '
         'muted gold on near black 11.01:1, and the light-surface gold #82672B '
         'on cream 4.66:1. Muted gold is 1.55:1 on cream and is therefore a '
         'dark-surface accent only, which the theme enforces for you.'),
    ]),
]

json.dump(schema, open(p, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
open(p, 'a', encoding='utf-8', newline='').write('\n')
print('settings_schema.json: three colour pickers -> one verified scheme select')

# ------------------------------------------------------------- settings_data
p = os.path.join(THEME, 'config', 'settings_data.json')
data = json.load(open(p, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)


def migrate(block):
    for dead in ('color_ink', 'color_cream', 'color_gold'):
        block.pop(dead, None)
    # Put the scheme first so the file reads in the same order as the schema.
    out = collections.OrderedDict()
    out['color_scheme'] = 'godsquad'
    for k, v in block.items():
        out[k] = v
    return out


data['current'] = migrate(data['current'])
for name in list(data.get('presets', {})):
    data['presets'][name] = migrate(data['presets'][name])

json.dump(data, open(p, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
open(p, 'a', encoding='utf-8', newline='').write('\n')
print('settings_data.json: migrated current and every preset')
