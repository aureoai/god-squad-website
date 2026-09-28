# -*- coding: utf-8 -*-
"""Phase 12 — the product card's secondary image.

The Phase 12 brief asks the card to support "secondary image where available",
on hover, desktop only, with no hover dependency on mobile, no layout shift, and
"no unnecessary JavaScript".

It is opt-in and OFF by default, for a reason that has to be stated plainly:
PHASE-2-DESIGN-SYSTEM.md section 22.4 specifies the approved card hover as a
1.03 image scale plus a title underline reveal, and nothing else. Turning an
image swap on by default would change the approved hover on every store, which
the brief's own CORE PRINCIPLE forbids. The brief says "allow" a secondary
image — so it is allowed, not imposed.

It is a GLOBAL setting rather than three per-section ones, on the same reasoning
Phase 10 used for the product image ratio: a card that swaps on one row of a shop
and not another is a bug, not a choice.
"""
import collections
import json
import os

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'god-squad-theme')
done = []


def patch(rel, old, new, label):
    p = os.path.join(THEME, rel)
    s = open(p, encoding='utf-8').read()
    assert s.count(old) == 1, 'NOT FOUND or ambiguous in %s: %s' % (rel, label)
    open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new, 1))
    done.append(label)


# ------------------------------------------------- 1. find the second image
patch('snippets/product-card.liquid',
      """  assign img = product.featured_image
""",
      """  assign img = product.featured_image

  comment
    The secondary image, for the hover swap. Global setting, off by default —
    Phase 2 section 22.4 specifies the approved hover as a 1.03 scale plus a
    title underline, so a swap is offered rather than imposed.

    The second image is the first one that is NOT the featured image, rather
    than images[1]: a merchant can promote any image to featured in admin
    without reordering the others, and images[1] would then be the SAME picture
    the card is already showing. Nothing renders when a product has only one.
  endcomment
  assign second_img = blank
  if settings.card_hover_secondary_image
    for candidate in product.images
      unless candidate == img
        assign second_img = candidate
        break
      endunless
    endfor
  endif
""",
      'product-card.liquid: the second image is the first that is not the featured one')

# ------------------------------------------------------- 2. render it
patch('snippets/product-card.liquid',
      """            alt: alt_text
        }}
      {%- else -%}""",
      """            alt: alt_text
        }}

        {%- if second_img != blank -%}
          {%- comment -%}
            Decorative: alt is empty because this is the same product the link
            already names, and a second alt would make the link announce the
            product twice. It is never the LCP candidate, so it is always lazy.
            It carries no width/height-driven layout of its own — the stylesheet
            lays both images over the one aspect-ratio box — so it cannot shift
            anything when it arrives.
          {%- endcomment -%}
          {{
            second_img
            | image_url: width: 1200
            | image_tag:
              class: 'product-card__image product-card__image--secondary',
              widths: '180, 240, 320, 400, 480, 600, 760, 900, 1100, 1200',
              sizes: card_sizes,
              loading: 'lazy',
              decoding: 'async',
              alt: ''
          }}
        {%- endif -%}
      {%- else -%}""",
      'product-card.liquid: the secondary image renders only when one exists')

# --------------------------------------------------------------- 3. the CSS
patch('assets/component-product-card.css',
      """@media (hover: hover) and (pointer: fine) {
  .product-card__link:hover .product-card__image {
    transform: scale(var(--hover-image-scale));
  }
}""",
      """@media (hover: hover) and (pointer: fine) {
  .product-card__link:hover .product-card__image {
    transform: scale(var(--hover-image-scale));
  }
}

/* --------------------------------------------------------- secondary image
   Laid over the primary inside the same aspect-ratio box, so the swap cannot
   move anything: both images occupy one slot whose height was already reserved
   by --product-aspect before either arrived.

   It is hidden by default and revealed ONLY inside the hover-capable query, so
   a touch device never depends on a hover it cannot perform — and, because the
   rule that reveals it lives inside that query, a phone has no state in which
   it can appear at all.

   The fade is a transition on opacity, so prefers-reduced-motion collapses it
   to 1ms through base.css's global rule rather than needing its own override:
   the swap still happens, it simply does not animate. */
.product-card__image--secondary {
  position: absolute;
  inset: 0;
  opacity: 0;
}

@media (hover: hover) and (pointer: fine) {
  .product-card__image--secondary {
    transition: opacity var(--transition-medium);
  }

  .product-card__link:hover .product-card__image--secondary,
  .product-card__link:focus-visible .product-card__image--secondary {
    opacity: 1;
  }
}""",
      'component-product-card.css: the swap, gated on a hover-capable pointer')

# ------------------------------------------------------- 4. the global setting
p = os.path.join(THEME, 'config', 'settings_schema.json')
schema = json.load(open(p, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
products = next(g for g in schema if g.get('name') == 'Products')
assert not any(s.get('id') == 'card_hover_secondary_image' for s in products['settings'])
products['settings'].append(collections.OrderedDict([
    ('type', 'checkbox'),
    ('id', 'card_hover_secondary_image'),
    ('label', 'Show a second photo on hover'),
    ('default', False),
    ('info',
     'On a mouse, hovering a product card fades to the next photo. Nothing '
     'changes on a phone or tablet, and a product with only one photo is '
     'unaffected. Off by default because the approved card hover is the image '
     'lift and the title underline.'),
]))
json.dump(schema, open(p, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
open(p, 'a', encoding='utf-8', newline='').write('\n')
done.append('settings_schema.json: one global control, in Products beside the image ratio')

p = os.path.join(THEME, 'config', 'settings_data.json')
data = json.load(open(p, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
for block in [data['current']] + [data['presets'][k] for k in data.get('presets', {})]:
    block.setdefault('card_hover_secondary_image', False)
json.dump(data, open(p, 'w', encoding='utf-8', newline=''), indent=2, ensure_ascii=False)
open(p, 'a', encoding='utf-8', newline='').write('\n')
done.append('settings_data.json: the default')

for i, label in enumerate(done, 1):
    print('%d. %s' % (i, label))
