/* ============================================================================
 * GOD SQUAD — facets.js
 * Phase 13. The filter drawer, and nothing else.
 *
 * FILTERING ITSELF NEEDS NO JAVASCRIPT.
 *
 * Shopify's filter parameters are ordinary query-string values, and
 * snippets/facets.liquid renders real checkboxes bound to a real GET form. A
 * customer with no script gets the whole feature: the panel sits in flow above
 * the grid, every group opens with <details>, and Apply submits. This file's
 * only job below --bp-md is to lift that panel into a drawer so it does not
 * push the products down the page.
 *
 * That is why the trigger button ships hidden in the markup and is revealed
 * here. A button that opens a drawer is a lie on a page where this file never
 * ran, and the layout's `js` class is set in the <head> before any of this
 * executes, so it cannot be used to tell the difference.
 *
 * THE SCROLL LOCK IS A CSS CLASS, DELIBERATELY.
 *
 * assets/cart.js locks by setting body.style.position = 'fixed' and restoring
 * window.scrollY on close. That is correct for the cart and it does NOT
 * compose: two owners doing it fight over one recorded scroll position. The
 * header's menu panel locks with a class instead — `.menu-open body { overflow:
 * hidden }` — and two classes compose without either knowing about the other.
 * This follows the header, not the cart.
 *
 * Every binding made outside this section's own subtree is recorded and
 * released as one unit, which is the shape Phase 11 established after the
 * header leaked a listener per re-render.
 * ========================================================================== */

(function () {
  'use strict';

  var FOCUSABLE = 'a[href], button:not([disabled]), input:not([disabled]), ' +
    'select:not([disabled]), textarea:not([disabled]), summary, [tabindex="0"]';

  var globalBindings = [];
  var activeTrap = null;
  var activeClose = null;

  function remember(undo) {
    globalBindings.push(undo);
  }

  function releaseGlobals() {
    if (activeClose) {
      var closeIt = activeClose;
      activeClose = null;
      try { closeIt(); } catch (err) { /* the node may already be detached */ }
    }
    if (activeTrap) {
      document.removeEventListener('keydown', activeTrap, true);
      activeTrap = null;
    }
    while (globalBindings.length) {
      try { globalBindings.pop()(); } catch (err) { /* already gone */ }
    }
    document.documentElement.classList.remove('facets-open');
    Array.prototype.forEach.call(document.querySelectorAll('[data-facets]'), function (p) {
      p.__gsFacetsInit = false;
    });
  }

  function initFacets(panel) {
    /* Idempotent per element. shopify:section:load can fire for a node that was
       not replaced, and binding the trigger twice makes one click toggle twice. */
    if (panel.__gsFacetsInit) return;
    panel.__gsFacetsInit = true;

    var section = panel.closest('.shopify-section') || document;
    var toggle = section.querySelector('[data-facets-toggle]');
    var closeBtn = panel.querySelector('[data-facets-close]');
    if (!toggle) return;

    var isOpen = false;

    /* THE DRAWER EXISTS ONLY BELOW --bp-md, AND THE WIDTH IS THE GATE.

       Every drawer rule in component-facets.css lives inside
       @media (max-width: 767px). `.facets-open body { overflow: hidden }` does
       not — it is top level. So revealing the trigger at a desktop width gave
       the customer a button that locked the page and opened nothing: measured
       at 1440, 1280 and 768, body overflow became hidden, `.facets__bar` (which
       holds the close button) was display:none so closeBtn.focus() was a no-op,
       and the Tab guard below then pulled focus into an in-flow panel with
       Escape as the only exit. That is a keyboard trap, SC 2.1.2.

       The original code set the drawer up unconditionally and registered a
       media-query listener that only ran on CHANGE — so it correctly closed a
       drawer left open by a rotation, and never once evaluated the width the
       page actually loaded at. The fix is to drive both directions from one
       function and call it immediately.

       sections/header.liquid solves the same problem the same way: header.css
       retires the mobile menu with a min-width rule rather than trusting a
       listener. */
    var mq = window.matchMedia('(min-width: 768px)');

    function applyWidth(isDesktop) {
      if (isDesktop) {
        if (isOpen) close(false);
        panel.classList.remove('facets--drawer');
        toggle.hidden = true;
      } else {
        panel.classList.add('facets--drawer');
        toggle.hidden = false;
      }
    }

    applyWidth(mq.matches);
    toggle.setAttribute('aria-expanded', 'false');
    /* Truthful only now that the panel can actually be controlled. */
    if (!panel.id) panel.id = 'FacetsPanel';
    toggle.setAttribute('aria-controls', panel.id);

    function onKeydown(event) {
      if (event.key === 'Escape' || event.key === 'Esc') {
        event.preventDefault();
        close(true);
        return;
      }
      if (event.key !== 'Tab') return;
      var items = Array.prototype.filter.call(
        panel.querySelectorAll(FOCUSABLE),
        function (el) { return el.offsetParent !== null || el === document.activeElement; }
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
      } else if (!panel.contains(document.activeElement)) {
        event.preventDefault();
        first.focus();
      }
    }

    function open() {
      if (isOpen) return;
      /* Belt and braces. applyWidth already hides the trigger above --bp-md, so
         this should be unreachable — but open() is what locks the page, and a
         second guard on the one function that can strand a customer costs a
         comparison. */
      if (mq.matches) return;
      isOpen = true;
      /* Reopened while the previous close was still sliding out. .is-open
         carries visibility on its own, so this only stops a late transitionend
         or the 500ms fallback from finding a stale class to act on. */
      panel.classList.remove('is-closing');
      panel.classList.add('is-open');
      document.documentElement.classList.add('facets-open');
      toggle.setAttribute('aria-expanded', 'true');
      document.addEventListener('keydown', onKeydown, true);
      activeTrap = onKeydown;
      activeClose = function () { close(false); };
      var target = closeBtn || panel.querySelector(FOCUSABLE);
      if (target) target.focus();
    }

    /* THE EXIT SLIDE HAS TO BE HELD VISIBLE.

       component-facets.css hides the closed drawer with `visibility: hidden`,
       and visibility is not in its transition list — so dropping .is-open used
       to hide the panel in the same frame the transform began, and the slide
       out never rendered. PHASE-2 §21 line 1725 specifies drawer entry AND
       exit, and assets/cart.js already does this for the cart drawer.

       .is-closing keeps it visible until the transform lands. Removal is driven
       by transitionend with a timeout fallback, because transitionend does not
       fire if the element is display:none'd, the media query flips mid-slide,
       or the transition is interrupted — and a drawer stuck visible would sit
       over the page. Under reduced motion the durations collapse to 1ms and
       there is nothing to wait for, so it is removed at once. */
    function settleClosed() {
      if (isOpen) return;              /* reopened mid-slide; open() owns it now */
      panel.classList.remove('is-closing');
    }

    function close(returnFocus) {
      if (!isOpen) return;
      isOpen = false;
      panel.classList.remove('is-open');
      document.documentElement.classList.remove('facets-open');
      toggle.setAttribute('aria-expanded', 'false');
      document.removeEventListener('keydown', onKeydown, true);
      if (activeTrap === onKeydown) activeTrap = null;
      activeClose = null;

      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        panel.classList.remove('is-closing');
      } else {
        panel.classList.add('is-closing');
        var done = function (event) {
          /* Only the panel's own transform, not a child's colour fade. */
          if (event && (event.target !== panel || event.propertyName !== 'transform')) return;
          panel.removeEventListener('transitionend', done);
          window.clearTimeout(timer);
          settleClosed();
        };
        var timer = window.setTimeout(function () {
          panel.removeEventListener('transitionend', done);
          settleClosed();
        }, 500);
        panel.addEventListener('transitionend', done);
      }

      if (returnFocus) toggle.focus();
    }

    var onToggle = function () { if (isOpen) { close(true); } else { open(); } };
    toggle.addEventListener('click', onToggle);
    remember(function () { toggle.removeEventListener('click', onToggle); });

    if (closeBtn) {
      var onClose = function () { close(true); };
      closeBtn.addEventListener('click', onClose);
      remember(function () { closeBtn.removeEventListener('click', onClose); });
    }

    /* Crossing the breakpoint in either direction, which a rotation or a
       resized window does. Re-uses the same function as the initial evaluation,
       so the two can never disagree. */
    var onChange = function (event) { applyWidth(event.matches); };
    if (mq.addEventListener) {
      mq.addEventListener('change', onChange);
      remember(function () { mq.removeEventListener('change', onChange); });
    } else if (mq.addListener) {
      mq.addListener(onChange);
      remember(function () { mq.removeListener(onChange); });
    }
  }

  function initAll() {
    releaseGlobals();
    Array.prototype.forEach.call(document.querySelectorAll('[data-facets]'), initFacets);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }

  document.addEventListener('shopify:section:load', function (event) {
    if (!event.target.querySelector('[data-facets]')) return;
    releaseGlobals();
    initAll();
  });

  document.addEventListener('shopify:section:unload', function (event) {
    if (event.target.querySelector('[data-facets]')) releaseGlobals();
  });
})();
