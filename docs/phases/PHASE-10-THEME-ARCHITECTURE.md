# GOD SQUAD — PHASE 10: SHOPIFY THEME ARCHITECTURE + CONVERSION

Phase 10 deliverable. Built against the Phase 10 brief as issued, `PHASE-1-WEBSITE-AUDIT.md` §29
(the recommended tree, which this phase treats as the authoritative target), `PHASE-2-DESIGN-SYSTEM.md`
§30 (the two colour guardrails assigned to this phase by name), and the sections delivered in
Phases 4–9.

Status: **delivered**. The theme is a complete, valid Online Store 2.0 theme with every storefront
surface a shopper can reach. 405 automated assertions pass, across eleven rendered pages at twelve
viewports each, with no console error on any of thirty-three pages.

The central finding of this phase is that **the conversion was already done**. Phases 2–9 built
natively rather than porting, so the brief's three prohibitions — do not upload the prototype, do
not wrap it in one giant Liquid file, do not rebuild the site as one `theme.liquid` — were already
satisfied before Phase 10 began. What Phase 10 actually did was finish the theme, fix two
production defects that had survived nine phases, and close the testing blind spot that let them
survive.

---

## 1. Verdict

**Was this already a valid OS 2.0 theme?** Yes. `layout/theme.liquid` was 187 lines of which about
half were comments, with no page content inlined anywhere; the header already rendered through a
real section group; all three JSON templates were well formed; all eight `{% schema %}` blocks
parsed; and every `asset_url`, `render` and `| t` target resolved.

**Would it have uploaded to Shopify?** Yes. shopify.dev is explicit that only `layout/theme.liquid`
is required for upload, and that file satisfied `RequiredLayoutThemeObject`.

**Could a merchant have run the store?** No — and this is the gap Phase 10 closed. Three things
stood in the way, in descending order of damage.

1. **The brand typefaces never loaded, on every page, and raw CSS rendered above the logo.**
2. **The logo broke the first time a merchant uploaded one.**
3. **Four page types a real shopper reaches had no template at all**, so the header's own navigation
   led to Shopify's error page from every page of the site.

---

## 2. The two production defects

Both had been live since Phase 4. Both are in §9 with their fixes; they are called out here because
they are the reason this phase exists in the form it took.

### 2.1 `font_face` emitted outside a style element

`layout/theme.liquid` carried:

```liquid
{{ settings.type_display_font | font_face: font_display: 'swap' }}
{{ settings.type_body_font | font_face: font_display: 'swap' }}
```

`font_face` returns a bare `@font-face` **rule**, not a style element. Emitted unwrapped this did
two things on every page of the store:

- **No face was ever registered.** Playfair Display and Jost never loaded, and every heading and
  every line of body copy fell back to a generic family. The entire Phase 2 typography was absent
  storewide.
- **The CSS text rendered as visible page content.** Per the HTML parser's "in head" insertion mode,
  a non-whitespace character token ends `<head>`. So the rule's text appeared above the logo, and
  everything after it in source order — `content_for_header`, all five stylesheets, the `:root`
  block and both scripts — was parsed in body context.

Fixed by wrapping both calls in `{% style %}`, which shopify.dev documents as generating a
`<style data-shopify>` element, and which is the form Dawn uses for this filter.

### 2.2 Ruby-style interpolation in the logo style attribute

`sections/header.liquid` built the logo's inline style with `"--logo-height-desktop: #{logo_h_desktop}px"`.
**Shopify Liquid does not interpolate inside a string literal.** The documented way to build a
string is the `append` filter.

The failure is not a harmless no-op. A custom property accepts almost any token sequence, so
`--logo-height-mobile: #{logo_h_mobile}px` was a *valid declaration with a garbage value*, set on
the `<img>` itself — where it shadowed the good `:root` defaults in `design-tokens.css`.
`header.css` then resolved `height: var(--logo-height-mobile)` to that garbage, which is invalid at
computed-value time, so `height` fell back to its initial value `auto` and the logo drew at its
intrinsic size.

It only bit once a logo was uploaded, because with the setting empty the section takes its
text-wordmark branch. That is the merchant's first Customize action.

Fixed by building the string with `append`.

**This corrects a Phase 8 conclusion.** In Phase 8 the mini-Liquid harness did not interpolate
`#{}`, which produced a 133px logo and a horizontal overflow at 320px. That was diagnosed as a
*harness* bug and the harness was taught to interpolate. It was not a harness bug. Teaching the
harness to interpolate did not fix anything; it hid a theme bug, and hid it for two phases. The
harness has been corrected in both copies, with the reasoning recorded in the file.

---

## 3. Why nine phases missed them

**The harness had never executed `layout/theme.liquid`.** Every suite from Phase 4 onward rendered
*sections* against a hand-written page template. The real layout — the file both defects lived in —
was never once run.

Phase 10 closes this with `layout.py`, which renders the actual layout and parses the result with a
model of the HTML "in head" insertion rule. It asserts, among other things, that no raw text is
emitted directly into `<head>`, that every `@font-face` sits inside a `<style>`, that every layout
stylesheet is in the head, that every referenced asset exists on disk, and that the cart-page drawer
guard still holds.

The first version of that suite **passed with the bug present**. `font_face` was stubbed to return
`''` and the harness defined no font settings, so there was nothing to emit in either case. A test
that cannot fail proves nothing, so the filter was made to emit a real `@font-face` rule and the
harness was given real font settings. The suite was then verified by reverting the fix and
confirming two checks fail with exact evidence, before restoring it. Every fix in this phase that
could be negative-controlled, was.

---

## 4. The architecture

### 4.1 The theme now has its own root

Both the Phase 10 brief's target tree and Phase 1 §29.1 root the theme at `god-squad-theme/`. Until
this phase the theme files sat in the project root, intermixed with the prototype, ~17 MB of loose
imagery, and the phase documents. Phase 1 is explicit that nothing from `images/` or the project
root is copied across, and that the non-theme files stay in the archived prototype.

49 files were relocated into `god-squad-theme/`, verified by file count before and after, with the
prototype originals confirmed byte-identical afterwards by the Phase 8 integrity check.

```
GodSquad Website/                  the project
├── god-squad-theme/               THE THEME — this is what uploads to Shopify
├── God Squad Website.html         the frozen prototype, read-only reference
├── images/  uploads/  phase-3-assets/
├── PHASE-0..PHASE-10 .md          the phase documents
└── PHASE-3-ASSET-MANIFEST.csv
```

### 4.2 The theme

66 files.

```
god-squad-theme/
├── assets/      21   design-tokens.css, base.css, 5 component-*.css,
│                     9 section-*.css, 3 *.js
├── config/       2   settings_schema.json, settings_data.json
├── layout/       1   theme.liquid
├── locales/      1   en.default.json (101 keys)
├── sections/    16   14 sections + header-group.json + footer-group.json
├── snippets/    18   icon-*, product-card, product-media-gallery,
│                     product-variant-picker, quantity-selector, cart-*,
│                     css-variables
└── templates/    7   index, product, collection, page, cart, search, 404
```

**No `blocks/` directory.** Theme blocks are an optional newer capability, not a requirement; Dawn's
`main` has no `blocks/` either, and nothing in this theme needs them. The brief's own tree says
"reusable theme blocks **where genuinely useful**". There is no such case here. This is a decision,
not an omission.

**No `templates/customers/*`.** Those are for classic customer accounts, which are superseded.
Publishing without them leaves the merchant on Shopify's hosted new customer accounts, which is the
better outcome; adding them would be a downgrade. The header already carries a sign-in entry point
at `routes.account_url`.

**`assets/` holds only CSS and JS.** Content imagery is not a theme asset: hero, story and product
images reach the page through `image_picker` settings and product media, so Shopify can resize them
per width with `image_url`. The correct treatment of `images/`, `uploads/` and `phase-3-assets/` is
exclusion, not relocation.

### 4.3 `base.css`

Phase 1 §29.1 and the brief's tree both name `base.css`. Before this phase the reset, the focus ring
and the reduced-motion suppression sat at the bottom of `design-tokens.css` — a file that should
define custom properties and nothing else.

The split is drawn so that **no token definition moved**: `design-tokens.css` keeps every `:root`
assignment including the two gutter breakpoints and the reduced-motion token overrides, because
splitting one token's definition across two files would be worse than the misnomer. `base.css` takes
only the rules that style *elements*, and is loaded immediately after the token file because it
consumes those tokens.

`base.css` contains the only four real `!important` declarations in the entire theme, all inside the
`prefers-reduced-motion` block, where a user preference must beat an author declaration — which is
the one thing `!important` is actually for. Verified by stripping comments from all 21 assets and
counting.

**`theme.css` was deliberately not created.** The brief's tree names it, but there is no third layer
to put in it, and Phase 9 §12 recorded the per-section stylesheet architecture as a deliberate
choice that the brief's own "do not create one enormous mobile.css" endorses. An empty or
duplicative file would be churn against a recorded decision.

---

## 5. The five storefront surfaces

Before this phase the theme had three working URLs — home, product and cart — and nearly every
navigation path out of them landed on Shopify's error page. Phase 1 §29.5 had already recorded the
rule: *"Shopify serves an error page for a storefront route whose template is missing, so the full
storefront set must exist even where the design is minimal."*

Live links that went nowhere: the "View all" CTA on both home rows (`collection.url`), the header's
search control (on by default, `routes.search_url`), the account control, and four of the five
top-level navigation links.

| Surface | Files | What it does |
|---|---|---|
| **Collection** | `main-collection.liquid`, `section-main-collection.css`, `collection.json` | The catalogue browse surface. Banner, native sort, pagination, the shared `.product-grid` and `product-card` snippet, and a real empty state. |
| **Page** | `main-page.liquid`, `section-main-page.css`, `page.json` | Merchant prose — About, size guide, shipping, returns. The stylesheet's substance is styling the elements Shopify's rich-text editor can emit, inside the theme's type scale and measure. |
| **404** | `main-404.liquid`, `section-main-404.css`, `404.json` | Every dead link, deleted product and shared sold-out URL. All copy is merchant-editable with neutral defaults. |
| **Search** | `main-search.liquid`, `section-main-search.css`, `search.json` | A real `role="search"` GET form with a labelled `q` input — the header's search control had no form anywhere in the theme. Handles three states: no query, results, zero results. |
| **Footer** | `footer.liquid`, `section-footer.css`, `footer-group.json` | The first footer the theme has had. `<footer role="contentinfo">`, merchant-editable blocks, Shopify policy links, and a copyright line built from `shop.name` and `'now' | date` — never a hardcoded year. |

Two things about how they were built.

**They reuse rather than re-declare.** The collection and search grids are the same `.product-grid`
and the same `product-card` snippet the home page uses, so a card looks identical everywhere and
Phase 9's grid work applies to all three surfaces for free. Measured: the collection grid renders
two columns of 156px at a 16px gap on a 375px phone — identical to the home grid — and four columns
at 1440.

**The footer's landmark is written out, and its schema `tag` is `div` on purpose.** `<footer>` maps
to the `contentinfo` role only while it is not a descendant of `article`, `aside`, `main`, `nav` or
`section`; a `section` wrapper would have silently demoted the site's only `contentinfo` to a
generic group.

### 5.1 The footer's default copy is approved copy

`footer-group.json` ships two strings: "Different People. Same Purpose." and "A Brighter Tomorrow".
Both were checked against the source before acceptance — they are prototype lines 156 and 164, and
Phase 1 §16 records both as the footer's existing content. Nothing was invented.

---

## 6. Theme Editor and the colour guardrails

Phase 1 SHOP-03 assigns the global settings surface (§29.6) to this phase; Phase 11 owns the
per-section schemas and blocks (§29.7). Phase 2 §30 assigns two guardrails to this phase by name:

> **G1 — the colours cannot be free pickers.** A Shopify `color` setting is unconstrained;
> `settings_schema.json` has no validation hook and no on-save callback, so there is no mechanism to
> check a ratio at save time.
>
> **G2 — a gold scheme must ship its light-surface partner.** `--color-accent-strong` `#82672B` is a
> fixed hex, not computed from the gold. Changing the gold token alone leaves the light-surface
> accent behind.

Both are answered the same way. The three free pickers are replaced by a **colour scheme select**,
and the scheme is resolved in exactly one place — `snippets/css-variables.liquid`, the snippet
Phase 1 §29.2 specifies by name — which emits the gold and its light-surface partner together, so
the two cannot desynchronise.

Every ratio in the system was **recomputed in this phase** from WCAG 2.2 relative luminance rather
than copied. Phase 2 §3 is exact to the second decimal:

| Pairing | Phase 2 | Recomputed |
|---|---|---|
| cream on ink | 17.04:1 | 17.04 |
| cream-200 on ink | 15.41:1 | 15.41 |
| gold on ink | 11.01:1 | 11.01 |
| gold-hover on ink | 13.25:1 | 13.25 |
| stone on ink | 9.70:1 | 9.70 |
| ink on cream | 17.04:1 | 17.04 |
| gold-strong on cream | 4.66:1 | 4.66 |
| gold on cream — **fails** | 1.55:1 | 1.55 |
| gold on tile cream — **fails** | 1.43:1 | 1.43 |

**One scheme ships, and that is a deliberate limitation.** G1 asks for "a fixed select of
pre-verified schemes", but only one palette is brand-approved, and inventing alternates would be the
identity redesign every phase has been forbidden. The select exists so a second scheme is additive
rather than a refactor, but adding one is **not an engineering decision**: it needs brand approval of
the colour values and a measurement pass across the §3 matrix.

The `css-variables` snippet takes a `part` parameter and is rendered twice, because the scheme has
two head outputs that cannot sit together: the `theme-color` meta belongs early, and the style
element must come *after* the stylesheets or its `:root` declarations lose to `design-tokens.css`.
Resolving the scheme twice in two places is exactly the desynchronising G2 exists to prevent.

### 6.1 Settings now exposed

`theme_info`, Colours (the scheme), Typography, Layout, Products, Brand (favicon), and **Social**
(Facebook and Instagram URLs, blank by default). The Social area was added because `footer.liquid`
reads `settings.social_facebook_url` and `settings.social_instagram_url`, and the schema had no
`social` key at all — so the social row could never have rendered. Each link is emitted only when its
URL is set, so the footer never shows a link that goes nowhere.

`theme_documentation_url` and `theme_support_url` shipped as empty strings against a schema that
types them `format: uri`, which was the theme's only Theme Check ERROR. Both keys are optional, so
they are now omitted rather than filled with a fabricated URL. **Supply real URLs and they can be
restored.**

---

## 7. Testing

| Suite | What it covers | Result |
|---|---|---|
| `validate.py` | Structure, schemas, tokens, translations, prototype integrity | 197 checks, 197 pass |
| `interact.py` | Cart drawer behaviour in a real browser | 49 assertions, 0 fail |
| `interact_cartpage.py` | Cart page behaviour | 17 assertions, 0 fail |
| `interact_product.py` | Product page behaviour | 26 assertions, 0 fail |
| `contrast8.py` | Measured contrast on rendered pixels | 56 measurements, 56 pass |
| `layout.py` | **new** — the real `layout/theme.liquid`, parsed | 19 checks, 19 pass |
| `surfaces.py` | **new** — the five new sections in every state | 41 checks, 41 pass |
| `respond.py` | 11 pages × 12 viewports | 0 overflow, 0 sub-24px targets |
| `console.py` | Console and Liquid errors | 0 errors across 33 pages |

**405 assertions.** Three harness capabilities were added to make this possible.

- **`{% paginate %}` was unimplemented** and raised. Two of the five new surfaces cannot render
  without it, so neither could be rendered even once until it was built. It now models Shopify's
  semantics: the paginated expression yields only the current page's items inside the block, and a
  `paginate` object carries the counts and link parts.
- **`font_face` was a stub returning `''`.** It now emits a real rule — see §3.
- **Asset copying and translation scanning were hand-written lists.** Both now *discover* instead.
  This was not cosmetic: the surface stylesheets were never copied into the harness, so the first
  responsive run measured the new surfaces **unstyled** and reported 17px footer links and a 19px
  select as real defects. With the CSS actually served, those measured 24px and the sort control
  passed. Every "defect" a harness reports is worthless until you have proved the harness is serving
  what the theme references.

---

## 8. Review

The five surfaces were put through an adversarial review, one reviewer per surface, each checking
Liquid correctness, schema validity, house style, reuse, invented content, hardcoded strings,
accessibility, responsiveness, and whether the builder's own report matched the files. **44 defects
were raised: 3 blockers, 15 major, 26 minor.** Each blocker and each major acted on below was
verified against the files and the cited documents before being fixed.

---

## 9. Issues found and fixed

| # | Severity | Issue | Fix |
|---|---|---|---|
| 1 | **P0** | `font_face` emitted outside a style element: fonts never loaded and raw CSS rendered on every page | Wrapped in `{% style %}` |
| 2 | **P0** | `#{}` interpolation broke the logo on the merchant's first upload | Built with `append` |
| 3 | **Blocker** | Collection's desktop `sizes` clause fired at 976px, below the 1024px breakpoint where the desktop grid applies — a 38% under-declaration | Threshold floored at the tier boundary |
| 4 | **Blocker** | Footer claimed a four-column ceiling; two block types at limits 4 and 2 allow **six**, giving 128px tracks at 1024 | `repeat(auto-fit, minmax(11rem, 1fr))` — wraps to rows instead of thinning |
| 5 | **Blocker** | `footer-group.json` bound Shopify's auto-created `footer` menu, printing `<h2>Footer menu</h2>` — admin vocabulary — on every page, duplicating the policy row | Ships with no menu bound |
| 6 | **Major** | The footer's social row could never render: no `social_*` settings existed | Social area added to `settings_schema.json` |
| 7 | **Major** | Social links at 24px, but Phase 2 line 2126 sizes this row explicitly at 44px | `--target-min` box |
| 8 | **Major** | Search uppercased the customer's own search term, destroying the casing they typed | Body treatment, term echoed as typed |
| 9 | **Major** | Page prose had no `overflow-wrap`: an unbreakable token made a 375px viewport **590px wide** | `overflow-wrap` on the content root |
| 10 | **Major** | Sort select auto-submitted on change and hid its button — WCAG **SC 3.2.2 On Input, Level A**. A keyboard user arrowing through options navigated on every option | Button submits; the section now ships **zero JavaScript** |
| 11 | **Major** | Search's "other results" link measured 21px, under the 24px floor, with no equivalent large target beside it | `--target-min` |
| 12 | Minor | `theme_documentation_url`/`theme_support_url` empty strings — the only Theme Check ERROR | Omitted |
| 13 | Minor | Stale comment attributing the footer to "Phase 16" | Corrected; Phase 16 is FINAL POLISH |

Items 3–11 were each verified against the files before being fixed; items 9 and 1 were additionally
negative-controlled, by reverting the fix and confirming the test fails.

---

## 10. Issues recorded, not fixed

Thirty-three review findings are recorded and deliberately not acted on in this phase. They fall
into three groups.

**Duplication that wants a shared snippet (major).** `main-search.liquid` repeats roughly 100 lines
of the `sizes` derivation from `main-collection.liquid`, and `main-collection.liquid` re-declares an
empty-state pattern `cart-empty-state.liquid` already solves. Both are real maintainability defects
against the brief's "modular, reusable, maintainable" objective. Extracting a shared `grid-sizes`
snippet and a shared empty-state snippet is the right fix and is a refactor across four files, which
wants its own pass rather than being done at the end of this one.

**Comment-accuracy findings (minor).** Several comments in the new surfaces cite a document section
slightly wrong, restate a precedent more strongly than the source does, or claim a property the
declaration does not have. This codebase holds comments to the same standard as code, so these are
genuine, but none changes rendered behaviour.

**One false positive.** A reviewer reported the footer builder's claim "I edited no shared files" as
dishonest because `locales/en.default.json` contained its keys. The builder was truthful: **I** merged
those keys, between the build and the review. The reviewer could not have known that.

Also carried: `component-product-card.css` now has three consumers (featured-collection,
main-collection, main-search), and the theme's own house rule is that a stylesheet with more than one
consumer moves to the layout. It is not double-linked on any single page, so this is a convention
question rather than a defect, and moving it would load card CSS on pages with no cards.

---

## 11. Known limitations

**One colour scheme.** Explained in §6. Adding a second needs brand-approved values and a
measurement pass.

**No real Shopify store.** Everything here is measured against mock Shopify data through a strict
mini-Liquid interpreter and headless Edge. The theme has not been uploaded to a development store,
so Section Rendering API behaviour, real `content_for_header` output, real image CDN behaviour and
Theme Check itself remain unverified against the platform.

**`theme_documentation_url` / `theme_support_url` are absent** pending real URLs.

**Social URLs are absent** pending the brand's actual profile addresses. Phase 1 records both
prototype social links as `href="#"` with no URLs supplied. The settings exist and are blank.

**No `list-collections`, `blog`, `article`, `password` or `gift_card` template.** Phase 1 §29.5
classifies each as OPTIONAL or BUSINESS DECISION REQUIRED. None is referenced by anything the theme
renders, so none was built speculatively.

**Collection filtering and faceting were not built.** Phase 6 deferred it and Phase 10's scope
confirmed sort-only. The section is built so filters are additive: the `{% paginate %}` block and the
GET form are already in place.

**The pagination link URLs are `?page=N` as modelled by the harness.** On a real store Shopify
supplies `paginate.parts` with its own URLs; this has not been verified against the platform.

---

## 12. Explicitly not in Phase 10

Assigned elsewhere by the Phase 1 dependency map, and deliberately left alone:

- **Open Graph, JSON-LD, the title pattern and meta description** → Phase 13 (SEO). DEBT-08,
  SEO-01, SEO-02.
- **The full per-section settings surface and block schemas (§29.7)** → Phase 11 (Theme Editor).
  SHOP-02.
- **An axe pass and a full keyboard audit** → Phase 14 (Accessibility). DEBT-09.
- **Core Web Vitals, font preloading and self-hosting** → Phase 12 (Performance). PERF-03 is gated
  on the unresolved self-hosting question.
- **Predictive search** → ECOM-03, later.
- **A newsletter block in the footer** → out of scope for this phase.
- **`locales/en.default.schema.json` and `t:` schema keys.** Converting 236 merchant-facing schema
  strings to translation keys without shipping the schema locale file in the same change turns a
  non-defect into an error. Both halves belong together, in Phase 11, which owns the Theme Editor
  surface.

---

## 13. Handoff to Phase 11

Phase 11 is THEME EDITOR, and owns §29.7: the per-section schemas, blocks and
`block.shopify_attributes`, agreed with the owner before build (RISK-11).

Four things are waiting for it:

1. **The `t:` schema keys and `locales/en.default.schema.json`**, shipped together.
2. **A second colour scheme**, if the brand wants one — values plus measurement.
3. **The shared `grid-sizes` and empty-state snippets**, which would remove the duplication in §10.
4. **`theme_documentation_url`, `theme_support_url` and the two social URLs** — business information,
   not engineering.

Phase 10 stops here.
