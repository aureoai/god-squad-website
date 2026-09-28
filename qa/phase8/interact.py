import tempfile
# -*- coding: utf-8 -*-
"""Drive the cart and the variant picker in a real browser.

Static pages cannot talk to Shopify, so window.fetch is replaced before
assets/cart.js runs with a stub that answers exactly the way the Ajax Cart API
documents: an items-only body from /cart/add.js, a `sections` object keyed by
section id whose values carry the shopify-section wrapper, a 422 whose body is
{status, message, description}, a null for a section that does not exist, and a
rejected promise for a transport failure.

The stub also records every request, so the tests can assert on what was SENT
— the locale-aware URL, the line item key rather than an index, the sections
parameter — and not only on what the page did afterwards.
"""
import os, re, json, shutil, subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = os.environ.get('GS_BROWSER') or r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 8808
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-interact')
SITE = os.path.join(HERE, 'site')

STUB = r"""
<script>
(function () {
  window.__req = [];
  window.__mode = 'ok';

  function drawerHtml(lines) {
    var items = '';
    for (var i = 0; i < lines.length; i++) {
      items += '<li class="cart-line" data-cart-line data-line-key="' + lines[i] + '" data-line-index="' + (i + 1) + '">' +
        '<div class="cart-line__controls"><div class="quantity" data-quantity data-line-key="' + lines[i] + '">' +
        '<button type="button" class="quantity__button" data-quantity-step="-1" aria-disabled="true"></button>' +
        '<input class="quantity__input" data-quantity-input type="number" name="updates[]" value="1" min="1">' +
        '<button type="button" class="quantity__button" data-quantity-step="1"></button></div>' +
        '<a class="cart-line__remove" href="/cart/change?id=' + lines[i] + '&quantity=0" data-cart-remove data-line-key="' + lines[i] + '">Remove</a>' +
        '</div></li>';
    }
    return '<div id="shopify-section-cart-drawer" class="shopify-section">' +
      '<div class="cart-drawer"><div class="cart-drawer__inner" data-cart-drawer-inner>' +
      '<form data-cart-form><ul class="cart-drawer__lines">' + items + '</ul>' +
      '<div class="cart-drawer__footer"><dd data-cart-total>REFRESHED</dd></div></form>' +
      '</div></div></div>';
  }

  function bubbleHtml(n) {
    return '<div id="shopify-section-cart-icon-bubble" class="shopify-section">' +
      '<span class="header__cart-count" data-cart-count>' + n + '</span>' +
      '<span class="visually-hidden" data-cart-count-text>' + n + ' items</span></div>';
  }

  window.__lines = ['k1:aaa', 'k2:bbb'];

  window.fetch = function (input, init) {
    var url = typeof input === 'string' ? input : String(input);
    var body = init && init.body;
    var rec = { url: url, method: (init && init.method) || 'GET', headers: (init && init.headers) || null };
    if (body instanceof FormData) {
      rec.form = {};
      body.forEach(function (v, k) { rec.form[k] = String(v); });
    } else if (typeof body === 'string') {
      try { rec.json = JSON.parse(body); } catch (e) { rec.raw = body; }
    }
    window.__req.push(rec);

    if (window.__mode === 'network') return Promise.reject(new TypeError('Failed to fetch'));

    var payload, status = 200;
    if (window.__mode === 'error422') {
      status = 422;
      payload = { status: 422, message: 'Cart Error',
                  description: "You can't add more Signature Oversized Tee to the cart.",
                  sections: { 'cart-drawer': drawerHtml(window.__lines), 'cart-icon-bubble': bubbleHtml(9) } };
    } else if (window.__mode === 'nullsection') {
      payload = { items: [], sections: { 'cart-drawer': null, 'cart-icon-bubble': bubbleHtml(4) } };
    } else if (url.indexOf('?sections=') !== -1) {
      // The query-parameter API puts the keys at the JSON root, not under `sections`.
      payload = { 'cart-drawer': drawerHtml(window.__lines), 'cart-icon-bubble': bubbleHtml(7) };
    } else {
      payload = { items: [{ id: 9102, quantity: 1, key: 'k1:aaa' }],
                  sections: { 'cart-drawer': drawerHtml(window.__lines), 'cart-icon-bubble': bubbleHtml(3) } };
    }
    return Promise.resolve({
      ok: status === 200,
      status: status,
      json: function () { return Promise.resolve(payload); }
    });
  };
})();
</script>
"""

RUNNER = r"""
<script>
(function () {
  var results = [];
  // Takes the ASSERTION'S RESULT, not a thunk: every call site is written as
  // `condition || 'why it failed'`, so a false assertion carries its own
  // diagnosis instead of reporting only that it was false.
  function t(name, r) {
    results.push({ name: name, pass: r === true, detail: r === true ? '' : String(r) });
  }
  function q(s) { return document.querySelector(s); }
  function wait(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  function last() { return window.__req[window.__req.length - 1] || {}; }
  /* Whichever region is the live one right now. While the drawer is open,
     aria-modal="true" makes the layout's region unreachable, so the drawer
     carries its own and the script routes to it. */
  function announced() {
    var inner = q('[data-cart-drawer-status]');
    var outer = document.getElementById('CartStatus');
    return ((inner && inner.textContent) || '') + ((outer && outer.textContent) || '');
  }

  var drawer = q('[data-cart-drawer]');
  var bubble = q('[data-cart-bubble]');

  function run() {
    return Promise.resolve()
      // ---------------------------------------------------------- open/close
      .then(function () {
        bubble.click();
        return wait(60);
      })
      .then(function () {
        t('drawer opens from the header cart control', drawer.hidden === false || 'hidden=' + drawer.hidden);
        t('html carries the open class', document.documentElement.classList.contains('cart-drawer-open') || 'no class');
        t('focus moves to the drawer heading',
          document.activeElement === document.getElementById('CartDrawerTitle')
            || 'focus on ' + (document.activeElement && document.activeElement.tagName));
        t('background regions are inert', q('main').hasAttribute('inert') || 'main is not inert');
        /* closest(), not hasAttribute(): inert is inherited, so a drawer whose
           section wrapper is inert is inert even though the drawer element
           carries no attribute itself. Asserting on the attribute alone passed
           while focus was in fact being refused. */
        t('the drawer is not inert, including through its wrapper',
          drawer.closest('[inert]') === null || 'inert ancestor: ' + drawer.closest('[inert]').id);
        t('the live region is NOT inert',
          !document.getElementById('CartStatus').hasAttribute('inert') || 'CartStatus is inert');
        t('body scroll is locked', document.body.style.position === 'fixed' || 'position=' + document.body.style.position);

        var e = new KeyboardEvent('keydown', { key: 'Escape', bubbles: true });
        document.dispatchEvent(e);
        return wait(60);
      })
      .then(function () {
        t('Escape closes the drawer', !document.documentElement.classList.contains('cart-drawer-open') || 'still open');
        t('focus returns to the trigger', document.activeElement === bubble || 'focus on ' + (document.activeElement && document.activeElement.className));
        t('inert is removed', !q('main').hasAttribute('inert') || 'main still inert');
        t('body scroll is restored', document.body.style.position === '' || 'position=' + document.body.style.position);

        bubble.click();
        return wait(60);
      })
      .then(function () {
        var overlay = q('[data-cart-overlay]');
        overlay.click();
        return wait(60);
      })
      .then(function () {
        t('clicking the overlay closes the drawer', !document.documentElement.classList.contains('cart-drawer-open') || 'still open');

        // Escape must not be captured when the drawer is closed.
        var seen = false;
        var probe = function () { seen = true; };
        document.addEventListener('keydown', probe);
        document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
        document.removeEventListener('keydown', probe);
        t('Escape is not intercepted while closed', seen === true || 'listener never fired');
        return null;
      })
      // ------------------------------------------------------------ add flow
      .then(function () {
        window.__req.length = 0;
        window.__mode = 'ok';
        var form = q('[data-product-form]');
        if (!form) { t('product form present', 'no product form on this page'); return null; }
        var btn = q('[data-add-to-cart]');
        form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
        t('the add button goes busy', btn.getAttribute('aria-busy') === 'true' || 'aria-busy=' + btn.getAttribute('aria-busy'));
        t('the busy label is shown',
          q('[data-add-to-cart-label]').textContent.indexOf('Adding') === 0
            || 'label=' + q('[data-add-to-cart-label]').textContent);
        return wait(120);
      })
      .then(function () {
        var r = last();
        t('add posts to the locale-aware cart/add.js', /\/cart\/add\.js$/.test(r.url) || 'url=' + r.url);
        t('add uses FormData, not a JSON body', !!r.form || 'no FormData recorded');
        t('add carries the variant id', r.form && r.form.id === '9102' || 'id=' + (r.form && r.form.id));
        t('add carries both render targets',
          (r.form && r.form.sections.indexOf('cart-drawer') !== -1
            && r.form.sections.indexOf('cart-icon-bubble') !== -1)
            || 'sections=' + (r.form && r.form.sections));
        t('add does not ask for a cart-page section that is not here',
          (r.form && r.form.sections.split(',').length === 2)
            || 'sections=' + (r.form && r.form.sections));
        t('sections_url begins with a slash', r.form && r.form.sections_url.charAt(0) === '/' || 'url=' + (r.form && r.form.sections_url));
        t('no Content-Type is set on a FormData body',
          !r.headers || !r.headers['Content-Type'] || 'Content-Type=' + r.headers['Content-Type']);
        t('the header count is replaced from the section',
          q('[data-cart-count]') && q('[data-cart-count]').textContent.trim() === '3'
            || 'count=' + (q('[data-cart-count]') && q('[data-cart-count]').textContent));
        t('the drawer body is replaced from the section',
          q('[data-cart-total]') && q('[data-cart-total]').textContent === 'REFRESHED'
            || 'total=' + (q('[data-cart-total]') && q('[data-cart-total]').textContent));
        t('the drawer opened after adding', document.documentElement.classList.contains('cart-drawer-open') || 'closed');
        t('nothing is announced when focus moves into the drawer',
          announced() === '' || 'announced: ' + announced());
        t('the add button is restored', q('[data-add-to-cart]').getAttribute('aria-busy') === null || 'still busy');
        t('the add button is never disabled by the busy state',
          q('[data-add-to-cart]').disabled === false || 'the button was left disabled');
        return wait(40);
      })
      // ------------------------------------------------------ quantity + key
      .then(function () {
        window.__req.length = 0;
        var up = q('[data-cart-line] [data-quantity-step="1"]');
        if (!up) { t('a cart line is present after the swap', 'no line rendered'); return null; }
        up.click();
        t('the stepper updates the field immediately',
          q('[data-cart-line] [data-quantity-input]').value === '2'
            || 'value=' + q('[data-cart-line] [data-quantity-input]').value);
        t('the change is debounced, not sent at once', window.__req.length === 0 || 'sent ' + window.__req.length);
        return wait(400);
      })
      .then(function () {
        var r = last();
        t('quantity change posts to cart/change.js', /\/cart\/change\.js$/.test(r.url) || 'url=' + r.url);
        t('the line is identified by its KEY, not an index',
          r.json && r.json.id === 'k1:aaa' || 'id=' + (r.json && r.json.id));
        t('the new quantity is sent', r.json && r.json.quantity === 2 || 'quantity=' + (r.json && r.json.quantity));
        t('a JSON body does carry Content-Type',
          r.headers && r.headers['Content-Type'] === 'application/json' || 'headers=' + JSON.stringify(r.headers));
        t('the change is announced', announced().length > 0 || 'nothing announced');
        return null;
      })
      // ----------------------------------------------------------- minimum 1
      .then(function () {
        window.__req.length = 0;
        var input = q('[data-cart-line] [data-quantity-input]');
        input.value = '1';
        var down = q('[data-cart-line] [data-quantity-step="-1"]');
        down.setAttribute('aria-disabled', 'true');
        down.click();
        return wait(350);
      })
      .then(function () {
        t('a disabled minus sends nothing', window.__req.length === 0 || 'sent ' + window.__req.length);
        t('the quantity never goes below one',
          q('[data-cart-line] [data-quantity-input]').value === '1'
            || 'value=' + q('[data-cart-line] [data-quantity-input]').value);
        return null;
      })
      // -------------------------------------------------------------- remove
      .then(function () {
        window.__req.length = 0;
        window.__lines = ['k2:bbb'];
        var link = q('[data-cart-remove]');
        var ev = new MouseEvent('click', { bubbles: true, cancelable: true });
        var defaultPrevented = !link.dispatchEvent(ev);
        t('the removal link does not navigate', defaultPrevented === true || 'default not prevented');
        return wait(120);
      })
      .then(function () {
        var r = last();
        t('remove sends quantity 0 for the line key',
          r.json && r.json.quantity === 0 && r.json.id === 'k1:aaa'
            || 'body=' + JSON.stringify(r.json));
        t('removal is announced', announced().length > 0 || 'nothing announced');
        return null;
      })
      // --------------------------------------------------------- error paths
      // ------------------------------------------------ a visible failure
      .then(function () {
        window.__mode = 'error422';
        window.__req.length = 0;
        var up = q('[data-cart-line] [data-quantity-step="1"]');
        if (up) up.click();
        return wait(420);
      })
      .then(function () {
        var box = q('[data-cart-error]');
        t('a failed quantity change is visible, not only announced',
          (box && box.hidden === false && box.textContent.indexOf("can't add more") !== -1)
            || 'box=' + (box && (box.hidden ? '(hidden)' : box.textContent)));
        t('a failed quantity change clears its busy state',
          q('[data-cart-line] [data-quantity]').getAttribute('aria-busy') === null
            || 'still busy');
        t('the failure is announced inside the dialog, not outside it',
          (q('[data-cart-drawer-status]') && q('[data-cart-drawer-status]').textContent.length > 0)
            || 'drawer region empty; layout region=' + document.getElementById('CartStatus').textContent);
        window.__mode = 'ok';
        return null;
      })
      .then(function () {
        window.__mode = 'error422';
        window.__req.length = 0;
        var form = q('[data-product-form]');
        form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
        return wait(150);
      })
      .then(function () {
        var box = q('[data-product-error]');
        t('a 422 shows Shopify\u2019s own description',
          box && box.hidden === false && box.textContent.indexOf("can't add more") !== -1
            || 'box=' + (box && box.textContent));
        t('a 422 still applies the returned sections \u2014 it may have partly succeeded',
          q('[data-cart-count]') && q('[data-cart-count]').textContent.trim() === '9'
            || 'count=' + (q('[data-cart-count]') && q('[data-cart-count]').textContent));
        t('the button is not left stuck in its busy state',
          q('[data-add-to-cart]').getAttribute('aria-busy') === null || 'still busy');
        return null;
      })
      .then(function () {
        window.__mode = 'network';
        var form = q('[data-product-form]');
        form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
        return wait(150);
      })
      .then(function () {
        var box = q('[data-product-error]');
        t('a transport failure shows the theme\u2019s own sentence',
          box && box.hidden === false && box.textContent.indexOf('could not reach') !== -1
            || 'box=' + (box && box.textContent));
        t('the button recovers after a transport failure',
          q('[data-add-to-cart]').disabled === false || 'still disabled');
        return null;
      })
      .then(function () {
        window.__mode = 'nullsection';
        var countBefore = q('[data-cart-count]') ? q('[data-cart-count]').textContent.trim() : null;
        var form = q('[data-product-form]');
        form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
        return wait(200).then(function () { return countBefore; });
      })
      .then(function (before) {
        t('a null section is skipped without throwing',
          q('[data-cart-count]') && q('[data-cart-count]').textContent.trim() === '4'
            || 'count=' + (q('[data-cart-count]') && q('[data-cart-count]').textContent));
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
    document.addEventListener('DOMContentLoaded', function () { setTimeout(run, 120); });
  } else {
    setTimeout(run, 120);
  }
})();
</script>
<pre id="o" style="display:none"></pre>
"""


def build(page, out_name):
    src = open(os.path.join(SITE, page), encoding='utf-8').read()
    src = src.replace('<meta charset="utf-8">', '<meta charset="utf-8">' + STUB, 1)
    src = src.replace('</body>', RUNNER + '</body>', 1)
    open(os.path.join(SITE, out_name), 'w', encoding='utf-8').write(src)


def run(out_name):
    out = os.path.join(HERE, 'interact-dom.html')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run',
                    '--no-default-browser-check', '--user-data-dir=' + PROFILE,
                    '--virtual-time-budget=40000', '--window-size=1500,1100', '--dump-dom',
                    'http://127.0.0.1:%d/%s' % (PORT, out_name)],
                   stdout=open(out, 'w', encoding='utf-8'), stderr=subprocess.DEVNULL)
    d = open(out, encoding='utf-8', errors='replace').read()
    m = re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>', d, re.S)
    if not m:
        print('NO READING')
        print(d[-1500:])
        return []
    return json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')
                      .replace('&lt;', '<').replace('&gt;', '>'))


if __name__ == '__main__':
    shutil.rmtree(PROFILE, ignore_errors=True)
    build('c-one.html', '_interact.html')
    results = run('_interact.html')
    fails = 0
    for r in results:
        if not r['pass']:
            fails += 1
        print('%-4s %-62s %s' % ('PASS' if r['pass'] else 'FAIL', r['name'], r['detail'][:70]))
    print()
    print('%d assertions, %d failed' % (len(results), fails))
