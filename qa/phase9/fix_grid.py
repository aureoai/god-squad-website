# -*- coding: utf-8 -*-
"""The product grid's mobile gutter.

Measured at 375: the gap between two cards is 32px and the gutter to the screen
edge is 24px. The space between the cards is therefore LARGER than the space
around the row, which inverts the spacing hierarchy — two cards read as two
separate things rather than as one row — and it costs each card 8px of the
147px it has.

Phase 2 §27.6 rule 4 already records the intended value as 24px and notes the
token's 32px as a comment "needing correction". This does not change the token,
which the tablet and desktop tiers still use; it tightens the COLUMN gap below
--bp-md, which is what the brief means by mobile using intentionally reduced
spacing rather than desktop spacing scaled down.

The row gap is deliberately left at 32px. Vertical space is not the scarce
dimension on a phone, and two rows of cards need the separation.

The Liquid's sizes arithmetic is updated in the same commit, because a narrower
gap makes the cards WIDER and a sizes attribute computed against the old gap
would under-declare them.
"""
import re

CSS = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\component-product-card.css"
LIQ = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\sections\featured-collection.liquid"
done = []

s = open(CSS, encoding='utf-8').read()
old = """/* Below the tablet tier the floor is relaxed, and only there. Phase 2 section
   13.9 permits two columns on a phone; the 272px catalogue floor would force
   one, because a 375px viewport has only 327px of content box."""
new = """/* Below the tablet tier, two things change and only there.

   The COLUMN gap tightens to --space-4 16px. Measured at 375, a 32px gap sat
   between two 147px cards inside a 24px gutter — the space between the cards
   was wider than the space around the row, which reads as two bands rather
   than one, and it cost each card 8px it could not spare. The row gap stays at
   32px: vertical space is not the scarce dimension on a phone. Phase 2 §27.6
   rule 4 records 24px as the intended grid gap and the token's 32px as a
   comment needing correction; this is the mobile half of that.

   The floor is relaxed too. Phase 2 section 13.9 permits two columns on a
   phone; the 272px catalogue floor would force one, because a 375px viewport
   has only 327px of content box."""
assert old in s
s = s.replace(old, new, 1)

# The mobile block already exists for the floor; add the gap to it.
m = re.search(r'@media \(max-width: 767px\) \{\s*\n  \.product-grid \{\n(.*?)\n  \}', s, re.S)
assert m, 'mobile .product-grid block not found'
body = m.group(1)
assert '--product-grid-gap' not in body, 'gap already set'
s = s.replace(m.group(0),
              '@media (max-width: 767px) {\n  .product-grid {\n'
              '    --product-grid-gap: var(--space-4);\n'
              '    row-gap: var(--space-6);\n'
              + body + '\n  }', 1)
open(CSS, 'w', encoding='utf-8', newline='').write(s)
done.append('component-product-card.css: the mobile column gap is 16px, the row gap stays 32px')

# ------------------------------------------------------------------- Liquid
t = open(LIQ, encoding='utf-8').read()
old_l = """  assign gap = 32
  assign col_min = 272
  assign step = 304"""
new_l = """  assign gap = 32
  comment
    The column gap is not the same at every tier. Below --bp-md the grid
    tightens to --space-4 16px, because a 32px gap between two 147px cards sat
    inside a 24px gutter and read as two bands rather than one row. A narrower
    gap makes the cards WIDER, so the mobile clauses of the sizes attribute
    have to be computed against it or they under-declare the slot.
  endcomment
  assign gap_m = 16
  assign col_min = 272
  assign step = 304"""
assert old_l in t
t = t.replace(old_l, new_l, 1)

old_m = """  assign need_m = cols_m | times: 128
  assign need_m = cols_m | minus: 1 | times: gap | plus: need_m
  assign threshold_m = need_m | plus: chrome_m"""
new_m = """  assign need_m = cols_m | times: 128
  assign need_m = cols_m | minus: 1 | times: gap_m | plus: need_m
  assign threshold_m = need_m | plus: chrome_m"""
assert old_m in t
t = t.replace(old_m, new_m, 1)

old_g = """  assign gaps_m = cols_m | minus: 1 | times: gap
  assign gaps_m_low = cols_m_low | minus: 1 | times: gap"""
new_g = """  assign gaps_m = cols_m | minus: 1 | times: gap_m
  assign gaps_m_low = cols_m_low | minus: 1 | times: gap_m"""
assert old_g in t
t = t.replace(old_g, new_g, 1)

old_c = """    Mobile: the floor is 8rem/128px below 768, so the step is 160."""
new_c = """    Mobile: the floor is 8rem/128px below 768 and the gap is 16px, so the step
    is 144."""
assert old_c in t
t = t.replace(old_c, new_c, 1)

open(LIQ, 'w', encoding='utf-8', newline='').write(t)
done.append('featured-collection.liquid: the mobile sizes clauses use the mobile gap')

for i, label in enumerate(done, 1):
    print('%d. %s' % (i, label))
