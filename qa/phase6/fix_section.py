# -*- coding: utf-8 -*-
p = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\sections\featured-collection.liquid"
s = open(p, encoding='utf-8').read()

def rep(a, b):
    global s
    assert a in s, "NOT FOUND: " + a[:90]
    s = s.replace(a, b, 1)

# The schema declares tag: section, so Shopify already wraps this in a
# <section id="shopify-section-...">. A second <section> inside it would nest
# two sectioning elements for one band.
rep("""<section
  class="{{ classes }}"
  {% if section.settings.anchor_id != blank %}id="{{ section.settings.anchor_id | handle }}"{% endif %}
  {{ section.shopify_attributes }}
>
  <div class="featured-collection__inner">""",
"""{%- comment -%}
  The column counts are merchant settings, so they arrive as scoped custom
  properties rather than as inline style on the grid: an inline declaration
  would outrank every media query and pin the mobile count to all three tiers.
  The section id scopes them, which is what lets two instances of this section
  on one page carry different counts.
{%- endcomment -%}
{% style %}
  #shopify-section-{{ section.id }} .product-grid { --product-cols: {{ cols_m }}; }
  @media (min-width: 768px) {
    #shopify-section-{{ section.id }} .product-grid { --product-cols: {{ cols_t }}; }
  }
  @media (min-width: 1024px) {
    #shopify-section-{{ section.id }} .product-grid { --product-cols: {{ cols_d }}; }
  }
{% endstyle %}

<div
  class="{{ classes }}"
  {% if section.settings.anchor_id != blank %}id="{{ section.settings.anchor_id | handle }}"{% endif %}
>
  <div class="featured-collection__inner">""")

rep("""        <ul
          class="product-grid"
          role="list"
          style="--product-cols: {{ cols_m }};"
        >""",
"""        <ul class="product-grid" role="list">""")

rep("""  {%- comment -%}
    The column counts are merchant settings, so they arrive as inline custom
    properties on the grid for the mobile tier and here for the two wider
    tiers. A section id scopes them, which is what lets two instances of this
    section on one page carry different counts.
  {%- endcomment -%}
  {% style %}
    @media (min-width: 768px) {
      #shopify-section-{{ section.id }} .product-grid { --product-cols: {{ cols_t }}; }
    }
    @media (min-width: 1024px) {
      #shopify-section-{{ section.id }} .product-grid { --product-cols: {{ cols_d }}; }
    }
  {% endstyle %}
</section>""",
"""</div>""")

open(p, 'w', encoding='utf-8', newline='').write(s)
print("featured-collection.liquid: wrapper and scoped style corrected")
