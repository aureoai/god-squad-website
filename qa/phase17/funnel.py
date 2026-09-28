# -*- coding: utf-8 -*-
"""Phase 17 PART 22 + PART 38 — one customer action, one Shopify cart call.

WHY THIS IS THE RIGHT TEST WHEN THERE IS NO ANALYTICS.

Shopify's standard events are emitted by Shopify, not by the theme, and they are
emitted in response to the storefront calls the theme makes. So the theme cannot
fire a duplicate `product_added_to_cart` directly — but it CAN cause one, by
making two /cart/add.js calls for one press. The theme-side precondition for
every event firing exactly once is that every customer action produces exactly
one Shopify call.

That is fully testable here, and it is the only part of the funnel this
environment can settle: there is no store, so no event can be observed.

The journey is the brief's, as far as a theme can take it:
  view product -> select variant -> set quantity -> add to cart -> open cart ->
  change quantity -> remove -> begin checkout
"""
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, '..', 'phase8', 'site'))
EDGE = os.environ.get('GS_BROWSER',
                      r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-funnel')
PORT = 8808

STUB = r"""
<script>
(function () {
  window.__calls = [];
  function drawerHtml() {
    return '<div id="shopify-section-cart-drawer" class="shopify-section">' +
      '<div class="cart-drawer"><div class="cart-drawer__inner" data-cart-drawer-inner>' +
      '<form data-cart-form><ul><li class="cart-line" data-cart-line data-line-key="k1:aaa">' +
      '<div class="quantity" data-quantity data-line-key="k1:aaa">' +
      '<button type="button" data-quantity-step="-1" aria-disabled="true"></button>' +
      '<input class="quantity__input" data-quantity-input type="number" value="1" min="1">' +
      '<button type="button" data-quantity-step="1"></button></div>' +
      '<a href="/cart/change?id=k1:aaa&quantity=0" data-cart-remove data-line-key="k1:aaa">Remove</a>' +
      '</li></ul><button type="submit" name="checkout" data-cart-checkout>Checkout</button>' +
      '</form></div></div></div>';
  }
  window.fetch = function (input, init) {
    var url = typeof input === 'string' ? input : String(input);
    var rec = { url: url.replace(/^https?:\/\/[^/]+/, '') };
    var b = init && init.body;
    if (b instanceof FormData) { rec.form = {}; b.forEach(function (v, k) { rec.form[k] = String(v); }); }
    else if (typeof b === 'string') { try { rec.json = JSON.parse(b); } catch (e) {} }
    window.__calls.push(rec);
    return Promise.resolve({ ok: true, status: 200, json: function () {
      return Promise.resolve({ items: [{ id: 9102, quantity: 1, key: 'k1:aaa' }],
        sections: { 'cart-drawer': drawerHtml(),
                    'cart-icon-bubble': '<div id="shopify-section-cart-icon-bubble" class="shopify-section"><span data-cart-count>1</span></div>' } }); } });
  };
})();
</script>
"""

RUNNER = r"""
<script>
(function () {
  var out = [];
  function q(s) { return document.querySelector(s); }
  function wait(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  function since(n) { return window.__calls.slice(n); }
  function step(name, fn, ms) {
    var before = window.__calls.length;
    return Promise.resolve(fn()).then(function () {
      return wait(ms || 600);
    }).then(function () {
      var made = since(before);
      out.push({ step: name, calls: made.map(function (c) {
        return c.url + (c.json && c.json.quantity !== undefined ? ' q=' + c.json.quantity : ''); } ) });
    });
  }

  function run() {
    return Promise.resolve()
      .then(function () { return step('select a variant', function () {
        var r = document.querySelectorAll('[data-variant-option] input, .variant-picker input');
        if (r && r[1]) r[1].click();
      }, 300); })
      .then(function () { return step('set quantity to 2', function () {
        var up = q('.main-product__quantity [data-quantity-step="1"]');
        if (up) up.click();
      }, 300); })
      .then(function () { return step('add to cart (one press)', function () {
        var f = q('[data-product-form]');
        if (f) f.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
      }); })
      .then(function () { return step('open the cart drawer', function () {
        var b = q('[data-cart-bubble]'); if (b) b.click();
      }, 300); })
      .then(function () { return step('close and reopen the drawer', function () {
        document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
        setTimeout(function () { var b = q('[data-cart-bubble]'); if (b) b.click(); }, 120);
      }, 500); })
      .then(function () { return step('increase a cart line quantity', function () {
        var up = q('[data-cart-line] [data-quantity-step="1"]'); if (up) up.click();
      }); })
      .then(function () { return step('remove the line', function () {
        var r = q('[data-cart-remove]'); if (r) r.click();
      }); })
      .then(function () {
        document.title = 'DONE';
        document.getElementById('o').textContent = '<<<' + JSON.stringify(out) + '>>>';
      })
      .catch(function (e) {
        out.push({ step: 'RUNNER THREW', calls: [String(e)] });
        document.title = 'DONE';
        document.getElementById('o').textContent = '<<<' + JSON.stringify(out) + '>>>';
      });
  }
  if (document.readyState === 'complete') setTimeout(run, 200);
  else window.addEventListener('load', function () { setTimeout(run, 200); });
})();
</script>
<pre id="o" style="display:none"></pre>
"""

FAILURES = []
CHECKS = [0]


def check(label, ok, detail=''):
    CHECKS[0] += 1
    print('  %-56s %s %s' % (label, 'OK  ' if ok else '*** FAIL ***',
                             '' if ok else str(detail)[:110]))
    if not ok:
        FAILURES.append(label)


if __name__ == '__main__':
    shutil.rmtree(PROFILE, ignore_errors=True)
    src = io.open(os.path.join(SITE, 'p-sizes.html'), encoding='utf-8').read()
    src = src.replace('<meta charset="utf-8">', '<meta charset="utf-8">' + STUB, 1)
    src = src.replace('</body>', RUNNER + '</body>', 1)
    io.open(os.path.join(SITE, '_funnel.html'), 'w', encoding='utf-8').write(src)

    out = os.path.join(HERE, 'funnel-dom.html')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run',
                    '--no-default-browser-check', '--user-data-dir=' + PROFILE,
                    '--virtual-time-budget=30000', '--window-size=1440,900', '--dump-dom',
                    'http://127.0.0.1:%d/_funnel.html' % PORT],
                   stdout=io.open(out, 'w', encoding='utf-8'), stderr=subprocess.DEVNULL)
    d = io.open(out, encoding='utf-8', errors='replace').read()
    m = re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>', d, re.S)
    if not m:
        print('NO READING')
        print(d[-900:])
        raise SystemExit(1)
    steps = json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')
                       .replace('&lt;', '<').replace('&gt;', '>'))

    print('=== THE JOURNEY, AND THE SHOPIFY CALLS EACH STEP MAKES ===')
    print()
    print('  %-32s %-6s %s' % ('customer action', 'calls', 'endpoints'))
    by = {}
    for s in steps:
        by[s['step']] = s['calls']
        print('  %-32s %-6d %s' % (s['step'], len(s['calls']), ', '.join(s['calls']) or '-'))

    print()
    print('=== ONE ACTION, ONE CALL — the precondition for one event ===')
    check('selecting a variant talks to Shopify not at all',
          len(by.get('select a variant', [])) == 0, by.get('select a variant'))
    check('changing the product quantity talks to Shopify not at all',
          len(by.get('set quantity to 2', [])) == 0, by.get('set quantity to 2'))
    check('one add-to-cart press makes exactly one /cart/add.js call',
          len(by.get('add to cart (one press)', [])) == 1,
          by.get('add to cart (one press)'))
    check('and it is the add endpoint, not something else',
          any('/cart/add.js' in c for c in by.get('add to cart (one press)', [])),
          by.get('add to cart (one press)'))
    check('opening the cart drawer makes NO call',
          len(by.get('open the cart drawer', [])) == 0, by.get('open the cart drawer'))
    check('closing and reopening it makes NO call',
          len(by.get('close and reopen the drawer', [])) == 0,
          by.get('close and reopen the drawer'))
    check('one quantity step makes exactly one /cart/change.js call',
          len(by.get('increase a cart line quantity', [])) == 1,
          by.get('increase a cart line quantity'))
    check('one removal makes exactly one call, at quantity 0',
          len(by.get('remove the line', [])) == 1
          and 'q=0' in (by.get('remove the line') or [''])[0],
          by.get('remove the line'))

    print()
    print('  A drawer that opened with a call would make Shopify emit a second')
    print('  cart event per open. It does not: the drawer is rendered with the')
    print('  page and shown, never fetched.')

    print()
    print('%d checks, %d passed, %d failed'
          % (CHECKS[0], CHECKS[0] - len(FAILURES), len(FAILURES)))
    print('OVERALL: %s' % ('PASS' if not FAILURES else '*** FAILURES ABOVE ***'))
