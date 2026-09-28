# -*- coding: utf-8 -*-
css = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\section-hero.css"
doc = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\PHASE-5-HERO.md"

c = open(css, encoding='utf-8').read()
def rc(a, b):
    global c
    assert a in c, "CSS NOT FOUND: " + a[:80]
    c = c.replace(a, b, 1)

rc("""  /* Content ends near 70% of the viewport at this width, so the hold has to
     reach further than it does on wider screens. Rendered and sampled with the
     hold at 50%, the darkest backdrop inside the heading's box measured 2.43:1
     against the 3:1 large-text minimum — a fail. At 66% the same pixel
     measures 9.48:1. This breakpoint is the one that needs the long hold: the
     same 50% test passes at 1280px (7.96:1) and 1440px (12.19:1). */""",
"""  /* The content column ends near 70% of the viewport at this width, so the
     hold has to reach further than it does on wider screens. What is protected
     here is the column, not today's copy: the shipped heading only reaches 48%
     and passes at any hold, but `heading` is a merchant field and a longer one
     fills the column. Rendered and sampled across the full column with the hold
     at 50%, the darkest backdrop in it carries cream at 2.43:1 and gold at
     1.57:1 — both fail the 3:1 large-text minimum. At 66% the same pixel gives
     9.48:1 and 6.12:1. 1024px is the only breakpoint that needs the long hold;
     the same 50% test passes at 1280px (7.96:1) and 1440px (12.19:1). */""")

rc("""   be. Measured worst backdrop inside the heading box after relaxing: 10.90:1
   at 1280px and 10.92:1 at 1440px, both far above the 3:1 minimum. */""",
"""   be. Measured across the full content column after relaxing: 10.90:1 at
   1280px and 10.92:1 at 1440px for cream, 7.05:1 and 7.06:1 for gold, all far
   above the 3:1 minimum. */""")

rc("clears it everywhere measured, worst case 8.08:1. Phase 5 section 10",
   "clears it everywhere measured, worst case 8.18:1. Phase 5 section 10")

open(css, 'w', encoding='utf-8', newline='').write(c)
print("section-hero.css comments corrected")

s = open(doc, encoding='utf-8').read()
def rd(a, b):
    global s
    assert a in s, "DOC NOT FOUND: " + a[:80]
    s = s.replace(a, b, 1)

rd("""This is not cosmetic tuning. Rendered with the hold fixed at 50% at every width,
the darkest backdrop inside the heading's box measures **2.43:1 at 1024px** —
below the 3:1 large-text minimum. At 66% the same pixel measures 9.48:1. 1024px
is the only breakpoint that needs the long hold; the same 50% test passes at
1280 (7.96:1) and 1440 (12.19:1). The 1280 and 1440 steps exist to *relax* the
wash and give the photograph back, not to fix contrast.""",
"""This is not cosmetic tuning, and what it protects is the **column**, not today's
copy. The shipped heading reaches only 48% of the viewport at 1024px and passes
at any hold — but `heading` is a merchant field, and a longer one fills the
column out to 70%. Sampled across the full column with the hold fixed at 50%:

| Width | Hold 50% (cream / gold) | Shipped hold (cream / gold) |
|---|---|---|
| 1024 | **2.43 / 1.57 — FAIL** | 66% → 9.48 / 6.12 — PASS |
| 1280 | 7.96 / 5.15 — PASS | 54% → 10.90 / 7.05 — PASS |
| 1440 | 12.19 / 7.88 — PASS | 48% → 10.92 / 7.06 — PASS |

1024px is the only breakpoint that needs the long hold. The 1280 and 1440 steps
exist to *relax* the wash and give the photograph back, not to fix contrast.""")

rd("text needing 3:1 and clears it everywhere measured (worst case 8.08:1).",
   "text needing 3:1 and clears it everywhere measured (worst case 8.18:1).")

rd("| **SC 1.4.3** Contrast (large text) | Heading PASS at all widths. Worst **8.08:1** (gold accent) against 3:1 |",
   "| **SC 1.4.3** Contrast (large text) | Heading PASS at all widths. Worst **8.18:1** (gold accent) against 3:1 |")

open(doc, 'w', encoding='utf-8', newline='').write(s)
print("PHASE-5-HERO.md corrected")
