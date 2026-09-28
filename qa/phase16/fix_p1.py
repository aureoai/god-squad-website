# -*- coding: utf-8 -*-
"""Phase 16 — the P1 findings that were verified by reading the code."""
import io
import json
import os
from collections import OrderedDict

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


# ================================================== the footer logo link
# <a href="/"> containing only <img alt=""> has NO accessible name. SC 2.4.4 and
# SC 4.1.2, Level A. The existing comment's reasoning — that the brand should not
# be announced twice, once as image text and once as the tagline beside it — is
# right and is preserved: the name goes in a visually-hidden span inside the
# anchor, so the LINK is named while the IMAGE stays decorative.
sub('sections/footer.liquid',
    """      that produces an empty gap is worse than no checkbox. The link goes home,
      matching the header's, and the alt text is empty because the adjacent
      tagline already names the brand — an image whose only job is decorative
      repetition should not be announced twice.
    {%- endcomment -%}""",
    """      that produces an empty gap is worse than no checkbox. The link goes home,
      matching the header's, and the alt text is empty because the adjacent
      tagline already names the brand — an image whose only job is decorative
      repetition should not be announced twice.

      PHASE 16: THE IMAGE IS DECORATIVE, THE LINK STILL HAS TO BE NAMED.
      alt="" on the only content of an anchor leaves the anchor with no
      accessible name at all — a screen reader announces "link" and nothing
      else, which is SC 2.4.4 and SC 4.1.2 at Level A. The tagline that names
      the brand is a sibling of this anchor, not inside it, so it never named
      the link. The hidden span below is the name; the image stays decorative,
      which is what the paragraph above is actually asking for.
    {%- endcomment -%}""",
    'footer logo: record why the link needs a name')

sub('sections/footer.liquid',
    """            widths: '112, 168, 224, 336, 400',
            sizes: '112px',
            loading: 'lazy'
        }}""",
    """            widths: '112, 168, 224, 336, 400',
            sizes: '112px',
            loading: 'lazy'
        }}
        <span class="visually-hidden">{{ shop.name }}</span>""",
    'footer logo: the link is named')


# ============================================ the product gallery's LCP frame
# eager + fetchpriority were spent on forloop.first. The slide the page OPENS on
# is is_active, which is the variant's featured media when it has one — so on
# any product whose selected variant is not the first medium, the browser was
# told to hurry the wrong image and to lazy-load the one actually on screen.
sub('snippets/product-media-gallery.liquid',
    """            {%- case media.media_type -%}
              {%- when 'image' -%}
                {%- if forloop.first -%}""",
    """            {%- case media.media_type -%}
              {%- when 'image' -%}
                {%- comment -%}
                  PHASE 16: is_active, NOT forloop.first.

                  The slide the page opens on is the active one — the variant's
                  featured media when it has one (see is_active above, which
                  falls back to forloop.first when it does not). Keying the
                  eager load and fetchpriority to forloop.first meant that on
                  any product whose selected variant is not the first medium,
                  the browser was told to hurry an image nobody was looking at
                  and to lazy-load the LCP element.

                  forloop.first still gets loading: eager, because the stacked
                  desktop layout renders every slide in document order and the
                  first one is on screen there regardless. Only ONE image gets
                  fetchpriority, and it is the active one.
                {%- endcomment -%}
                {%- if is_active -%}""",
    'gallery: eager and priority follow the active slide')

sub('snippets/product-media-gallery.liquid',
    """                {%- else -%}
                  {{
                    media
                    | image_url: width: 1800
                    | image_tag:
                      class: 'product-gallery__image',
                      widths: '360, 480, 640, 800, 960, 1200, 1400, 1600, 1800',
                      sizes: media_sizes,
                      loading: 'lazy',
                      decoding: 'async',
                      alt: media.alt
                  }}
                {%- endif -%}""",
    """                {%- elsif forloop.first -%}
                  {{
                    media
                    | image_url: width: 1800
                    | image_tag:
                      class: 'product-gallery__image',
                      widths: '360, 480, 640, 800, 960, 1200, 1400, 1600, 1800',
                      sizes: media_sizes,
                      loading: 'eager',
                      decoding: 'async',
                      alt: media.alt
                  }}
                {%- else -%}
                  {{
                    media
                    | image_url: width: 1800
                    | image_tag:
                      class: 'product-gallery__image',
                      widths: '360, 480, 640, 800, 960, 1200, 1400, 1600, 1800',
                      sizes: media_sizes,
                      loading: 'lazy',
                      decoding: 'async',
                      alt: media.alt
                  }}
                {%- endif -%}""",
    'gallery: the first stacked slide stays eager')


# ================================== aria-controls points at nothing on /cart
sub('sections/header.liquid',
    """          {% if settings.cart_type != 'page' %}aria-controls="CartDrawer"{% endif %}""",
    """          {%- comment -%}
            PHASE 16: the second arm. The drawer is absent for TWO reasons, and
            this only knew about one. layout/theme.liquid skips it when the
            merchant picks the cart page, and ALSO on the cart template itself,
            because there the page is the cart. Without the second condition
            this control pointed aria-controls at an element id that does not
            exist on /cart.
          {%- endcomment -%}
          {% if settings.cart_type != 'page' and template.name != 'cart' %}aria-controls="CartDrawer"{% endif %}""",
    'aria-controls is not emitted on the cart page')


# ============================ focus must not land on an aria-hidden element
# The last-resort fallback took the first FOCUSABLE match in the line, and the
# first one is .cart-line__media-link — tabindex="-1" aria-hidden="true". Focus
# on an element removed from the accessibility tree leaves a screen reader on
# something it cannot describe, which is the exact failure the drawer chose
# inert over aria-hidden to avoid.
sub('assets/cart.js',
    """          if (step) target = freshLine.querySelector('[data-quantity-step="' + step + '"]:not([aria-disabled="true"])');
          if (!target && isInput) target = freshLine.querySelector('[data-quantity-input]');
          if (!target && isRemove) target = freshLine.querySelector('[data-cart-remove]');
          if (!target) target = freshLine.querySelector(FOCUSABLE);""",
    """          if (step) target = freshLine.querySelector('[data-quantity-step="' + step + '"]:not([aria-disabled="true"])');
          if (!target && isInput) target = freshLine.querySelector('[data-quantity-input]');
          if (!target && isRemove) target = freshLine.querySelector('[data-cart-remove]');
          /* The line's own quantity input before the generic sweep: it is the
             control a customer editing this line most likely wants back. */
          if (!target) target = freshLine.querySelector('[data-quantity-input]');
          /* And the sweep must skip what is not in the accessibility tree. The
             FIRST focusable element in a cart line is .cart-line__media-link,
             which carries tabindex="-1" aria-hidden="true" precisely so it is
             not a stop — focusing it strands a screen reader on an element it
             has been told to ignore. This is the same failure mode the cart
             drawer chose inert over aria-hidden to avoid. */
          if (!target) target = freshLine.querySelector(FOCUSABLE_VISIBLE);""",
    'focus never lands on an aria-hidden element')

sub('assets/cart.js',
    """  var SUPPORTS_INERT = 'inert' in HTMLElement.prototype;""",
    """  /* FOCUSABLE minus anything hidden from assistive technology. Used for the
     last-resort focus target after a section swap; see captureFocusIntent. */
  var FOCUSABLE_VISIBLE = FOCUSABLE
    .split(',')
    .map(function (s) { return s + ':not([aria-hidden="true"])'; })
    .join(',');

  var SUPPORTS_INERT = 'inert' in HTMLElement.prototype;""",
    'a focusable-and-announceable selector')


# ================== the filtered-empty copy promises a control that is absent
lp = os.path.join(THEME, 'locales', 'en.default.json')
loc = json.load(io.open(lp, encoding='utf-8'), object_pairs_hook=OrderedDict)
loc['collection']['filters']['none_match']['body'] = 'Clear them and start again.'
io.open(lp, 'w', encoding='utf-8').write(json.dumps(loc, indent=2, ensure_ascii=False) + '\n')
print('  ok  %-32s %s' % ('locales/en.default.json',
                          'filtered-empty copy matches the control offered'))
