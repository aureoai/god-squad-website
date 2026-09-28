# -*- coding: utf-8 -*-
"""Apply the confirmed review findings, plus the corrected floor measurement."""

CARD_CSS = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\component-product-card.css"
BTN_CSS = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\component-button.css"
CARD = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\snippets\product-card.liquid"
SECT = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\sections\featured-collection.liquid"


def patch(path, pairs):
    s = open(path, encoding='utf-8').read()
    for old, new in pairs:
        assert old in s, 'NOT FOUND in %s:\n%s' % (path.rsplit('\\', 1)[-1], old[:110])
        s = s.replace(old, new, 1)
    open(path, 'w', encoding='utf-8', newline='').write(s)
    print('patched', path.rsplit('\\', 1)[-1])


# --------------------------------------------------------- 1. floor comment
card_css = open(CARD_CSS, encoding='utf-8').read()
start = card_css.index("/* Below the tablet tier the floor is relaxed")
end = card_css.index("/* ------------------------------------------------------------------- card */")
floor_block = """/* Below the tablet tier the floor is relaxed, and only there. Phase 2 section
   13.9 permits two columns on a phone; the 272px catalogue floor would force
   one, because a 375px viewport has only 327px of content box.

   8rem (128px) is measured, not chosen. Two columns need 2F + 32px of gap to
   fit the grid's width, so the floor alone decides where the grid drops to one
   column. With the body reset in place (the first measurement of this was
   taken before it, and was 16px out at every width):

     layout  grid   columns at 8rem   columns at 8.5rem
       320    272         1                 1
       336    288         2                 1
       352    304         2                 2
       375    327         2                 2
       430    382         2                 2
       768    704    the 272px catalogue floor takes over again

   Both values behave identically from 352 up, because there the merchant's
   ceiling of two columns is the binding constraint and the tracks come out the
   same width either way. They differ only between 336 and 351, and 8rem is
   chosen so that a merchant who asks for two columns on mobile gets two on the
   narrowest phones as well. The narrowest resulting track is 128px, which was
   rendered and read before it was adopted: the tracked-caps title still wraps
   inside its two-line clamp and the price and swatch row still read.

   320px still gets one column, which is correct: two 128px tracks plus the gap
   do not fit 272px of grid.

   A merchant who chooses one column on mobile still gets one. The ceiling
   governs; the floor only stops the ceiling asking for something the viewport
   cannot carry. */
@media (max-width: 767px) {
  .product-grid {
    --product-track-floor: 8rem;
  }
}

"""
open(CARD_CSS, 'w', encoding='utf-8', newline='').write(
    card_css[:start] + floor_block + card_css[end:])
print('patched component-product-card.css (floor comment re-measured)')

# ------------------------------------------- 2. :has() fallback comment
patch(CARD_CSS, [(
    """/* Fallback for engines without :has(). :focus-within also fires for the
   optional quick-add control, which is acceptable: the ring is still correct,
   it is just drawn for one more element. Engines that support :has() apply
   the rule above as well; both draw the same ring, so there is no conflict. */""",
    """/* Fallback for engines without :has(). The two rules are mutually exclusive
   by construction: `not selector(:has(*))` is true only where :has() is
   unsupported, so an engine applies one or the other and never both. Where the
   fallback does run, :focus-within also fires for the optional quick-add
   control, which is acceptable — the ring is still correct, it is just drawn
   for one more element. An engine too old to understand @supports selector()
   treats the condition as false and gets neither rule, which is why the
   anchor's own outline is suppressed with :focus-visible rather than :focus:
   those engines fall back to the browser's default ring. */"""),
])

# --------------------------------------- 3. button: pointer-gate the hovers
btn = open(BTN_CSS, encoding='utf-8').read()
hover_pairs = [
    ("""".surface-light .button--primary:hover {
  /* #2A2823, the value the prototype's own runtime emitted for this button.
     12.83:1. */
  background-color: var(--color-surface-raised);
}\"""", None),
]
patch(BTN_CSS, [
    ("""".surface-light .button--primary:hover {""" if False else
     """.surface-light .button--primary:hover {
  /* #2A2823, the value the prototype's own runtime emitted for this button.
     12.83:1. */
  background-color: var(--color-surface-raised);
}""",
     """@media (hover: hover) and (pointer: fine) {
  .surface-light .button--primary:hover {
    /* #2A2823, the value the prototype's own runtime emitted for this button.
       12.83:1. */
    background-color: var(--color-surface-raised);
  }
}"""),
    ("""".surface-dark .button--primary:hover {""" if False else
     """.surface-dark .button--primary:hover {
  /* --gs-cream-200. 15.41:1 against ink. NOT gold: see note 1 above. */
  background-color: var(--color-text-secondary);
}""",
     """@media (hover: hover) and (pointer: fine) {
  .surface-dark .button--primary:hover {
    /* --gs-cream-200. 15.41:1 against ink. NOT gold: see note 1 above. */
    background-color: var(--color-text-secondary);
  }
}"""),
    ("""".surface-light .button--secondary:hover {""" if False else
     """.surface-light .button--secondary:hover {
  background-color: var(--color-border-inverse);
}

.surface-dark .button--secondary:hover {
  background-color: var(--color-border);
}

.button--secondary:active {
  background-color: transparent;
}""",
     """@media (hover: hover) and (pointer: fine) {
  .surface-light .button--secondary:hover {
    background-color: var(--color-border-inverse);
  }

  .surface-dark .button--secondary:hover {
    background-color: var(--color-border);
  }
}

/* Scoped to the surfaces to match the hover rules above. An unscoped
   .button--secondary:active is (0,2,0) and loses to a (0,3,0) surface-scoped
   hover, so a pointer press — which is necessarily also a hover — would keep
   the hover wash and the pressed state would never paint, while a keyboard
   activation would paint it. Primary and accent never had the problem because
   their hover and active rules are written at the same specificity. */
.surface-light .button--secondary:active,
.surface-dark .button--secondary:active {
  background-color: transparent;
}"""),
    ("""".surface-dark .button--accent:hover {""" if False else
     """.surface-dark .button--accent:hover {
  background-color: var(--color-accent-hover);
}""",
     """@media (hover: hover) and (pointer: fine) {
  .surface-dark .button--accent:hover {
    background-color: var(--color-accent-hover);
  }
}"""),
    # 4. full-width comment: restore the qualifier Phase 2 actually carries.
    ("""/* ---------------------------------------------------------------- full width
   Phase 2 section 10.4 permits this only where the button is the sole action
   in a stacked block. Never in the header, never in a product card row. */""",
     """/* ---------------------------------------------------------------- full width
   Phase 2 section 10.4, quoted in full: "Full-width buttons are permitted on
   mobile only where the button is the sole action in a stacked block; never in
   the header, never in a product card row."

   The product card's optional quick action uses this class at every width, not
   only on mobile. That is not a breach of the rule above but a separate
   sanction: section 27.5 specifies the quick action as "full card width". The
   card is not a "product card row" in the sense section 10.4 forbids — that
   phrase means a row of buttons inside a card — and the control is the card's
   sole action. Any OTHER full-width use is mobile-only. */"""),
    # Pointer-gate note in the header.
    ("""   No outline is declared anywhere in this file.""",
     """   Every hover rule sits inside @media (hover: hover) and (pointer: fine).
   Phase 2 section 22.1 makes that mandatory: without it a touch tap can leave
   a button stuck in its hover fill after navigation, with no pointer present
   to explain it.

   No outline is declared anywhere in this file."""),
])

# ------------------------------------- 5. card: swatch list, sold-out control
patch(CARD, [
    # Build the colourway name list from the values actually printed.
    ("""  assign swatch_option = nil
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
  endif""",
     """  assign swatch_option = nil
  assign swatch_names = ''
  if show_swatches
    for option in product.options_with_values
      assign swatch_count = 0
      assign names = ''
      for value in option.values
        if value.swatch.color or value.swatch.image
          assign swatch_count = swatch_count | plus: 1
          if names == blank
            assign names = value.name
          else
            assign names = names | append: ', ' | append: value.name
          endif
        endif
      endfor
      if swatch_count > 1
        assign swatch_option = option
        assign swatch_names = names
        break
      endif
    endfor
  endif"""),
    # The hidden list must separate the values it prints, not the values it
    # iterates: an option can carry values with no swatch configured.
    ("""      <span class="visually-hidden">
        {{- swatch_option.name }}:
        {%- for value in swatch_option.values -%}
          {%- if value.swatch.color or value.swatch.image %} {{ value.name }}{% unless forloop.last %},{% endunless %}{% endif -%}
        {%- endfor -%}
      </span>""",
     """      {%- comment -%}
        The names come from the list built above, which contains only the values
        that actually render a dot. Separating on forloop.last instead would put
        a trailing comma after the last name whenever the option's final value
        has no swatch configured — a mixed option Shopify allows.
      {%- endcomment -%}
      <span class="visually-hidden">{{ swatch_option.name }}: {{ swatch_names }}</span>"""),
    # A span is not a control. Phase 2 section 10.5.
    ("""      {%- else -%}
        <span class="button button--secondary button--full" aria-disabled="true">
          {{ 'products.card.sold_out' | t }}
        </span>
      {%- endif -%}""",
     """      {%- else -%}
        {%- comment -%}
          A real button, not a span wearing the button classes: Phase 2 section
          10.5 forbids the latter, and aria-disabled on an element with no role
          announces nothing. aria-disabled rather than the disabled attribute
          keeps it in the tab order, which section 10.3 asks for so the reason
          can be reached — the reason being the Sold out text the card already
          carries above.
        {%- endcomment -%}
        <button class="button button--secondary button--full" type="button" aria-disabled="true">
          {{ 'products.card.sold_out' | t }}
        </button>
      {%- endif -%}"""),
])

# ----------------------------- 6. section: empty guard and heading level
patch(SECT, [
    ("""{%- if collection == blank and request.design_mode == false -%}""",
     """{%- if has_products == false and request.design_mode == false -%}"""),
    ("""  Nothing is rendered on the live storefront until a collection is chosen. A
  heading floating above an empty band is worse than no band, and the Phase 6
  brief forbids standing anything in for products that do not exist. In the
  Theme Editor the section always renders, with a note saying what is missing,
  so the merchant can see and configure it.""",
     """  Nothing is rendered on the live storefront until there are products to show.
  The test is has_products, not "is a collection chosen": a merchant can point
  the section at a collection and later empty or unpublish it, and the result
  would otherwise be a full-height band of copy and a View all button over
  nothing — the very thing a heading floating above an empty band describes.

  In the Theme Editor the section always renders, with a note saying which of
  the two is missing, so the merchant can see and configure it."""),
    # The card heading level has to follow whether this section renders its h2.
    ("""  assign classes = 'featured-collection '""",
     """  comment
    The card titles sit one level below this section's heading — but the
    heading is a free-text setting a merchant can clear, and when it is blank
    no h2 renders. Hard-coding level 3 would then jump from the hero's h1
    straight to h3, which is the outline defect Phase 1 HTML-03 assigns to this
    phase. The level follows the heading instead.
  endcomment
  assign card_heading_level = 3
  if heading == blank
    assign card_heading_level = 2
  endif

  assign classes = 'featured-collection '"""),
    ("""                heading_level: 3,""",
     """                heading_level: card_heading_level,"""),
])
print('all confirmed findings applied')
