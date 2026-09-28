# -*- coding: utf-8 -*-
"""Phase 18 — consolidate the two paginators into one component.

section-main-collection.css stated the promotion rule and its trigger in
writing; the trigger had been met since Phase 13 shipped search. This performs
the move, merges the two implementations (see snippets/pagination.liquid for
which half of each survived and why), and deletes both originals.
"""
import io
import json
import os
import re
from collections import OrderedDict

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
def read(rel):
    return io.open(os.path.join(THEME, rel), encoding='utf-8').read()


def write(rel, s):
    io.open(os.path.join(THEME, rel), 'w', encoding='utf-8').write(s)


def sub(rel, old, new, label):
    s = read(rel)
    if old not in s:
        raise SystemExit('NOT FOUND in %s: %s' % (rel, label))
    if s.count(old) != 1:
        raise SystemExit('AMBIGUOUS (%d) in %s: %s' % (s.count(old), rel, label))
    write(rel, s.replace(old, new, 1))
    print('  ok  %-34s %s' % (rel, label))


def cut(rel, start_marker, end_marker, label):
    """Remove everything from start_marker up to (not including) end_marker."""
    s = read(rel)
    i = s.index(start_marker)
    j = s.index(end_marker, i)
    write(rel, s[:i] + s[j:])
    print('  ok  %-34s %s (-%d bytes)' % (rel, label, j - i))


# ===================================================== 1. the component sheet
collection_css = read('assets/section-main-collection.css')
start = collection_css.index('/* --------------------------------------------------------------- pagination')
end = collection_css.index('/* ------------------------------------------------------------------- empty */')
block = collection_css[start:end]

# Keep only the rules, replacing the section-local preamble with a component one.
rules = block[block.index('.pagination {'):]

header = """/* ============================================================================
   GOD SQUAD — Pagination
   Phase 18. The paginator, as a component, because it has two consumers.

   It lived in section-main-collection.css with a comment that named its own
   promotion trigger: "It stays in this stylesheet only while this is its single
   consumer. The moment a second surface renders it, the block moves to
   assets/component-pagination.css and is linked from layout/theme.liquid."

   Phase 13 gave it a second consumer and the move did not happen, so
   main-search grew its own paginator under its own class names in its own
   stylesheet — and the two drifted. Collection rendered caption type and marked
   the current page with weight and a rule; search rendered tracked uppercase
   label type and marked the current page with gold.

   These are collection's rules. snippets/pagination.liquid records which half
   of each implementation survived and why; the short version is that the type
   and the current-page marker are collection's, and the accessibility is
   search's.

   Loaded from layout/theme.liquid beside the other shared components, which is
   the rule Phase 6 applied to the button system and Phase 8 to the cart line.
   ========================================================================== */

"""
write('assets/component-pagination.css', header + rules.rstrip() + '\n')
print('  ok  %-34s created (%d bytes)'
      % ('assets/component-pagination.css', len(header + rules)))

# ============================================== 2. remove both original blocks
cut('assets/section-main-collection.css',
    '/* --------------------------------------------------------------- pagination',
    '/* ------------------------------------------------------------------- empty */',
    'pagination block removed')

search_css = read('assets/section-main-search.css')
s_start = search_css.index('.main-search__pagination {')
# Everything up to the rule that does NOT belong to the paginator.
s_end = search_css.index('.main-search__other-link:hover')
# Walk back to the comment that introduces that surviving rule, if there is one.
tail = search_css[:s_end]
comment_at = tail.rfind('/*')
if comment_at > s_start:
    s_end = comment_at
write('assets/section-main-search.css', search_css[:s_start] + search_css[s_end:])
print('  ok  %-34s pagination block removed (-%d bytes)'
      % ('assets/section-main-search.css', s_end - s_start))

# ================================================== 3. link the component
sub('layout/theme.liquid',
    """    {{ 'component-quantity.css' | asset_url | stylesheet_tag }}""",
    """    {%- comment -%}
      Phase 18 promoted the paginator for the reason Phase 6 promoted the button
      system: a second consumer appeared. It had been built twice, under two
      class systems, and the two had drifted.
    {%- endcomment -%}
    {{ 'component-pagination.css' | asset_url | stylesheet_tag }}
    {{ 'component-quantity.css' | asset_url | stylesheet_tag }}""",
    'component-pagination.css linked from the layout')

# ================================================== 4. both markups render it
coll = read('sections/main-collection.liquid')
c_start = coll.index('          <nav class="pagination" aria-label=')
c_end = coll.index('          </nav>', c_start) + len('          </nav>\n')
write('sections/main-collection.liquid',
      coll[:c_start] + '          {% render \'pagination\', paginate: paginate %}\n' + coll[c_end:])
print('  ok  %-34s renders the shared paginator' % 'sections/main-collection.liquid')

srch = read('sections/main-search.liquid')
s2 = srch.index('          <nav class="main-search__pagination" aria-label=')
s3 = srch.index('          </nav>', s2) + len('          </nav>\n')
write('sections/main-search.liquid',
      srch[:s2]
      + "          {% render 'pagination', paginate: paginate, label: 'sections.search.pagination' | t %}\n"
      + srch[s3:])
print('  ok  %-34s renders the shared paginator' % 'sections/main-search.liquid')

# ================================================== 5. one set of locale keys
lp = os.path.join(THEME, 'locales', 'en.default.json')
loc = json.load(io.open(lp, encoding='utf-8'), object_pairs_hook=OrderedDict)
pag = loc['general']['pagination']
# Search's wordings are the better ones out of context: a link whose whole
# accessible name is "Previous" says less than "Previous page".
pag['previous'] = 'Previous page'
pag['next'] = 'Next page'
pag['page_number'] = 'Page {{ number }}'
pag.pop('page', None)
# The four search-only keys are gone with the markup that used them, except the
# nav label, which main-search still passes.
for k in ('page_number', 'previous_page', 'next_page'):
    loc['sections']['search'].pop(k, None)
io.open(lp, 'w', encoding='utf-8').write(json.dumps(loc, indent=2, ensure_ascii=False) + '\n')
print('  ok  %-34s one pagination string set' % 'locales/en.default.json')
