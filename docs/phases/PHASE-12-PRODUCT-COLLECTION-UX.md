# GOD SQUAD — PHASE 12: PRODUCT + COLLECTION + CATALOG UX

Phase 12 deliverable. Built against the Phase 12 brief as issued, `PHASE-2-DESIGN-SYSTEM.md` §13
(the card), §22.4 (hover), §27 (the five ecommerce questions), and the catalog surfaces delivered in
Phases 6, 8, 9, 10 and 11.

Status: **delivered**. **508 automated assertions pass**, across twelve rendered pages at twelve
viewports each, with no console error on any of thirty-four pages.

A nine-cluster audit itemised the brief into 104 checkable requirements and found **91 already
passing**. Phase 12 is a correction phase, not a construction phase: every defect it found was a few
lines, none was architectural, and none needed a new component or dependency.

---

## 1. Product card architecture

`snippets/product-card.liquid` remains the **single** card. Three call sites — featured-collection,
main-collection, main-search — one snippet, zero page-scoped CSS overrides. No second card was
created, and none should be.

Its contract was already right and is unchanged: one anchor wrapping the media and the title with no
other interactive element inside it, swatches and price outside it, the focus ring drawn around the
whole card by a `:focus-within` rule, a real heading at a caller-chosen level, and every value read
from the Shopify product object.

### 1.1 The secondary image

The brief's one clearly-absent feature. It is now supported, in pure CSS, with no JavaScript.

Both images occupy the same `aspect-ratio` box, so the swap cannot shift anything — the height was
reserved before either arrived. The reveal rule lives **inside**
`@media (hover: hover) and (pointer: fine)`, so a touch device has no state in which it can appear.
The fade is an opacity transition, which `base.css`'s global reduced-motion rule collapses to 1ms:
the swap still happens, it simply does not animate.

It picks **the first image that is not the featured one**, not `images[1]`. A merchant can promote
any image to featured in Shopify admin without reordering the others, and `images[1]` would then be
the same picture the card is already showing.

**It is off by default, and that is a decision rather than an oversight.** Phase 2 §22.4 specifies
the approved card hover as a 1.03 image lift plus a title underline reveal — nothing else. Turning a
swap on by default would change the approved hover on every store, which this brief's CORE PRINCIPLE
forbids. The brief says *allow* a secondary image; it is allowed, not imposed. One global setting,
in Products beside the image ratio, for the reason Phase 10 made that global: a card that swaps on
one row of a shop and not another is a bug, not a choice.

### 1.2 The defect that shipped with it

`.product-card--sold-out .product-card__image` is specificity (0,2,0). The rule hiding the secondary
image, `.product-card__image--secondary { opacity: 0 }`, is (0,1,0) — and the secondary `<img>`
carries **both** classes. The higher-specificity rule won, so a sold-out product with two photos
painted both images superimposed at 60%, **on every device including touch**, because the rule doing
the hiding was the one that lost.

The stylesheet's own comment claimed "a phone has no state in which it can appear at all". It was
false, and it has been corrected along with the CSS.

The fix is `:not(.product-card__image--secondary)` on the dim, plus a rule that dims the secondary
*when it is revealed* on a sold-out card, so a hover cannot make an unavailable product look more
available.

**The first test of this passed.** It asserted the rule *contained* `opacity: 0`. String-matching CSS
cannot verify the cascade — only a browser can answer which rule won. See §18.

---

## 2. Product grid architecture

One `gap` on the grid, no per-card margins, no page-scoped overrides. Column counts arrive as scoped
custom properties rather than inline styles, so Phase 6's "settings are ceilings" semantics survive:
the grid is `auto-fill` with a floor, and the setting is the most it will paint.

The shipped ladder is 4 / 2 / 2, matching the brief's baseline. featured-collection's copy-column
preset uses 3, which is the approved Phase 6 value the brief explicitly defers to.

### 2.1 `snippets/grid-sizes.liquid`

**New.** The `sizes` derivation is now one snippet shared by `main-collection` and `main-search`.

It was three copies of the same ninety lines. Phase 10 found that the desktop clause fired below its
own breakpoint, booked it as a **blocker**, and fixed it in one copy. The other two carried the bug
for two more phases, because the fix was applied to an instance rather than to the rule. Measured:
`main-search` at three columns still emitted `(min-width: 976px)` — below the 1024px breakpoint where
the desktop column count takes effect — so between 976 and 1023 it declared a slot narrower than the
one that paints.

The snippet encodes two rules, both learned the hard way:

1. **A clause may not claim a width before the layout that produces it applies.** The desktop
   threshold is floored at 1024.
2. **A clause may not divide by more columns than actually fit.** At the container cap the row stops
   growing, but the grid is auto-fill with a 272px floor. With the shipped maximum of four columns
   and the container narrowed to its 1200px minimum, dividing by the requested four declared **253px
   for a track that paints 346px** — a 27% under-declaration, reachable with default columns.

Both errors ran in the same direction: under-declaring, which is the direction that costs image
quality.

**`featured-collection` is deliberately not consolidated.** Its copy-column layout scales the needed
row by 1000/727 because the grid occupies only 72.7% of it, so its derivation is genuinely different
rather than duplicated. It received both corrections in place.

Verified by capturing the `sizes` string across 21 configurations before and after: **13 byte-identical**,
and every change moves the declaration *up*.

---

## 3. Collection architecture

`sections/main-collection.liquid` + `templates/collection.json`. Real `collection.title`,
`collection.description`, collection image and product count; a GET sort form that works with
JavaScript off; `{% paginate %}`; and a real empty state.

### 3.1 A populated collection could announce itself as empty

The grid/empty split was keyed on `collection.products.size` **inside** the paginate block — where
`collection.products` is the *page slice*. An out-of-range `?page=`, which Shopify answers with a 200
and an empty slice rather than a 404, printed "This collection is empty." over a collection that has
products.

It now tests `paginate.items`, which is the size of the set actually being paginated. The section
already used `paginate.items` correctly for the product count, with a comment explaining exactly
why — the empty test simply had not followed the section's own reasoning.

### 3.2 Page size

`products_per_page` defaults to **24** and stays there. The brief's 12/16 baseline defers to
"existing design", and 24 divides evenly into 4, 3 and 2 columns, so no tier ends on a ragged row.

---

## 4. Product page architecture

Exactly one `<h1>`, and it is `product.title` — verified across all seven templates. The description
is rendered by Liquid and never touched by JavaScript. Accordions are native `<details>`. Sticky info
cannot cover content and is off below 1024px.

`{{ product | structured_data }}` is emitted **once**, theme-wide.

---

## 5. Variant architecture

The hard parts were already right and are unchanged: availability is re-derived against the real
variant table rather than trusting `product_option_value.available`; the unavailable note shares one
server-rendered hook so a screen reader does not hear "Small, Unavailable, Unavailable"; and three
independent guards stop a wrong variant reaching `/cart/add`.

Phase 12 corrected three things.

**The SKU row could never appear for a later variant.** It was gated on the render-time variant's
SKU, so when the first variant had none the markup was absent — and `product.js` updates the SKU by
querying `[data-variant-sku]`, so a hook that was never rendered could never be filled. It now
renders if **any** variant carries a SKU, and hides itself when the selected variant has none,
because a `<dt>SKU</dt>` standing over an empty `<dd>` is a labelled row that says nothing.

**"Sold out" was being said about products that never existed.** `updateButton` was two-way:
`buyable = !!(variant && variant.available)`, so a **null** variant — an option combination that was
never manufactured — fell through to the sold-out label. That tells the customer something false:
that it existed and ran out, so it might come back. The button now carries a third
`data-label-unavailable`, and the locale already had `products.variants.unavailable`.

**The unit price is documented as variant-driven.** It is rendered from the variant the page opened
on; a per-litre price left over from a different size would be worse than none.

---

## 6. Cart integration

Shopify's cart only. The add path applies section renders *before* testing `result.ok`, so a 422
partial add is still reflected; double submission is guarded with `aria-busy` rather than `disabled`,
because disabling the focused element blurs it.

**The quick-add form was invisible to the cart script.** It posted correctly — `cart.js` finds the
button through its `[type="submit"]` fallback — but it had no `[data-add-to-cart-label]` to write
"Adding…" into and no `[data-cart-error]` to put a failure in. A failed quick add reached the
layout's live region, so a screen-reader user heard it while a sighted customer saw the card sit
there unchanged. All three hooks are now present, and its error line joins the **shared** error
treatment used by the drawer and the cart page rather than inventing a third look.

Quick-add remains **off in every shipped configuration**, and a multi-variant product still gets a
link to its page rather than a silent default-variant add.

---

## 7. Inventory handling

**New in Phase 12: a "Low stock" line, on the product page only.**

The brief permits In stock / Low stock / Sold out, forbids inventing them, and forbids exposing exact
numbers "unless the merchant explicitly wants that functionality". So:

- **The comparison happens in Liquid, server-side. Only a boolean reaches the page.**
  `variant.inventory_quantity` is public on the storefront, and Phase 8 built the variant table
  field-by-field precisely to keep it out of the source. That decision stands: the table now carries
  `"low_stock": true|false` and no figure.
- **Two guards**, because the number alone does not mean what it looks like.
  `inventory_management == 'shopify'` — an untracked variant reports 0 forever.
  `inventory_policy == 'deny'` — a continue-selling variant is never low, it is unlimited.
- **The threshold is a merchant setting, set to 3** by the brand owner. It shipped at 0 — showing
  nothing — until that decision was made, because a threshold nobody has chosen is a claim nobody has
  made. It is set in both places it can come from: the schema default, which governs a section added
  fresh in the Theme Editor, and `templates/product.json`, which governs the shipped product page.
  0 still disables the line entirely.
- **Product page only.** Repeated down a grid, "Low stock" stops being information and becomes
  urgency marketing, which Phase 1 §29.8 and the CORE PRINCIPLE both rule out.

No permanent "In stock" line: the enabled "Add to bag" button already says it.

The six-case matrix in §16 proves each guard, including that no inventory figure reaches the page.

---

## 8. Product media

Unchanged from Phase 8. Images, video, external video and 3D all render; the gallery works with
JavaScript off and improves with it on; mobile navigation is never hover-dependent.

**No zoom was added.** The brief is explicit — "only if already established... do not add an
elaborate zoom system in this phase." None exists. A zoom layer would add a modal, a focus trap and a
second media request per product.

---

## 9. Pricing

Every price goes through the money filter against the store's own format. No currency symbol is
hardcoded anywhere in the theme — verified by grep for `₱`, `PHP`, `USD` and `$<digit>`, which hits
only comment prose.

Compare-at pricing renders only when a valid compare-at exists, and is suppressed when the price
varies: a range beside a strike-through is not information. The sale state also carries
visually-hidden "Sale price" / "Regular price" labels, which most themes omit.

---

## 10. Badges

The card ships **one** badge, SOLD OUT, from `product.available` — real data, real text, never colour
alone, inside the link's accessible name.

**No SALE badge and no NEW badge, by decision.** Phase 2 §13.4 allows the card a single badge slot
and records the badge vocabulary as BUSINESS INFORMATION REQUIRED.

- **SALE** has an obvious real source, but the question it answers is already answered twice — by the
  struck compare-at price and by those screen-reader labels. A second badge would compete for the one
  slot or require a second, which is a redesign.
- **NEW** has no honest native source. `published_at` resets on re-publishing, unhiding, an import or
  a store migration, so a date-based badge would eventually lie about every product at once. The only
  defensible mechanism is a merchant-set **tag name**, default empty, with SOLD OUT always winning the
  slot — pre-approved by this document, about half a day, and blocked on the brand owner deciding what
  a badge means.

---

## 11. Empty states

Every one is graceful and none invents content: a collection with no products, a sold-out product, an
unavailable variant, a product with no image (the tile ground still renders so the grid keeps its
rhythm, and nothing stands in for a photograph that does not exist), and a collection with no image.

---

## 12. Pagination

Shopify's `{% paginate %}`, with accessible previous/next, current-page semantics, and a presentation
that does not dominate the page.

---

## 13. Accessibility

Focus handling is the strongest thing in this theme — three surfaces, three different correct
answers: `:has()` on the card, `:has()` on the quantity box to avoid concentric rings, and
ring-on-label for the visually-hidden radio, each with the failure it avoids written down.

Quantity controls have real `<label for>` and "Increase quantity for {title}" rather than "+".
`min`/`max`/`step` come only from `quantity_rule`. The sold-out state is text, never colour alone.

Phase 9's floor holds across the catalog: **zero targets under 24px at any tested viewport.**

---

## 14. SEO

`{{ product | structured_data }}`, emitted exactly once, produced by Shopify's own filter rather than
hand-built — which is what keeps every price, currency, availability URL and per-variant identifier
derived from real data, and what makes a fabricated rating impossible: the filter does not emit one
and no review data exists.

Canonical lives in the layout only. Exactly one `<h1>` per template.

**Not verified:** whether `page_description` falls back to the product body on a real store. It must
be checked on a development store, and a description must **not** be synthesised — a generated
sentence about a garment nobody on this project has seen is invented product copy.

---

## 15. Performance

Lazy/eager discipline is exemplary and unchanged: exactly one non-lazy image per page, and the LCP
tile on a collection page is identified by counting emitted tiles rather than `forloop.first` —
`main-search` documents why that test is wrong there. On the home page no card is eager, correctly,
because the hero is the LCP and carries `fetchpriority="high"`.

The secondary image is **always** lazy: it is never an LCP candidate. Its cost is one additional
image request per multi-photo card, which is why it is off by default.

The `sizes` corrections in §2.1 are performance fixes: an under-declared slot makes the browser fetch
a candidate it then has to upscale.

---

## 16. Mobile QA

375 / 390 / 430, plus 480, 768, 834, 1024, 1280, 1440, 1920 and two landscape cases, across twelve
pages. **Zero horizontal overflow, zero sub-24px targets.**

The low-stock matrix, rendered:

| Case | Result |
|---|---|
| tracked, cannot oversell, 2 left, threshold 3 | **Low stock** |
| tracked, 3 left, on the shipped default | **Low stock** |
| tracked, 4 left, on the shipped default | silent |
| tracked, cannot oversell, 10 left, threshold 3 | silent |
| not tracked by Shopify, 2 left | silent |
| continue-selling, 2 left | silent |
| tracked, 2 left, threshold 0 | silent |
| tracked, 0 left and unavailable | silent |

---

## 17. Desktop QA

1280 / 1440 / 1920. The container cap is wired to `settings.container_width` through one custom
property, so the CSS cap and the Liquid `sizes` cap cannot disagree.

---

## 18. Theme Editor QA

Phase 11's behaviour is intact: `editor.py` still passes 10/10, including the listener accounting and
the scroll-lock release.

### The test that could not see the bug

`catalog.py` renders the card and asserts on its markup. That cannot see the cascade — it confirmed
the secondary image's rule *said* `opacity: 0` while a higher-specificity rule was quietly repainting
it to 0.6.

`cardcascade.py` is new and measures **computed styles in a browser**. The fixture that exposes the
defect does not exist in the shipped set — a sold-out product with two images — so it is composed
from `P_MULTI` by marking its variants unavailable. Nothing is invented; the fields are the ones
Shopify itself sets.

Negative-controlled: without the fix the sold-out secondary computes to `0.6`; with it, `0`.

**Its own first run reported 900px stacked images.** Not a subtle wrong number — the shape of *no
stylesheet*. The card's CSS is linked by the **sections** that use the card, not by the snippet, and
the probe was rendering the snippet bare. The same trap Phase 10 hit with unstyled surfaces.

---

## 19. Files changed

**Created**
| File | Purpose |
|---|---|
| `snippets/grid-sizes.liquid` | The shared `sizes` derivation |

**Modified**
| File | Change |
|---|---|
| `snippets/product-card.liquid` | Secondary image; quick-add cart hooks |
| `assets/component-product-card.css` | The swap; the sold-out cascade fix |
| `assets/component-cart-line.css` | The card error joins the shared error treatment |
| `sections/main-collection.liquid` | Empty state tests `paginate.items`; uses the snippet |
| `sections/main-search.liquid` | Uses the snippet (gains the 1024 floor) |
| `sections/featured-collection.liquid` | Both `sizes` corrections, in place |
| `sections/main-product.liquid` | SKU row; Unavailable label; low stock |
| `assets/product.js` | Three-way button state; SKU row; low stock |
| `assets/section-main-product.css` | The Low stock line |
| `config/settings_schema.json` | `card_hover_secondary_image` |
| `config/settings_data.json` | Its default |
| `locales/en.default.json` | `products.inventory.low_stock` |

---

## 20. Known limitations

**No real Shopify store.** Everything is measured against mock data through a strict mini-Liquid
interpreter and headless Edge. `{{ product | structured_data }}`'s real output has never been seen.

**Theme Check has never been run** — no Shopify CLI in this environment. What is checked mechanically
is listed in `PHASE-11-THEME-EDITOR.md` §13, plus every `{% schema %}` parsing on every run.

**`page_description` on a product page is unverified.** §14.

**The out-of-range `?page=` fix is verified at source level, not by rendering one.** The harness's
`{% paginate %}` always serves page 1, so the empty slice cannot be simulated. The assertion checks
that the branch tests `paginate.items` and no longer tests the page slice.

**No badge vocabulary.** §10. Blocked on Phase 2 §13.4.

**No size guide, no materials, no care instructions.** Blocked on ECOM-04 — there is no approved
copy, and inventing it is forbidden. Recording it as a future requirement *is* the deliverable the
brief asks for.

**`featured-collection` still carries its own `sizes` derivation.** Deliberate — §2.1 — but it means
a future change to the shared rules must be applied there too.

---

## 21. Future recommendations

1. **Run Theme Check** against a development store, and verify `page_description` and the real
   structured-data output.
2. **Decide the badge vocabulary** (Phase 2 §13.4). If NEW is wanted, the tag-setting mechanism in
   §10 is pre-approved.
3. **A size guide**, once approved copy exists. The product page already has the accordion pattern.
4. **Consider consolidating `featured-collection`'s derivation** into `grid-sizes.liquid` with a row
   fraction parameter, with its own re-measurement.
5. **Review the low-stock threshold** once real stock levels exist. It is set to 3; whether that
   reads as scarce depends on the size run a garment actually carries.

---

## Appendix — verification

| Suite | Covers | Result |
|---|---|---|
| `validate.py` | Structure, schemas, tokens, translations, data discipline | 198 / 198 |
| `interact.py` | Cart drawer in a real browser | 49 / 49 |
| `interact_cartpage.py` | Cart page | 17 / 17 |
| `interact_product.py` | Product page | 26 / 26 |
| `contrast8.py` | Measured contrast on rendered pixels | 56 / 56 |
| `layout.py` | The real `layout/theme.liquid`, parsed | 19 / 19 |
| `surfaces.py` | The five Phase 10 surfaces in every state | 41 / 41 |
| `editor.py` | Section load/unload lifecycle | 10 / 10 |
| `settings.py` | Every Phase 11 setting, rendered both ways | 28 / 28 |
| **`catalog.py`** | **New.** Card, SKU, quick-add, low stock, the collection empty test | 54 / 54 |
| **`cardcascade.py`** | **New.** Computed card styles in a browser | 10 / 10 |
| `respond.py` | 12 pages × 12 viewports | 0 overflow, 0 sub-24px targets |
| `console.py` | Console and Liquid errors | 0 across 34 pages |

**508 assertions.**

Two method notes worth carrying forward. A `sizes` baseline was captured across 21 configurations
*before* the refactor and diffed after, which is how a malformed output — caused by single-line
`comment … endcomment` statements inside a `{% liquid %}` block, where every line is its own
statement — was caught immediately. And a comment containing a tag delimiter will terminate the tag
that encloses it: the enclosing `{% liquid %}` block ended at the `%}` inside the prose.

Phase 12 stops here.
