# -*- coding: utf-8 -*-
"""Reorganise the GOD SQUAD project root into something navigable.

Thirty-three loose files at the root, including twenty phase documents, five
stray prototype images and the prototype's own entry HTML. This sorts them
without touching the theme and without deleting anything.

    GodSquad Website/
      god-squad-theme/     the deliverable, untouched
      preview-site/        double-click index.html to browse the design
      qa/                  the test suite, rescued from a temp directory
      docs/                the manual, the reviews, and phases/ beneath them
      brand-assets/        images, the Phase 3 asset set, the uploads
      prototype/           the original Claude Design export, read-only archive
      README.md            what each of those is and how to run things

WHAT IS NOT MOVED, AND WHY

  god-squad-theme/  is the product. Nothing inside it changes.
  .claude/          is tooling configuration and belongs at the root.

THE ONE DEPENDENCY THAT HAD TO BE HANDLED

  The QA harness builds its fixture pages by copying six images out of the
  project's images/ folder — four references to PROJECT/images in phase8 and
  phase9. Moving that folder silently breaks the harness build, which is exactly
  the sort of break that shows up three steps later as an unrelated-looking test
  failure. The copied suite is rewritten to locate the project from its own
  position on disk instead of hardcoding it, so the move is safe and the suite
  survives the project being moved again later.

Every move is verified afterwards: file counts in, file counts out, nothing
lost.
"""
import io
import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRS = ['preview-site', 'qa', 'docs', os.path.join('docs', 'phases'),
        'brand-assets', 'prototype']

# (pattern-or-name, destination relative to ROOT)
MOVES = [
    # --- the phase record ------------------------------------------------
    ('PHASE-0-PROJECT-FOUNDATION.md', 'docs/phases'),
    ('PHASE-1-WEBSITE-AUDIT.md', 'docs/phases'),
    ('PHASE-2-DESIGN-SYSTEM.md', 'docs/phases'),
    ('PHASE-2-DESIGN-TOKENS.css', 'docs/phases'),
    ('PHASE-3-ASSET-SYSTEM.md', 'docs/phases'),
    ('PHASE-3-ASSET-MANIFEST.csv', 'docs/phases'),
    ('PHASE-4-HEADER-NAVIGATION.md', 'docs/phases'),
    ('PHASE-5-HERO.md', 'docs/phases'),
    ('PHASE-6-COLLECTIONS-BEST-SELLERS.md', 'docs/phases'),
    ('PHASE-7-OUR-STORY.md', 'docs/phases'),
    ('PHASE-8-PRODUCT-SHOPPING-UX.md', 'docs/phases'),
    ('PHASE-9-MOBILE-RESPONSIVE.md', 'docs/phases'),
    ('PHASE-10-THEME-ARCHITECTURE.md', 'docs/phases'),
    ('PHASE-11-THEME-EDITOR.md', 'docs/phases'),
    ('PHASE-12-PRODUCT-COLLECTION-UX.md', 'docs/phases'),
    ('PHASE-13-SEARCH-FILTERING-DISCOVERY.md', 'docs/phases'),
    ('PHASE-14-CART-CHECKOUT-UX.md', 'docs/phases'),
    ('PHASE-15-CUSTOMER-ACCOUNT-POST-PURCHASE.md', 'docs/phases'),
    ('PHASE-16-PERFORMANCE-SEO-CONVERSION.md', 'docs/phases'),
    ('PHASE-17-ANALYTICS-TRACKING-MARKETING.md', 'docs/phases'),
    ('PHASE-18-FINAL-POLISH-REPORT.md', 'docs/phases'),
    ('PHASE-18-VISUAL-AUDIT.md', 'docs/phases'),

    # --- the current, working documents ----------------------------------
    ('GODSQUAD-THEME-REFERENCE-MANUAL.md', 'docs'),
    ('PRE-INTEGRATION-DESIGN-REVIEW.md', 'docs'),

    # --- the prototype, archived read-only -------------------------------
    ('God Squad Website.html', 'prototype'),
    ('support.js', 'prototype'),
    ('.thumbnail', 'prototype'),

    # --- stray brand images that were sitting at the root ----------------
    ('01-hero-model-mu98p88t-7jig.webp', 'brand-assets'),
    ('chatgpt-image-sep-20-2026-11_06_34-am-mu98j9xl-evm9.png', 'brand-assets'),
    ('white-font-300x300-mu98qi59-mytq.png', 'brand-assets'),
    ('white-font-trans-mu98q2ez-zrdd.png', 'brand-assets'),
    ('white-font-trans-mu98qky0-5tt6.png', 'brand-assets'),

    # --- whole folders ----------------------------------------------------
    ('images', 'brand-assets'),
    ('phase-3-assets', 'brand-assets'),
    ('uploads', 'brand-assets'),

    # --- the old entry point, superseded by preview-site ------------------
    ('TEST-INDEX.html', 'qa'),
]

if __name__ == '__main__':
    before = sum(1 for _r, _d, fs in os.walk(ROOT) for _f in fs)
    print('project has %d files before the move' % before)
    print()

    for d in DIRS:
        p = os.path.join(ROOT, d)
        if not os.path.isdir(p):
            os.makedirs(p)
            print('  created  %s/' % d.replace(os.sep, '/'))

    print()
    moved = skipped = 0
    for name, dest in MOVES:
        src = os.path.join(ROOT, name)
        dst_dir = os.path.join(ROOT, dest.replace('/', os.sep))
        dst = os.path.join(dst_dir, os.path.basename(name))
        if not os.path.exists(src):
            print('  --  %-52s not found' % name)
            skipped += 1
            continue
        if os.path.exists(dst):
            print('  --  %-52s already at %s' % (name, dest))
            skipped += 1
            continue
        shutil.move(src, dst)
        moved += 1
        print('  ->  %-52s %s/' % (name, dest))

    after = sum(1 for _r, _d, fs in os.walk(ROOT) for _f in fs)
    print()
    print('%d moved, %d skipped' % (moved, skipped))
    print('project has %d files after the move' % after)
    if after != before:
        print('*** FILE COUNT CHANGED BY %+d — INVESTIGATE ***' % (after - before))
    else:
        print('file count unchanged: nothing was lost.')

    print()
    print('root now holds:')
    for e in sorted(os.listdir(ROOT)):
        p = os.path.join(ROOT, e)
        if os.path.isdir(p):
            n = sum(1 for _r, _d, fs in os.walk(p) for _f in fs)
            print('  [dir]  %-22s %4d files' % (e + '/', n))
        else:
            print('  file   %-22s %4d bytes' % (e, os.path.getsize(p)))
