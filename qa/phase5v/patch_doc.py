# -*- coding: utf-8 -*-
p = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\PHASE-5-HERO.md"
s = open(p, encoding='utf-8').read()

def rep(a, b):
    global s
    assert a in s, "NOT FOUND: " + a[:90]
    s = s.replace(a, b, 1)

# --- 2. Content hierarchy: the accent is now its own line
rep(
'        ├── h1.hero__heading         "Walk By" + span.hero__heading-accent "Faith."\n',
'        ├── h1.hero__heading         "Walk By"\n'
'        │                             └── span.hero__heading-accent "Faith."  (display:block)\n')

rep(
"""- **One `<h1>`, always.** The accent is a `<span>` inside the same heading, not a
  second heading, so the approved two-tone lockup survives without two headings
  competing. Validated automatically: `exactly one <h1>` is a check in the
  Phase 5 validator.""",
"""- **One `<h1>`, always.** The accent is a `<span>` inside the same heading, not a
  second heading, so the approved two-tone lockup survives without two headings
  competing. Validated automatically: `exactly one <h1>` is a check in the
  Phase 5 validator. The span is `display: block`, which is what makes the
  two-line lockup structural rather than a wrapping accident — see §6 and
  HERO-03 in §12.""")

# --- 6. Typography: the lockup
rep(
"""The heading scales fluidly between 56px and 112px. It is capped at 112px: past
1440 the section gets taller but the type does not keep growing, because at 1920
a larger heading would start to compete with the photograph rather than sit in
it.""",
"""The heading scales fluidly between 56px and 112px. It is capped at 112px: past
1440 the section gets taller but the type does not keep growing, because at 1920
a larger heading would start to compete with the photograph rather than sit in
it.

**The lockup is two lines at every width the column can hold the first phrase.**
`.hero__heading-accent` is `display: block`, so the break before the gold word
is structural, not a wrapping outcome. Measured line counts:

| 320 | 375 | 390 | 430 | 768 | 900 | 1024 | 1280 | 1366 | 1440 | 1920 |
|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |

Only 320px breaks it, and it has to: WALK BY at 56px is about 258px wide and the
content column there is 272px, so the browser wraps inside it. That is the right
outcome at a width where the alternative is horizontal scrolling.

`text-wrap: balance` is still on the heading, but it now only governs how a
longer merchant-entered heading wraps. The approved lockup no longer depends on
it, which is what HERO-03 asked for.""")

# --- 12. The Phase 1 hero register
rep(
"""**Phase 1 findings answered.** The hero contributed three issues to the Phase 1
matrix: text over photography with no measured contrast; a call to action
pointing at `#`; and a heading split across two `<span>`s with hard-coded
colours. All three are closed by construction rather than by styling.""",
"""### The eight Phase 1 hero issues

`PHASE-1-WEBSITE-AUDIT.md` opened eight issues in the HERO register and assigned
every one of them to **PHASE 5 — HERO**. Their status after this phase:

| ID | Pri | Issue | Status |
|---|---|---|---|
| **HERO-01** | P1 / HIGH | The hero contains no link or button; on 1366x768 and 1280x720 the first screen is the hero alone | **MECHANISM BUILT, BLOCKED.** The CTA is built, styled and measured. Rendered with a link supplied, its bottom edge sits at y=649 on a 1280x720 laptop and y=655 on 1366x768 — inside the fold at every viewport tested. It does not render today because no collection URL exists (§7). Closing this needs one field, not one commit. |
| **HERO-02** | P1 / HIGH | Nav links sit on open sky; the scrim thins from .55 to 0 by 30% of the hero height | **CLOSED in Phase 4.** The header moved into the header group with a mandatory scrim holding about 0.86 alpha plus a 4rem overhang. Worst nav pixel re-measured at 13.61:1, against 2.4:1 in the prototype. |
| **HERO-03** | P2 / MEDIUM | The h1 stacks WALK / BY / FAITH. at 1024 and above and collapses to one line at 768-900; the signature lockup is never seen on a desktop | **CLOSED.** `.hero__heading-accent` is `display: block`. Measured two lines at 375, 390, 430, 768, 900, 1024, 1280, 1366, 1440 and 1920; three only at 320. |
| **HERO-04** | P2 / MEDIUM | Six copy elements with no priority rule; 563px of text under a 320px image, hero 970px tall at 375 | **CLOSED.** Four copy elements, ranked in DOM order, with the two side-column blocks not reproduced. Measured hero height at 375: **517px**, against 970px in the prototype. |
| **HERO-05** | P1 / MEDIUM | The three-model group photo was substituted for the mockup's single model; the direction is unconfirmed | **OPEN — BUSINESS INFORMATION REQUIRED.** Nothing in this phase can close it. The build uses the group photo, as the owner chose, and the Theme Editor help text carries the provenance warning. |
| **HERO-06** | P3 / LOW | The photo begins directly beneath the announcement bar with sky and tower tops, giving a hard horizontal seam | **CLOSED.** The header scrim now holds at the top of the hero and dissolves downward. Sampled at every x across the full boundary, the worst luminance step is **0.0066** at 1440 and 1920 and 0.0053 at 375 — below the threshold of perception. The only visible line is the announcement bar's own 1px hairline border, which is intentional. |
| **HERO-07** | P3 / LOW | More Than Clothing. and A Higher Purpose. sit over the right model's back print at 1024-1440 | **CLOSED BY REMOVAL.** The side column is not part of this section, so the collision cannot occur. The copy is unplaced rather than deleted — §16. |
| **HERO-08** | P3 / LOW | No portrait source for phones; the 375x320 band crops 96px from each side | **MECHANISM BUILT, BLOCKED.** A `<picture>` with a `(max-width: 749px)` source and a five-rung srcset is in place, and the focal point is now a setting with measured defaults. The portrait master does not exist — §15. |

Five closed here, one closed in Phase 4, two blocked on an asset or a business
decision this phase is forbidden to invent.""")

# --- 14. contrast table, re-measured after the lockup change
rep(
"""| 375 | 11.99 / 11.98 | 12.99 / 12.64 | 8.94 / 8.50 | 13.86 / 13.68 | 12.71 / 12.67 |
| 390 | 11.98 / 11.98 | 12.96 / 12.63 | 8.84 / 8.84 | 13.81 / 13.81 | 12.81 / 12.66 |
| 430 | 12.53 / 12.15 | 12.96 / 12.51 | 9.06 / 8.82 | 14.02 / 14.02 | 12.77 / 12.54 |
| 768 | 12.61 / 12.61 | 12.96 / 12.95 | 8.19 / 8.08 | 13.98 / 13.97 | 12.75 / 12.67 |
| 1024 | 14.14 / 13.94 | 13.80 / 9.48 | 9.03 / 8.94 | 16.67 / 16.67 | 13.22 / 12.21 |
| 1280 | 14.01 / 13.77 | 13.46 / 10.90 | 8.61 / 8.61 | 16.58 / 16.57 | 13.25 / 13.08 |
| 1440 | 13.84 / 13.67 | 12.46 / 10.92 | 8.53 / 8.53 | 16.58 / 16.54 | 15.08 / 13.39 |
| 1920 | 13.63 / 13.60 | 12.91 / 10.80 | 8.61 / 8.50 | 14.09 / 13.97 | 14.36 / 13.89 |""",
"""| 375 | 11.99 / 11.98 | 12.99 / 12.97 | 8.94 / 8.72 | 13.86 / 13.68 | 12.71 / 12.67 |
| 390 | 11.98 / 11.98 | 12.96 / 12.96 | 8.84 / 8.84 | 13.81 / 13.81 | 12.81 / 12.66 |
| 430 | 12.53 / 12.15 | 12.96 / 12.79 | 9.06 / 8.84 | 14.02 / 14.02 | 12.77 / 12.54 |
| 768 | 12.40 / 12.28 | 12.78 / 12.61 | 8.61 / 8.51 | 15.70 / 15.70 | 12.91 / 12.67 |
| 1024 | 14.14 / 13.94 | 13.80 / 13.63 | 9.05 / 8.21 | 16.67 / 16.67 | 13.22 / 12.21 |
| 1280 | 14.01 / 13.77 | 13.33 / 12.34 | 8.81 / 8.18 | 16.58 / 16.57 | 13.25 / 13.08 |
| 1440 | 13.84 / 13.67 | 12.46 / 12.16 | 8.53 / 8.53 | 16.58 / 16.54 | 15.08 / 13.39 |
| 1920 | 13.63 / 13.60 | 12.91 / 12.16 | 8.70 / 8.50 | 14.09 / 13.97 | 14.36 / 13.89 |""")

rep(
"""**40 measurements, 40 passes, on both metrics.** The lowest absolute figure
anywhere is the gold accent at 768px, 8.08:1 against a 3:1 requirement. The
narrowest margin relative to its own requirement is the eyebrow at 375–390px:
11.98:1 against 4.5:1, or 2.7× the minimum.""",
"""**40 measurements, 40 passes, on both metrics.** The lowest absolute figure
anywhere is the gold accent at 1280px, 8.18:1 against a 3:1 requirement. The
narrowest margin relative to its own requirement is the eyebrow at 375-390px:
11.98:1 against 4.5:1, or 2.7x the minimum. Every figure in this table was
re-measured after the HERO-03 lockup change; none of them is carried over.""")

rep("| Medium *(default)* | 11.98 | 12.64 | 13.67 | 10.92 | **PASS** |",
    "| Medium *(default)* | 11.98 | 12.97 | 13.67 | 12.16 | **PASS** |")

# --- 13. sizes
rep("| `assets/section-hero.css` | 14,040 B | 4,495 B | 6,911 B / 1,570 B gzip once comments are stripped |",
    "| `assets/section-hero.css` | 14,704 B | 4,792 B | 6,929 B / 1,571 B gzip once comments are stripped |")
rep("reduces it to **1,570 bytes gzipped**.", "reduces it to **1,571 bytes gzipped**.")

rep("| 768 | Single-line heading, announcement bar goes horizontal, header height still 88px |",
    "| 768 | Two-line lockup — the width at which the prototype lost it — announcement bar goes horizontal, header height still 88px |")

# --- 10 / file change report sizes
rep("""sections/hero.liquid        12,145 B   the section, its schema, one preset
assets/section-hero.css     14,040 B   all of the styling""",
"""sections/hero.liquid        12,145 B   the section, its schema, one preset
assets/section-hero.css     14,704 B   all of the styling""")
rep("| `assets/section-hero.css` | 14,040 |", "| `assets/section-hero.css` | 14,704 |")
rep("assets/section-hero.css              14,040 B     ← new", "assets/section-hero.css              14,704 B     ← new")
rep("TOTAL                                96,133 B     18 files", "TOTAL                                96,797 B     18 files")

open(p, 'w', encoding='utf-8', newline='').write(s)
print("document updated")
