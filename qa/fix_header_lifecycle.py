# -*- coding: utf-8 -*-
"""Theme Editor lifecycle for assets/header.js.

Three defects, all of which only appear in the Theme Editor, because only there
is a section re-rendered or removed while the page stays alive:

1. The scroll lock survives a re-render. open() puts `menu-open` on <html>. When
   the merchant changes a header setting with the mobile menu open, the section
   is replaced: the new closure starts with isOpen = false, but the class stays,
   so the page is scroll-locked with no menu on screen and no way to clear it.
   This is the same failure Phase 8 already fixed for the cart drawer, whose
   Drawer.init() tears the old state down first. The header never got it.

2. The focus trap's document-level keydown listener leaks, still bound to the
   detached panel, and keeps intercepting Tab and Escape.

3. matchMedia and scroll listeners accumulate. Every shopify:section:load calls
   initHeader again, which binds a new pair and removes neither. A merchant who
   adjusts header settings twenty times has twenty scroll handlers firing on
   every scroll event. The spec names this one: "do not attach the same event
   listener repeatedly".

The fix records every binding the header makes OUTSIDE its own subtree, and
releases them before re-initialising and on unload. Bindings INSIDE the subtree
(the toggle, the close button, the overlay) need no teardown: they are removed
with the nodes that carry them.
"""
import os

THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'god-squad-theme')
p = os.path.join(THEME, 'assets', 'header.js')
s = open(p, encoding='utf-8').read()

# ---------------------------------------------------------------- 1. registry
OLD_MQ = """    // If the viewport grows past the point where the panel is offered, close it
    // so focus is never left inside a panel that is no longer visible.
    var mq = window.matchMedia('(min-width: 1024px)');
    var onChange = function (event) {
      if (event.matches && isOpen) close(false);
    };
    if (mq.addEventListener) {
      mq.addEventListener('change', onChange);
    } else if (mq.addListener) {
      mq.addListener(onChange);
    }

    // Sticky header: reflect scroll state so the scrim can strengthen once the
    // header no longer sits over the top of a section.
    if (header.classList.contains('header--sticky')) {
      var onScroll = function () {
        header.classList.toggle('header--scrolled', window.scrollY > 8);
      };
      onScroll();
      window.addEventListener('scroll', onScroll, { passive: true });
    }
  }"""

NEW_MQ = """    // If the viewport grows past the point where the panel is offered, close it
    // so focus is never left inside a panel that is no longer visible.
    var mq = window.matchMedia('(min-width: 1024px)');
    var onChange = function (event) {
      if (event.matches && isOpen) close(false);
    };
    if (mq.addEventListener) {
      mq.addEventListener('change', onChange);
      rememberGlobal(function () { mq.removeEventListener('change', onChange); });
    } else if (mq.addListener) {
      mq.addListener(onChange);
      rememberGlobal(function () { mq.removeListener(onChange); });
    }

    // Sticky header: reflect scroll state so the scrim can strengthen once the
    // header no longer sits over the top of a section.
    if (header.classList.contains('header--sticky')) {
      var onScroll = function () {
        header.classList.toggle('header--scrolled', window.scrollY > 8);
      };
      onScroll();
      window.addEventListener('scroll', onScroll, { passive: true });
      rememberGlobal(function () {
        window.removeEventListener('scroll', onScroll, { passive: true });
      });
    }
  }"""
assert s.count(OLD_MQ) == 1, 'mq/scroll block not found'
s = s.replace(OLD_MQ, NEW_MQ, 1)

# --------------------------------------------------- 2. track the active trap
OLD_OPEN = """      document.addEventListener('keydown', onKeydown, true);"""
NEW_OPEN = """      document.addEventListener('keydown', onKeydown, true);
      activeTrap = onKeydown;"""
assert s.count(OLD_OPEN) == 1, 'trap bind not found'
s = s.replace(OLD_OPEN, NEW_OPEN, 1)

OLD_CLOSE = """      document.removeEventListener('keydown', onKeydown, true);"""
NEW_CLOSE = """      document.removeEventListener('keydown', onKeydown, true);
      if (activeTrap === onKeydown) activeTrap = null;"""
assert s.count(OLD_CLOSE) == 1, 'trap unbind not found'
s = s.replace(OLD_CLOSE, NEW_CLOSE, 1)

# ------------------------------------------------- 3. the registry + teardown
OLD_INITALL = """  function initAll() {
    Array.prototype.forEach.call(document.querySelectorAll('[data-header]'), initHeader);
  }"""

NEW_INITALL = """  /* ------------------------------------------------------------------ editor
     Everything the header binds OUTSIDE its own subtree is recorded here, so it
     can be released when the section is re-rendered or removed. Bindings inside
     the subtree — the toggle, the close button, the overlay — are not recorded,
     because they are removed along with the nodes that carry them.

     The theme renders exactly one header, from sections/header-group.json, so a
     single module-level registry is sufficient. If a second header were ever
     added this would need to be keyed per element. */
  var globalBindings = [];
  var activeTrap = null;

  function rememberGlobal(undo) {
    globalBindings.push(undo);
  }

  function releaseGlobals() {
    if (activeTrap) {
      document.removeEventListener('keydown', activeTrap, true);
      activeTrap = null;
    }
    while (globalBindings.length) {
      try { globalBindings.pop()(); } catch (err) { /* already gone */ }
    }
    /* The scroll lock is on <html>, so it outlives any header node. Left behind
       by a re-render with the menu open, it locks the page with no menu on
       screen — which in the Theme Editor is unrecoverable without a reload. */
    document.documentElement.classList.remove('menu-open');
  }

  function initAll() {
    releaseGlobals();
    Array.prototype.forEach.call(document.querySelectorAll('[data-header]'), initHeader);
  }"""
assert s.count(OLD_INITALL) == 1, 'initAll not found'
s = s.replace(OLD_INITALL, NEW_INITALL, 1)

# --------------------------------------------------- 4. the editor event pair
OLD_EVT = """  document.addEventListener('shopify:section:load', function (event) {
    var header = event.target.querySelector('[data-header]');
    if (header) initHeader(header);
  });"""
NEW_EVT = """  document.addEventListener('shopify:section:load', function (event) {
    var header = event.target.querySelector('[data-header]');
    if (!header) return;
    /* Release first. Shopify fires unload before load for a re-render, but not
       every host does, and a second bind is worse than a redundant release. */
    releaseGlobals();
    initHeader(header);
  });

  document.addEventListener('shopify:section:unload', function (event) {
    if (event.target.querySelector('[data-header]')) releaseGlobals();
  });"""
assert s.count(OLD_EVT) == 1, 'section:load handler not found'
s = s.replace(OLD_EVT, NEW_EVT, 1)

open(p, 'w', encoding='utf-8', newline='').write(s)
print('assets/header.js: global bindings are released on re-render and on unload')
