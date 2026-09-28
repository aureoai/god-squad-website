# -*- coding: utf-8 -*-
"""Phase 14 — the four cart.js changes.

Written as a script rather than typed into a heredoc because the file is full
of regular expressions and escaped quotes that a shell rewrites.
"""
import io
import os

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
P = os.path.join(THEME, 'assets', 'cart.js')
s = io.open(P, encoding='utf-8').read()
orig = s


def sub(old, new, label):
    global s
    if old not in s:
        raise SystemExit('NOT FOUND: %s' % label)
    if s.count(old) != 1:
        raise SystemExit('AMBIGUOUS (%d): %s' % (s.count(old), label))
    s = s.replace(old, new, 1)
    print('  ok  %s' % label)


# ---------------------------------------------------------------------- (1)
# showCartError broadcast into every [data-cart-error] in the document. The
# only other element that carries that attribute is a quick-add product card,
# so a failed quantity change in the cart printed itself onto product tiles.
sub(
    """/* A failed cart request reported only to a live region leaves a sighted
     customer watching a quantity snap back with no explanation. Every cart
     surface carries a visible line for it, outside the node the section render
     replaces, so a message survives the re-render that produced it. */
  function showCartError(message) {
    Array.prototype.forEach.call(document.querySelectorAll('[data-cart-error]'), function (box) {""",
    """/* A failed cart request reported only to a live region leaves a sighted
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
    Array.prototype.forEach.call(document.querySelectorAll(CART_ERROR_BOXES), function (box) {""",
    'showCartError is scoped to cart surfaces')

# ---------------------------------------------------------------------- (2)
# A form's own error box. product-card.liquid emitted data-cart-error, which
# this never looked at, so a failed quick add was announced to a screen reader
# and shown to nobody. The card now carries data-product-error; accept both so
# a caller that has not been updated still gets its message.
sub(
    """  function showFormError(form, message) {
    var box = form.querySelector('[data-product-error]');""",
    """  function showFormError(form, message) {
    var box = form.querySelector('[data-product-error], [data-cart-error]');""",
    'showFormError accepts either error-box attribute')

# ---------------------------------------------------------------------- (3)
# A debounced quantity change outlived the removal of its own line: Remove sent
# quantity 0 immediately, and 250ms later the pending timer sent the stepped
# quantity for the same key — re-adding the line the customer had just removed.
sub(
    """  function changeLine(key, quantity, origin) {
    if (!key) return;
""",
    """  function changeLine(key, quantity, origin) {
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
""",
    'an immediate change cancels the queued one for that line')

# ---------------------------------------------------------------------- (4)
# The cart note. Shopify's own cart note field, saved through Shopify's own
# /cart/update.js. Nothing is stored client-side.
sub(
    """  // ------------------------------------------------------------ remove line
""",
    """  // -------------------------------------------------------------- the note

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
""",
    'the cart note')

# The swap has to restore the unsaved note as well as the focus.
sub(
    """    var restore = captureFocusIntent(target, fallbackId);
    target.innerHTML = fresh.innerHTML;
    restore();""",
    """    var restore = captureFocusIntent(target, fallbackId);
    var restoreNote = captureNote(target);
    target.innerHTML = fresh.innerHTML;
    restoreNote();
    restore();""",
    'the swap restores an unsaved note')

# And focus has to be able to come back to the note, which is not inside a line.
sub(
    """    var step = active.getAttribute ? active.getAttribute('data-quantity-step') : null;
    var isInput = active.hasAttribute && active.hasAttribute('data-quantity-input');
    var isRemove = active.hasAttribute && active.hasAttribute('data-cart-remove');

    return function () {
      var target = null;
      if (key) {""",
    """    var step = active.getAttribute ? active.getAttribute('data-quantity-step') : null;
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
      if (!target && key) {""",
    'focus returns to the note')

# ---------------------------------------------------------------------- (5)
# A visible success confirmation for the case where no drawer opens.
sub(
    """      var opensDrawer = Drawer.autoOpens() && Drawer.el;
      if (opensDrawer) {
        /* Focus is moving into the drawer, so the addition is NOT announced:
           announcing and moving focus at the same moment makes a screen reader
           talk over itself, and the drawer's heading already says where the
           customer now is. */
        Drawer.open(button);
      } else {
        announce(stringFor('added', null));
      }""",
    """      var opensDrawer = Drawer.autoOpens() && Drawer.el;
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
      }""",
    'a visible confirmation when no drawer opens')

sub(
    """  function showFormError(form, message) {""",
    """  /* Returns true when a confirmation line exists and was filled, so the
     caller knows whether the live region still has to say it. */
  function showFormSuccess(form, message) {
    var box = form.querySelector('[data-product-success]');
    if (!box) return false;
    if (message) {
      box.hidden = false;
      var text = box.querySelector('[data-product-success-text]') || box;
      text.textContent = message;
    } else {
      box.hidden = true;
    }
    return !!message;
  }

  function showFormError(form, message) {""",
    'showFormSuccess')

# A new add clears the previous confirmation, and so does a failure.
sub(
    """    if (button && button.getAttribute('aria-busy') === 'true') return; // no double submits
    showFormError(form, null);""",
    """    if (button && button.getAttribute('aria-busy') === 'true') return; // no double submits
    showFormError(form, null);
    showFormSuccess(form, null);""",
    'a new add clears the previous confirmation')

# ---------------------------------------------------------------------- wire
sub(
    """    document.addEventListener('change', onQuantityChange);
""",
    """    document.addEventListener('change', onQuantityChange);
    document.addEventListener('input', onNoteInput);
    document.addEventListener('change', onNoteChange);
""",
    'note listeners')

io.open(P, 'w', encoding='utf-8').write(s)
print('\ncart.js  %d -> %d bytes' % (len(orig), len(s)))
