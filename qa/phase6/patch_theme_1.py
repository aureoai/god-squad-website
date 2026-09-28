# -*- coding: utf-8 -*-
"""Two corrections found by rendering the real Liquid."""
card = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\snippets\product-card.liquid"
sect = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\sections\featured-collection.liquid"

# --- 1. product-card: drop fetchpriority="auto", and pick the swatch option
#        in the logic block instead of breaking out of a render loop.
s = open(card, encoding='utf-8').read()

old = """  assign loading_attr = 'lazy'
  assign fetch_attr = 'auto'
  if eager
    assign loading_attr = 'eager'
  endif
-%}"""
new = """  assign loading_attr = 'lazy'
  if eager
    assign loading_attr = 'eager'
  endif

  comment
    Colourways, if the product has any. The option is chosen here rather than
    inside the markup so the markup stays a straight render with no control
    flow to reason about. Only an option whose values carry native Shopify
    swatches qualifies, which is what keeps every colour real store data.
  endcomment
  assign swatch_option = nil
  if show_swatches
    for option in product.options_with_values
      assign swatch_count = 0
      for value in option.values
        if value.swatch.color or value.swatch.image
          assign swatch_count = swatch_count | plus: 1
        endif
      endfor
      if swatch_count > 1
        assign swatch_option = option
        break
      endif
    endfor
  endif
-%}"""
assert old in s, 'loading block not found'
s = s.replace(old, new, 1)

s = s.replace("""            loading: loading_attr,
            fetchpriority: fetch_attr,
            decoding: 'async',""",
"""            loading: loading_attr,
            decoding: 'async',""", 1)

old_sw = s[s.index("  {%- if show_swatches -%}"):s.index("  {%- if quick_add -%}")]
new_sw = """  {%- if swatch_option != nil -%}
    {%- comment -%}
      Information, not controls (Phase 2 section 27.4: "The card shows swatches
      as information, not as a control"). Because they are not controls, their
      size is not governed by SC 2.5.8, and because the colour is never the
      name, the colourway names sit beside the dots as visually hidden text.
      Phase 1 DATA-03 recorded the prototype's three identical hard-coded hexes
      as the thing this replaces.
    {%- endcomment -%}
    <div class="product-card__swatches">
      <span class="visually-hidden">
        {{- swatch_option.name }}:
        {%- for value in swatch_option.values -%}
          {%- if value.swatch.color or value.swatch.image %} {{ value.name }}{% unless forloop.last %},{% endunless %}{% endif -%}
        {%- endfor -%}
      </span>
      {%- for value in swatch_option.values -%}
        {%- if value.swatch.color -%}
          <span class="product-card__swatch" style="--swatch-fill: {{ value.swatch.color }};" aria-hidden="true"></span>
        {%- elsif value.swatch.image -%}
          <span class="product-card__swatch product-card__swatch--image" style="--swatch-image: url({{ value.swatch.image | image_url: width: 40 }});" aria-hidden="true"></span>
        {%- endif -%}
      {%- endfor -%}
    </div>
  {%- endif -%}

"""
s = s.replace(old_sw, new_sw, 1)
open(card, 'w', encoding='utf-8', newline='').write(s)
print('product-card.liquid: swatch selection hoisted, fetchpriority dropped')

# --- 2. featured-collection: an unconfigured section must not request CSS.
t = open(sect, encoding='utf-8').read()
old_css = """{{ 'component-product-card.css' | asset_url | stylesheet_tag }}
{{ 'section-featured-collection.css' | asset_url | stylesheet_tag }}

{%- liquid"""
new_css = """{%- liquid"""
assert old_css in t, 'stylesheet header not found'
t = t.replace(old_css, new_css, 1)

old_guard = """{%- if collection == blank and request.design_mode == false -%}
  {%- comment -%} Not configured yet: render nothing. {%- endcomment -%}
{%- else -%}
"""
new_guard = """{%- if collection == blank and request.design_mode == false -%}
  {%- comment -%}
    Not configured yet: render nothing, and request nothing. The stylesheets
    are emitted inside this branch rather than at the top of the file so an
    unconfigured section costs no requests either.
  {%- endcomment -%}
{%- else -%}

{{ 'component-product-card.css' | asset_url | stylesheet_tag }}
{{ 'section-featured-collection.css' | asset_url | stylesheet_tag }}
"""
assert old_guard in t, 'guard not found'
t = t.replace(old_guard, new_guard, 1)
open(sect, 'w', encoding='utf-8', newline='').write(t)
print('featured-collection.liquid: stylesheets moved inside the render guard')
