# -*- coding: utf-8 -*-
"""Rewrite the testing and limitations sections around the review."""
p = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\PHASE-8-PRODUCT-SHOPPING-UX.md"
s = open(p, encoding='utf-8').read()

start = s.index('| Pass | Coverage | Result |')
end = s.index('### Three known Phase 7 validator failures')
new_table = """| Pass | Coverage | Result |
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

"""
s = s[:start] + new_table + s[end:]
open(p, 'w', encoding='utf-8', newline='').write(s)
print('testing section rewritten')
