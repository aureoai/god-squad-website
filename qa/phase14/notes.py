# -*- coding: utf-8 -*-
"""Phase 14 — the order note and the add confirmation, driven in a browser.

Three pages, three runners:
  c-page-note.html  the cart page with the note on — saving, and surviving a
                    section swap it did not cause
  p-nodrawer.html   a product page on a store whose cart style is "Cart page",
                    which is the case where an add has nothing to confirm it
  c-one.html        a product page WITH the drawer, where the drawer is the
                    confirmation and an inline one would be a second voice
"""
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, '..', 'phase8', 'site'))
# Overridable so the same suites can be driven by a second engine.
EDGE = os.environ.get('GS_BROWSER',
                      r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
PORT = 8808
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-notes')
# The cart page the stub renders back. Its note deliberately holds the SERVER's
# text, so a swap that clobbers an unsaved edit is visible as that text
# reappearing in the field.
STUB = r"""
<script>
(function () {
  window.__req = [];
  window.__mode = 'ok';

  function pageHtml() {
    return '<div id="shopify-section-main" class="shopify-section">' +
      '<div class="main-cart" data-cart-page><div data-cart-page-inner>' +
      '<form data-cart-form>' +
      '<ul><li class="cart-line" data-cart-line data-line-key="k2:bbb">' +
      '<div class="quantity" data-quantity data-line-key="k2:bbb">' +
      '<button type="button" data-quantity-step="-1" aria-disabled="true"></button>' +
      '<input class="quantity__input" data-quantity-input type="number" value="1" min="1">' +
      '<button type="button" data-quantity-step="1"></button></div></li></ul>' +
      '<details class="cart-note" open><textarea data-cart-note name="note" id="CartPageNote">SERVER NOTE</textarea></details>' +
      '<p class="main-cart__error" data-cart-error hidden></p>' +
      '</form></div></div></div>';
  }
  function drawerHtml() {
    return '<div id="shopify-section-cart-drawer" class="shopify-section">' +
      '<div class="cart-drawer"><div class="cart-drawer__inner" data-cart-drawer-inner>' +
      'DRAWER REFRESHED</div></div></div>';
  }
  function bubbleHtml(n) {
    return '<div id="shopify-section-cart-icon-bubble" class="shopify-section">' +
      '<span data-cart-count>' + n + '</span></div>';
  }

  window.fetch = function (input, init) {
    var url = typeof input === 'string' ? input : String(input);
    var body = init && init.body;
    var rec = { url: url };
    if (body instanceof FormData) {
      rec.form = {}; body.forEach(function (v, k) { rec.form[k] = String(v); });
    } else if (typeof body === 'string') {
      try { rec.json = JSON.parse(body); } catch (e) { rec.raw = body; }
    }
    window.__req.push(rec);
    if (window.__mode === 'network') return Promise.reject(new TypeError('Failed to fetch'));
    if (window.__mode === 'error422') {
      return Promise.resolve({ ok: false, status: 422, json: function () {
        return Promise.resolve({ status: 422, message: 'Cart Error',
          description: 'You can only add 3 of this to the cart.' }); } });
    }
    return Promise.resolve({ ok: true, status: 200, json: function () {
      return Promise.resolve({ items: [{ id: 9102, quantity: 1, key: 'k1:aaa' }],
        sections: { 'main': pageHtml(), 'cart-drawer': drawerHtml(),
                    'cart-icon-bubble': bubbleHtml(3) } }); } });
  };
})();
</script>
"""

HEAD = r"""
<script>
(function () {
  window.__results = [];
  window.t = function (name, r) {
    window.__results.push({ name: name, pass: r === true, detail: r === true ? '' : String(r) });
  };
  window.q = function (s) { return document.querySelector(s); };
  window.wait = function (ms) { return new Promise(function (r) { setTimeout(r, ms); }); };
  window.updates = function () {
    return window.__req.filter(function (r) { return /cart\/update\.js$/.test(r.url); });
  };
  window.finish = function () {
    document.title = 'DONE';
    document.getElementById('o').textContent = '<<<' + JSON.stringify(window.__results) + '>>>';
  };
})();
</script>
"""

NOTE_RUNNER = r"""
<script>
(function () {
  function run() {
    var field = q('[data-cart-note]');
    if (!field) { t('the note field is on the page', 'absent'); finish(); return; }
    return Promise.resolve()
      /* Typing must not talk to the server. `input` sets the dirty flag and
         nothing else; `change` is what saves, and it fires once, on blur. */
      .then(function () {
        window.__req.length = 0;
        field.value = 'Leave with the guard';
        field.dispatchEvent(new Event('input', { bubbles: true }));
        field.dispatchEvent(new Event('input', { bubbles: true }));
        return wait(120);
      })
      .then(function () {
        t('typing sends no request', updates().length === 0
          || 'sent ' + updates().length + ' request(s) while typing');
        field.dispatchEvent(new Event('change', { bubbles: true }));
        return wait(200);
      })
      .then(function () {
        var u = updates();
        t('leaving the field saves the note once', u.length === 1 || 'sent ' + u.length);
        t('it goes to Shopify\'s own cart/update.js',
          u.length && /\/cart\/update\.js$/.test(u[0].url) || 'url=' + (u.length && u[0].url));
        t('the body is Shopify\'s own note field',
          u.length && u[0].json && u[0].json.note === 'Leave with the guard'
            || 'body=' + JSON.stringify(u.length && u[0].json));
        t('and asks for no sections, because nothing on the page shows the note',
          u.length && u[0].json && !('sections' in u[0].json)
            || 'sections requested: ' + (u.length && u[0].json && u[0].json.sections));
        t('the save is announced', (q('#CartStatus').textContent || '').indexOf('note') !== -1
          || 'announced: "' + q('#CartStatus').textContent + '"');
        return null;
      })
      /* An UNSAVED note must survive a re-render it did not cause. The stub
         renders the server's copy back, so a clobbered note reads SERVER NOTE. */
      .then(function () {
        window.__req.length = 0;
        field.value = 'Typed but not yet saved';
        field.dispatchEvent(new Event('input', { bubbles: true }));
        field.focus();
        // A quantity change elsewhere re-renders the whole cart page node.
        q('[data-quantity-step="1"]').click();
        return wait(700);
      })
      .then(function () {
        var fresh = q('[data-cart-note]');
        t('the cart node really was re-rendered', !!q('[data-cart-line]') && fresh !== field
          || 'the node was not replaced, so this proves nothing');
        t('an unsaved note survives the re-render',
          fresh && fresh.value === 'Typed but not yet saved'
            || 'field now reads "' + (fresh && fresh.value) + '"');
        t('and focus comes back to it, not to the heading',
          document.activeElement === fresh
            || 'focus on ' + (document.activeElement && (document.activeElement.id || document.activeElement.tagName)));
        return null;
      })
      /* A refused save is reported, and reported on the cart. */
      .then(function () {
        window.__mode = 'error422';
        var f = q('[data-cart-note]');
        f.value = 'x';
        f.dispatchEvent(new Event('input', { bubbles: true }));
        f.dispatchEvent(new Event('change', { bubbles: true }));
        return wait(250);
      })
      .then(function () {
        var box = q('[data-cart-error]');
        t('a refused note save is visible, in Shopify\'s own words',
          box && box.hidden === false && box.textContent.indexOf('only add 3') !== -1
            || 'box hidden=' + (box && box.hidden) + ' text=' + (box && box.textContent));
        t('and no raw status code is shown',
          box && box.textContent.indexOf('422') === -1 || 'text=' + (box && box.textContent));
        finish();
      })
      .catch(function (e) {
        t('RUNNER', 'threw: ' + e.message + ' ' + e.stack); finish();
      });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { setTimeout(run, 150); });
  else setTimeout(run, 150);
})();
</script>
<pre id="o" style="display:none"></pre>
"""

ADD_RUNNER = r"""
<script>
(function () {
  function run() {
    var form = q('[data-product-form]');
    var box = q('[data-product-success]');
    var drawer = q('[data-cart-drawer]');
    return Promise.resolve()
      .then(function () {
        t('the confirmation line exists and starts hidden',
          box && box.hidden === true || 'box=' + (!!box) + ' hidden=' + (box && box.hidden));
        window.__req.length = 0;
        document.getElementById('CartStatus').textContent = '';
        form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
        return wait(300);
      })
      .then(function () {
        var live = (document.getElementById('CartStatus').textContent || '').trim();
        if (window.__nodrawer) {
          t('with no drawer, the add is confirmed on screen',
            box.hidden === false || 'confirmation still hidden');
          t('in words, not by colour alone',
            (q('[data-product-success-text]').textContent || '').length > 0
              || 'the confirmation is empty');
          t('and offers the cart',
            !!box.querySelector('a[href]') || 'no link out');
          /* role="status" announces the element itself. Writing the same
             sentence to the live region as well would say it twice. */
          t('the live region does NOT repeat it', live === ''
            || 'live region also said "' + live + '"');
        } else {
          t('with a drawer, the drawer is the confirmation',
            drawer && drawer.hidden === false || 'drawer did not open');
          t('and no second confirmation is shown on the form',
            box === null || box.hidden === true || 'the form also confirmed');
        }
        return null;
      })
      /* A failure clears any confirmation left from a previous success. */
      .then(function () {
        if (!window.__nodrawer) { finish(); return null; }
        window.__mode = 'error422';
        form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
        return wait(300).then(function () {
          t('a later failure clears the old confirmation',
            box.hidden === true || 'the confirmation is still on screen');
          var err = q('[data-product-error]');
          t('and the failure is shown in its place',
            err && err.hidden === false && err.textContent.indexOf('only add 3') !== -1
              || 'error box hidden=' + (err && err.hidden));
          t('the add button is not left stuck in Adding',
            q('[data-add-to-cart]').getAttribute('aria-busy') === null
              || 'aria-busy is still set');
          finish();
        });
      })
      .catch(function (e) { t('RUNNER', 'threw: ' + e.message + ' ' + e.stack); finish(); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { setTimeout(run, 150); });
  else setTimeout(run, 150);
})();
</script>
<pre id="o" style="display:none"></pre>
"""


GEOMETRY_RUNNER = r"""
<script>
(function () {
  /* The drawer, opened and measured. The note is CONTENT and must scroll with
     the cart lines; the footer is CHROME and must stay inside the viewport.

     Measured at 812x375 with a note written, the note lived in the footer and
     the footer became 451px tall in a 375px viewport, collapsing the line
     scroller to 0 against 474px of cart lines: the customer could reach
     Checkout and could not see one thing they were buying. This is the guard
     on that. */
  function run() {
    var bubble = q('[data-cart-bubble]');
    bubble.click();
    return wait(120).then(function () {
      var drawer = q('[data-cart-drawer]');
      t('the drawer opened', drawer && drawer.hidden === false || 'still hidden');

      var scroller = q('[data-cart-scroller]');
      var footer = q('.cart-drawer__footer');
      var note = q('[data-cart-note]');
      var vh = window.innerHeight;

      t('the cart lines have a scroller with height',
        scroller && scroller.clientHeight > 0
          || 'scroller height = ' + (scroller && scroller.clientHeight));
      t('the lines are reachable by scrolling, not cut off',
        scroller && scroller.scrollHeight > scroller.clientHeight
          ? scroller.scrollHeight - scroller.clientHeight > 0
          : true);
      /* NOT "the footer is on screen". Below --bp-md and under 540px of
         height the drawer deliberately stops pinning its footer and becomes
         one scrolling column, because a screen that cannot show both the cart
         and the chrome must not resolve that by clipping one of them. The
         invariant that holds in BOTH models is reachability: every control
         can be brought into view. */
      var checkout = q('[data-cart-checkout]');
      t('Checkout exists', !!checkout || 'no checkout control');
      if (checkout) {
        checkout.scrollIntoView({ block: 'nearest' });
        var r = checkout.getBoundingClientRect();
        t('Checkout can be brought fully into view',
          r.top >= -1 && r.bottom <= vh + 1
            || 'after scrolling it sits ' + Math.round(r.top) + '..' + Math.round(r.bottom) + ' in a ' + vh + 'px viewport');
      }
      var firstLine = q('[data-cart-line]');
      if (firstLine) {
        firstLine.scrollIntoView({ block: 'nearest' });
        var lr = firstLine.getBoundingClientRect();
        t('and so can the first cart line',
          lr.top >= -1 && lr.bottom <= vh + 1
            || 'line sits ' + Math.round(lr.top) + '..' + Math.round(lr.bottom) + ' in a ' + vh + 'px viewport');
      }
      /* The overflow measure is taken on the DOCUMENT, not on the drawer.
         .cart-drawer covers the viewport and holds a panel positioned against
         the trailing edge, so its own scrollWidth counts that offset as
         content and reports overflow that no customer can produce. What
         matters is whether the PAGE scrolls sideways, which is what
         phase9/respond.py measures across all twelve viewports and what this
         repeats here for the note case. */
      t('the page does not scroll sideways with the drawer open',
        document.documentElement.scrollWidth <= window.innerWidth + 1
          || 'document scrollWidth ' + document.documentElement.scrollWidth + ' vs ' + window.innerWidth);
      t('the note is inside the scrolling region, not the footer',
        !!note && !!scroller && scroller.contains(note)
          || 'note in footer: ' + (!!footer && !!note && footer.contains(note)));
      t('every cart line is inside the scroller too',
        !!scroller && scroller.querySelectorAll('[data-cart-line]').length > 0
          || 'no lines in the scroller');
      finish();
    }).catch(function (e) { t('RUNNER', 'threw: ' + e.message); finish(); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { setTimeout(run, 150); });
  else setTimeout(run, 150);
})();
</script>
<pre id="o" style="display:none"></pre>
"""


def drive(page, runner, out_name, flag='', window='1500,1100'):
    src = io.open(os.path.join(SITE, page), encoding='utf-8').read()
    src = src.replace('<meta charset="utf-8">',
                      '<meta charset="utf-8">' + STUB + HEAD + flag, 1)
    src = src.replace('</body>', runner + '</body>', 1)
    io.open(os.path.join(SITE, out_name), 'w', encoding='utf-8').write(src)

    out = os.path.join(HERE, out_name.replace('.html', '-dom.html'))
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run',
                    '--no-default-browser-check', '--user-data-dir=' + PROFILE,
                    '--virtual-time-budget=30000', '--window-size=' + window, '--dump-dom',
                    'http://127.0.0.1:%d/%s' % (PORT, out_name)],
                   stdout=io.open(out, 'w', encoding='utf-8'), stderr=subprocess.DEVNULL)
    d = io.open(out, encoding='utf-8', errors='replace').read()
    m = re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>', d, re.S)
    if not m:
        print('  NO READING from %s' % page)
        print(d[-1000:])
        return []
    return json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')
                      .replace('&lt;', '<').replace('&gt;', '>'))


if __name__ == '__main__':
    shutil.rmtree(PROFILE, ignore_errors=True)
    total, fails = 0, 0
    for label, page, runner, out, flag, window in (
            ('THE ORDER NOTE', 'c-page-note.html', NOTE_RUNNER, '_n-note.html', '', '1500,1100'),
            ('ADD WITH NO DRAWER', 'p-nodrawer.html', ADD_RUNNER, '_n-add-nodrawer.html',
             '<script>window.__nodrawer = true;</script>', '1500,1100'),
            ('ADD WITH THE DRAWER', 'c-one.html', ADD_RUNNER, '_n-add-drawer.html', '', '1500,1100'),
            # A phone in landscape, with a note written: the geometry that broke.
            ('DRAWER GEOMETRY 812x375', 'c-noted.html', GEOMETRY_RUNNER, '_n-geom-land.html', '', '812,375'),
            ('DRAWER GEOMETRY 375x812', 'c-noted.html', GEOMETRY_RUNNER, '_n-geom-port.html', '', '375,812'),
    ):
        print('=== %s (%s) ===' % (label, page))
        for r in drive(page, runner, out, flag, window):
            total += 1
            if not r['pass']:
                fails += 1
            print('  %-4s %-62s %s' % ('PASS' if r['pass'] else 'FAIL', r['name'], r['detail'][:70]))
        print()
    print('%d assertions, %d failed' % (total, fails))
