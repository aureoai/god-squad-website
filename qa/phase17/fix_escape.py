# -*- coding: utf-8 -*-
"""Phase 17 — escape the two customer-controlled values the theme rendered raw.

SURFACED BY THE PRIVACY WORK, NOT BY THE TRACKING WORK. Phase 17 asks what
customer data the theme handles and where it could leak; the answer turned up
two values that a customer controls and the theme printed as markup.

Shopify Liquid does NOT auto-escape. Rendered with a payload:

  cart line property   <p class="cart-line__property">Engraving: </p>
                       <img src=x onerror=alert(1)>
  cart note            <textarea ...></textarea><img src=x onerror=alert(2)>

Both broke out and produced a live element with an event handler. The theme
already escapes search.terms — the same class of untrusted input — in 27 places,
so this is an inconsistency rather than a policy.
"""
import io
import os

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
def sub(rel, old, new, label):
    p = os.path.join(THEME, rel)
    s = io.open(p, encoding='utf-8').read()
    if old not in s:
        raise SystemExit('NOT FOUND in %s: %s' % (rel, label))
    if s.count(old) != 1:
        raise SystemExit('AMBIGUOUS (%d) in %s: %s' % (s.count(old), rel, label))
    io.open(p, 'w', encoding='utf-8').write(s.replace(old, new, 1))
    print('  ok  %-32s %s' % (rel, label))


sub('snippets/cart-line-item.liquid',
    """      Line properties a merchant or app has attached. Shopify's convention is
      that a property whose name begins with an underscore is private, so it is
      not shown, and an empty value means nothing was chosen.
    {%- endcomment -%}""",
    """      Line properties a merchant or app has attached. Shopify's convention is
      that a property whose name begins with an underscore is private, so it is
      not shown, and an empty value means nothing was chosen.

      PHASE 17: BOTH HALVES ARE ESCAPED, AND THAT IS NOT OPTIONAL.
      Shopify Liquid does not escape output. A line item property is supplied by
      whoever posted to /cart/add.js, which makes both its name and its value
      untrusted input rendered into markup. Without the filter, a property value
      of "</p><img src=x onerror=...>" closed this paragraph and produced a live
      element with an event handler — verified by rendering it.

      The theme already escapes search.terms for exactly this reason
      (sections/main-search.liquid); this was the inconsistency, not the policy.
    {%- endcomment -%}""",
    'record why the property must be escaped')

sub('snippets/cart-line-item.liquid',
    """          <p class="cart-line__property">{{ property.first }}: {{ property.last }}</p>""",
    """          <p class="cart-line__property">{{ property.first | escape }}: {{ property.last | escape }}</p>""",
    'escape both halves of the line property')

sub('snippets/cart-note.liquid',
    """    <textarea
      class="cart-note__field"
      id="{{ id }}"
      name="note"
      rows="3"
      data-cart-note
      {% if form_id != blank %}form="{{ form_id }}"{% endif %}
    >{{ cart.note }}</textarea>""",
    """    {%- comment -%}
      PHASE 17: cart.note IS ESCAPED.

      Liquid does not escape output, and a </textarea> inside the note closes
      this element early — verified by rendering a note of
      "</textarea><img src=x onerror=...>", which produced a live element after
      the field. The note is customer-supplied and is also settable through
      /cart/update.js, so it is untrusted input however it arrived.

      escape, not escape_once: the stored value is plain text, and escape_once
      would leave a literal "&amp;" typed by a customer looking like an entity.
    {%- endcomment -%}
    <textarea
      class="cart-note__field"
      id="{{ id }}"
      name="note"
      rows="3"
      data-cart-note
      {% if form_id != blank %}form="{{ form_id }}"{% endif %}
    >{{ cart.note | escape }}</textarea>""",
    'escape the cart note')
