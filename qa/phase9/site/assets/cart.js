/* GOD SQUAD — cart behaviour
 * Phase 8.
 *
 * Answers PHASE-1-WEBSITE-AUDIT.md ECOM-02: "There is no cart, cart drawer,
 * add-to-cart, quantity control or checkout pathway; the cart icon is an inert
 * image with a literal 0 badge."
 *
 * WHAT THIS FILE IS ALLOWED TO ASSUME: NOTHING.
 * Every control it enhances already works without it. The product form posts
 * natively to /cart/add. The cart form posts natively to /cart with updates[].
 * Removal is a real link to item.url_to_remove. The header's cart control is a
 * real link to the cart page. This file cancels those default behaviours and
 * does the same work over Shopify's Ajax Cart API, and if it fails to load,
 * every one of them still works with a page reload.
 *
 * No framework, no dependency, no polyfill, one file, no global beyond the
 * single namespace below.
 *
 * DESIGN NOTES THAT ARE NOT OBVIOUS FROM THE CODE
 *
 * 1. URLs come from window.Shopify.routes.root, never from a literal
 *    '/cart/add.js'. A store with Markets or a secondary language serves the
 *    cart under a locale prefix, and a hardcoded path silently 404s there.
 *
 * 2. Cart lines are identified by their line item KEY, never by index and
 *    never by variant id. Two lines can share a variant id — the same variant
 *    with different properties, or split by an automatic discount — and an
 *    index shifts the moment anything is removed. The key is also not stable
 *    across mutations, so it is re-read from freshly rendered markup every
 *    time rather than cached.
 *
 * 3. A 422 from /cart/add can mean the cart changed anyway: when the requested
 *    quantity exceeds stock, Shopify adds the maximum it can AND returns the
 *    error. So an error response is never treated as "nothing happened" — the
 *    cart is re-read either way.
 *
 * 4. Sections are requested in the same round trip as the mutation rather than
 *    fetched afterwards, so the drawer and the header badge are always the
 *    server's view of the cart after the change, never a number this file
 *    calculated.
 *
 * 5. The background is made inert rather than aria-hidden. aria-hidden leaves
 *    content focusable while removing it from the accessibility tree, which
 *    strands a screen reader on an element it cannot describe.
 */
(function () {
  'use strict';

  /* Phase 2 §12.4 sets this literal explicitly and says not to use a motion
     token: --duration-* collapses to 1ms under prefers-reduced-motion, which
     would remove the debounce for exactly the people most likely to be using
     a keyboard to step a quantity. */
  var QUANTITY_DEBOUNCE_MS = 250;

  /* The render targets, built from what is actually on THIS page rather than
     fixed, because the three surfaces do not all coexist:

       cart-icon-bubble  a standalone section file, always requested
       cart-drawer       rendered from the layout on every template but /cart
       the cart page     rendered by templates/cart.json, its id read at runtime

     The cart page had to be added. The script intercepts its quantity steppers
     and its Remove links, and without a way to re-render it the customer saw
     their change do nothing — and after a removal the page's POSITIONAL
     updates[] inputs no longer lined up with the server's lines, so pressing
     Checkout would have applied each surviving quantity to the wrong product.

     Shopify allows at most five sections per request; this asks for at most
     three. */
  var SECTIONS = ['cart-icon-bubble'];
  var CART_PAGE_ID = null;

  function collectSections() {
    SECTIONS = ['cart-icon-bubble'];
    CART_PAGE_ID = null;
    if (document.querySelector('[data-cart-drawer]')) SECTIONS.push('cart-drawer');
    var page = document.querySelector('[data-cart-page-section]');
    if (page) {
      CART_PAGE_ID = page.getAttribute('data-cart-page-section');
      if (CART_PAGE_ID) SECTIONS.push(CART_PAGE_ID);
    }
  }

  var FOCUSABLE = [
    'a[href]',
    'button:not([disabled])',
    'input:not([disabled]):not([type="hidden"])',
    'select:not([disabled])',
    'textarea:not([disabled])',
    '[tabindex]:not([tabindex="-1"])'
  ].join(',');

  /* FOCUSABLE minus anything hidden from assistive technology. Used for the
     last-resort focus target after a section swap; see captureFocusIntent. */
  var FOCUSABLE_VISIBLE = FOCUSABLE
    .split(',')
    .map(function (s) { return s + ':not([aria-hidden="true"])'; })
    .join(',');

  var SUPPORTS_INERT = 'inert' in HTMLElement.prototype;

  // ----------------------------------------------------------------- routes

  function root() {
    var r = window.Shopify && window.Shopify.routes && window.Shopify.routes.root;
    return r || '/';
  }

  function url(path) {
    return root() + path;
  }

  // ------------------------------------------------------------------- i18n
  /* Every string this file can display comes from Liquid, through data
     attributes on the elements themselves. Nothing user-facing is written in
     JavaScript, so nothing here can be untranslatable. */

  function stringFor(name, fallback) {
    var host = document.querySelector('[data-cart-strings]');
    if (!host) return fallback || null;
    var value = host.getAttribute('data-' + name);
    return value === null ? (fallback || null) : value;
  }

  /* Liquid writes the sentence with a [count] token in it, because where the
     number falls in a sentence is a translation decision, not a code one. */
  function stringWithCount(name, count) {
    var template = stringFor(name, null);
    return template ? template.replace('[count]', count) : null;
  }

  /* event.target is an Element for every listener below, but a synthetic or
     retargeted event can arrive with something that has no closest(). */
  function closestFrom(event, selector) {
    var node = event.target;
    if (!node || typeof node.closest !== 'function') return null;
    return node.closest(selector);
  }

  // --------------------------------------------------------------- announce

  function announce(message) {
    if (!message) return;
    /* While the drawer is open, aria-modal="true" tells assistive technology to
       treat everything outside it as absent — including the layout's region. The
       drawer carries its own for exactly that window. Looked up each time rather
       than cached, because the drawer does not exist on every page. */
    var liveRegion = null;
    if (Drawer.isOpen) liveRegion = document.querySelector('[data-cart-drawer-status]');
    if (!liveRegion) liveRegion = document.getElementById('CartStatus');
    if (!liveRegion) return;
    /* Injected into a region that was already in the DOM and already empty.
       A region created together with its content announces nothing, which is
       what happens if the region lives inside markup the section render
       replaces — so it lives in the layout instead. The timeout gives the
       accessibility tree a turn to notice the node before the text lands. */
    liveRegion.textContent = '';
    window.setTimeout(function () {
      liveRegion.textContent = message;
    }, 0);
  }

  // ------------------------------------------------------------------ fetch

  /* One request shape for every mutation. Returns a promise that always
     resolves to {ok, data, sections} — a rejected promise would make every
     call site handle transport and application errors differently. */
  function post(path, body, isFormData) {
    var options = { method: 'POST', body: body };
    if (!isFormData) {
      /* Only the JSON shape gets a Content-Type. Setting one on a FormData
         body overwrites the multipart boundary the browser generated and the
         request arrives unparseable. */
      options.headers = { 'Content-Type': 'application/json', Accept: 'application/json' };
    } else {
      options.headers = { Accept: 'application/json' };
    }

    return fetch(url(path), options)
      .then(function (response) {
        return response
          .json()
          .catch(function () { return null; })
          .then(function (data) {
            return { response: response, data: data };
          });
      })
      .then(function (result) {
        var data = result.data || {};
        /* Shopify signals an application error with a `description`. The
           `status` field is sometimes the integer 422 and sometimes the string
           'bad_request', so it is not a reliable test on its own. */
        var failed = !result.response.ok || typeof data.description === 'string';
        return {
          ok: !failed,
          data: data,
          message: data.description || null,
          sections: data.sections || null
        };
      })
      .catch(function (error) {
        /* A transport failure: offline, DNS, a blocked request. The customer
           gets the theme's own sentence; the detail goes to the console for
           whoever is debugging it. */
        if (window.console && console.warn) console.warn('[god-squad] cart request failed', error);
        return { ok: false, data: {}, message: stringFor('error-network', null), sections: null, network: true };
      });
  }

  /* A failed cart request reported only to a live region leaves a sighted
     customer watching a quantity snap back with no explanation. Every cart
     surface carries a visible line for it, outside the node the section render
     replaces, so a message survives the re-render that produced it.

     SCOPED TO THE CART SURFACES. This selected [data-cart-error] across the
     whole document, and a quick-add product card carries one too — so a line
     that Shopify refused in the cart printed its refusal onto unrelated
     product tiles behind the drawer. A per-form failure is showFormError's
     job; this one belongs to the drawer and the cart page only. */
  var CART_ERROR_BOXES = '[data-cart-drawer] [data-cart-error], [data-cart-page] [data-cart-error]';

  function showCartError(message) {
    Array.prototype.forEach.call(document.querySelectorAll(CART_ERROR_BOXES), function (box) {
      if (message) {
        box.textContent = message;
        box.hidden = false;
      } else {
        box.textContent = '';
        box.hidden = true;
      }
    });
  }

  function sectionParams() {
    return {
      sections: SECTIONS.join(','),
      /* Must begin with a slash, or the whole request returns 400 — and the
         docs warn that a 400 for this reason does not mean the cart mutation
         was rolled back. location.pathname always begins with one, and using
         it keeps the rendered sections in the context of the page the
         customer is actually on. */
      sections_url: window.location.pathname
    };
  }

  // ------------------------------------------------------- section swapping

  function sectionInner(html) {
    if (typeof html !== 'string') return null;
    var parsed = new DOMParser().parseFromString(html, 'text/html');
    /* The response always carries the <div id="shopify-section-..."> wrapper.
       Replacing outerHTML with it would nest a second wrapper on every
       update, so the inside is taken instead. */
    var wrapper = parsed.querySelector('.shopify-section');
    return wrapper ? wrapper : parsed.body;
  }

  function applySections(sections) {
    if (!sections) return;

    // The header badge: replace the contents of the cart control.
    var bubbleHtml = sections['cart-icon-bubble'];
    var bubbleTarget = document.querySelector('[data-cart-bubble]');
    if (bubbleHtml && bubbleTarget) {
      var bubble = sectionInner(bubbleHtml);
      if (bubble) bubbleTarget.innerHTML = bubble.innerHTML;
    }

    // The drawer: replace only the part below the heading.
    swapInner(sections['cart-drawer'], '[data-cart-drawer-inner]', 'CartDrawerTitle');

    // The cart page, when this is one.
    if (CART_PAGE_ID) {
      swapInner(sections[CART_PAGE_ID], '[data-cart-page-inner]', 'CartPageTitle');
    }
  }

  /* One swap, used by both cart surfaces. The fallback focus target is that
     surface's own heading, which is why both headings sit outside the node
     being replaced. */
  function swapInner(html, selector, fallbackId) {
    if (!html) return;
    var target = document.querySelector(selector);
    if (!target) return;
    var parsed = sectionInner(html);
    var fresh = parsed && parsed.querySelector(selector);
    if (!fresh) return;
    var restore = captureFocusIntent(target, fallbackId);
    var restoreNote = captureNote(target);
    target.innerHTML = fresh.innerHTML;
    restoreNote();
    restore();
  }

  /* Replacing a subtree destroys whatever inside it had focus, and the browser
     drops focus to <body>. That is a keyboard user losing their place in the
     middle of editing a quantity. The line being edited is remembered before
     the swap and the equivalent control is focused after it; if that line is
     gone — which is what removal means — focus goes to the drawer's heading,
     which is where the dialog pattern puts it. */
  function captureFocusIntent(container, fallbackId) {
    var active = document.activeElement;
    if (!active || !container.contains(active)) return function () {};

    var line = typeof active.closest === 'function' ? active.closest('[data-line-key]') : null;
    var key = line ? line.getAttribute('data-line-key') : null;
    var step = active.getAttribute ? active.getAttribute('data-quantity-step') : null;
    var isInput = active.hasAttribute && active.hasAttribute('data-quantity-input');
    var isRemove = active.hasAttribute && active.hasAttribute('data-cart-remove');
    /* The note is the one control in the swapped node that does not belong to
       a line, so the key-based path below cannot find it and the customer was
       thrown to the heading mid-sentence by a quantity change they had made
       before starting to type. */
    var isNote = active.hasAttribute && active.hasAttribute('data-cart-note');

    return function () {
      var target = null;
      if (isNote) target = container.querySelector('[data-cart-note]');
      if (!target && key) {
        var selector = '[data-line-key="' + (window.CSS && CSS.escape ? CSS.escape(key) : key) + '"]';
        var freshLine = container.querySelector('[data-cart-line]' + selector);
        if (freshLine) {
          if (step) target = freshLine.querySelector('[data-quantity-step="' + step + '"]:not([aria-disabled="true"])');
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
          if (!target) target = freshLine.querySelector(FOCUSABLE_VISIBLE);
        }
      }
      if (!target) target = document.getElementById(fallbackId || 'CartDrawerTitle');
      if (target && typeof target.focus === 'function') target.focus();
    };
  }

  // ------------------------------------------------------------ the drawer

  var Drawer = {
    el: null,
    opener: null,
    isOpen: false,
    scrollY: 0,

    /* Everything the drawer puts OUTSIDE its own subtree: the open class on
       <html>, the inert attribute on its siblings, the document-level focus
       trap and the fixed-position scroll lock on <body>. None of it goes away
       with the drawer's node, so all of it has to be undone explicitly.

       Called from init() — the Theme Editor re-renders a section in place, and
       if the drawer was open the new node arrived hidden while every one of
       those outlived it, leaving the page scroll-locked and the background
       unreachable with no drawer on screen — and from the unload handler, for
       the case where no new node follows. */
    reset: function () {
      if (!this.isOpen) return;
      this.isOpen = false;
      document.documentElement.classList.remove('cart-drawer-open');
      this.setBackgroundInert(false);
      document.removeEventListener('keydown', this.onKeydown, true);
      this.unlockScroll();
      this.opener = null;
    },

    init: function () {
      this.reset();

      this.el = document.querySelector('[data-cart-drawer]');
      if (!this.el) return;

      var self = this;
      var overlay = this.el.querySelector('[data-cart-overlay]');
      if (overlay) overlay.addEventListener('click', function () { self.close(); });

      this.el.addEventListener('click', function (event) {
        if (closestFrom(event, '[data-cart-close]')) self.close();
      });
    },

    open: function (opener) {
      if (!this.el || this.isOpen) return;
      this.isOpen = true;
      this.opener = opener || document.activeElement;

      this.el.hidden = false;
      // Force a frame so the slide has a start state to animate from.
      void this.el.offsetWidth;

      document.documentElement.classList.add('cart-drawer-open');
      this.lockScroll();
      this.setBackgroundInert(true);

      var title = document.getElementById('CartDrawerTitle');
      if (title) title.focus();

      document.addEventListener('keydown', this.onKeydown, true);
    },

    close: function () {
      if (!this.el || !this.isOpen) return;
      this.isOpen = false;

      document.documentElement.classList.remove('cart-drawer-open');
      this.setBackgroundInert(false);
      document.removeEventListener('keydown', this.onKeydown, true);

      var el = this.el;
      var self = this;
      var done = function () {
        if (!self.isOpen) el.hidden = true;
        el.removeEventListener('transitionend', done);
      };
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        done();
      } else {
        el.addEventListener('transitionend', done);
        window.setTimeout(done, 500);
      }

      this.unlockScroll();

      /* Focus returns to whatever opened the drawer — but only if it is still
         in the document. An add-to-cart button on a product card can be
         re-rendered away while the drawer is open, and focusing a detached
         node silently puts focus on <body>. */
      var target = this.opener;
      if (!target || !document.contains(target) || typeof target.focus !== 'function') {
        target = document.querySelector('[data-cart-bubble]');
      }
      if (target) target.focus();
      this.opener = null;
    },

    onKeydown: function (event) {
      if (event.key !== 'Escape' && event.key !== 'Esc') {
        Drawer.trapTab(event);
        return;
      }
      event.preventDefault();
      Drawer.close();
    },

    /* Only runs where inert is unavailable. Where it is available the browser
       does this correctly, including for pointer input and find-in-page, and a
       hand-rolled trap on top of it would fight it. */
    trapTab: function (event) {
      if (SUPPORTS_INERT || event.key !== 'Tab' || !Drawer.el) return;
      var items = Array.prototype.filter.call(
        Drawer.el.querySelectorAll(FOCUSABLE),
        function (el) { return el.offsetParent !== null; }
      );
      if (!items.length) return;
      var first = items[0];
      var last = items[items.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      } else if (!Drawer.el.contains(document.activeElement)) {
        event.preventDefault();
        first.focus();
      }
    },

    setBackgroundInert: function (on) {
      if (!SUPPORTS_INERT || !this.el) return;
      var self = this;
      Array.prototype.forEach.call(document.body.children, function (child) {
        /* contains(), not identity. Shopify wraps every section in
           <div id="shopify-section-..."> when the layout renders it, so the
           drawer is never itself a child of <body> — it is inside that
           wrapper. Comparing identity marked the wrapper inert, which made the
           drawer inert with it, and focus could not be moved into a drawer
           that had just been opened. */
        if (child === self.el || child.contains(self.el)) return;
        if (child.hasAttribute('data-cart-no-inert')) return;
        if (child.tagName === 'SCRIPT' || child.tagName === 'STYLE' || child.tagName === 'LINK') return;
        if (on) {
          child.setAttribute('inert', '');
        } else {
          child.removeAttribute('inert');
        }
      });
    },

    /* overflow:hidden does not lock iOS Safari, and position:fixed without
       saving the offset is the "close the cart and you are back at the top of
       the page" bug. Both halves are needed. The reserved scrollbar gutter
       that stops the page jumping sideways is in section-cart-drawer.css,
       because it has to be in force before this runs. */
    lockScroll: function () {
      this.scrollY = window.scrollY || window.pageYOffset || 0;
      var body = document.body;
      body.style.position = 'fixed';
      body.style.top = -this.scrollY + 'px';
      body.style.left = '0';
      body.style.right = '0';
      body.style.width = '100%';
    },

    unlockScroll: function () {
      var body = document.body;
      body.style.position = '';
      body.style.top = '';
      body.style.left = '';
      body.style.right = '';
      body.style.width = '';
      window.scrollTo(0, this.scrollY);
    },

    autoOpens: function () {
      return this.el && this.el.getAttribute('data-auto-open') === 'true';
    }
  };

  // ----------------------------------------------------------- add to cart

  /* aria-busy ONLY. Two reasons not to touch `disabled` here.

     Disabling the element that currently holds focus blurs it, so every single
     add to cart dropped a keyboard user back to <body>. And restoring it
     afterwards asserted `disabled = false` with no knowledge of why it might be
     disabled — switch to a sold-out size while an add is in flight, and the
     response re-enabled a button for a variant that cannot be bought.

     Nothing is lost by dropping it: the submit is always cancelled, and the
     double-submit guard in onAddSubmit reads aria-busy. The label change is
     announced, because the button keeps focus while its name changes. */
  function setButtonBusy(button, busy) {
    if (!button) return;
    var label = button.querySelector('[data-add-to-cart-label]');
    if (busy) {
      button.setAttribute('aria-busy', 'true');
      if (label) label.textContent = button.getAttribute('data-label-busy') || label.textContent;
    } else {
      button.removeAttribute('aria-busy');
      /* The idle label only while the control is still buyable: product.js owns
         disabled, and may have changed variant while this was in flight. */
      if (label && !button.disabled) {
        label.textContent = button.getAttribute('data-label-idle') || label.textContent;
      }
    }
  }

  /* Returns true when a confirmation line exists and was filled, so the
     caller knows whether the live region still has to say it. */
  function showFormSuccess(form, message) {
    var box = form.querySelector('[data-product-success]');
    if (!box) return false;
    if (message) {
      var text = box.querySelector('[data-product-success-text]') || box;
      /* Reveal first, write on the next turn. Same reasoning as announce()
         above, and for the same reason it needs a timeout: a region that is
         created — or un-hidden — together with its content announces nothing,
         because the accessibility tree never sees it empty and so never sees
         the text arrive as a change.

         This used to work by accident. `.main-product__success` declared
         `display: flex`, which beat the user agent's `[hidden]` rule, so the
         region was permanently rendered and permanently registered and a
         same-turn write was a plain text change. Fixing that cascade defect
         (section-main-product.css, `.main-product__success[hidden]`) makes the
         region genuinely display:none between adds, which is correct and which
         is exactly the case announce() warns about.

         The clear is for the second add: the message is identical to the first,
         and writing a string a region already contains is not a change and
         announces nothing either. It is guarded because when the dedicated span
         is missing `text` falls back to the box itself, and clearing the box
         would delete the View cart link inside it. */
      box.hidden = false;
      if (text !== box) text.textContent = '';
      window.setTimeout(function () {
        text.textContent = message;
      }, 0);
    } else {
      box.hidden = true;
    }
    return !!message;
  }

  function showFormError(form, message) {
    var box = form.querySelector('[data-product-error], [data-cart-error]');
    if (!box) {
      announce(message);
      return;
    }
    if (message) {
      box.textContent = message;
      box.hidden = false;
    } else {
      box.textContent = '';
      box.hidden = true;
    }
  }

  function onAddSubmit(event) {
    var form = closestFrom(event, 'form[action*="/cart/add"]');
    if (!form) return;

    event.preventDefault();

    var button = form.querySelector('[data-add-to-cart]') || form.querySelector('[type="submit"]');
    if (button && button.getAttribute('aria-busy') === 'true') return; // no double submits
    showFormError(form, null);
    showFormSuccess(form, null);
    setButtonBusy(button, true);

    /* FormData rather than a hand-built JSON body: it carries the variant id,
       the quantity and any line item properties or selling plan the form
       already contains, without this file having to know they are there. */
    var body = new FormData(form);
    var params = sectionParams();
    body.append('sections', params.sections);
    body.append('sections_url', params.sections_url);

    /* Adds share the counter with quantity changes. Two quick-add buttons on
       different product cards are not blocked by the per-button guard above, so
       without this the slower response could paint an older cart over a newer
       one. */
    var seq = ++requestSeq;

    post('cart/add.js', body, true).then(function (result) {
      setButtonBusy(button, false);

      /* Sections are rendered after the mutation, so they are applied whether
         or not the call reported success — a 422 for "more than we have" has
         already added what it could, and showing the old cart would be a lie.
         Unless a later request has already been answered, in which case this
         markup is older than what is on screen. */
      if (seq === requestSeq) applySections(result.sections);

      if (!result.ok) {
        showFormError(form, result.message || stringFor('error-generic', null));
        showCartError(null);
        /* A partial add with no sections back means this file no longer knows
           what the cart holds. Re-render rather than guess. */
        if (!result.sections && !result.network) refreshSections();
        return;
      }

      var opensDrawer = Drawer.autoOpens() && Drawer.el;
      if (opensDrawer) {
        /* Focus is moving into the drawer, so the addition is NOT announced:
           announcing and moving focus at the same moment makes a screen reader
           talk over itself, and the drawer's heading already says where the
           customer now is. */
        Drawer.open(button);
      } else {
        /* No drawer opened — the merchant chose the cart page, or switched
           auto-open off. The header badge changes, and that was the ONLY
           sighted feedback an add produced. showFormSuccess reveals the
           form's own confirmation line, which is a role="status" region and
           therefore announces itself; announce() is called only when the form
           has no such line, so nothing is ever said twice. */
        if (!showFormSuccess(form, stringFor('added', null))) {
          announce(stringFor('added', null));
        }
      }
    });
  }

  /* Used when a mutation succeeded but returned no usable sections. */
  function refreshSections() {
    fetch(window.location.pathname + '?sections=' + SECTIONS.join(','), {
      headers: { Accept: 'application/json' }
    })
      .then(function (r) { return r.json(); })
      .then(applySections)
      .catch(function () { /* The cart is still correct on the server; a reload will show it. */ });
  }

  // ------------------------------------------------------- change quantity

  var pending = {};
  var requestSeq = 0;

  function changeLine(key, quantity, origin) {
    if (!key) return;

    /* Cancel anything still queued for this line. Removal calls straight in
       here rather than through queueChange, so without this a step made
       inside the debounce window fired 250ms AFTER the removal and re-added
       the line at the stepped quantity. Any immediate change also supersedes
       a queued one by definition. */
    if (pending[key]) {
      window.clearTimeout(pending[key]);
      delete pending[key];
    }

    var line = origin ? origin.closest('[data-cart-line]') : null;
    var control = line ? line.querySelector('[data-quantity]') : null;
    if (control) control.setAttribute('aria-busy', 'true');

    var seq = ++requestSeq;
    var params = sectionParams();
    var body = JSON.stringify({
      id: key,
      quantity: quantity,
      sections: params.sections,
      sections_url: params.sections_url
    });

    post('cart/change.js', body, false).then(function (result) {
      /* The busy state and the error are ALWAYS cleared and always reported,
         even for a superseded request. Returning early on the sequence check
         left a line dimmed and inert forever and swallowed the reason a change
         was refused; only the markup swap is genuinely made stale by a later
         response, so only the markup swap is gated. */
      if (control) control.removeAttribute('aria-busy');

      if (!result.ok) {
        var message = result.message || stringFor('error-generic', null);
        showCartError(message);
        announce(message);
        if (!result.sections && !result.network) refreshSections();
        return;
      }

      showCartError(null);
      if (seq !== requestSeq) return;
      applySections(result.sections);

      if (quantity === 0) {
        announce(stringFor('removed', null));
      } else {
        announce(stringFor('updated', null));
      }
    });
  }

  function queueChange(key, quantity, origin) {
    if (pending[key]) window.clearTimeout(pending[key]);
    pending[key] = window.setTimeout(function () {
      delete pending[key];
      changeLine(key, quantity, origin);
    }, QUANTITY_DEBOUNCE_MS);
  }

  function clampToInput(input, next) {
    var min = parseInt(input.getAttribute('min'), 10);
    var max = parseInt(input.getAttribute('max'), 10);
    if (!isNaN(min) && next < min) next = min;
    if (!isNaN(max) && next > max) next = max;
    return next;
  }

  function onQuantityClick(event) {
    var button = closestFrom(event, '[data-quantity-step]');
    if (!button) return;
    event.preventDefault();
    if (button.getAttribute('aria-disabled') === 'true') return;

    var control = button.closest('[data-quantity]');
    var input = control && control.querySelector('[data-quantity-input]');
    if (!input) return;

    var step = parseInt(button.getAttribute('data-quantity-step'), 10) || 0;
    var current = parseInt(input.value, 10);
    if (isNaN(current)) current = parseInt(input.getAttribute('min'), 10) || 1;

    var next = clampToInput(input, current + step);
    if (next === current) return;

    input.value = next;
    syncStepperState(control, next, input);

    var key = control.getAttribute('data-line-key');
    if (key) {
      queueChange(key, next, button);
    } else {
      /* The product form's quantity: nothing to tell the server until the
         form is submitted, but the change is still announced, because a
         stepper that moves a number a screen reader never reads is a control
         with no feedback (Phase 2 §12.4). */
      announce(stringWithCount('quantity-announce', next));
    }
  }

  function syncStepperState(control, value, input) {
    var min = parseInt(input.getAttribute('min'), 10);
    var max = parseInt(input.getAttribute('max'), 10);
    var down = control.querySelector('[data-quantity-step="-1"]');
    var up = control.querySelector('[data-quantity-step="1"]');
    if (down) {
      if (!isNaN(min) && value <= min) {
        down.setAttribute('aria-disabled', 'true');
      } else {
        down.removeAttribute('aria-disabled');
      }
    }
    if (up) {
      if (!isNaN(max) && value >= max) {
        up.setAttribute('aria-disabled', 'true');
      } else {
        up.removeAttribute('aria-disabled');
      }
    }
  }

  function onQuantityChange(event) {
    var input = closestFrom(event, '[data-quantity-input]');
    if (!input) return;
    var control = input.closest('[data-quantity]');
    if (!control) return;

    var value = parseInt(input.value, 10);
    if (isNaN(value)) value = parseInt(input.getAttribute('min'), 10) || 1;
    value = clampToInput(input, value);
    input.value = value;
    syncStepperState(control, value, input);

    var key = control.getAttribute('data-line-key');
    if (key) queueChange(key, value, input);
  }

  // -------------------------------------------------------------- the note

  /* Shopify's native cart note, and nothing else: one field named `note`,
     saved with /cart/update.js, read back from the cart the server renders.

     WHY IT IS SAVED AT ALL, RATHER THAN LEFT TO THE FORM.
     The cart form posts `note` natively, so with scripting off the note is
     saved by Update or by Checkout and this code is unnecessary. With
     scripting on it is necessary: a quantity change re-renders the cart from
     the server, and the server does not know about text the customer has only
     typed. Without this, editing the note and then changing a quantity threw
     the note away.

     `change` rather than `input`: it fires once, when the field is left with a
     different value, so a note is one request rather than one per keystroke.
     No sections are requested — nothing on the page depends on the note's
     value — so this is the cheapest mutation the cart makes. */
  var noteDirty = false;

  function onNoteInput(event) {
    if (closestFrom(event, '[data-cart-note]')) noteDirty = true;
  }

  function onNoteChange(event) {
    var field = closestFrom(event, '[data-cart-note]');
    if (!field) return;
    var value = field.value;
    post('cart/update.js', JSON.stringify({ note: value }), false).then(function (result) {
      if (!result.ok) {
        showCartError(result.message || stringFor('error-generic', null));
        return;
      }
      /* Only clear the flag if the field still holds what was saved. The
         customer may have typed on while the request was in flight. */
      if (field.value === value) noteDirty = false;
      showCartError(null);
      announce(stringFor('note-saved', null));
    });
  }

  /* Carried across a section swap while unsaved. The swap replaces the
     textarea with the server's copy, which is correct for a saved note and
     destroys an unsaved one. */
  function captureNote(container) {
    var field = container.querySelector('[data-cart-note]');
    if (!field || !noteDirty) return function () {};
    var value = field.value;
    return function () {
      var fresh = container.querySelector('[data-cart-note]');
      if (fresh) fresh.value = value;
    };
  }

  // ------------------------------------------------------------ remove line

  function onRemoveClick(event) {
    var link = closestFrom(event, '[data-cart-remove]');
    if (!link) return;
    event.preventDefault();
    var key = link.getAttribute('data-line-key');
    if (!key) {
      window.location.href = link.href; // fall back to Shopify's own removal URL
      return;
    }
    changeLine(key, 0, link);
  }

  // ------------------------------------------------------------ cart opener

  function onOpenerClick(event) {
    var trigger = closestFrom(event, '[data-cart-bubble]');
    if (!trigger || !Drawer.el) return;
    /* Modified clicks are the customer asking for a new tab or a saved link.
       The control is a real link to the cart page and must keep behaving like
       one. */
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button !== 0) return;
    event.preventDefault();
    Drawer.open(trigger);
  }

  // ------------------------------------------------------------------- init

  function init() {
    collectSections();
    Drawer.init();

    /* Set here rather than in the layout's inline no-js/js swap. That swap runs
       whether or not THIS file arrives, and it is what hides the cart form's
       no-JavaScript update control — so if this file failed to load, the
       control would be hidden with nothing to take its place and a typed
       quantity could not be applied at all. The class is this file saying it
       is present, which is the only honest thing to key that on. */
    document.documentElement.classList.add('cart-js');

    document.addEventListener('submit', onAddSubmit);
    document.addEventListener('click', onOpenerClick);
    document.addEventListener('click', onQuantityClick);
    document.addEventListener('click', onRemoveClick);
    document.addEventListener('change', onQuantityChange);
    document.addEventListener('input', onNoteInput);
    document.addEventListener('change', onNoteChange);

    /* One delegated listener per event for the whole document, so markup the
       Section Rendering API swaps in needs no re-binding — which is also what
       keeps this file from leaking listeners on every cart update. */
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // The Theme Editor re-renders sections in place.
  document.addEventListener('shopify:section:load', function (event) {
    collectSections();
    if (event.target.querySelector('[data-cart-drawer]')) Drawer.init();
  });

  /* The drawer is rendered statically from the layout, so a merchant cannot
     remove it and a load almost always follows an unload. "Almost always" is
     not a safe basis for leaving the page fixed-position with its background
     inert, which is what the drawer's open state does, so the teardown runs
     here too. It is idempotent: reset() returns immediately unless the drawer
     is actually open. */
  document.addEventListener('shopify:section:unload', function (event) {
    if (event.target.querySelector('[data-cart-drawer]')) {
      Drawer.reset();
      Drawer.el = null;
    }
  });

  /* Deliberately the only global this file creates, and it holds nothing but
     the drawer, so another script — or a later phase — can open the cart
     without duplicating any of the above. window.Shopify is never touched. */
  window.GodSquad = window.GodSquad || {};
  window.GodSquad.cart = {
    open: function () { Drawer.open(document.activeElement); },
    close: function () { Drawer.close(); },
    refresh: refreshSections
  };
})();
