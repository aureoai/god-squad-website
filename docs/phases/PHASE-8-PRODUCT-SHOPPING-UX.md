# GOD SQUAD — PHASE 8: PRODUCT & SHOPPING UX

Phase 8 deliverable. Built against the Phase 8 brief as issued, `PHASE-1-WEBSITE-AUDIT.md`,
`PHASE-2-DESIGN-SYSTEM.md`, `PHASE-3-ASSET-SYSTEM.md`, and the sections delivered in Phases 4–7.

This is the first phase in which the theme can take money.

Status: **delivered**. 197 structural checks, 92 browser-driven interaction assertions, 56 contrast
measurements and 10 rendered widths across 8 pages — all passing. No file from Phases 0–7 was
modified except the two the cart is obliged to touch, and both are recorded in §13.

It was then put through a multi-agent adversarial review — 58 findings raised, 46 confirmed after
three independent skeptics each — and every confirmed finding is fixed. The eight blockers among
them are listed in §12, because two of them would have taken a customer's money for the wrong
product.

---

## 1. Product page architecture

### The composition

`--split-60-40` (1.6fr 0.9fr, renders 64/36) from `--bp-lg` up: media left, buying right. Below the
split it stacks in exactly the order the brief sets — media, title, price, variants, quantity, add to
cart, buy now, description — which is also DOM order, so nothing is reordered visually away from how
a screen reader reads it.

```
templates/product.json
  └── sections/main-product.liquid            the whole page
        ├── snippets/product-media-gallery.liquid
        ├── snippets/product-variant-picker.liquid
        ├── snippets/quantity-selector.liquid   (shared with both carts)
        └── {% form 'product', product %}       Shopify's own form
```

### Settings, not blocks

The section is a fixed composition of **12 settings in 4 groups**, not a block list. Phase 2 §29.7
is explicit about when each is right: *"If a block type has one field, it is a setting… A block is
never created to let a merchant reorder two items that have a correct order."* A product page's
title, price, variant picker and add-to-cart have a correct order, and it is the brief's own order.

This is a deliberate departure from Dawn, which uses blocks so that apps can inject `@app` blocks.
The cost is recorded in §14: an app that ships a product-page block cannot place itself here without
a one-line schema change.

| Group | Setting | Type | Default |
|---|---|---|---|
| Media | `media_layout` | select | `stacked` |
| Buying | `show_quantity` | checkbox | true |
| Buying | `show_accelerated_checkout` | checkbox | true |
| Details | `description_layout` | select | `open` |
| Details | `show_vendor` | checkbox | false |
| Details | `show_product_type` | checkbox | false |
| Details | `show_sku` | checkbox | false |
| Layout | `sticky_info` | checkbox | true |
| Layout | `surface` | select | `light` (cream) |

Nine settings against Phase 2 §29.6's ceiling of fourteen. There is exactly one colour setting,
which is what §29.6 allows below theme level. There is no spacing, size or type setting anywhere.

### The form is Shopify's own

```liquid
{%- form 'product', product,
  id: form_id,
  class: 'shopify-product-form main-product__form',
  data-product-form: 'true' -%}
  <input type="hidden" name="id" value="{{ current_variant.id }}"
         data-variant-input {% unless can_buy %}disabled{% endunless %}>
  {% render 'product-variant-picker', product: product, section_id: section.id %}
```

Four things about this are easy to get wrong and are worth recording:

1. **The form tag does not generate the variant input.** It generates `form_type`, `utf8` and
   `product-id` — and `product-id` is not `id`, and adds nothing to a cart. The theme supplies
   `name="id"` itself.
2. **Passing `class:` replaces the tag's own default**, so `shopify-product-form` is repeated in the
   string rather than added to it.
3. **The variant input is disabled when the variant cannot be bought**, so a form submitted by any
   route — Enter in the quantity field, a script, browser autofill — cannot post a sold-out variant.
4. **There is no `novalidate`.** It was there because Dawn has it, and it switched off exactly the
   browser constraint validation the quantity control depends on: with scripting off, `min="1"` is
   the only thing standing between a typed `-3` and a POST to `/cart/add`. The script still clamps
   and still shows its own themed error, so nothing was gained by keeping it.

The variant picker is **inside** the form. It was outside, which left its radios unassociated with
the form entirely.

### Availability

```liquid
assign can_buy = false
if current_variant != blank and current_variant.available
  assign can_buy = true
endif
```

Read from the variant, never from whether a variant resolved.
`product.selected_or_first_available_variant` returns the **first** variant when everything is sold
out, so a nil check always passes and would report a sold-out product as buyable.

### Structured data

One `<script type="application/ld+json">` per page, produced by `{{ product | structured_data }}`.
Shopify injects no product structured data of its own, so the theme owns it — and using Shopify's
filter rather than hand-building the JSON is what keeps every price, currency, availability URL and
per-variant identifier derived from real product data. The filter emits no rating and no review
count, because no review data exists.

---

## 2. Product media implementation

### `product.media`, never `product.images`

`images` cannot represent a video or a 3D model, and a variant's `featured_image` cannot either —
only `featured_media` can. The gallery dispatches on `media.media_type` with an `{% else %}` arm, so
a type Shopify adds later still draws rather than vanishing.

| `media_type` | Rendered by | Notes |
|---|---|---|
| `image` | `image_url` → `image_tag` | Eight srcset candidates, 360–1800 w |
| `video` | `video_tag` | Controls on, **autoplay off** — Phase 2 §21.5; and a stranger on a phone did not choose to spend that data |
| `external_video` | `external_video_url` → `external_video_tag` | Order matters and fails silently if reversed |
| `model` | the preview image | See §14: the model viewer needs a Shopify feature loader this theme does not ship |

### Every medium is reachable with JavaScript off

The brief's rule — *"All actual product media must remain accessible. Do not display only the first
image if additional product media exists"* — is met structurally. Every medium is in the DOM at full
size, and the two layouts are a CSS switch over one markup:

- **stacked** — the media run down the column and the customer scrolls. No script at all.
- **carousel** — one frame at a time in a scroll-snap scroller. Native scrolling and swiping still
  work; the thumbnail rail is a list of in-page anchors, so it works too.

There is no carousel library and no slider. `assets/product.js` cancels the anchor jump (so no
history entry is written per photograph) and scrolls smoothly instead; with the script blocked the
anchor still brings its slide into view.

**`media_layout` governs the desktop composition only.** Below `--bp-lg` the gallery is always a
carousel, whatever the setting says, because a stacked gallery on a phone puts the price and the
add-to-cart control six screens below the fold. That is a layout decision a merchant should not be
able to make by accident.

### Loading

| Medium | `loading` | `fetchpriority` |
|---|---|---|
| First | `eager` | `high` |
| All others | `lazy` | — |

The brief's rule cuts both ways: *"do NOT blindly lazy-load every product image"*, and equally do not
eagerly load six of them.

### The `sizes` attribute is arithmetic, and it was checked against the rendered box

```
(min-width: 1440px) 840px,
(min-width: 1106px) calc((100vw - 128px) * 0.64),
(min-width: 1024px) calc(100vw - 480px),
(min-width: 768px)  calc(100vw - 64px),
calc(100vw - 48px)
```

Four regions, because the buying column has a 22rem floor and that floor changes which track absorbs
the remainder. 1106 is where the floor stops binding: `128 + 352 / 0.36`. The 1440 figure is the
theme's own `container_width`, so a merchant who widens the content width gets a correct cap.

The first version of this declared 573px where the element measured 544, and 901px where it measured
840 — both because it forgot that `max-width` includes the padding under `box-sizing: border-box`.
Measured at sixteen viewport widths after the correction:

| Viewport | Rendered | Declared | Δ |
|---:|---:|---:|---:|
| 375 | 312 | 327 | +15 |
| 768 | 689 | 704 | +15 |
| 1024 | 529 | 529 | 0 |
| 1105 | 610 | 610 | 0 |
| 1106 | 611 | 616 | +5 |
| 1280 | 728 | 728 | 0 |
| 1439 | 829 | 829 | 0 |
| 1920 | 840 | 840 | 0 |

**Zero under-declarations at any width.** The residual +15 below the split is the scrollbar the
harness leaves in place; the browser errs toward a larger candidate, which is the safe direction.

### `object-position` is Shopify's

`image_tag` writes the image's focal point onto the element as an inline style, and an inline style
outranks any rule in a stylesheet. The gallery therefore crops with `object-fit` and leaves the
position alone, and no `style:` parameter is passed to `image_tag`. This is the same finding Phase 7
recorded for the story band.

### One ratio for the whole catalogue

The media frame takes `--product-aspect`, the theme-level setting Phase 2 §27.6 rule 5 requires:
*"One ratio for the whole catalogue… chosen once at theme level, never per section and never per
product."* Different source ratios therefore cannot break the layout, which is the brief's
requirement for controlled media containers.

---

## 3. Variant system

### Built from `options_with_values`, never from `variants`

Shopify's own performance guidance is explicit: `product.variants` truncates silently at 250 and
costs render time on every request, while `options_with_values` is the object designed for this.
Each `product_option_value` carries its own `selected` and `available`, so **the server renders the
correct initial state with no JavaScript involved.**

### Radios, not a select

Phase 2 §27.4: *"Never a native `<select>` on a product page where the options are fewer than
eight."* A radio group also gives the selected state an accessible name change for free, which the
same section requires — a checked radio announces itself, a styled `<div>` does not.

```
<fieldset class="variant-picker__option">
  <legend>Size <span data-option-value-for="1">S</span></legend>
  <input type="radio" class="visually-hidden" id="…" name="…" checked>
  <label for="…">XS</label>
  …
```

| State | Treatment |
|---|---|
| Rest | 1px `--color-border-current-interactive` (3.02:1 on ink, 3.13:1 on cream) |
| Selected | `--border-width-strong` 2px in `currentColor`, **plus** the checked radio. Padding gives back exactly the pixel the border takes, so choosing a value does not nudge the row |
| Unavailable | struck through, muted, **still in the DOM and still focusable**, with the state in the accessible name |
| Focus | the ring is drawn on the label, because the input it belongs to is visually hidden |

Phase 2 §27.4 names `--color-border-current` for the chip boundary; §12.2 is the later, measured
correction — those tokens composite to about 1.3:1 and fail SC 1.4.11's 3:1 for a control's visual
boundary — and this follows §12.2. The same substitution is already made for `.button--secondary`.

### Swatches

Only from Shopify's own swatch data. A value with no swatch in a mixed option falls back to its
name, so it stays choosable. The dot keeps the product card's ring treatment; the **selected** ring
is drawn at the 44px target's edge, separated from the dot, because a ring drawn *on* an ink swatch
sitting on an ink band would be invisible. An unavailable swatch carries a diagonal rule across the
dot **plus** the words in its accessible name — colour is never the only signal.

### What changes when a variant is chosen

`assets/product.js`, with no network request:

- the hidden `name="id"` input, and its `disabled` state
- the price, and whether the compare-at price is shown
- the add-to-cart button's label and `disabled` state
- the SKU, where it is shown
- the option legends' chosen-value text
- which values are marked unavailable, and their accessible names
- the active gallery slide, when the variant carries a `featured_media`
- the URL, via `history.replaceState` — **never `pushState`**: trying three sizes must not put three
  entries between the customer and the page they came from
- the quantity control's `min`, `max` and `step`, because `quantity_rule` is carried **per variant**
  and a customer who chose a variant with its own minimum would otherwise keep the previous one's
  and be refused at `/cart/add` with no idea why

When a chosen combination resolves to no variant at all — routine on a product whose option grid is
not fully populated — the add-to-cart control is disabled and **the price is left as it was**. An
empty price where a number used to be reads as a broken page.

### Why the variant table is embedded

The alternative is to re-render the section from the server on every size click — a network round
trip per tap. The six fields the picker needs are a few hundred bytes, and the money strings are
formatted by Liquid against the store's own money format, which is the one thing the browser
genuinely cannot do correctly.

The table is written out rather than using `{{ product.variants | json }}`, for two reasons: the
whole-object dump publishes `inventory_quantity` and `inventory_management` into the page source,
which is a stock-level leak; and it is several times larger than the six fields that are used.

### `available` means two different things

`product_option_value.available` is true when *some* variant carrying that value is available — not
that the combination the customer has built is. The combination is resolved against the variant
table by the script. **Server-rendered state is correct on load and refined on interaction, never
the other way round.**

---

## 4. Quantity selector

Phase 2 §12.4, built: a minus `<button>`, an `<input type="number" inputmode="numeric">`, a plus
`<button>`. Three consumers — the product form, the cart drawer line, the cart page line — which is
what makes it a component rather than markup inside one section.

| Rule | Implementation |
|---|---|
| Minimum 1 | `min` on the input; the minus disables itself at the floor rather than silently clamping |
| Buttons ≥ 44px | `min-width`/`min-height: var(--target-min)`. SC 2.5.8's spacing exception cannot rescue two flush steppers — their 24px circles necessarily intersect |
| Value 16px, centred | `--type-body-size`. The floor also stops iOS zooming the viewport on focus |
| Untracked | `letter-spacing: 0` — §27.6 rule 1: tracking never touches numerals |
| Keyboard | a real number input; arrows, typing and the two buttons all work |
| Invalid values | clamped to `min`/`max` on `change`, and by the browser |
| 250ms debounce | a **literal**, not `--duration-medium`: a motion token collapses to 1ms under `prefers-reduced-motion` and would remove the debounce for exactly the people most likely to be stepping a quantity from a keyboard |
| Announced | every change goes to whichever live region is currently reachable (§9) |
| Without the script | the two stepper buttons are **not rendered** and the browser's own number spinner is left in place. They are `type="button"` and do nothing until `assets/cart.js` binds them; shipping them regardless put two 44px controls on the page that a customer with scripting off could press forever |

The upper bound is Shopify's, never the theme's: `max` and `step` come from
`variant.quantity_rule` when the merchant has set one, and are simply absent when they have not.
`variant.inventory_quantity` is never rendered — it is public on the storefront and publishing it
leaks either stock levels or lifetime sales.

**On a cart line the floor is one, not zero.** Stepping down to nothing would make the minus button
destructive at its last press; removal is the explicit control beside it.

---

## 5. Add-to-cart behaviour

| Step | What happens |
|---|---|
| 1 | The submit is intercepted. A second submit while one is in flight is ignored. |
| 2 | The button takes `aria-busy="true"` and its label becomes "Adding…" — from a `data-` attribute written by Liquid, so the word is translatable. It is **not** disabled: disabling the element that holds focus blurs it, so every add dropped a keyboard user back to `<body>`, and re-enabling it afterwards clobbered a sold-out state a variant change had set in the meantime. The double-submit guard reads `aria-busy` instead |
| 3 | `FormData` from the form itself, so any line item property or selling plan the form carries goes with it, plus `sections` and `sections_url` |
| 4 | The response's rendered sections replace the header count and the drawer's contents |
| 5 | The button is restored |
| 6 | If `auto_open` is on the drawer opens and focus moves into it; otherwise the addition is announced |

**The customer is never sent to checkout.** The button is a submit inside a form whose action is
`/cart/add`; with the script it never navigates at all.

### Feedback, and why it is not announced twice

When the same gesture both adds the item and opens the drawer, the addition is **not** announced:
moving focus and announcing at the same moment makes a screen reader talk over itself, and the
drawer's heading already says where the customer now is. The announcement is made only when adding
without opening.

### Errors

| Failure | What the customer sees |
|---|---|
| 422, e.g. more than we have | Shopify's own `description`, in a `role="alert"` region under the button |
| Transport failure | the theme's own sentence, from the locale file |
| A cart mutation that returned no usable sections | the cart is re-fetched rather than guessed at |

**A 422 can mean the cart changed anyway.** When the requested quantity exceeds stock Shopify adds
the maximum it can *and* returns the error, so an error response is never treated as "nothing
happened" — the returned sections are applied either way, and if there are none the cart is re-read.

The button is restored on every path, including the transport failure. There is no code path that
leaves it saying "Adding…".

---

## 6. Ajax cart implementation

`assets/cart.js` — 27 KB, about half of it comment. No framework, no dependency, no polyfill.

### Locale-aware URLs

```js
function root() {
  var r = window.Shopify && window.Shopify.routes && window.Shopify.routes.root;
  return r || '/';
}
```

Never a literal `/cart/add.js`. A store with Markets or a second language serves the cart under a
locale prefix, and a hardcoded path silently 404s there.

### One request shape

| Endpoint | Body | Headers |
|---|---|---|
| `cart/add.js` | `FormData` from the form | **no `Content-Type`** — setting one overwrites the multipart boundary the browser generated |
| `cart/change.js` | `{id: <line key>, quantity: n, sections, sections_url}` | `application/json` |

A response counts as failed when `data.description` is present or the HTTP status is not ok. The
`status` field is sometimes the integer 422 and sometimes the string `bad_request`, so it is not a
reliable test on its own.

### Lines are identified by their key

Never by index, never by variant id. Two lines can share a variant id — the same variant with
different properties, or split by an automatic discount — and an index shifts the moment anything is
removed. The key is also **not stable across mutations**, so it is re-read from freshly rendered
markup every time rather than cached.

### Section rendering in the same round trip

The render targets are **collected from the page at init**, not fixed, because the three surfaces do
not all coexist:

| Target | When it is requested |
|---|---|
| `cart-icon-bubble` | always — a standalone section file with a stable id |
| `cart-drawer` | every template except `/cart` |
| the cart page's own section | only on `/cart`, its id read from the DOM |

The cart page had to be one of them. The script intercepts its quantity steppers and its Remove
links, and without a way to re-render it the customer saw their change do nothing — and after a
removal the page's **positional** `updates[]` inputs no longer lined up with the server's lines, so
pressing Checkout would have applied each surviving quantity to the wrong product.

`sections_url=<location.pathname>` goes with every mutation, so both surfaces are always the
server's view of the cart after the change — never a number this file calculated. `sections_url` must begin with a slash or the whole
request returns 400, and the docs warn that such a 400 does not mean the mutation was rolled back;
`location.pathname` always begins with one.

Both render targets are section files with **stable ids**: `cart-drawer` is rendered from the layout
and `cart-icon-bubble` is a standalone file that exists only to be requested. A section placed in a
JSON template is given a generated id such as `sections--1234__header`, which changes; a standalone
file keeps its filename.

`sections/cart-icon-bubble.liquid` carries **no schema** — it needs no settings (a standalone render
target cannot receive them; the docs are explicit that it falls back to defaults), and a preset would
wrongly expose an internal render target in the merchant's Add section list.

A section that comes back `null` is skipped. The returned HTML always carries the
`<div id="shopify-section-…">` wrapper, so the inside is taken rather than the outside — replacing
`outerHTML` would nest a second wrapper on every update.

### Delegation

Five listeners on `document`, for the whole page. Markup the Section Rendering API swaps in needs no
re-binding, which is also what stops the file leaking listeners on every cart update.

---

## 7. Cart drawer

`sections/cart-drawer.liquid`, rendered once from `layout/theme.liquid` so it is on every page
**except `/cart`**. There, the page is the cart: rendering the drawer as well put two views of one
thing on one screen, which can disagree after an update, and gave every cart line a duplicate DOM id
— silently re-pointing the drawer's quantity labels at the page's inputs.

### It is a real cart form first and a drawer second

Everything inside is Shopify's documented no-JavaScript cart: a form posting to `routes.cart_url`,
one `updates[]` field per line in cart order, a submit named `checkout`, and `item.url_to_remove`
links. With scripting disabled the drawer simply is not openable and the header's cart control is
what it has always been — a link to the cart page.

### Structure

```
<div class="cart-drawer" role="dialog" aria-modal="true" aria-labelledby="CartDrawerTitle" hidden>
  <div class="cart-drawer__overlay">                    pointer-only; Escape is the keyboard equivalent
  <div class="cart-drawer__panel">
    <div class="cart-drawer__header">
      <h2 id="CartDrawerTitle" tabindex="-1">           focus lands here; OUTSIDE the swapped region
      <button data-cart-close>
    <div role="status" data-cart-drawer-status>         the drawer's own announcements
    <p data-cart-error role="alert" hidden>             the visible failure line
    <div data-cart-drawer-inner>                        replaced after every cart change
      <form action="{{ routes.cart_url }}" method="post">
        <div class="cart-drawer__scroller">  … lines …
        <div class="cart-drawer__footer">    totals, update, checkout, view cart
```

**The heading, the live region and the error line are all outside the swapped region** on purpose:
a focused element inside a replaced subtree is destroyed and the browser drops focus to `<body>`,
and a live region recreated together with its text announces nothing at all.

### Totals: three lines, not one

| Line | Source |
|---|---|
| Subtotal | `cart.items_subtotal_price` — after line-level discounts, before cart-level |
| Each cart-level discount | `cart.cart_level_discount_applications` |
| Estimated total | `cart.total_price` |

Showing `items_subtotal_price` alone as "the price" silently overstates what the customer will pay
the moment a cart-level discount is active.

The line under them is **derived, not asserted**. Whether tax is already in the price is a fact
about the store and Shopify knows it, so the note branches on `cart.taxes_included` rather than
printing "Taxes and shipping are calculated at checkout" at every store — which would be a claim
about this merchant's tax configuration that nobody supplied, and wrong for any tax-inclusive
market, which the Philippines is.

There is no shipping claim, no delivery estimate and no free-shipping threshold anywhere — shipping
scope is BUSINESS INFORMATION REQUIRED (Phase 1 UX-05, VAL-04).

The totals and the empty state are `snippets/cart-totals.liquid` and
`snippets/cart-empty-state.liquid`, shared by both cart surfaces. They were two byte-identical
copies under renamed classes until the review pointed out that a correction to one would never reach
the other.

### The update submit comes first

A browser submits a form with its **first** submit button when Enter is pressed in a field. If the
checkout button came first, pressing Enter after typing a quantity would take the customer to
checkout instead of applying the change they had just typed.

The update control is visible only when focused, and is removed from the document entirely once
`assets/cart.js` has run — keyed on a class **the cart script sets on itself**, not the layout's
`js` class. The layout's class is set by an inline script that runs whether or not the cart script
ever arrives; keying on it would have hidden the only control that can apply a quantity change in
precisely the case where nothing else can.

### Checkout

A submit named `checkout` inside the cart form — Shopify's own control. It applies any pending
quantity edit and *then* goes to checkout, in one action. A plain link to `/checkout` would silently
discard an edit the customer had just made.

### Line item fields that look right and are not

`line_item.product_title` and `line_item.variant_title` **do not exist in Liquid**. They exist only
in the Ajax Cart API's JSON, which is a different API and the usual source of this mistake. The name
comes from `item.product.title` and the variant line from `item.options_with_values`, guarded by
`has_only_default_variant` so a product with no options does not print a spurious
"Title: Default Title" row.

### `updates[]` is positional

Exactly one input per line, in `cart.items` order, with no gaps. A quantity field wrapped in a
condition that can be false would shift every later line's quantity onto the wrong product. The
snippet therefore never makes it conditional, and the validator asserts that.

### Removal

A text control — "Remove" — rather than a glyph. Phase 2 §18.1 closes the icon set to decorative
additions and contains no bin mark, and in a 420px drawer a word is less ambiguous than an icon at
44px. The destination is Shopify's own `item.url_to_remove`, so it works with no script; the cart
script cancels the navigation and does the same thing through the Ajax API.

### Empty state

A real destination, never `href="#"`, and no invented recommendations.

The default is the **home page**, not `routes.all_products_collection_url`. That route is the
obvious answer and the wrong one in this theme today: no `templates/collection.json` exists yet, so
Shopify would have served an error page to every customer who opened an empty cart and pressed the
one button in it. The home page does exist and carries both the New Drop and Best Sellers rows. The
merchant can point it anywhere once a collection template ships.

### Why it is not a `<dialog>`

`showModal()` would give inertness, the top layer, Escape and focus return for free. The trade was
made deliberately against three costs:

1. the panel is promoted out of its stacking and containing-block context, and `::backdrop` is a
   separate pseudo-element, so scrim and panel cannot animate as one composited group; the UA's
   centring and max-size defaults must all be overridden;
2. the exit animation needs `@starting-style` plus `transition: display … allow-discrete, overlay …
   allow-discrete` — omit the `overlay` line and the drawer snaps away instead of sliding out;
3. any stray `method="dialog"` or `formmethod="dialog"` on a control inside it silently closes the
   dialog and discards the POST. In a cart, that is a discarded `/cart/change`.

Worth revisiting when `closedby="any"` is Baseline.

---

## 8. Cart count

`snippets/cart-icon-bubble.liquid`, rendered in two places: inline by `sections/header.liquid`, and
alone by `sections/cart-icon-bubble.liquid` as the target the script swaps in. Dawn keeps two copies
of this markup in parallel and they drift; one snippet cannot.

```liquid
{%- if cart.item_count > 0 -%}
  <span class="header__cart-count" data-cart-count aria-hidden="true">{{ cart.item_count }}</span>
  <span class="visually-hidden" data-cart-count-text>{{ 'cart.item_count' | t: count: cart.item_count }}</span>
{%- endif -%}
```

Phase 1 NAV-09 recorded the prototype's badge as the literal character `0`, painted whether or not
anything was in a cart that did not exist. An empty cart shows **no badge at all**, so nothing
announces "0 items" — the control's own name is still "Cart", which is the whole message when the
cart is empty. The visually hidden count is pluralised through the locale file's `one`/`other`
forms.

After every cart change the badge is replaced from the server's own render, not incremented in
JavaScript.

---

## 9. Accessibility

Measured on rendered pages, not asserted.

| Criterion | Result |
|---|---|
| **1.4.3 Contrast** | **55 measurements** across the product page on both surfaces, the drawer, the empty drawer and the cart page — **0 failures**. See the table below |
| **1.4.11 Non-text contrast** | Control boundaries use `--color-border-current-interactive`: 3.02:1 on ink, 3.13:1 on cream. The selected chip and the active thumbnail use `currentColor` at 17.04:1 |
| **1.4.1 Use of colour** | Sold-out is a word on the button; an unavailable chip is struck through **and** says so; an unavailable swatch carries a diagonal rule **and** says so; a discount line is gold **and** labelled |
| **2.5.8 Target size** | **0 under-size targets** at ten widths across six pages, with the drawer both open and closed. Steppers and the close control are 44px; the cart line's title link is boxed to 24px because neither SC 2.5.8 exception rescues it |
| **2.4.11 Focus not obscured** | The drawer's footer is pinned *below* the scroller, not over it, and the scroller carries `scroll-padding-block-end`; the sticky buying column carries `scroll-padding-block` |
| **2.1.1 Keyboard** | Every control is a real `<button>` or `<a>`. **0 positive `tabindex`.** No clickable `<div>` anywhere |
| **1.3.1 / 4.1.2** | `role="dialog"` + `aria-modal` + `aria-labelledby`; `fieldset`/`legend` per option; a real `<label for>` on every input; `role="list"` on the line list |
| **2.4.6 Headings** | One `h1` per product page — measured at ten widths on five products. The drawer's heading is an `h2` |
| **1.4.10 Reflow** | No horizontal scroll at 320px or at any of the ten widths measured |
| **2.3.3 Motion** | Only `opacity`, `transform`, `background-color`, `color`, `border-color` transition. Every transition is switched off under `prefers-reduced-motion`, and the gallery's smooth scroll falls back to instant |

### Focus, in every path

| Event | Where focus goes |
|---|---|
| Drawer opens | the heading (`tabindex="-1"`), not the close button — "Close, button" tells the customer nothing about what just happened |
| Escape, overlay click, close button | back to whatever opened it, or the header cart control if that element is gone |
| A cart line is updated | back to the equivalent control in the freshly rendered line |
| A cart line is removed | that surface's own heading — the drawer's, or the cart page's `h1` — because the control that had focus no longer exists |
| Add to cart, start to finish | stays on the add button. It is never disabled, only `aria-busy` |
| Drawer closes | the opener, checked for still being in the document — focusing a detached node silently puts focus on `<body>` |

### The background is `inert`, not `aria-hidden`

`aria-hidden` leaves content focusable while removing it from the accessibility tree, which strands
a screen reader on an element it cannot describe. `inert` handles focus, pointer input, find-in-page
and the accessibility tree in one attribute. Where `inert` is unavailable, a minimal Tab-cycling
trap takes over; where it is available, no hand-rolled trap runs alongside it.

**The drawer's own section wrapper is excluded by `contains()`, not by identity.** Shopify wraps
every section in `<div id="shopify-section-…">` when the layout renders it, so the drawer is never
itself a child of `<body>`. Comparing identity marked the wrapper inert, which made the drawer inert
with it — and focus could not be moved into a drawer that had just been opened. This was caught by
the browser test suite and is the single most consequential defect this phase found in its own work.

### Two live regions, because `aria-modal` hides one of them

`aria-modal="true"` instructs assistive technology to treat everything **outside** the dialog as
absent from the accessibility tree. The layout's `#CartStatus` is a sibling of the drawer, not a
descendant — so while the drawer was open, every status it produced was announced to nobody.

There are therefore two, and `announce()` routes between them:

| When | Region |
|---|---|
| The drawer is open | `[data-cart-drawer-status]`, inside the panel and outside the swapped node |
| Otherwise | `#CartStatus`, in the layout, carrying `data-cart-no-inert` |

Both are empty at page load and text is injected inside a `setTimeout`: a region created together
with its content announces nothing.

### And a visible failure line, because a live region is not feedback for everyone

A failed quantity change or removal used to be reported **only** to the live region. A sighted
customer saw the number snap back with no explanation. Each cart surface now carries a
`role="alert"` line outside its swapped node — text plus a left rule, never colour alone — and the
message is always either Shopify's own `description` or one of the theme's own sentences from the
locale file.

Every sentence comes from the locale file. `assets/cart.js` writes no user-facing English of its
own, so none of it can be untranslatable.

### Contrast, measured

The product page and the cart are flat surface tokens, so the effective background is composited
exactly from the computed styles rather than sampled. Selected rows:

| Role | Cream page | Ink page / drawer | Needs |
|---|---:|---:|---:|
| Product title | 17.04 | 17.04 | 3.0 |
| Price, current | 17.04 | 17.04 | 4.5 |
| Price, compare-at | 5.97 | 9.70 | 4.5 |
| Variant chip | 17.04 | 17.04 | 4.5 |
| Variant chip, unavailable | 5.97 | 9.70 | 4.5 |
| Add-to-cart label | 17.04 | 17.04 | 4.5 |
| Description | 5.97 | 9.70 | 4.5 |
| Cart line title | — | 17.04 | 4.5 |
| Cart line discount (gold) | — | 11.01 | 4.5 |
| Remove | — | 9.70 | 4.5 |
| Estimated total | — | 17.04 | 4.5 |
| Checkout label | — | 17.04 | 4.5 |
| Empty-cart button (gold fill) | — | 11.01 | 4.5 |

---

## 10. Responsive behaviour

| | < 768 | 768 – 1023 | ≥ 1024 |
|---|---|---|---|
| Product page | stacked | stacked | `--split-60-40`, media left |
| Gallery | carousel + rail | carousel + rail | setting: stacked (no rail) or carousel |
| Buying column | in flow | in flow | sticky, `top: --header-offset-desktop` |
| Cart line | image + detail, price under | image + detail + price column | as 768 |
| Drawer | `min(90vw, 420px)` | 420px | 420px |

### Measured, at ten widths on six pages, drawer open and closed

| Width | Scroll W | H-scroll | Media | Buying column | Sticky |
|---:|---:|---|---:|---:|---|
| 320 | 320 | no | 272 | 272 | static |
| 375 | 375 | no | 327 | 327 | static |
| 768 | 768 | no | 704 | 704 | static |
| 1024 | 1024 | no | 544 | 352 | sticky |
| 1280 | 1280 | no | 737 | 415 | sticky |
| 1440 | 1440 | no | 840 | 472 | sticky |
| 1920 | 1920 | no | 840 | 472 | sticky |

No element exceeds the viewport at any width, on any page, with the drawer open or closed.

The buying column carries a 22rem floor, so at 1024 it holds its 352px rather than collapsing to the
0.9fr share of 322px — which is what makes the variant chips and the quantity control fit without
wrapping awkwardly.

### Sticky, and when it stops

`position: sticky` with `align-self: start`, plus `max-height: calc(100vh - header offset - space)`
and its own scroll. If the buying column is ever taller than the screen, sticking it would otherwise
hide its own bottom — including the add-to-cart button.

---

## 11. Performance

- **No framework, no dependency, no polyfill, no cart library.** Two files, 41 KB of JavaScript
  uncompressed, about half of it comment.
- **`cart.js` from the layout** (it is needed on every page — the header control and the product
  card's optional quick-add are everywhere); **`product.js` from the product section only**.
- **Section stylesheets are requested by the section that needs them**, so a page without a product
  page does not download `section-main-product.css`. The three shared components —
  `component-button.css`, `component-quantity.css`, `component-cart-line.css` — load from the
  **layout**, because the drawer is rendered there on nearly every page and linking them from the
  sections as well put two `<link>` tags for one URL on every product and cart page. This is the
  same promotion Phase 6 performed for the button system when it acquired a second consumer.
- **One network request per cart action, not two.** Sections are bundled into the mutation rather
  than fetched afterwards.
- **Opening the drawer costs no request at all** — it is already rendered.
- **Layout shift:** every image reserves its box through `--product-aspect`; the drawer is
  `position: fixed` and shifts nothing; `scrollbar-gutter: stable` is set permanently on `html` so
  locking the page scroll does not move the layout sideways by the scrollbar's width.
- **The variant table** carries six fields per variant, not the whole variant object.
- **`fetchpriority="high"`** on the first product image only.

### One global

`window.GodSquad.cart` — `{open, close, refresh}`. `window.Shopify` is never written to.
`product.js` creates no global at all.

---

## 12. Testing

Rendering was done against the **real `.liquid` files** by the mini-Liquid harness built in Phase 5,
extended here with `{% form %}`, `{% case %}`, twenty-eight filters, `#{}` string interpolation,
translation interpolation and pluralisation, and a `structured_data` stand-in.

| Pass | Coverage | Result |
|---|---|---|
| **Structural validation** | 197 assertions: files, schema parse, template wiring, source-of-truth prohibitions, the product form contract, the cart contract, markup, JavaScript, the design-system corrections, locales, token fidelity, earlier phases, original files | **197 pass, 0 fail** |
| **Render cases** | 17 pages: one variant, several variants with one sold out, two option types with swatches on sale, a wholly sold-out product, a long title with no media, a quantity rule with a unit price, carousel layout, ink surface, all details shown, no quantity or accelerated checkout, sticky off, and five cart states | all render; **0 missing translations** |
| **Console** | all 18 pages loaded in a real browser | **0 errors**, both scripts initialise, variant JSON parses, JSON-LD parses on every product page |
| **Cart interaction** | 49 assertions against a stubbed Ajax Cart API: open, close, Escape, overlay, focus, inert through the section wrapper, scroll lock, the add request's URL/body/headers/sections, the section swap, the debounce, the line key, the minimum, removal, a 422, a transport failure, a null section, the visible failure line, the in-dialog announcement | **49 pass, 0 fail** |
| **Cart page interaction** | 17 assertions: no drawer on the page, its own render hook and section id, the request's section list, the removed line, the replaced totals and badge, `updates[]` realignment, focus to the `h1`, a quantity change, a visible failure | **17 pass, 0 fail** |
| **Product interaction** | 26 assertions: variant resolution, legends, URL, history, availability, unavailable combinations, the sold-out label, the gallery rail, the hash | **26 pass, 0 fail** |
| **Geometry and targets** | 10 widths × 8 pages × drawer open and closed | **0 overflow, 0 under-size targets, 0 positive tabindex, 1 h1** |
| **`sizes` accuracy** | 16 widths, declared vs rendered | **0 under-declarations** |
| **Contrast** | 56 role measurements on both surfaces | **56 pass, 0 fail** |
| **Visual** | 9 captures at 375 and 1440 | reviewed |

### Product and cart states covered

One variant · multiple variants · multiple option types · a sold-out variant · a sold-out product ·
a product on sale · no compare-at price · a long title · a long description · one image · multiple
images · a video · a quantity rule · a unit price · an empty cart · one cart item · multiple cart
items · two lines of the same product in different variants · a line with a discount · a line
carrying Shopify's own error · quantity increase · quantity decrease · removal · an add-to-cart
error · a transport failure · a null section · mobile drawer · desktop drawer · keyboard navigation ·
Escape · screen-reader announcement · reduced motion.

### The adversarial review

Seven reviewers worked in parallel — Shopify correctness, accessibility, design system, JavaScript
robustness, no-JS and progressive enhancement, scope and invention, performance and SEO — and every
finding was then put to three independent skeptics instructed to refute it, each reading the file
themselves. **58 raised, 46 confirmed, 12 refuted.** All 46 are fixed.

The eight blockers, in the order they mattered:

| Finding | What it would have done |
|---|---|
| The cart page was intercepted and never re-rendered | Removing a line did nothing on screen, and the page's **positional** `updates[]` inputs then no longer lined up with the server's lines — so pressing Checkout would have applied each surviving quantity to the wrong product. Fixed by making the cart page a render target and by not rendering the drawer on it |
| The drawer rendered on the cart page too | Two views of one cart that can disagree, and a duplicate DOM id on every line — `<label for>` resolves to the first match, so the drawer's quantity labels silently pointed at the page's inputs |
| Duplicate quantity ids | Same cause. Ids are now namespaced by their surface as well as by the line key |
| The variant picker sat outside the form | Its radios were not associated with the product form at all. Moved inside; the no-JS switching limitation is recorded in §14 |
| An unconditional tax-and-shipping claim | A business fact nobody supplied, asserted at every store and wrong for any tax-inclusive market. Now branches on `cart.taxes_included` |
| The empty-cart button pointed at `/collections/all` | No collection template exists yet, so the one button in an empty cart led to an error page. Now the home page |
| The live region was outside `aria-modal` | Every status the drawer produced while open was announced to nobody. The drawer has its own |
| Cart failures were announced but never shown | A sighted customer saw a quantity snap back with no explanation. Both surfaces now carry a visible `role="alert"` line |

The other confirmed findings were of the same character and are all fixed: the add button blurring
focus by disabling itself; `setButtonBusy` re-enabling a sold-out control; a superseded quantity
change stranding `aria-busy` and swallowing its error; `novalidate` defeating the quantity minimum;
the steppers being dead without the script; the quantity rule not following the variant; the price
being blanked when no combination matched; the gallery ignoring the server's chosen slide and
branching on the setting rather than the rendered layout; a Theme Editor re-render stranding an open
drawer; a swatch at a raw 28px; two concentric focus rings; a 14px value in the drawer; the wrong
scrim duration; the wrong disabled opacity; an opacity hover where the system specifies colour; a
second copy of the visually-hidden recipe; duplicated totals and empty-state CSS; a duplicated
stylesheet link; a lazy LCP image on the cart page; an under-declared thumbnail `sizes`; and four
comments that described code that did something else.

### Two defects the harness found that reading could not

1. **`inert` on the section wrapper made the drawer itself inert**, so focus could not be moved into
   a drawer that had just opened. The browser test caught it; a first version of that same test gave
   a false pass by checking `hasAttribute('inert')` on the drawer instead of `closest('[inert]')` —
   inert is inherited.
2. **The cart thumbnail rendered 76 × 900.** `image_tag` emits `width` and `height` *attributes*,
   which the browser turns into presentational hints for both dimensions; a rule that sets only
   `width` leaves the intrinsic height in force and `aspect-ratio` is ignored entirely. Every cart
   line was 948px tall. Found only once the harness started emitting those attributes the way
   Shopify does. Every other image rule in the theme sets both dimensions and is unaffected.

### Two harness defects worth recording

Both produced *plausible wrong numbers*, which is the dangerous kind:

- **`#{}` interpolation was unimplemented**, so the header's logo style attribute rendered
  literally, the custom property was invalid, the logo drew at 133px and the header appeared to
  overflow at 320px. The theme never had that defect.
- **`blank` did not compare equal to itself**, so `assign x = blank` followed by `if x != blank`
  took the true branch and the quantity input rendered `max=""`.

### Three known Phase 7 validator failures

Running Phase 7's validator against the Phase 8 theme reports three failures. All three are the
older validator's limitations, not theme defects:

1. `sections/cart-icon-bubble.liquid no schema` — it is a render target and deliberately has none.
2. and 3. `cart.item_count` — Phase 7's validator flattens the locale tree without understanding
   `one`/`other` pluralisation. Phase 8's validator does.

---

## 13. Shopify configuration

### Required before a customer can buy

1. **Add products.** *Products → Add product.* Every price, variant, image, description, SKU and
   stock level on the storefront comes from here; the theme invents none of them.
2. **Model the options.** Colour and size are product **options** in admin, not theme settings. The
   picker renders whatever options exist, in the order they are set. The size run itself is
   BUSINESS INFORMATION REQUIRED (Phase 1 ECOM-04).
3. **Set colour swatches.** *Settings → Products → Swatches*, or per option value. A colour renders
   as a swatch only when Shopify carries swatch data for it; otherwise it renders as a named chip.
4. **Set each image's focal point.** *Content → Files → (image) → Edit.* This is the crop control;
   the theme deliberately offers no second one, for the reason in §2.
5. **Set the store currency and money format.** *Settings → Store details.* Every price is rendered
   through the `money` filter against that format. Phase 1 ECOM-09 records the currency and markets
   decision as BUSINESS INFORMATION REQUIRED.
6. **Check the peso glyph.** Phase 2 §27.2 records that Jost carries neither `₱` nor `→`, so the
   peso falls back to a per-platform face in the single most legibility-critical string on the page.
   Still BUSINESS INFORMATION REQUIRED.

### Optional

7. **Accelerated checkout.** *Settings → Payments.* The Buy it now button only appears when it is
   enabled, and its colours, typeface and label are Shopify's and cannot be themed. The section
   setting turns it off without a code change.
8. **Quantity rules.** *Products → (variant) → Quantity rules.* Minimum, maximum and increment are
   honoured by the quantity selector.
9. **The empty-cart destination.** *Customize → Cart drawer → Where the empty-cart button goes.*
   Defaults to the store's all-products collection.
10. **Drawer behaviour.** *Customize → Cart drawer → Open the drawer after adding.* With it off,
    adding still updates the count and announces itself; the customer is simply not interrupted.

### What Phase 8 changed outside its own files

| File | Change | Why it was unavoidable |
|---|---|---|
| `layout/theme.liquid` | loads `cart.js`; renders `{% section 'cart-drawer' %}`; adds the live region and the strings host | The drawer must be a direct child of `<body>` — a drawer nested inside a region the script marks inert would be made inert with it — and a statically rendered section is the only way to get a stable section id |
| `sections/header.liquid` | the cart control's contents moved into a snippet; `data-cart-bubble` added | The Section Rendering API needs a second copy of that markup to swap in, and two hand-maintained copies drift |
| `locales/en.default.json` | 30 keys added | Additions only; no existing key was changed or removed |

The header's cart control is still exactly the link to the cart page it was in Phase 4, and with
scripting off that is exactly what it does. A modified click — cmd, ctrl, shift, middle — is left
alone, so it still opens the cart page in a new tab.

---

## 14. Known limitations

### BUSINESS INFORMATION REQUIRED

1. **No products exist yet.** Every state in this phase was rendered against mock data in the
   harness. The theme is correct against the Shopify object model; it has not been run against a
   real catalogue.
2. **Shipping scope.** No shipping claim, threshold or estimate appears anywhere, and none can until
   the policy exists (Phase 1 UX-05, VAL-04).
3. **Currency and markets** (ECOM-09), the **size run** (ECOM-04) and the **peso glyph** (Phase 2
   §27.2) are all still open.
4. **Whether accelerated checkout should show at all**, and for which payment methods. It defaults
   to on and cannot be previewed until the store is configured.
5. **Whether low-stock messaging is wanted.** It is the only thing that would justify exposing
   `inventory_quantity`, and nothing does so today.

### Real gaps

6. **With scripting off, the variant picker does not switch anything.** The radios render, they can
   be chosen, and nothing about the page changes — the value that is submitted is the hidden
   `name="id"` input, which the server rendered for the default variant. A customer without
   scripting can buy that variant and no other.

   This is where Shopify itself now stands: the platform formally dropped the no-JavaScript
   variant-switching requirement, Dawn behaves identically, and the documented alternatives — a
   `<select name="id">` mirror or a link per option value — either collide with the hidden input on
   submit or force a per-value variant resolution in Liquid that the same guidance says to avoid.
   It is recorded here as a genuine gap rather than dressed up: a control that looks operable and
   is not is a real cost, and the honest fix is a small no-JS `<select>` in a later phase once the
   duplicate-`id` submit behaviour can be tested against a real store.

### Deliberate scope decisions

7. **A cart page was built, and it is arguably outside the brief's four-item scope.** The argument
   for: with JavaScript off, the product form this phase is *required* to build posts natively to
   `/cart/add` and Shopify redirects to `/cart`, and Shopify serves an error page for any storefront
   route whose template is missing (Phase 1 SHOP-09). Without `templates/cart.json` the
   no-JavaScript path would end on an error page, and the drawer's own View cart link would too. It
   is therefore the lean version — the same cart lines, the same totals, the same controls, no new
   components — and a fuller cart design remains available to whichever phase owns it.
8. **The remaining templates SHOP-09 lists are still missing**: collection, list-collections,
   search, page, 404, password, gift card and the customer set. They belong to their own phases.
9. **`main-product` uses settings rather than blocks**, for the reason in §1. An app that ships a
   product-page block cannot place itself here. The fix is a `blocks` array with a `{% when '@app' %}`
   arm, and it is a small one.
10. **3D models render their preview image, not a model viewer.** `model_viewer_tag` produces inert
   markup until the theme calls `Shopify.loadFeatures({name: 'model-viewer-ui'})`, and augmented
   reality needs a second, independent call. No God Squad product carries a model, and neither call
   can be verified in the harness because `Shopify.loadFeatures` comes from `content_for_header`.
11. **`product.variants` truncates at 250**, which is the ceiling on the embedded variant table. Not
   a realistic case for apparel; recorded rather than papered over.

### Carried forward

12. **The Phase 4 mobile menu tab-order defect is still open** — the closed panel keeps its links in
   the tab order. One line fixes it and it is not applied, because the briefs forbid touching the
   header beyond what the cart needs.
13. **The header's cart control is a link that opens a dialog.** A screen reader announces "Cart, 3
   items, link" and the customer gets a drawer rather than a page. Focus moves to a heading that
   says "Your cart", so they are told where they are; it is what Dawn and essentially every Shopify
   theme does; and it is what keeps the no-JavaScript fallback a real link. Recorded as a known
   trade-off rather than hidden.
14. **The drawer and the mobile menu can in principle both be open.** The menu traps focus and
   covers the screen, so reaching the cart control from inside it is not a realistic path, and both
   respond correctly to Escape if it happens. Untested against a real device.

15. **The three glyphs Phase 8 added use round caps and mitre-free joins**, which is what every
   glyph Phase 3 drew and Phases 4–7 shipped uses — and which Phase 2 §18.3 rule 2 specifies the
   opposite of. Matching the set is what keeps the icons looking like one drawing, so the deviation
   was left whole rather than half-corrected. It belongs to the icon set and should be settled for
   all of them at once.

### Design-system gaps

16. **Phase 2 defines no product-page title scale.** §27.1 covers only the card's 12px label, so the
   `h1` takes the story scale's size and tracking with the interface family — Jost, per §5.5's rule
   that anything telling the customer *what something is* is Jost. Recorded as a token gap.
17. **Phase 2 §27.4 names `--color-border-current` for a variant chip's boundary, and §12.2
   contradicts it** with a measurement: those tokens composite to about 1.3:1 and fail SC 1.4.11.
   §12.2 wins here, as it already does for `.button--secondary`.
18. **`--type-body-lg-size` carries the product-page price.** No price scale above the card's 15px
   exists in the system.

---

## Phase 8 is complete. Phase 9 has not been started.
