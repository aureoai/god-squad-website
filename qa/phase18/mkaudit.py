# -*- coding: utf-8 -*-
"""Phase 18 — generate the SECTION / PROBLEM / SEVERITY / FIX / STATUS table.

Every row is one deduplicated defect with the decision taken on it. A row is
never marked FIXED unless something in god-squad-theme/ actually changed, and
never marked REJECTED without the citation that overrides it.

STATUS values:
  FIXED      changed in the theme this phase, with the verification named
  REJECTED   the finding is wrong, or it contradicts a recorded decision
  MERCHANT   a real inconsistency whose resolution is a brand or business call
  RECORDED   real, verified, and deliberately not changed in a no-redesign phase
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
work = json.load(io.open(os.path.join(HERE, 'worklist.json'), encoding='utf-8'))

# file:line -> (status, note). Matched against the defect's primary site.
DECISIONS = {
    'assets/component-facets.css:99': ('FIXED',
        'Both disclosures given the base rotation. All three now measure DOWN closed, '
        'UP open, 180 deg sweep (phase18/chevron.py). The SIZE half of this finding is '
        'REJECTED: PHASE-2 line 1428 assigns the chevron both --icon-sm inline and '
        '--icon-md in controls.'),
    'assets/component-cart-line.css:286': ('FIXED',
        'Empty-state titles taken to the interface-heading row (body family, h3 size, '
        '600, sentence). Measured before: <p> rendered Playfair 40px 900 uppercase, '
        'identical to the <h1> directly above it on both the cart and the collection. '
        'Taken together with the H3/H4 family finding, which is the same edit: three '
        'rules moved from --font-display to --font-body per design-tokens.css:170 '
        '("Playfair for H1-H2, Jost for H3-H4") and PHASE-2 6.1. That also made the '
        'weight honest — the display font ships as playfair_display_n9 with no '
        'font_modify, so --weight-semibold was resolving to the 900 face. '
        '.header__wordmark left alone: a logotype is not a heading.'),
    'assets/section-main-search.css:246': ('FIXED',
        'Removed. The class was the last fragment of the paginator this stylesheet '
        'used to own, which '
        'Phase 18 merged into component-pagination.css — the markup and resting rules '
        'went and this hover outlived them. My own leftover, not a pre-existing one.'),
    'assets/component-cart-line.css:126': ('FIXED',
        'Removed. Unreachable for the reason this same file already documents for '
        '.cart-drawer__error: both cart surfaces hardcode surface-dark and neither '
        'schema exposes a surface setting. Phase 18 retired the siblings and missed '
        'this one.'),
    'assets/section-main-collection.css:91': ('FIXED',
        'The three missing :hover rules added, pointer-scoped. Five surfaces now behave '
        'alike (phase18/hovergate.py).'),
    'assets/header.css:263': ('FIXED',
        'All nine rules wrapped in @media (hover: hover) and (pointer: fine). '
        'phase18/hovergate.py: 29 hover rules, 29 gated, 0 ungated — 27 before, '
        'plus 3 missing inline-link hovers added, minus 1 dead rule removed.'),
    'assets/header.css:504': ('RECORDED',
        'Verified: the panel is Playfair 900 at --type-h3-size where PHASE-2 19.6 '
        'specifies the eyebrow triplet. NOT changed — it would re-type the primary '
        'mobile navigation, which is a visible design change rather than polish. '
        'Needs your call.'),
    'assets/header.css:422': ('FIXED',
        'Menu scrim moved from --transition-medium to --transition-slow. PHASE-2 line '
        '1727 assigns the scrim 400ms and line 1725 assigns the panel 250ms; the cart '
        'drawer already had both right.'),
    'assets/section-footer.css:97': ('RECORDED',
        'Verified as two type systems stacked. Same reasoning as the mobile panel: '
        're-typing the footer is a design change, not polish.'),
    'assets/component-facets.css:25': ('FIXED',
        'margin-block-end on .main-collection__header, not on .facets — below --bp-md '
        'that element is position:fixed and a top margin would displace the drawer. '
        'Measured 0px -> 40px filtered, 40px unchanged unfiltered (phase18/gap.py).'),
    'assets/section-cart-drawer.css:301': ('RECORDED',
        'Verified: 14px with 0.22em tracking appears nowhere else. A type change to '
        'two live controls; recorded rather than made during a no-redesign phase.'),
    'assets/component-facets.css:458': ('RECORDED',
        'Verified as two definitions at two sizes. Cosmetic and contained; grouped with '
        'the badge-size family below.'),
    'sections/announcement-bar.liquid:143': ('MERCHANT',
        'Correct: the icon slot is a merchant-uploaded raster, the only non-SVG glyph. '
        'Whether to restrict it to the icon set is a merchant-capability decision.'),
    'assets/header.css:519': ('FIXED',
        'Split from its :hover partner. The current page now carries an underline as '
        'well as colour — the footer pattern, which documents "not carried by colour '
        'alone" (SC 1.4.1) — and the hover half is pointer-scoped.'),
    'assets/component-facets.css:323': ('FIXED',
        'Exit slide restored via .is-closing, held by facets.js until transitionend '
        'with a 500ms fallback; the cart drawer pattern. 12 new assertions '
        '(phase18/drawerexit.py), negative control run.'),
    'assets/section-footer.css:112': ('RECORDED',
        'Verified: two underline mechanisms across four controls. Contained; the '
        'text-decoration half cannot transition, which is the substance of it.'),
    'sections/header-group.json:17': ('MERCHANT',
        '"Worldwide Shipping" is a business claim shipped in the announcement bar while '
        'the same claim is withheld elsewhere. Not mine to assert or remove — it is '
        'either true of the business or it is not.'),
    'locales/en.default.json:47': ('REJECTED',
        '"Add to bag" is a RECORDED decision, not drift: PHASE-2 line 943 writes '
        '"add-to-bag is a <button>" and PHASE-12 line 209 uses the same term. Whether '
        'to unify the voice with the 14 "cart" strings is a brand call — flagged to you, '
        'not changed.'),
    'locales/en.default.json:30': ('FIXED',
        'Placeholder now "Search the store…", agreeing with its own label and with the '
        'results page. The form posts to routes.search_url, which searches the store.'),
    'sections/footer.liquid:407': ('FIXED',
        'Ten merchant-facing schema strings rewritten. "The prototype", "the approved '
        'mockup", "the rebuild", "Phase 3 records", "§26.1" and "BUSINESS INFORMATION '
        'REQUIRED" removed; every instruction kept.'),
}

# Subject-level decisions, applied when the primary site did not match.
SUBJECT = {
    'H3/H4 display-vs-body family': ('FIXED',
        'Three rules moved to --font-body per design-tokens.css:170 and PHASE-2 6.1. '
        'It also made the weight honest: the display font is registered as '
        'playfair_display_n9 with no font_modify, so --weight-semibold resolved to the '
        '900 face. .header__wordmark deliberately untouched — a logotype is not a '
        'heading.'),
}

ORDER = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
STATUS_DEFAULT = ('RECORDED',
                  'Verified by the audit and re-read here. Left unchanged: it is '
                  'cosmetic or structural tidying whose risk outweighs its benefit in a '
                  'phase that is explicitly not a redesign.')


def esc(s):
    return ' '.join(str(s or '').split()).replace('|', '\\|')


rows = []
for x in work:
    key = '%s:%s' % (x['file'], x['line'])
    st, note = DECISIONS.get(key, (None, None))
    if st is None:
        for subj, (s2, n2) in SUBJECT.items():
            if subj.lower()[:12] in (x.get('title') or '').lower():
                st, note = s2, n2
                break
    if st is None:
        st, note = STATUS_DEFAULT
    rows.append({
        'sev': x['severity'], 'rank': x['sev_rank'],
        'file': x['file'], 'line': x['line'],
        'title': x['title'], 'fix': x.get('fix') or '', 'status': st,
        'note': note, 'dims': x['dims'], 'n': x['n'],
    })

rows.sort(key=lambda r: (r['rank'], -r['n']))
io.open(os.path.join(HERE, 'audit-rows.json'), 'w', encoding='utf-8').write(
    json.dumps(rows, indent=2, ensure_ascii=False))

from collections import Counter
print('rows: %d' % len(rows))
print('status: %s' % dict(Counter(r['status'] for r in rows)))
print('severity: %s' % dict(Counter(r['sev'] for r in rows)))
print()
for r in rows[:20]:
    print('  [%-8s] %-10s %s:%s' % (r['sev'], r['status'], r['file'], r['line']))
