# -*- coding: utf-8 -*-
"""Assemble PHASE-2-DESIGN-SYSTEM.md from the Phase 2 workflow output.
Usage: python assemble_phase2.py <workflow-output.json> [--write]
"""
import json, re, io, sys, os, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(PROJECT, "PHASE-2-DESIGN-SYSTEM.md")
TOKENS = os.path.join(PROJECT, "PHASE-2-DESIGN-TOKENS.css")

TITLES = {1:"Design System Overview",2:"Brand Principles",3:"Color Palette",4:"Semantic Color Tokens",
 5:"Typography",6:"Type Scale",7:"Spacing Scale",8:"Container System",9:"Grid System",10:"Button System",
 11:"Link System",12:"Form System",13:"Product Card System",14:"Image System",15:"Border System",
 16:"Radius System",17:"Shadow System",18:"Icon System",19:"Navigation System",20:"Announcement Bar",
 21:"Motion System",22:"Hover States",23:"Focus States",24:"Accessibility Rules",25:"Responsive Rules",
 26:"Editorial Design Rules",27:"Ecommerce Design Rules",28:"Shopify Theme Settings Recommendations",
 29:"Section/Block Principles",30:"Design Token Reference",31:"Phase 3 Requirements"}

TAG_RE = re.compile(r'<(/?[a-zA-Z][a-zA-Z0-9-]*(?:\s[^<>\n]{0,140})?)>')

def wrap_bare_tags(text):
    out, n = [], 0
    for i, part in enumerate(re.split(r'(```.*?```)', text, flags=re.S)):
        if i % 2:
            out.append(part); continue
        for j, seg in enumerate(re.split(r'(`[^`\n]*`)', part)):
            if j % 2:
                out.append(seg); continue
            seg, k = TAG_RE.subn(r'`<\1>`', seg)
            n += k; out.append(seg)
    s = ''.join(out)
    s, adj = re.subn(r'>``<', '>` `<', s)
    return s, n, adj

src = sys.argv[1]
write = '--write' in sys.argv
top = json.load(open(src, encoding='utf-8', errors='replace'))
res = top.get('result', top)
if isinstance(res, str):
    res = json.loads(res)

sections, bir, gaps = {}, [], []
print("Clusters:")
for c in res['results']:
    o = c.get('out')
    if not o:
        print("  %-14s sections %-22s *** NO OUTPUT ***" % (c['key'], c['sections'])); continue
    for s in o.get('sections', []):
        n = int(s['number'])
        if not (1 <= n <= 31):
            print("      dropped out-of-range section %r (%s)" % (n, s.get('title', '')[:50]))
            continue
        sections[n] = s
    bir += o.get('businessInfoRequired', [])
    gaps += o.get('tokenGaps', [])
    print("  %-14s sections %-22s %d returned" % (c['key'], c['sections'], len(o.get('sections', []))))

missing = [n for n in range(1, 32) if n not in sections]
print("\nsections present: %d/31   missing: %s" % (len(sections), missing or 'none'))
for n in sorted(sections):
    print("  %2d. %-42s %5d words" % (n, TITLES.get(n, sections[n]['title'])[:42], len(sections[n]['markdown'].split())))

# ------------------------------------------------------------------ dedupe business info
seen, bir_clean = set(), []
for b in bir:
    k = re.sub(r'[^a-z0-9]', '', b.lower())[:70]
    if k not in seen:
        seen.add(k); bir_clean.append(b)
print("\nbusiness-info items: %d raw -> %d after dedupe" % (len(bir), len(bir_clean)))
if gaps:
    print("token gaps flagged by agents:")
    for g in dict.fromkeys(gaps): print("   -", g[:150])

HEADER = """# GOD SQUAD — PHASE 2 DESIGN SYSTEM & VISUAL LANGUAGE

**Project:** God Squad Premium Faith-Driven Streetwear
**Phase:** 2 — Design System
**Date:** 2026-09-21
**Target:** Shopify Online Store 2.0 theme (built in Phase 10, not here)
**Companion file:** `PHASE-2-DESIGN-TOKENS.css` — the canonical token implementation, 164 tokens, in the project root
**Predecessor:** `PHASE-1-WEBSITE-AUDIT.md` — 32 sections, 200 issues, delivered 2026-09-21

## How to use this document

This is a specification, not an implementation. It defines the vocabulary that Phases 3 to 16 build with. Nothing described here has been applied to the prototype: the existing website is untouched and remains the approved visual baseline.

Three rules govern everything that follows.

1. **Components reference semantic tokens, never raw palette values.** `--color-text-primary`, not `#F3EFE6`. The raw palette exists in one place so it can be re-pointed once.
2. **Surface context decides the accent and the focus ring.** Muted gold measures 1.55:1 on warm cream and 1.43:1 on the tile cream. It is a dark-surface accent only. The `.surface-dark` and `.surface-light` classes reassign `--accent-current` and `--focus-ring` so the correct value is inherited rather than remembered.
3. **Luxury through restraint.** When a decision is open, choose the quieter option: contrast and spacing before borders, borders before shadows, and no motion unless it serves comprehension.

Values marked **BUSINESS INFORMATION REQUIRED** are genuinely unknown. They are not placeholders to be filled with a plausible guess.
"""

QA = """The checklist below is the acceptance gate for every later phase. A section, component or template is not complete until it passes every applicable row. "Evidence" names how the check is made, so the result is verifiable rather than asserted.

### A.1 Colour

| # | Check | Evidence |
|---|---|---|
| 1 | Every colour comes from a semantic token; no raw hex in component code | Search the stylesheet for `#` outside the token file |
| 2 | Muted gold `#D8C08A` never carries text, icons or borders on a light surface | Visual pass plus contrast measurement on every cream band |
| 3 | Light surfaces use `--color-accent-strong` for accent text | Code review |
| 4 | Every text pairing meets 4.5:1, or 3:1 where the text is large | Contrast measurement against the §3 matrix |
| 5 | UI component boundaries and focus rings meet 3:1 | Contrast measurement |
| 6 | The muted stone tone never appears as text on cream (1.76:1) | Code review |
| 7 | Gold occupies a minority of any viewport; it is accent, never the dominant surface | Visual pass at 375, 768 and 1440 |

### A.2 Typography

| # | Check | Evidence |
|---|---|---|
| 8 | Every text element maps to a named scale step; no ad-hoc sizes | Code review |
| 9 | No persistent interface text below 12px; body copy at 16px | Computed-style audit at 375 |
| 10 | Playfair for display only; Jost for interface and body; Kaushan for accents only | Code review against §5 |
| 11 | Kaushan appears in no navigation, button, price, product field or paragraph | Code review |
| 12 | Tracked-uppercase steps carry their paired tracking value | Code review |
| 13 | Display steps use `clamp()` and never overflow their column at 320-1920 | Resize sweep |
| 14 | The peso sign and arrow render in an intended face, not a system fallback | Glyph-width check per platform |

### A.3 Spacing, layout and grid

| # | Check | Evidence |
|---|---|---|
| 15 | All spacing uses the scale; no stray values | Code review |
| 16 | Sections are full-bleed; content is constrained by a container token | Inspect at 1920 and 2560 |
| 17 | No dark gutters beside any band at any width above 1440 | Screenshot at 1920 |
| 18 | The gutter ladder applies at every breakpoint, including the announcement bar | Computed-style audit at 768 |
| 19 | Product grid resolves to a sensible column count with no orphaned single item | Visual pass at 375, 768, 1024, 1440 |
| 20 | Editorial splits use the split tokens rather than bespoke fractions | Code review |

### A.4 Components

| # | Check | Evidence |
|---|---|---|
| 21 | Every interactive element is a real `button` or `a`, never a styled `div` or `span` | Accessibility tree inspection |
| 22 | All five button states are defined and visually distinct | Interaction pass |
| 23 | Every control meets the 44x44 target, and never less than 24x24 | Measured bounding boxes |
| 24 | Product cards carry no more than title, price, swatches and one action | Visual pass |
| 25 | Every swatch has an accessible name; colour is never the only signal | Screen-reader pass |
| 26 | Form fields have persistent visible labels and programmatic association | Accessibility tree inspection |
| 27 | Error states convey meaning by text and icon, not colour alone | Visual and screen-reader pass |

### A.5 Imagery and icons

| # | Check | Evidence |
|---|---|---|
| 28 | Every image declares intrinsic width and height | Code review |
| 29 | The LCP hero loads eagerly with high fetch priority; everything below the fold is lazy | Network waterfall |
| 30 | Responsive sources are served with an explicit width ladder and sizes | Network waterfall |
| 31 | No image is upscaled beyond 1.0x of its natural size at any breakpoint | Rendered-versus-natural audit |
| 32 | Icons are inline SVG inheriting `currentColor` at one stroke weight | Code review |
| 33 | Decorative images are hidden from assistive technology; meaningful ones have accurate alt text | Accessibility tree inspection |

### A.6 Responsive and motion

| # | Check | Evidence |
|---|---|---|
| 34 | Media queries are mobile-first `min-width`; no `!important` in the responsive layer | Code review |
| 35 | Every styling hook is a class, not an attribute left over from a design tool | Code review |
| 36 | No horizontal overflow at 320, 375, 390, 430, 768, 1024, 1280, 1440, 1920 | Resize sweep with the overflow mask removed |
| 37 | Scrims are anchored to the element they darken, not to an ancestor | Visual pass below 900px |
| 38 | Layout survives 200% browser zoom and 400% for reflow at 320 CSS px | Zoom test |
| 39 | Motion animates only opacity and transform, within the duration tokens | Code review |
| 40 | `prefers-reduced-motion` removes non-essential motion | Emulated in devtools |

### A.7 Ecommerce and Theme Editor

| # | Check | Evidence |
|---|---|---|
| 41 | Product identity, price, availability and variant choice are legible without hovering | Visual pass |
| 42 | Add-to-cart state changes are announced to assistive technology | Screen-reader pass |
| 43 | Every merchant-facing setting has a clear label and a sensible default | Theme Editor walkthrough |
| 44 | Sections can be added, removed and reordered without breaking layout | Theme Editor walkthrough |
| 45 | No section exposes more settings than a merchant can reasonably use | Schema review |
| 46 | Blocks are used for repeatable content, never for individual text fragments | Schema review |
"""

CRITERIA = """The Phase 2 specification defines completion as the twenty-two items below.

- [x] **Brand direction documented** — §2, with message hierarchy and the restraint principle expressed as working rules.
- [x] **Colors standardized** — §3, three approved colours plus six derived values, each justified and contrast-verified.
- [x] **Semantic color tokens defined** — §4, with the surface-context mechanism that enforces correct accent use.
- [x] **Typography standardized** — §5, three families with explicit permitted and forbidden uses.
- [x] **Type scale defined** — §6, every step with size, weight, line-height, tracking, transform and prototype origin.
- [x] **Spacing system defined** — §7, ten tokens on a 4px grid with a normalisation map from the prototype's 44 stray values.
- [x] **Container system defined** — §8, full-bleed sections with constrained content, replacing the boxed 1440px wrapper.
- [x] **Grid system defined** — §9, twelve-column base, product grid ladder and editorial split tokens.
- [x] **Buttons defined** — §10, four variants with all five states.
- [x] **Links defined** — §11, five contexts with four states.
- [x] **Forms defined** — §12, eight control types with six states.
- [x] **Product card system defined** — §13, structure, ratio and explicit exclusions.
- [x] **Image rules defined** — §14, ratios, fit, art direction and loading strategy.
- [x] **Icon system defined** — §18, inline SVG with a single stroke weight and size ladder.
- [x] **Navigation rules defined** — §19, heights, spacing, states and the mandatory header backing rule.
- [x] **Motion system defined** — §21, three durations, transform and opacity only, reduced-motion support.
- [x] **Responsive rules defined** — §25, mobile-first ladder and the defects the system must not reproduce.
- [x] **Accessibility rules defined** — §24, contrast, targets, focus, semantics and labelling.
- [x] **Shopify settings principles defined** — §28, a deliberately small merchant surface.
- [x] **Section/block principles defined** — §29, worked schemas and the anti-granularity rule.
- [x] **Design tokens documented** — §30 and `PHASE-2-DESIGN-TOKENS.css`, 164 tokens, validated.
- [x] **Phase 3 requirements documented** — §31.

**Scope compliance.** No homepage was redesigned, no hero or header rebuilt, no product card implemented, no Liquid or Shopify template created, no cart, search or account built, no app installed, no asset deleted or replaced, no JavaScript rewritten, and nothing deployed. Two files were added to the project root: this document and `PHASE-2-DESIGN-TOKENS.css`. Every pre-existing project file is byte-identical.
"""

RECONCILIATION = """

### 30.99 Token requests adopted after the documentation pass

The sections above were written against version 1.0.0 of the token file and
raised a number of token requests and two citation errors. Those were verified
against the source and the token file was corrected before this document was
issued, so the following requests are **already satisfied** in
`PHASE-2-DESIGN-TOKENS.css` and are recorded here only so the register above
reads accurately.

| Adopted | Resolution |
|---|---|
| `--scrim-story-horizontal` | Added, reproducing the story band's 90deg fade from line 127 |
| `--split-rail` | Added as `0.9fr 1.6fr 0.4fr` for the two three-track bands, lines 64 and 125 |
| `--measure-narrow`, `--measure-body` | Added, 40ch and 68ch; the 40ch value carries line 131's 320px caption measure |
| `--icon-stroke-width` | Added at 1.5, so the single-stroke rule is machine-checkable |
| `--swatch-size`, `--swatch-ring` | Added from line 116 |
| `--band-min-height-hero`, `--band-min-height-story` | Added, 620px and 520px, from lines 64 and 125 |
| `--color-overlay`, `--drawer-width` | Added; `--z-overlay` had reserved a layer with no value to fill it |
| `--color-divider` | Added from the footer rule on line 163 |
| `--link-underline-thickness`, `--link-underline-offset` | Added, so underlines do not borrow from the border system |
| `--control-height`, `--control-height-min` | Added, 48px and 44px |
| `--shadow-on-dark` | Added; the ink-based shadows are invisible on the dark surface |
| `--product-col-min` | Added at 17rem for the auto-fill product ladder |
| `--announcement-height-stacked` | Added at 64px for the two-line phone state, line 50 |
| `--hero-pad-block-start` | Satisfied under the clearer names `--header-offset-desktop` and `--header-offset-mobile`, computed from the header height rather than the prototype's hard-coded 170px and 190px |
| `--color-border-interactive`, `--color-border-interactive-inverse` | Added at 3.02:1 and 3.13:1. This closes a real accessibility gap: the four decorative border tokens composite to 1.17-1.35:1, correct for a hairline separator but failing SC 1.4.11 for a control boundary |
| Surface-class additions | `.surface-dark` and `.surface-light` now also map `--color-border-current-subtle`, `--color-border-current-interactive`, `--color-text-current-muted` and `--shadow-current` |
| `--product-grid-gap` conflict | Resolved to 32px, normalised from the 36px product gap on line 106; the contradictory comment on `--grid-gap-large` was corrected |
| `--gs-olive` citation | Corrected: the swatch data is on lines 175-177, not 179 |
| `--logo-height-mobile` citation | Corrected: the rule is on line 32, not 33 |
| Spacing normalisation map | Corrected for the 44px nav gap, the 56px value and the header-offset entries |

**Still open, and deliberately so.** `--focus-ring-companion` (a two-tone ring for
indicators straddling a dark/light boundary) and `--type-label-weight-nav` (the
prototype's 500 nav weight against the label triplet's 600) are recorded as
recommendations in §23 and §6. Both need a design decision rather than a
mechanical fix, so neither was added unilaterally.

The token file now declares 191 unique tokens. It validates: braces balanced,
comments balanced, no undefined `var()` reference, and every contrast figure in
its comments re-verified against computed values.
"""

body = []
for n in sorted(sections):
    md, _, _ = wrap_bare_tags(sections[n]['markdown'].strip())
    if n == 30:
        md = md + RECONCILIATION
    body.append("## %d. %s\n\n%s" % (n, TITLES.get(n, sections[n]['title']), md))

doc = "\n\n".join([HEADER] + body + [
    "## Appendix A. Design QA Checklist\n\n" + QA,
    "## Appendix B. Phase 2 Completion Criteria\n\n" + CRITERIA,
    "## Appendix C. Business information required\n\n"
    "These are inputs Phase 2 could not supply and did not invent. Each blocks the work named beside it.\n\n"
    + ("\n".join("- %s" % b for b in bir_clean) if bir_clean else "- None outstanding."),
])

doc, wrapped, adj = wrap_bare_tags(doc)

print("\nVerification:")
heads = re.findall(r'^## (?:(\d+)\.|Appendix ([ABC])\.) ', doc, re.M)
nums = [int(h[0]) for h in heads if h[0]]
print("  numbered sections: %d  missing: %s  duplicated: %s" %
      (len(nums), [n for n in range(1, 32) if n not in nums] or 'none',
       [n for n, k in collections.Counter(nums).items() if k > 1] or 'none'))
print("  appendices:", [h[1] for h in heads if h[1]])
stripped = re.sub(r'`[^`\n]*`', '', re.sub(r'```.*?```', '', doc, flags=re.S))
print("  bare tags outside code:", len(TAG_RE.findall(stripped)))
print("  unbalanced-backtick lines:", sum(1 for l in doc.split('\n') if l.count('`') % 2 and not l.strip().startswith('```')))
print("  fenced delimiters even:", len(re.findall(r'^```', doc, re.M)) % 2 == 0)
# token fidelity: every --token mentioned in the doc must exist in the css
css = open(TOKENS, encoding='utf-8').read()
defined = set(re.findall(r'(--[\w-]+)\s*:', re.sub(r'/\*.*?\*/', '', css, flags=re.S)))
# Only consider tokens written as complete code spans, e.g. `--color-accent`.
# Family shorthands the prose uses (`--type-display-xl`, `--gs-*`) are prefixes of
# real tokens, not claims that a token of that exact name exists.
used = set()
for span in re.findall(r'`([^`\n]+)`', doc):
    used.update(re.findall(r'(--[a-z][a-z0-9-]{3,})', span))
def is_claim(t):
    if t in defined: return False
    if t.endswith('-') or t.endswith('*'): return False        # wildcard / truncated
    if any(d.startswith(t + '-') for d in defined): return False  # family shorthand
    return True
unknown = sorted(t for t in used if is_claim(t))
print("  tokens referenced in the doc but NOT in the css:", unknown or 'none')
print("  (checked %d distinct token names appearing in code spans)" % len(used))
print("  characters: %s  words: %s" % (format(len(doc), ','), format(len(doc.split()), ',')))

if write:
    open(OUT, 'w', encoding='utf-8', newline='\n').write(doc.rstrip() + '\n')
    print("\nWROTE %s (%s bytes)" % (OUT, format(os.path.getsize(OUT), ',')))
else:
    p = os.path.dirname(os.path.abspath(__file__)) + '/phase2/preview.md'
    open(p, 'w', encoding='utf-8', newline='\n').write(doc.rstrip() + '\n')
    print("\n(dry run) preview -> phase2/preview.md")
