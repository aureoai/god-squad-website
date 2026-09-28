# -*- coding: utf-8 -*-
"""Phase 14 — the cart drawer through the Theme Editor's section lifecycle.

Phase 11's finding was that editor defects are invisible to markup tests: a
section re-rendered in place is a new DOM node, and everything the old one put
OUTSIDE itself — the scroll lock on <body>, inert on its siblings, a
document-level keydown listener — outlives it unless something tears it down.

assets/cart.js says in writing that it handles this. This is the test of that
claim, plus the Phase 14 settings a merchant can toggle while the drawer is on
screen.
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
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-lifecycle')
COUNTER = r"""
<script>
/* Counts document-level listeners, so "it re-binds on every editor render"
   is measured rather than assumed. Installed before assets/cart.js runs. */
(function () {
  window.__listeners = { keydown: 0, submit: 0, click: 0, change: 0, input: 0 };
  var addDoc = Document.prototype.addEventListener;
  var remDoc = Document.prototype.removeEventListener;
  Document.prototype.addEventListener = function (type) {
    if (type in window.__listeners) window.__listeners[type]++;
    return addDoc.apply(this, arguments);
  };
  Document.prototype.removeEventListener = function (type) {
    if (type in window.__listeners) window.__listeners[type]--;
    return remDoc.apply(this, arguments);
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
  function wait(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  function snap() { return JSON.parse(JSON.stringify(window.__listeners)); }

  /* What the Theme Editor does: replaces the section's contents in place and
     fires unload for the old node, then load for the new one. */
  function rerender(withNote) {
    var wrapper = document.getElementById('shopify-section-cart-drawer');
    var html = wrapper.innerHTML;
    document.dispatchEvent(new CustomEvent('shopify:section:unload',
      { detail: { sectionId: 'cart-drawer' } , bubbles: true }));
    // The event's target is what cart.js inspects, so dispatch it ON the wrapper.
    wrapper.dispatchEvent(new CustomEvent('shopify:section:unload', { bubbles: true }));
    if (withNote === false) {
      html = html.replace(/<details class="cart-note"[\s\S]*?<\/details>/, '');
    }
    wrapper.innerHTML = html;
    wrapper.dispatchEvent(new CustomEvent('shopify:section:load', { bubbles: true }));
  }

  function run() {
    var bubble = q('[data-cart-bubble]');
    var base;
    return Promise.resolve()
      .then(function () {
        base = snap();
        bubble.click();
        return wait(120);
      })
      .then(function () {
        t('the drawer opened', q('[data-cart-drawer]').hidden === false || 'still hidden');
        t('the page is scroll-locked while it is open',
          document.body.style.position === 'fixed' || 'position=' + document.body.style.position);
        t('the background is inert',
          q('main').hasAttribute('inert') || 'main is not inert');

        /* THE EDITOR RENDER, WITH THE DRAWER OPEN. This is the case the code
           comments name: the new node arrives hidden while the lock, the inert
           siblings and the keydown listener all outlive the old one. */
        rerender(true);
        return wait(150);
      })
      .then(function () {
        t('an editor re-render releases the scroll lock',
          document.body.style.position === '' || 'body is still position=' + document.body.style.position);
        t('and un-inerts the background',
          !q('main').hasAttribute('inert') || 'main is still inert');
        t('and leaves no drawer on screen claiming to be open',
          !document.documentElement.classList.contains('cart-drawer-open')
            || 'html still carries cart-drawer-open');
        var now = snap();
        t('the document keydown listener was released too',
          now.keydown <= base.keydown || 'keydown listeners: ' + base.keydown + ' -> ' + now.keydown);
        return null;
      })
      /* The drawer must still WORK after the editor touched it. */
      .then(function () {
        q('[data-cart-bubble]').click();
        return wait(150);
      })
      .then(function () {
        t('the drawer still opens after an editor re-render',
          q('[data-cart-drawer]').hidden === false || 'it did not reopen');
        t('focus still moves to its heading',
          document.activeElement === document.getElementById('CartDrawerTitle')
            || 'focus on ' + (document.activeElement && document.activeElement.tagName));
        t('Checkout is still in the form after the re-render',
          !!q('[data-cart-checkout]') || 'the checkout control is gone');
        t('the quantity controls still work',
          !!q('[data-cart-line] [data-quantity-step]') || 'no stepper found');
        document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
        return wait(150);
      })
      .then(function () {
        t('Escape still closes it', !document.documentElement.classList.contains('cart-drawer-open')
          || 'still open');
        return null;
      })
      /* A merchant toggling "Let customers add an order note" off and on is
         five re-renders. Delegated listeners must not accumulate. */
      .then(function () {
        var before = snap();
        for (var i = 0; i < 5; i++) rerender(i % 2 === 0 ? false : true);
        return wait(200).then(function () {
          var after = snap();
          var grown = [];
          Object.keys(after).forEach(function (k) {
            if (after[k] > before[k]) grown.push(k + ' ' + before[k] + '->' + after[k]);
          });
          t('five setting toggles add no document listeners',
            grown.length === 0 || 'grew: ' + grown.join(', '));
          t('the cart still has exactly one form after five re-renders',
            document.querySelectorAll('[data-cart-drawer] [data-cart-form]').length === 1
              || 'forms=' + document.querySelectorAll('[data-cart-drawer] [data-cart-form]').length);
          t('and exactly one note field',
            document.querySelectorAll('[data-cart-note]').length <= 1
              || 'notes=' + document.querySelectorAll('[data-cart-note]').length);
          return null;
        });
      })
      .then(function () {
        /* And it is still usable after all of that. */
        q('[data-cart-bubble]').click();
        return wait(150).then(function () {
          t('the drawer opens after five toggles',
            q('[data-cart-drawer]').hidden === false || 'it did not open');
          t('the page is scroll-locked again, not stuck unlocked',
            document.body.style.position === 'fixed' || 'position=' + document.body.style.position);
          document.querySelector('[data-cart-close]').click();
          return wait(150);
        });
      })
      .then(function () {
        t('and the close button still unlocks it',
          document.body.style.position === '' || 'body left at position=' + document.body.style.position);
        document.title = 'DONE';
        document.getElementById('o').textContent = '<<<' + JSON.stringify(results) + '>>>';
      })
      .catch(function (e) {
        results.push({ name: 'RUNNER', pass: false, detail: 'threw: ' + e.message + ' ' + e.stack });
        document.title = 'DONE';
        document.getElementById('o').textContent = '<<<' + JSON.stringify(results) + '>>>';
      });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { setTimeout(run, 150); });
  else setTimeout(run, 150);
})();
</script>
<pre id="o" style="display:none"></pre>
"""

STUB = r"""
<script>
(function () {
  window.fetch = function () {
    return Promise.resolve({ ok: true, status: 200,
      json: function () { return Promise.resolve({ sections: {} }); } });
  };
})();
</script>
"""


if __name__ == '__main__':
    shutil.rmtree(PROFILE, ignore_errors=True)
    src = io.open(os.path.join(SITE, 'c-noted.html'), encoding='utf-8').read()
    src = src.replace('<meta charset="utf-8">', '<meta charset="utf-8">' + COUNTER + STUB, 1)
    src = src.replace('</body>', RUNNER + '</body>', 1)
    io.open(os.path.join(SITE, '_lifecycle.html'), 'w', encoding='utf-8').write(src)

    out = os.path.join(HERE, 'lifecycle-dom.html')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run',
                    '--no-default-browser-check', '--user-data-dir=' + PROFILE,
                    '--virtual-time-budget=30000', '--window-size=1500,1100', '--dump-dom',
                    'http://127.0.0.1:%d/_lifecycle.html' % PORT],
                   stdout=io.open(out, 'w', encoding='utf-8'), stderr=subprocess.DEVNULL)
    d = io.open(out, encoding='utf-8', errors='replace').read()
    m = re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>', d, re.S)
    if not m:
        print('NO READING')
        print(d[-1200:])
        raise SystemExit(1)
    results = json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')
                         .replace('&lt;', '<').replace('&gt;', '>'))
    fails = 0
    for r in results:
        if not r['pass']:
            fails += 1
        print('%-4s %-62s %s' % ('PASS' if r['pass'] else 'FAIL', r['name'], r['detail'][:70]))
    print()
    print('%d assertions, %d failed' % (len(results), fails))
