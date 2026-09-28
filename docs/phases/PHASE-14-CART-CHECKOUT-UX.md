# GOD SQUAD — PHASE 14
## Cart + Cart Drawer + Checkout Experience

**Status:** delivered · **Date:** 2026-09-24 · **Theme:** `god-squad-theme/`

---

## 0. What this phase was, and what it was not

Phase 8 built the cart: the drawer, the cart page, the line component, the
quantity control, the Ajax layer, the empty state, the checkout submit. Phase 14
did not rebuild any of it, and the brief's own instruction — *"Inspect the
current implementation before changing anything. Do not blindly rewrite
completed work"* — is why.

So this phase is an audit with repairs, plus the four things in the Phase 14
scope list that Phase 8 did not own:

- **four defects**, three of them live on the storefront today
- **the order note**, which did not exist
- **continue shopping**, which the cart page had no route to at all
- **a visible add confirmation** for stores whose cart style is "Cart page"
- **the desktop cart layout**, which ran one column to 1440px

Every defect below was **reproduced with a failing test before it was fixed**,
and every fix was **negative-controlled** — reverted, watched to fail again,
restored. A test that has never been seen to fail proves nothing, and this
project has twice shipped a green test that was asserting on a comment.

---

## 1. Cart architecture

Unchanged from Phase 8, and restated here because everything below depends on
it.

**Shopify is the cart.** There is no client-side cart object, no localStorage,
no second source of truth. `grep` confirms it: no `localStorage`,
`sessionStorage`, `indexedDB` or `document.cookie` appears in any theme script.
After a refresh the cart is whatever the server says it is, because that is the
only place it has ever been.

**Every control works without JavaScript.** The product form posts natively to
`/cart/add`. The cart form posts natively to `routes.cart_url` with `updates[]`.
Removal is `item.url_to_remove`. The header cart control is a link to `/cart`.
`assets/cart.js` cancels those defaults and does the same work over Shopify's
Ajax Cart API; if it fails to load, all of them still work with a reload.

**One file, no dependencies.** `assets/cart.js` is 38,737 bytes, of which 46% is
comment — 20,390 bytes of executable code. It creates exactly one global,
`window.GodSquad.cart`. A dead-code scan of all 31 named functions found **no
function referenced only by its own declaration**.

**Mutations carry their own re-render.** Sections are requested in the same
round trip as the mutation, so the drawer, the cart page and the header badge
are always the server's view of the cart after the change — never a number this
theme calculated.

### 1.1 Four defects, found and fixed

#### D1 — The cart page's Update button was never hidden `LIVE`

`sections/main-cart.liquid` renders a `name="update"` submit for the
no-JavaScript path. The theme states in writing that it is removed once the
cart script runs, because there it does nothing: quantity changes are applied as
they are made and the page re-renders itself.

The rule that hid it was:

```css
/* assets/section-cart-drawer.css */
.cart-js .cart-drawer__update,
.cart-js .main-cart__update { display: none; }
```

`section-cart-drawer.css` is loaded by `sections/cart-drawer.liquid`, and
`layout/theme.liquid` does not render the drawer on the cart template. **The one
page that has a `.main-cart__update` is the one page that never loads the
stylesheet hiding it.** Measured before the fix: `display: inline-flex`.

The `.main-cart__update` half now lives in `section-main-cart.css`, which that
page does load. This is the Phase 12 lesson again in a new costume: *a selector
is not a rule until something on the page it names has read the file it is in.*

#### D2 — A cart failure printed itself onto product tiles `LATENT`

`showCartError()` selected `[data-cart-error]` **document-wide**. The quick-add
product card carries one. So a quantity Shopify refused in the drawer would have
written "You can't add more…" into the error line of every product tile on the
collection page behind it.

Reproduced by injecting the card's exact markup into a cart page and failing a
quantity change; the card carried the cart's message. `showCartError` is now
scoped to `[data-cart-drawer] [data-cart-error], [data-cart-page] [data-cart-error]`.

Marked **latent** honestly: no section currently passes `quick_add`, so no page
renders a second error box today. See §19.

#### D3 — A removed line came back 250ms later `LIVE`

Quantity steps are debounced by 250ms. Removal calls `changeLine()` directly.
Neither cancelled the other, so stepping a quantity and then removing the line
inside that window sent **two** requests:

```
POST /cart/change.js  {id: "k2:bbb", quantity: 0}   ← the removal
POST /cart/change.js  {id: "k2:bbb", quantity: 2}   ← 250ms later
```

The customer removes an item, watches it go, and it returns at quantity 2 — or,
if Shopify has already dropped the key, they get "Unable to update your cart"
immediately after a removal that worked. `changeLine()` now clears
`pending[key]` on entry: an immediate change supersedes a queued one by
definition.

#### D4 — A quick-add failure was shown to nobody `LATENT`

The product card carried `data-cart-error`. `showFormError()` looks inside the
form for `[data-product-error]`. The two never met, so a failed quick add fell
through to the live region: a screen-reader user heard it, a sighted customer
watched the card sit there unchanged.

This is precisely the defect the comment beside that markup claims to have
fixed. The fix had used the wrong attribute name, and the Phase 12 test asserted
the box **existed** rather than that the add path could **find** it — so the
test was green while the bug was live. The card now carries
`data-product-error`, `.product-card__error` has styling (it had none at all),
and the Phase 12 assertion now names the function that has to find it.

---

## 2. Cart drawer architecture

`sections/cart-drawer.liquid` + `assets/section-cart-drawer.css`. Rendered once
from `layout/theme.liquid` as a **statically rendered section**, so its id is its
filename and `cart.js` never has to discover it at runtime. Not rendered on the
cart template, and not rendered at all when `settings.cart_type` is `page`.

- `role="dialog"` + `aria-modal="true"`, with the page's other top-level regions
  marked `inert` on open — which removes them from the tab order, the
  accessibility tree, pointer input and find-in-page in one attribute.
- Not a `<dialog>`: `showModal()` promotes the panel out of its stacking
  context, splits the scrim into a `::backdrop` that cannot animate as one group
  with the panel, and brings a live hazard into a cart — a stray
  `method="dialog"` silently closes it and discards the POST.
- Width `--drawer-width: min(90vw, 420px)`. Measured at 420px on every desktop
  viewport and 338/351/387px at 375/390/430.
- Close: the X, Escape, the overlay, and now **Continue shopping**.

### 2.1 The short-viewport failure, found by adding the note

Putting the order note in the drawer footer broke the drawer in landscape.
Measured at an 812×283 viewport with a note written:

```
footer  69 .. 520   (451px tall, 145px past the bottom of a 283px viewport)
scroller     0px    against 474px of cart lines
```

The customer could read their note and reach Checkout, and could not see or
change a single thing they were buying.

Two changes, because there were two problems.

**The note moved into the scroller.** The footer is *chrome* — the totals and the
actions, the things that must stay put. The note is *content*. Content in the
chrome makes the chrome grow with it.

**Below 540px of height the drawer stops pinning its footer at all.** The
structural fault is that `.cart-drawer__scroller` is `flex: 1; min-height: 0` —
it is the only thing that can give — while the footer is intrinsically sized and
cannot. Whenever header + footer exceed the panel, the scroller goes to zero and
the footer overflows. The existing landscape block only trimmed padding, worth
about 30px; Phase 9's own measurement (scroller 0px → 44px) shows how little
that left. Below 540px the panel is now a single scrolling column: Checkout is
no longer permanently on screen, but it is always **reachable**, and on a screen
that cannot show both that is the correct trade.

After: scroller 68px, footer inside the panel, Checkout and the first cart line
both verified as scrollable into full view at 812×283 and 375×812.

---

## 3. Cart page architecture

`sections/main-cart.liquid` + `assets/section-main-cart.css`, driven by
`templates/cart.json`. It works entirely independently of the drawer, and the
two never coexist — verified on all three cart-page fixtures.

**Phase 14 gave it a second column.** Below 1024px it is one column: lines, then
totals under them, which is the only honest order on a phone. From 1024px:

```css
.main-cart__form {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 24rem;
  gap: var(--space-8);
  align-items: start;
}
```

This is not decoration. At the 1440 container the single column ran the cart
lines to 1344px, so a 120px thumbnail sat beside a product title with roughly
1000px of empty rule between it and its own price — the eye had to cross the
whole viewport to pair a name with a number.

`24rem` fixed rather than a fraction: the summary holds a fixed set of short
lines and a button, and a fraction would stretch the same content wider on a
wider screen for no reason.

The summary is `position: sticky` at `--header-offset-desktop` — the same offset
the product page's buying column uses — with its own `max-height` and scroll, so
a long note or a stack of discounts can never hide Checkout under the column's
own bottom edge (WCAG 2.2 SC 2.4.11).

---

## 4. Add-to-cart behaviour

### 4.1 States

| State | How it is produced |
|---|---|
| Default | `data-label-idle` |
| Adding | `aria-busy="true"` + `data-label-busy`; **never `disabled`** |
| Added | drawer opens, or the confirmation line (§4.2) |
| Sold out | `disabled` + `data-label-sold-out`, from `variant.available` |
| Unavailable | `data-label-unavailable` — a combination with no variant at all, which is not the same fact as sold out |
| Error | Shopify's own `description`, in `[data-product-error]` |

**`aria-busy` only, never `disabled`.** Disabling the element that holds focus
blurs it, so every add dropped a keyboard user to `<body>`; and restoring it
afterwards asserted `disabled = false` with no knowledge of why it might be
disabled — switch to a sold-out size mid-flight and the response re-enabled a
button for a variant that cannot be bought. The double-submit guard reads
`aria-busy` instead. Verified: the button is never left stuck in *Adding*, on
success, on a 422 and on a transport failure.

### 4.2 Feedback — the Phase 14 addition

When the drawer opens, **the drawer is the confirmation**: it shows the customer
exactly what the cart now holds. The addition is deliberately *not* announced in
that case, because announcing and moving focus at the same moment makes a screen
reader talk over itself.

But the drawer is optional twice over — a merchant can set the cart style to
"Cart page", and can switch auto-open off. In both, the only sighted response to
pressing **Add to cart** was the header count changing by one in the far corner
of the screen. The brief asks for "a clear success confirmation" and that was
not one.

`[data-product-success]` is a `role="status"` line under the form carrying the
sentence and a link to the cart. `role="status"`, not `alert`: the customer got
what they asked for, so it waits its turn instead of interrupting.

That also makes it **self-announcing**, which is why `cart.js` only writes to
the live region when the form has no such line:

```js
if (!showFormSuccess(form, stringFor('added', null))) {
  announce(stringFor('added', null));
}
```

Verified both ways: with no drawer the line is shown and the live region stays
empty; with a drawer the drawer opens and no second confirmation appears. A
later failure clears the stale confirmation and shows the error in its place.

No confetti, no full-screen animation. The brief rules them out and so does the
brand.

### 4.3 Cart count

`cart.item_count`, never a literal, rendered by one snippet with two consumers —
`sections/header.liquid` inline, and `sections/cart-icon-bubble.liquid` as the
Section Rendering API target. Dawn keeps two parallel copies and they drift; one
snippet cannot.

An empty cart shows **no badge at all**, so nothing announces "0 items" — the
control's own name is still "Cart", which is the whole message when the cart is
empty. Accessible name when full: *"Cart, 2 items"*.

### 4.4 Quick add

`snippets/product-card.liquid` refuses to guess. More than one variant →
a **Choose options** link to the product page. One variant, available → a real
form carrying `product.selected_or_first_available_variant.id`. Unavailable → a
real `<button aria-disabled>`, never a `<span>` wearing button classes.

It therefore **cannot add an incorrect variant**, which is what the brief's
COLLECTION → CART test asks. Its error wiring was D4 above, now corrected.

---

## 5. Quantity handling

`snippets/quantity-selector.liquid` — three consumers: the product form, the
drawer line, the cart page line.

- **Floor is 1.** The minus button takes `aria-disabled` at the minimum rather
  than clamping silently, so the control never looks live while doing nothing.
  The input carries `min`, so a typed `0` or `-3` is rejected by the browser
  *and* by the script. Removal is the explicit control beside it, not the last
  press of a decrement.
- **The ceiling is Shopify's.** `max` comes from the variant's own quantity rule
  when one exists. No inventory number is ever rendered.
- **Accessible names are per product**: *"Increase quantity for Heavyweight
  Hoodie"*, not `+`.
- **`updates[]` is positional**, so exactly one input is emitted per line, in
  cart order, with no gaps and no conditionals. A quantity field wrapped in a
  condition that can be false would shift every later line's quantity onto the
  wrong product.

### 5.1 Race conditions

| Behaviour | Result |
|---|---|
| The number on screen | moves on **every** press, with no wait |
| Five rapid presses | **one** request, carrying the fifth value |
| Two lines changed quickly | **one request each**, each with its own line key |
| A superseded response | its markup is discarded; its busy state and its error are **not** |
| Remove during the debounce | the queued change is cancelled (D3) |

Lines are identified by **line item key**, never by index and never by variant
id — two lines can share a variant id (same variant, different properties, or
split by an automatic discount), and an index shifts the moment anything is
removed. The key is re-read from freshly rendered markup every time rather than
cached.

Only the markup swap is gated on the sequence number. Returning early on the
sequence check left a line dimmed and inert forever and swallowed the reason a
change was refused.

---

## 6. Remove behaviour

A text control, not a glyph: Phase 2 §18.1 closes the icon set to decorative
additions and contains no bin mark, and in a 420px drawer a word is less
ambiguous than an icon at 44px. Accessible name: *"Remove Heavyweight Hoodie
from your cart"*.

The href is Shopify's own `item.url_to_remove`, so it works with no script. With
script, the navigation is cancelled and the same thing happens over the Ajax
API. There is **no undo**, per the brief.

After a removal, focus does not fall to `<body>`: the line being acted on is
remembered before the section swap and the equivalent control focused after it;
if that line is gone — which is what removal means — focus goes to the surface's
heading, which is why both headings sit outside the node being replaced.

---

## 7. Error handling

| Failure | What the customer sees |
|---|---|
| 422 from `/cart/add` | Shopify's own `description`, in the form's error line |
| 422 from `/cart/change` | Shopify's own `description`, on the cart surface |
| 422 from `/cart/update` (note) | the same, on the cart surface |
| Transport failure | *"We could not reach the store. Check your connection and try again."* |
| Anything else | *"Unable to update your cart. Please try again."* |
| A line Shopify cannot honour | `item.error_message`, the platform's own text |

**No raw API error is ever shown.** No status code, no exception, no stack.
Verified: the 422 message reaches the customer and the string `422` does not.

Three things that are easy to get wrong and are handled:

1. **A 422 from `/cart/add` can mean the cart changed anyway.** When the
   requested quantity exceeds stock, Shopify adds the maximum it can *and*
   returns the error. So an error response is never treated as "nothing
   happened" — the rendered sections are applied either way, because showing the
   old cart would be a lie.
2. **A failure is visible, not just audible.** Every cart surface carries a
   visible error line, and it sits *outside* the node the section render
   replaces, so the message survives the re-render that produced it. Before
   Phase 8 this was announced only to a screen reader, leaving a sighted
   customer watching a number snap back with no explanation.
3. **The cart is never left disabled.** The busy state is always cleared, even
   for a superseded request, so the customer can always retry.

---

## 8. Empty state

`snippets/cart-empty-state.liquid` — two consumers, one snippet. Verified on
both surfaces: **no checkout control, no quantity control, no cart line, no note
field, and no invented product.** The checkout CTA is not disabled, it is
**absent**, which is the strongest form of "not active".

> YOUR CART IS EMPTY.
> Find something that speaks to your purpose.
> [ Shop the collection → ]

The default destination is the **home page**, not `/collections/all`. That was
written when no collection template existed; one exists now, so a merchant can
point it anywhere — but the fallback stays the page that is certain to render.

---

## 9. The order note (new)

`snippets/cart-note.liquid` — two consumers, one snippet.

**Off by default, per surface.** Whether this store wants order notes is
business information nobody supplied, and the brief is explicit: *"If not
required: do not add a large unnecessary field."* So it is a merchant setting,
default `false`, on both the drawer and the cart page. The setting's help text
says the quiet part: *"Turn this on only if you act on what customers write
there — a field nobody reads is worse than no field."*

**It is one field named `note`**, because that is the whole feature. Shopify's
cart carries a single free-text note. A second field, a dropdown of reasons or a
gift-message variant would all be inventing store policy.

**Labelled "Order note"**, which the brief names, and never "Special
instructions", which the brief rules out. Both strings are in the locale file.

**A native `<details>`.** A permanently open textarea costs about 120px, which in
a 420px drawer is taken from the cart lines. This is safe because of a fact
Phase 13 established and tested: *form controls inside a closed `<details>` are
still submitted.* It renders **open** when the cart already carries a note, so an
existing note is never hidden behind a control the customer has to find.

### 9.1 Saving it

With scripting off, the note posts with the form — Update or Checkout saves it,
and no script is needed.

With scripting on it must be saved separately, and this is the part that is easy
to get wrong: **a quantity change re-renders the cart from the server, and the
server does not know about text the customer has only typed.** Without handling,
editing the note and then changing a quantity throws the note away.

- Saved on `change`, not `input` — it fires once, when the field is left with a
  different value, so a note is one request and not one per keystroke.
- Through Shopify's own `/cart/update.js`, with `{note: value}` and **no
  sections requested**, because nothing on the page displays the note's value.
  It is the cheapest mutation the cart makes.
- An **unsaved** note is carried across a section swap, and focus returns to the
  field rather than to the heading — the note is the one control in the swapped
  node that does not belong to a line, so the key-based focus path could not
  find it and threw the customer to the heading mid-sentence.

All four verified, and all four negative-controlled.

---

## 10. Continue shopping (new)

**The cart page had no route back to shopping at all.** Its only controls were
Update and Checkout, so a customer who did not want to check out had nothing but
the browser's Back button — which the brief rules out by name.

The two surfaces get different controls, deliberately:

- **Cart page: a link.** Arriving on `/cart` is a navigation; there is nothing to
  return to. It goes wherever the merchant sends an empty cart — the same
  question asked twice — falling back to the shop root.
- **Drawer: a button that closes the drawer.** The drawer is a layer over the page
  the customer was shopping, and closing it returns them there. A link would
  navigate them away from the thing they were looking at in order to let them
  carry on looking at it. It reuses `[data-cart-close]`, so it is the drawer's
  one close path rather than a second one.

Both are quiet text controls under the two buttons, not a third button: this is
the way *out* of a decision, and giving it a button's weight would compete with
Checkout, which is the way *through*.

---

## 11. Checkout integration

**Shopify's, entirely.** Verified by test on both surfaces:

- a `<button type="submit" name="checkout">` inside the cart form — Shopify's own
  control, which applies any pending quantity edits *and then* goes to checkout
  in one action. A plain link to `/checkout` would silently discard an edit the
  customer had just made.
- the form posts to `{{ routes.cart_url }}`
- **no checkout URL is constructed anywhere**, and no `checkout_url` is
  referenced
- **no payment field of any kind** exists in the theme — no card number, no CVV,
  no expiry
- **no shipping calculator, no tax calculation.** The tax line is *derived*, not
  asserted: `cart.taxes_included` decides which sentence is shown, because
  printing "Taxes and shipping are calculated at checkout" unconditionally would
  be a claim about this merchant's tax configuration that nobody supplied — and
  wrong for any tax-inclusive market, which the Philippines is.
- `content_for_additional_checkout_buttons` renders on the cart page, guarded by
  `additional_checkout_buttons`, so it appears only if the store actually has
  accelerated checkout.

Checkout branding is a Shopify Admin concern and is **not** reproduced in the
theme. See §15.

---

## 12. Accessibility

| Area | State |
|---|---|
| Semantics | `<button>` for actions, `<a>` for navigation, `<input>`/`<textarea>` for entry. No clickable `<div>` or `<span>` anywhere in the cart. |
| Dialog | `role="dialog"` + `aria-modal="true"` + `aria-labelledby`, background `inert` |
| Focus on open | the drawer heading — not the close button, which announces "Close, button" and says nothing about what just happened |
| Focus on close | the element that opened it, or the cart control if that element has been re-rendered away |
| Focus across a swap | the equivalent control on the same line; the note if that is where it was; the heading if the line is gone |
| Live regions | one in the layout, one inside the drawer — because `aria-modal="true"` makes the layout's region unreachable while the drawer is open |
| Announcements | never doubled: the confirmation line is `role="status"`, so the live region stays silent when it is used |
| Keyboard | Escape closes; Escape is **not** intercepted while closed; Tab is trapped only where `inert` is unsupported |
| Reduced motion | drawer, quantity and note transitions all removed under `prefers-reduced-motion` |
| Focus visible | every new control has a `:focus-visible` ring; no global `outline` removal |
| Contrast | **73 measurements, 73 pass** — see §13 |

The quantity debounce is a hard 250ms literal and deliberately *not* a motion
token: `--duration-*` collapses to 1ms under `prefers-reduced-motion`, which
would remove the debounce for exactly the people most likely to be stepping a
quantity from a keyboard.

### 12.1 Contrast

Every new Phase 14 role measured on the rendered page:

| Role | fg | bg | size/weight | ratio | needs |
|---|---|---|---|---|---|
| note label | `#BDB6A8` | `#0D0C0A` | 12/600 | 9.70 | 4.5 |
| note field text | `#F3EFE6` | `#0D0C0A` | 16/400 | 17.04 | 4.5 |
| note help | `#BDB6A8` | `#0D0C0A` | 12/400 | 9.70 | 4.5 |
| continue shopping (drawer) | `#BDB6A8` | `#0D0C0A` | 14/400 | 9.70 | 4.5 |
| continue shopping (page) | `#BDB6A8` | `#0D0C0A` | 14/400 | 9.70 | 4.5 |
| add confirmation | `#0D0C0A` | `#F3EFE6` | 14/400 | 17.04 | 4.5 |
| confirmation link | `#0D0C0A` | `#F3EFE6` | 14/400 | 17.04 | 4.5 |
| add failure line | `#0D0C0A` | `#F3EFE6` | 14/400 | 17.04 | 4.5 |

The note field is 16px for a reason beyond type: below 16px iOS zooms the
viewport the moment the field takes focus, and a zoomed cart is a cart the
customer has to pan to read.

Neither the confirmation nor the error carries meaning in colour alone — both
say it in words (SC 1.4.1), and the confirmation's link is underlined rather
than relying on colour to read as a link.

---

## 13. Mobile UX

Measured at every viewport in the brief, plus two landscape cases.

**375 / 390 / 430 px** — image, title, variant, price, quantity, remove,
subtotal and checkout all usable; drawer 338 / 351 / 387px wide; no horizontal
overflow; no touch target under 24px anywhere.

The only sub-44px targets are `.cart-line__title` text links (230×24), which are
inline links inside a line whose image and controls are all full-size — a
pre-existing, accepted soft flag carried from earlier phases, not a Phase 14
regression.

**Landscape** is the case that broke and was fixed — see §2.1.

---

## 14. Desktop UX

**1280 / 1440 / 1920 px** — drawer 420px at all three (`min(90vw, 420px)`), so it
is substantial without dominating. The cart page is capped at
`--container-standard` (1440px), so 1920 adds margin rather than width, and from
1024px it is the two-column layout of §3 with a sticky summary.

No horizontal overflow at any viewport, with the drawer open or closed.

---

## 15. Performance

| Asset | raw | gzip |
|---|---:|---:|
| `cart.js` | 38,737 | 11,783 |
| `header.js` | 13,963 | 4,319 |
| `product.js` | 18,096 | 5,597 |
| `facets.js` | 7,055 | 2,473 |
| **all JS** | **77,851** | **24,172** |
| `section-cart-drawer.css` | 15,354 | 5,214 |
| `section-main-cart.css` | 6,683 | 2,527 |
| `component-cart-line.css` | 13,769 | 3,725 |
| `component-quantity.css` | 6,123 | 2,514 |
| **all CSS (19 files)** | **239,386** | **77,778** |

No page loads all of it. `section-cart-drawer.css` is linked by the drawer
section and therefore absent on `/cart`; `section-main-cart.css` only on `/cart`.

- **No dependencies.** No framework, no polyfill, no library.
- **No polling.** No `setInterval` anywhere.
- **No duplicate requests.** One delegated listener per event type for the whole
  document, so markup the Section Rendering API swaps in needs no re-binding —
  which is also what keeps the file from leaking listeners on every cart update.
  Measured: five section re-renders add **zero** document listeners.
- **Cart images are sized for their slot** — `image_url: width: 300` with
  `widths: '76, 96, 120, 152, 192, 240, 300'` and `sizes` declaring 76px in the
  drawer, 96px on the cart page below 768 and 120px above it. No original-
  resolution product photography is ever requested.
- **`sections_url` is `location.pathname`**, which must begin with a slash or the
  whole request returns 400 — and Shopify's docs warn that a 400 for this reason
  does not mean the mutation was rolled back.

---

## 16. Theme Editor compatibility

Phase 11's architecture is intact. Phase 14 added **two settings, both
checkboxes, both defaulting to off**:

| Section | Setting | Default |
|---|---|---|
| Cart drawer | Let customers add an order note | `false` |
| Cart | Let customers add an order note | `false` |

And re-labelled one: the cart page's `empty_link` is now *"Where the shopping
buttons go"*, because Continue shopping uses the same destination.

Nothing else was exposed. **No drawer width, no animation speed, no overlay
opacity, no padding** — the brief rules them out and so does Phase 11.

### 16.1 The lifecycle test

Phase 11's finding was that editor defects are invisible to markup tests: a
section re-rendered in place is a new DOM node, and everything the old one put
*outside* itself outlives it. `cart.js` claims in writing to handle this. Phase
14 tested the claim, on the drawer, with the drawer **open**:

- an editor re-render releases the scroll lock, un-inerts the background, drops
  the `cart-drawer-open` class and releases the document keydown listener
- the drawer still opens afterwards, focus still moves to its heading, Checkout
  and the quantity controls are still there, Escape still closes it
- **five setting toggles add no document listeners**, leave exactly one cart form
  and at most one note field, and the drawer still opens and still unlocks

Negative-controlled: with the teardown disabled, five of those assertions fail —
the page stays scroll-locked, the background stays inert, and focus lands on
`<body>`.

---

## 17. Shopify Admin requirements

Nothing in Phase 14 is blocked on the Admin, but four things belong there and
not in the theme:

1. **Checkout branding** — logo, colours and type at checkout are configured in
   *Settings › Checkout › Branding*, not in this theme. The brief forbids
   reproducing checkout inside the theme and none of it is.
2. **Shipping rates** — *Settings › Shipping and delivery*. The theme builds no
   shipping calculator; the cart says shipping is calculated at checkout and
   nothing more.
3. **Taxes** — *Settings › Taxes and duties*. Whether prices include tax drives
   `cart.taxes_included`, which is what chooses the cart's tax sentence. If the
   store is configured tax-inclusive, the cart will say so automatically.
4. **Accelerated checkout** — *Settings › Payments*. The cart page renders
   Shopify's dynamic checkout buttons only when the store has them.

Carried forward and still outstanding from Phase 13: **filtering renders nothing
until filters are created in *Apps › Search & Discovery › Filters***.

---

## 18. Testing results

Every suite, final run:

```
=== markup and platform contract ===
validate            198 / 198
cartdoc (new)        84 /  84
layout               19 /  19      surfaces      41 /  41
settings             28 /  28      catalog       55 /  55
cardcascade          10 /  10      facets        62 /  62
editor               10 /  10

=== driven in a real browser ===
interact             49            interact_cartpage   17
interact_product     26            cartqa (new)        14
notes (new)          40            lifecycle (new)     18

=== measured ===
contrast8            73 measurements, 73 pass
respond              18 pages x 12 viewports — 0 hard problems
console              38 pages — 0 errors
```

**744 assertions, 0 failures.** Plus 216 viewport measurements and 38 console
checks.

The browser suites were run under **Edge 153** and **Chrome**, both green. Both
are Chromium — see §19 on what that does and does not prove.

### 18.1 The brief's test matrix

| Case | Where it is covered |
|---|---|
| 1 product / 2 products / multiple quantities | `c-one`, `c-noted`, `c-many` fixtures |
| multiple variants | `c-many` — two sizes of one product as separate lines |
| sold-out product / variant unavailable | `p-soldout`, `p-sizes`; `data-label-unavailable` |
| cart note if enabled | `c-note`, `c-noted`, `c-page-note` |
| empty cart | `c-empty`, `c-page-empty` |
| quantity increase / decrease | `cartqa`, `interact`, `interact_cartpage` |
| remove item | `interact`, `interact_cartpage` |
| rapid quantity changes | `cartqa` — five presses, and two lines at once |
| page refresh | no client-side cart state exists to go stale (§1) |
| navigation away and back | drawer re-init verified by `lifecycle` |
| drawer open/close | `interact` — X, Escape, overlay; `cartdoc` — Continue shopping |
| mobile / desktop drawer | `respond`, 12 viewports; `notes` geometry at 812×283 and 375×812 |
| checkout | `cartdoc` — native submit, no constructed URL, no payment UI |

### 18.2 Data hygiene

Asserted across all seven cart Liquid files:

- no currency symbol written in markup; every price through `| money`
- no product name, size or colour written in markup
- no `inventory_quantity`, no "Low stock", no "In stock", no "left"
- no invented discount — only `line_level_discount_allocations` and
  `cart_level_discount_applications`, Shopify's own
- the count is `cart.item_count`, and absent when the cart is empty
- every cart line field from `item.*`; the variant shown by option, never by id

---

## 19. Known limitations

1. **Theme Check was not run.** Shopify CLI is not installed in this
   environment — `shopify` is not on the PATH. Every check it would perform on
   the cart that could be reproduced without it was reproduced: schema validity,
   translation completeness (0 missing across 21 fixtures), undefined custom
   properties, raw hex, `!important`, and unreferenced assets. **Run
   `shopify theme check` before going live.**

2. **Quick add is unreachable.** `snippets/product-card.liquid` contains a
   complete, correct quick-add implementation — and **no section passes
   `quick_add`**, so no template renders it. Its two defects (D2, D4) are
   therefore latent rather than live, and both are fixed. Exposing it is a
   one-line setting per section, but that is a catalog decision that belonged to
   Phase 12 and was deliberately not taken there; Phase 14's scope list does not
   include it. Flagged for your call rather than decided here.

3. **Cross-browser testing is Chromium-only.** Edge and Chrome both pass, but
   they share an engine, so that mainly rules out harness artefacts. **Safari
   (WebKit) and Firefox (Gecko) are untested.** The two things most worth
   checking there: the `position: fixed` scroll lock on iOS Safari, and
   `inert` support, which the trap falls back to a Tab cycle without.

4. **No real Shopify store.** Every test renders the real `.liquid` files against
   mock cart data through the Mini-Liquid harness, and every Ajax response is a
   stub shaped to the documented API. That proves the markup, the wiring and the
   requests sent. It does not prove Shopify's actual responses, real money
   formatting for PHP, real discount allocations, or checkout itself.

5. **The order note has no length limit.** Shopify's own limit applies at the
   API; the theme adds none, because inventing one would reject text Shopify
   would have accepted.

6. **The drawer has no accelerated checkout buttons.** Only the cart page renders
   `content_for_additional_checkout_buttons`. That is deliberate — it can appear
   only once per page — and the drawer's Checkout submit reaches the same place.

---

## 20. Future recommendations

Not done, deliberately, and each is someone's decision rather than an oversight:

- **Decide on quick add** (§19.2). The code is written and correct.
- **Free-shipping progress / order threshold** — needs a real threshold from the
  business, and inventing one is exactly the fake-data failure this project has
  refused at every phase.
- **Cart recommendations** — ruled out for this phase, and there is no
  recommendation data to draw on.
- **Discount code entry in the cart** — Shopify's cart accepts one, but checkout
  already collects it, and a second field that can disagree with checkout is a
  support burden. Worth revisiting only if the business runs codes heavily.
- **Run Theme Check and a real-store QA pass** before launch (§19.1, §19.4).

---

**STOP AFTER PHASE 14.**
