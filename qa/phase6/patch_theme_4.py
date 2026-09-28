# -*- coding: utf-8 -*-
"""Surface the copy-column trade-off in the Theme Editor.

Measured: with the copy rail beside it, the New Drop grid carries 2 columns
from 1024 to 1280 and reaches 3 only at 1440, because the rail takes about a
third of the row and a tile never goes below 272px. In the full-width layout
the same collection reaches 3 columns at 1024. A merchant choosing between the
two layouts should be told that, not left to discover it.
"""
p = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\sections\featured-collection.liquid"
s = open(p, encoding='utf-8').read()

old = """    {
      "type": "select",
      "id": "layout",
      "label": "Layout",
      "options": ["""
new = """    {
      "type": "select",
      "id": "layout",
      "label": "Layout",
      "info": "The copy column takes about a third of the row, so the grid beside it carries fewer products per row: a three-column grid reaches three columns at 1440px wide with the copy beside it, and at 1024px with the copy above it.",
      "options": ["""
assert old in s, 'layout setting not found'
s = s.replace(old, new, 1)

old2 = """    {
      "type": "range",
      "id": "products_to_show",
      "label": "Products to show",
      "min": 2,
      "max": 12,
      "step": 1,
      "default": 3
    },"""
new2 = """    {
      "type": "range",
      "id": "products_to_show",
      "label": "Products to show",
      "min": 2,
      "max": 12,
      "step": 1,
      "default": 3,
      "info": "A count that divides evenly into the column count fills its rows. Three products in a two-column grid leaves one on a row of its own."
    },"""
assert old2 in s, 'products_to_show setting not found'
s = s.replace(old2, new2, 1)

open(p, 'w', encoding='utf-8', newline='').write(s)
print('featured-collection.liquid: layout and count trade-offs documented in the editor')
