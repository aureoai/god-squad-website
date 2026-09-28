# GOD SQUAD — PHASE 11: THEME EDITOR + MERCHANT CUSTOMIZATION

Phase 11 deliverable. Built against the Phase 11 brief as issued, `PHASE-1-WEBSITE-AUDIT.md` §29.6
(global settings areas), §29.7 (per-section schemas — the target Phase 1 assigns to this phase by
name via SHOP-02) and §29.8 (*"What stays static"*, which is RISK-11), and the sections delivered in
Phases 4–10.

Status: **delivered**. **443 automated assertions pass**, across twelve rendered pages at twelve
viewports each, with no console error on any of thirty-four pages.

The headline finding is that the merchant surface was already most of the way there. A seven-cluster
audit against the brief scored the theme at **12 of the spec's 16 merchant tasks passing before this
phase began**. What failed clustered in three places — global brand plumbing, global cart behaviour,
and two of the spec's own "must offer" lists — plus a set of editor-runtime defects that no
storefront test could see.

---

## 1. Global settings

`config/settings_schema.json` now carries eight groups. The whole global surface is **eleven
settings**, which is the point: Phase 1 §29.8 and the brief's closing rule both say the brand reads
as premium only while the composition stays tight.

| Group | Settings | Notes |
|---|---|---|
| `theme_info` | God Squad, v0.5.0 | |
| **Brand** | `logo`, `favicon` | **New in Phase 11.** The logo moved here from the header section. |
| **Colours** | `color_scheme` | Relabelled **"Brand palette"** so it stops colliding with every section's own "Colour scheme". |
| **Typography** | `type_display_font`, `type_body_font` | Two pickers, not fifty. |
| **Layout** | `container_width`, `radius_sm` | One page width for the whole theme. |
| **Products** | `product_image_ratio` | One catalogue ratio, deliberately global. |
| **Cart** | `cart_type` | **New in Phase 11.** Slide-out drawer or cart page. |
| **Social** | `social_facebook_url`, `social_instagram_url` | Blank; a row renders only when its URL exists. |

### 1.1 The logo is uploaded once

Before this phase the only logo control in the theme was an `image_picker` on the **header section**,
and `sections/footer.liquid` recorded the consequence in its own comment: a section cannot read
another section's settings, so a footer wordmark would have meant uploading the same asset twice —
and the file ended *"Promoting the logo to a theme setting is the fix, and it belongs with whoever
owns that file."* That is this phase.

`settings.logo` now feeds the header and the footer. The header keeps its two **size** controls,
because how large the mark sits in each bar is a per-section decision; the upload is not.

**The migration cost was exactly zero, and only today.** `sections/header-group.json` stores the two
height ranges and no `logo` key, because no logo has ever been uploaded. Shopify does not migrate a
section setting to a theme setting, so the day a merchant uploads one, moving it becomes a forced
re-upload. Doing it now costs nothing; doing it in Phase 12 costs the merchant their logo.

That comment in `footer.liquid` also mis-cited **INV-04** for "the duplication". INV-04 is the
asset's raster quality and URL-unsafe name; the duplicate-file id is DUP-04, and neither actually
described a second upload field. Corrected in the same edit.

### 1.2 The cart can be a drawer or a page

`cart_type` gates `{% section 'cart-drawer' %}` in the layout. That is the entire switch, because
`assets/cart.js` was already written to tolerate an absent drawer:

- `onOpenerClick` returns early when `Drawer.el` is null, so the header control stays what it is
  without scripting — an ordinary link to `routes.cart_url`;
- `Drawer.open()` guards on `this.el`;
- the add-to-cart path gates auto-open on `Drawer.el` explicitly.

Phase 10 fork F6 declined this switch, on the grounds that Phase 8 recorded the cart page as
deliberately lean. The Phase 11 brief names cart behaviour as a scope item and Phase 1 §29.6 names
`cart_type` twice, so the decision is reversed here — and §29.8 does not list it among the things
that must stay static.

### 1.3 One palette, and why

`Colours` offers a single verified scheme. The brief sanctions *"a small, intentional set. Example:
Dark, Light, Dark Gold Accent"* — but all three of those are **already reachable**, through each
section's own `surface` control and the surface-aware `--accent-current`. A *second global palette*
would mean new colour values, which is a brand act rather than an engineering one, plus a
measurement pass across the 56-assertion contrast suite.

So Phase 11 changed the label, not the mechanism. Phase 10's guardrails G1/G2 stand: the scheme is
resolved in exactly one place and emits the gold with its light-surface partner `#82672B` together,
so an illegal pairing is structurally impossible.

---

## 2. Section settings

**100 settings across 13 sections.** Every one already used a correct Shopify setting type before
this phase — `collection`, `link_list`, `image_picker`, `url`, `range`, `select`, `checkbox`. There
is not one handle text field or pasted CDN URL anywhere in the theme.

| Section | Settings | Blocks | Presets |
|---|---|---|---|
| announcement-bar | 2 | message (3) | 1 |
| header | 8 | — | — |
| hero | 14 | — | 1 |
| featured-collection | 19 | — | 2 |
| our-story | 14 | value (6) | 1 |
| footer | 6 | link_list (4), text (2) | — |
| main-product | 9 | — | — |
| main-collection | 10 | — | — |
| main-search | 6 | — | — |
| main-page | 4 | — | — |
| main-cart | 2 | — | — |
| main-404 | 2 | — | — |
| cart-drawer | 4 | — | — |

### 2.1 What Phase 11 changed

**The announcement bar** was the weakest schema in the theme: one setting. It gained an
**alignment** control, which the brief names among its four required controls. Both target states
already existed in shipped CSS — centred below the tablet tier, spread to the edges above it — and
neither was reachable from the editor. It is labelled "Alignment on desktop" because below `--bp-md`
the bar always stacks and centres; a phone has no width to distribute across, and a setting that
silently does nothing on the most common viewport would be worse than none.

**Its colour control was also the odd one out.** Seven sections label this setting "Colour scheme"
with options *Cream* / *Ink*; the announcement bar called it "Surface" with *Dark (near black)* /
*Light (warm cream)* — the same concept in two vocabularies. Now consistent.

**The header** gained **Show cart**. The audit recommended declining it, on the grounds that hiding
the only header path to the cart is closer to the brief's *"do not expose settings that can break
the purchase flow"* than to merchant flexibility. The brief lists it explicitly under HEADER, so it
ships — with the cost written into the setting's own `info` text: *"With it off the header has no
cart control at all, and a customer who has added something can only reach the cart by typing the
address."*

**The hero's focal point** now tells the truth. "Focal point on narrow screens" is overridden — 
silently — on any image whose focal point the merchant set in Shopify admin, because `image_tag`
emits an inline `object-position` that outranks the stylesheet. That is the same mechanism Phase 7
recorded and Phase 8 hit again. The control is not dead: it governs whenever no admin focal point
exists, which is the default. Removing it would have changed the approved centre-left composition,
so the proportionate fix was to say so in the `info` rather than delete a composition control.

**The footer** gained **Show the logo**, fed by the new global setting and sized by
`--logo-height-footer`, a token that has been in `design-tokens.css` since Phase 2 waiting for it.
It renders only when the merchant asks for it **and** a logo exists — a checkbox that produces an
empty gap is worse than no checkbox.

### 2.2 A setting that could break the purchase flow

`main-product.liquid` wrapped the **only** quantity input in `{% if section.settings.show_quantity %}`.
Turning that presentation setting off submitted **no quantity at all**. Shopify then defaults to 1,
which is correct for most products and wrong for any variant whose `quantity_rule.min` exceeds 1 —
the add is rejected with a 422 the customer cannot act on. Phase 8 deliberately publishes
`quantity_rule` in the variant table, so the theme supports exactly those products.

The hidden branch now submits `qty_min`, and carries `data-quantity-input` so `product.js`'s
`updateQuantityRule` keeps it in step on a variant change through the same hook the visible control
uses. That function already guards its stepper update with `if (control)`, so the wrapper-less hidden
input is safe.

This is the brief's own rule — *"Do not expose settings that can break the product purchase flow"* —
and it was being broken by a setting that looks purely cosmetic.

---

## 3. Block settings

Three sections take blocks, and all three pass the test the brief sets — blocks are for content
whose **count** genuinely varies, not for every text fragment.

| Section | Block | Fields | Limit |
|---|---|---|---|
| announcement-bar | `message` | text, link, icon | 3 |
| our-story | `value` | title, body | 6 |
| footer | `link_list` | heading, menu | 4 |
| footer | `text` | heading, body | 2 |

Every block wrapper carries `{{ block.shopify_attributes }}`, which is what lets the editor select,
outline and reorder them. Verified in all three sections.

**The hero deliberately takes no blocks.** Phase 2 §29.7 is explicit: a reorderable eyebrow /
heading / accent / scripture would let a merchant put the scripture above the headline and destroy
the lockup. The hero's content is a composition, not a list.

---

## 4. Dynamic sources

Shopify exposes dynamic sources automatically for compatible setting types, and the theme already
uses those types throughout — so metafield binding is available today on every `text`, `textarea`,
`richtext`, `url`, `image_picker`, `collection` and `product` setting without any code change.

The brief says to support them *"where useful"* and *"do not force dynamic sources everywhere"*, so
nothing was added. The three places a binding would genuinely help this brand:

- **hero `scripture`** — a verse-of-the-season metafield, so the hero rotates without a theme edit.
- **our-story `body`** — the brand narrative as a shop metafield, reusable on a page template.
- **product page** — a care-instructions or fabric metafield, once the product data exists.

None can be demonstrated without a real store and real metafield definitions.

---

## 5. Menu configuration

Navigation is Shopify's, entirely. `sections/header.liquid` reads a `link_list` setting and iterates
`link.title` / `link.url`; there is **no hardcoded menu label anywhere in the theme** — not HOME,
SHOP, COLLECTIONS, OUR STORY or VERSE. Verified by grep across every Liquid file.

The footer's `link_list` block binds a menu the same way, and falls back to the menu's own title
from Navigation when the merchant gives the column no heading — rather than inventing a word for it.

**`footer-group.json` ships with no menu bound.** Phase 10 shipped it bound to the `footer` handle,
which Shopify auto-creates as "Footer menu"; with no heading the column fell back to that title and
printed Shopify's admin vocabulary as customer-facing copy on every page, duplicating the policy row
beneath it. Fixed in Phase 10's review pass.

---

## 6. Collection configuration

Collections are Shopify's. `featured-collection` takes a real `collection` picker, and the same
section serves **both** the New Drop and Best Sellers rows through two named presets — the merchant
picks the collection for each.

There is no "choose bestseller product #1" setting, no ranking logic and no hardcoded handle
anywhere. Verified: no product name, price, currency symbol or collection handle appears in any
Liquid file.

The section is safe to duplicate: nothing derives from a hardcoded section id, and every generated
id is scoped by `section.id`.

---

## 7. Image configuration

Every image in the theme is an `image_picker` or Shopify product media. No URL text fields, and no
merchant is ever asked to paste a CDN link.

Both the hero and Our Story take a **separate mobile image**, because the 16:9 desktop frame loses
about a third of its width on a phone. Every image goes through `image_url` with a `widths` ladder
and an explicit `sizes`, so Shopify serves a candidate matched to the slot.

---

## 8. Theme Editor behaviour

This is where Phase 11's real defects were, and none of them was visible to any storefront suite:
the editor is the only place a section is replaced while the page stays alive.

**`assets/header.js` had three failures.**

1. **The scroll lock survived a re-render.** `open()` puts `menu-open` on `<html>`. A merchant who
   changed a header setting with the mobile menu open got a new node whose closure started with
   `isOpen = false` while the class stayed behind — leaving the page scroll-locked, with no menu on
   screen and no way to clear it without reloading. This is the identical failure Phase 8 already
   fixed for the cart drawer, whose `Drawer.init()` tears the old state down first. The header never
   got it.
2. **The focus trap leaked.** The document-level capture listener stayed bound to the detached panel
   and kept intercepting Tab and Escape.
3. **Listeners accumulated.** Every `shopify:section:load` called `initHeader` again, binding a new
   `matchMedia` listener and a new `scroll` listener and removing neither. Twenty setting tweaks,
   twenty scroll handlers on every scroll event. The brief names this one: *"do not attach the same
   event listener repeatedly."*

Every binding the header makes is now recorded in one registry and released as a unit, on re-render
and on removal. The teardown **closes the panel first**, so it cannot leave the half-torn state of a
panel still open on screen with its lock already released. `initHeader` is idempotent per element,
because `shopify:section:load` can fire for a node that was not replaced — and binding the toggle
twice made one click open the menu twice.

**`assets/cart.js`** already tore down on load. Its teardown is now a reusable `reset()` that also
runs on `shopify:section:unload`. The drawer is a static layout section, so a merchant cannot remove
it and a load almost always follows an unload — but "almost always" is not a safe basis for leaving
the page fixed-position with its background `inert`.

**`assets/product.js` was already correct and got nothing.** It is idempotent via a
`data-gsProductBound` guard and binds nothing to `document` or `window` beyond its own lifecycle
listener, so it holds no state to clean up. The brief says *"do not add event handlers if the section
requires no JavaScript"*; a no-op unload handler would have been noise.

**The hero no longer takes clearance it has not earned.** `--header-overlay-offset` says how tall the
overlaying header is, not which section it sits over — and the header overlays whichever section is
**first**. Now that the home page is reorderable, a merchant who dragged another section above the
hero left it carrying 122px of desktop clearance for a header that was somewhere else. Measured at
1440: hero first, clearance 122px and `padding-top` 170px; hero demoted, clearance 0 and
`padding-top` 48px. Expressed as a selector (`#MainContent > .shopify-section:first-child`), because
position is a fact only a selector can know — not a setting the merchant would have to keep in sync
with the order they just changed.

---

## 9. Preview inspector behaviour

Section and block boundaries outline correctly. `block.shopify_attributes` is present on every block
wrapper in all three block-bearing sections, which is what the inspector needs to select one.

The theme prefers grid, flex, padding and gap throughout; the brief's warning about negative margins
and absolute positioning applies to two elements only, and both are legitimate: the header overlays
the first section by design (a merchant setting, `overlay_first_section`), and the cart drawer is
`position: fixed` because it is a drawer.

**Every `request.design_mode` branch in the theme is a configuration notice**, never a different
layout — which is exactly the line the brief draws. Four sections carry one: featured-collection,
our-story, main-page and footer. They say "choose a collection", "choose an image", "this menu is
empty" — and they render **nothing at all** on the live storefront, so an unconfigured section costs
no requests either.

---

## 10. Theme Editor events

| Event | Handled by | Why |
|---|---|---|
| `shopify:section:load` | header.js, cart.js, product.js | Re-initialise a dynamically inserted section without a page refresh. |
| `shopify:section:unload` | header.js, cart.js | **New in Phase 11.** Release scroll locks, focus traps, `inert` siblings and every global binding. |
| `shopify:block:select` | — | Not implemented, deliberately. No section in the theme hides or sequences block content, so there is nothing for a select to reveal. The brief: *"Do not add event handlers if the section requires no JavaScript."* |

---

## 11. Mobile and desktop preview

The brief asks for 375 / 390 / 430 and 1280 / 1440. The responsive sweep covers all five, plus 480,
768, 834, 1024, 1920 and two landscape cases, across twelve pages — including the **reordered** home
page added this phase.

Result: **zero horizontal overflow and zero sub-24px touch targets at any viewport on any page.**

Phase 9 measured the storefront at these viewports in detail; Phase 11 adds the editor-specific
cases — a reordered home page, and the section lifecycle events — which are what the editor does that
the storefront does not.

---

## 12. Merchant workflow

The brief's own acceptance test is sixteen tasks a non-developer must complete without touching
Liquid, CSS, JS or JSON. **Twelve passed before this phase. All sixteen pass now.**

| Task | Before | Now |
|---|---|---|
| Change the logo | **FAIL** — header-only upload, footer could never show one | Theme settings › Brand, once, for both |
| Change the announcement | **FAIL** — no alignment control | Text, link, icon, colour scheme, alignment |
| Change the menu | pass | Shopify Navigation, via `link_list` |
| Change the hero image | pass | Desktop and mobile pickers |
| Change the hero heading | pass | |
| Change the hero CTA | pass | Renders only with both label and link; no `href="#"` anywhere |
| Change the featured collection | pass | Real collection picker |
| Change the bestseller collection | pass | Same section, second preset |
| Change the story image | pass | Desktop and mobile |
| Change the story text | pass | |
| Reorder sections | pass (defective) | The hero no longer keeps header clearance when demoted |
| Remove Best Sellers | pass | |
| Add Best Sellers back | pass | Two named presets |
| Preview mobile | pass | |
| Save | pass | |
| Change cart behaviour | **FAIL** — no Cart group at all | Drawer or cart page |

---

## 13. Theme Check results

**Not run. Shopify CLI is not installed in this environment** — `shopify` is not on the path, so
`shopify theme check` cannot be executed and no result is claimed here.

What was verified instead, mechanically:

- every `{% schema %}` in the theme parses as JSON, checked on every run;
- every setting id is unique within its section;
- every JSON template and both section groups are well formed, and every `type` resolves to a real
  section file;
- every `asset_url` target exists on disk;
- every `| t` key resolves, and no locale key is unused — both directions, across every Liquid file;
- no `{% include %}`, no hardcoded route, no `#{}` interpolation, no raw hex, no `!important`
  outside `base.css`;
- `config/settings_schema.json` has no `format: uri` violation (Phase 10 removed the two empty
  strings that were the theme's only known Theme Check ERROR).

Running the real linter against a development store remains outstanding and is listed in §14.

---

## 14. Known limitations

**Theme Check has never been run.** No Shopify CLI in this environment. §13 lists what was checked
mechanically instead.

**No real Shopify store.** Everything is measured against mock Shopify data through a strict
mini-Liquid interpreter and headless Edge. The Theme Editor itself has never opened this theme, so
the section lifecycle is verified by **dispatching the real events against the real markup and
scripts**, not by driving Shopify's editor. Section reordering is verified by rendering a reordered
home page, not by dragging one.

**One colour scheme.** §1.3. A second needs brand-approved values and a measurement pass.

**Schema labels are plain English, not `t:` keys, and there is no `locales/en.default.schema.json`.**
Phase 10 handed both to Phase 11 together, and two auditors raised it. It is not done here: the brief
requires *customer-facing* strings to come from locale files — which they do, all 101 of them — and
does not require schema labels to be translatable. Converting roughly 236 merchant-facing strings is
a large mechanical change whose failure mode is a raw `t:sections.x.y` showing in the editor, and it
should ship as its own pass with a validator that proves every key resolves. **Carried to Phase 12.**

**The hero focal point is overridden by an admin focal point**, silently, by Shopify's own
`image_tag`. Documented in the setting rather than fixed, because the alternative is losing a
composition control. §2.1.

**`show_cart` can hide the only header path to the cart.** Shipped because the brief lists it, with
the consequence in its `info`. A merchant who turns it off and saves has a store whose customers
must type `/cart`.

**Duplication carried from Phase 10**: ~100 lines of `sizes` derivation repeated between
`main-search` and `main-collection`, and a re-declared empty-state pattern. Still recorded, still
unfixed; it wants a shared snippet and its own pass.

---

## 15. Shopify Admin setup required

None of this is theme work. The theme is complete without it, and renders a graceful editor notice
wherever a piece is missing.

| What | Where | Why |
|---|---|---|
| **A logo file** | Theme settings › Brand | Until then the header renders the shop name as a text wordmark. Phase 3 records **VECTOR LOGO REQUIRED** — the current PNG's transparent padding renders the mark at about half its intended size. |
| **A favicon** | Theme settings › Brand | Phase 3 records that `/favicon.ico` 404s on every load. |
| **Social URLs** | Theme settings › Social | Both prototype links were `href="#"`. Each row renders only when its URL exists; none is invented. |
| **A main menu** | Navigation | The header reads it; it hardcodes nothing. |
| **A footer menu** | Navigation, then add a footer column block | Ships with no menu bound, deliberately. |
| **Collections** | Products › Collections | Then pick one in each of the two home rows. |
| **Pages** | Online Store › Pages | `our-story.liquid`'s CTA and the page template both need one. |
| **Store policies** | Settings › Policies | The footer renders whichever exist. |
| **`theme_documentation_url` / `theme_support_url`** | `config/settings_schema.json` | Omitted rather than shipped as empty strings, which is a schema violation. Restore when real URLs exist. |

---

## Appendix — verification

| Suite | Covers | Result |
|---|---|---|
| `validate.py` | Structure, schemas, tokens, translations, prototype integrity | 197 / 197 |
| `interact.py` | Cart drawer in a real browser | 49 / 49 |
| `interact_cartpage.py` | Cart page | 17 / 17 |
| `interact_product.py` | Product page | 26 / 26 |
| `contrast8.py` | Measured contrast on rendered pixels | 56 / 56 |
| `layout.py` | The real `layout/theme.liquid`, parsed | 19 / 19 |
| `surfaces.py` | The five Phase 10 surfaces in every state | 41 / 41 |
| **`editor.py`** | **New.** Section load/unload lifecycle, listener accounting | 10 / 10 |
| **`settings.py`** | **New.** Every Phase 11 setting, rendered both ways | 28 / 28 |
| `respond.py` | 12 pages × 12 viewports | 0 overflow, 0 sub-24px targets |
| `console.py` | Console and Liquid errors | 0 across 34 pages |

**443 assertions.**

Two suites are new, and both were **negative-controlled** — the fix reverted, the suite confirmed to
fail with real evidence, the fix restored. `editor.py` installs a counting shim on
`EventTarget.prototype` before any theme script runs, so it can measure the net number of listeners
bound to `window` and `document` by type; with the teardown disabled it reports *"html still carries
menu-open, so the page is stuck."* That discipline caught a defect the first fix missed:
`initHeader` re-bound the in-subtree toggle, so one click opened the menu three times.

Phase 11 stops here.
