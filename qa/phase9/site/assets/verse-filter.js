/* ============================================================================
   GOD SQUAD — verse-filter.js

   The category chips on the Explore Verses band.

   WHAT IT DOES, IN ORDER OF IMPORTANCE.

   1. It REVEALS the chip row. The markup ships it hidden. Filtering is client
      side, so without this file it cannot happen, and a row of controls that
      does nothing is worse than no row. Nothing else on the band depends on
      script: with JavaScript off the page is every verse, correctly laid out,
      with no dead controls.

   2. It filters by setting the `hidden` attribute on cards, never by removing
      them. Phase 8 recorded the rule as "never intercept a surface you cannot
      re-render" — this script owns no markup, so it must be able to put the
      grid back exactly as Liquid rendered it, and an attribute toggle is
      reversible where a detach is not.

   3. It moves aria-pressed and announces the new count.

   WHY `hidden` NEEDS A CSS RULE. `[hidden] { display: none }` lives in the user
   agent stylesheet, and any author `display` on the same element beats it
   whatever the specificity. The grid's children are flex/grid items with an
   author display, so section-verse-index.css carries an explicit
   `.verse-card[hidden] { display: none }`. Without it this script would appear
   to do nothing at all. The theme has hit that cascade four times; this is the
   fifth place it is handled deliberately rather than discovered.

   THEME EDITOR. Three lifecycle events matter and all three are handled:
     shopify:section:load    the section was re-rendered; wire the new DOM
     shopify:block:select    the merchant clicked a verse in the sidebar. If it
                             is filtered out it is display:none, so the editor
                             cannot outline or scroll to it — reset to All first
     shopify:section:select  the merchant selected the whole section; reset, so
                             they see everything they are about to edit
   ========================================================================== */
(function () {
  'use strict';

  var ALL = 'all';

  function chipsOf(root) {
    return Array.prototype.slice.call(root.querySelectorAll('[data-verse-chip]'));
  }

  function cardsOf(root) {
    var grid = root.querySelector('[data-verse-grid]');
    return grid ? Array.prototype.slice.call(grid.children) : [];
  }

  /* Apply a category. Returns how many cards are showing. */
  function apply(root, category) {
    var shown = 0;
    cardsOf(root).forEach(function (card) {
      var cat = card.getAttribute('data-verse-category');
      var show = category === ALL || cat === category;
      if (show) {
        card.removeAttribute('hidden');
        shown += 1;
      } else {
        card.setAttribute('hidden', '');
      }
    });

    chipsOf(root).forEach(function (chip) {
      var on = chip.getAttribute('data-verse-chip') === category;
      chip.setAttribute('aria-pressed', on ? 'true' : 'false');
    });

    root.setAttribute('data-verse-active', category);
    return shown;
  }

  /* The count, spoken. The number is placed into a flat locale string carrying
     a literal [count] placeholder, which is how assets/cart.js already does it
     (locales/en.default.json "quantity": "Quantity: [count]"): pluralisation
     that lives in the locale file can be translated, pluralisation assembled in
     JavaScript cannot.

     Cleared first, then written on the next turn. A region whose text is
     replaced in one go with a string it may already hold announces nothing,
     which is the same trap announce() in cart.js documents. */
  function announce(root, shown) {
    var region = root.querySelector('[data-verse-status]');
    if (!region) return;
    var template = region.getAttribute('data-verse-status') || '';
    var message = template
      ? template.replace('[count]', String(shown))
      : String(shown);
    region.textContent = '';
    window.setTimeout(function () {
      region.textContent = message;
    }, 0);
  }

  function init(root) {
    if (!root || root.__gsVerseFilter) return;
    var filter = root.querySelector('[data-verse-filter]');
    var grid = root.querySelector('[data-verse-grid]');
    if (!filter || !grid) return;
    root.__gsVerseFilter = true;

    /* The reveal. Until this line the row does not exist for anyone. */
    filter.removeAttribute('hidden');

    filter.addEventListener('click', function (event) {
      var chip = event.target.closest ? event.target.closest('[data-verse-chip]') : null;
      if (!chip || !filter.contains(chip)) return;
      var category = chip.getAttribute('data-verse-chip');
      if (root.getAttribute('data-verse-active') === category) return;
      announce(root, apply(root, category));
    });

    apply(root, ALL);
  }

  function initAll(scope) {
    var roots = (scope || document).querySelectorAll('.verse-index');
    Array.prototype.forEach.call(roots, init);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { initAll(); });
  } else {
    initAll();
  }

  /* ---------------------------------------------------------- Theme Editor */

  document.addEventListener('shopify:section:load', function (event) {
    initAll(event.target);
  });

  /* A filtered-out card is display:none, so the editor cannot outline it or
     scroll to it and the merchant sees nothing happen when they click it in the
     sidebar. Resetting to All first makes every block reachable. */
  function resetFor(node) {
    if (!node) return;
    var root = node.closest ? node.closest('.verse-index') : null;
    if (!root) return;
    if (root.getAttribute('data-verse-active') !== ALL) apply(root, ALL);
  }

  document.addEventListener('shopify:block:select', function (event) {
    resetFor(event.target);
  });

  document.addEventListener('shopify:section:select', function (event) {
    resetFor(event.target);
  });
})();
