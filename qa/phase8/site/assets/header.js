/* GOD SQUAD — header behaviour
 * Phase 4.
 *
 * Answers PHASE-1-WEBSITE-AUDIT.md NAV-01 and A11Y-01: the prototype's
 * hamburger was a <span> with no role, no tabindex and no handler, so below
 * 900px there was no way to reach any destination. This gives the menu a real
 * button, a real panel, and the keyboard contract a disclosure owes:
 *
 *   aria-expanded reflects state
 *   Escape closes and returns focus to the trigger
 *   focus moves into the panel on open and is trapped while it is open
 *   the background is inert to screen readers and to pointer input
 *   the panel closes if the viewport grows past the breakpoint while open
 *
 * No framework, no dependency. Phase 2 section 36 asks the system to stay
 * lightweight, and a disclosure does not need more than this.
 */
(function () {
  'use strict';

  var FOCUSABLE = [
    'a[href]',
    'button:not([disabled])',
    'input:not([disabled]):not([type="hidden"])',
    'select:not([disabled])',
    'textarea:not([disabled])',
    '[tabindex]:not([tabindex="-1"])'
  ].join(',');

  function initHeader(header) {
    /* Idempotent per element. shopify:section:load can fire for a node that
       was NOT replaced, and binding the toggle a second time makes one click
       open the menu twice — which installs two focus traps and leaves one
       behind on close. Marked on the node itself, so a genuine re-render
       (a new node, no mark) still initialises normally. */
    if (header.__gsHeaderInit) return;
    header.__gsHeaderInit = true;

    var toggle = header.querySelector('[data-menu-toggle]');
    var panel = header.querySelector('[data-menu-panel]');
    var overlay = header.querySelector('[data-menu-overlay]');
    var closeBtn = header.querySelector('[data-menu-close]');
    if (!toggle || !panel) return;

    var isOpen = false;
    var lastFocused = null;

    function focusable() {
      return Array.prototype.filter.call(
        panel.querySelectorAll(FOCUSABLE),
        function (el) { return el.offsetParent !== null; }
      );
    }

    function open() {
      if (isOpen) return;
      isOpen = true;
      lastFocused = document.activeElement;

      panel.hidden = false;
      if (overlay) overlay.hidden = false;
      // Force a frame so the transition has a start state to animate from.
      void panel.offsetWidth;

      header.classList.add('header--menu-open');
      document.documentElement.classList.add('menu-open');
      toggle.setAttribute('aria-expanded', 'true');

      var first = focusable()[0];
      if (first) first.focus();

      document.addEventListener('keydown', onKeydown, true);
      activeTrap = onKeydown;
      activeClose = function () { close(false); };
    }

    function close(returnFocus) {
      if (!isOpen) return;
      isOpen = false;

      header.classList.remove('header--menu-open');
      document.documentElement.classList.remove('menu-open');
      toggle.setAttribute('aria-expanded', 'false');

      document.removeEventListener('keydown', onKeydown, true);
      if (activeTrap === onKeydown) activeTrap = null;
      activeClose = null;

      var done = function () {
        if (!isOpen) {
          panel.hidden = true;
          if (overlay) overlay.hidden = true;
        }
        panel.removeEventListener('transitionend', done);
      };

      // Respect a reduced-motion preference: hide immediately rather than
      // waiting for a transition that will not run.
      var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (reduced) {
        done();
      } else {
        panel.addEventListener('transitionend', done);
        // Fallback in case the transition never fires.
        window.setTimeout(done, 400);
      }

      // Focus returns to the control that opened the panel. Prefer whatever was
      // focused at open time, but only if it is still in the document and is a
      // real target; otherwise fall back to the toggle itself. Trusting
      // lastFocused alone strands focus inside the closed panel whenever the
      // panel was opened without the toggle being focused first.
      if (returnFocus !== false) {
        var target = toggle;
        if (
          lastFocused &&
          typeof lastFocused.focus === 'function' &&
          lastFocused !== document.body &&
          document.contains(lastFocused)
        ) {
          target = lastFocused;
        }
        target.focus();
      }
    }

    function onKeydown(event) {
      if (event.key === 'Escape' || event.key === 'Esc') {
        event.preventDefault();
        close(true);
        return;
      }
      if (event.key !== 'Tab') return;

      var items = focusable();
      if (items.length === 0) {
        event.preventDefault();
        return;
      }
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

    /* Recorded like the rest. These live inside the section's own subtree and
       would go with it on a real re-render, but a host that fires
       unload+load for the SAME node would otherwise double-bind them. */
    var onToggle = function () { if (isOpen) { close(true); } else { open(); } };
    toggle.addEventListener('click', onToggle);
    remember(function () { toggle.removeEventListener('click', onToggle); });

    if (closeBtn) {
      var onCloseBtn = function () { close(true); };
      closeBtn.addEventListener('click', onCloseBtn);
      remember(function () { closeBtn.removeEventListener('click', onCloseBtn); });
    }
    if (overlay) {
      var onOverlay = function () { close(true); };
      overlay.addEventListener('click', onOverlay);
      remember(function () { overlay.removeEventListener('click', onOverlay); });
    }

    /* ------------------------------------------------------ search panel
       Phase 13. An upgrade of the existing link, not a replacement for it: the
       markup still ships <a href="/search">, so with no script the control
       navigates to a complete search page. Only when this runs does it become
       a disclosure, and only then are the ARIA attributes that claim so applied.

       It reuses this file's binding registry, so it is released by the same
       teardown that Phase 11 added for the menu — one place that knows what the
       header has bound outside its own subtree. */
    var searchTrigger = header.querySelector('[data-search-trigger]');
    var searchPanel = header.querySelector('[data-search-panel]');

    if (searchTrigger && searchPanel) {
      var searchInput = searchPanel.querySelector('[data-search-input]');
      var searchClose = searchPanel.querySelector('[data-search-close]');
      var searchOpen = false;

      searchTrigger.setAttribute('aria-haspopup', 'dialog');
      searchTrigger.setAttribute('aria-expanded', 'false');
      searchTrigger.setAttribute('aria-controls', searchPanel.id || 'HeaderSearch');

      var onSearchKeydown = function (event) {
        if (event.key !== 'Escape' && event.key !== 'Esc') return;
        event.preventDefault();
        closeSearch(true);
      };

      var openSearch = function () {
        if (searchOpen) return;
        searchOpen = true;
        searchPanel.hidden = false;
        header.classList.add('header--search-open');
        searchTrigger.setAttribute('aria-expanded', 'true');
        document.addEventListener('keydown', onSearchKeydown, true);
        activeSearchTrap = onSearchKeydown;
        activeSearchClose = function () { closeSearch(false); };
        if (searchInput) searchInput.focus();
      };

      closeSearch = function (returnFocus) {
        if (!searchOpen) return;
        searchOpen = false;
        searchPanel.hidden = true;
        header.classList.remove('header--search-open');
        searchTrigger.setAttribute('aria-expanded', 'false');
        document.removeEventListener('keydown', onSearchKeydown, true);
        if (activeSearchTrap === onSearchKeydown) activeSearchTrap = null;
        activeSearchClose = null;
        if (returnFocus) searchTrigger.focus();
      };

      var onSearchTrigger = function (event) {
        /* A modified click is the customer asking for a new tab. The control is
           a real link to the search page and must keep behaving like one — the
           same guard assets/cart.js applies to the cart bubble. */
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey ||
            event.button !== 0) return;
        event.preventDefault();
        if (searchOpen) { closeSearch(true); } else { openSearch(); }
      };
      searchTrigger.addEventListener('click', onSearchTrigger);
      remember(function () {
        searchTrigger.removeEventListener('click', onSearchTrigger);
      });

      if (searchClose) {
        var onSearchCloseClick = function () { closeSearch(true); };
        searchClose.addEventListener('click', onSearchCloseClick);
        remember(function () {
          searchClose.removeEventListener('click', onSearchCloseClick);
        });
      }
    }

    // If the viewport grows past the point where the panel is offered, close it
    // so focus is never left inside a panel that is no longer visible.
    var mq = window.matchMedia('(min-width: 1024px)');
    var onChange = function (event) {
      if (event.matches && isOpen) close(false);
    };
    if (mq.addEventListener) {
      mq.addEventListener('change', onChange);
      remember(function () { mq.removeEventListener('change', onChange); });
    } else if (mq.addListener) {
      mq.addListener(onChange);
      remember(function () { mq.removeListener(onChange); });
    }

    // Sticky header: reflect scroll state so the scrim can strengthen once the
    // header no longer sits over the top of a section.
    if (header.classList.contains('header--sticky')) {
      var onScroll = function () {
        header.classList.toggle('header--scrolled', window.scrollY > 8);
      };
      onScroll();
      window.addEventListener('scroll', onScroll, { passive: true });
      remember(function () {
        window.removeEventListener('scroll', onScroll, { passive: true });
      });
    }
  }

  /* ------------------------------------------------------------------ editor
     Everything the header binds OUTSIDE its own subtree is recorded here, so it
     can be released when the section is re-rendered or removed. Bindings inside
     the subtree — the toggle, the close button, the overlay — are not recorded,
     because they are removed along with the nodes that carry them.

     The theme renders exactly one header, from sections/header-group.json, so a
     single module-level registry is sufficient. If a second header were ever
     added this would need to be keyed per element. */
  var globalBindings = [];
  var activeTrap = null;
  var activeClose = null;
  /* The search panel's equivalents. Separate slots rather than shared ones,
     because the menu and the search panel can be torn down independently. */
  var activeSearchTrap = null;
  var activeSearchClose = null;
  var closeSearch = null;

  function remember(undo) {
    globalBindings.push(undo);
  }

  function releaseGlobals() {
    /* Close first, so the teardown leaves a coherent state rather than a panel
       that is still open on screen with its scroll lock already released. */
    if (activeClose) {
      var closeIt = activeClose;
      activeClose = null;
      try { closeIt(); } catch (err) { /* the node may already be detached */ }
    }
    if (activeSearchClose) {
      var closeSearchIt = activeSearchClose;
      activeSearchClose = null;
      try { closeSearchIt(); } catch (err) { /* already detached */ }
    }
    if (activeTrap) {
      document.removeEventListener('keydown', activeTrap, true);
      activeTrap = null;
    }
    if (activeSearchTrap) {
      document.removeEventListener('keydown', activeSearchTrap, true);
      activeSearchTrap = null;
    }
    while (globalBindings.length) {
      try { globalBindings.pop()(); } catch (err) { /* already gone */ }
    }
    /* Clear the per-node guard. Every binding has just been removed, so a node
       that survives the teardown must be allowed to initialise again — otherwise
       an unload+load pair on the SAME node would leave it wired to nothing. */
    Array.prototype.forEach.call(document.querySelectorAll('[data-header]'), function (h) {
      h.__gsHeaderInit = false;
    });
    /* The scroll lock is on <html>, so it outlives any header node. Left behind
       by a re-render with the menu open, it locks the page with no menu on
       screen — which in the Theme Editor is unrecoverable without a reload. */
    document.documentElement.classList.remove('menu-open');
  }

  function initAll() {
    releaseGlobals();
    Array.prototype.forEach.call(document.querySelectorAll('[data-header]'), initHeader);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }

  // The Theme Editor re-renders sections in place; re-bind when it does.
  document.addEventListener('shopify:section:load', function (event) {
    var header = event.target.querySelector('[data-header]');
    if (!header) return;
    /* Release first. Shopify fires unload before load for a re-render, but not
       every host does, and a second bind is worse than a redundant release. */
    releaseGlobals();
    initHeader(header);
  });

  document.addEventListener('shopify:section:unload', function (event) {
    if (event.target.querySelector('[data-header]')) releaseGlobals();
  });
})();
