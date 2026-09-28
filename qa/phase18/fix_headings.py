# -*- coding: utf-8 -*-
"""Phase 18 — one heading level, one treatment. Five rules, one decision.

TWO FINDINGS THAT ARE THE SAME EDIT.

1. THE EMPTY STATES. Measured on the built pages, not read off the stylesheet:

     empty cart        <h1> "Your cart"           Playfair 40px 900 uppercase
                       <p>  "Your cart is empty." Playfair 40px 900 uppercase
     empty collection  <h1> "Empty Drop"          Playfair 40px 900 uppercase
                       <p>  "This collection…"    Playfair 40px 900 uppercase
     search, none      <h1> "Search"              Playfair 40px 900 uppercase
                       <p>  "No results for…"     Playfair 24px 600 sentence

   The page <h1> renders unconditionally above the empty state, so two of the
   three show a <p> at the exact size, weight and case of the real page title
   directly beneath it — a heading level drawn twice, one of which is not a
   heading. Search already does the subordinate thing.

2. THE H3/H4 FAMILY. design-tokens.css:170 states the rule in the token file
   itself — "Headings — Playfair for H1-H2, Jost for H3-H4 (interface
   headings)" — and PHASE-2 §6.1 line 486-487 gives --type-h3 and --type-h4
   Family = body, Weight = 600, Transform = sentence, Usage "Interface heading"
   / "Card and block heading". Three rules ask the display family at those
   sizes. section-main-page.css does it correctly, so the theme already
   contains both the rule and a working example of it.

   There is a second consequence. layout/theme.liquid registers the display
   font with font_face alone and no font_modify, and settings_data.json sets
   type_display_font to playfair_display_n9 — weight 900 only. CSS font
   matching for a target above 500 searches heavier faces first, so
   --weight-semibold against a 900-only family resolves to 900: these rules
   said 600 and rendered 900. Moving them to the body family makes the
   declaration true, because theme.liquid DOES register Jost 600.

WHAT IS NOT CHANGED. .header__wordmark also sets the display family at
--type-h3-size, and it stays: a wordmark is a logotype, not an interface
heading, and the H1-H2 rule is about headings. Sweeping it in because it
matched a grep would be the "fixing an instance is not fixing a rule" error in
reverse.
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ASSETS = os.path.join(
    r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\god-squad-theme", 'assets')

EMPTY_NOTE = """/* Phase 18 took this down to the interface-heading row. It carried the same
   four type declarations as its own page's <h1> — measured as Playfair 40px 900
   uppercase on both — so an empty %s rendered the page title twice, once
   as the real <h1> and once as this <p> immediately beneath it.

   PHASE-2 §6.1 gives --type-h3 Family = body, Weight = 600, Transform =
   sentence, Usage "Interface heading", which is what this is. The search page's
   equivalent was already the subordinate size and is now the same family too,
   so all three empty states read as one treatment. */"""

JOBS = [
    # ---------------------------------------------------------- empty states
    ('component-cart-line.css', 'cart',
     """.cart-empty__title {
  margin: 0;
  font-family: var(--font-display);
  font-size: var(--type-display-m-size);
  font-weight: var(--weight-black);
  line-height: var(--type-display-m-lh);
  text-transform: uppercase;
}""",
     """.cart-empty__title {
  margin: 0;
  font-family: var(--font-body);
  font-size: var(--type-h3-size);
  font-weight: var(--weight-semibold);
  line-height: var(--type-h3-lh);
}"""),

    ('section-main-collection.css', 'collection',
     """.main-collection__empty-title {
  margin: 0;
  color: inherit;
  font-family: var(--font-display);
  font-size: var(--type-display-m-size);
  font-weight: var(--weight-black);
  line-height: var(--type-display-m-lh);
  text-transform: uppercase;
}""",
     """.main-collection__empty-title {
  margin: 0;
  color: inherit;
  font-family: var(--font-body);
  font-size: var(--type-h3-size);
  font-weight: var(--weight-semibold);
  line-height: var(--type-h3-lh);
}"""),
]

# ------------------------------------------- the three display-family h3/h4s
FAMILY = [
    ('section-main-search.css', '.main-search__empty-title'),
    ('section-main-search.css', '.main-search__other-title'),
    ('component-facets.css', '.facets__bar-title'),
]

FAMILY_NOTE = """/* Phase 18: --font-body, not --font-display. design-tokens.css:170 states the
   rule — "Playfair for H1-H2, Jost for H3-H4 (interface headings)" — and
   PHASE-2 §6.1 assigns the h3/h4 rows the body family at weight 600. It also
   made the weight honest: the display font is registered as playfair_display_n9
   with no font_modify, so --weight-semibold against a 900-only family resolved
   to 900. Jost 600 IS registered (layout/theme.liquid), so 600 now means 600. */
"""

for fname, what, old, new in JOBS:
    p = os.path.join(ASSETS, fname)
    s = io.open(p, encoding='utf-8').read()
    if s.count(old) != 1:
        print('  *** %-30s anchor not unique (%d)' % (fname, s.count(old)))
        continue
    io.open(p, 'w', encoding='utf-8').write(
        s.replace(old, (EMPTY_NOTE % what) + '\n' + new, 1))
    print('  ok  %-30s %s -> interface heading' % (fname, old.split(' {')[0]))

for fname, sel in FAMILY:
    p = os.path.join(ASSETS, fname)
    s = io.open(p, encoding='utf-8').read()
    i = s.find(sel + ' {')
    if i < 0:
        print('  *** %-30s %s not found' % (fname, sel))
        continue
    j = s.index('}', i)
    block = s[i:j]
    if 'var(--font-display)' not in block:
        print('  --  %-30s %s already body family' % (fname, sel))
        continue
    newblock = block.replace('var(--font-display)', 'var(--font-body)', 1)
    s = s[:i] + FAMILY_NOTE + newblock + s[j:]
    io.open(p, 'w', encoding='utf-8').write(s)
    print('  ok  %-30s %s -> --font-body' % (fname, sel))
