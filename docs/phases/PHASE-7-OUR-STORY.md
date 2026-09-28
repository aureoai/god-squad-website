# GOD SQUAD — PHASE 7: OUR STORY + BRAND PURPOSE

Phase 7 deliverable. Built against `PHASE-7-SPEC` as issued, `PHASE-1-WEBSITE-AUDIT.md`,
`PHASE-2-DESIGN-SYSTEM.md`, `PHASE-3-ASSET-MANIFEST.csv`, and the sections delivered in
Phases 4, 5 and 6.

Status: **delivered**. 92 automated checks pass, 48 pixel-sampled contrast measurements pass,
10 viewport widths render with no horizontal overflow, and no file from an earlier phase was
modified.

---

## 1. Objective

Build the homepage Our Story band — the brand's statement of who God Squad is and why it
exists — as an Online Store 2.0 section, together with the small brand-purpose row that
follows it.

The brief's framing was explicit: this is **not** a generic About Us block. It had to feel
premium, emotional, authentic, editorial, minimal, cinematic and faith-driven, use the
established editorial grid rather than a two-column layout, carry an `h2` rather than an
`h1`, run without JavaScript, and invent nothing — no founder, no founding date, no location,
no partnership, no statistic, no testimonial, no theological claim.

It also had to **preserve approved existing brand copy rather than replace it**. The project
contains that copy, so the brief's own suggested direction ("More Than Clothing. A Declaration
of Faith.") was not used. Every default in this section is the prototype's own wording, and
every one of them is a Theme Editor field, so the brief's direction remains one edit away
rather than imposed.

### Phase 1 issues in scope

| ID | Issue | Outcome |
|---|---|---|
| STORY-01 | Wrong asset: a 650×480 crop of the hero with headline fragments baked in | **Structurally closed.** The asset is an `image_picker` and the schema names the canonical composition. The master itself is a sourcing gap — see §12. |
| DEBT-07 | The same asset recorded as technical debt | **Structurally closed**, same mechanism. |
| STORY-02 | Slot has no aspect-ratio and no focal-point rule; crop changes unpredictably per width | **Closed.** A ratio per tier (§8) and the crop centre delegated to Shopify's own focal point (§6). |
| STORY-03 | CTA repeats the eyebrow word for word and points at `#` | **Closed.** Label defaults to "Discover Our Story"; the button does not render without a real destination. |
| STORY-04 | Caption rail stacks as a 145px orphan after the CTA below 900px | **Closed.** Not rendered below 1024px, and a setting turns it off everywhere. |
| STORY-05 | Heading wraps to three lines at 1440 and four at 1024 | **Closed.** Measured two lines at 375–1920 (three only at 320). |
| UX-07 | Nav item and CTA both promise story content that does not exist | **Half closed.** The CTA now stays hidden until a page exists. The nav item belongs to the header and was not touched. |
| UX-03 | No Verse / Faith section | **Out of scope by instruction** — the brief defers the standalone Verse section. |

---

## 2. What was implemented

**One section, `our-story`,** carrying the whole band:

- An **eyebrow**, a **hard-broken display heading**, a **body paragraph** and an optional
  **call to action**, set in the copy track.
- A **photograph** that occupies 70% of the band and bleeds to one edge, with a mandatory
  scrim that always fades toward the copy.
- A **caption rail** — a narrow tracked column at the band's far edge — rendered only in the
  wide composition.
- A **brand-purpose row** of value tiles, built from repeatable blocks.
- A **Theme Editor notice** that names what is missing, rendered in the editor only.

**The composition is the three-track rail, not a two-column block.** Phase 2 §26.3 records
`--split-rail` (0.9fr 1.6fr 0.4fr) as the band's signature: copy / image window / caption rail,
with the photograph offset rather than centred behind the copy. That is what is built. The
brief asked specifically for the established editorial grid rather than a generic two-column
section.

**Zero JavaScript.** No script tag, no inline handler, no dependency on motion. The band is
complete and legible with JS disabled, animation disabled, and CSS gradients unsupported — the
scrim only ever softens an edge, it never carries meaning.

### What was deliberately not built

Header, navigation, hero, featured collection, best sellers, product card, cart, product page,
search, footer, customer accounts — all untouched, and the validator asserts it. The standalone
**Verse** section and the standalone **Social gallery** are not implemented. No dedicated
About/Our Story **page** was created; the brief forbids inventing one, and its content is
BUSINESS INFORMATION REQUIRED.

---

## 3. Files created

| File | Size | Purpose |
|---|---:|---|
| `sections/our-story.liquid` | 20,009 B | The section: 14 settings in 5 groups, 1 block type, 1 preset |
| `assets/section-our-story.css` | 20,448 B | The band's stylesheet, loaded by the section rather than the layout |

Both files are entirely new. No snippet was added — the CTA reuses `snippets/icon-arrow.liquid`
and the button system delivered in Phase 6.

## 4. Files modified

| File | Change |
|---|---|
| `templates/index.json` | Added the `our-story` section, fourth in `order`, with three value blocks |
| `locales/en.default.json` | Added `sections.our_story.no_image`, `.no_alt`, `.no_cta_url` |

Nothing else. `assets/design-tokens.css`, `PHASE-2-DESIGN-TOKENS.css`, `sections/header.liquid`,
`sections/hero.liquid`, `sections/featured-collection.liquid`, `snippets/product-card.liquid`
and `assets/header.js` are byte-identical to their Phase 6 state, and the validator checks this
on every run. All 44 original project files (the prototype, the mockups, the source images) are
unmodified and undeleted.

---

## 5. Story content structure

### The copy that ships

| Field | Default | Provenance |
|---|---|---|
| Eyebrow | `Our Story` | Prototype, line 129 |
| Heading | `Real People.` / `Bigger Purpose.` | Prototype, line 130 |
| Body | "God Squad is a Philippine streetwear brand built on faith, creativity, and community. We create pieces that inspire a generation to live different — with purpose." | Prototype, line 131 |
| Caption rail | `Faith` / `Lives` / `Different` / `Here.` | Prototype, line 136 |
| Button label | `Discover Our Story` | New label only; replaces the prototype's duplicate of the eyebrow (STORY-03) |
| Button link | *(blank)* | BUSINESS INFORMATION REQUIRED — the button does not render |

Nothing here invents a founder, a date, a place, a partnership, a statistic, a testimonial or a
theological claim. There is no `★★★★★`, no customer count, no "trusted by", no press mention,
no endorsement. The scripture reference is not touched — it belongs to the hero and reads
`2 CORINTHIANS 5:7` there, unchanged.

### The heading break is the merchant's

`heading` is a `textarea` and each typed line becomes a rendered line, via `newline_to_br`.
Phase 2 §26.1 defines the display headline as hard-broken; left to wrap, "Real People. Bigger
Purpose." came out on three lines at every width measured, which is exactly the defect
STORY-05 recorded. The copy track also carries a 26rem floor so the browser cannot re-break the
second line even with the break present — see §8.

### The brand-purpose row

Repeatable `value` blocks, limit 6, each a title and one line. No icons, no dividers, no
numbers. Phase 2 §29.5 scopes a fuller standalone `brand-values` section — icons, dividers, up
to six tiles — as its own band; this is the small version the Phase 7 brief permits inside Our
Story.

The three shipped tiles are the prototype's own value copy (`God Squad Website.html`, lines
180–183):

| Title | Line |
|---|---|
| Faith Driven | More Than Clothing |
| Community | People With Purpose |
| Premium Quality | Crafted To Inspire |

The prototype's fourth tile, **"Worldwide / Shipping Available", is deliberately not shipped.**
Phase 1 VAL-04 and UX-05 record it as the one value that is a checkable commercial promise with
no shipping policy, destination list or rate table behind it anywhere in the project. It is
BUSINESS INFORMATION REQUIRED. A merchant who can stand behind it adds it as a fourth block in
one edit.

Every value line is brand messaging, never a measurable claim, and the block's help text says so
in the editor.

### Heading levels

The band's heading is an `h2` — Phase 5 established the home page's single `h1` in the hero, and
Phase 1 HTML-03 recorded the prototype's outline as a defect. The value titles are `h3`s beneath
it, and their level **follows the heading**: if a merchant clears the heading, the `h2` goes with
it, so the tiles become `h2`s rather than hanging off the hero's `h1` with a level skipped.

Measured on the full home page:

```
H1 Walk By Faith.
  H2 The Faithful                             (Phase 6)
    H3 Signature Oversized Tee / Heavyweight Hoodie / Utility Cap
  H2 The Pieces That Define The Movement      (Phase 6)
    H3 Signature Oversized Tee / Heavyweight Hoodie / Utility Cap / Faith Crew
  H2 Real People. Bigger Purpose.             (Phase 7)
    H3 Faith Driven / Community / Premium Quality

h1 count: 1    skipped levels: none
```

---

## 6. Image system

### The asset

The canonical composition is the **three-model community photograph** that Phase 3 identified —
`images/our-story.webp` in the project. The schema names it to the merchant in the image
picker's help text. It is **not** hard-coded: the section has an `image_picker`, the theme never
constructs a Shopify CDN URL, and the validator checks that no image path appears anywhere in
the markup.

The prototype used `./01-hero-model-mu98p88t-7jig.webp` — a crop of the hero with the headline
fragments "A PURPOSE", "K BY", "TH." and the "More Than Clothing" script baked into the pixels
(STORY-01, DEBT-07). Nothing in this section references it.

### Responsive delivery

`image_tag` with explicit `widths` and `sizes` — never a bare `img_url`:

```liquid
{{ img | image_url: width: 2400 | image_tag:
     class: 'our-story__image',
     widths: '480, 640, 900, 1200, 1500, 1800, 2100, 2400',
     sizes: img_sizes,
     loading: 'lazy', decoding: 'async', alt: img.alt }}
```

`img_sizes` is `(min-width: 1024px) 70vw, 100vw`.

That is not an approximation. `.our-story__media` is `width: 70%` of a band that is
`width: 100%` **with no max-width** — only the copy container and the values row are capped at
`--container-standard`. Measured against the rendered slot:

| Viewport | Rendered media | Declared by `sizes` | Error |
|---:|---:|---:|---:|
| 375 | 375 px | 375 px | 0 |
| 768 | 768 px | 768 px | 0 |
| 1024 | 717 px | 717 px | 0 |
| 1280 | 896 px | 896 px | 0 |
| 1440 | 1008 px | 1008 px | 0 |
| 1920 | 1344 px | 1344 px | 0 |

An earlier revision also capped the slot at 70% of `settings.container_width`. That declared
1008 px on a 1920 screen for a slot that renders 1344 px, and let the browser settle for a
candidate a quarter too small. The cap was the mistake — there is nothing above
`--container-standard` for the photograph to stop at.

### Optional mobile crop

A second `image_picker` supplies a portrait or squarer crop for the stacked tiers, delivered
through `<picture><source media="(max-width: 1023px)">` at 480/640/900/1200/1500/2048 w. The
source covers up to 1023 CSS px, which is ~3069 device px at DPR 3, so it reaches past 1200 w.
Leaving it empty falls back to the desktop image.

### The crop centre is Shopify's, not a second control

`image_tag` writes `style="object-position: X% Y%"` **directly onto the `<img>`** whenever the
image carries a focal point set in Shopify admin, and an inline style outranks every rule in a
stylesheet. A theme-side focal select would therefore have moved nothing on exactly the images a
merchant had bothered to position — a control that silently did nothing.

So the theme does not offer one. Shopify's admin focal point is the single source of truth,
which is what STORY-02 asked for ("using the Shopify image focal point"). The stylesheet
supplies `object-position: center 33%` as the default for an image with **no** focal point set;
the prototype's `center top` discarded about a fifth of the picture's height at 1440 — the hands
and chest that carry the composition's gesture.

### Alt text

`alt: img.alt` — taken from the image the merchant uploaded, never invented here. The theme
cannot know what is in the photograph. An empty alt announces the image as decorative, which is
the correct default for a mood photograph beside a heading that already carries the message, and
the editor notice tells the merchant how to change it.

### The scrim

Not optional and not a merchant choice. Phase 2 §29.4 offers an `overlay_style` select; it is
deliberately not exposed, for the same reason Phase 4 made the header scrim mandatory — the copy
sits over the photograph's edge, and a merchant who picked "none" would put cream text on an
unknown image. The direction is derived from the image side instead, so it always fades toward
the copy.

Its base colour follows the surface (`--os-scrim-rgb`), so the photograph dissolves into the
band it is actually in rather than into a colour the band is not.

---

## 7. Theme Editor settings

**14 settings in 5 groups, plus one block type.** Phase 2 §29.6 sets a per-section ceiling of
14.

### Content
| ID | Type | Default |
|---|---|---|
| `eyebrow` | text | `Our Story` |
| `heading` | textarea | `Real People.` ⏎ `Bigger Purpose.` |
| `body` | richtext | the approved brand statement |

### Image
| ID | Type | Notes |
|---|---|---|
| `image` | image_picker | Help text names the canonical asset and the admin focal point |
| `mobile_image` | image_picker | Optional portrait crop below 1024px |
| `image_side` | select | Right *(default)* / Left — the copy and the scrim mirror with it |

### Call to action
| ID | Type | Notes |
|---|---|---|
| `button_label` | text | `Discover Our Story` |
| `button_url` | url | Blank; the button is hidden until it points somewhere |

### Caption rail
| ID | Type | Notes |
|---|---|---|
| `show_caption` | checkbox | On; turns the rail off at every width |
| `caption` | textarea | `Faith` ⏎ `Lives` ⏎ `Different` ⏎ `Here.` |

### Layout
| ID | Type | Notes |
|---|---|---|
| `surface` | select | Ink *(default)* / Cream |
| `spacing_top` | select | None / Tight / Standard — system values, not free pixels |
| `spacing_bottom` | select | None / Tight / Standard |
| `anchor_id` | text | Optional, lets a menu item link to the band |

### Blocks
`value`, limit 6: `title` and `body` (one line). Preset ships three.

### Preset
One preset, "Our Story", carrying every approved default and the three value blocks.

### Surface behaviour

Choosing **Cream** changes three things automatically, none of which the merchant has to know
about:

1. The scrim's base colour flips to cream, so the photograph still dissolves into the band.
2. Text roles flip through Phase 2's surface classes — the eyebrow takes
   `--color-accent-strong` (4.66:1) because muted gold on cream is 1.55:1.
3. The call to action switches from the accent variant to the primary variant. Phase 2 §10.1
   gives the accent variant no light-surface rule at all; used there it would render with no
   fill and no visible border. §10.2 permits the primary as the band's one primary.

Ink is the approved treatment and the default.

---

## 8. Responsive behaviour

Three tiers. The rail arrives at `--bp-lg` (1024px), because a 0.9fr copy track inside a 704px
tablet row is about 190px and cannot hold the display heading — the same reason the Phase 6
collection row's copy column waits.

| | < 768 | 768 – 1023 | ≥ 1024 |
|---|---|---|---|
| Composition | stacked | stacked | three-track rail |
| Media | full width, `4/5` | full width, `3/2` | 70% of the band, offset, `min-height: 520px` |
| Scrim | bottom fade | bottom fade | horizontal, toward the copy |
| Copy | below the photograph | below the photograph | in the 0.9fr track, over the photograph's edge |
| Body measure | `--measure-body` (68ch) | `--measure-body` (68ch) | `--measure-narrow` (40ch) |
| Caption rail | not rendered | not rendered | rendered, with its own backing |
| Value tiles | 1 column | 2 columns | 3 columns at 1024, up to 4 above |

### Measured, at ten widths

| Width | Scroll W | H-scroll | Band | Media | Copy column | Caption | Heading |
|---:|---:|---|---:|---|---|---|---|
| 320 | 320 | no | 1232 | 320×400 | 24–296 | not rendered | 272px @32px, **3 lines** |
| 375 | 375 | no | 1241 | 375×469 | 24–351 | not rendered | 325px @32px, 2 lines |
| 390 | 390 | no | 1259 | 390×488 | 24–366 | not rendered | 325px @32px, 2 lines |
| 430 | 430 | no | 1283 | 430×538 | 24–406 | not rendered | 325px @32px, 2 lines |
| 768 | 768 | no | 1164 | 768×512 | 32–736 | not rendered | 325px @32px, 2 lines |
| 900 | 900 | no | 1276 | 900×600 | 32–868 | not rendered | 365px @36px, 2 lines |
| 1024 | 1024 | no | 902 | 717×520 | 48–464 | 832–976 | 406px @40px, 2 lines |
| 1280 | 1280 | no | 995 | 896×583 | 48–464 | 1088–1232 | 406px @40px, 2 lines |
| 1440 | 1440 | no | 1087 | 1008×656 | 48–464 | 1216–1392 | 406px @40px, 2 lines |
| 1920 | 1920 | no | 1325 | 1344×874 | 288–704 | 1456–1632 | 406px @40px, 2 lines |

No element exceeds the viewport at any width. Reflow at 320px (SC 1.4.10) holds; the heading
takes three lines there, which is the correct outcome for a 272px column.

### The copy track's floor is measured, not chosen

`minmax(26rem, 0.9fr)`. With the real face and tracking, the approved heading's two lines set at
253 / 325 (32px), 285 / 366 (36px) and 316 / **406** (40px). The scale caps at 40px from a
1000px viewport, so the track has to clear 406px or the browser re-breaks the second line even
with the break already in the markup — which is what the first render did, at a track of 397px.
The width comes out of the empty image-window track, not out of the photograph, which is 70% of
the band either way. Inner tracks at 1440 measure **416 / 688 / 176**.

A longer merchant heading still wraps. That is correct: the floor guarantees the approved lockup
sets as drawn, not that any text will.

### The media ratio per tier

`4/5` below 768 — the same portrait the hero uses on a phone; the band sits under a thumb and
the taller frame holds the subject where a landscape crop would lose it. `3/2` from 768, because
`4/5` at 768 is a 960px-tall band that pushes every word below the fold (measured, not assumed),
and 3:2 is also the canonical asset's own ratio, so the photograph is shown essentially
uncropped there. From 1024 the ratio is released and the media takes `min-height: 520px`
(`--band-min-height-story`) with the copy driving the band's height.

### The values row

`repeat(auto-fit, minmax(min(17rem, 100%), 1fr))`. The floor is 17rem rather than 14 because the
row is capped at `--container-standard`: at 1440 it is 1344px wide, a 14rem floor fits five
tracks there, and the schema's sixth permitted block then sits alone on a second row. Measured
at both block counts:

| Blocks | 1024 | 1280 | 1440 | 1920 |
|---:|---|---|---|---|
| 3 (shipped) | 3 across | 3 across | 3 across | 3 across |
| 6 (schema limit) | 3 + 3 | 4 + 2 | 4 + 2 | 4 + 2 |

`auto-fit` collapses the tracks nobody fills, so three tiles span the full width at every tier.

### The caption rail's backing

Left over the open photograph, the rail's cream 12px measured 1.69, 2.07, 2.14 and 1.86 to one
at 1024, 1280, 1440 and 1920 — against the 4.5:1 a tracked 12px line needs.

A stop in the photograph's own gradient cannot fix that, because the photograph is 70% of a
full-bleed band while the rail sits in a container capped at `--container-standard`, so the
rail's position across the picture moves with the viewport: 73.2% at 1024, 78.6% at 1280, 77.8%
at 1440, 65.5% at 1920, and further left as the screen grows. Strengthening the wash enough for
1920 would have darkened the picture at every other width.

The backing is therefore anchored to the **rail**, not to the photograph: a horizontal gradient
starting fully transparent 10rem to its left, masked vertically so it fades out above and below
rather than cutting two hard lines across the picture. Exact at every width, and it darkens
nothing the words do not need.

---

## 9. Accessibility

Measured on the rendered home page, not asserted.

| Criterion | Result |
|---|---|
| **1.4.3 Contrast (text)** | 48 measurements across both surfaces and four widths — **0 failures**. See the table below. |
| **1.4.11 Non-text contrast** | The band draws no interactive boundary of its own; the CTA is the Phase 6 button component. |
| **1.3.1 Info and relationships** | `h2` + `h3`s, one `<ul role="list">` for the tiles, no `role="menu"`. |
| **2.4.6 Headings and labels** | 1 `h1` on the page, no skipped levels; the tile level follows the band heading. |
| **2.4.11 Focus not obscured** | The scrim and the caption backing are `pointer-events: none` and sit behind the content layer; nothing overlays a focusable element. |
| **2.5.8 Target size** | 0 under-size targets on the page. The band's only target is the CTA, which is hidden as shipped; rendered with a destination it measures **262×50** (ink on gold, 11.01:1). |
| **1.4.10 Reflow** | No horizontal scroll at 320px, or at any of the ten widths measured. |
| **2.1.1 Keyboard** | 26 focusable elements on the page, all in DOM order, **0 positive `tabindex`**. |
| **2.3.3 / prefers-reduced-motion** | Nothing in the stylesheet transitions, moves or fades at any viewport. Rendered under `--force-prefers-reduced-motion`. |
| **1.1.1 Non-text content** | Alt from the asset; the scrim is `aria-hidden="true"`. |

### Contrast, pixel-sampled through the photograph

Each role was measured against the real rendered backdrop — the page captured twice, once
normally and once with the text hidden — so the figures are against the photograph and the
scrim as they actually composite, not against a flat swatch. Both the worst glyph pixel and the
worst pixel in the text's bounding box are reported.

**Ink surface (default)**

| Role | Colour | 1024 | 1280 | 1440 | 1920 | Required |
|---|---|---:|---:|---:|---:|---:|
| Eyebrow | `#D8C08A` | 11.01 | 11.01 | 11.01 | 11.01 | 4.5 |
| Heading | `#F3EFE6` | 16.54 | 16.81 | 16.93 | 16.81 | 3.0 |
| Body | `#BDB6A8` | 9.56 | 9.70 | 9.70 | 9.64 | 4.5 |
| Caption rail | `#F3EFE6` | 8.69 | 8.62 | 8.01 | 8.86 | 4.5 |
| Value title | `#F3EFE6` | 17.04 | 17.04 | 17.04 | 17.04 | 4.5 |
| Value line | `#BDB6A8` | 9.70 | 9.70 | 9.70 | 9.70 | 4.5 |

**Cream surface**

| Role | Colour | 1024 | 1280 | 1440 | 1920 | Required |
|---|---|---:|---:|---:|---:|---:|
| Eyebrow | `#82672B` | 4.66 | 4.66 | 4.66 | 4.66 | 4.5 |
| Heading | `#0D0C0A` | 16.73 | 16.73 | 16.89 | 16.73 | 3.0 |
| Body | `#5F5A50` | 5.80 | 5.92 | 5.97 | 5.87 | 4.5 |
| Caption rail | `#0D0C0A` | 11.91 | 8.26 | 7.32 | 10.52 | 4.5 |
| Value title | `#0D0C0A` | 17.04 | 17.04 | 17.04 | 17.04 | 4.5 |
| Value line | `#5F5A50` | 5.97 | 5.97 | 5.97 | 5.97 | 4.5 |

### Gold is spent once

Phase 2 §26.5 allows a band two accent marks. The eyebrow is the one. An earlier revision also
set the three value titles in gold, which made four — and the prototype's own tiles set their
titles in cream, not gold. The titles now inherit the band's text colour, which also lifts them
from 11.01:1 to 17.04:1. Weight, tracking and caps carry the hierarchy instead.

---

## 10. Performance

- **No JavaScript.** Nothing to parse, nothing to execute, nothing to hydrate.
- **No web font added.** The band uses the faces already loaded by the layout.
- **One stylesheet, requested by the section** rather than the layout, so a page without this
  section does not download it. A section with neither an image nor a heading requests nothing
  at all.
- **`loading="lazy"` and `decoding="async"`** on the photograph. The band is below the fold on
  every layout measured; it is not the LCP element.
- **Eight `srcset` candidates** (480–2400 w) with a `sizes` that is exact at every width
  measured — see §6. An under-declared `sizes` is the common way a correct `srcset` still
  downloads the wrong file.
- **`width` and `height` on the mobile `<source>`**, and an `aspect-ratio` on the media wrapper
  at every tier, so the band reserves its space and contributes no layout shift.
- **No `!important`, no raw hex** (other than the `#000` keyword inside a mask gradient), **no
  magic numbers** — every value is a Phase 2 token or a measured floor with its arithmetic in a
  comment.
- Stylesheet 20,448 B uncompressed; section template 20,009 B, of which roughly half is comment
  and schema.

---

## 11. Testing

Rendering was done against the **real `.liquid` files** by the mini-Liquid harness built in
Phase 5 and extended here — the section, the snippets and the token stylesheets are executed
against mock Shopify data. No fixture HTML was hand-written.

| Pass | Coverage | Result |
|---|---|---|
| **Static validation** | 92 assertions: schema and JSON parse, template wiring, approved copy, markup contract, review contract, token fidelity, no-JS, translation keys, earlier phases intact, original files untouched | **92 pass, 0 fail** |
| **Render cases** | 19 pages: home, story alone, mobile image, image left, no image (live and editor), no alt, CTA present, CTA label without URL, long heading, short heading, long body, no caption, no values, six values, no heading, cream surface, story first, story removed | all render; **0 missing translations** |
| **Geometry** | 10 widths, 320–1920 | no horizontal overflow; heading two lines at 375–1920 |
| **Contrast** | 6 roles × 4 widths × 2 surfaces, pixel-sampled through the photograph | **48 measurements, 0 failures** |
| **Values wrapping** | 2 block counts × 4 widths | no orphaned tile at any combination |
| **Accessibility** | full home page | 1 `h1`, no skipped levels, 0 positive `tabindex`, 0 under-size targets |
| **Visual** | 375 / 768 / 1440 / 1920 ink, 1440 cream, 1440 no-image, 1440 six values | reviewed |

### Adversarial review

The build was put through a multi-agent adversarial review before this document was written:
**44 findings raised, 30 confirmed after verification.** Nine of the confirmed findings had
already been closed by a fix applied while the review was running (the cream surface, the scrim
base colour and the CTA variant). The remaining live defects were fixed and are now locked by
new validator assertions:

| Defect | Fix |
|---|---|
| `image_tag`'s inline focal-point style made the theme's focal select inert | Select removed; admin focal point is the source of truth (§6) |
| `sizes` capped the slot at the container width | `(min-width: 1024px) 70vw, 100vw` (§6) |
| The media wrapper rendered with a ratio and an ink fill even with no image | Wrapper moved inside the image guard |
| Four gold marks against Phase 2 §26.5's budget of two | Value titles inherit (§9) |
| The 40ch editorial cap applied at 768–1023, where the copy runs full width | Reading measure when stacked, editorial measure at the split (§8) |
| Value blocks shipped copy I had written over approved copy the project holds | The prototype's own three tiles (§5) |
| One value line duplicated the hero's shipped copy | Replaced with the approved line |
| A sixth value block orphaned on its own row at 1440 | 17rem track floor (§8) |
| `--os-wash-hold` / `--os-wash-end` read with fallbacks but defined nowhere | Inlined |
| A `::after` override that re-declared the value it overrode | Deleted |
| Three comments that described the code inaccurately | Corrected |
| The mobile `<source>` topped out at 1200 w | Extended to 2048 w |
| `h3` tiles could outlive the `h2` above them | Level derived from the heading (§5) |

### A measurement hazard worth recording

Two harness results had to be discarded and re-taken:

- **`read_probe.py` only parses a dump already on disk.** Run on its own after an edit it
  reports the *previous* build's geometry. It now has a driver (`run_probe.py`) that regenerates
  the dump first, on a browser profile thrown away each time.
- **`http.server` answers `If-Modified-Since` at one-second granularity.** Rewriting one probe
  filename inside the same second hands the browser a 304 and the previous page's geometry. The
  values probe now writes a unique filename per reading.

This is the same class of problem as the Phase 5 capture artifact: the harness quietly returning
a plausible number for the wrong thing. Both were caught because a measured result contradicted
the arithmetic.

---

## 12. Known limitations

### BUSINESS INFORMATION REQUIRED

1. **No Our Story master image exists.** `images/our-story.webp` is 535×348, which upscales
   about 1.9× in this slot. A master of at least 2000px wide with no text baked into it is
   still needed. **`templates/index.json` therefore ships the band with no image** — it renders
   correctly as copy on flat ink, and the Theme Editor notice names the gap.
2. **No Our Story page exists**, so `button_url` is blank and the CTA does not render. The
   brief forbids `href="#"` and forbids inventing the page. (STORY-03, UX-07, Appendix A item
   10.)
3. **"Worldwide / Shipping Available" is withheld** pending a shipping policy, destination list
   and rate table. (VAL-04, UX-05, Appendix A item 22.)
4. **The nav "Our Story" item still targets the homepage section.** Deciding whether it should
   target a page is half of UX-07 and belongs to the header, which Phase 7 must not touch.

### Carried forward

5. **The Phase 5 hero has the same focal-point conflict.** Its `focal_point` select is inert for
   any image that carries an admin focal point, for the reason in §6. The Phase 7 brief forbids
   rebuilding the hero, so it is recorded here rather than changed.
6. **The Phase 4 mobile menu tab-order defect is still open** — the closed panel keeps its links
   in the tab order. One line (`.header__panel[hidden] { visibility: hidden; }`) fixes it, and
   it is not applied because the briefs forbid touching the header.

### Design-system gaps

7. **Phase 2 §14.4 defines no editorial landscape ratio token.** The `3/2` used from 768 is
   written out in this stylesheet and recorded as a token gap rather than a value chosen here.
8. **`--scrim-story-horizontal` exists and is not used.** Its stops are the prototype's, the
   caption rail over them measured 1.69–2.14:1, and it is a fixed ink while this band must also
   fade into cream. Recorded as a token the band cannot use, not a token overlooked.
9. **Phase 2 §26.1 allows one body paragraph; the Phase 7 brief allows up to four.** The field
   accepts up to four and the schema says so. A deliberate, recorded departure.

### Behavioural notes

10. **The caption rail is not rendered below 1024px** — `display: none`, so it leaves the
    accessibility tree as well as the layout. This is the STORY-04 decision, and the
    `show_caption` setting turns it off at every width. It is not read out on a phone.
11. **Three value tiles wrap 2 + 1 at 768–1023.** A floor low enough for three tracks there
    would put five tracks back at 1440 and re-orphan a sixth block. Two-up is a normal editorial
    rhythm at that width and the tiles stay wide.
12. **A long merchant heading still wraps.** The 26rem track floor guarantees the approved lockup
    sets as drawn, not that any text will.

---

## 13. Shopify Admin setup instructions

### Required before launch

1. **Upload the Our Story photograph.**
   *Content → Files*, or directly through the section's image picker.
   Use the approved three-model community composition. **At least 2000px wide**, with no text
   baked into the pixels.
   Then: *Online Store → Themes → Customize → Home page → Our Story → Image*.

2. **Set the image's alt text.**
   *Content → Files → (the image) → Edit alt text.*
   The theme never writes alt text. Left empty, the photograph is announced as decorative, which
   is correct for a mood image beside a heading that already carries the message — but if the
   picture carries meaning the heading does not, describe it here.

3. **Set the image's focal point.**
   *Content → Files → (the image) → Edit → focal point.*
   This is the crop control. The theme deliberately offers no second one, because Shopify writes
   the admin focal point onto the image as an inline style that a stylesheet cannot override.
   With no focal point set, the theme centres the crop at 33% from the top.

4. **Create the Our Story page and link the button.**
   *Online Store → Pages → Add page*, then
   *Customize → Our Story → Button link → select the page*.
   **The button stays hidden until this is set** — by design, so the band never ships a dead
   link.

### Optional

5. **A mobile crop.** *Customize → Our Story → Mobile image.* A portrait or squarer version
   holds the subject better in the full-width band below 1024px. Leave empty to use the desktop
   image.

6. **The value tiles.** *Customize → Our Story → (blocks).* Three ship. Add up to six, reorder
   them, or edit the copy. Keep each line to brand messaging — not a statistic, not a claim
   about reach, not anything a customer could not verify.
   **Add "Worldwide / Shipping Available" only once a shipping policy, destination list and
   rates exist**, and link it to the shipping policy when the brand-values section arrives.

7. **The caption rail.** *Customize → Our Story → Show the caption rail.* On by default at
   1024px and above; never rendered below it.

8. **Colour scheme.** *Customize → Our Story → Colour scheme.* **Ink is the approved treatment.**
   Cream is supported and measured, and the gold button is swapped automatically there because
   gold on cream is 1.55:1.

9. **Anchor.** *Customize → Our Story → Anchor*, default `story`. Lets a menu item link
   straight to the band.

### Nothing to install

No app, no dependency, no external service. The section is pure Liquid and CSS.

---

## Phase 7 is complete. Phase 8 has not been started.
