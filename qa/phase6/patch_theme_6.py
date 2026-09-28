# -*- coding: utf-8 -*-
"""Sold-out reading order.

Measured: the card link's accessible name came out "Sold out Utility Cap",
because the badge sits inside the media div (it has to, to be positioned over
the photograph) and the media precedes the title. The name is understandable
either way, but "Utility Cap, sold out" is the order a person would say it in.

The visible badge becomes decorative and the same words are carried after the
title, inside the same anchor, so the state is still part of the accessible
name exactly as Phase 2 section 13.4 requires.
"""
p = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\snippets\product-card.liquid"
s = open(p, encoding='utf-8').read()

old = """      {%- unless product.available -%}
        {%- comment -%}
          Phase 2 section 27.3: availability is a badge only when no add-to-cart
          control is visible, which is the case in a grid. Text, never colour
          alone, and outlined so it never depends on the photograph behind it.
        {%- endcomment -%}
        <span class="product-card__badge">{{ 'products.card.sold_out' | t }}</span>
      {%- endunless -%}
    </div>

    <h{{ heading_level }} class="product-card__title">{{ product.title }}</h{{ heading_level }}>
  </a>"""

new = """      {%- unless product.available -%}
        {%- comment -%}
          Phase 2 section 27.3: availability is a badge only when no add-to-cart
          control is visible, which is the case in a grid. Text, never colour
          alone.

          The badge has to live inside the media box to sit over the
          photograph, and the media comes before the title, so a screen reader
          reading this link in order would say "Sold out, Utility Cap". The
          visible badge is therefore marked decorative and the same words are
          repeated after the title, which puts the state where a person would
          say it. It is still inside the one anchor, so the sold-out fact is
          still part of the link's accessible name, which section 13.4
          requires.
        {%- endcomment -%}
        <span class="product-card__badge" aria-hidden="true">{{ 'products.card.sold_out' | t }}</span>
      {%- endunless -%}
    </div>

    <h{{ heading_level }} class="product-card__title">{{ product.title }}</h{{ heading_level }}>
    {%- unless product.available -%}
      <span class="visually-hidden">{{ 'products.card.sold_out' | t }}</span>
    {%- endunless -%}
  </a>"""

assert old in s, 'badge block not found'
open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new, 1))
print('product-card.liquid: sold-out state now reads after the product name')
