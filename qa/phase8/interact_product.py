import tempfile
# -*- coding: utf-8 -*-
"""Drive the variant picker and the media gallery in a real browser.

No network is involved: the picker resolves combinations against the variant
table the section publishes, which is the whole reason it is embedded. So these
tests need no stub — they exercise the shipped code exactly as a customer would.
"""
import os, re, json, shutil, subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = os.environ.get('GS_BROWSER') or r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 8808
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-product')
SITE = os.path.join(HERE, 'site')

RUNNER = r"""
<script>
(function () {
  var results = [];
  function t(name, r) {
    results.push({ name: name, pass: r === true, detail: r === true ? '' : String(r) });
  }
  function q(s) { return document.querySelector(s); }
  function all(s) { return [].slice.call(document.querySelectorAll(s)); }
  function wait(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  function pick(value) {
    var input = all('.variant-picker__input').filter(function (i) { return i.value === value; })[0];
    if (!input) return null;
    input.checked = true;
    input.dispatchEvent(new Event('change', { bubbles: true }));
    return input;
  }
  function label(input) { return q('label[for="' + input.id + '"]'); }

  function run() {
    var variantInput = q('[data-variant-input]');
    var addButton = q('[data-add-to-cart]');
    var priceNow = q('[data-price-current]');
    var compareWrap = q('[data-price-compare-wrap]');
    var startEntries = history.length;

    return Promise.resolve()
      .then(function () {
        t('the page starts on the server-rendered variant',
          variantInput.value === '9201' || 'value=' + variantInput.value);
        t('the server-rendered variant is buyable', addButton.disabled === false || 'disabled at load');
        t('a sale price shows its compare-at',
          compareWrap.hidden === false || 'compare-at hidden on a product that is on sale');

        // The fixture numbers from 9201 = Ink / S, so M is the next id along.
        pick('M');
        return wait(30);
      })
      .then(function () {
        t('choosing another size resolves a new variant',
          variantInput.value === '9202' || 'value=' + variantInput.value);
        t('the legend reports the chosen value',
          q('[data-option-value-for="2"]').textContent.trim() === 'M'
            || 'legend=' + q('[data-option-value-for="2"]').textContent);
        t('the URL carries the variant',
          location.search.indexOf('variant=9202') !== -1 || 'search=' + location.search);
        t('choosing a variant adds no history entry',
          history.length === startEntries || 'history grew by ' + (history.length - startEntries));
        t('the price is still rendered by Liquid, not built in the browser',
          priceNow.textContent.indexOf('2,490') !== -1 || 'price=' + priceNow.textContent);

        // Cream / L is the one unavailable combination inside an available colour.
        pick('Cream');
        return wait(30);
      })
      .then(function () {
        t('switching colour keeps a buyable size selected',
          addButton.disabled === false || 'disabled after switching to Cream');
        pick('L');
        return wait(30);
      })
      .then(function () {
        t('an unavailable combination disables add to cart',
          addButton.disabled === true || 'still enabled for Cream / L');
        t('an unavailable combination says so on the button',
          q('[data-add-to-cart-label]').textContent.trim() === 'Sold out'
            || 'label=' + q('[data-add-to-cart-label]').textContent);
        t('the variant input is disabled with it',
          variantInput.disabled === true || 'input still enabled');

        // Olive has no available variant at all.
        var olive = all('.variant-picker__input').filter(function (i) { return i.value === 'Olive'; })[0];
        t('a wholly unavailable colour is still in the DOM', !!olive || 'Olive was removed');
        t('a wholly unavailable colour is still focusable',
          olive && olive.disabled === false || 'Olive is disabled, so it cannot be reached');
        t('a wholly unavailable colour is marked',
          olive && olive.getAttribute('data-unavailable') === 'true'
            || 'data-unavailable=' + (olive && olive.getAttribute('data-unavailable')));
        t('its label carries the state in words',
          label(olive) && label(olive).textContent.toLowerCase().indexOf('unavailable') !== -1
            || 'label text=' + (label(olive) && label(olive).textContent.trim()));

        pick('S');
        return wait(30);
      })
      .then(function () {
        t('going back to an available combination re-enables add to cart',
          addButton.disabled === false || 'still disabled');
        t('the variant input is re-enabled with it',
          variantInput.disabled === false || 'input still disabled');
        t('the label goes back to the idle one',
          q('[data-add-to-cart-label]').textContent.trim() === 'Add to bag'
            || 'label=' + q('[data-add-to-cart-label]').textContent);
        return null;
      })
      // ------------------------------------------------------------- gallery
      .then(function () {
        var thumbs = all('[data-gallery-thumb]');
        t('the gallery renders one thumbnail per medium',
          thumbs.length === 3 || 'thumbs=' + thumbs.length);
        t('the first slide is active at load',
          all('.product-gallery__slide')[0].classList.contains('is-active') || 'no active slide');

        var before = location.hash;
        var ev = new MouseEvent('click', { bubbles: true, cancelable: true });
        var prevented = !thumbs[2].dispatchEvent(ev);
        t('a thumbnail click is cancelled so no hash is written', prevented === true || 'not prevented');
        t('the hash is unchanged', location.hash === before || 'hash=' + location.hash);
        return wait(60).then(function () { return thumbs; });
      })
      .then(function (thumbs) {
        t('the chosen thumbnail becomes current',
          thumbs[2].getAttribute('aria-current') === 'true' || 'aria-current missing');
        t('only one thumbnail is current',
          all('[data-gallery-thumb][aria-current="true"]').length === 1
            || 'current count=' + all('[data-gallery-thumb][aria-current="true"]').length);
        t('a non-image medium still renders a slide',
          !!q('.product-gallery__slide[data-media-type="video"]') || 'no video slide');
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
    src = open(os.path.join(SITE, 'p-multi.html'), encoding='utf-8').read()
    src = src.replace('</body>', RUNNER + '</body>', 1)
    open(os.path.join(SITE, '_interact-product.html'), 'w', encoding='utf-8').write(src)

    out = os.path.join(HERE, 'product-dom.html')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run',
                    '--no-default-browser-check', '--user-data-dir=' + PROFILE,
                    '--virtual-time-budget=30000', '--window-size=1500,1100', '--dump-dom',
                    'http://127.0.0.1:%d/_interact-product.html' % PORT],
                   stdout=open(out, 'w', encoding='utf-8'), stderr=subprocess.DEVNULL)
    d = open(out, encoding='utf-8', errors='replace').read()
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
        print('%-4s %-60s %s' % ('PASS' if r['pass'] else 'FAIL', r['name'], r['detail'][:70]))
    print()
    print('%d assertions, %d failed' % (len(results), fails))
