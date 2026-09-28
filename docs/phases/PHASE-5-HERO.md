# GOD SQUAD — PHASE 5: HERO SECTION

**Deliverable for Phase 5 of the Shopify Online Store 2.0 theme build.**
Written 2026-09-22. Supersedes nothing; extends `PHASE-4-HEADER-NAVIGATION.md`.

Sources of truth this phase is built on:

| Document | What it governs here |
|---|---|
| `PHASE-0-PROJECT-FOUNDATION.md` | What the prototype is, and why it is a rebuild target |
| `PHASE-1-WEBSITE-AUDIT.md` | The defects this section must not reproduce |
| `PHASE-2-DESIGN-SYSTEM.md` / `PHASE-2-DESIGN-TOKENS.css` | Type, colour, spacing, scrims, motion, surface contexts |
| `PHASE-3-ASSET-SYSTEM.md` / `PHASE-3-ASSET-MANIFEST.csv` | The hero asset, its ladder, and what is missing |
| `PHASE-4-HEADER-NAVIGATION.md` | How the header overlays this section |

Every number in this document was measured on a rendered page, not estimated.
The method, and one measurement artifact that had to be corrected mid-phase, are
described in §14.

---

## 1. Hero Purpose

The hero is the first thing a visitor sees and the only part of the page that
has to work before anything is read. It has three jobs, in this order:

1. **Say what the brand is** — premium streetwear, not a church merchandise
   table. The photograph does this, which is why the section is built around an
   image that fills the viewport rather than a boxed banner.
2. **Say what the brand stands for** — the two-tone lockup *WALK BY* / **FAITH.**
   with the scripture reference beneath it. This is the approved line and it is
   not editorialised here.
3. **Offer one way forward** — a single call to action, and only one.

### What it replaces, and where it departs

The prototype's hero is `<div data-r="hero-copy">` inside a full-bleed
`<section>`: no classes at all, every value inline, the eyebrow and supporting
statement as bare `<div>`s, and a real `<h1>` carrying one `<span>` with a
hard-coded `color:#d8c08a`. None of that markup survives. Four differences are
deliberate and are recorded here so they are not mistaken for drift:

| Prototype | Here | Why |
|---|---|---|
| Eyebrow in muted gold `#d8c08a` | Eyebrow in cream | Measured. Gold at 13px is normal text needing 4.5:1 and fails on the Subtle overlay at 3.02:1 — see §6 |
| A second column: rotated Kaushan Script *"More / Than / Clothing."*, a rule, and *"A Higher / Purpose."* | Not reproduced | Not in the Phase 5 content brief for this section. It is a candidate for a later section, not a silent deletion — see §16 |
| No call to action in the hero at all | A CTA is built, and hidden until it has a destination | The Phase 5 brief specifies *Shop The Collection*; Phase 1 records every destination as `BUSINESS INFORMATION REQUIRED`, so it renders nothing rather than a dead link — see §7 |
| Supporting statement as three `<br>`-separated lines | One editable line | It is a merchant field now, not markup. The line break is a rendering outcome of the column width, not a hard-coded decision |

The composition — full-bleed photograph, left-weighted wash, the two-tone lockup
over the scripture reference — is unchanged.

**What this section is not.** It is not a slideshow, not a video, not an
animated entrance, and it carries no JavaScript at all. Phase 5 forbids the
first three and the fourth is a deliberate choice: the hero is the LCP element
on the home page, and the cheapest hero is one the browser can paint from markup
and CSS with nothing else to wait for.

---

## 2. Content Hierarchy

The DOM order is the reading order is the visual order. There is no CSS that
reorders anything.

```
section.hero
├── div.hero__media          (absolutely positioned, behind everything)
│   ├── img.hero__image      (or <picture> when a mobile master exists)
│   └── div.hero__scrim      aria-hidden="true"
└── div.hero__inner          (the constrained container)
    └── div.hero__content
        ├── p.hero__eyebrow          "Streetwear With A Purpose."
        ├── h1.hero__heading         "Walk By"
        │                             └── span.hero__heading-accent "Faith."  (display:block)
        ├── p.hero__scripture        "2 Corinthians 5:7"
        ├── p.hero__description      "Different People. Same Purpose."
        └── a.hero__cta              rendered only when a link exists (§7)
```

Five decisions worth stating:

- **One `<h1>`, always.** The accent is a `<span>` inside the same heading, not a
  second heading, so the approved two-tone lockup survives without two headings
  competing. Validated automatically: `exactly one <h1>` is a check in the
  Phase 5 validator. The span is `display: block`, which is what makes the
  two-line lockup structural rather than a wrapping accident — see §6 and
  HERO-03 in §12.
- **The eyebrow is a `<p>`, not an `<h2>`.** It is a tagline, not a section
  title, and promoting it would put an `<h2>` above the `<h1>`.
- **The scripture reference is a `<p>`.** It is a citation, not a quotation, and
  it is rendered verbatim: `2 Corinthians 5:7`. Phase 5 forbids changing it or
  adding any other scripture, and the validator asserts both.
- **The separator above the supporting statement is a `::before`**, not an
  `<hr>`. It is decoration and carries no meaning, so it stays out of the
  accessibility tree entirely.
- **The scrim is `aria-hidden`.** It is a presentation layer over a photograph.

---

## 3. Hero Image

### The asset

| Property | Value |
|---|---|
| Master | `images/hero-group.png` |
| Dimensions | 1672 × 941 (16:9) |
| Bytes | 1,989,201 |
| Colour | RGB, no alpha |
| Provenance | AI-generated. **Unverified licensing** — Phase 3 flags this for confirmation before launch |
| Production ladder | `phase-3-assets/hero/hero-walk-by-faith-desktop-{420,640,960,1280,1672}w.webp` |

| Rung | Bytes | Of the PNG master |
|---|---|---|
| 420w | 19,260 | 1.0% |
| 640w | 31,500 | 1.6% |
| 960w | 59,210 | 3.0% |
| 1280w | 81,354 | 4.1% |
| 1672w | 119,850 | 6.0% |

In production these rungs are not uploaded as separate files. The merchant
uploads the master once through the Theme Editor and Shopify's CDN generates the
ladder from the `widths:` list on `image_tag`. The Phase 3 files exist to prove
the encoding quality and the size envelope, and as the fallback if the CDN is
ever bypassed.

### How it is delivered

```liquid
{{ img | image_url: width: 3000 | image_tag:
     class: 'hero__image',
     loading: 'eager', fetchpriority: 'high', decoding: 'async',
     widths: '420, 640, 750, 960, 1100, 1280, 1440, 1680, 1920, 2200, 2600, 3000',
     sizes: '100vw', alt: img.alt }}
```

- `widths:` and `sizes:` are both explicit. `image_url: width:` on its own emits
  neither a `srcset` nor a `sizes`, which would ship one fixed width to every
  device.
- `fetchpriority` is set on the `img`. Shopify's `preload: true` parameter does
  **not** set fetch priority; it emits a preload link. For an image this high in
  the document the preload scanner finds the `<img>` immediately, so the
  attribute is the useful half and a duplicate preload is not emitted.
- `alt` comes from the image object. It is never invented here. If the merchant
  leaves the alt text empty in the admin, the image is announced as decorative —
  which is the correct default for a photograph behind a heading that already
  carries the message.
- No CDN URL is hand-built anywhere. Phase 5 forbids it and the validator checks.

### Focal points

The frame is 16:9. Every viewport narrower than 16:9 crops it horizontally, so
the crop centre is a setting rather than a constant. Crops were rendered at
fixed band sizes against the real asset and compared:

| Band | Finding |
|---|---|
| 375 × 320 (phone) | 37% and 45% both keep the seated model's chest logo and the second model's logo legible with no cropped third figure. 50% admits a sliver of the third figure; 60% cuts it in half. |
| 768 × 476 (tablet) | 30%–50% all hold three figures with the back print readable. 60% cuts the third figure. |
| 1440 × 510 (desktop) | The frame is wider than the image is tall, so the full width is always visible and only the vertical matters. |

The default is **centre-left, 40%** — between the two values that tested clean.
The five options map to:

```css
.hero--focal-left         { --hero-focal-x: 20%; }
.hero--focal-centre-left  { --hero-focal-x: 40%; }
.hero--focal-centre       { --hero-focal-x: 50%; }
.hero--focal-centre-right { --hero-focal-x: 62%; }
.hero--focal-right        { --hero-focal-x: 80%; }
```

The vertical is fixed at 30% for every option. That holds the faces in frame at
every crop, which is the one thing that must not be lost.

### Why the photograph needs a scrim

Column luminance sampled across the master in twenty bands:

| Band | Relative luminance |
|---|---|
| 0–5% | 0.094 |
| 5–10% | 0.217 |
| **10–15%** | **0.339** |
| **15–20%** | **0.413** |
| **20–25%** | **0.374** |
| 25–30% | 0.285 |
| 30–35% | 0.130 |
| 35–40% | 0.101 |
| … | … |
| 79–84% | 0.094 |
| 94–99% | 0.442 |

The left third averages 0.29 and peaks at 0.41 — **the brightest part of the
frame is exactly where the copy sits.** Rendered with the scrim removed
entirely, the worst backdrop pixel behind every one of the four text elements
carries cream at **1.00:1** at both 375px and 1440px. The wash is not a stylistic
choice; without it the hero has no readable text at all.

---

## 4. Desktop Behavior

From 1024px up:

- The header overlays the hero. `sections/header.liquid` publishes its own
  clearance as `--header-overlay-offset`, and the hero consumes it:
  `padding-block: calc(var(--header-overlay-offset, 0px) + var(--space-8)) var(--space-9)`.
  The hero never reads the header's settings; if the merchant turns overlay off,
  the custom property is absent, the fallback `0px` applies, and the hero simply
  starts below the header in normal flow.
- Measured clearance from the top of the hero to the top of the copy block:
  **170px at 1024/1280/1440**, 208px at 1920 (the section is taller there, and
  the copy is vertically centred).
- The wash runs horizontally, left-weighted, following the approved design.
- The content column is capped at 42rem inside a centred `--container-standard`.
  Measured column width: **672px** at every width from 1024 up.
- The full width of the image is always visible, because the section is wider
  than 16:9 at these sizes. The focal-point setting has no visible effect here,
  which is why its label says *"Focal point on narrow screens"*.

## 5. Mobile Behavior

Below 1024px:

- The header still overlays; the published clearance is 88px, and the measured
  distance from the top of the hero to the copy is **170px at 375**, 177 at 390,
  190 at 430 and 238 at 768.
- The wash runs **vertically**, bottom-weighted. The copy sits low over the
  picture and the upper third holds the faces, so a left-weighted wash would
  darken the wrong part of the frame.
- The gutter is 24px below 768 and 32px at 768. Content column: 327px at 375,
  342 at 390, 382 at 430, 608 at 768.
- The heading wraps to two lines at 375–430 and to three at 320. It is a single
  line at 768. `text-wrap: balance` keeps the break sensible.
- `hero--h-full` subtracts `--announcement-height-stacked` below 768, because
  the announcement bar stacks its messages on narrow screens and is 65px tall
  rather than 41px. Measured and confirmed at both.

**There is no mobile hero master.** The desktop 16:9 frame is cropped to the
phone band with the focal point applied. The `mobile_image` picker exists and is
wired (including a `<picture>` with a `(max-width: 749px)` source) but is
deliberately left empty, because inventing a crop is not the same as
art-directing one. See §15.

---

## 6. Typography

Everything comes from Phase 2 tokens. Nothing is a literal.

| Element | Token | Rendered 375 | Rendered 768 | Rendered 1440 |
|---|---|---|---|---|
| Eyebrow | `--type-eyebrow-*` | 13px / 500 / 3.9px tracking | 13px | 13px |
| Heading | `--type-display-xl-*` | 56px / 900 / lh 49.28 / ls −0.56 | 65.28px / lh 57.45 | 112px / lh 98.56 / ls −1.12 |
| Scripture | `--type-label-size` + eyebrow tracking | 12px / 400 / 3.6px | 12px | 12px |
| Supporting | `--type-label-*`, `--type-tagline-lh` | 12px / lh 20.4 / 2.64px | 12px | 12px |
| Button label | `--type-label-*` | 12px | 12px | 12px |

Faces: **Playfair Display** (display, 900) for the heading; **Jost** for
everything else. Both are the Phase 2 families, reached through
`--font-display` and `--font-body`.

The heading scales fluidly between 56px and 112px. It is capped at 112px: past
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
it, which is what HERO-03 asked for.

**Colour.** The heading is cream with a gold accent phrase. The eyebrow,
scripture and supporting statement are all cream (the supporting statement uses
`--color-text-secondary`, a slightly softened cream). Gold appears exactly twice
in the section: the heading accent and the 32px hairline above the supporting
statement. This is the Phase 2 rule that muted gold is a dark-surface accent
only, applied.

**The eyebrow is cream, not gold, and that is a measured decision.** Gold at
13px is normal text, so it needs 4.5:1, and it needs a backdrop at or below
0.081 relative luminance to get there — about half the 0.153 cream can live
with. The merchant can choose the *Subtle* overlay, and that is where the
difference bites: rendered at 375px on Subtle, the worst backdrop pixel behind
the eyebrow carries **cream at 4.67:1 and gold at 3.02:1**. Cream passes, gold
fails, and rescuing gold would mean a heavier wash on every setting, which
Phase 5 §9 forbids. Gold therefore stays on the heading accent, which is large
text needing 3:1 and clears it everywhere measured (worst case 8.18:1).

---

## 7. CTA

**In the shipped configuration the button does not render, on purpose.**

Phase 1 Appendix A records every navigation destination in this project as
`BUSINESS INFORMATION REQUIRED`. Phase 5 forbids inventing a URL. The prototype
shipped six `href="#"` anchors. Rather than reproduce that, the section treats a
label without a link as *not ready*:

```liquid
assign has_cta = false
if btn_label != blank and btn_link != blank
  assign has_cta = true
endif
```

`button_link` has **no default value** in the schema, so the button stays hidden
until a merchant points it somewhere. The setting's help text says so. The
moment a collection handle exists, one field in the Theme Editor turns it on —
no code change.

The button is fully built and was rendered and measured with a link supplied:

| Property | Measured |
|---|---|
| Size | 259 × 48 px at both 375 and 1440 |
| `min-height` | 44px (`--target-min`) |
| Padding | 16px 32px |
| Face / label | cream `#F3EFE6` on ink `#0D0C0A` — **17.04:1** |
| Corner radius | 2px (`--radius-sm`) — a rectangle, not a pill, per Phase 2 §10 |
| Hover | face changes to `--color-accent`, label stays ink |
| Focus ring | 2px gold, 2px offset |

Target size clears WCAG 2.2 SC 2.5.8 (24 × 24) by a wide margin and also clears
the 44 × 44 usability target in both dimensions.

**Focus indicator contrast.** The ring is gold `#D8C08A`, and gold on the cream
button face is only 1.55:1 — which would fail SC 1.4.11 if the ring touched the
button. It does not: `--focus-offset: 2px` leaves a 2px gap of dark hero
backdrop between the ring and the cream face. Sampled pixel by pixel across the
button's left and top edges, the sequence is backdrop → gold ring (2px) →
backdrop (2px) → cream face. The ring's adjacent colours are therefore the
backdrop on both sides, measured at **9.24:1** at worst. Passes.

---

## 8. Overlay

Four settings. Narrow viewports get a vertical, bottom-weighted wash; from
1024px up the wash turns horizontal and left-weighted, following the approved
design and the content column.

The horizontal wash holds its alpha across the column instead of fading at a
fixed point, because where the column ends as a fraction of the viewport changes
with width: **70% at 1024px, 56% at 1280px, 50% from 1440px up**. Two custom
properties track it:

| Breakpoint | `--hero-wash-hold` | `--hero-wash-end` |
|---|---|---|
| ≥ 1024px | 66% | 90% |
| ≥ 1280px | 54% | 82% |
| ≥ 1440px | 48% | 76% |

This is not cosmetic tuning, and what it protects is the **column**, not today's
copy. The shipped heading reaches only 48% of the viewport at 1024px and passes
at any hold — but `heading` is a merchant field, and a longer one fills the
column out to 70%. Sampled across the full column with the hold fixed at 50%:

| Width | Hold 50% (cream / gold) | Shipped hold (cream / gold) |
|---|---|---|
| 1024 | **2.43 / 1.57 — FAIL** | 66% → 9.48 / 6.12 — PASS |
| 1280 | 7.96 / 5.15 — PASS | 54% → 10.90 / 7.05 — PASS |
| 1440 | 12.19 / 7.88 — PASS | 48% → 10.92 / 7.06 — PASS |

1024px is the only breakpoint that needs the long hold. The 1280 and 1440 steps
exist to *relax* the wash and give the photograph back, not to fix contrast.

### Measured worst-case contrast per setting

Worst single pixel anywhere inside each text element's box, against the shipped
copy.

| Setting | 375 eyebrow | 375 heading | 1440 eyebrow | 1440 heading | Verdict |
|---|---|---|---|---|---|
| Subtle | 4.67 | 5.71 | 7.88 | 5.16 | **PASS** (cream) |
| Medium *(default)* | 11.98 | 12.97 | 13.67 | 12.16 | **PASS** |
| Strong | 14.52 | 14.96 | 15.29 | 13.50 | **PASS** |
| None | 1.00 | 1.00 | 1.00 | 1.00 | **FAIL** |

Subtle, Medium and Strong all clear WCAG AA against the approved photograph.
**None cannot be made safe over this image** — it is retained because a merchant
may later supply an image that is already dark where the words sit, and the
setting's help text now says exactly that.

When the text alignment is centre or right, the horizontal wash would leave the
words on the bright side of the frame, so `hero--align-centre` and
`hero--align-right` swap in their own gradients. Those two combinations have not
been contrast-measured, because they are not the approved configuration; see §15.

---

## 9. Theme Editor Settings

Fourteen settings in four groups. Every one has a purpose; none is a knob for
its own sake.

| Group | ID | Type | Default | Notes |
|---|---|---|---|---|
| Image | `image` | image_picker | — | Help text carries the Phase 3 provenance warning |
| Image | `mobile_image` | image_picker | — | Empty by design; help text explains the gap |
| Image | `focal_point` | select ×5 | `centre-left` | Labelled *"Focal point on narrow screens"* |
| Image | `overlay` | select ×4 | `medium` | Help text names the one unsafe option |
| Content | `eyebrow` | text | Streetwear With A Purpose. | |
| Content | `heading` | text | Walk By | Help text says it becomes the page's only H1 |
| Content | `heading_accent` | text | Faith. | Separate field so the lockup survives editing |
| Content | `scripture` | text | 2 Corinthians 5:7 | |
| Content | `description` | textarea | Different People. Same Purpose. | |
| Call to action | `button_label` | text | Shop The Collection | |
| Call to action | `button_link` | url | **none** | Button hidden until set |
| Layout | `height` | select ×4 | `medium` | small / medium / large / full |
| Layout | `text_position` | select ×3 | `centre` | top / centre / bottom |
| Layout | `text_alignment` | select ×3 | `left` | left / centre / right |

One preset, **God Squad Hero**, carrying the approved configuration so the
section can be added to any template and look right immediately.

Every select value the schema can emit has a corresponding CSS class, verified
automatically. Two classes are styleless on purpose: `hero--overlay-none` (there
is no scrim element to style) and `hero--align-left` (it is the base state, and
a rule would only restate the default).

---

## 10. Shopify Architecture

```
sections/hero.liquid        12,145 B   the section, its schema, one preset
assets/section-hero.css     14,986 B   all of the styling
templates/index.json           540 B   wires the hero into the home page
```

- **Section, not a snippet, not a block.** The hero is a top-level composition
  the merchant reorders in the Theme Editor, so it is a section with a preset.
  It has no blocks: there is nothing inside it a merchant would want to add,
  remove or reorder, and inventing blocks would only let them break the lockup.
- **Loaded from `templates/index.json`**, not from a section group. Section
  groups are for the header and footer; body sections belong to the template.
- **`{{ section.shopify_attributes }}`** is emitted on the root element, so the
  Theme Editor can target the section for selection and live updates.
- **No `enabled_on` restriction.** The hero is deliberately available on any
  template, not just the home page.
- **The stylesheet is loaded by the section**, via
  `{{ 'section-hero.css' | asset_url | stylesheet_tag }}`, not by
  `layout/theme.liquid`. A page without a hero never pays for hero CSS. Verified
  by the validator in both directions.
- **No `shopify:section:load` handler**, because there is no JavaScript to
  re-initialise. The section is fully declarative and re-renders correctly in the
  editor with no help.
- **The button system lives in `section-hero.css` for now.** The hero is the
  first section with a button. The file carries a note to promote `.button` /
  `.button--primary` to a shared stylesheet the moment a second section needs
  it, rather than duplicating it — a Phase 6 decision, flagged in §16.

### The contract with the header

`sections/header.liquid` publishes, and only when it actually overlays:

```liquid
<style>
  :root { --header-overlay-offset: var(--header-height-mobile); }
  @media (min-width: 1024px) {
    :root { --header-overlay-offset: var(--header-height-desktop); }
  }
</style>
```

The hero consumes it with a `0px` fallback. Neither section imports anything
from the other, and either can be removed without breaking the page. Measured
values in use: 88px below 1024, 122px from 1024 up.

---

## 11. Responsive Strategy

No JavaScript, no resize listeners, no breakpoint classes in markup. Everything
is CSS, and the breakpoints are the Phase 2 set.

| What changes | Where | Why |
|---|---|---|
| Wash direction | 1024px | The copy moves from "low over the picture" to "left of the picture" |
| Content column cap | 768px (38rem), 1024px (42rem) | Keeps the measure readable as the gutter grows |
| Vertical rhythm | 1024px (`--space-8` / `--space-9`) | More air once the header clearance grows |
| Wash hold / end | 1024, 1280, 1440 | Tracks the content column (§8) |
| Full-height maths | 768px | The announcement bar stacks below 768 and is 65px, not 41px |

**Heights use `svh`, not `vh`.** On phones the browser toolbar makes `vh` jump
during scroll, which would make a `100vh` hero resize under the reader's thumb.
Every option is also clamped so the hero cannot grow without limit on a very
tall or very short screen:

```css
.hero--h-small  { min-height: clamp(24rem, 52svh, 34rem); }
.hero--h-medium { min-height: clamp(32rem, 68svh, 45rem); }
.hero--h-large  { min-height: clamp(38rem, 82svh, 55rem); }
.hero--h-full   { min-height: calc(100svh - var(--header-overlay-offset, 0px) - var(--announcement-height)); }
```

Measured section heights on the default *medium*: 517 / 530 / 558 / 612 / 546 /
584 / 590 / 666 px at 375 / 390 / 430 / 768 / 1024 / 1280 / 1440 / 1920.

---

## 12. Accessibility

| Requirement | Result |
|---|---|
| **SC 1.4.3** Contrast (text) | All four text elements PASS at all eight widths. Worst body-size measurement **11.98:1** against a 4.5:1 requirement |
| **SC 1.4.3** Contrast (large text) | Heading PASS at all widths. Worst **8.18:1** (gold accent) against 3:1 |
| **SC 1.4.11** Non-text contrast | Focus ring **9.24:1** against adjacent colours (§7). The scrim is decorative and `aria-hidden` |
| **SC 1.4.10** Reflow | No horizontal scroll at **320px**. Document scroll width equals viewport width at 320, 360, 375, 390, 430, 768, 1024, 1280, 1440 and 1920 |
| **SC 1.4.4 / 1.4.10** Zoom | No horizontal scroll or loss of content at 200% (720 CSS px) or 400% (360 CSS px) |
| **SC 1.4.12** Text spacing | With line-height 1.5, letter-spacing 0.12em, word-spacing 0.16em and paragraph spacing 2em forced, nothing clips or overlaps. The section grows from 517→649px at 375 and 590→959px at 1440 and absorbs it |
| **SC 2.5.8** Target size | CTA 259 × 48 px. No other interactive target in the section |
| **SC 2.4.7 / 2.4.11** Focus | Visible 2px ring with a 2px offset; not obscured by any author content |
| **SC 1.3.1** Info and relationships | One `<h1>`, no skipped heading levels, no layout tables, no meaning carried by colour alone |
| **SC 1.1.1** Non-text content | Image `alt` comes from the merchant's asset; the scrim and the hairline are `aria-hidden` / `::before` |
| **SC 2.3.3 / prefers-reduced-motion** | The hero has no entrance animation at all. The only transition in the file is the button's colour change, explicitly disabled under `prefers-reduced-motion: reduce` |
| **Keyboard** | Nothing in the section is a tab stop except the CTA when it renders. No traps, no custom key handling |
| **Screen reader** | Reading order equals DOM order equals visual order. No `aria-label` overrides the visible text |

### The eight Phase 1 hero issues

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
decision this phase is forbidden to invent.

---

## 13. Performance

**What the hero adds to the page:** one stylesheet and one image. Nothing else.

| Resource | Raw | gzip | Note |
|---|---|---|---|
| `assets/section-hero.css` | 14,986 B | 4,907 B | 6,929 B / 1,571 B gzip once comments are stripped |
| Hero image (1672w WebP) | 119,850 B | — | Already compressed; the CDN serves the right rung |
| JavaScript | **0 B** | — | The section has none |

The stylesheet is comment-heavy on purpose — roughly half of it is the recorded
reasoning behind the measured values. A build step that strips CSS comments
reduces it to **1,571 bytes gzipped**. That is a deployment decision for a later
phase, not a reason to delete the reasoning now.

**LCP.** The hero image is the LCP element on the home page. It carries
`loading="eager"`, `fetchpriority="high"` and `decoding="async"`, sits in the
first section of the document, and is discovered by the preload scanner before
any stylesheet finishes. The `widths:` ladder and `sizes="100vw"` mean a 390px
phone fetches a 420w rung (19 KB), not the 1672w master (120 KB).

**CLS — proven, not asserted.** The page was rendered twice at all eight widths,
once with the hero image and once with its `src` pointed at a file that does not
exist. Every measured box — section, content column, heading, supporting
statement — was byte-identical in all sixteen renders:

```
 width  hero (with image)      hero (no image)        identical
   375  [0, 65, 375, 582]      [0, 65, 375, 582]      yes
   768  [0, 41, 768, 653]      [0, 41, 768, 653]      yes
  1440  [0, 41, 1440, 631]     [0, 41, 1440, 631]     yes
  1920  [0, 41, 1920, 707]     [0, 41, 1920, 707]     yes
```

The section is sized by `min-height` and by its own content; the image is an
absolutely positioned `object-fit: cover` layer inside it. It cannot move
anything, whenever it arrives or if it never does.

**Render-blocking.** `section-hero.css` is emitted in the body by the section.
It blocks rendering of what follows it, which is the hero itself — the correct
trade, since an unstyled flash of the heading over an unscrimmed photograph
would be both ugly and illegible.

---

## 14. QA Results

### Method

The section was rendered in headless Edge at eight widths (375, 390, 430, 768,
1024, 1280, 1440, 1920) plus 320 for reflow. For every width, two renders were
captured: the page as shipped, and the same page with the four text elements set
to `visibility: hidden`. Element geometry was read from
`getBoundingClientRect()`. Contrast was then computed per pixel: for every pixel
the glyphs touch, the backdrop colour was read from the text-hidden capture and
measured against the element's computed colour.

Two figures are reported for each element:

- **Glyph worst** — the darkest-contrast pixel under an actual glyph. This is
  the WCAG-relevant number.
- **Box worst** — the worst pixel anywhere inside the element's block box,
  including where there is currently no text. This is the headroom available if
  a merchant types a longer heading, and it is the stricter of the two.

**A measurement artifact had to be corrected mid-phase, and it is recorded here
because it invalidated a first round of results.** Headless Edge on Windows will
not lay out below roughly 492 CSS pixels, and `--screenshot` crops or scales the
result to the requested window size rather than re-laying it out. A request for
`--window-size=375,760` produced a 375-pixel-wide PNG of a **492-pixel-wide
layout**; at 768 it produced a 768-pixel PNG of a 744-pixel layout. Verified by
rendering a page that prints `window.innerWidth` and a 50% colour split: at
`--window-size=375` the page reported `innerWidth=492` and the split landed at
x=246. Every capture in this document was therefore re-taken through a wrapper
page holding an iframe of the exact target width, cropped to that width — which
reports `innerWidth=375` and puts the split at x=187. Unrelated but also caught:
large WebP renders occasionally miss the screenshot deadline, so each capture is
now verified to contain the photograph before it is measured, and re-taken with
a longer budget if not.

### Contrast, all eight widths

Requirement: 4.5:1 for the eyebrow, scripture and supporting statement (normal
text); 3:1 for the heading and its accent (large text).

| Width | Eyebrow | Heading (cream) | Accent (gold) | Scripture | Supporting |
|---|---|---|---|---|---|
| 375 | 11.99 / 11.98 | 12.99 / 12.97 | 8.94 / 8.72 | 13.86 / 13.68 | 12.71 / 12.67 |
| 390 | 11.98 / 11.98 | 12.96 / 12.96 | 8.84 / 8.84 | 13.81 / 13.81 | 12.81 / 12.66 |
| 430 | 12.53 / 12.15 | 12.96 / 12.79 | 9.06 / 8.84 | 14.02 / 14.02 | 12.77 / 12.54 |
| 768 | 12.40 / 12.28 | 12.78 / 12.61 | 8.61 / 8.51 | 15.70 / 15.70 | 12.91 / 12.67 |
| 1024 | 14.14 / 13.94 | 13.80 / 13.63 | 9.05 / 8.21 | 16.67 / 16.67 | 13.22 / 12.21 |
| 1280 | 14.01 / 13.77 | 13.33 / 12.34 | 8.81 / 8.18 | 16.58 / 16.57 | 13.25 / 13.08 |
| 1440 | 13.84 / 13.67 | 12.46 / 12.16 | 8.53 / 8.53 | 16.58 / 16.54 | 15.08 / 13.39 |
| 1920 | 13.63 / 13.60 | 12.91 / 12.16 | 8.70 / 8.50 | 14.09 / 13.97 | 14.36 / 13.89 |

*(glyph worst / box worst)*

**40 measurements, 40 passes, on both metrics.** The lowest absolute figure
anywhere is the gold accent at 1280px, 8.18:1 against a 3:1 requirement. The
narrowest margin relative to its own requirement is the eyebrow at 375-390px:
11.98:1 against 4.5:1, or 2.7x the minimum. Every figure in this table was
re-measured after the HERO-03 lockup change; none of them is carried over.

### Visual QA

| Width | Result |
|---|---|
| 320 | Heading wraps to three lines, everything fits, no clipping, no horizontal scroll |
| 375 / 390 / 430 | Two-line heading, announcement bar stacks, all five header controls fit, faces read in the upper third |
| 768 | Two-line lockup — the width at which the prototype lost it — announcement bar goes horizontal, header height still 88px |
| 1024 | Header 122px, horizontal wash begins, photograph reads clearly right of 66% |
| 1280 / 1440 | Two-line lockup left, full composition visible right, no letterboxing |
| 1920 | Content column stays at 672px inside the centred container; image upscaled from 1672 (see §15) |

No horizontal overflow at any width. Document scroll width equals viewport width
in all ten renders.

### Structural validation

Automated and re-runnable: 8 parse checks plus 32 assertions, all passing.

```
JSON and schema parse            8 files, all OK
Template wiring                  every setting and select value valid
CSS classes                      every modifier the schema can emit is styled
Token fidelity                   0 undefined properties, 0 raw hex, 0 !important,
                                 0 palette-layer tokens reached directly
Markup contract                  1 <h1>, 0 <script>, 0 <video>, 0 inline handlers,
                                 0 hard-coded href, 0 hand-built CDN URLs
Scripture                        "2 Corinthians 5:7", unchanged, nothing added
Translation keys                 0 missing, 0 use of the non-existent `t: default:`
Token copy                       theme copy identical to the canonical file
Originals                        44 tracked files, 0 modified, 0 deleted
```

The 31 `rgba(13, 12, 10, …)` values in the stylesheet are scrim stops. That is
the ink literal Phase 2 defines as the scrim base; CSS custom properties cannot
carry an alpha channel into a gradient stop without `color-mix()`, which is not
yet safe to rely on across the target browser set.

---

## 15. Known Limitations

1. **No mobile hero master.** `BUSINESS INFORMATION REQUIRED` / asset gap,
   carried from Phase 3. The phone view crops the 16:9 desktop frame, which
   loses roughly a third of its width and with it the third model and the back
   print. The `mobile_image` setting and the `<picture>` element are built and
   waiting; nothing invents a crop in the meantime.
2. **The phone wash is heavy.** Because the copy sits *over* the picture on a
   phone and the picture is bright where the copy lands, the medium wash reaches
   0.86 alpha by 30% down the frame. The photograph still reads — the models,
   both chest logos and the garment detail are all visible — but the lower two
   thirds are noticeably dimmed. The better answer is an art-directed phone crop
   with the copy below the image, which needs the master from limitation 1.
3. **The image is upscaled above 1672px.** The master is 1672 wide. Shopify will
   not upscale, so the `widths:` entries above 1672 resolve to the master and the
   browser stretches it: 1.15× at a 1920 viewport, and 2× or worse on a
   high-density laptop. Visible softening at 1920 is slight but real. A
   higher-resolution master is a sourcing problem, not a processing one.
4. **Image provenance is unverified.** The hero is AI-generated and its licensing
   has not been established. Phase 3 flagged it; it is still open, and it is
   surfaced in the Theme Editor help text so it cannot be forgotten.
5. **The CTA does not render.** By design, pending a collection URL. This is the
   correct state, not a defect, but the home page currently has no forward path
   out of the hero.
6. **Centre and right alignment are unmeasured.** Those two options swap in their
   own gradients and pass visual inspection, but their contrast has not been
   measured pixel by pixel because they are not the approved configuration. If a
   merchant selects either, the AA guarantee in §12 does not automatically carry.
   Measuring them is cheap and should be done before the theme ships.
7. **The `None` overlay cannot be safe over the current image** (1.00:1). It is
   retained for a future image that is already dark behind the copy, and the
   setting's help text says so plainly.
8. **The button system lives in the hero's stylesheet.** Correct today, wrong the
   moment a second section needs a button. See §16.
9. **`hero--h-full` has not been measured on a real phone.** `svh` behaviour
   under a live, collapsing browser toolbar cannot be reproduced in headless
   rendering. The maths is right and the fallback is safe, but it wants one pass
   on a physical device.

---

## 16. Phase 6 Dependencies

Things the next phase inherits, and decisions it will have to make.

1. **Promote the button system.** `.button` and `.button--primary` are defined in
   `assets/section-hero.css` because the hero is the first section to need them.
   The second section that needs a button must move them to a shared stylesheet
   rather than duplicating them. This is the single highest-value piece of
   housekeeping waiting for Phase 6.
2. **`templates/index.json` grows.** The home page currently contains one
   section. Phase 6 appends to `order` and adds to `sections`; the hero's key
   (`hero`) and settings should not be disturbed.
3. **The section below the hero must own its own top spacing.** The hero ends at
   its own bottom padding (`--space-8` below 1024, `--space-9` above). It does
   not reserve space for whatever follows.
4. **The prototype's hero side column is unplaced.** The rotated Kaushan Script
   *"More Than Clothing."* and *"A Higher Purpose."* block is not in this
   section and has not been deleted from the design — it has nowhere to live
   yet. Phase 6 should decide whether it becomes part of the next section or is
   formally retired.
5. **Surface alternation starts here.** The hero is `surface-dark`. Phase 2's
   surface-context system expects the page to alternate deliberately; the next
   section's surface class is a design decision Phase 6 has to make explicitly,
   not inherit by accident.
6. **`--header-overlay-offset` is a home-page-only contract.** It exists because
   the header overlays the *first* section on the index template. Any section
   that might become the first one needs the same clearance treatment; any
   section that cannot be first does not.
7. **The measurement harness is reusable.** The capture wrapper, the text-hidden
   contrast method, the CLS proof and the validator all generalise to
   the next section with the selector lists swapped. The one thing that must
   carry forward without fail is the iframe wrapper described in §14 — direct
   headless captures below ~492px are not what they appear to be.
8. **Still blocked on business information:** the collection URL for the CTA, a
   mobile hero master, a higher-resolution hero master, and confirmation of the
   hero image's licensing.

---

## File Change Report

### CREATED (2)

| File | Bytes |
|---|---|
| `sections/hero.liquid` | 12,145 |
| `assets/section-hero.css` | 14,986 |

### MODIFIED (2)

| File | Bytes | Change |
|---|---|---|
| `sections/header.liquid` | 10,342 | Publishes `--header-overlay-offset` when it overlays, so the hero can clear it without reading the header's settings |
| `templates/index.json` | 540 | Adds the `hero` section and its approved settings to `order` |

### DELETED (0)

**None.** No file in this project has been deleted in any phase. All 44 tracked
original files were re-hashed after every write in this phase and are byte-for-
byte unchanged.

### Also written

| File | Bytes |
|---|---|
| `PHASE-5-HERO.md` | this document |

### Theme as it now stands

```
layout/theme.liquid                   3,809 B
sections/announcement-bar.liquid      4,008 B
sections/header-group.json              893 B
sections/header.liquid               10,342 B
sections/hero.liquid                 12,145 B     ← new
snippets/icon-account.liquid            708 B
snippets/icon-cart.liquid               856 B
snippets/icon-close.liquid              759 B
snippets/icon-menu.liquid               795 B
snippets/icon-search.liquid             772 B
assets/design-tokens.css             25,275 B
assets/header.css                    11,404 B
assets/header.js                      6,302 B
assets/section-hero.css              14,986 B     ← new
config/settings_data.json               533 B
config/settings_schema.json           2,539 B
locales/en.default.json                 413 B
templates/index.json                    540 B
                                     ─────────
TOTAL                                97,079 B     18 files
```
