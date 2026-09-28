# -*- coding: utf-8 -*-
"""Phase 15 — delete the sizing CSS that measurement proved was dead."""
import io
import os
import re

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
p = os.path.join(THEME, 'assets', 'header.css')
s = io.open(p, encoding='utf-8').read()
n0 = len(s)

start = s.index('/* ===========================================================================\n   THE ACCOUNT CONTROL')
end = s.index('.header__cart-count {')
old = s[start:end]

new = """/* ===========================================================================
   THE ACCOUNT CONTROL
   Phase 15. <shopify-account> is Shopify's own element, not this theme's, and
   the theme styles it through exactly three published hooks: the
   --shopify-account-* custom properties, ::part(signed-out-avatar), and the
   signed-out-avatar slot. Nothing below reaches inside it with a descendant
   selector. Shopify states it may change the element independently of the
   theme, so a selector aimed at its internals is a rule with an expiry date.

   THERE IS NO SIZE RESERVATION HERE, AND THAT IS A MEASURED RESULT.

   A custom element has no dimensions until its defining script runs, so the
   usual guard is a :not(:defined) rule reserving the box — Dawn ships one, and
   Phase 15 shipped one too. Measured at seven viewports with the reservation
   removed, then with ALL of this file's account sizing removed, the element
   still occupied exactly 44x44 and the end cluster still measured 148px. Both
   rules were dead the day they were written.

   The reason is that the element carries `class="header__control"`, the class
   every header control already uses, and that class sets min-width and
   min-height to --target-min inside a flex cluster. So the box is reserved
   before the component exists, by a rule that predates Phase 15 entirely.

   This is better than a :not(:defined) reservation, not merely equal to it. A
   :not(:defined) rule stops applying the moment the component upgrades, which
   leaves the upgraded element free to be any size it likes. An author rule on
   the element wins over the component's own :host styles, so the 44px target
   floor holds permanently rather than only until the script lands.

   The harness cannot see any of this from the other side: it never loads
   Shopify's script, so the element is permanently un-upgraded there. Every
   harness reading is of the reservation, never of the component. */

shopify-account.header__control {
  /* ---------------------------------------------------------------------
     The six primaries whose meaning is unambiguous from their names. The
     account sheet is a layer over the page, so it is dressed as the theme's
     other layer is: the cart drawer, which is ink.

     That choice is what makes the accent safe. Phase 2 section 10.1 allows gold
     on dark surfaces only and gives --color-accent-strong for cream; on ink,
     --color-accent measures 11.01:1 and the cream text on it 17.04:1. Had the
     sheet been cream, every one of these would have to be the other token. */
  --shopify-account-color-background: var(--color-bg-primary);
  --shopify-account-color-text: var(--color-text-primary);
  --shopify-account-color-accent: var(--color-accent);
  --shopify-account-font-heading: var(--font-display);
  --shopify-account-font-body: var(--font-body);
  --shopify-account-radius-base: var(--radius-sm);

  /* Derived properties, set only where the theme knows something the
     derivation cannot: God Squad headings are uppercase Playfair at 900, which
     no amount of deriving from a font family will produce. */
  --shopify-account-font-heading-weight: var(--weight-black);
  --shopify-account-font-heading-transform: uppercase;
  --shopify-account-font-body-weight: var(--weight-regular);
  --shopify-account-radius-button: var(--radius-sm);
  --shopify-account-radius-input: var(--radius-sm);

  /* The signed-in avatar is a filled disc carrying the customer's initials.
     Gold disc, ink initials - the same 11.01:1 pairing, inverted. */
  --shopify-account-signed-in-avatar-color-background: var(--color-accent);
  --shopify-account-signed-in-avatar-color-text: var(--color-bg-primary);

  /* --shopify-account-dialog-position-top is deliberately NOT set. Its
     semantics - an absolute top, an offset from the trigger, or a gap - could
     not be settled from the documentation, and this theme has a sticky header
     that a wrong guess would put the sheet underneath. Shopify's default is
     left in place; it is the first thing to check on a live store. */
}

/* The slotted content: the Phase 3 account mark, at the same size the search
   and cart icons use, so the three read as one set. This one IS needed - the
   class is new in Phase 15 and nothing else sizes it. */
.header__account-avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: var(--icon-md);
  height: var(--icon-md);
  color: inherit;
}

.header__account-avatar .icon {
  width: 100%;
  height: 100%;
}

"""

s = s[:start] + new + s[end:]
io.open(p, 'w', encoding='utf-8').write(s)
print('assets/header.css  %d -> %d bytes' % (n0, len(s)))
print('removed: the :not(:defined) block, the duplicated box declarations, the duplicated :hover')
