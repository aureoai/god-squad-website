# -*- coding: utf-8 -*-
"""Phase 14 — the stylesheet changes."""
import io
import os

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
class F(object):
    def __init__(self, rel):
        self.path = os.path.join(THEME, rel)
        self.rel = rel
        self.s = io.open(self.path, encoding='utf-8').read()
        self.n0 = len(self.s)

    def sub(self, old, new, label):
        if old not in self.s:
            raise SystemExit('NOT FOUND in %s: %s' % (self.rel, label))
        if self.s.count(old) != 1:
            raise SystemExit('AMBIGUOUS (%d) in %s: %s' % (self.s.count(old), self.rel, label))
        self.s = self.s.replace(old, new, 1)
        print('  ok  %-30s %s' % (self.rel, label))

    def append(self, text, label):
        self.s = self.s.rstrip() + '\n' + text
        print('  ok  %-30s %s' % (self.rel, label))

    def save(self):
        io.open(self.path, 'w', encoding='utf-8').write(self.s)
        print('      %-30s %d -> %d bytes' % (self.rel, self.n0, len(self.s)))


# ================================================ 1. the drawer's stylesheet
# It held the rule that hides the CART PAGE's Update control — a page that
# never loads this file, because the layout does not render the drawer there.
drawer = F('assets/section-cart-drawer.css')
drawer.sub(
    """.cart-js .cart-drawer__update,
.cart-js .main-cart__update {
  display: none;
}""",
    """.cart-js .cart-drawer__update {
  display: none;
}

/* The cart page's copy of this rule is NOT here. It was, and it never applied:
   layout/theme.liquid does not render the drawer on the cart template, so the
   page that carries .main-cart__update is the one page that never loads this
   stylesheet. The Update button sat visible beside Checkout on every scripted
   cart page, doing what the Ajax layer had already done. The rule now lives in
   section-main-cart.css, which that page does load.

   The general lesson, which Phase 12 learned the same way: a selector is not a
   rule until something on the page it names has read the file it is in. */""",
    'the cart page half of the hide rule moves out')

drawer.sub(
    """/* ------------------------------------------------------------- landscape""",
    """/* ------------------------------------------------------- continue shopping
   The named form of the close X. A quiet text control under the two buttons:
   it is the way OUT of a decision, and giving it a third button's weight would
   compete with Checkout, which is the way through. */

.cart-drawer__continue {
  display: block;
  width: 100%;
  min-height: var(--target-min);
  margin-block-start: var(--space-3);
  padding: var(--space-2);
  border: none;
  background: none;
  color: var(--color-text-current-muted);
  font-family: var(--font-body);
  font-size: var(--type-body-sm-size);
  letter-spacing: var(--type-label-ls);
  text-transform: uppercase;
  text-align: center;
  cursor: pointer;
  transition: color var(--transition-fast);
}

.cart-drawer__continue:hover {
  color: inherit;
}

.cart-drawer__continue:focus-visible {
  outline: var(--focus-width) solid var(--focus-ring);
  outline-offset: var(--focus-offset);
}

@media (prefers-reduced-motion: reduce) {
  .cart-drawer__continue {
    transition: none;
  }
}

/* ------------------------------------------------------------- landscape""",
    'continue shopping')


# ================================================== 2. the cart page's own
page = F('assets/section-main-cart.css')
page.sub(
    """.main-cart__update {
  margin-block-end: var(--space-3);
  width: 100%;
}""",
    """.main-cart__update {
  margin-block-end: var(--space-3);
  width: 100%;
}

/* Hidden once the cart script is running, because there it does nothing:
   quantity changes are applied as they are made and this page re-renders
   itself, so the control is a tab stop that leads to a no-op.

   This rule used to live in section-cart-drawer.css beside the drawer's
   identical one. That file is loaded by sections/cart-drawer.liquid, and the
   layout does not render the drawer on the cart template — so on the only page
   that has a .main-cart__update, the rule hiding it was never loaded. It is
   here now, in the stylesheet this page actually links.

   The class is `cart-js`, which assets/cart.js sets on itself — NOT the
   layout's `js` class, which an inline script sets whether or not the cart
   script ever arrives. Keying on `js` would hide the only control that can
   apply a quantity change in precisely the case where nothing else can. */
.cart-js .main-cart__update {
  display: none;
}""",
    'the hide rule arrives where it applies')

page.sub(
    """/* ------------------------------------------------------------------ empty */""",
    """/* --------------------------------------------------------- continue shopping
   The route back to shopping, which this page had none of. Quiet, under the
   two buttons, for the reason the drawer's copy records: it is the way out of
   a decision and must not compete with Checkout. */

.main-cart__continue {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: var(--target-min);
  margin-block-start: var(--space-3);
  color: var(--color-text-current-muted);
  font-family: var(--font-body);
  font-size: var(--type-body-sm-size);
  letter-spacing: var(--type-label-ls);
  text-transform: uppercase;
  text-align: center;
  transition: color var(--transition-fast);
}

.main-cart__continue:hover {
  color: inherit;
}

@media (prefers-reduced-motion: reduce) {
  .main-cart__continue {
    transition: none;
  }
}

/* ------------------------------------------------------------- two columns
   Below --bp-lg the page is one column: the lines, then the totals under them,
   which is the only honest order on a phone.

   From --bp-lg it becomes the editorial two-column cart. This is not
   decoration. At the 1440 container the single column ran the cart lines to
   1344px, so a 120px thumbnail sat beside a product title with roughly 1000px
   of empty rule between it and its own price — the eye has to travel the whole
   width to pair a name with a number. The second column both shortens that
   journey and puts the subtotal where it can stay in view.

   24rem, not a share of the row: the summary holds a fixed set of short lines
   and a button, and giving it a fraction would stretch the same content wider
   on a wider screen for no reason. */

@media (min-width: 1024px) {
  .main-cart__form {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 24rem;
    gap: var(--space-8);
    align-items: start;
  }

  .main-cart__lines {
    /* The rule under the last line closed the single column. In two columns
       the summary is beside the list, not under it, so the line has nothing
       left to separate. */
    border-block-end: none;
  }

  .main-cart__summary {
    /* Both of these are the single-column layout's: a cap that pulled the
       block to the trailing edge of a full-width row. The grid track is the
       width now. */
    max-width: none;
    margin-block-start: 0;
    margin-inline-start: 0;
    position: sticky;
    /* Clear of the sticky header, the same offset the product page's buying
       column uses. */
    top: var(--header-offset-desktop);
    /* If the summary is ever taller than the screen — a long order note, a
       stack of discounts — sticking it would hide its own bottom, Checkout
       included. Its own scroll keeps every control reachable, and the
       scroll-padding keeps a focused control clear of the bottom edge
       (WCAG 2.2 SC 2.4.11). */
    max-height: calc(100dvh - var(--header-offset-desktop) - var(--space-6));
    overflow-y: auto;
    scroll-padding-block: var(--space-6);
  }
}

/* ------------------------------------------------------------------ empty */""",
    'continue shopping and the two-column layout')


# ============================================ 3. the note, shared component
line = F('assets/component-cart-line.css')
line.append("""
/* ============================================================================
   THE CART NOTE
   Phase 14. Shopify's own cart note, rendered by snippets/cart-note.liquid on
   both cart surfaces — which is why it is here, beside the totals and the
   empty state, rather than in either surface's own stylesheet.

   It is a native <details>. The summary is the label; the field is the body.
   ========================================================================== */

.cart-note {
  margin-block-end: var(--space-5);
  border-block: var(--border-width) solid var(--color-border-current-subtle);
}

.cart-note__summary {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  /* The Phase 9 floor. A disclosure the customer has to hit on a phone is a
     primary control on this surface. */
  min-height: var(--target-min);
  padding-block: var(--space-3);
  cursor: pointer;
  color: var(--color-text-current-muted);
  font-family: var(--font-body);
  font-size: var(--type-label-size);
  font-weight: var(--type-label-weight);
  letter-spacing: var(--type-label-ls);
  text-transform: uppercase;
  list-style: none;
}

/* Safari paints its own disclosure triangle without this. */
.cart-note__summary::-webkit-details-marker {
  display: none;
}

.cart-note__summary:focus-visible {
  outline: var(--focus-width) solid var(--focus-ring);
  outline-offset: var(--focus-offset);
}

.cart-note__summary-label {
  flex: 1 1 auto;
}

.cart-note__summary .icon {
  flex: 0 0 auto;
  width: var(--icon-sm);
  height: var(--icon-sm);
  transition: transform var(--transition-fast);
}

.cart-note[open] .cart-note__summary .icon {
  transform: rotate(180deg);
}

.cart-note__body {
  padding-block-end: var(--space-4);
}

.cart-note__field {
  display: block;
  width: 100%;
  padding: var(--space-3);
  border: var(--border-width) solid var(--color-border-current-interactive);
  border-radius: var(--radius-sm);
  background-color: transparent;
  color: inherit;
  font-family: var(--font-body);
  /* 16px. Below it iOS zooms the viewport the moment the field takes focus,
     and a zoomed cart is a cart the customer has to pan to read. */
  font-size: var(--type-body-size);
  line-height: var(--type-body-lh);
  /* Vertical only: a horizontally resizable field inside a 420px drawer can be
     dragged straight out of its own panel. */
  resize: vertical;
}

.cart-note__field:focus-visible {
  outline: var(--focus-width) solid var(--focus-ring);
  outline-offset: var(--focus-offset);
}

.cart-note__help {
  margin: var(--space-2) 0 0;
  color: var(--color-text-current-muted);
  font-family: var(--font-body);
  font-size: var(--type-caption-size);
  line-height: var(--type-caption-lh);
}

@media (prefers-reduced-motion: reduce) {
  .cart-note__summary .icon {
    transition: none;
  }
}
""", 'the cart note')


# ====================================== 4. the quick-add card's failure line
card = F('assets/component-product-card.css')
card.append("""
/* ----------------------------------------------------------- quick add error
   Phase 14. The quick-add form's own failure line. It had markup and no rules
   at all, so even once assets/cart.js could find it — it could not, until
   Phase 14 corrected the attribute it carried — the message would have
   rendered as unstyled body text under the button.

   Left-ruled rather than boxed, which is the form-error treatment
   section-main-product.css established for the product page. */

.product-card__error {
  margin: var(--space-2) 0 0;
  padding-inline-start: var(--space-3);
  border-inline-start: var(--border-width-strong) solid var(--color-error);
  color: inherit;
  font-family: var(--font-body);
  font-size: var(--type-caption-size);
  line-height: var(--type-caption-lh);
}

.surface-dark .product-card__error {
  border-inline-start-color: var(--color-error-on-dark);
}
""", 'the quick-add failure line')


# ================================= 5. the product page's add confirmation
prod = F('assets/section-main-product.css')
prod.sub(
    """/* ------------------------------------------------------------ description */""",
    """/* -------------------------------------------------------- add confirmation
   Phase 14. Shown only when no cart drawer opened to do the confirming — the
   merchant set the cart style to "Cart page", or switched auto-open off. Until
   this existed, the sole sighted response to a successful add was the header
   count changing in the corner of the screen.

   It mirrors the error line's construction — same placement, same rule, same
   type — because they are the same kind of thing said in two directions, and a
   customer should not have to learn two shapes. The colour is the difference,
   and it is the one carrying no meaning on its own: the sentence says
   "Added to your cart" in words (SC 1.4.1). */

.main-product__success {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: var(--space-2) var(--space-4);
  margin-block-start: var(--space-4);
  padding: var(--space-3) var(--space-4);
  border-inline-start: var(--border-width-strong) solid var(--color-success);
  font-family: var(--font-body);
  font-size: var(--type-body-sm-size);
  line-height: var(--type-body-sm-lh);
}

.surface-dark .main-product__success {
  border-inline-start-color: var(--color-success-on-dark);
}

.main-product__success-link {
  /* The one control in the line, so it is underlined rather than left to
     colour to say it is a link (SC 1.4.1 again). */
  min-height: var(--target-min);
  display: inline-flex;
  align-items: center;
  color: inherit;
  text-decoration: underline;
  text-underline-offset: 0.25em;
}

/* ------------------------------------------------------------ description */""",
    'the add confirmation')

for f in (drawer, page, line, card, prod):
    f.save()
