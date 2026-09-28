# PHASE 18 — FINAL POLISH + AWARD-LEVEL UI/UX QA

**GOD SQUAD — Shopify Online Store 2.0 theme**
**Date:** 2026-09-25
**Theme:** `god-squad-theme/` — 75 files
**Scope:** final visual polish, UX QA, responsive QA, design consistency, regression testing.
**Not in scope, and not done:** redesign, deployment, publishing, domain, payment, advertising, irreversible Admin changes.

---

## Preface: what this phase could not assess

**There is no merchant photography in this project.** Phase 3 recorded sourcing — not processing — as the ceiling, and no merchant photography exists. The QA harness renders six placeholder images copied from the prototype's own folder (`hero.webp`, `tee.webp`, `hoodie.webp`, `cap.webp`, `story.webp`, `logo.png`), which are AI-generated with unconfirmed rights — so the test pages show approximate imagery, not the real thing. The theme itself ships **zero** image files.

Image cropping, focal points, image quality, art direction, and the rhythm of real photography against real copy are the substance of a visual audit. **None of them is assessable in this environment.** Everything in this report audits the *reservation* — the aspect-ratio box, the object-fit, the scrim, the alt-text path — never the picture that will sit in it.

A claim to have reviewed the imagery would be invented, so none is made. The same applies to real-server timings: TTFB, FCP and field LCP/INP are unavailable here and are reported as unavailable rather than estimated.

---

## 1. Visual audit

Two independent passes.

**Measured.** Harnesses render the real `.liquid` files against mock Shopify data and read computed styles from a browser. This produced the coherence table below, the leading measurements, the chevron angles and every spacing figure quoted.

**Reviewed.** Fourteen agents across seven dimensions — typography, spacing, buttons, icons, legacy code, motion/states, copy/brand — each dimension audited by one agent and every finding adversarially verified by a second. **98 confirmed findings**, deduplicating to **70 distinct defects**.

Full table with SECTION / PROBLEM / SEVERITY / RECOMMENDED FIX / STATUS: **`PHASE-18-VISUAL-AUDIT.md`**.

| Outcome | Count |
|---|---:|
| FIXED | 12 (+4 found by measurement) |
| RECORDED — verified, deliberately unchanged | 55 |
| MERCHANT — business/brand decision | 2 |
| REJECTED — finding does not stand | 1 |

**Design coherence, measured.** Every element matching each design role, across 13 built surfaces, grouped by computed signature:

| | Before Phase 18 | After |
|---|---:|---:|
| Roles resolving to ONE signature | 9 of 15 | **10 of 15** |
| Distinct border radii in use | 3 | 3 |
| Distinct box shadows | 1 | 1 |
| Distinct transition durations | 2 | 2 |
| Distinct easing curves | 1 | 1 |

The five roles that still show more than one signature were investigated individually. **No single class renders more than one way** — every remaining difference is between *different components that share a heading tag* (`.product-card__title` and `.our-story__value-title` are both `h3`), which is design, not drift. Verified with `phase18/whichh3.py`.

Two findings the reviewers rated HIGH were **rejected** after checking them against the specification — details in §25 and in the audit document.

---

## 2. Typography

**Fixed.**

- **The label role had no line-height token.** `--type-label-size`, `--type-label-ls` and `--type-label-weight` shipped; leading did not. So every consumer either invented one or inherited `normal`, which for Jost resolves to **1.167**. Measured: the same product name rendered **14.0px per line in the cart against 17.4px on a product card**, and at 375px the current fixture title already wraps to two lines — this was live on phones. Added `--type-label-lh: 1.45` (the value the card had already chosen privately) and applied it to the two label consumers whose text wraps. The 22 single-line consumers are untouched, because `normal` and 1.45 render identically on one line.
- **Empty-state titles were a second page heading.** `.cart-empty__title` and `.main-collection__empty-title` carried the same four type declarations as their own page's `<h1>`, which renders unconditionally above them. Measured: `<h1>` Playfair 40px/900/uppercase, then a `<p>` at **identical** type directly beneath. Taken to the interface-heading row (body family, `--type-h3-size`, 600, sentence case). The search page already did this correctly; all three now agree.
- **H3/H4 family.** `design-tokens.css:170` states the rule in the token file itself — *"Playfair for H1-H2, Jost for H3-H4 (interface headings)"* — and PHASE-2 §6.1 assigns both rows Family = body, Weight = 600, Transform = sentence. Three rules did the opposite. Moved to `--font-body`. This also made the **weight honest**: the display font ships as `playfair_display_n9` with `font_face` and no `font_modify`, so `--weight-semibold` was resolving to the 900 face. Jost 600 *is* registered, so 600 now means 600.
- `.header__wordmark` deliberately left on the display family. A logotype is not an interface heading.

**Recorded, not changed.** The mobile menu panel types its links as Playfair 900 at `--type-h3-size` where PHASE-2 §19.6 specifies the eyebrow triplet, and the footer stacks two link type systems. Both are real. Both would **re-type a primary surface**, which is a visible design change rather than polish — see §25.

---

## 3. Spacing

**Fixed.** The collection page had no rule for `.main-collection__header`, so the distance below it depended on a merchant setting. Measured at 1440: with filters configured the first 44px filter row sat **flush against the description at 0px**; without them the toolbar sat correctly at 40px. Same page, two answers.

The margin was placed on `.main-collection__header`, **not** on `.facets` — below `--bp-md` that element becomes `.facets--drawer`, which is `position: fixed` with `inset-block: 0`, so a top margin there would displace the fixed drawer rather than space the page. It collapses against the toolbar's own top margin, so the unfiltered page is unchanged. Verified 0px → 40px filtered, 40px → 40px unfiltered.

**The `.container` utility.** PHASE-2 §8 specified `.container`, `.container--wide` and `.container--narrow` and the implementation never built them, so **twelve elements across eleven stylesheets each carried a private copy of the same four declarations** — the width of the site defined twelve times. All twelve verified byte-identical with no breakpoint overrides before consolidating. Three narrow-width rules (`.header__search-form`, `.main-page__column`, `.main-search__form`) deliberately **not** swept in: they use a narrow measure with no gutter padding, and `--container--narrow` would give them padding they do not have. The reason is recorded in the component file so the next reader does not "finish the job".

**Recorded.** Eyebrow-to-headline gap differs between hero (16px) and the two content bands (24px); five templates put three different distances under the same `display-m` h1; the footer column gap gets *smaller* as the viewport grows. All verified, all cosmetic, all left for a deliberate decision rather than changed silently.

---

## 4. Header

**Fixed.**

- **The menu scrim faded at the wrong speed.** 250ms against the cart drawer's 400ms, for the identical full-viewport wash, opened from the same header. PHASE-2 §21 assigns the two parts of a drawer different durations on purpose: line 1725 gives the *panel* `--duration-medium`, line 1727 gives the *scrim behind a drawer or modal* `--duration-slow`, and line 1690 states 400ms is for "full-surface changes only". The cart drawer already cited this table correctly; the menu scrim had taken the panel's value.
- **Four ungated hover rules** (announcement link, control, nav link, panel link) — see §15.
- **The mobile menu's current page was marked by colour alone.** It shared one declaration block with `:hover`, which made "the current page" and "a passing cursor" literally the same state. Split apart. The current page now carries an underline as well as colour — the pattern `.footer__link.is-active` already uses under the comment *"so the state is not carried by colour alone"* (SC 1.4.1). Its two siblings both avoided colour-only; the panel was the only navigation that did not.

---

## 5. Navigation

Navigation destinations continue to come from the merchant's Shopify menu (`linklists`), never from the theme — verified by `phase16/refs.py`, which also confirms every literal internal `href` is a route Shopify serves.

The mobile panel is the only navigation below `--bp-lg`, which is why its two defects above were treated as header-critical rather than cosmetic. Its **type** remains an open decision (§25).

Skip link, focus order and the panel's tab order are unchanged from Phase 4/9 and still pass.

---

## 6. Hero

No visual change. The hero's schema `info` string was rewritten: it told the merchant *"The approved hero. Phase 3 records its provenance as AI-generated and unverified; confirm before launch."* — project vocabulary in the merchant's Theme Editor. It now reads as the instruction it needs to be: the supplied image is AI-generated with unconfirmed rights, replace it with your own photography or confirm you are cleared to use it, **before launch**. The substance was kept precisely because it matters.

Recorded, not changed: the hero CTA is the only band-level call to action without the trailing `icon-arrow`, and the hero eyebrow is title-cased where the band below it is sentence-cased.

---

## 7. Collections

**Fixed:** the 0px/40px spacing contradiction (§3); the collection description's rich-text link now has a hover like its counterparts (§15); the empty-state title is no longer a second `<h1>` (§2); the paginator is now shared (§8).

Grid column settings remain ceilings, not fixed counts — unchanged from Phase 6. Measured geometry after the container consolidation is **pixel-identical** to Phase 13: 2 columns / 156px / 16px gap at 375, 4 / 312 / 32 at 1440.

---

## 8. Best Sellers / Featured collection

No visual change. The section lost its private container declarations to the shared `.container` utility, with geometry verified unchanged (homepage 3 columns / 297px / 32px gap at 1440 and 1920, 2 / 156 / 16 at 375 — matching Phase 13 exactly).

**The paginator, which had been built twice.** `main-collection` and `main-search` each had their own, under their own class names, in their own stylesheet — and the two had already drifted where a customer could see it: caption type against tracked uppercase label type; a weight-plus-rule current-page marker against a gold one. `section-main-collection.css` had stated its own promotion rule in writing — *"the moment a second surface renders it, the block moves to `assets/component-pagination.css`"* — and the second surface had existed since Phase 13.

Merged into one snippet plus one component stylesheet, taking the better half of each: **type and current-page marker from collection** (gold alone makes the state colour-dependent, SC 1.4.1), **accessibility from search** (the gap's `aria-hidden` belongs on the `<li>`, not the span inside it). That also closed a Phase 16 finding in passing — collection's gap list item was announced as a blank entry and inflated the list count.

---

## 9. Product cards

**Fixed.** `.product-card__error` was defined **twice at equal specificity**, in `component-cart-line.css` and `component-product-card.css`. Later-wins applies *per property*, not wholesale, so the card took margin, font-size and border from its own rule and **padding and line-height from the cart grouping** — rendering boxed, the exact treatment the comment directly above its own rule says it is not.

The card left the cart grouping. A failure inside a 300px tile and a failure across a cart panel are not the same object, and forcing one rule to serve both is what produced a card with 16px of padding on a side it never asked for. Three unreachable `.surface-light` selectors were removed with it — both cart surfaces hardcode `surface-dark` and neither schema exposes a surface setting.

Card title leading is unchanged; it was already correct, and the cart was brought to match it (§2).

---

## 10. Product page

**Fixed:** the description's rich-text link now has a hover (§15); the disclosure chevron was already correct and became the reference the other two were corrected against (§14).

**Verified unchanged:** gallery, variant picker, quantity stepper, add-to-cart lifecycle, `aria-busy` handling, sold-out and unavailable states. `interact_product` 26 assertions pass.

**Recorded:** the product page price uses `--type-body-lg-size` where cards and cart use `--type-price-size`; the accelerated-checkout skeleton colour is pinned to a cream tile with no dark-surface counterpart.

---

## 11. Cart

**Fixed.**

- **The wrapped-title leading defect** (§2) — the flagship measured finding of this phase.
- **The cart note's disclosure chevron** pointed right when closed and swung to *left* when open (§14).
- **`.surface-light .cart-line__error`** removed as unreachable, for the reason this same file already documents 200 lines later for the identical override — my own Phase 18 sweep had retired the siblings and missed this one.
- The drawer's "continue shopping" hover is now pointer-scoped; it closes a drawer over the same page, so nothing navigated to clear a tapped hover state.

**Verified unchanged:** Ajax add/change/update, section rendering, the drawer's focus trap and `inert` handling, the note, quantity, remove, and the empty state's link. `cartdoc` 85, `cartqa` 14, `notes` 40, `lifecycle` 18, `interact_cartpage` 17 — all pass.

---

## 12. Our Story

No visual change beyond the shared container consolidation (geometry verified identical). The body's rich-text link gained the hover its counterparts already had (§15).

The section's schema `info` string was rewritten to drop *"Phase 2 §26.1"* and *"The Phase 7 brief"*; it now says plainly that one paragraph reads best, the field accepts about four short ones, and the column is capped at a reading measure so longer copy makes the band taller rather than the lines wider.

Approved value copy is unchanged. No value marks, claims or statistics were added.

---

## 13. Footer

**Fixed:** two ungated hover rules (`.footer__link`, `.footer__text a`); four merchant-facing schema strings rewritten to remove *"the prototype"*, *"the approved mockup"*, *"the rebuild"* and *"BUSINESS INFORMATION REQUIRED"* while keeping every instruction — including that the theme supplies no contact details and guesses nothing.

**Recorded:** the footer stacks two link type systems (policy/menu at 14px sentence case, social at 12px uppercase tracked), and four controls reveal an underline by two incompatible mechanisms, three of them with `text-decoration`, which cannot be transitioned. Both verified; both are type/motion changes to a live surface rather than polish.

---

## 14. Icons

**Fixed — the highest-corroborated defect in the audit, found seven times across four dimensions.**

`icon-chevron.svg` is drawn **pointing right** and rotated per consumer. The product page rotated it `90deg` at rest (down) and `-90deg` open (up) — correct. The filter groups and the cart note applied **no base rotation**, so the chevron pointed **right when closed and left when open**: a 180° flip with nothing to flip from, and "left" says nothing about a disclosure.

PHASE-2 §18 line 1489 permits exactly one transform, *"the chevron rotating 180° when its disclosure opens"*, and line 2917 describes one mark *"rotated in CSS for all four directions"*. The 180° had been implemented; the direction it rotates **from** had not. Both disclosures were given the base rotation.

Measured after, with transitions disabled (the transform is animated, so an immediate read returns the start value):

| Disclosure | Closed | Open | Sweep | Size |
|---|---|---|---:|---:|
| Filter group | DOWN (90°) | UP (270°) | 180° | 16px |
| Cart note | DOWN (90°) | UP (270°) | 180° | 16px |
| Product details | DOWN (90°) | UP (270°) | 180° | 24px |

**The size half of this finding was rejected.** The reviewers rated "two sizes" HIGH; PHASE-2 line 1428 assigns the chevron *both* — *"`--icon-sm` 16px inline; `--icon-md` in controls"*. A 24px glyph beside a 12px filter label would be the defect.

**Recorded:** three icon-only close buttons where only the header's has a hover; three gold count badges at three sizes; nine icon snippets accept a BEM modifier class no stylesheet defines.

---

## 15. Buttons and interactive states

**Fixed — hover is now pointer-scoped everywhere.** PHASE-2 §22.1 rule 5: *"Hover rules sit inside `@media (hover: hover)` so a touch tap never leaves an element stuck in a hover state."* Nine rules across five stylesheets sat outside it.

This matters most where nothing navigates away to clear the state: `.header__control` is the search and menu toggle in the persistent header, and `.cart-drawer__continue` closes a drawer over the same page.

| | Before | After |
|---|---:|---:|
| Hover rules total | 27 | 29 |
| Correctly pointer-scoped | 18 | **29** |
| Ungated | 9 | **0** |

**Also fixed:** the merchant rich-text inline link. Five stylesheets declare the same three-declaration rest rule; only two had a hover. The same `<a>` a merchant types into a description responded in the footer and on a page and sat inert in a collection description, a product description and the Our Story body. The three missing hovers were added.

The total moves 27 → 29, not 27 → 30: three hovers were added and one was **deleted** — `.main-search__page-link:hover`, styling a class no template emits since the paginator merge (§22).

---

## 16. Mobile

Tested at **375, 390, 430** (plus 480 and both landscape orientations). **Zero hard problems** — no horizontal overflow, no target below the 24px AA floor, on every page.

The phase's flagship defect was mobile-only in practice: at 375px the cart's product title already wraps to two lines, so the missing leading token was visible on phones and invisible on desktop. The filter drawer's exit animation is likewise a mobile-only surface (every drawer rule lives inside `@media (max-width: 767px)`).

`.cart-line__title` remains flagged UNDER-44 — it is 24px, which **meets** WCAG 2.2 SC 2.5.8's AA minimum and does not meet the 44px AAA figure. That is the deliberate Phase 8 call for a text link inside a line, not a regression.

---

## 17. Tablet

Tested at **768, 820, 1024**. Zero hard problems.

**820 was added to the responsive suite this phase.** The list carried 834 (iPad Pro) where the spec names 820, so the nine required widths were being tested as eight. Now nine.

768 is the drawer/row boundary for filters and the one/two-column boundary for the cart line — both verified either side.

---

## 18. Desktop

Tested at **1280, 1440, 1920**. Zero hard problems.

Geometry after the container consolidation is pixel-identical to Phase 13's measured values: homepage 3 columns / 297px / 32px gap at 1440 and 1920; collection 4 / 312 / 32 at 1440.

The Phase 16 P0 — the filter drawer's desktop keyboard trap — remains closed: `facetsgate` 10/10.

---

## 19. Accessibility

| Check | Result |
|---|---|
| Contrast | **73 measurements, 73 pass** (`contrast8`) |
| Keyboard / focus traps | `facetsgate` 10/10; drawer and panel lifecycle 18 assertions pass |
| Reduced motion | honoured in 13 assets; the new drawer-exit path skips the wait entirely under `prefers-reduced-motion` |
| Colour alone (SC 1.4.1) | **improved** — the mobile menu's current page now carries an underline as well as colour; the shared paginator's current page uses weight + rule, not gold |
| Accessible names | pagination merged to search's stronger treatment: `aria-label` on links (an anchor has a role that supports naming), hidden text on the current page (a bare span does not) |
| List semantics | **fixed** — collection's pagination gap was an `<li>` with no accessible content, announced as a blank entry |
| Reduced-motion durations | `--duration-*` collapse to 1ms; verified unchanged |

No accessibility regression was introduced. The drawer-exit change keeps the panel visible for 250ms after close; focus has already returned to the trigger and the keydown trap is released at that point — the same tradeoff the cart drawer already makes and which passed earlier review.

---

## 20. Performance regression

No regression. Phase 18 added **no images, no libraries, no blocking scripts and no new animation**; the one motion change restores an exit transition PHASE-2 §21 line 1725 already specified.

**CSS payload went down.** The two new component files grew the raw byte count because they carry their reasoning in comments, so the number that matters is rules-only:

| | Before | After | Delta |
|---|---:|---:|---:|
| CSS, comments stripped | 98,129 B | 95,628 B | **−2,501 B (−2.5%)** |
| Declarations | 2,451 | 2,380 | **−71** |
| Stylesheets | 19 | 21 | +2 |

Measured page weight and request counts (gzipped, CSS + JS):

| Surface | Requests | CSS gz | JS gz |
|---|---:|---:|---:|
| Homepage | 26 | 55,093 | 16,392 |
| Collection | 21 | 46,599 | 16,392 |
| Collection + filters | 23 | 51,708 | 20,230 |
| Product | 23 | 40,519 | 21,989 |
| Cart page | 17 | 31,421 | 16,392 |
| Search | 18 | 46,507 | 16,392 |
| 404 | 15 | 38,316 | 16,392 |

Duplicate requests: **0** on every surface.

`cart.js` remains above Shopify's 10,000-byte compressed `AssetSizeJavaScript` threshold at 12,073 B gzipped — **unchanged from Phase 16, not introduced here.** It is 4,930 B with comments stripped, so the threshold is not reachable by deleting prose; it needs restructuring, which is not a Phase 18 action.

**TTFB, FCP and field LCP/INP are not measurable in this environment** — there is no Shopify server. Reported as unavailable rather than estimated.

---

## 21. Analytics regression

**No analytics regression, because there is still no analytics to regress.** `phase17/tracking.py`: 31 checks, 31 clean, **NO TRACKING PRESENT** — unchanged.

Phase 17 established that the theme ships **no** analytics IDs, pixels or properties, because none exist to ship and inventing them was explicitly forbidden. The five events named in the spec (`view_item`, `add_to_cart`, `view_cart`, `begin_checkout`, `purchase`) therefore have nothing in the theme to break.

What *was* verified, because Phase 18 touched the purchase surfaces:

- `phase17/funnel.py` 8/8 — the purchase path still emits what a future integration would bind to.
- `phase17/negctl.py` 12 seeded violations, 12 fully caught — the guard that would catch a tracking regression still works.
- `phase17/escaping.py` 7/7 — the Phase 17 escaping fixes in `cart-line-item.liquid` and `cart-note.liquid` are intact.

Also relevant: a theme **cannot** publish Shopify standard events (Shopify: *"partners and merchants cannot publish standard events"*), so none of these five could be theme-emitted in any case.

---

## 22. Legacy design cleanup

Dead code was **confirmed** before removal, not guessed at. A first scan reported 162 candidates; three scanner defects were found and fixed before any of it was believed:

1. It skipped classes built by Liquid concatenation, calling `quantity` dead when the stepper plainly exists (`class="{{ classes }}"`).
2. It anchored selectors to line start, silently skipping **every rule inside a `@media` block** — where this theme keeps its responsive and hover rules.
3. It split `class="{{ classes }}"` on whitespace and let the *variable name* through, filling the orphan list with `endif`, `handle` and `cta_variant`.

Corrected results:

| | Count | Assessment |
|---|---:|---|
| CSS classes no markup can reach | **2** | Both explained: `shopify-payment-button` is Shopify's own output that the theme styles; `variant-picker__swatch--square` is reachable via the snippet's documented `swatch_shape` option. **Effectively zero dead CSS.** |
| Markup classes with no CSS rule | 28 | Semantic hooks, several created by this phase's own container consolidation. Kept — they are useful targets, including for the QA probes. |
| `data-` attributes no script reads | 25 | Candidates, recorded not removed. |

**Removed this phase:** `.main-search__page-link:hover` (the last fragment of the paginator this stylesheet used to own — my own leftover from the merge, not a pre-existing one); `.surface-light .cart-line__error` and three sibling `.surface-light` selectors (unreachable — both cart surfaces hardcode `surface-dark`); eight whole container rules absorbed into `.container`; two duplicate pagination blocks.

---

## 23. Files created

| File | Bytes | Purpose |
|---|---:|---|
| `snippets/pagination.liquid` | 5,644 | The merged paginator, rendered by both collection and search |
| `assets/component-pagination.css` | 3,220 | Its rules, promoted per the trigger the collection stylesheet had documented |
| `assets/component-container.css` | 1,747 | The content column PHASE-2 §8 specified and the implementation never built |

**Theme total: 75 files.** `templates/customers/` remains absent — that absence is Shopify's auto-upgrade trigger for new customer accounts and must stay.

---

## 24. Files modified

**34 files.**

**Tokens and components (7):** `design-tokens.css` (the new `--type-label-lh`), `component-cart-line.css`, `component-product-card.css`, `component-facets.css`, `facets.js`, `header.css`, `section-cart-drawer.css`.

**Section stylesheets (10):** `section-featured-collection.css`, `section-footer.css`, `section-hero.css`, `section-main-404.css`, `section-main-cart.css`, `section-main-collection.css`, `section-main-page.css`, `section-main-product.css`, `section-main-search.css`, `section-our-story.css`.

**Sections (12):** `announcement-bar.liquid`, `featured-collection.liquid`, `footer.liquid`, `header.liquid`, `hero.liquid`, `main-404.liquid`, `main-cart.liquid`, `main-collection.liquid`, `main-page.liquid`, `main-product.liquid`, `main-search.liquid`, `our-story.liquid`.

**Snippets (2):** `cart-line-item.liquid`, `cart-note.liquid`.

**Configuration (3):** `layout/theme.liquid` (two new stylesheet links), `locales/en.default.json` (one pagination string set; the search placeholder), `config/settings_schema.json` (two merchant strings de-jargoned).

---

## 25. Remaining issues

### Decisions required from you

1. **"Add to bag" versus "cart".** The audit rated this HIGH and it is factually correct — it is the only "bag" string against 14 "cart" strings. But it is a **recorded decision**, not drift: PHASE-2 line 943 writes *"add-to-bag is a `<button>`"* and PHASE-12 line 209 uses the same term. The action is "add to bag" and the container is the "cart" by choice. Unifying the voice is a brand call. **Not changed.**
2. **Mobile menu panel type.** Playfair 900 at `--type-h3-size` where PHASE-2 §19.6 specifies the eyebrow triplet; no phase document defends the deviation. Correcting it would re-type the **primary mobile navigation** — a visible design change, not polish. Your call.
3. **Footer link type systems.** Policy/menu links at 14px sentence case sit directly above social links at 12px uppercase tracked. Same reasoning as (2).
4. **"Worldwide Shipping"** ships in the announcement bar on every page while the same claim is deliberately withheld from the Our Story values row. This is a business claim — either it is true of the business or it is not. **Not mine to assert or remove.**
5. **Announcement bar icon** is a merchant-uploaded raster, the only glyph in the theme that is not an inline SVG in `currentColor`. Restricting it to the icon set is a merchant-capability decision.

### Verified, recorded, not changed (55 items)

Full list with evidence in `PHASE-18-VISUAL-AUDIT.md`. The substantial ones: the applied-filter badge defined twice at two sizes; three overlays locking the page three ways; the cart page inventing its own sidebar width where the product page uses a token; the editor-only merchant notice built five times; `aria-busy` styled on only one of the two surfaces that set it; three rules hardcoding `0.25em` where `--link-underline-offset` exists; the product price using `--type-body-lg-size` where cards and cart use `--type-price-size`.

Each is real and each was left alone deliberately: they are cosmetic or structural tidying whose risk outweighs its benefit in a phase whose first instruction is **"THIS IS NOT A REDESIGN."**

### Pre-existing, unchanged

- **Theme Check: 2 offenses**, both `ValidJSON` on `config/settings_schema.json` — missing `theme_support_email` and `theme_documentation_url`. **Business information required**, not code defects.
- **`cart.js` exceeds Shopify's 10 KB compressed script threshold** (12,073 B). Unchanged from Phase 16; needs restructuring, not comment-stripping.
- **No merchant photography, no logo vector master, no favicon.** Phase 3's ceiling, unchanged and unchangeable from here.
- **Legacy customer accounts are deprecated**, so order history and tracking are not theme-buildable (Phase 15).

---

## Regression suite — full run, after every Phase 18 change

```
Theme Check          2 offenses (both business information)
validate             199/199        contrast8      73/73 measurements
layout                19/19         surfaces        41/41
catalog               55/55         cardcascade     10/10
facets                62/62         facetsgate      10/10
editor                10/10         settings        28/28
cartdoc               85/85         cartqa          14 assertions
notes                 40            lifecycle       18
accounts              52/52         negctl(15)      22/22 caught
hygiene               0 findings    images          54/54
seo                   52/52         refs            10/10
tracking              31/31 clean   negctl(17)      12/12 caught
funnel                 8/8          escaping         7/7
interact              49            interact_cart   17
interact_product      26            console          0 errors / 22 pages
respond               0 hard problems across 12 viewports
chevron               3/3 disclosures agree
hovergate             29 rules, 29 gated, 0 ungated
drawerexit            12/12 (negative control run)
```

**New tests added this phase:** `chevron.py` (disclosure direction), `hovergate.py` (pointer-scoping, doubles as the regression guard), `drawerexit.py` (12 assertions on the exit animation and its fallback), `coherence.py` (design-role signatures), plus the measurement probes `lineheight.py`, `linebox.py`, `gap.py`, `emptystate.py`, `deadcode.py`, `whichh3.py`.

---

## What I got wrong during this phase, and how it was caught

Recorded because the method matters more than the result.

1. **`getClientRects()` on an atomic inline returns one rect** no matter how many lines its content occupies. Two probes reported the cart title as "1 line" and "2 lines" from the same element. A `Range` over the text node gives real line fragments — that is what produced the 14.0px/17.4px measurement.
2. **A transitioned property reads as its start value** if you read it in the same frame. The chevron probe first reported the filter chevron as unchanged after flipping `[open]`. Phase 4 had already recorded this lesson; the probe forgot it. Transitions are now disabled before measuring.
3. **The dead-code scanner was wrong three times** before it was right (§22). Its first answer — 162 items — would have been a fabricated number in this report.
4. **A "nothing moved" result meant the rule never applied.** The blast-radius probe reported no change from the line-height fix; a negative control showed the injected rule had applied but the fixture's titles simply did not wrap at that width. Without the control the conclusion would have been backwards.
5. **A docstring claimed "assertions 2–5 fail" under negative control.** Running it showed exactly **one** fails. Corrected in the file.

---

## Acceptance criteria

**DESIGN** — one visual language: 10/15 roles single-signature, and no class renders two ways. 3 radii, 1 shadow, 2 durations, 1 easing across the whole site. Legacy conflicts: effectively zero dead CSS. Typography, buttons and icons: consistent after this phase's fixes, with three type decisions listed above awaiting your call. **Images: NOT ASSESSABLE — no merchant photography exists.**

**UX** — navigation, discovery, product, cart and checkout transition unchanged and passing. **Empty states improved** (no longer a duplicated page heading). Error states unchanged and passing.

**RESPONSIVE** — all nine specified widths tested, 0 hard problems. 820 added this phase.

**ACCESSIBILITY** — keyboard, focus, contrast (73/73), labels, reduced motion all pass; two SC 1.4.1 improvements made. Alt text path verified; **alt text content depends on merchant images that do not exist.**

**TECHNICAL** — no broken images, no broken internal links, 0 console errors across 22 pages, Theme Check clean except the two business-information properties, no performance regression (CSS rules −2.5%), analytics unaffected.

**BRAND** — GOD SQUAD presented consistently; Philippine streetwear positioning untouched; premium aesthetic preserved; nothing generic added. **No fake claims, reviews, awards, statistics, testimonials or imagery were introduced**, and the one unsupported business claim already present ("Worldwide Shipping") is flagged to you rather than propagated.

---

## Final recommendation

The theme is **code-complete and internally coherent**, and it is **not launchable**, for reasons that have nothing to do with code.

Three things gate a launch and none is a development task: **merchant photography**, a **vector logo master and favicon**, and the **business information** Theme Check is still asking for. On the photography: the theme contains **zero image files** and no template sets one, so every image slot is empty until a merchant fills it. The imagery in the approved mockup sits in the project's `uploads/` folder, is AI-generated, and its rights are unconfirmed (Phase 3's ceiling). Until the photography exists, the single largest component of a visual review has not been done by anyone.

Before Phase 19, I would want: the five decisions in §25 answered, the merchant assets supplied, and then a genuine visual pass against real imagery — which is the review this environment could not perform.

**Phase 18 is complete. Stopping here. No Phase 19 work has been started, the theme has not been published, and no Shopify Admin change has been made.**
