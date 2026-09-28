# -*- coding: utf-8 -*-
"""Phase 15 — the account control's stylesheet half."""
import io
import os

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
p = os.path.join(THEME, 'assets', 'header.css')
s = io.open(p, encoding='utf-8').read()
n0 = len(s)

anchor = """.header__cart-count {"""
assert s.count(anchor) == 1

block = """/* ===========================================================================
   THE ACCOUNT CONTROL
   Phase 15. <shopify-account> is Shopify's own element, not this theme's, and
   the theme styles it through exactly three published hooks: the
   --shopify-account-* custom properties, ::part(signed-out-avatar), and the
   signed-out-avatar slot. Nothing below reaches inside it with a descendant
   selector. Shopify states it may change the element independently of the
   theme, so a selector aimed at its internals is a rule with an expiry date.

   THE SIZE RESERVATION IS NOT COSMETIC.
   A custom element has no dimensions until its defining script runs. Between
   first paint and that upgrade <shopify-account> is an inline element of zero
   width, so the header's end cluster is short by one control and everything in
   it shifts sideways the moment Shopify's script lands — on every page, every
   load. :not(:defined) matches only during that window and reserves the same
   44px box every other header control occupies, so the upgrade changes what is
   inside the box and never the layout around it. Dawn ships the same guard.

   This is also the state the Mini-Liquid harness is permanently stuck in: it
   never loads Shopify's script, so the element is never defined there and the
   rule below is the only thing a harness render can show. A harness screenshot
   of this control is a screenshot of the reservation, not of the component. */

shopify-account.header__control {
  /* The same box as the search and cart controls beside it. */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: var(--target-min);
  min-height: var(--target-min);
  color: inherit;
  cursor: pointer;

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
     Gold disc, ink initials — the same 11.01:1 pairing, inverted. */
  --shopify-account-signed-in-avatar-color-background: var(--color-accent);
  --shopify-account-signed-in-avatar-color-text: var(--color-bg-primary);

  /* --shopify-account-dialog-position-top is deliberately NOT set. Its
     semantics — an absolute top, an offset from the trigger, or a gap — could
     not be settled from the documentation, and this theme has a sticky header
     that a wrong guess would put the sheet underneath. Shopify's default is
     left in place; it is the first thing to check on a live store. */
}

/* Only while the element is still undefined. Once Shopify's script upgrades
   it, the component owns its own box. */
shopify-account.header__control:not(:defined) {
  display: inline-flex;
  width: var(--target-min);
  height: var(--target-min);
}

/* The slotted content: the Phase 3 account mark, at the same size the search
   and cart icons use, so the three read as one set. */
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

shopify-account.header__control:hover {
  color: var(--accent-current);
}

"""

s = s.replace(anchor, block + anchor, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print('assets/header.css  %d -> %d bytes' % (n0, len(s)))
