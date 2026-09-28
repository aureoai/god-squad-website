# -*- coding: utf-8 -*-
"""Phase 14 — the cart, driven in a real browser.

Written BEFORE the fixes, so every assertion here is a negative control first:
each one is expected to fail against the Phase 8 code and to pass after the
Phase 14 change. A test that has never been seen to fail proves nothing.

The fetch stub is the Phase 8 one, extended to record timing so a debounced
request that should have been cancelled can be seen arriving late.
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
PHASE8 = os.path.abspath(os.path.join(HERE, '..', 'phase8'))
SITE = os.path.join(PHASE8, 'site')
# Overridable so the same suites can be driven by a second engine.
EDGE = os.environ.get('GS_BROWSER',
                      r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
PORT = 8808
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-cartqa')
STUB = r"""
<script>
(function () {
  window.__req = [];
  window.__mode = 'ok';
  window.__lines = ['k2:bbb', 'k3:ccc', 'k4:ddd'];

  function pageHtml(lines) {
    var items = '';
    for (var i = 0; i < lines.length; i++) {
      items += '<li class="cart-line" data-cart-line data-line-key="' + lines[i] + '" data-line-index="' + (i + 1) + '">' +
        '<div class="quantity" data-quantity data-line-key="' + lines[i] + '">' +
        '<button type="button" data-quantity-step="-1" aria-disabled="true"></button>' +
        '<input class="quantity__input" data-quantity-input type="number" name="updates[]" value="1" min="1">' +
        '<button type="button" data-quantity-step="1"></button></div>' +
        '<a href="/cart/change?id=' + lines[i] + '&quantity=0" data-cart-remove data-line-key="' + lines[i] + '">Remove</a>' +
        '</li>';
    }
    return '<div id="shopify-section-main" class="shopify-section">' +
      '<div class="main-cart"><div data-cart-page-inner>' +
      '<form data-cart-form><ul>' + items + '</ul>' +
      '<textarea data-cart-note name="note">SERVER NOTE</textarea>' +
      '<dd data-cart-total>PAGE REFRESHED</dd></form>' +
      '</div></div></div>';
  }

  window.fetch = function (input, init) {
    var url = typeof input === 'string' ? input : String(input);
    var body = init && init.body;
    var rec = { url: url, at: Date.now() };
    if (body instanceof FormData) {
      rec.form = {};
      body.forEach(function (v, k) { rec.form[k] = String(v); });
    } else if (typeof body === 'string') {
      try { rec.json = JSON.parse(body); } catch (e) { rec.raw = body; }
    }
    window.__req.push(rec);
    if (window.__mode === 'network') return Promise.reject(new TypeError('Failed to fetch'));
    if (window.__mode === 'error422') {
      return Promise.resolve({
        ok: false, status: 422,
        json: function () {
          return Promise.resolve({ status: 422, message: 'Cart Error',
            description: 'All 3 Utility Cap are in your cart.',
            sections: { 'main': pageHtml(window.__lines) } });
        }
      });
    }
    return Promise.resolve({
      ok: true, status: 200,
      json: function () {
        return Promise.resolve({ sections: { 'main': pageHtml(window.__lines) } });
      }
    });
  };
})();
</script>
"""

RUNNER = r"""
<script>
(function () {
  var results = [];
  function t(name, r) {
    results.push({ name: name, pass: r === true, detail: r === true ? '' : String(r) });
  }
  function q(s) { return document.querySelector(s); }
  function wait(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  function changes() {
    return window.__req.filter(function (r) { return /cart\/change\.js$/.test(r.url); });
  }

  function run() {
    return Promise.resolve()
      /* ---------------------------------------------------------------- D4
         The no-JavaScript Update control is redundant once the cart script is
         applying changes as they are made, and the theme says so in writing.
         The rule that hides it has to be in a stylesheet THIS page loads.

         Checked FIRST, before any section swap: the stub's rendered cart page
         does not carry this control, so a later check would read the stub's
         markup and report it missing rather than visible. */
      .then(function () {
        t('the cart script announced itself',
          document.documentElement.classList.contains('cart-js') || 'no cart-js class');
        var update = q('.main-cart__update');
        t('the cart page has an Update control in the markup', !!update || 'none rendered');
        if (update) {
          t('and it is hidden once the cart script is running',
            getComputedStyle(update).display === 'none'
              || 'display=' + getComputedStyle(update).display);
        }
        return null;
      })
      /* ---------------------------------------------------------------- D3
         A quantity step is debounced by 250ms. Removing the line inside that
         window must CANCEL it: /cart/change.js with a key the server has just
         dropped answers 404, so the customer would watch a successful removal
         be followed by "Unable to update your cart". */
      .then(function () {
        window.__req.length = 0;
        window.__mode = 'ok';
        var line = document.querySelectorAll('[data-cart-line]')[0];
        var key = line.getAttribute('data-line-key');
        window.__key = key;
        line.querySelector('[data-quantity-step="1"]').click();
        return wait(40).then(function () {
          t('the stepper does not fire immediately', changes().length === 0
            || 'fired ' + changes().length + ' request(s) inside the debounce');
          document.querySelector('[data-cart-remove][data-line-key="' + key + '"]').click();
          return wait(600);
        });
      })
      .then(function () {
        var c = changes();
        t('removing a line inside the debounce sends ONE request',
          c.length === 1 || 'sent ' + c.length + ': ' +
            c.map(function (r) { return r.json && r.json.quantity; }).join(','));
        t('and that request is the removal, not the stepped quantity',
          (c.length && c[c.length - 1].json && c[c.length - 1].json.quantity === 0)
            || 'last quantity=' + (c.length ? c[c.length - 1].json.quantity : 'none'));
        t('no request carries a quantity for a line already removed',
          c.every(function (r) { return r.json.quantity === 0; })
            || 'quantities=' + c.map(function (r) { return r.json.quantity; }).join(','));
        return null;
      })
      /* --------------------------------------------------- RACE CONDITIONS
         The brief: "Prevent multiple rapid quantity requests from producing
         inconsistent cart state." Five presses of + is ONE request carrying
         the fifth value, not five requests racing each other to land last. */
      .then(function () {
        window.__req.length = 0;
        window.__mode = 'ok';
        var line = document.querySelectorAll('[data-cart-line]')[0];
        var up = line.querySelector('[data-quantity-step="1"]');
        var input = line.querySelector('[data-quantity-input]');
        for (var i = 0; i < 5; i++) up.click();
        t('the number on screen moves on every press, with no wait',
          parseInt(input.value, 10) === 6 || 'input reads ' + input.value);
        return wait(600);
      })
      .then(function () {
        var c = changes();
        t('five rapid presses send ONE request', c.length === 1 || 'sent ' + c.length);
        t('and it carries the final quantity, not an intermediate one',
          c.length === 1 && c[0].json.quantity === 6
            || 'quantity=' + (c.length && c[0].json.quantity));
        return null;
      })
      /* Two different lines are two different debounces, and must not collapse
         into one another: the timers are keyed by line. */
      .then(function () {
        window.__req.length = 0;
        var lines = document.querySelectorAll('[data-cart-line]');
        if (lines.length < 2) { t('two lines are present to race', 'only ' + lines.length); return null; }
        lines[0].querySelector('[data-quantity-step="1"]').click();
        lines[1].querySelector('[data-quantity-step="1"]').click();
        return wait(600).then(function () {
          var c = changes();
          t('changing two lines quickly sends one request each',
            c.length === 2 || 'sent ' + c.length);
          var keys = c.map(function (r) { return r.json.id; });
          t('each carries its OWN line key, never an index',
            c.length === 2 && keys[0] !== keys[1]
              && keys.every(function (k) { return /:/.test(k); })
              || 'ids=' + keys.join(','));
          return null;
        });
      })
      /* ---------------------------------------------------------------- D2
         A cart-line failure must reach the CART's error line and nothing else.
         showCartError() selected [data-cart-error] document-wide, which is the
         attribute a quick-add product card also carries. */
      .then(function () {
        var card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML = '<form action="/cart/add"><p class="product-card__error" data-cart-error hidden></p></form>';
        q('main').appendChild(card);
        window.__card = card.querySelector('[data-cart-error]');

        window.__req.length = 0;
        window.__mode = 'error422';
        var line = document.querySelectorAll('[data-cart-line]')[0];
        line.querySelector('[data-quantity-step="1"]').click();
        return wait(700);
      })
      .then(function () {
        var page = q('.main-cart__error');
        t('the failure is visible on the cart surface',
          (page && page.hidden === false && page.textContent.indexOf('Utility Cap') !== -1)
            || 'cart error box: hidden=' + (page && page.hidden) + ' text=' + (page && page.textContent));
        t('the failure does NOT leak into a product card elsewhere on the page',
          (window.__card.hidden === true && window.__card.textContent === '')
            || 'card error box carried: "' + window.__card.textContent + '"');
        return null;
      })
      .then(function () {
        document.title = 'DONE';
        document.getElementById('o').textContent = '<<<' + JSON.stringify(results) + '>>>';
      })
      .catch(function (e) {
        results.push({ name: 'RUNNER', pass: false, detail: 'threw: ' + e.message + ' ' + e.stack });
        document.title = 'DONE';
        document.getElementById('o').textContent = '<<<' + JSON.stringify(results) + '>>>';
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { setTimeout(run, 150); });
  } else {
    setTimeout(run, 150);
  }
})();
</script>
<pre id="o" style="display:none"></pre>
"""


def drive(page, out_name, dom_name):
    src = open(os.path.join(SITE, page), encoding='utf-8').read()
    src = src.replace('<meta charset="utf-8">', '<meta charset="utf-8">' + STUB, 1)
    src = src.replace('</body>', RUNNER + '</body>', 1)
    open(os.path.join(SITE, out_name), 'w', encoding='utf-8').write(src)

    out = os.path.join(HERE, dom_name)
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run',
                    '--no-default-browser-check', '--user-data-dir=' + PROFILE,
                    '--virtual-time-budget=30000', '--window-size=1500,1100', '--dump-dom',
                    'http://127.0.0.1:%d/%s' % (PORT, out_name)],
                   stdout=open(out, 'w', encoding='utf-8'), stderr=subprocess.DEVNULL)
    d = open(out, encoding='utf-8', errors='replace').read()
    m = re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>', d, re.S)
    if not m:
        print('NO READING from %s' % page)
        print(d[-1200:])
        return []
    return json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')
                      .replace('&lt;', '<').replace('&gt;', '>'))


if __name__ == '__main__':
    shutil.rmtree(PROFILE, ignore_errors=True)
    results = drive('c-page-many.html', '_cartqa.html', 'cartqa-dom.html')
    fails = 0
    for r in results:
        if not r['pass']:
            fails += 1
        print('%-4s %-64s %s' % ('PASS' if r['pass'] else 'FAIL', r['name'], r['detail'][:80]))
    print()
    print('%d assertions, %d failed' % (len(results), fails))
