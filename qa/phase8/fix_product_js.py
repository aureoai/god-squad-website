# -*- coding: utf-8 -*-
"""The product script's share of the Phase 8 review findings, plus one class
name the drawer's empty state no longer carries."""
P = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\product.js"
s = open(P, encoding='utf-8').read()
done = []


def sub(old, new, label):
    global s
    assert old in s, 'NOT FOUND: ' + label
    assert s.count(old) == 1, 'AMBIGUOUS: ' + label
    s = s.replace(old, new, 1)
    done.append(label)


# ----------------------------------------------------- the blanked price
sub("""      updateLegends();
      refreshAvailability(values);
      updatePrice(variant || { price: '', compare_at_price: null });
      updateButton(variant);
      updateSku(variant);
      updateUrl(variant);
      updateMedia(variant);

      /* A combination with no variant at all — possible on a product whose
         option grid is not fully populated. The button is already disabled by
         updateButton; the price is left as it was rather than blanked, because
         an empty price where a number used to be reads as a broken page. */
      if (!variant && addButton) addButton.disabled = true;""",
    """      updateLegends();
      refreshAvailability(values);
      updateButton(variant);
      updateSku(variant);
      updateUrl(variant);
      updateMedia(variant);

      /* A combination with no variant at all — routine on a product whose
         option grid is not fully populated, a colour that exists only in some
         sizes. The button is already disabled by updateButton, and the price
         is LEFT AS IT WAS rather than blanked: an empty price where a number
         used to be reads as a broken page. The previous version passed a
         synthetic empty string here and did exactly what this comment said it
         did not. */
      if (variant) {
        updatePrice(variant);
        updateQuantityRule(variant);
      } else if (addButton) {
        addButton.disabled = true;
      }""",
    'the price is not blanked when no variant matches')

# ------------------------------------------- the quantity rule per variant
sub("""    function updateSku(variant) {""",
    """    /* Shopify carries the minimum, maximum and increment per VARIANT, and the
       section renders them from whichever variant the page opened on. Without
       this the customer could choose a variant with its own rule and keep the
       previous one's floor — and then be refused at /cart/add with no idea
       why. Absent rules clear the attributes rather than leaving stale ones. */
    function updateQuantityRule(variant) {
      var input = root.querySelector('[data-quantity-input]');
      if (!input) return;
      var control = input.closest('[data-quantity]');
      var rule = (variant && variant.quantity_rule) || null;
      var min = rule && rule.min ? rule.min : 1;
      var step = rule && rule.increment ? rule.increment : 1;

      input.setAttribute('min', min);
      input.setAttribute('step', step);
      if (rule && rule.max) {
        input.setAttribute('max', rule.max);
      } else {
        input.removeAttribute('max');
      }

      var value = parseInt(input.value, 10);
      if (isNaN(value) || value < min) value = min;
      if (rule && rule.max && value > rule.max) value = rule.max;
      input.value = value;

      /* The steppers' disabled state is derived from the same numbers, and the
         cart script owns that function — so tell it rather than reimplement
         it here. A change event is what it already listens for. */
      if (control) input.dispatchEvent(new Event('change', { bubbles: true }));
    }

    function updateSku(variant) {""",
    'the quantity rule follows the variant')

# ------------------------------------------------- the gallery on load
sub("""    /* Keep the rail in step with a swipe or a scroll. IntersectionObserver""",
    """    /* The server already marked the slide this page should open on — a URL
       carrying ?variant= for a variant whose featured_media is not the first
       medium. Below the split the gallery is a scroll-snap carousel whatever
       the merchant's layout setting says, so without this the viewport stays
       on slide one and the customer sees the wrong photograph. */
    var active = gallery.querySelector('.product-gallery__slide.is-active');
    var first = gallery.querySelector('.product-gallery__slide');
    if (active && first && active !== first) showSlide(gallery, active, false);

    /* Keep the rail in step with a swipe or a scroll. IntersectionObserver""",
    'the gallery opens on the slide the server chose')

# --------------------------------- showSlide branches on what is rendered
sub("""    if (gallery.getAttribute('data-gallery-layout') === 'carousel') {
      /* Scroll the scroller, not the page: scrollIntoView on a horizontally
         scrolled slide also scrolls the document vertically, which jumps the
         page under the customer's thumb. */
      viewport.scrollTo({ left: slide.offsetLeft - viewport.offsetLeft, behavior: behavior });
    } else if (smooth) {
      slide.scrollIntoView({ behavior: behavior, block: 'nearest' });
    }""",
    """    /* Branch on what is RENDERED, not on the merchant's setting. The stacked
       overrides live inside a min-width query, so below the split the gallery
       is a horizontal scroller even when the setting says stacked — which is
       the shipped default, and therefore every phone. Asking the element
       whether it scrolls horizontally is the question that actually matters. */
    if (viewport.scrollWidth > viewport.clientWidth + 1) {
      /* Scroll the scroller, not the page: scrollIntoView on a horizontally
         scrolled slide also scrolls the document vertically, which jumps the
         page under the customer's thumb. */
      viewport.scrollTo({ left: slide.offsetLeft - viewport.offsetLeft, behavior: behavior });
    } else if (smooth) {
      slide.scrollIntoView({ behavior: behavior, block: 'nearest' });
    }""",
    'the scroll strategy follows the rendered layout')

open(P, 'w', encoding='utf-8', newline='').write(s)

# The drawer's empty state is now the shared component's class.
C = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\section-cart-drawer.css"
c = open(C, encoding='utf-8').read()
old = """.cart-drawer__empty {
  padding-inline: var(--space-5);
}"""
new = """.cart-drawer__inner .cart-empty {
  padding-inline: var(--space-5);
}"""
assert old in c, 'drawer empty rule not found'
open(C, 'w', encoding='utf-8', newline='').write(c.replace(old, new, 1))
done.append('the drawer empty rule targets the shared class')

for i, label in enumerate(done, 1):
    print('%2d. %s' % (i, label))
