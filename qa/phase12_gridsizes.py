# -*- coding: utf-8 -*-
"""Point the two identical grids at snippets/grid-sizes.liquid, and fix the third.

main-collection and main-search carried the SAME ninety-line derivation.
Phase 10 fixed a blocker in one; the other kept it — main-search at three
columns still emits `(min-width: 976px)`, below the 1024 breakpoint where the
desktop column count actually takes effect.

featured-collection is NOT consolidated, and that is deliberate: its
copy-column layout scales the needed row by 1000/727 because the grid occupies
only 72.7% of it, so its derivation is genuinely different rather than
duplicated. It gets the same two corrections in place.
"""
import os

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'god-squad-theme')
done = []

REPLACEMENT = """  comment
    The sizes attribute is derived by snippets/grid-sizes.liquid, shared with
    the other grid that uses this exact arithmetic.

    It used to be ninety duplicated lines here. Phase 10 found that the desktop
    clause fired below its own breakpoint, booked it as a blocker, and fixed it
    in ONE of the copies; the other carried the bug for two more phases. Fixing
    an instance is not fixing a rule.
  endcomment
  assign chrome_d = 96
  capture sizes_attr
    render 'grid-sizes', cols_d: cols_d, cols_t: cols_t, cols_m: cols_m, chrome_d: chrome_d
  endcapture
"""

for name in ('main-collection.liquid', 'main-search.liquid'):
    p = os.path.join(THEME, 'sections', name)
    lines = open(p, encoding='utf-8').read().split('\n')

    start = next(i for i, ln in enumerate(lines) if ln.strip() == 'assign gap = 32')
    end = next(i for i in range(start, len(lines)) if lines[i].strip() == 'endcapture')
    span = '\n'.join(lines[start:end + 1])
    assert 'capture sizes_attr' in span, 'span missed the capture in ' + name
    assert 'times: 1000' not in span, 'this file has a scaled derivation: ' + name

    lines[start:end + 1] = REPLACEMENT.rstrip('\n').split('\n')
    open(p, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
    done.append('%s: %d lines -> the shared snippet' % (name, end - start + 1))


# ---------------------------------------------------- featured-collection
p = os.path.join(THEME, 'sections', 'featured-collection.liquid')
s = open(p, encoding='utf-8').read()

old = """  assign threshold_d = need_d | plus: chrome_d
"""
new = """  assign threshold_d = need_d | plus: chrome_d

  comment
    Floored at the tier boundary. The desktop column count only takes effect at
    --bp-lg 1024, but the threshold is derived from the column arithmetic alone,
    so the full-bleed layout at three columns computes 976. Left there, the
    clause would match from 976 up while the grid between 976 and 1023 is still
    painting the TABLET count — declaring a slot narrower than the one that
    paints. A sizes clause must never claim a width before the layout that
    produces it applies.

    This section is not consolidated into snippets/grid-sizes.liquid because its
    copy-column layout scales the needed row by 1000/727 above: its derivation
    is genuinely different, not duplicated.
  endcomment
  if threshold_d < 1024
    assign threshold_d = 1024
  endif
"""
assert s.count(old) == 1, 'threshold line not found'
s = s.replace(old, new, 1)

old = """  assign capped_track = capped_row | minus: gaps_d | divided_by: cols_d | plus: 1"""
new = """  comment
    Divide by what FITS, not by what was asked for. The grid is auto-fill with a
    272px floor, so at the container cap it paints only as many columns as that
    floor allows: with four columns and the container at its 1200px minimum,
    dividing by the requested four declares 253px for a track that actually
    paints 346px — a 27% under-declaration, which makes the browser fetch a
    candidate it then has to upscale.
  endcomment
  assign col_slot = col_min | plus: gap
  assign fits_d = capped_row | plus: gap | divided_by: col_slot
  if fits_d < 1
    assign fits_d = 1
  endif
  assign cols_capped = cols_d
  if fits_d < cols_d
    assign cols_capped = fits_d
  endif
  assign gaps_capped = cols_capped | minus: 1 | times: gap
  assign capped_track = capped_row | minus: gaps_capped | divided_by: cols_capped | plus: 1"""
assert s.count(old) == 1, 'capped_track not found'
s = s.replace(old, new, 1)
open(p, 'w', encoding='utf-8', newline='').write(s)
done.append('featured-collection.liquid: both corrections applied in place')

for i, label in enumerate(done, 1):
    print('%d. %s' % (i, label))
