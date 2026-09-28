# -*- coding: utf-8 -*-
"""Phase 18 - the search placeholder described the wrong scope.

The field posts to routes.search_url, which searches the whole store. Its own
accessible label says "Search the store" and sections.search.prompt says "search
the store". Only the placeholder said "Search the collection", which is the one
string a customer reads before deciding what to type.

NOT changed: "Add to bag". The audit called it an inconsistency against fourteen
"cart" strings, and it is one - but it is a DECIDED one. PHASE-2-DESIGN-SYSTEM
line 943 writes "add-to-bag is a <button> even though the prototype's CTAs are
anchors" and PHASE-12 line 209 reads 'the enabled "Add to bag" button already
says it'. Two specs use the term, so the action is "add to bag" and the
container is the "cart" by choice. Whether to unify the brand voice is the
merchant's call, and it is recorded in PHASE-18-VISUAL-AUDIT.md rather than
settled here.
"""
import io
import json
import os
import sys
from collections import OrderedDict

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
LOC = os.path.join(
    r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\god-squad-theme",
    'locales', 'en.default.json')

loc = json.load(io.open(LOC, encoding='utf-8'), object_pairs_hook=OrderedDict)
old = loc['header']['search_placeholder']
new = 'Search the store' + u'\u2026'
if old == new:
    print('  already correct')
else:
    loc['header']['search_placeholder'] = new
    io.open(LOC, 'w', encoding='utf-8').write(
        json.dumps(loc, indent=2, ensure_ascii=False) + '\n')
    print('  header.search_placeholder  %r -> %r' % (old, new))
    print('  now agrees with header.search_label %r' % loc['header']['search_label'])
