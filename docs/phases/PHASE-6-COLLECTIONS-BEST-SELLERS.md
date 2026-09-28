# GOD SQUAD — PHASE 6: COLLECTIONS & BEST SELLERS

**Deliverable for Phase 6 of the Shopify Online Store 2.0 theme build.**
Written 2026-09-22. Extends `PHASE-5-HERO.md`.

Sources of truth this phase is built on:

| Document | What it governs here |
|---|---|
| `PHASE-1-WEBSITE-AUDIT.md` | The eleven issues assigned to **PHASE 6 — COLLECTIONS & BEST SELLERS** |
| `PHASE-2-DESIGN-SYSTEM.md` §9.3, §10, §11.5, §13, §14, §22.4, §27, §29.3 | Grid, buttons, product links, the card, images, hover, commerce rules, this section's worked schema |
| `PHASE-2-DESIGN-TOKENS.css` | Every value used here |
| `PHASE-5-HERO.md` §16 | What Phase 5 handed over, including the button promotion |

Every number below was measured on a rendered page. The method, and the two
measurement mistakes that had to be corrected during the phase, are in §11.

---

## 1. What Was Implemented

One reusable collection section, one reusable product card, and the button
component both of them needed.

**The home page now reads:** announcement bar → header → hero → New Drop →
Best Sellers. Sections 6–10 of the intended flow (Our Story, Brand Values,
Verse, Social, Footer) are **not** built; they belong to later phases.

**Shopify is the only source of product data.** There is no product, price,
currency, rating, review, inventory figure, availability claim, colour value or
bestseller ranking anywhere in the theme. "Best Sellers" names a collection the
merchant chooses; nothing in this code decides what sells. A validator check
asserts each of those, and the section ships with **no collection handle at
all** — both rows are `BUSINESS INFORMATION REQUIRED` until a merchant picks
one, and until then they render nothing on the live store.

**One section, not two.** The brief offered `sections/best-sellers.liquid`. It
is not here: Best Sellers and New Drop differ only in which collection is
selected and what the copy says, so a second file would mean fixing every
future bug twice. The section ships **two presets** instead — "New Drop" and
"Best Sellers" — so both are one click away in the Theme Editor with the right
defaults already set, and `templates/index.json` uses the same section type
twice with different settings.

**Zero JavaScript.** The grid renders server-side through Liquid. Nothing
fetches products on the client, nothing hydrates, and every state — hover,
focus, sold out, on sale, empty — is markup and CSS.

---

## 2. Files Created

| File | Bytes | What it is |
|---|---|---|
| `sections/featured-collection.liquid` | 19,478 | The collection row. 19 settings, 2 presets |
| `snippets/product-card.liquid` | 11,394 | The one card the whole theme uses |
| `snippets/icon-arrow.liquid` | 1,068 | Inline SVG arrow, replacing the prototype's `→` glyph |
| `assets/component-product-card.css` | 12,498 | Card and grid. 4,364 B with comments stripped |
| `assets/section-featured-collection.css` | 6,151 | The band. 2,978 B stripped |
| `assets/component-button.css` | 7,576 | The full Phase 2 §10 button system. 2,520 B stripped |
| `PHASE-6-COLLECTIONS-BEST-SELLERS.md` | this document | |

## 3. Files Modified

| File | Change |
|---|---|
| `assets/section-hero.css` | Button system removed from it (see §2 of the button file for the three values it had wrong). Only `.hero__cta`'s placement rule stays |
| `layout/theme.liquid` | Loads `component-button.css`; maps the new `product_image_ratio` theme setting onto `--product-aspect` |
| `assets/design-tokens.css` | **`body { margin: 0 }` added** — see §12 item 1 |
| `PHASE-2-DESIGN-TOKENS.css` | Same reset, so the canonical file and its theme copy stay in step |
| `config/settings_schema.json` | New **Products** group with `product_image_ratio` |
| `config/settings_data.json` | Default and preset for it |
| `templates/index.json` | Adds `new-drop` and `best-sellers`, both `featured-collection` |
| `locales/en.default.json` | 8 new keys under `products.*` and `sections.*` |

**Deleted: 0.** All 44 tracked original project files were re-hashed after every
write and are byte-for-byte unchanged.

**The Phase 4 header and the Phase 5 hero are untouched**, apart from the hero's
stylesheet losing the button block it was explicitly told to hand over.

---

## 4. Shopify Objects Used

Everything the card and section read, and nothing else:

| Object / property | Where | Note |
|---|---|---|
| `collection` (setting type) | section | The merchant's choice; never a handle in code |
| `collection.products` | section | Iterated with `limit:` |
| `collection.url` | section | The View all destination. Never constructed by hand |
| `product.url` | card | The card's one anchor |
| `product.title` | card | The card's heading text |
| `product.featured_image` | card | Fed to `image_url` / `image_tag` |
| `product.price`, `product.price_min` | card | Through the `money` filter |
| `product.price_varies` | card | Switches to the "From X" form |
| `product.compare_at_price_max` | card | The sale signal |
| `product.available` | card | The sold-out state |
| `product.options_with_values[].values[].swatch` | card | `.color` / `.image`, native Shopify swatches only |
| `product.variants.size` | card | Quick add routes multi-variant products to the product page |
| `product.selected_or_first_available_variant.id` | card | The quick-add form's variant |
| `routes.cart_add_url` | card | The quick-add form action |
| `request.design_mode` | section | Editor-only empty states |
| `settings.container_width`, `settings.product_image_ratio` | section / layout | |
| `section.id`, `section.settings` | section | |

**`section.shopify_attributes` is deliberately absent.** The review checked it
against shopify.dev: `shopify_attributes` exists on the **block** object only,
not on `section`. The hero emits it and gets an empty string — harmless, but it
is a no-op, and this section does not repeat it. Recorded in §12 as a Phase 5
documentation correction.

---

## 5. Theme Editor Settings

### Section: "Collection row" — 19 settings in 6 groups

| Group | ID | Type | Default |
|---|---|---|---|
| Collection | `collection` | collection | — |
| | `products_to_show` | range 2–12 | 3 |
| Content | `eyebrow` | text | New Drop / |
| | `heading` | text | The Faithful |
| | `description` | textarea | Premium Essentials for a Higher Purpose. |
| View all | `show_view_all` | checkbox | true |
| | `view_all_label` | text | View All Products |
| | `view_all_url` | url | *(blank — falls back to the collection's own URL)* |
| Layout | `surface` | select: Cream / Ink | Cream |
| | `layout` | select: copy beside / copy above | copy beside |
| Grid | `columns_desktop` | range 2–4 | 3 |
| | `columns_tablet` | range 2–3 | 2 |
| | `columns_mobile` | range 1–2 | 2 |
| Product card | `show_price` | checkbox | true |
| | `show_compare_at_price` | checkbox | true |
| | `show_swatches` | checkbox | true |
| Spacing | `spacing_top` | select: none / tight / standard | standard |
| | `spacing_bottom` | select: none / tight / standard | standard |
| Advanced | `anchor_id` | text | *(blank; the New Drop preset sets `shop`)* |

### Theme setting added

`product_image_ratio` — Square (1:1) or Portrait (4:5), default Square.

### Three deliberate departures from Phase 2 §29.3, and why

Phase 2 worked this section's schema out in advance. Three of its decisions are
overridden here, all three because the Phase 6 brief asks for something else.
They are recorded rather than quietly taken.

1. **`image_ratio` is NOT a section setting.** The brief lists it; Phase 2
   §27.6.5 says the ratio is "chosen once at theme level, never per section",
   because two rows of the same shop with different image shapes is a bug, not
   a choice. Phase 2 wins: it is the theme setting `product_image_ratio`. A
   validator check asserts no section-level `image_ratio` exists.
2. **`show_vendor` is not offered.** The brief says "only if actually useful".
   Phase 2 §27.1 lists vendor name under "Never", because no God Squad surface
   uses one while the catalogue is single-brand. Not offered.
3. **`columns_tablet` and `columns_mobile` ARE offered**, though Phase 2 §29.3
   says both should be derived from `columns_desktop` and §29.6 budgets 14
   settings per section against the 19 here. The brief asks for all three by
   name, twice. Phase 2's stated reason for deriving them was "one fewer way to
   break the grid" — and the grid mechanism in §8 removes that risk
   mechanically: no column count a merchant can choose produces a squeezed
   tile, because the track floor drops a column instead. The settings are
   therefore safe in a way Phase 2 could not assume. The two `spacing_*`
   settings are the same story: the brief asks for them, and they select from
   three system values rather than accepting a free pixel number, so a merchant
   cannot land off the Phase 2 §7.4 rhythm.

If any of the three should go the other way, they are one edit each.

---

## 6. Product Card Behaviour

Structure, in Phase 2 §13.2's closed order:

```
article.product-card
├── a.product-card__link              ← the one anchor, wrapping media + title
│   ├── div.product-card__media       ← fixed ratio, tile ground, overflow hidden
│   │   ├── img.product-card__image
│   │   └── span.product-card__badge  ← "Sold out", aria-hidden (see below)
│   ├── h3.product-card__title
│   └── span.visually-hidden          ← "Sold out", when unavailable
├── p.product-card__price
├── div.product-card__swatches        ← information, not controls
└── div.product-card__actions         ← optional quick add, off by default
```

| Behaviour | Rule |
|---|---|
| **Link** | One anchor per card wrapping media and title, with no interactive element inside it. Swatches and price sit outside it (Phase 2 §11.5) |
| **Focus** | The ring is drawn around the **whole card**, not the anchor's box — `:has(:focus-visible)` with an `@supports not selector(:has(*))` `:focus-within` fallback. Measured: ink ring at 17.04:1 on cream, gold ring at 11.01:1 on ink, bounding box covering media through swatches |
| **Title** | A real heading (Phase 1 HTML-03). Its level follows the section: 3 when the section renders its h2, **2 when the merchant has cleared the heading**, so the outline never skips |
| **Title clamp** | Two lines maximum, with the box always reserving both so prices align across a row. Clamping is visual only: the complete title stays in the DOM and in the link's accessible name |
| **Price** | `money` filter, never string concatenation (Phase 1 DATA-02). Untracked — Phase 2 §27.6.1 stops tracking at numerals |
| **Varying price** | "From X" and no compare-at. A range beside a strike-through is not information |
| **Sale** | Current price at full contrast, compare-at struck through in `--color-text-inverse-muted` (5.97:1). **No SALE badge** — Phase 2 §27.2 says never a red sale flash, §13.5 bans a second badge. Each figure carries a visually hidden "Sale price" / "Regular price" label, so the strike-through is not the only signal |
| **Sold out** | Solid ink badge with a cream label — 17.04:1 over any photograph, which an outlined badge over an unknown image could not guarantee. Media dims to 0.6 as the *secondary* cue. The state is in the link's accessible name, reading "Utility Cap Sold out" |
| **Swatches** | Rendered only from native Shopify swatch data (`value.swatch.color` / `.image`). No colour is ever guessed from an image or a name. Decorative dots plus a visually hidden list of the real colourway names — "Colour: Ink, Cream, Olive". Information, not controls (Phase 2 §27.4), so SC 2.5.8 does not govern their size and `--swatch-size` 16px applies |
| **Hover** | Media scales to `--hover-image-scale` 1.03 over `--transition-medium`; title reveals a 1px underline. Both gated on `@media (hover: hover) and (pointer: fine)`, never on viewport width. The card itself gets no background, border, shadow or lift at any state |
| **Missing image** | The tile ground renders and nothing stands in for a photograph that does not exist |
| **Alt text** | From the image object. When Shopify has defaulted it to the product title — which is already inside the same link — it is emitted empty rather than announcing the name twice |

### Quick add

**Off in every shipped configuration**, and the section exposes no setting to
turn it on. The structural foundation is built and working: when a caller
passes `quick_add: true`, a single-variant product renders a real
`<form action="{{ routes.cart_add_url }}" method="post">` that adds to cart
**with JavaScript disabled**, a multi-variant product renders a link to its
page rather than silently adding a default, and an unavailable product renders
a real `<button aria-disabled="true">` — not a `<span>` wearing button classes,
which Phase 2 §10.5 forbids.

Phase 8 owns the cart. If it adds a drawer it replaces this form's *behaviour*,
not this card's *structure*.

---

## 7. Collection Behaviour

| Case | What happens |
|---|---|
| No collection chosen, live store | **The section renders nothing at all** — no markup, and no stylesheet requests either, because the `stylesheet_tag` calls sit inside the render guard |
| No collection chosen, Theme Editor | Copy column plus a dashed note: "Choose a collection for this section. Nothing is shown on the live store until you do." |
| Collection chosen but empty, live store | **Renders nothing.** The guard tests `has_products`, not "is a collection chosen" — a merchant can empty or unpublish a collection later, and a full-height band of copy with a View all button over nothing is the outcome that avoids |
| Collection chosen but empty, Theme Editor | A different note: "This collection has no products yet. Add products to it in Shopify admin and they will appear here." |
| Fewer products than `products_to_show` | Renders what exists. No placeholders, ever |
| View all | Points at `collection.url` unless the merchant overrides it. A `url` setting cannot default to a dynamic value, so the override is what is offered and the collection URL is the fallback. The button renders only when it has both a label and a destination |

---

## 8. Responsive Behaviour

### The grid mechanism

```css
.product-grid {
  --product-track-ideal: calc((100% - (var(--product-cols) - 1) * var(--product-grid-gap)) / var(--product-cols));
  grid-template-columns: repeat(auto-fill,
    minmax(max(var(--product-track-floor, var(--product-col-min)), var(--product-track-ideal)), 1fr));
}
```

The merchant's column count is a **ceiling, not a command**. `auto-fill` asks
how many tracks of at least `max(floor, ideal)` fit. Where the viewport can
carry the requested count at 272px or wider the count comes out exactly as
asked; where it cannot, the floor wins and the grid **drops a column instead of
squeezing one**. There is no breakpoint gap for a layout to fail in, and no
setting a merchant can choose that produces a broken grid.

272px is Phase 2 §9.3's figure, derived to retire Phase 1 RESP-08 — the
prototype squeezed three columns into ~230px between 901 and 1100, where the
eyebrow, the product names and the CTA all wrapped.

### Measured ladder

Both shipped rows, every width, rendered and read:

| Viewport | New Drop (3 products, asks 3) | Best Sellers (4 products, asks 4) |
|---|---|---|
| 320 | 1 × 272px | 1 × 272px |
| 375 | 2 × 147px | 2 × 147px |
| 430 | 2 × 175px | 2 × 175px |
| 768 | 2 × 336px | 2 × 336px |
| 900 | 2 × 402px | 2 × 402px |
| 1024 | 2 × 300px | 3 × 288px |
| 1180 | 2 × 358px | 3 × 340px |
| 1256 | 2 × 387px | 3 × 365px |
| 1280 | 2 × 396px | **4 × 272px** |
| 1440 | **3 × 297px** | 4 × 312px |
| 1920 | 3 × 297px | 4 × 312px |

Two things follow, and both are trade-offs rather than defects:

**The copy-column layout reaches three columns at 1440, not 1024.** The rail
takes about a third of the row, so the grid beside it carries fewer. The
`layout` setting's help text now says so, and a merchant who wants three
columns from 1024 has the "copy above the products" layout one click away,
where the same collection reaches three at 1024.

**A three-product collection leaves one tile on its own row below 1440.** That
is Phase 1 RESP-03. It is a consequence of the count, not of the grid: three
products cannot fill a two-column row at any tile width the 272px floor allows.
The `products_to_show` help text now says a count that divides evenly into the
column count fills its rows.

### The mobile floor

Below 768 the floor relaxes to **8rem (128px)**, because Phase 2 §13.9 permits
two columns on a phone and the 272px catalogue floor would force one. The value
is measured, not chosen — the full table and both scrollbar regimes are in the
stylesheet's own comment. The 1 → 2 threshold is a layout width of 336px, so a
320px phone gets one column and every phone from 336 up gets two.

### Other responsive behaviour

| What changes | Where | Why |
|---|---|---|
| Copy column appears | 1024 | A 0.9fr rail inside a 704px tablet row is 190px, which cannot hold the display heading |
| Gutter | 768, 1024 | The Phase 2 §8.3 ladder: 24 / 32 / 48 per side |
| Grid track floor | 768 | Catalogue floor above, phone floor below |

**No horizontal overflow at any width, including 320.** Document scroll width
equals the layout viewport width at 320, 336, 344, 352, 360, 375, 390, 430,
768, 900, 1024, 1180, 1256, 1280, 1440, 1600 and 1920.

---

## 9. Accessibility

| Requirement | Result |
|---|---|
| **SC 1.3.1** Heading order | Measured on the rendered home page: **1 h1, 2 h2, 7 h3, no skipped levels.** The card's heading level follows whether its section renders an h2, so clearing the heading setting cannot create a jump |
| **SC 1.4.3** Contrast | **14 text roles across both bands, all pass, verified two ways** — computed from the tokens and sampled from the rendered pixels. Worst figure: the compare-at price at 5.97:1 against a 4.5:1 requirement. Every other role is 13–17:1 |
| **SC 1.4.11** Non-text contrast | Focus ring 17.04:1 on cream, 11.01:1 on ink |
| **SC 1.4.10** Reflow | No horizontal scroll at 320px |
| **SC 2.4.3** Focus order | DOM order throughout; **0 positive `tabindex` anywhere on the page** |
| **SC 2.4.7** Focus visible | Ring around the whole card, both surfaces, captured and measured |
| **SC 2.5.8** Target size | Every interactive element in both bands measured: smallest is the View all button at 250 × 50. **0 under 24 × 24** |
| **SC 1.4.1** Use of colour | Sold out is text; the sale is two labelled prices; swatch colours are named in hidden text |
| **SC 1.1.1** Non-text content | Alt from the image object, de-duplicated against the title; badge and swatch dots `aria-hidden` |
| **Reduced motion** | Verified by rendering with `prefers-reduced-motion: reduce` emulated: transition duration collapses to 0.001s and `--hover-image-scale` resolves to 1 |
| **Pointer-only affordances** | None. Every hover rule in both new stylesheets is gated on `(hover: hover) and (pointer: fine)`, so nothing is revealed on hover and nothing sticks after a touch tap |
| **Keyboard** | Every product reachable; the card is one tab stop; the optional quick-add form is a real form |

---

## 10. Performance

**What the two bands add:** two stylesheets and one image per product. No
JavaScript.

| Resource | Raw | gzip | Stripped of comments |
|---|---|---|---|
| `component-product-card.css` | 12,498 B | 4,432 B | 4,364 B |
| `section-featured-collection.css` | 6,151 B | 2,251 B | 2,978 B |
| `component-button.css` | 7,576 B | 2,751 B | 2,520 B |
| JavaScript | **0** | — | — |

An unconfigured section costs **nothing at all** — the stylesheet links are
emitted inside the render guard.

### Responsive images

Every card image carries an explicit `widths` ladder (180 → 1200) and a `sizes`
attribute the **section** computes, because the section is what knows the grid.

The `sizes` value is exact, not conservative. The first version divided each row
by the *requested* column count, which under-declared the slot by 25–32%
wherever the track floor had dropped a column — the browser then fetched a
candidate it had to upscale. The section now computes the viewport at which the
requested count first fits and emits an extra clause below it, because between
a tier's minimum width and that threshold the rendered count is exactly one
lower. Verified against the rendered grid at twelve widths:

| Viewport | New Drop painted / declared | Best Sellers painted / declared |
|---|---|---|
| 375 | 147.5 / 147.5 | 147.5 / 147.5 |
| 768 | 336.0 / 336.0 | 336.0 / 336.0 |
| 1024 | 300.5 / 309.7 | 288.0 / 288.0 |
| 1280 | 395.6 / 402.8 | 272.0 / 272.0 |
| 1440 | 296.7 / 296.0 | 312.0 / 312.0 |

**Zero clauses under-declare.** The largest over-declaration is 9px (3%).

### Loading

`loading="lazy"` and `decoding="async"` on every card image. Both bands sit
below the hero, which is the home page's LCP element, so eager-loading the
first row would compete with it for bandwidth. The card accepts an `eager`
parameter for a future collection template whose first row is above the fold.
No `fetchpriority` is emitted: `auto` is the default and only the hero needs
`high`.

---

## 11. Testing Performed

### Method

The theme's **real `.liquid` files** are rendered — not a hand-written mock. A
small strict Liquid interpreter was written for this QA
(`scratchpad/phase6/miniliquid.py`, ~600 lines) which raises on an unknown tag,
filter or syntax rather than rendering empty, and `build.py` drives it against
mock Shopify data to produce 15 static pages. The mock data lives only in the
scratchpad; nothing in the theme knows about it.

Pages are then captured through an iframe wrapper at exact CSS widths and
cropped — headless Edge's `--screenshot` never matches `--window-size`, which
Phase 5 established and this phase re-used.

### Two measurement mistakes, corrected

Recorded because both produced confident wrong answers before they were caught.

1. **The harness swallowed the swatch row.** `break` inside a `for` discarded
   the text rendered before it, so swatches looked absent when the Liquid was
   correct. The interpreter was fixed to carry the partial output, as Liquid
   does.
2. **The portrait ratio test never tested the portrait ratio.** The harness
   injected the override outside any rule block, so it was discarded and the
   page rendered square — a false pass on the only evidence for
   `product_image_ratio`. Found by the review, fixed, and re-measured: the
   media box now reports `aspect-ratio: 4 / 5` and 312 × 390.

### Adversarial review

A seven-dimension review ran over the phase — Shopify API correctness against
shopify.dev, Phase 2 compliance, accessibility, Phase 1 issue closure, brief
compliance, CSS correctness, and regression on Phases 4 and 5 — with **two
independent skeptics per finding, each instructed to refute it**.

**30 findings raised, 20 survived, 10 refuted.** All 20 are fixed or recorded
below. The 10 refuted are not acted on; they include the claim that
`section.shopify_attributes` is a Phase 6 defect (it is a Phase 5 no-op), that
RESP-03's orphan tile is a code defect (it is a product-count consequence), and
that the Best Sellers preset copy is invented store data (it is placeholder
copy from the brief, which a merchant edits).

The most valuable finding was the `sizes` defect in §10 — confirmed
independently by six verifiers, three of whom reproduced it in a real browser.

### The brief's 20-case matrix

| # | Case | Evidence |
|---|---|---|
| 1 | No collection selected | `case-nocollection-live.html` renders zero markup; `case-nocollection-editor.html` renders the note |
| 2 | Collection with products | `index.html`, both bands |
| 3 | One product | `case-count-1.html` |
| 4 | Two products | `case-count-2.html` |
| 5 | Many products | `case-count-12.html` |
| 6 | Product with one image | `case-states.html`, hoodie and cap |
| 7 | Product with multiple images | `case-states.html`, tee (second image present, deliberately unused — see §12) |
| 8 | Product with variants | `case-states.html`, tee and hoodie |
| 9 | Product without variants | `case-states.html`, "One Variant Piece" |
| 10 | Sold out | `case-states.html`, cap — badge, dimmed media, accessible name |
| 11 | On sale | `case-states.html`, hoodie — ₱2,490.00 with ₱2,990.00 struck |
| 12 | No compare-at price | `case-states.html`, tee |
| 13 | Long product title | `case-states.html` — clamped to two lines, price still aligned |
| 14 | Missing product image | `case-states.html` — bare tile ground, no placeholder |
| 15 | Missing collection image | The section never renders a collection image |
| 16 | Mobile layout | 320, 375, 390, 430 captured; grid ladder measured at 17 widths |
| 17 | Keyboard navigation | Tab order enumerated; 0 positive tabindex; focus ring captured on both surfaces |
| 18 | Reduced motion | Rendered with the media feature emulated |
| 19 | Theme Editor settings | Every setting exercised; all 19 validated against the schema; both presets validated |
| 20 | View All link | Rendered on both bands, pointing at `collection.url` |

### Structural validation

85 automated checks, re-runnable, **all passing**: JSON and schema parse,
template wiring, preset validity, no invented store data, markup contract,
token fidelity (0 undefined properties, 0 raw hex, 0 `!important`, 0
palette-layer reaches), stylesheet loading, button promotion correctness,
translation keys (0 missing, 0 unused), theme settings, and the 44 original
files unmodified.

---

## 12. Known Limitations

1. **The theme had no `body { margin: 0 }`, and now does.** Found by measuring:
   every band came out 16px narrower than the viewport at every width, so
   Phase 2 §8's full-bleed container model never actually reached the viewport
   edge — the hero photograph, the header scrim and both new bands all carried
   an 8px strip of page background down each side. Phase 5's harness set the
   reset in its own styles, which is why it was not caught then. **Fixed** in
   both token files. It changes the rendering of every previously-built
   section, all for the better, but it is a change to Phase 2's file and should
   be confirmed.

2. **Six invisible tab stops on phones — a Phase 4 defect, not fixed here.**
   `.header__panel` is `display: flex`, which outranks the user agent's
   `[hidden] { display: none }`, so the closed mobile menu's close button and
   five links stay in the tab order at x = −313. Measured: **7 outside-viewport
   tab stops at 375px, 1 at 1440px** (the skip link, which is correct). A
   keyboard user on a phone passes six invisible stops before reaching page
   content — WCAG 2.2 SC 2.4.11 and SC 2.4.3.
   **The one-line fix is `.header__panel[hidden] { visibility: hidden; }`** —
   `visibility`, not `display`, so the close transition still runs. It is not
   applied because the brief says not to modify the header unless collection
   links require it, and they do not. **This needs your decision.**

3. **`section.shopify_attributes` does not exist.** `sections/hero.liquid` uses
   it and gets an empty string. Harmless, but `PHASE-5-HERO.md` §10 presents it
   as a working Theme Editor hook and its validator asserts its presence. Both
   should be corrected when Phase 5's document is next touched.

4. **`PHASE-5-HERO.md` byte figures are now stale.** `section-hero.css` lost
   the button block, so every size in its §10, §13 and file-change report is
   out of date, as is its §16 item 1 (the promotion it asked for is done).

5. **`config/settings_schema.json` fails `shopify theme check`** on two
   pre-existing Phase 4 lines: `theme_documentation_url` and
   `theme_support_url` are empty strings, which Shopify's schema rejects as
   non-URIs. Real URLs are `BUSINESS INFORMATION REQUIRED`; inventing one is
   forbidden, so they are left and recorded.

6. **Second-image-on-hover is not implemented.** Phase 2 §22.4 does not define
   it and §14.3 warns that a partial set — some products with a back
   photograph, some without — makes the grid look broken. The brief permits
   either the image swap or the subtle scale; the scale is implemented.

7. **UI-02 is only partly closed.** The card now has a fixed ratio and is
   reusable, which is what the issue asked for structurally. But the product
   photographs' own off-white boxes remain visible against the `#EBE6DC` tile
   ground, which is the visual half of UI-02. That needs transparent or
   tonally-consistent masters — a sourcing problem, not a code one.

8. **Centre and right text alignment are not offered** by this section, and the
   `--split-30-70` rail is fixed. Neither was asked for.

9. **No collection is selected in `templates/index.json`.** Both rows render
   nothing until a merchant picks one. This is correct — `BUSINESS INFORMATION
   REQUIRED` — but it means the shipped home page is hero-only until §13 is
   done.

10. **The mini-Liquid interpreter is evidence, not proof.** It renders the real
    files and catches real mistakes, but it is not Shopify. Everything in §4
    that depends on Shopify's own behaviour was checked against shopify.dev by
    the review rather than assumed, and the theme still needs one run against a
    real development store.

---

## 13. Shopify Setup Instructions

Nothing in this phase works until a merchant does these in Shopify admin. None
of it can be done from the theme.

**1. Create the collections.**
Products → Collections → Create collection.
- One for the drop — the brief calls it **The Faithful**. Manual or automated.
- One for **Best Sellers**. Make it an automated collection, or a manual one,
  and set its **sort order to "Best selling"** so Shopify decides the ranking.
  *The theme never decides what sells; this setting is where that comes from.*

**2. Add products**, with for each: a title, a price, at least one image, and
a compare-at price only where the product genuinely is reduced.

**3. Configure colour swatches**, if the catalogue has colourways.
Settings → Custom data → Products, or the product's Colour option → assign a
colour or an image to each option value. **Swatches render only where this is
configured** — the theme will not guess a colour from a name or an image, so an
unconfigured option simply shows no dots.

**4. Point the sections at the collections.**
Online Store → Themes → Customise → Home page.
- The **New Drop** row → Collection → The Faithful.
- The **Best Sellers** row → Collection → Best Sellers.
Until this is done both rows are invisible on the live store and show a note in
the editor.

**5. Set the product image shape**, if 1:1 is not wanted.
Theme settings → Products → Product image shape → Portrait (4:5). It applies to
the whole catalogue, by design.

**6. Optionally set the View all destinations.** Leave them blank and each
button points at its own collection, which is usually what you want.

**7. Check the hero's CTA.** Phase 5 left `button_link` empty pending a
collection URL. Once The Faithful exists, setting it turns the hero's
"Shop The Collection" button on and closes Phase 1 HERO-01.

---

## Phase 1 Issues Assigned To This Phase

All eleven, honestly assessed:

| ID | Pri | Status |
|---|---|---|
| **DATA-01** Product catalogue | P1 | **CLOSED.** Every field comes from the Shopify product object; nothing is a literal |
| **DATA-02** Price and currency | P1 | **CLOSED.** `money` filter against the store's format; the symbol-only enum is gone |
| **HTML-03** Heading hierarchy | P1 | **CLOSED.** Product titles are headings, the level adapts, one h1 per template. Measured: 1 h1, 2 h2, 7 h3, no skips |
| **UX-02** Best Sellers step | P2 | **CLOSED.** The step exists, collection-driven, reusing the same card |
| **COLL-03** Merchandising model | P2 | **CLOSED.** Drops are collections bound to a collection picker; the drop updates without editing code |
| **DATA-03** Colour swatches | P2 | **CLOSED for the card.** Driven by native Shopify swatch data with real colourway names. Variant *selection* is Phase 8 |
| **UI-02** Card media treatment | P2 | **PARTLY CLOSED.** Fixed ratio, tile ground, two-line clamp, hover and link states all done. The visible box edges around the product photographs need better masters — see §12 item 7 |
| **RESP-03** Tablet grid orphan | P3 | **NOT CLOSED, by design.** Three products cannot fill a two-column row. The grid ladder is Phase 2 §9.3's, the trade-off is now surfaced in the editor, and a four-product collection or the full-width layout resolves it |
| **COLL-01** Collection page | P1 | **OUT OF SCOPE.** The brief excludes collection page templates |
| **COLL-02** Collection index | P2 | **OUT OF SCOPE**, and `BUSINESS INFORMATION REQUIRED` — the taxonomy is undefined |
| **ECOM-06** Filters and sorting | P2 | **OUT OF SCOPE.** The brief excludes both explicitly |

Six closed, one partly, one deliberately not, three out of scope.

---

## File Change Report

**CREATED (7)** — `sections/featured-collection.liquid`,
`snippets/product-card.liquid`, `snippets/icon-arrow.liquid`,
`assets/component-product-card.css`, `assets/section-featured-collection.css`,
`assets/component-button.css`, `PHASE-6-COLLECTIONS-BEST-SELLERS.md`

**MODIFIED (8)** — `assets/section-hero.css`, `layout/theme.liquid`,
`assets/design-tokens.css`, `PHASE-2-DESIGN-TOKENS.css`,
`config/settings_schema.json`, `config/settings_data.json`,
`templates/index.json`, `locales/en.default.json`

**DELETED (0).** 44 tracked originals re-hashed, all unmodified.

```
layout/theme.liquid                       4,596 B
sections/announcement-bar.liquid          4,008 B
sections/featured-collection.liquid      19,478 B   ← new
sections/header-group.json                  893 B
sections/header.liquid                   10,342 B
sections/hero.liquid                     12,145 B
snippets/icon-account.liquid                708 B
snippets/icon-arrow.liquid                1,068 B   ← new
snippets/icon-cart.liquid                   856 B
snippets/icon-close.liquid                  759 B
snippets/icon-menu.liquid                   795 B
snippets/icon-search.liquid                 772 B
snippets/product-card.liquid             11,394 B   ← new
assets/component-button.css               7,576 B   ← new
assets/component-product-card.css        12,498 B   ← new
assets/design-tokens.css                 25,610 B
assets/header.css                        11,404 B
assets/header.js                          6,302 B
assets/section-featured-collection.css    6,151 B   ← new
assets/section-hero.css                  14,293 B
config/settings_data.json                   609 B
config/settings_schema.json               3,305 B
locales/en.default.json                     974 B
templates/index.json                      1,925 B
                                        ──────────
TOTAL                                   158,461 B   24 files
```
