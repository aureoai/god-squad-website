# -*- coding: utf-8 -*-
"""Correct the "the QA harness has no image files at all" claim.

It is false. Verified two ways today: loading home.html in a browser shows ten
<img> elements with real src values and non-zero naturalWidth, and listing the
harness directory shows six files — hero.webp 119,850 B, logo.png 47,147 B,
story.webp 41,004 B, hoodie.webp 12,328 B, cap.webp 10,002 B, tee.webp 9,012 B.
Both phase8/build.py and phase9/build.py copy them from the project's images/
folder at line 42 and 47.

The claim originated in PHASE-16 (lines 149 and 652) and propagated into both
Phase 18 documents and the consolidated manual. PHASE-16 is left alone: the
twenty phase documents are the historical record and rewriting them would
destroy the provenance the manual depends on. The documents written in THIS
session are corrected, and the manual carries a note that PHASE-16's version is
superseded.

What remains true, and is the point those passages were making: no MERCHANT
photography exists. The six images are the prototype's own AI-generated crops
with unconfirmed rights. So the harness shows approximate imagery, and what
genuinely cannot be assessed is how real merchant photography will crop, sit and
scale — not that there is nothing on screen at all.
"""
import io
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRUE_STATEMENT = (
    "Phase 3 recorded sourcing \u2014 not processing \u2014 as the ceiling, and no merchant "
    "photography exists. The QA harness renders six placeholder images copied from the "
    "prototype's own folder (`hero.webp`, `tee.webp`, `hoodie.webp`, `cap.webp`, "
    "`story.webp`, `logo.png`), which are AI-generated with unconfirmed rights \u2014 so the "
    "test pages show approximate imagery, not the real thing. The theme itself ships **zero** "
    "image files."
)

JOBS = [
    ('PHASE-18-FINAL-POLISH-REPORT.md',
     "**There is no merchant photography in this project.** Phase 3 recorded sourcing "
     "\u2014 not processing \u2014 as the ceiling, and the QA harness contains no image "
     "files at all.",
     "**There is no merchant photography in this project.** " + TRUE_STATEMENT),
    ('PHASE-18-VISUAL-AUDIT.md',
     "not processing \u2014 as the ceiling, and the QA harness has no image files at all.",
     "not processing \u2014 as the ceiling, and no merchant photography exists. The harness\n"
     "renders six placeholder images copied from the prototype's own folder, which are\n"
     "AI-generated with unconfirmed rights \u2014 approximate imagery, not the real thing.\n"
     "The theme itself ships zero image files."),
]

for rel, old, new in JOBS:
    p = os.path.join(ROOT, rel)
    s = io.open(p, encoding='utf-8').read()
    n = s.count(old)
    if n != 1:
        print('  *** %-34s %d match(es), expected 1 \u2014 SKIPPED' % (rel, n))
        continue
    io.open(p, 'w', encoding='utf-8').write(s.replace(old, new, 1))
    print('  ok  %s' % rel)

print()
print('Remaining occurrences of the false claim, by file:')
for rel in sorted(os.listdir(ROOT)):
    if not rel.endswith('.md'):
        continue
    s = io.open(os.path.join(ROOT, rel), encoding='utf-8', errors='replace').read()
    hits = (s.count('harness has no image files')
            + s.count('harness contains no image files')
            + s.count('harness ships **no image files'))
    if hits:
        note = '  <- historical record, deliberately not rewritten' \
            if rel.startswith('PHASE-16') else ''
        print('  %-44s %d%s' % (rel, hits, note))
