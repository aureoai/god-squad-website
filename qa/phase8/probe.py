import tempfile
# -*- coding: utf-8 -*-
"""Geometry and accessibility, measured rather than asserted.

Every page is loaded in an iframe of an exact CSS width — headless Edge's own
window size does NOT give the layout the width it is asked for, which Phase 5
measured and Phase 7 confirmed — and the DOM is read at each one.

The drawer is opened for the second pass, because the controls inside it are
the ones most at risk of failing SC 2.5.8 in a 420px column, and they do not
exist in the layout until it is open.
"""
import os, re, json, shutil, subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 8808
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-probe8')
SITE = os.path.join(HERE, 'site')

WIDTHS = [(320, 2400), (375, 2400), (390, 2400), (430, 2200), (768, 2000),
          (900, 2000), (1024, 1800), (1280, 1800), (1440, 1800), (1920, 1800)]

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var PAGE = 'SRC', OPEN_DRAWER = OPENFLAG;
var W = WIDTHS;
var res = {}, i = 0;

function step() {
  if (i >= W.length) {
    document.getElementById('o').textContent = '<<<' + JSON.stringify(res) + '>>>';
    document.title = 'DONE';
    return;
  }
  var pair = W[i++], w = pair[0], h = pair[1];
  var f = document.createElement('iframe');
  f.style.cssText = 'width:' + w + 'px;height:' + h + 'px;border:0;position:absolute;left:-9999px;top:0';
  f.src = PAGE;
  f.onload = function () {
    var d = f.contentDocument, win = f.contentWindow;
    var st = d.createElement('style');
    st.textContent = '*,*::before,*::after{transition:none!important;animation:none!important}'
      + '::-webkit-scrollbar{width:0!important;height:0!important;display:none!important}'
      + 'html{scrollbar-width:none}';
    d.head.appendChild(st);

    win.setTimeout(function () {
      // Only where there IS a drawer. On the cart page the control is still
      // just a link to /cart, so clicking it navigates the frame away and the
      // pass measures whatever the harness serves at that URL.
      if (OPEN_DRAWER && d.querySelector('[data-cart-drawer]')) {
        var b = d.querySelector('[data-cart-bubble]');
        if (b) b.click();
      }
      win.setTimeout(function () { measure(d, win, w); f.remove(); step(); }, 120);
    }, 140);
  };
  document.body.appendChild(f);

  function measure(d, win, w) {
    function R(s) {
      var e = d.querySelector(s); if (!e) return null;
      var r = e.getBoundingClientRect();
      return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)];
    }
    var over = [];
    d.querySelectorAll('body *').forEach(function (e) {
      var r = e.getBoundingClientRect();
      if (r.width > 0 && r.right > w + 0.5 && win.getComputedStyle(e).position !== 'fixed') {
        var cls = (e.className && e.className.baseVal !== undefined) ? e.className.baseVal : (e.className || e.tagName);
        over.push(String(cls).slice(0, 44) + '|' + Math.round(r.left) + '..' + Math.round(r.right));
      }
    });

    // Every focusable control, with its hit box.
    var small = [], focusables = 0, positiveTab = 0;
    d.querySelectorAll('a[href],button,input:not([type=hidden]),select,textarea,[tabindex]').forEach(function (e) {
      var ti = e.getAttribute('tabindex');
      if (ti && parseInt(ti, 10) > 0) positiveTab++;
      if (e.disabled) return;
      var r = e.getBoundingClientRect();
      if (r.width === 0 && r.height === 0) return;
      var cs = win.getComputedStyle(e);
      if (cs.visibility === 'hidden' || cs.display === 'none') return;
      // The visually-hidden radios are the label's control, not a target of
      // their own; the label beside them is what a pointer hits.
      if (e.classList && e.classList.contains('visually-hidden')) return;
      // tabindex="-1" is a script focus target, not a pointer target: SC 2.5.8
      // measures things a pointer can activate, and the drawer's heading is
      // not one of them.
      if (e.getAttribute('tabindex') === '-1' && e.tagName !== 'BUTTON' && e.tagName !== 'A') return;
      // The harness's stand-in for Shopify's accelerated checkout button. The
      // real control is Shopify's markup in a closed shadow DOM and its size is
      // Shopify's to answer for, so measuring the stub proves nothing.
      if (e.closest('[data-harness-stub]')) return;
      focusables++;
      if (r.width < 24 || r.height < 24) {
        var cls = (e.className && e.className.baseVal !== undefined) ? e.className.baseVal : (e.className || '');
        small.push(e.tagName + '.' + String(cls).slice(0, 34) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height));
      }
    });

    var heads = [];
    d.querySelectorAll('h1,h2,h3,h4,h5,h6').forEach(function (h) {
      heads.push(h.tagName + ' ' + (h.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 42));
    });

    res[w] = {
      scrollW: d.documentElement.scrollWidth,
      hscroll: d.documentElement.scrollWidth > w + 1,
      overflowing: over.slice(0, 5),
      focusables: focusables,
      undersized: small.slice(0, 6),
      positiveTabindex: positiveTab,
      headings: heads,
      h1: d.querySelectorAll('h1').length,
      inner: R('.main-product__inner') || R('.main-cart__inner'),
      media: R('.main-product__media'),
      info: R('.main-product__info'),
      panel: R('.cart-drawer__panel'),
      title: R('.main-product__title'),
      infoSticky: (function () {
        var e = d.querySelector('.main-product__info');
        return e ? win.getComputedStyle(e).position : null;
      })(),
      galleryCols: (function () {
        var e = d.querySelector('.product-gallery__viewport');
        return e ? win.getComputedStyle(e).display : null;
      })()
    };
  }
}
step();
</script>
"""


def run(page, open_drawer=False):
    name = '_probe-%s-%s.html' % (page.replace('.html', ''), 'open' if open_drawer else 'shut')
    body = (PROBE.replace('SRC', page)
            .replace('OPENFLAG', 'true' if open_drawer else 'false')
            .replace('WIDTHS', json.dumps(WIDTHS)))
    open(os.path.join(SITE, name), 'w', encoding='utf-8').write(body)
    out = os.path.join(HERE, 'probe-dom.html')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run',
                    '--no-default-browser-check', '--force-prefers-reduced-motion',
                    '--user-data-dir=' + PROFILE, '--virtual-time-budget=90000',
                    '--window-size=2200,2600', '--dump-dom',
                    'http://127.0.0.1:%d/%s' % (PORT, name)],
                   stdout=open(out, 'w', encoding='utf-8'), stderr=subprocess.DEVNULL)
    d = open(out, encoding='utf-8', errors='replace').read()
    m = re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>', d, re.S)
    if not m:
        return None
    return json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')
                      .replace('&lt;', '<').replace('&gt;', '>'))


def w(box):
    return (box[2] - box[0]) if box else 0


if __name__ == '__main__':
    shutil.rmtree(PROFILE, ignore_errors=True)
    pages = sys.argv[1:] or ['p-sizes.html', 'p-multi.html', 'p-long.html',
                             'p-carousel.html', 'p-soldout.html', 'c-page-many.html']
    problems = 0
    for page in pages:
        for open_drawer in (False, True):
            data = run(page, open_drawer)
            tag = page + (' [drawer open]' if open_drawer else '')
            if not data:
                print('%-32s NO READING' % tag)
                problems += 1
                continue
            print('=' * 104)
            print(tag)
            print('%6s %8s %7s %6s %4s %10s %8s %9s %s' %
                  ('vw', 'scrollW', 'hscroll', 'focus', 'h1', 'media', 'info', 'sticky', 'undersized / overflow'))
            for k in sorted(data, key=int):
                r = data[k]
                flag = []
                if r['hscroll']:
                    flag.append('OVERFLOW ' + ','.join(r['overflowing'][:2]))
                    problems += 1
                if r['undersized']:
                    flag.append('SMALL ' + ','.join(r['undersized'][:2]))
                    problems += 1
                if r['positiveTabindex']:
                    flag.append('TABINDEX %d' % r['positiveTabindex'])
                    problems += 1
                if r['h1'] != 1 and 'c-page' not in page:
                    flag.append('h1=%d' % r['h1'])
                    problems += 1
                print('%6s %8s %7s %6s %4s %10s %8s %9s %s' %
                      (k, r['scrollW'], r['hscroll'], r['focusables'], r['h1'],
                       '%dx%d' % (w(r['media']), (r['media'][3] - r['media'][1]) if r['media'] else 0),
                       w(r['info']), r['infoSticky'] or '-',
                       ' | '.join(flag) or 'ok'))
            if not open_drawer:
                print('  headings:', ' > '.join(data[str(1440)]['headings'][:8]))
    for f in os.listdir(SITE):
        if f.startswith('_probe-'):
            os.remove(os.path.join(SITE, f))
    print()
    print('problems: %d' % problems)
