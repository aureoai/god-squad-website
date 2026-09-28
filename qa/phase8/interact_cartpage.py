import tempfile
# -*- coding: utf-8 -*-
"""The cart PAGE, driven in a real browser.

This suite exists because of the blocker the Phase 8 review found: the script
intercepted the cart page's quantity steppers and Remove links and then had
nowhere to put the answer, so the page showed a cart that no longer existed —
and after a removal its positional updates[] inputs no longer lined up with the
server's lines, which would have made Checkout apply each surviving quantity to
the wrong product.

Nothing about that is visible by reading. It needs the page, the request and
the swap.
"""
import os, re, json, shutil, subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = os.environ.get('GS_BROWSER') or r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 8808
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-cartpage')
SITE = os.path.join(HERE, 'site')

STUB = r"""
<script>
(function () {
  window.__req = [];
  window.__mode = 'ok';
  window.__lines = ['k2:bbb', 'k3:ccc', 'k4:ddd'];   // k1 removed

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
      '<dd data-cart-total>PAGE REFRESHED</dd></form>' +
      '</div></div></div>';
  }

  function bubbleHtml(n) {
    return '<div id="shopify-section-cart-icon-bubble" class="shopify-section">' +
      '<span data-cart-count>' + n + '</span></div>';
  }

  window.fetch = function (input, init) {
    var url = typeof input === 'string' ? input : String(input);
    var body = init && init.body;
    var rec = { url: url, headers: (init && init.headers) || null };
    if (body instanceof FormData) {
      rec.form = {};
      body.forEach(function (v, k) { rec.form[k] = String(v); });
    } else if (typeof body === 'string') {
      try { rec.json = JSON.parse(body); } catch (e) { rec.raw = body; }
    }
    window.__req.push(rec);
    if (window.__mode === 'network') return Promise.reject(new TypeError('Failed to fetch'));
    return Promise.resolve({
      ok: true, status: 200,
      json: function () {
        return Promise.resolve({
          sections: { 'main': pageHtml(window.__lines), 'cart-icon-bubble': bubbleHtml(4) }
        });
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
  function t(name, r) { results.push({ name: name, pass: r === true, detail: r === true ? '' : String(r) }); }
  function q(s) { return document.querySelector(s); }
  function all(s) { return [].slice.call(document.querySelectorAll(s)); }
  function wait(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  function last() { return window.__req[window.__req.length - 1] || {}; }

  function run() {
    return Promise.resolve()
      .then(function () {
        t('the drawer is not rendered on the cart page',
          q('[data-cart-drawer]') === null || 'a drawer is present');
        t('the page carries its own render hook',
          !!q('[data-cart-page-inner]') || 'no [data-cart-page-inner]');
        t('the page declares its section id',
          q('[data-cart-page]') && q('[data-cart-page]').getAttribute('data-cart-page-section') === 'main'
            || 'id=' + (q('[data-cart-page]') && q('[data-cart-page]').getAttribute('data-cart-page-section')));
        t('the page starts with four lines',
          all('[data-cart-line]').length === 4 || 'lines=' + all('[data-cart-line]').length);

        window.__req.length = 0;
        var link = q('[data-cart-remove]');
        // A real click focuses the link first; a synthetic one does not, and
        // captureFocusIntent has nothing to restore if focus was never inside
        // the node being replaced.
        link.focus();
        var prevented = !link.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
        t('the removal link does not navigate', prevented === true || 'default not prevented');
        return wait(160);
      })
      .then(function () {
        var r = last();
        t('the request asks for the cart page section',
          r.json && r.json.sections.indexOf('main') !== -1 || 'sections=' + (r.json && r.json.sections));
        t('the request does NOT ask for a drawer that is not here',
          r.json && r.json.sections.indexOf('cart-drawer') === -1 || 'sections=' + (r.json && r.json.sections));
        t('the removed line is gone from the page',
          all('[data-cart-line]').length === 3 || 'lines=' + all('[data-cart-line]').length);
        t('the page totals were replaced',
          q('[data-cart-total]') && q('[data-cart-total]').textContent === 'PAGE REFRESHED'
            || 'total=' + (q('[data-cart-total]') && q('[data-cart-total]').textContent));
        t('the header count was replaced',
          q('[data-cart-count]') && q('[data-cart-count]').textContent === '4'
            || 'count=' + (q('[data-cart-count]') && q('[data-cart-count]').textContent));
        t('updates[] now matches the server, one input per surviving line',
          all('input[name="updates[]"]').length === 3
            || 'inputs=' + all('input[name="updates[]"]').length);
        t('focus landed on the page heading, not on <body>',
          document.activeElement === q('#CartPageTitle')
            || 'focus on ' + (document.activeElement && (document.activeElement.id || document.activeElement.tagName)));
        return null;
      })
      .then(function () {
        window.__req.length = 0;
        var up = q('[data-cart-line] [data-quantity-step="1"]');
        up.click();
        return wait(420);
      })
      .then(function () {
        var r = last();
        t('a quantity change on the page posts to cart/change.js',
          /\/cart\/change\.js$/.test(r.url) || 'url=' + r.url);
        t('it identifies the line by key',
          r.json && r.json.id === 'k2:bbb' || 'id=' + (r.json && r.json.id));
        t('the page re-rendered after the change',
          q('[data-cart-total]') && q('[data-cart-total]').textContent === 'PAGE REFRESHED'
            || 'total=' + (q('[data-cart-total]') && q('[data-cart-total]').textContent));
        return null;
      })
      .then(function () {
        window.__mode = 'network';
        window.__req.length = 0;
        var up = q('[data-cart-line] [data-quantity-step="1"]');
        up.click();
        return wait(420);
      })
      .then(function () {
        var box = q('[data-cart-error]');
        t('a failed change is visible on the page',
          box && box.hidden === false && box.textContent.length > 0
            || 'box=' + (box && (box.hidden ? '(hidden)' : box.textContent)));
        t('a failed change clears the line busy state',
          q('[data-cart-line] [data-quantity]').getAttribute('aria-busy') === null || 'still busy');
        return null;
      })
      .then(function () {
        document.title = 'DONE';
        document.getElementById('o').textContent = '<<<' + JSON.stringify(results) + '>>>';
      })
      .catch(function (e) {
        results.push({ name: 'RUNNER', pass: false, detail: 'threw: ' + e.message });
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

if __name__ == '__main__':
    shutil.rmtree(PROFILE, ignore_errors=True)
    src = open(os.path.join(SITE, 'c-page-many.html'), encoding='utf-8').read()
    src = src.replace('<meta charset="utf-8">', '<meta charset="utf-8">' + STUB, 1)
    src = src.replace('</body>', RUNNER + '</body>', 1)
    open(os.path.join(SITE, '_interact-cartpage.html'), 'w', encoding='utf-8').write(src)

    out = os.path.join(HERE, 'cartpage-dom.html')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run',
                    '--no-default-browser-check', '--user-data-dir=' + PROFILE,
                    '--virtual-time-budget=30000', '--window-size=1500,1100', '--dump-dom',
                    'http://127.0.0.1:%d/_interact-cartpage.html' % PORT],
                   stdout=open(out, 'w', encoding='utf-8'), stderr=subprocess.DEVNULL)
    d = open(out, encoding='utf-8', errors='replace').read()
    m = re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>', d, re.S)
    if not m:
        print('NO READING')
        print(d[-1500:])
        raise SystemExit(1)
    results = json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')
                         .replace('&lt;', '<').replace('&gt;', '>'))
    fails = 0
    for r in results:
        if not r['pass']:
            fails += 1
        print('%-4s %-62s %s' % ('PASS' if r['pass'] else 'FAIL', r['name'], r['detail'][:60]))
    print()
    print('%d assertions, %d failed' % (len(results), fails))
