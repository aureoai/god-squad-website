# GOD SQUAD — PHASE 16
## Performance + SEO + Conversion Optimization

**Status:** delivered · **Date:** 2026-09-24 · **Theme:** `god-squad-theme/`

---

## 0. Two things that changed what this phase could do

**Theme Check runs. It always could.** Every phase since 10 has reported it
unavailable "because Shopify CLI is not installed". That was true of the CLI and
false of the checker: `@shopify/theme-check-node` — the same engine the CLI
wraps — has been in the scratchpad's `node_modules` since Phase 10. The runner
written then pointed at the *project* root, which stopped being the theme root
the moment Phase 10 moved the theme into `god-squad-theme/`. It had been
scanning a directory with no theme in it and reporting zero offenses. Pointed
correctly it found four. **That limitation should not have been carried through
three phases, and it is retired.**

**Lighthouse genuinely is unavailable.** Not installed, and `npm` has no network
here. No Lighthouse number appears anywhere in this document, because the brief
forbids inventing one and there is nothing to report.

---

## 1. Performance baseline

Measured, from the real rendered pages and the real files on disk.

| Surface | requests | HTML gz | CSS files | CSS gz | JS files | JS gz | `<img>` | inline SVG |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Homepage | 24 | 4.1 KB | 11 | 50.2 KB | 2 | 16.4 KB | 10 | 10 |
| Collection | 19 | 3.8 KB | 10 | 41.7 KB | 2 | 16.4 KB | 6 | 8 |
| Collection + filters | 21 | 4.6 KB | 11 | 45.8 KB | 3 | 19.5 KB | 6 | 13 |
| Product | 21 | 4.9 KB | 8 | 35.8 KB | 3 | 22.0 KB | 9 | 10 |
| Cart page | 15 | 3.5 KB | 7 | 26.9 KB | 2 | 16.4 KB | 5 | 14 |
| Search | 16 | 3.5 KB | 10 | 41.8 KB | 2 | 16.4 KB | 3 | 9 |
| 404 | 13 | 2.8 KB | 9 | 33.7 KB | 2 | 16.4 KB | 1 | 9 |

The icon set costs **zero requests** on every surface — 8 to 14 inline SVG
snippets per page instead of files.

### 1.1 What is NOT measured, and why no number is given

| Metric | Why not |
|---|---|
| LCP, FCP, TTFB **timings** | No Shopify server and no network. The harness serves localhost. |
| INP as a field metric | Needs real users. Handler duration is measured instead and labelled as an input to INP, not INP. |
| Image **bytes** | The merchant's photography does not exist yet — Phase 3 recorded sourcing as the ceiling. Image count and declared size are reported instead. |
| CLS from **font swap** | The harness has no font files, so no swap occurs. This is the one CLS source that cannot be reproduced locally, and it is called out rather than silently scored zero. |
| Lighthouse | Not installed, no network to install it. |

---

## 2. Performance changes

Seven changes. Every one traced to a measured finding or a Theme Check offense;
nothing was changed on taste.

| # | Change | Why |
|---|---|---|
| 1 | Gate the filter drawer on viewport width | **P0** — desktop scroll lock and keyboard trap (§4) |
| 2 | Load Jost 500 and 600 | Faux-bold on every label, price and eyebrow (§9) |
| 3 | `eager` + `fetchpriority` follow the *active* gallery slide | The LCP image was not the one on screen (§6) |
| 4 | Open Graph + Twitter card | No social metadata existed at all (§10) |
| 5 | `apple-touch-icon` + 192px icon | Only a 32px PNG was declared (§10) |
| 6 | Remove two orphaned Liquid assigns | Theme Check `UnusedAssign` (§0) |
| 7 | Footer logo link given an accessible name | Level A failure (§12) |

Plus two correctness fixes with no performance dimension: `aria-controls` no
longer points at a non-existent id on `/cart`, and cart focus can no longer land
on an `aria-hidden` element (§12).

---

## 3. The audit that produced the findings

Ten dimensions, each audited by one agent reading the real source and then
**adversarially verified** by a second told to *reject* rather than agree.

```
                    findings  confirmed  REJECTED  needs-measurement
css-waste                11       8          2          1
js-waste                 10       6          3          1
liquid-perf               5       1          4          0
seo-head                  7       5          0          2
structured-data           5       4          0          1
images                   12      11          0          1
critical-path             8       5          2          1
broken                    7       6          1          0
a11y                      9       8          0          1
conversion                8       8          0          0
                        ----    ----       ----       ----
                          82      62         12          8
```

**62 confirmed: 2 P0, 10 P1, 30 P2, 20 P3.** The 12 rejections are the point of
the second pass — among them "the focus trap is written three times" (the three
are genuinely different traps), "featured-collection computes the slot width
twice" (the second is used), and "`main-collection` and `facets` both derive
`has_filters`" (deliberate, so the snippet works standalone).

---

## 4. LCP findings

### 4.1 The P0: a Filter button that locked the desktop page

Found independently by the JavaScript audit and the accessibility audit, from
different directions, tracing to the same two lines. **Reproduced before fixing.**

`assets/facets.js` revealed the filter trigger unconditionally. Every drawer rule
in `component-facets.css` lives inside `@media (max-width: 767px)` — but
`.facets-open body { overflow: hidden }` does not; it is top level.

Measured at 1440, 1280 and 768 on a collection with filters configured:

```
viewport   toggle visible   press it -> scrollLocked   drawer header
1440x900   yes              YES                        display:none
1280x800   yes              YES                        display:none
 768x1024  yes              YES                        display:none
```

So a desktop customer got a visible Filter button that **locked the page scroll
and opened nothing**. Worse, `.facets__bar` holds the close button and is
`display: none` at that width, so `closeBtn.focus()` was a no-op — focus stayed
on the trigger, and the panel's own Tab guard then pulled it into an in-flow
panel. **Escape was the only way out of a page that no longer scrolled: a
keyboard trap, SC 2.1.2.**

The cause is precise. The media-query listener only ran on **change**, so it
correctly closed a drawer left open by a rotation and *never once evaluated the
width the page loaded at*. Both directions now run through one `applyWidth()`
called immediately and on change, `open()` refuses above the breakpoint, and CSS
retires the trigger at `min-width: 768px` — the same pattern `header.css`
already uses to retire the mobile menu.

After: **10/10**, desktop clean, mobile drawer fully working.

This is a defect I shipped in Phase 13, and Phase 13's own suite missed it
because it only asserted the trigger *ships* `hidden` in the markup — never what
happens after script upgrade at desktop width.

### 4.2 The LCP element, audited statically

The first attempt measured LCP with `PerformanceObserver` and reported the
collection page's largest paint as the **78px header logo**. That would be
serious. It is an artifact: the harness ships **no image files at all**, so every
`<img>` 404s and the logo wins by default. The reading was discarded.

What decides LCP on a real store is in the markup, and that is fully checkable:

| Surface | eager | lazy | the eager one | `fetchpriority` |
|---|---:|---:|---|---|
| Homepage | 1 | 8 | `hero__image` | high ×1 |
| Collection | 1 | 4 | `product-card__image` (first tile) | — |
| Search | 1 | 1 | `product-card__image` | — |
| Product | 1 | 7 | `product-gallery__image` | high ×1 |
| Cart page | 1 | 3 | `cart-line__image` | — |

**One eager image per surface, and it is the right one every time.** No image
above the fold is lazy-loaded; `fetchpriority` is used at most once per page.

### 4.3 The gallery was hurrying the wrong frame

`product-media-gallery.liquid` keyed `loading: eager` and `fetchpriority: high`
to `forloop.first`. The slide the page **opens on** is `is_active` — the
variant's featured media when it has one. So on any product whose selected
variant is not the first medium, the browser was told to hurry an image nobody
was looking at and to lazy-load the actual LCP element.

Now: `fetchpriority` follows `is_active`; `forloop.first` keeps `eager` because
the stacked desktop layout renders every slide in document order.

---

## 5. INP findings

| Control | handler time |
|---|---:|
| menu toggle | 0.00 ms |
| cart bubble | 0.00 ms |
| quantity stepper | 0.00 ms |
| filter toggle | 0.00 ms |
| search trigger | 0.00 ms |

**No long tasks on any surface during load.** This is handler duration — one
component of INP, not INP — and it is reported as such.

The theme's INP posture is structural rather than tuned: one delegated listener
per event type for the whole document, no framework, no polling, no `setInterval`
anywhere, and the only debounce is a deliberate 250ms on cart quantity.

---

## 6. CLS findings

Load CLS, measured before any interaction:

| Surface | CLS | source |
|---|---:|---|
| Homepage | 0.0003 | header nav settling |
| Collection | 0.0003 | header nav settling |
| Collection + filters | 0.0003 | header nav settling |
| Product | 0.0000 | none |
| **Cart page** | **0.0125** | the Update button being hidden |
| Search | 0.0003 | header nav settling |

Against Google's 0.1 threshold, the worst surface is **8× under**.

The cart page's 0.0125 is a known, deliberate trade. `.cart-js
.main-cart__update { display: none }` removes the no-JavaScript Update button
once `cart.js` confirms it is running, and everything below it moves up. Phase 14
documented why it keys on `cart-js` and not the layout's `js` class: keying on
`js` would hide the only control that can apply a quantity change in exactly the
case where nothing else can. Reserving the space leaves a gap; reordering it
visually breaks DOM/visual order. **0.0125 is the correct price for a working
no-JavaScript fallback**, and it is recorded rather than hidden.

**Every `<img>` on every surface carries `width` and `height`** — the CLS
precondition — verified across six surfaces.

An early reading put the product page at 0.0035 and the cart at 0.0036. That was
my own measurement error: synthetic `dispatchEvent` clicks do not set
`hadRecentInput`, so shifts I caused by opening a drawer were being counted as
load instability. Load and interaction shift are now measured separately.

---

## 7. Image optimization

**11 of 12 image findings confirmed, and the pipeline was already sound.** 54
checks pass across six surfaces:

- every `<img>` has `width` and `height`
- every content image has `srcset` **and** a matching `sizes`
- no `srcset` overshoots 3× its largest declared slot
- every `<img>` has an `alt`; none reads as keyword stuffing
- video is rendered through Shopify's filters with `autoplay: false`,
  `controls: true`, `preload: 'metadata'` and a lazy-loaded external player —
  there is no background or decorative video

The one change made is §4.3. The remaining image findings are P2/P3 refinements
listed in §18.

---

## 8. JavaScript optimization

| File | raw | gzip | code only | code gz |
|---|---:|---:|---:|---:|
| `cart.js` | 39,750 | 12,073 | 20,616 | 4,930 |
| `header.js` | 13,963 | 4,319 | 9,062 | 2,091 |
| `product.js` | 18,096 | 5,597 | 11,734 | 2,863 |
| `facets.js` | 8,818 | 3,120 | 4,938 | 1,356 |

**Zero dependencies. No framework, no jQuery, no Swiper, no GSAP, no polyfill, no
duplicate library** — verified, not assumed. One global (`window.GodSquad`).

Theme Check's `AssetSizeJavaScript` flags three script tags against a 10,000-byte
compressed threshold, and `cart.js` at 12,073 is genuinely over it. The
diagnostic column above answers the only question that matters: **the executable
code is 4,930 bytes gzipped; the other 7,143 is comments.** Shopify measures
shipped bytes, so the offense is real — but "restructure the cart with
import-on-interaction" is the wrong response to 7KB of documentation on a theme
whose *total* JavaScript is 24KB gzipped with no dependencies. Recommended, not
done: a minification step at deploy (§20).

---

## 9. Font optimization

**The one finding in this phase a customer would have seen on every page.**

`design-tokens.css` defines four weights and the type scale spends three of them
on the **body** family: `--type-eyebrow-weight` is 500, `--type-label-weight` and
`--type-price-weight` are 600, covering 19+ rules — every label, price and
eyebrow in the store.

`layout/theme.liquid` called `font_face` exactly twice, once per family, and each
call emits a face for the **one** variant in the setting: `jost_n4` (400) and
`playfair_display_n9` (900). **Jost 500 and 600 had no `@font-face` at all**, so
the browser synthesised them from Jost 400. Faux bold is thicker, wider and
differently tracked than a real cut — on a type system built out of tracked caps,
visible everywhere.

Now emitted, via `font_modify`:

```
Jost 400   Jost 500   Jost 600   Playfair Display 900
```

Every call is **guarded**, because `font_modify` returns nil when a family has no
such variant. Negative-controlled with a single-weight family: 2 faces emitted,
no broken rules.

`font_display: swap` is unchanged, and all four faces remain inside one
`{% style %}` block — the Phase 10 fix that must not regress.

---

## 10. SEO audit

Measured on the rendered `<head>` of all seven templates.

**Already correct and left alone:** exactly one canonical per template, from
Shopify's `canonical_url`, with nothing competing; titles built from `page_title`
with the shop name appended only when absent and the page number named on
paginated views; meta description from `page_description`; no `robots.txt.liquid`
and no meta-robots competing with Shopify's defaults; no custom sitemap.

**Heading structure is clean on every surface** — exactly one `h1`, no skipped
levels:

```
Homepage    h1 h2 h3 h3 h3 h2 h3 h3 h3 h3 h2 h3 h3 h3 h2
Collection  h1 h2 h2 h2 h2 h2 h2 h2 h2
Product     h1 h2          Cart  h1          404  h1 h2 h2
```

**Three gaps found and closed:**

1. **No Open Graph and no Twitter card on any template.** A link to the store
   pasted into Messenger, Viber, Instagram or X showed whatever the platform
   could scrape. Phase 1 SEO-04 specified `snippets/meta-tags.liquid` by name and
   routed it to "Phase 13 — SEO"; the delivered Phase 13 was Search and
   Filtering. The work was orphaned, not decided against.
2. **No `apple-touch-icon`.** The only declared icon was a 32px PNG, which iOS
   ignores entirely — a customer adding the store to their home screen got a
   screenshot of the page.
3. **No share-image source** for the five templates that have neither a product
   nor a collection image.

`snippets/meta-social.liquid` emits `og:site_name`, `og:url`, `og:title`,
`og:type`, `og:description`, `og:image` (+ `secure_url`, width, height, alt),
`twitter:card`, `twitter:title`, `twitter:description`. **Every value is a
Shopify object; there is no written marketing copy in the file.** `og:type` is
`product` on a product page and `website` elsewhere. The image chain is
product → collection → new `settings.share_image` → logo, each branch guarded so
a store with no image emits no `og:image` rather than a URL that 404s.

**A bug my own test caught before it shipped:** the first version derived the
image height by dividing 1200 by `aspect_ratio`, which is not populated on every
image drop — Liquid treats the missing value as 0 and it threw a division by zero
on **all seven templates, in the head, on every page**. Height is now derived
from `width`/`height`, guarded against a zero width.

Two corrections to what the audit proposed, both deliberate: `og:image:width` is
the literal 1200 with height derived for *that* rendering (reading `image.width`
would publish the source asset's dimensions alongside a 1200px URL), and no
`og:price` is emitted because `structured_data` already publishes price and
availability in the vocabulary search engines consume.

---

## 11. Structured data audit

**Current state: `{{ product | structured_data }}` on the product template, and
nothing else.** That is Shopify's own filter, so price, availability and SKU come
from the platform and cannot drift.

**Confirmed missing:** Organization, WebSite, BreadcrumbList, and any
collection-level markup.

**Not implemented this phase, deliberately.** Organization's useful fields —
`sameAs`, `logo`, `contactPoint` — are exactly the values this project has
refused to invent for fifteen phases. The theme has `social_facebook_url` and
`social_instagram_url` settings which may be empty, and `shop.name`/`shop.url`.
An Organization block built only from what exists would carry a name, a URL and
possibly a logo, which is close to what Shopify already emits itself. The rest is
**BUSINESS INFORMATION REQUIRED**, and a `sameAs` array that is empty half the
time is worse than no block.

BreadcrumbList is declined on stronger grounds: this theme has **no navigation
hierarchy to describe**. Products are not scoped to a parent collection in the
URL, and the menu is the merchant's. A fabricated trail is exactly the fake
structure the brief forbids.

Both are carried to §20 with the precise condition that would unblock them.

---

## 12. Accessibility audit

8 of 9 findings confirmed. Three fixed this phase; the P0 in §4.1 was the
largest.

**The footer logo link had no accessible name.** `<a href="/">` containing only
`<img alt="">` — a screen reader announced "link" and nothing else. SC 2.4.4 and
SC 4.1.2, Level A. The existing comment's reasoning (don't announce the brand
twice) was right and is preserved: the name is a visually-hidden span *inside*
the anchor; the image stays decorative. The tagline that names the brand is a
**sibling** of the anchor, so it never named the link.

**Cart focus could land on an `aria-hidden` element.** After a section swap the
last-resort focus target was the first focusable element in the line — which is
`.cart-line__media-link`, carrying `tabindex="-1" aria-hidden="true"` precisely
so it is *not* a stop. Focusing it strands a screen reader on an element it has
been told to ignore. The sweep now excludes `[aria-hidden="true"]` and prefers
the line's own quantity input.

**`aria-controls="CartDrawer"` was emitted on `/cart`**, where the layout
deliberately renders no drawer — pointing at an id that does not exist. It now
carries both conditions.

Unchanged and verified: 73 contrast measurements all passing; zero touch targets
under 24px across 17 pages × 12 viewports; `prefers-reduced-motion` covered;
global `:focus-visible` ring with no `outline: none` escapes.

---

## 13. Analytics audit

**There is no analytics in this theme, and that is the whole finding.**

Verified by search across all 72 files: no Meta Pixel, no Google Analytics or
Ads tag, no TikTok pixel, no chat widget, no reviews app, no social embed, no
third-party script of any kind, no `dataLayer`, no custom event dispatch.

So there is **no duplicate tracking, no fake purchase event and no consent
system to break** — the four things the brief warns about cannot occur. Shopify's
own analytics arrive through `content_for_header` and are untouched.

If a pixel is added later, the one rule that matters here: a purchase event must
come from Shopify's order-status integration, never from the theme observing a
cart or a checkout click.

---

## 14. Conversion UX findings

All 8 confirmed. These are the findings most entangled with business decisions,
and none is a code defect.

| Finding | Status |
|---|---|
| Hero CTA still renders nothing — no destination supplied | **BUSINESS DECISION** |
| Empty-cart and 404 buttons go to the home page, which has no product link as shipped | **BUSINESS DECISION** (§20) |
| Footer has no navigation columns as shipped | Merchant content, blocks exist |
| "Worldwide Shipping" is an unlinked sitewide commercial claim | **BUSINESS DECISION** — the theme cannot verify it |
| No policy, shipping or returns link on any purchase surface | `shop.policies` exists; the merchant must publish them |
| No contact route: no `page.contact` template | Missing template (§18) |
| Filtered-empty copy promised a control that was not rendered | **FIXED** |

The last one was mine, from Phase 13. When filters matched nothing, the copy read
*"Try removing one, or clear them all"* — and the filter controls and chips were
not rendered, because they sit inside the `paginate.items > 0` branch. It was
never a dead end (a prominent **Clear all** button is always there), but the copy
promised an action the page did not offer. The copy now matches the control.
Rendering the controls on a zero-result page is the better fix and is recorded in
§20; it requires hoisting the form as well, which restructures Phase 13's
single-form design.

---

## 15. Third-party scripts

| App / script | Purpose | Pages | Impact | Required | Recommendation |
|---|---|---|---|---|---|
| *(none)* | — | — | — | — | — |

The theme carries no third-party code. `content_for_header` is Shopify's own and
is untouched — the `ContentForHeaderModification` check passes.

**Search & Discovery** (Phase 13) is the one app the storefront depends on, and
it adds no storefront script: it populates `collection.filters` server-side.

---

## 16. Broken links and assets

Every reference the theme makes, resolved — and negative-controlled with four
seeded breakages, all caught.

| Kind | Referenced | Missing |
|---|---:|---:|
| `asset_url` | 23 | **0** |
| `render` (snippets) | 22 | **0** |
| sections (tags, JSON, groups) | 15 | **0** |
| translation keys used | 117 | **0** |
| translation keys defined but unused | — | **0** |
| literal internal hrefs | all | **0** unknown |

No orphaned asset, no orphaned snippet, no orphaned section (bar
`cart-icon-bubble`, which is reached by name through the Section Rendering API).

**Templates Shopify can route to that this theme does not have:** `article`,
`blog`, `gift_card`, `list-collections`, `password`. Each serves Shopify's error
page to anyone who reaches its URL. Phase 1 SHOP-09 tracks the same list; §20.

---

## 17. Mobile, desktop and browser results

**17 pages × 12 viewports (375 → 1920, plus two landscape): 0 hard problems** —
no horizontal overflow, no touch target under 24px, on any page at any width.

The account control measures 44×44 at every viewport and the header's end cluster
measures 148px at every viewport — unchanged from before Phase 15 touched it.

**Browsers:** Edge 153 and Chrome, both green on every browser-driven suite.
**Safari is untested** — unavailable on Windows. The two things most worth
checking there are the `position: fixed` cart scroll lock on iOS and `inert`
support.

**Console: 0 errors across 38 pages.**

---

## 18. Remaining confirmed findings, not fixed

48 of the 62 confirmed findings were not acted on. Every one is P2 or P3, and the
reason is the same in each case: Phase 16 says *optimize the existing experience,
do not rebuild*, and each of these is either a refactor of tested code, a
business decision, or a byte-level tidy with no measurable user benefit.

**Worth doing next, in order:**

1. **Pagination is implemented twice** under two class systems (`section-main-collection.css`
   and `section-main-search.css`), and they have already drifted — collection uses
   caption type, search uses uppercase label type. The file's own comment states
   the promotion trigger and the trigger has been met. → `component-pagination.css`.
2. **The container wrapper is copy-pasted into twelve rules across eleven
   stylesheets**, and `PHASE-2-DESIGN-SYSTEM.md` §674-681 specifies a `.container`
   utility that was never built.
3. **`.product-card__error` is defined twice**, and the loser's `padding` and
   `line-height` leak through, so the rule renders boxed where its own comment
   says left-ruled.
4. **Our Story and the hero declare `sizes="100vw"`** for boxes that are
   `object-fit: cover`, under-declaring the phone tier by roughly 1.9×.
5. **The header search form hardcodes `type=product`**, diverging from the
   search-types setting.
6. **One Escape closes two layers** — the search panel and the cart drawer install
   independent document-level handlers.

**Measured but deliberately unchanged:**

- **The homepage emits two duplicate stylesheet `<link>` tags** (two
  `featured-collection` sections each emit their own). Measured at the network
  layer: **11 CSS requests, not 13 — the browser deduplicates.** Zero extra
  requests. Promoting the stylesheets to the layout would push ~4KB onto four
  surfaces that do not need it, to save two `<link>` elements. Not a trade worth
  making.
- **`.variant-picker__swatch--square` is unreachable** — the snippet accepts a
  `swatch_shape` parameter and its only caller never passes it. Measured across
  26 pages, the sole genuinely dead selector in the theme. It is 40 bytes and a
  documented extension point; the adversarial verifier disagreed with this
  finding and my measurement stands against it. Recorded, not deleted.
- **40 of 192 design tokens are unreferenced.** A design system is allowed a
  vocabulary larger than its current usage.

---

## 19. Theme Check results

```
root:    god-squad-theme/        files scanned: 49        checks: 84

BEFORE                                  AFTER
4 offenses (default config)             2 offenses
  2 ERROR  ValidJSON                      2 ERROR  ValidJSON
  2 WARNING UnusedAssign                  — fixed

7 offenses (theme-check:all)            5 offenses
  3 ERROR  AssetSizeJavaScript             3 ERROR  AssetSizeJavaScript
```

**The two remaining `ValidJSON` errors are business information**, not code:
`theme_support_email` and `theme_documentation_url` in `theme_info`. They are
distribution metadata for themes shipped to other merchants; you chose bespoke in
Phase 15, so they have no functional effect here. Supply them and the default
config is clean.

**The three `AssetSizeJavaScript` errors** are §8 — real, quantified, and
answered with a recommendation rather than a restructure of tested cart code.

---

## 20. Shopify Admin actions required

1. **Upload a social sharing image** — *Theme settings › Brand › Social sharing
   image*, around 1200×630. Without it, shared links to non-product pages fall
   back to the logo, which crops badly.
2. **Upload a favicon** if none is set — it now feeds three icon sizes including
   the iOS home-screen icon.
3. **Decide the hero CTA destination** and the empty-cart/404 destination. Both
   currently fall back to the home page, and the home page as shipped has no
   product link. `/collections/all` is servable now that a collection template
   exists.
4. **Publish the policies** — *Settings › Policies*. `shop.policies` is available
   to the footer the moment they exist; until then no purchase surface can link
   them.
5. **Supply `theme_support_email` and `theme_documentation_url`** to clear the
   last two Theme Check errors.
6. Carried forward: **Search & Discovery filters** (Phase 13), **checkout
   branding** (Phase 14), **confirm the customer-account system** (Phase 15).

---

## 21. Performance budget

Set from what this theme actually measures today, not from a round number.

| Budget | Current worst | Target | Basis |
|---|---:|---:|---|
| JavaScript, all pages | 22.0 KB gz | **≤ 30 KB gz** | zero dependencies; only a new feature should move it |
| JavaScript, per page-load script | 12.1 KB gz | **≤ 10 KB gz** | Shopify's own `AssetSizeJavaScript` threshold |
| CSS, worst page | 50.2 KB gz | **≤ 55 KB gz** | 11 stylesheets on the homepage |
| Requests, worst page | 24 | **≤ 30** | measured 19 at the network layer |
| Load CLS | 0.0125 | **≤ 0.05** | half of Google's "good" |
| Theme handler time | 0.00 ms | **≤ 50 ms** | one component of INP |
| Eager images per page | 1 | **exactly 1** | the LCP element and nothing else |
| `fetchpriority="high"` per page | 1 | **≤ 1** | |
| Third-party scripts | 0 | **each one justified in writing** | |

---

## 22. Testing results

```
=== Phase 16 (new) ===
images        54 / 54     the pipeline, on rendered markup
seo           52 / 52     head, social, fonts, headings
refs          10 / 10     every reference resolved (+4 seeded breakages caught)
facetsgate    10 / 10     the P0, reproduced then fixed
cssuse        497 selectors measured across 26 pages
weight        7 surfaces  requests and bytes
vitals        6 surfaces  LCP element, load CLS, handler cost, long tasks
themecheck    49 files, 84 checks

=== regression, every prior phase ===
validate     199/199   surfaces  41/41   catalog     55/55   facets    62/62
cartdoc       84/ 84   accounts  52/52   settings    28/28   layout    19/19
editor        10/ 10   cardcascade 10/10
interact      49       interact_cartpage 17    interact_product 26
cartqa        14       notes     40      lifecycle   18
negctl        22 violations seeded, 22 caught
contrast8     73 measurements, 73 pass
respond       17 pages x 12 viewports — 0 hard problems
console       38 pages — 0 errors
```

**945 assertions, 0 failures**, plus 22 seeded violations, 204 viewport
measurements, 497 measured CSS selectors and 38 console checks.

### 22.1 Four measurement errors caught before they reached this document

Worth recording, because each would have produced a confident and wrong number:

1. **LCP by observer** named a 78px logo as the collection page's largest paint.
   The harness has no image files; every image 404s. Reading discarded, replaced
   with a static attribute audit.
2. **CLS counted my own clicks.** Synthetic `dispatchEvent` does not set
   `hadRecentInput`, so drawer-opening shifts were scored as load instability.
   Load and interaction shift now measured separately.
3. **CSS coverage reported 100%**, including two deliberately dead selectors.
   Pages on the second port are cross-origin, `contentDocument` threw, and the
   catch marked every selector as seen. Also: the selector extractor split
   `:where(a, button)` on its internal commas, and took only the last line of
   multi-line selector lists.
4. **The reference resolver called `grid-sizes` an orphan.** Inside a
   `{% liquid %}` block `render` is a bare statement with no tag around it.

---

## 23. Files created

| File | |
|---|---|
| `snippets/meta-social.liquid` | Open Graph and Twitter card, every value from a Shopify object |

The theme is now **72 files**.

Test suites, in `scratchpad/phase16/`: `themecheck.mjs`, `weight.py`,
`vitals.py`, `images.py`, `seo.py`, `cssuse.py`, `refs.py`, `facetsgate.py`.

---

## 24. Files modified

| File | Change |
|---|---|
| `layout/theme.liquid` | Jost 500/600 faces; social metadata; apple-touch-icon + 192px icon |
| `assets/facets.js` | **P0** — width gates the drawer; `open()` refuses above `--bp-md` |
| `assets/component-facets.css` | **P0** — the trigger is retired at `min-width: 768px` |
| `assets/cart.js` | Focus never lands on an `aria-hidden` element |
| `sections/header.liquid` | `aria-controls` not emitted on `/cart` |
| `sections/footer.liquid` | The logo link is named |
| `sections/featured-collection.liquid` | Orphaned `step` assign removed |
| `snippets/product-media-gallery.liquid` | Orphaned `loading_attr` removed; eager/priority follow the active slide |
| `config/settings_schema.json` | `share_image` setting (Brand) |
| `config/settings_data.json` | `share_image` in current + preset |
| `locales/en.default.json` | Filtered-empty copy matches the control offered |

---

## 25. Known limitations

1. **No Lighthouse.** Not installed, no network to install it. No score is
   claimed anywhere in this document.
2. **No real Core Web Vitals.** LCP/FCP/TTFB timings and field INP need a live
   store and real users. What could be measured was measured; what could not is
   named in §1.1 rather than estimated.
3. **Font-swap CLS is unmeasurable here** — the harness has no font files. This
   matters more after §9, which added two faces: **verify CLS on a real store**.
4. **Safari untested.** Edge and Chrome are both Chromium, so cross-browser
   coverage mainly rules out harness artifacts.
5. **No merchant photography exists.** Image *bytes* — the largest real
   contributor to page weight — cannot be measured. Phase 3 recorded sourcing as
   the ceiling and it still is.
6. **48 confirmed P2/P3 findings remain open** (§18), deliberately.
7. **Two Theme Check errors remain**, both business information (§19).
8. **Five storefront templates are still missing** (§16), each an error page for
   anyone who reaches its URL.

---

## 26. Future recommendations

- **Add a deploy-time minification step.** It would clear the three
  `AssetSizeJavaScript` errors without touching a line of tested logic, because
  the code is 4.9KB gzipped and the comments are 7.1KB. This is the single
  highest-value change available and it is a tooling decision, not a code one.
- **Do §18's top three** — the duplicated pagination, the twelve-times-copied
  container, and the double-defined card error. All three are consolidations of
  code that already works, and the first two are the theme drifting from its own
  written rules.
- **Ship the missing templates**, `password` first if the store will ever go
  behind a password page, then `page.contact`, `list-collections`, `blog` and
  `article`.
- **Revisit Organization JSON-LD** once the social URLs and a contact route
  exist. Not before: an Organization block whose `sameAs` is empty is worse than
  none.
- **Render the filter controls on a zero-result collection** (§14), so a customer
  can adjust one filter instead of clearing all of them.
- **Measure on the real store** — CLS after the font change, the account sheet's
  position, and one Lighthouse run per template.

---

**STOP AFTER PHASE 16.**
