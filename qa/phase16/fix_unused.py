# -*- coding: utf-8 -*-
"""Phase 16 — remove the two assignments Theme Check found unused.

Both verified by reading the code, not by trusting the checker:

  featured-collection.liquid  `step = 304` is a leftover from the sizes
  arithmetic that Phase 12 extracted into snippets/grid-sizes.liquid. The only
  other occurrences of the word in that file are a comment and four "step": 1
  schema keys.

  product-media-gallery.liquid  `loading_attr` is computed from forloop.first
  and then never read: the two image_tag calls below it branch on forloop.first
  themselves and hardcode loading: 'eager' / 'lazy'. The rendered markup is
  correct, which is why the Phase 16 image audit passes; the variable is simply
  orphaned.

Deleting the assignment is the whole fix. Collapsing the two near-identical
image_tag calls into one that USES the variable would also be valid, and is
deliberately not done: it changes emitted attributes on the product page's LCP
image, and this is an optimization phase, not a refactoring one.
"""
import io
import os

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
def sub(rel, old, new, label):
    p = os.path.join(THEME, rel)
    s = io.open(p, encoding='utf-8').read()
    if old not in s:
        raise SystemExit('NOT FOUND in %s: %s' % (rel, label))
    if s.count(old) != 1:
        raise SystemExit('AMBIGUOUS (%d) in %s: %s' % (s.count(old), rel, label))
    n0 = len(s)
    io.open(p, 'w', encoding='utf-8').write(s.replace(old, new, 1))
    print('  ok  %-38s %s  (%d -> %d bytes)' % (rel, label, n0, n0 - len(old) + len(new)))


sub('sections/featured-collection.liquid',
    """  assign gap_m = 16
  assign col_min = 272
  assign step = 304
""",
    """  assign gap_m = 16
  assign col_min = 272
""",
    'drop the orphaned `step`')

sub('snippets/product-media-gallery.liquid',
    """          assign slide_id = section_id | append: '-media-' | append: media.id
          assign loading_attr = 'lazy'
          if forloop.first
            assign loading_attr = 'eager'
          endif
""",
    """          assign slide_id = section_id | append: '-media-' | append: media.id
""",
    'drop the orphaned `loading_attr`')
