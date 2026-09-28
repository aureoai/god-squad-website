# PHASE 19 — SHOPIFY BASELINE

**Date:** 2026-09-28
**Status of the theme at the moment of this audit:** 35/35 QA suites pass, Theme Check **0 offences**.
**Store access:** none. Shopify CLI 4.8.2 is installed; there is no authenticated session, no store URL and no credentials.

Phase 19 STEP 01 says: *"Before modifying anything, inspect the entire project… Do not assume previous implementation details. Understand the actual current codebase first."* This document is that inspection. It records what is **on disk**, not what earlier phase documents claim.

---

## 0. What changed immediately before this audit, and was not ours

Between the end of the previous session and the start of Phase 19, work landed in the theme from outside this session. There is **no git repository**, so these changes could not be diffed — only their current state read. That is itself the first finding.

| Added | What it is |
|---|---|
| `templates/gift_card.liquid` | The page a customer reaches from a gift-card email |
| `templates/password.json`, `sections/main-password.liquid`, `assets/section-main-password.css` | The storefront password gate |
| `snippets/image-fallback.liquid` + 6 files in `assets/` | Bundled stand-in photographs for unset `image_picker` settings |
| `shopify-upload/` | 8 images and a 5-product CSV staged for import |

It closed two of the five missing templates and added a genuinely useful fallback system. It also shipped **three P0 defects** and broke four QA suites. All are fixed in this phase; see the integration report.

---

## 1. Current architecture

Shopify **Online Store 2.0**, no build step, no framework, no dependencies.

- **8 of 9 templates are JSON.** The ninth, `gift_card.liquid`, is Liquid because Shopify does not accept a JSON gift-card template.
- **Two section groups** — `sections/header-group.json` and `sections/footer-group.json` — rendered by the OS 2.0 `{% sections %}` tag at `layout/theme.liquid:220` and `:305`.
- **No pre-OS-2.0 constructs.** Zero `{% stylesheet %}` / `{% javascript %}` tags.
- **Two layouts**: `theme.liquid`, and `password.liquid` added in this phase.

## 2. Current theme structure

| Directory | Files |
|---|---|
| `assets/` | 38 |
| `snippets/` | 33 |
| `sections/` | 22 |
| `templates/` | 9 |
| `config/` | 2 |
| `layout/` | 2 |
| `locales/` | 1 |
| **Total** | **107** |

Packaged size: **~500 KB** against Shopify's 50 MB ceiling.

## 3. Existing templates

`404.json` · `cart.json` · `collection.json` · `gift_card.liquid` · `index.json` · `page.json` · `password.json` · `product.json` · `search.json`

**Still absent, and Shopify routes to all three:** `article`, `blog`, `list-collections`. Each serves Shopify's error page to anyone reaching its URL. `list-collections` is the one that matters now — see §15.

## 4. Existing sections

`announcement-bar` · `brand-values` · `cart-drawer` · `cart-icon-bubble` · `featured-collection` · `footer` · `header` · `hero` · `main-404` · `main-cart` · `main-collection` · `main-page` · `main-password` · `main-product` · `main-search` · `our-story` · `verse-feature` · `verse-index` · `words-we-wear` — plus the two group JSONs.

All three Verse sections carry `presets` and **declare no `enabled_on`**, so they are already addable to any JSON template. A `/pages/verse` route needs a template, not Liquid changes.

## 5. Existing snippets

33, including the shared commerce pieces that keep STEP 03 satisfied: `product-card` (used by all three product grids), `cart-line-item`, `cart-totals`, `cart-note`, `cart-empty-state` (shared by the drawer and the cart page), `pagination`, `grid-sizes`, `product-variant-picker`, `product-media-gallery`, `meta-social`, `css-variables`, 13 `icon-*` snippets, and `image-fallback`.

## 6. Existing assets

37 code files plus **6 bundled images** (`hero.webp`, `story.webp`, `tee.webp`, `hoodie.webp`, `cap.webp`, `logo.png` — 230 KB total).

The images are new, and they **reverse a recorded decision**: the reference manual states the assets directory holds *"No images, no fonts"* because content images arrive through `image_picker`. They are all genuinely referenced — `logo.png` by the header and footer logo fallbacks, the five `.webp` by `image-fallback` — and they make an unconfigured store look like its design. They also cost 230 KB on every upload, and the hero becomes a single-candidate 120 KB LCP image with no responsive variants. **Owner decision, listed in the report.**

## 7. Existing product data dependencies

Every product fact comes from a Shopify object. Verified across `snippets/product-card.liquid`, `sections/main-product.liquid` and `snippets/product-variant-picker.liquid`: `title`, `featured_image`, `price`, `compare_at_price`, `url`, `available`, `options_with_values`, `variants`, `selected_or_first_available_variant`, `quantity_rule`.

**Inventory is never published as a number.** `main-product.liquid:89` and `:567` emit a per-variant low-stock **boolean**; the reason is recorded at `main-product.liquid:33-36`. No hardcoded product, price, variant or inventory fact exists anywhere in `sections/`, `snippets/` or `templates/`.

## 8. Existing collection dependencies

`templates/index.json` pins two handles: **`new-drop`** and **`best-sellers`**. `sections/featured-collection.liquid:314` renders nothing when the handle resolves to blank, so on a store without those two collections both homepage bands disappear silently. This is the first thing to check on upload.

`sections/main-collection.liquid` reads `collection.title`, `.description`, `.image` and paginates `.products` — all store data, none verifiable offline.

## 9. Existing cart implementation

Ajax via `assets/cart.js`: `/cart/add.js`, `/cart/change.js`, `/cart/update.js`. Count from `cart.item_count`. Two surfaces — `sections/cart-drawer.liquid` and `sections/main-cart.liquid` — sharing four snippets. The drawer is not rendered on the cart template (two views of one cart disagree).

## 10. Existing customer account implementation

`templates/customers/*` is **absent, deliberately, and must stay absent**: shipping those files withholds the merchant's automatic upgrade off legacy accounts, which Shopify deprecated. `sections/header.liquid:287-296` renders Shopify's own `<shopify-account>` element, gated on `shop.customer_accounts_enabled`. `qa/phase16/accounts.py` passes 52/52. This is as far as a theme is now permitted to go.

## 11. Existing search

`sections/main-search.liquid`, using Shopify's `search` object with `predictive_search` absent by choice. Filters render only when `collection.filters` is populated, which requires the Search & Discovery app.

## 12. Existing Verse implementation

Three homepage sections in `templates/index.json`, after Our Story:

| Section | Blocks | Content |
|---|---|---|
| `verse-feature` | none | Today's Verse strip; `anchor_id: verse` |
| `verse-index` | `verse` ×4, max 12 | Explore Verses; chips **derived** from block categories |
| `words-we-wear` | `phrase` ×4, max 8 | Words We Wear tiles |

**Against STEP 16's list:** present are TODAY'S VERSE, EXPLORE VERSES, WORDS WE WEAR, and the categories Faith, Purpose, Courage, Light. **Absent from the entire theme** (confirmed by grep): the categories **HOPE**, **LOVE**, **STRENGTH**, and the strings **"THE VERSE"**, **"WORDS TO LIVE BY."**, **"INSPIRED COLLECTION"**. There is **no `/pages/verse` route**.

Most of the gap is Theme Editor data entry, not code: adding three categories is adding three blocks. "INSPIRED COLLECTION" is the exception — it would be a new section.

## 13. Existing analytics

**None, and none is possible.** `qa/phase17/tracking.py` reports 31 checks clean, 0 findings; `qa/phase17/negctl.py` catches 12/12 seeded violations. `content_for_header` is emitted unmodified. A theme can no longer publish Shopify standard events — that moved to Custom Pixels in admin. STEP 30's "preserve the existing analytics implementation" is satisfied by there being nothing to preserve but Shopify's own.

## 14. Existing third-party dependencies

**Zero.** No `package.json`, lockfile, `node_modules`, bundler, framework or CDN reference in the theme. Total JavaScript ~24 KB gzipped, no dependencies. `qa/package.json` exists but builds nothing — it is the Theme Check runner.

## 15. Known issues

**Fixed in this phase** (see the integration report): three P0 defects in the newly-added templates, four broken QA checks, and the parser-blocking script.

**Outstanding, not fixed:**

| # | Issue | Why it stands |
|---|---|---|
| 1 | `shopify-upload/products.csv` is **fabricated** | 5 products, 17 variants, invented prices, invented stock, invented SKUs, and compare-at prices that manufacture a discount from a price never charged. **Do not import.** |
| 2 | "Worldwide Shipping" ships as a live default | `header-group.json:17` and `footer-group.json:47`. The theme's own `our-story.liquid:261-267` refuses to assert this exact claim for want of a shipping policy. |
| 3 | No `list-collections` template | STEP 05 wants a COLLECTIONS nav item; the route has no template. |
| 4 | No `/pages/verse` route | STEP 16. |
| 5 | No git repository | Today's changes could not be diffed. |
| 6 | Bundled images reverse a recorded decision | §6. |
| 7 | `theme_version` still `0.5.0` | Production preparation. |
| 8 | No `*.schema.json` locale | Every Theme Editor label is hardcoded English. |

## 16. Recommended migration approach

1. **Do not import the CSV.** Enter the real catalogue, or export it from an existing system.
2. **Create `new-drop` and `best-sellers`** (or re-point the two bands in the Theme Editor).
3. **Upload the theme as a draft** — `python qa/make-theme-zip.py`, then Online Store → Draft themes → Import theme. It does not publish.
4. **Upload images to Content → Files** and select them in the Theme Editor. The bundled fallbacks are stand-ins, not the delivery mechanism.
5. **Then, and only then**, run the store-dependent half of Phase 19: checkout, Buy It Now, filters, real Theme Check, browser QA.
6. **Adopt version control before anything else changes.**

---

*Compiled by reading the files. Where a claim could not be verified without a store, it is listed as blocked rather than asserted.*
