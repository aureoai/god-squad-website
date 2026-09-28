# -*- coding: utf-8 -*-
"""Phase 14 — the Liquid changes."""
import io
import json
import os
from collections import OrderedDict

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
        print('  ok  %-28s %s' % (self.rel, label))

    def save(self):
        io.open(self.path, 'w', encoding='utf-8').write(self.s)


# ===================================================== 1. the product card
# The card emitted data-cart-error, which is the CART surfaces' attribute.
# assets/cart.js reads a form's own failures out of [data-product-error], so a
# failed quick add was announced to a screen reader and shown to nobody — the
# exact defect the comment beside it claims to have fixed.
card = F('snippets/product-card.liquid')
card.sub(
    """          The three hooks assets/cart.js needs. Without them the form still
          posted — cart.js finds the button through its [type="submit"] fallback
          — but it had no [data-add-to-cart-label] to write "Adding…" into and no
          [data-cart-error] to put a failure in. A failed quick add reached the
          layout's live region, so a screen-reader user heard it, and a sighted
          customer saw the card sit there unchanged. Phase 8 owns the cart; these
          are its contract, not this card's invention.""",
    """          The three hooks assets/cart.js needs. Without them the form still
          posted — cart.js finds the button through its [type="submit"] fallback
          — but it had no [data-add-to-cart-label] to write "Adding…" into and no
          error box to put a failure in. A failed quick add reached the layout's
          live region, so a screen-reader user heard it, and a sighted customer
          saw the card sit there unchanged. Phase 8 owns the cart; these are its
          contract, not this card's invention.

          Phase 14 corrected the third hook's NAME. It was data-cart-error,
          which is the attribute the drawer and the cart page use for their own
          failure lines — a different contract, read by a different function.
          The consequence ran both ways: a failed quick add still showed the
          customer nothing, because showFormError looks inside the form for
          [data-product-error]; and showCartError, which selected every
          [data-cart-error] in the document, printed a cart-line failure onto
          every product tile on the page. Both are fixed — the attribute here,
          and the selector there.""",
    'quick-add error box is renamed (comment)')

card.sub(
    """          <p class="product-card__error" data-cart-error hidden></p>""",
    """          <p class="product-card__error" data-product-error role="alert" hidden></p>""",
    'quick-add error box is renamed')


# ===================================================== 2. the cart drawer
drawer = F('sections/cart-drawer.liquid')
drawer.sub(
    """          <div class="cart-drawer__footer">
            {% render 'cart-totals' %}""",
    """          <div class="cart-drawer__footer">
            {%- comment -%}
              Phase 14. Shopify's own cart note, off unless the merchant turns
              it on. It is inside the form, so with scripting off it is saved
              by the Update control below or by Checkout; with scripting on
              assets/cart.js saves it through /cart/update.js when the field is
              left, because a quantity change re-renders this node from the
              server and the server does not know about text that has only been
              typed.
            {%- endcomment -%}
            {%- if section.settings.show_note -%}
              {% render 'cart-note', id: 'CartDrawerNote' %}
            {%- endif -%}

            {% render 'cart-totals' %}""",
    'cart note')

drawer.sub(
    """              {%- if section.settings.show_view_cart -%}
                <a class="button button--secondary button--full" href="{{ routes.cart_url }}">
                  {{ 'cart.view_cart' | t }}
                </a>
              {%- endif -%}
            </div>""",
    """              {%- if section.settings.show_view_cart -%}
                <a class="button button--secondary button--full" href="{{ routes.cart_url }}">
                  {{ 'cart.view_cart' | t }}
                </a>
              {%- endif -%}
            </div>

            {%- comment -%}
              Continue shopping. A BUTTON that closes the drawer, not a link
              somewhere — the customer is already on the page they were
              shopping, and the drawer is a layer over it, so returning them to
              it is the whole action. A link would navigate them away from the
              thing they were looking at in order to let them carry on looking
              at it.

              The close X above does the same job; this is the same action
              named in words, for a customer who does not read an X as "back to
              what I was doing". It reuses [data-cart-close], so it is the
              drawer's one close path rather than a second one.
            {%- endcomment -%}
            <button type="button" class="cart-drawer__continue" data-cart-close>
              {{ 'cart.continue_shopping' | t }}
            </button>""",
    'continue shopping')

drawer.sub(
    """    {
      "type": "checkbox",
      "id": "show_view_cart",
      "label": "Show the View cart link",
      "default": true
    },""",
    """    {
      "type": "checkbox",
      "id": "show_view_cart",
      "label": "Show the View cart link",
      "default": true
    },
    {
      "type": "checkbox",
      "id": "show_note",
      "label": "Let customers add an order note",
      "default": false,
      "info": "Adds Shopify's own cart note. Turn this on only if you act on what customers write there — a field nobody reads is worse than no field. The cart page has its own copy of this setting, under Cart."
    },""",
    'show_note setting')


# ===================================================== 3. the cart page
page = F('sections/main-cart.liquid')
page.sub(
    """          <div class="main-cart__summary">
            {% render 'cart-totals' %}""",
    """          <div class="main-cart__summary">
            {%- comment -%}
              Phase 14. The same note the drawer renders, from the same
              snippet, so a correction to one reaches the other.
            {%- endcomment -%}
            {%- if section.settings.show_note -%}
              {% render 'cart-note', id: 'CartPageNote' %}
            {%- endif -%}

            {% render 'cart-totals' %}""",
    'cart note')

page.sub(
    """            {%- if additional_checkout_buttons -%}
              <div class="main-cart__accelerated">
                {{ content_for_additional_checkout_buttons }}
              </div>
            {%- endif -%}
          </div>""",
    """            {%- if additional_checkout_buttons -%}
              <div class="main-cart__accelerated">
                {{ content_for_additional_checkout_buttons }}
              </div>
            {%- endif -%}

            {%- comment -%}
              Phase 14. Continue shopping, which this page had no route to at
              all: its only controls were Update and Checkout, so a customer
              who did not want to check out yet had nothing but the browser's
              Back button — which the brief rules out by name.

              A LINK, unlike the drawer's. The drawer is a layer over the page
              the customer was shopping and closing it returns them there;
              arriving on /cart is a navigation, and there is nothing to return
              to. It goes wherever the merchant sends an empty cart, because
              that is the same question asked twice, and it falls back to the
              home page for the reason snippets/cart-empty-state.liquid
              records.
            {%- endcomment -%}
            {%- assign shop_on_url = section.settings.empty_link | default: routes.root_url -%}
            <a class="main-cart__continue" href="{{ shop_on_url }}">
              {{ 'cart.continue_shopping' | t }}
            </a>
          </div>""",
    'continue shopping')

page.sub(
    """    {
      "type": "text",
      "id": "empty_link_label",
      "label": "Empty-cart button label",
      "default": "Shop the collection",
      "info": "The cart drawer has its own copy of this setting."
    }""",
    """    {
      "type": "text",
      "id": "empty_link_label",
      "label": "Empty-cart button label",
      "default": "Shop the collection",
      "info": "The cart drawer has its own copy of this setting."
    },
    {
      "type": "checkbox",
      "id": "show_note",
      "label": "Let customers add an order note",
      "default": false,
      "info": "Adds Shopify's own cart note. Turn this on only if you act on what customers write there — a field nobody reads is worse than no field. The cart drawer has its own copy of this setting."
    }""",
    'show_note setting')

# The empty-cart destination is now two things, so its label says so.
page.sub(
    """      "label": "Where the empty-cart button goes",
      "info": "Leave empty to use the home page. The cart drawer has its own copy of this setting."
    },""",
    """      "label": "Where the shopping buttons go",
      "info": "Used by both the empty-cart button and the Continue shopping link. Leave empty to use the home page. The cart drawer has its own copy of this setting."
    },""",
    'empty_link label covers both uses')


# ================================================== 4. the product form
prod = F('sections/main-product.liquid')
prod.sub(
    """        {%- comment -%}
          The form's own error region. Populated only from Shopify's response
          description, never from a raw exception, and empty until something
          fails. assertive because the customer has just pressed a button and
          is waiting on its result.
        {%- endcomment -%}
        <div
          class="main-product__error"
          data-product-error
          role="alert"
          hidden
        ></div>""",
    """        {%- comment -%}
          The form's own error region. Populated only from Shopify's response
          description, never from a raw exception, and empty until something
          fails. assertive because the customer has just pressed a button and
          is waiting on its result.
        {%- endcomment -%}
        <div
          class="main-product__error"
          data-product-error
          role="alert"
          hidden
        ></div>

        {%- comment -%}
          Phase 14. The confirmation, for the case where nothing else confirms.

          When the cart drawer opens after an add, the drawer IS the feedback —
          it shows the customer exactly what the cart now holds. But the drawer
          is optional twice over: a merchant can set the cart style to "Cart
          page", and can switch auto-open off. In both of those the only
          sighted response to pressing Add to cart was the header count
          changing by one, in the far corner of the screen, which is not a
          confirmation a customer can be expected to notice.

          role="status" rather than assertive: the customer got what they
          asked for, so this waits its turn instead of interrupting. That also
          makes it self-announcing, which is why assets/cart.js does NOT also
          write to the live region when this element is present — a success
          said twice is worse than a success said once.

          The View cart link is a plain link to a page that exists. It is the
          one thing a customer wants next if the addition was not what they
          meant, and it is not an interruption because nothing moved focus.

          It ships hidden, and no script is needed to keep it that way: with
          scripting off the form posts natively and Shopify redirects to the
          cart page, which is a stronger confirmation than any of this.
        {%- endcomment -%}
        <div
          class="main-product__success"
          data-product-success
          role="status"
          hidden
        >
          <span data-product-success-text></span>
          <a class="main-product__success-link" href="{{ routes.cart_url }}">
            {{ 'cart.view_cart' | t }}
          </a>
        </div>""",
    'add-to-cart confirmation')


# ================================================== 5. the locale strings
lp = os.path.join(THEME, 'locales', 'en.default.json')
loc = json.load(io.open(lp, encoding='utf-8'), object_pairs_hook=OrderedDict)
cart = loc['cart']
added = OrderedDict()
for k, v in cart.items():
    added[k] = v
    if k == 'view_cart':
        # Phase 14. The two new surfaces' own words.
        added['continue_shopping'] = 'Continue shopping'
added['note'] = OrderedDict([
    ('label', 'Order note'),
    ('help', 'Anything we should know about this order.'),
])
added.setdefault('status', cart['status'])
added['status']['note_saved'] = 'Order note saved.'
loc['cart'] = added
io.open(lp, 'w', encoding='utf-8').write(
    json.dumps(loc, indent=2, ensure_ascii=False) + '\n')
print('  ok  locales/en.default.json        cart.continue_shopping, cart.note.*, cart.status.note_saved')


# ================================================== 6. the strings the script says
layout = F('layout/theme.liquid')
layout.sub(
    """      data-removed="{{ 'cart.status.removed' | t | escape }}\"""",
    """      data-removed="{{ 'cart.status.removed' | t | escape }}"
      data-note-saved="{{ 'cart.status.note_saved' | t | escape }}\"""",
    'note-saved string')

for f in (card, drawer, page, prod, layout):
    f.save()
    print('      %-32s %d -> %d bytes' % (f.rel, f.n0, len(f.s)))
