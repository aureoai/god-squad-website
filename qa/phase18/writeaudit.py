# -*- coding: utf-8 -*-
"""Phase 18 — write PHASE-18-VISUAL-AUDIT.md from the triaged rows."""
import io
import json
import os
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
rows = json.load(io.open(os.path.join(HERE, 'audit-rows.json'), encoding='utf-8'))


def esc(s):
    return ' '.join(str(s or '').split()).replace('|', '\\|')


# Map a file to the surface a reader thinks in.
def section_of(f):
    f = f.lower()
    for key, name in [
        ('header', 'Header / navigation'), ('announcement', 'Header / navigation'),
        ('footer', 'Footer'),
        ('facets', 'Search & filtering'), ('main-search', 'Search & filtering'),
        ('pagination', 'Search & filtering'),
        ('cart', 'Cart & checkout'),
        ('product-card', 'Product card / grid'), ('product-media', 'Product page'),
        ('product-variant', 'Product page'), ('main-product', 'Product page'),
        ('main-collection', 'Collection page'),
        ('our-story', 'Our Story'), ('hero', 'Hero'),
        ('main-page', 'Page template'), ('main-404', '404'),
        ('settings_schema', 'Theme settings'), ('locales', 'Copy & voice'),
        ('header-group', 'Header / navigation'), ('icon-', 'Icon system'),
        ('theme.liquid', 'Layout'),
    ]:
        if key in f:
            return name
    return 'Theme-wide'


STATUS_BLURB = {
    'FIXED': 'changed in the theme this phase; the verification is named',
    'RECORDED': 'verified and deliberately left alone — see the note',
    'MERCHANT': 'real, but the resolution is a business or brand decision',
    'REJECTED': 'the finding does not stand, and the citation that overrides it is given',
}

by_status = Counter(r['status'] for r in rows)
by_sev = Counter(r['sev'] for r in rows)

out = []
w = out.append

w('# PHASE 18 — VISUAL AUDIT')
w('')
w('**GOD SQUAD — Shopify Online Store 2.0 theme**  ')
w('**Date:** 2026-09-25  ')
w('**Scope:** final polish and award-level UI/UX QA. Not a redesign.')
w('')
w('---')
w('')
w('## How this audit was produced')
w('')
w('Two independent passes, deliberately different in kind.')
w('')
w('**Pass 1 — measured.** Harnesses render the real `.liquid` files against mock')
w('Shopify data and read computed styles out of a browser. This is what produced the')
w('design-coherence table, the leading measurements, the chevron angles and the')
w('spacing figures quoted below. A measurement is quoted only where one was taken.')
w('')
w('**Pass 2 — reviewed.** Fourteen agents across seven dimensions (typography,')
w('spacing, buttons, icons, legacy code, motion and states, copy and brand). Each')
w('dimension was audited by one agent and every finding adversarially verified by a')
w('second. They returned **98 confirmed findings**, which deduplicate to **%d distinct'
  % len(rows))
w('defects** — one defect can arrive four times wearing four labels, and the chevron')
w('below arrived seven times.')
w('')
w('**Every finding in this table was then re-checked by hand before any action was')
w('taken.** That mattered: two well-argued, "CONFIRMED" findings did not survive')
w('contact with the specification, and are marked REJECTED with the citation.')
w('')
w('### What this audit could NOT assess')
w('')
w('There is **no merchant photography in this project.** Phase 3 recorded sourcing —')
w('not processing — as the ceiling, and the QA harness has no image files at all.')
w('Image cropping, focal points, image quality, art direction and the visual rhythm')
w('of real photography against real copy are the core of a visual audit, and none of')
w('them is assessable here. Everything below audits the *reservation* — the box the')
w('picture goes in — never the picture. Any claim to have reviewed the imagery would')
w('be invented.')
w('')
w('---')
w('')
w('## Summary')
w('')
w('| Status | Count | Meaning |')
w('|---|---:|---|')
for st in ('FIXED', 'RECORDED', 'MERCHANT', 'REJECTED'):
    w('| **%s** | %d | %s |' % (st, by_status.get(st, 0), STATUS_BLURB[st]))
w('| | **%d** | |' % len(rows))
w('')
w('| Severity | Count |')
w('|---|---:|')
for s in ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW'):
    w('| %s | %d |' % (s, by_sev.get(s, 0)))
w('')
w('Severity is the *reviewers\'* rating, kept as returned so the table is not quietly')
w('re-scored after the fact. My own decision on each is the STATUS column.')
w('')
w('---')
w('')
w('## The table')
w('')
w('Ordered by severity, then by how many independent dimensions found it. `SECTION`')
w('is the surface a reader thinks in; `PROBLEM` is the defect; `RECOMMENDED FIX` is')
w('the action; `STATUS` is what was actually done and why.')
w('')

groups = defaultdict(list)
for r in rows:
    groups[section_of(r['file'])].append(r)

n = 0
w('| # | SECTION | PROBLEM | SEVERITY | RECOMMENDED FIX | STATUS |')
w('|---:|---|---|---|---|---|')
for r in rows:
    n += 1
    corro = (' *(found by %d dimensions: %s)*' % (r['n'], ', '.join(r['dims']))
             if r['n'] > 1 else '')
    fix = esc(r['fix'])[:420] or '—'
    w('| %d | %s | %s%s | %s | %s | **%s** — %s |'
      % (n, section_of(r['file']),
         esc(r['title'])[:330], corro, r['sev'], fix,
         r['status'], esc(r['note'])[:520]))
w('')
w('*File references for every row are in `scratchpad/phase18/worklist.json`, with the')
w('full verifier reasoning for each.*')
w('')
w('---')
w('')
w('## Found by measurement, not by the review')
w('')
w('These came out of the harnesses rather than the audit, and are Phase 18 work of')
w('the same kind. They are listed separately because nothing in the table above')
w('covers them.')
w('')
w('| # | SECTION | PROBLEM | SEVERITY | RECOMMENDED FIX | STATUS |')
w('|---:|---|---|---|---|---|')
w('| M1 | Cart & checkout | `.cart-line__title` carried every part of the label role '
  'except leading, so a wrapped product name fell back to `line-height: normal`. For '
  'Jost that resolves to 1.167 against the 1.45 the same name gets on a product card '
  '— 14.0px versus 17.4px per line. | HIGH | Add the missing `--type-label-lh` token '
  'and apply it to the two label consumers whose text wraps. | **FIXED** — measured '
  'at 375px, where the current fixture title already wraps to two lines, so this was '
  'live on phones. Token added to `design-tokens.css`; `--product-title-lh` now '
  'points at it. The 22 single-line label consumers are untouched: `normal` and 1.45 '
  'render identically on one line. |')
w('| M2 | Search & filtering | The paginator was built twice — once for collection, '
  'once for search — under two class systems in two stylesheets, and the two had '
  'already drifted: caption type versus tracked uppercase, a weight-and-rule current '
  'marker versus a gold one. | HIGH | Merge into one snippet and one component '
  'stylesheet, taking the better half of each. | **FIXED** — `section-main-collection.'
  'css` named its own promotion trigger in writing and the trigger had been met since '
  'Phase 13. Type and current-page marker from collection, accessibility from search. '
  'Also fixed a Phase 16 finding in passing: collection\'s gap `<li>` was announced as '
  'a blank list entry. |')
w('| M3 | Theme-wide | `.container` was specified in PHASE-2 §8 and never built, so '
  'twelve elements across eleven stylesheets each carried a private copy of the same '
  'four declarations — the width of the site defined twelve times. | MEDIUM | Build '
  'the utility and sweep the copies. | **FIXED** — all twelve verified byte-identical '
  'with no breakpoint overrides first. Geometry re-measured pixel-identical after: '
  'homepage 2/156/16px at 375 and 3/297/32px at 1440, collection 4/312/32px at 1440, '
  'matching Phase 13. Three narrow-width rules deliberately NOT swept in; the reason '
  'is recorded in the component file. |')
w('| M4 | Product card / grid | `.product-card__error` was defined twice at equal '
  'specificity. Later-wins-per-property left it taking padding and line-height from '
  'the cart grouping and everything else from its own rule — so it rendered boxed, '
  'the exact treatment the comment above it says it is not. | MEDIUM | Take the card '
  'out of the cart grouping. | **FIXED** — the two are legitimately different objects: '
  'a failure inside a 300px tile and a failure across a cart panel. Three unreachable '
  '`.surface-light` selectors removed with it. |')
w('')
w('---')
w('')
w('## The two findings that were rejected, and why')
w('')
w('Both were returned CONFIRMED by a verifier with evidence attached. Both are wrong,')
w('and both would have made the theme worse.')
w('')
w('**1. "Three disclosure chevrons render at two sizes — 24px on the product page,')
w('16px in the cart note and filter groups."** Rated HIGH. The sizes do differ. But')
w('`PHASE-2-DESIGN-SYSTEM.md` line 1428 assigns the chevron *both*: "`--icon-sm` 16px')
w('inline; `--icon-md` in controls". A 24px glyph beside a 12px filter label would be')
w('the defect. **Only the direction half of this finding was acted on.**')
w('')
w('**2. "\'Add to bag\' is the only \'bag\' string in a purchase flow whose every other')
w('string says \'cart\'."** Rated HIGH, and factually correct — 14 "cart" strings')
w('against it. But it is a *decided* term, not drift: `PHASE-2` line 943 writes')
w('"add-to-bag is a `<button>` even though the prototype\'s CTAs are anchors", and')
w('`PHASE-12` line 209 reads \'the enabled "Add to bag" button already says it\'. The')
w('action is "add to bag" and the container is the "cart" by choice. Unifying the')
w('brand voice is **your** call, not a silent fix. See Decisions Required.')
w('')

io.open(os.path.join(ROOT, 'PHASE-18-VISUAL-AUDIT.md'), 'w', encoding='utf-8').write(
    '\n'.join(out) + '\n')
print('PHASE-18-VISUAL-AUDIT.md written: %d rows, %d lines' % (len(rows), len(out)))
