# -*- coding: utf-8 -*-
"""The cart script's share of the Phase 8 review findings."""
p = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\cart.js"
s = open(p, encoding='utf-8').read()
done = []


def sub(old, new, label):
    global s
    assert old in s, 'NOT FOUND: ' + label
    assert s.count(old) == 1, 'AMBIGUOUS: ' + label
    s = s.replace(old, new, 1)
    done.append(label)


sub("""  /* The two render targets. Both are section files with stable ids: one is
     rendered from the layout, the other is a standalone file that exists only
     to be requested. Shopify allows at most five per request. */
  var SECTIONS = ['cart-drawer', 'cart-icon-bubble'];""",
    """  /* The render targets, built from what is actually on THIS page rather than
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
  }""",
    'render targets are discovered, not assumed')

sub("""  var liveRegion = null;

  function announce(message) {
    if (!message) return;
    if (!liveRegion) liveRegion = document.getElementById('CartStatus');
    if (!liveRegion) return;""",
    """  function announce(message) {
    if (!message) return;
    /* While the drawer is open, aria-modal="true" tells assistive technology to
       treat everything outside it as absent — including the layout's region. The
       drawer carries its own for exactly that window. Looked up each time rather
       than cached, because the drawer does not exist on every page. */
    var liveRegion = null;
    if (Drawer.isOpen) liveRegion = document.querySelector('[data-cart-drawer-status]');
    if (!liveRegion) liveRegion = document.getElementById('CartStatus');
    if (!liveRegion) return;""",
    'announcements reach inside the modal')

sub("""  function sectionParams() {""",
    """  /* A failed cart request reported only to a live region leaves a sighted
     customer watching a quantity snap back with no explanation. Every cart
     surface carries a visible line for it, outside the node the section render
     replaces, so a message survives the re-render that produced it. */
  function showCartError(message) {
    Array.prototype.forEach.call(document.querySelectorAll('[data-cart-error]'), function (box) {
      if (message) {
        box.textContent = message;
        box.hidden = false;
      } else {
        box.textContent = '';
        box.hidden = true;
      }
    });
  }

  function sectionParams() {""",
    'a visible failure line')

sub("""    // The drawer: replace only the part below the heading.
    var drawerHtml = sections['cart-drawer'];
    var drawerTarget = document.querySelector('[data-cart-drawer-inner]');
    if (drawerHtml && drawerTarget) {
      var drawer = sectionInner(drawerHtml);
      var fresh = drawer && drawer.querySelector('[data-cart-drawer-inner]');
      if (fresh) {
        var restore = captureFocusIntent(drawerTarget);
        drawerTarget.innerHTML = fresh.innerHTML;
        restore();
      }
    }
  }""",
    """    // The drawer: replace only the part below the heading.
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
    target.innerHTML = fresh.innerHTML;
    restore();
  }""",
    'the cart page is swapped too')

sub("""  function captureFocusIntent(container) {
    var active = document.activeElement;""",
    """  function captureFocusIntent(container, fallbackId) {
    var active = document.activeElement;""",
    'focus intent takes its own fallback')

sub("""      if (!target) target = document.getElementById('CartDrawerTitle');
      if (target && typeof target.focus === 'function') target.focus();""",
    """      if (!target) target = document.getElementById(fallbackId || 'CartDrawerTitle');
      if (target && typeof target.focus === 'function') target.focus();""",
    'focus falls back to the right heading')

sub("""    init: function () {
      this.el = document.querySelector('[data-cart-drawer]');
      if (!this.el) return;""",
    """    init: function () {
      /* The Theme Editor re-renders a section in place. If the drawer was open
         when that happened, the new node arrived with its hidden attribute
         while isOpen, the open class, the inert siblings and the fixed body all
         stayed behind — leaving the page scroll-locked and the background
         unreachable with no drawer on screen. Tear the old state down first. */
      if (this.isOpen) {
        this.isOpen = false;
        document.documentElement.classList.remove('cart-drawer-open');
        this.setBackgroundInert(false);
        document.removeEventListener('keydown', this.onKeydown, true);
        this.unlockScroll();
        this.opener = null;
      }

      this.el = document.querySelector('[data-cart-drawer]');
      if (!this.el) return;""",
    'a re-rendered drawer cannot strand the page')

sub("""  function setButtonBusy(button, busy) {
    if (!button) return;
    var label = button.querySelector('[data-add-to-cart-label]');
    if (busy) {
      button.setAttribute('aria-busy', 'true');
      button.disabled = true;
      if (label) label.textContent = button.getAttribute('data-label-busy') || label.textContent;
    } else {
      button.removeAttribute('aria-busy');
      button.disabled = false;
      if (label) label.textContent = button.getAttribute('data-label-idle') || label.textContent;
    }
  }""",
    """  /* aria-busy ONLY. Two reasons not to touch `disabled` here.

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
  }""",
    'the add button keeps focus and its sold-out state')

sub("""    var body = new FormData(form);
    var params = sectionParams();
    body.append('sections', params.sections);
    body.append('sections_url', params.sections_url);

    post('cart/add.js', body, true).then(function (result) {""",
    """    var body = new FormData(form);
    var params = sectionParams();
    body.append('sections', params.sections);
    body.append('sections_url', params.sections_url);

    /* Adds share the counter with quantity changes. Two quick-add buttons on
       different product cards are not blocked by the per-button guard above, so
       without this the slower response could paint an older cart over a newer
       one. */
    var seq = ++requestSeq;

    post('cart/add.js', body, true).then(function (result) {""",
    'adds carry a sequence number')

sub("""      /* Sections are rendered after the mutation, so they are applied whether
         or not the call reported success — a 422 for "more than we have" has
         already added what it could, and showing the old cart would be a lie. */
      applySections(result.sections);""",
    """      /* Sections are rendered after the mutation, so they are applied whether
         or not the call reported success — a 422 for "more than we have" has
         already added what it could, and showing the old cart would be a lie.
         Unless a later request has already been answered, in which case this
         markup is older than what is on screen. */
      if (seq === requestSeq) applySections(result.sections);""",
    'a stale add cannot repaint a newer cart')

sub("""    post('cart/change.js', body, false).then(function (result) {
      /* A later request has already been answered; this one's markup is stale
         and applying it would move the quantity backwards. */
      if (seq !== requestSeq) return;

      if (control) control.removeAttribute('aria-busy');
      applySections(result.sections);

      if (!result.ok) {
        announce(result.message || stringFor('error-generic', null));
        if (!result.sections && !result.network) refreshSections();
        return;
      }

      if (quantity === 0) {""",
    """    post('cart/change.js', body, false).then(function (result) {
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

      if (quantity === 0) {""",
    'a superseded change still clears its busy state and reports its error')

sub("""  function init() {
    Drawer.init();
""",
    """  function init() {
    collectSections();
    Drawer.init();
""",
    'sections are collected at init')

sub("""  document.addEventListener('shopify:section:load', function (event) {
    if (event.target.querySelector('[data-cart-drawer]')) Drawer.init();
  });""",
    """  document.addEventListener('shopify:section:load', function (event) {
    collectSections();
    if (event.target.querySelector('[data-cart-drawer]')) Drawer.init();
  });""",
    'a theme-editor re-render recollects them')

# The add path's own error box is the product form's; the cart surfaces have
# their own. Clear both when an add succeeds.
sub("""      if (!result.ok) {
        showFormError(form, result.message || stringFor('error-generic', null));""",
    """      if (!result.ok) {
        showFormError(form, result.message || stringFor('error-generic', null));
        showCartError(null);""",
    'an add failure does not leave a stale cart error')

open(p, 'w', encoding='utf-8', newline='').write(s)
for i, label in enumerate(done, 1):
    print('%2d. %s' % (i, label))
print('cart.js: %d fixes' % len(done))
