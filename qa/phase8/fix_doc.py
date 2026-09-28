# -*- coding: utf-8 -*-
"""Bring the Phase 8 document up to what the adversarial review changed."""
p = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\PHASE-8-PRODUCT-SHOPPING-UX.md"
s = open(p, encoding='utf-8').read()
done = []


def sub(old, new, label):
    global s
    assert old in s, 'NOT FOUND: ' + label
    s = s.replace(old, new, 1)
    done.append(label)


sub("""Status: **delivered**. 163 structural checks, 70 browser-driven interaction assertions, 55 contrast
measurements and 10 rendered widths across 6 pages — all passing. No file from Phases 0–7 was
modified except the two the cart is obliged to touch, and both are recorded in §13.""",
    """Status: **delivered**. 197 structural checks, 92 browser-driven interaction assertions, 56 contrast
measurements and 10 rendered widths across 8 pages — all passing. No file from Phases 0–7 was
modified except the two the cart is obliged to touch, and both are recorded in §13.

It was then put through a multi-agent adversarial review — 58 findings raised, 46 confirmed after
three independent skeptics each — and every confirmed finding is fixed. The eight blockers among
them are listed in §12, because two of them would have taken a customer's money for the wrong
product.""",
    'status line')

sub("""```liquid
{%- form 'product', product,
  id: form_id,
  class: 'shopify-product-form main-product__form',
  novalidate: 'novalidate',
  data-product-form: 'true' -%}
  <input type="hidden" name="id" value="{{ current_variant.id }}"
         data-variant-input {% unless can_buy %}disabled{% endunless %}>
```

Three things about this are easy to get wrong and are worth recording:

1. **The form tag does not generate the variant input.** It generates `form_type`, `utf8` and
   `product-id` — and `product-id` is not `id`, and adds nothing to a cart. The theme supplies
   `name="id"` itself.
2. **Passing `class:` replaces the tag's own default**, so `shopify-product-form` is repeated in the
   string rather than added to it.
3. **The variant input is disabled when the variant cannot be bought**, so a form submitted by any
   route — Enter in the quantity field, a script, browser autofill — cannot post a sold-out variant.""",
    """```liquid
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
the form entirely.""",
    'the product form')

sub("""- the URL, via `history.replaceState` — **never `pushState`**: trying three sizes must not put three
  entries between the customer and the page they came from""",
    """- the URL, via `history.replaceState` — **never `pushState`**: trying three sizes must not put three
  entries between the customer and the page they came from
- the quantity control's `min`, `max` and `step`, because `quantity_rule` is carried **per variant**
  and a customer who chose a variant with its own minimum would otherwise keep the previous one's
  and be refused at `/cart/add` with no idea why

When a chosen combination resolves to no variant at all — routine on a product whose option grid is
not fully populated — the add-to-cart control is disabled and **the price is left as it was**. An
empty price where a number used to be reads as a broken page.""",
    'what a variant change updates')

sub("""| Announced | every change goes to the shared live region |""",
    """| Announced | every change goes to whichever live region is currently reachable (§9) |
| Without the script | the two stepper buttons are **not rendered** and the browser's own number spinner is left in place. They are `type="button"` and do nothing until `assets/cart.js` binds them; shipping them regardless put two 44px controls on the page that a customer with scripting off could press forever |""",
    'the quantity table')

sub("""| 2 | The button takes `aria-busy="true"`, is disabled, and its label becomes "Adding…" — from a `data-` attribute written by Liquid, so the word is translatable |""",
    """| 2 | The button takes `aria-busy="true"` and its label becomes "Adding…" — from a `data-` attribute written by Liquid, so the word is translatable. It is **not** disabled: disabling the element that holds focus blurs it, so every add dropped a keyboard user back to `<body>`, and re-enabling it afterwards clobbered a sold-out state a variant change had set in the meantime. The double-submit guard reads `aria-busy` instead |""",
    'the add-to-cart table')

sub("""### Section rendering in the same round trip

`sections=cart-drawer,cart-icon-bubble` and `sections_url=<location.pathname>` go with every
mutation, so the drawer and the header badge are always the server's view of the cart after the
change — never a number this file calculated.""",
    """### Section rendering in the same round trip

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
server's view of the cart after the change — never a number this file calculated.""",
    'render targets')

sub("""`sections/cart-drawer.liquid`, rendered once from `layout/theme.liquid` so it is on every page.""",
    """`sections/cart-drawer.liquid`, rendered once from `layout/theme.liquid` so it is on every page
**except `/cart`**. There, the page is the cart: rendering the drawer as well put two views of one
thing on one screen, which can disagree after an update, and gave every cart line a duplicate DOM id
— silently re-pointing the drawer's quantity labels at the page's inputs.""",
    'drawer scope')

sub("""    <div data-cart-drawer-inner>                        replaced after every cart change""",
    """    <div role="status" data-cart-drawer-status>         the drawer's own announcements
    <p data-cart-error role="alert" hidden>             the visible failure line
    <div data-cart-drawer-inner>                        replaced after every cart change""",
    'drawer structure')

sub("""**The heading is outside the swapped region** on purpose: a focused element inside a replaced
subtree is destroyed, and the browser drops focus to `<body>`.""",
    """**The heading, the live region and the error line are all outside the swapped region** on purpose:
a focused element inside a replaced subtree is destroyed and the browser drops focus to `<body>`,
and a live region recreated together with its text announces nothing at all.""",
    'why the heading is outside')

sub("""| Estimated total | `cart.total_price` |

Showing `items_subtotal_price` alone as "the price" silently overstates what the customer will pay
the moment a cart-level discount is active. "Estimated" is accurate: taxes and shipping are
calculated by Shopify at checkout. There is no shipping claim, no delivery estimate and no
free-shipping threshold anywhere — shipping scope is BUSINESS INFORMATION REQUIRED (Phase 1 UX-05,
VAL-04).""",
    """| Estimated total | `cart.total_price` |

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
the other.""",
    'totals')

sub("""A real destination — the store's all-products collection by default, overridable by a merchant
setting — never `href="#"`, and no invented recommendations.""",
    """A real destination, never `href="#"`, and no invented recommendations.

The default is the **home page**, not `routes.all_products_collection_url`. That route is the
obvious answer and the wrong one in this theme today: no `templates/collection.json` exists yet, so
Shopify would have served an error page to every customer who opened an empty cart and pressed the
one button in it. The home page does exist and carries both the New Drop and Best Sellers rows. The
merchant can point it anywhere once a collection template ships.""",
    'empty state')

sub("""### The live region

`<div id="CartStatus" role="status" aria-live="polite">`, in the **layout**, empty at page load, and
carrying `data-cart-no-inert` so it is never removed from the accessibility tree while the drawer is
open. A region created together with its content announces nothing, which is what happens if it
lives inside markup the section render replaces. Text is injected into it inside a `setTimeout`.""",
    """### Two live regions, because `aria-modal` hides one of them

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
locale file.""",
    'live regions')

sub("""| A cart line is updated | back to the equivalent control in the freshly rendered line |
| A cart line is removed | the drawer's heading, because the control that had focus no longer exists |""",
    """| A cart line is updated | back to the equivalent control in the freshly rendered line |
| A cart line is removed | that surface's own heading — the drawer's, or the cart page's `h1` — because the control that had focus no longer exists |
| Add to cart, start to finish | stays on the add button. It is never disabled, only `aria-busy` |""",
    'focus table')

sub("""- **`cart.js` from the layout** (it is needed on every page — the header control and the product
  card's optional quick-add are everywhere); **`product.js` from the product section only**.
- **Stylesheets are requested by the section that needs them**, so a page without a product page
  does not download `section-main-product.css`. The three shared components
  (`component-quantity.css`, `component-cart-line.css`, `component-button.css`) are requested by
  each consumer.""",
    """- **`cart.js` from the layout** (it is needed on every page — the header control and the product
  card's optional quick-add are everywhere); **`product.js` from the product section only**.
- **Section stylesheets are requested by the section that needs them**, so a page without a product
  page does not download `section-main-product.css`. The three shared components —
  `component-button.css`, `component-quantity.css`, `component-cart-line.css` — load from the
  **layout**, because the drawer is rendered there on nearly every page and linking them from the
  sections as well put two `<link>` tags for one URL on every product and cart page. This is the
  same promotion Phase 6 performed for the button system when it acquired a second consumer.""",
    'stylesheet loading')

open(p, 'w', encoding='utf-8', newline='').write(s)
for i, label in enumerate(done, 1):
    print('%2d. %s' % (i, label))
