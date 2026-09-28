/* GOD SQUAD — product page behaviour
 * Phase 8. Loaded only by sections/main-product.liquid.
 *
 * Two jobs, and nothing else: keep the buy controls in step with the selected
 * variant, and keep the media gallery's rail in step with what is on screen.
 *
 * NOTHING HERE IS REQUIRED TO BUY THE PRODUCT.
 * The server renders the correct variant, price, availability and button state
 * for the page's initial variant, and the form posts natively. With this file
 * blocked, a customer can still add the default variant to their cart; they
 * simply cannot switch variant without a page load. Shopify formally dropped
 * the no-JavaScript variant-switching requirement, so no link-per-variant
 * fallback is built — but the hidden variant input is always correct at render
 * time, which is the part that matters.
 *
 * WHY THE VARIANT TABLE IS EMBEDDED RATHER THAN FETCHED.
 * The alternative is to re-render the section from the server on every size
 * click, which is a network round trip per tap. For an apparel catalogue the
 * six fields the picker needs are a few hundred bytes, and the money strings
 * are formatted by Liquid against the store's own money format — which is the
 * one thing the browser genuinely cannot do correctly.
 */
(function () {
  'use strict';

  function init(root) {
    if (!root || root.dataset.gsProductBound === 'true') return;
    root.dataset.gsProductBound = 'true';

    initVariants(root);
    initGallery(root);
  }

  // --------------------------------------------------------------- variants

  function initVariants(root) {
    var dataEl = root.querySelector('[data-variant-data]');
    var picker = root.querySelector('[data-variant-picker]');
    if (!dataEl) return;

    var variants;
    try {
      variants = JSON.parse(dataEl.textContent);
    } catch (error) {
      if (window.console && console.warn) console.warn('[god-squad] variant data is not valid JSON', error);
      return;
    }
    if (!Array.isArray(variants) || !variants.length) return;

    var form = root.querySelector('[data-product-form]');
    var variantInput = root.querySelector('[data-variant-input]');
    var addButton = root.querySelector('[data-add-to-cart]');

    function selectedOptions() {
      if (!picker) return [];
      var checked = picker.querySelectorAll('.variant-picker__input:checked');
      var values = [];
      Array.prototype.forEach.call(checked, function (input) {
        var position = parseInt(input.getAttribute('data-option-position'), 10);
        values[position - 1] = input.value;
      });
      return values;
    }

    function matches(variant, values) {
      if (!variant.options) return false;
      for (var i = 0; i < values.length; i++) {
        if (values[i] === undefined) continue;
        if (variant.options[i] !== values[i]) return false;
      }
      return true;
    }

    function findVariant(values) {
      for (var i = 0; i < variants.length; i++) {
        if (matches(variants[i], values)) return variants[i];
      }
      return null;
    }

    /* A value is offered when some AVAILABLE variant exists that carries it
       alongside everything else currently chosen. This is why the picker
       cannot rely on product_option_value.available alone: that flag says
       "some variant with this value is in stock", not "the combination you
       have built is in stock". */
    function refreshAvailability(values) {
      if (!picker) return;
      var inputs = picker.querySelectorAll('.variant-picker__input');
      Array.prototype.forEach.call(inputs, function (input) {
        var position = parseInt(input.getAttribute('data-option-position'), 10);
        var probe = values.slice();
        probe[position - 1] = input.value;

        var available = false;
        for (var i = 0; i < variants.length; i++) {
          if (variants[i].available && matches(variants[i], probe)) {
            available = true;
            break;
          }
        }

        var label = picker.querySelector('label[for="' + input.id + '"]');
        if (available) {
          input.removeAttribute('data-unavailable');
          if (label) label.classList.remove('variant-picker__value--unavailable');
        } else {
          input.setAttribute('data-unavailable', 'true');
          if (label) label.classList.add('variant-picker__value--unavailable');
        }
        /* The words follow the styling. A struck-through chip whose accessible
           name never changed would look unavailable and announce available.
           The element is kept in the DOM and kept focusable either way, which
           is what Phase 2 §27.4 requires. */
        if (label) {
          var note = label.querySelector('[data-unavailable-note]');
          if (!available && !note) {
            note = document.createElement('span');
            note.className = 'visually-hidden';
            note.setAttribute('data-unavailable-note', '');
            note.textContent = ' ' + (root.getAttribute('data-string-unavailable') || '');
            label.appendChild(note);
          } else if (available && note) {
            note.parentNode.removeChild(note);
          }
        }
      });
    }

    function updateLegends() {
      if (!picker) return;
      var checked = picker.querySelectorAll('.variant-picker__input:checked');
      Array.prototype.forEach.call(checked, function (input) {
        var position = input.getAttribute('data-option-position');
        var out = picker.querySelector('[data-option-value-for="' + position + '"]');
        if (out) out.textContent = input.value;
      });
    }

    function updatePrice(variant) {
      var current = root.querySelector('[data-price-current]');
      var compareWrap = root.querySelector('[data-price-compare-wrap]');
      var compare = root.querySelector('[data-price-compare]');
      var saleLabel = root.querySelector('[data-price-label-sale]');
      if (!current) return;

      /* innerHTML, not textContent: a money string is rendered by Liquid
         against the store's money format, which a merchant may set with markup
         in it. The value came from this page's own server render, so there is
         no untrusted input in it. */
      current.innerHTML = variant.price;

      var onSale = !!variant.compare_at_price;
      if (compare && variant.compare_at_price) compare.innerHTML = variant.compare_at_price;
      if (compareWrap) compareWrap.hidden = !onSale;
      if (saleLabel) saleLabel.hidden = !onSale;
    }

    function updateButton(variant) {
      if (!addButton) return;
      var label = addButton.querySelector('[data-add-to-cart-label]');
      var buyable = !!(variant && variant.available);

      addButton.disabled = !buyable;
      if (label) {
        /* Three states, not two. A null variant is an option combination that
           was never manufactured — it is not sold out, and saying "Sold out"
           tells the customer something false: that it existed and ran out, so
           it might come back. "Unavailable" is the honest word, and the locale
           already carries it. */
        var next;
        if (buyable) {
          next = addButton.getAttribute('data-label-idle');
        } else if (variant) {
          next = addButton.getAttribute('data-label-sold-out');
        } else {
          next = addButton.getAttribute('data-label-unavailable')
            || addButton.getAttribute('data-label-sold-out');
        }
        label.textContent = next || label.textContent;
      }

      /* The variant input is disabled alongside the button, so a form
         submitted some other way — Enter in the quantity field, a script, a
         browser autofill — cannot post a sold-out variant either. */
      if (variantInput) {
        variantInput.value = variant ? variant.id : '';
        variantInput.disabled = !buyable;
      }
    }

    /* Shopify carries the minimum, maximum and increment per VARIANT, and the
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

    /* Hidden rather than emptied: a labelled row with nothing after it is not
       information. The row only exists when some variant has a SKU. */
    function updateSkuRow(variant) {
      var row = root.querySelector('[data-variant-sku-row]');
      if (!row) return;
      var has = !!(variant && variant.sku);
      if (has) {
        row.removeAttribute('hidden');
      } else {
        row.setAttribute('hidden', '');
      }
    }

    /* The theme never learns the count — the server sent a boolean — so this
       can only show or hide the line it was given. */
    function updateLowStock(variant) {
      var line = root.querySelector('[data-low-stock]');
      if (!line) return;
      if (variant && variant.low_stock) {
        line.removeAttribute('hidden');
      } else {
        line.setAttribute('hidden', '');
      }
    }

    function updateSku(variant) {
      var sku = root.querySelector('[data-variant-sku]');
      if (sku) sku.textContent = variant && variant.sku ? variant.sku : '';
    }

    function updateUrl(variant) {
      if (!variant || !window.history || !window.history.replaceState) return;
      /* replaceState, never pushState. Trying three sizes should not put three
         entries between the customer and the page they came from, which the
         brief calls out directly. */
      try {
        var next = new URL(window.location.href);
        next.searchParams.set('variant', variant.id);
        window.history.replaceState({}, '', next.toString());
      } catch (error) {
        /* A browser that cannot parse its own URL is not a reason to stop the
           rest of the update. */
      }
    }

    function updateMedia(variant) {
      if (!variant || variant.media_id === null || variant.media_id === undefined) return;
      var gallery = root.querySelector('[data-product-gallery]');
      if (!gallery) return;
      var slide = gallery.querySelector('[data-media-id="' + variant.media_id + '"]');
      if (slide) showSlide(gallery, slide, false);
    }

    function onChange() {
      var values = selectedOptions();
      var variant = findVariant(values);

      updateLegends();
      refreshAvailability(values);
      updateButton(variant);
      updateSkuRow(variant);
      updateLowStock(variant);
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
      }
    }

    if (picker) picker.addEventListener('change', onChange);

    // Run once so a page loaded with ?variant= has its availability marks right.
    refreshAvailability(selectedOptions());

    /* A guard, not decoration: if the form is submitted while the variant
       input is disabled, nothing is added and the customer gets no reason. */
    if (form) {
      form.addEventListener('submit', function (event) {
        if (variantInput && (variantInput.disabled || !variantInput.value)) {
          event.preventDefault();
          event.stopImmediatePropagation();
        }
      }, true);
    }
  }

  // ---------------------------------------------------------------- gallery

  function showSlide(gallery, slide, smooth) {
    var viewport = gallery.querySelector('[data-gallery-viewport]');
    if (!viewport || !slide) return;

    Array.prototype.forEach.call(gallery.querySelectorAll('.product-gallery__slide'), function (el) {
      el.classList.toggle('is-active', el === slide);
    });

    var id = slide.getAttribute('data-media-id');
    Array.prototype.forEach.call(gallery.querySelectorAll('[data-gallery-thumb]'), function (thumb) {
      var on = thumb.getAttribute('data-media-id') === id;
      thumb.classList.toggle('is-active', on);
      if (on) {
        thumb.setAttribute('aria-current', 'true');
      } else {
        thumb.removeAttribute('aria-current');
      }
    });

    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var behavior = smooth && !reduced ? 'smooth' : 'auto';

    /* Branch on what is RENDERED, not on the merchant's setting. The stacked
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
    }
  }

  function initGallery(root) {
    var gallery = root.querySelector('[data-product-gallery]');
    if (!gallery) return;

    var viewport = gallery.querySelector('[data-gallery-viewport]');
    var rail = gallery.querySelector('[data-gallery-rail]');

    if (rail) {
      rail.addEventListener('click', function (event) {
        var thumb = event.target && typeof event.target.closest === 'function'
          ? event.target.closest('[data-gallery-thumb]')
          : null;
        if (!thumb) return;
        /* Cancelled so the hash is never written. The anchor is what makes the
           rail work with no script at all; with script, it should not fill the
           back button with one entry per photograph. */
        event.preventDefault();
        var slide = gallery.querySelector(
          '.product-gallery__slide[data-media-id="' + thumb.getAttribute('data-media-id') + '"]'
        );
        showSlide(gallery, slide, true);
      });
    }

    /* The server already marked the slide this page should open on — a URL
       carrying ?variant= for a variant whose featured_media is not the first
       medium. Below the split the gallery is a scroll-snap carousel whatever
       the merchant's layout setting says, so without this the viewport stays
       on slide one and the customer sees the wrong photograph. */
    var active = gallery.querySelector('.product-gallery__slide.is-active');
    var first = gallery.querySelector('.product-gallery__slide');
    if (active && first && active !== first) showSlide(gallery, active, false);

    /* Keep the rail in step with a swipe or a scroll. IntersectionObserver
       rather than a scroll listener: it fires only when a slide actually
       becomes the one on screen, and it costs nothing while nothing moves. */
    if (viewport && 'IntersectionObserver' in window) {
      var observer = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (!entry.isIntersecting || entry.intersectionRatio < 0.6) return;
            var id = entry.target.getAttribute('data-media-id');
            Array.prototype.forEach.call(gallery.querySelectorAll('[data-gallery-thumb]'), function (thumb) {
              var on = thumb.getAttribute('data-media-id') === id;
              thumb.classList.toggle('is-active', on);
              if (on) {
                thumb.setAttribute('aria-current', 'true');
              } else {
                thumb.removeAttribute('aria-current');
              }
            });
          });
        },
        { root: viewport, threshold: [0.6] }
      );
      Array.prototype.forEach.call(gallery.querySelectorAll('.product-gallery__slide'), function (slide) {
        observer.observe(slide);
      });
    }
  }

  // ------------------------------------------------------------------- boot

  function initAll() {
    Array.prototype.forEach.call(document.querySelectorAll('[data-main-product]'), init);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }

  document.addEventListener('shopify:section:load', function (event) {
    var product = event.target.querySelector('[data-main-product]');
    if (product) init(product);
  });
})();
