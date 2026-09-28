# -*- coding: utf-8 -*-
"""The cart drawer on a phone.

Two findings, both measured.

1. LANDSCAPE. At 812x375 the drawer's fixed chrome is 375px tall — an 85px
   header plus a 290px footer — in a viewport that is 375px tall. The scroller
   that holds the cart lines is therefore ZERO pixels high, against a 1091px
   list. A customer who turns their phone sideways cannot see or change a
   single thing in their cart. At 932x430 it is 55px, which is a sliver.

2. THE VIEWPORT'S OWN EDGES. The drawer is position:fixed with inset:0, so on
   a phone with a dynamic toolbar it is laid out against the LARGE viewport
   and its footer — the one that holds Checkout — can sit under the browser
   chrome. And with no safe-area padding, on a notched phone it sits under the
   home indicator.
"""
p = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\section-cart-drawer.css"
s = open(p, encoding='utf-8').read()
done = []


def sub(old, new, label):
    global s
    assert old in s, 'NOT FOUND: ' + label
    assert s.count(old) == 1, 'AMBIGUOUS: ' + label
    s = s.replace(old, new, 1)
    done.append(label)


sub(""".cart-drawer {
  position: fixed;
  inset: 0;
  z-index: var(--z-drawer);
}""",
    """.cart-drawer {
  position: fixed;
  inset-inline: 0;
  inset-block-start: 0;
  /* The VISIBLE viewport, not the large one. A fixed element with inset:0 is
     laid out against the large viewport on a phone whose toolbar can retract,
     so the drawer's footer — the one holding Checkout — could sit behind the
     browser's own chrome. dvh tracks what the customer can actually see; the
     vh line above it is the fallback for a browser that does not know dvh,
     which is the behaviour this replaces rather than a regression. */
  height: 100vh;
  height: 100dvh;
  z-index: var(--z-drawer);
}""",
    'the drawer is the height of the visible viewport')

sub(""".cart-drawer__footer {
  padding: var(--space-5);
  border-block-start: var(--border-width) solid var(--color-border-current);
  background-color: var(--color-bg-primary);
}""",
    """.cart-drawer__footer {
  padding: var(--space-5);
  border-block-start: var(--border-width) solid var(--color-border-current);
  background-color: var(--color-bg-primary);
}

/* The footer is the last thing above the phone's home indicator, and Checkout
   is in it. max() keeps the designed padding wherever there is no inset. */
@supports (padding: max(0px)) {
  .cart-drawer__footer {
    padding-block-end: max(var(--space-5), env(safe-area-inset-bottom));
  }

  .cart-drawer__header {
    padding-block-start: max(var(--space-5), env(safe-area-inset-top));
  }
}""",
    'the drawer respects the safe area')

anchor = "@media (prefers-reduced-motion: reduce) {"
assert anchor in s
block = """/* ------------------------------------------------------------- landscape
   A phone turned sideways. Measured before this block, at 812x375: the header
   was 85px, the footer 290px, and the scroller that holds the cart lines was
   therefore 0px against a 1091px list. The cart was unreadable and unchangeable
   in landscape; only Checkout was reachable, which is the worst possible
   subset to leave working.

   Nothing is removed. The chrome is re-proportioned — the header loses its
   generous padding, the totals tighten, and the two actions sit side by side
   instead of stacked, which is the one layout change landscape actually
   invites, because width is the dimension it has to spare.

   Bounded to max-width 1023px as well, so a short desktop window is untouched. */

@media (max-height: 540px) and (max-width: 1023px) {
  .cart-drawer__header {
    padding-block: var(--space-3);
  }

  .cart-drawer__footer {
    padding-block: var(--space-4);
  }

  .cart-totals {
    margin-block-end: var(--space-3);
  }

  .cart-totals__note {
    margin-block-end: var(--space-3);
  }

  /* Both actions stay. Side by side they cost one button's height instead of
     two, and the drawer is 420px wide even in landscape, so each still clears
     the target minimum comfortably. */
  .cart-drawer__actions {
    grid-template-columns: 1fr 1fr;
    gap: var(--space-3);
  }

  /* A tighter line, so more than one is visible in what is left. Every control
     inside it keeps its 44px target — that is not what is being compressed. */
  .cart-drawer__scroller .cart-line {
    padding-block: var(--space-3);
  }

  .cart-drawer__scroller .cart-line__controls {
    margin-block-start: var(--space-3);
  }
}

"""
s = s.replace(anchor, block + anchor, 1)
done.append('the drawer is usable in landscape')

open(p, 'w', encoding='utf-8', newline='').write(s)
for i, label in enumerate(done, 1):
    print('%d. %s' % (i, label))
