# -*- coding: utf-8 -*-
"""Phase 18 — one definition of the quick-add error, and no unreachable rules.

TWO FINDINGS, ONE BLOCK, both confirmed by Phase 16 and re-verified here.

1. .product-card__error was defined twice at equal specificity, in
   component-cart-line.css (head) and component-product-card.css (body). Later
   wins PER PROPERTY, so the card's rule took margin, font-size and the border,
   while the cart grouping's `padding: var(--space-3) var(--space-4)` and its
   line-height survived — leaving the element BOXED, which contradicts the
   comment directly above the card's own rule ("Left-ruled rather than boxed").

   The card error and the cart error are legitimately different: one is inline
   in a tile, the other is a block in a panel. So the card leaves the grouping
   rather than the two being forced together.

2. The .surface-light overrides beneath cannot match. Both cart surfaces
   hardcode surface-dark — sections/cart-drawer.liquid:53 and
   sections/main-cart.liquid:37 — and neither schema exposes a surface setting
   (verified: drawer has auto_open/show_view_cart/show_note/empty_link/
   empty_link_label, cart page has empty_link/empty_link_label/show_note).
"""
import io
import os

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
p = os.path.join(THEME, 'assets', 'component-cart-line.css')
s = io.open(p, encoding='utf-8').read()
n0 = len(s)

old = """.cart-drawer__error,
.main-cart__error,
.product-card__error {
  margin: 0;
  padding: var(--space-3) var(--space-4);
  border-inline-start: var(--border-width-strong) solid var(--color-error-on-dark);
  color: inherit;
  font-family: var(--font-body);
  font-size: var(--type-body-sm-size);
  line-height: var(--type-body-sm-lh);
}

.surface-light .cart-drawer__error,
.surface-light .main-cart__error,
.surface-light .product-card__error {
  border-inline-start-color: var(--color-error);
}

/* Phase 12. The quick-add form's failure line joins the same rule rather than
   inventing a third treatment: one look for "this did not work", wherever it
   happens. The card's own top margin is all it adds. */
.product-card__error {
  margin-block-start: var(--space-3);
}"""

new = """/* The CART surfaces' failure line. Phase 18 removed .product-card__error from
   this grouping: it was also defined in component-product-card.css, which loads
   later, and at equal specificity the later rule wins PER PROPERTY rather than
   wholesale. The card took margin, font-size and the border from its own rule
   and the padding and line-height from this one, so it rendered boxed — the
   exact treatment the comment above its own rule says it is not.

   Phase 12 grouped them for a good reason, "one look for this did not work,
   wherever it happens". The reason did not survive contact with the two
   contexts: a failure inside a 300px product tile and a failure across a cart
   panel are not the same object, and forcing one rule to serve both is what
   produced a card with 16px of padding on a side it never asked for.

   No .surface-light override. It cannot match: both cart surfaces hardcode
   surface-dark (cart-drawer.liquid:53, main-cart.liquid:37) and neither schema
   exposes a surface setting, so --color-error-on-dark below is always the
   correct one. The override was five lines that never applied. If a surface
   setting is ever added to either section, this is the rule that has to come
   back with it. */
.cart-drawer__error,
.main-cart__error {
  margin: 0;
  padding: var(--space-3) var(--space-4);
  border-inline-start: var(--border-width-strong) solid var(--color-error-on-dark);
  color: inherit;
  font-family: var(--font-body);
  font-size: var(--type-body-sm-size);
  line-height: var(--type-body-sm-lh);
}"""

assert s.count(old) == 1, 'anchor not unique'
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new, 1))
print('assets/component-cart-line.css  %d -> %d bytes' % (n0, n0 - len(old) + len(new)))
