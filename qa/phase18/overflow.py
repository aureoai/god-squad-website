# -*- coding: utf-8 -*-
"""Phase 18 — a long product name in the cart does not wrap. Where does it go?

longtitle.py put a 51-character name into .cart-line__title and the box stayed
24px tall and one line. At 12px with 0.22em tracking, uppercase, that string is
far wider than the column it sits in, so it is not fitting -- it is going
somewhere. This finds out where.

.cart-line__title is display:inline-flex. Its text becomes an anonymous flex
item, and a flex item is sized from its max-content width by default, so the
line does not break: it runs past the column edge. Whether a customer sees that
as clipped text, a scrollbar, or text sitting on top of the price depends on
what the ancestors do with the overflow, which is what this measures.

Shopify product titles are merchant data. This theme cannot assume they are
short, and the fixtures' invented names are the shortest case, not the typical
one.
"""
import io
import json
import os
import re
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = os.environ.get('GS_BROWSER',
                      r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-ovf')
NAMES = [
    'Signature Oversized Tee',
    'Signature Oversized Heavyweight Tee Cream',
    'Faith Over Fear Signature Oversized Heavyweight Tee In Cream Cotton',
]

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var NAMES = NAMELIST, WIDTHS = [1440, 768, 375], out = [];
var wi = 0, ni = 0;
function chain(el, d) {
  /* Walk up recording who could contain or clip the overflow. */
  var r = [], n = el.parentElement, w = el.ownerDocument.defaultView, guard = 0;
  while (n && guard++ < 6) {
    var cs = w.getComputedStyle(n);
    r.push({cls: (n.className || n.tagName).toString().split(' ')[0],
            w: Math.round(n.getBoundingClientRect().width),
            ox: cs.overflowX, sw: n.scrollWidth});
    n = n.parentElement;
  }
  return r;
}
function step() {
  if (wi >= WIDTHS.length) {
    document.title = 'DONE';
    document.getElementById('o').textContent = '<<<' + JSON.stringify(out) + '>>>';
    return;
  }
  var W = WIDTHS[wi];
  var f = document.createElement('iframe');
  f.style.cssText = 'border:0;width:' + W + 'px;height:2000px';
  f.src = 'c-page-many.html';
  document.body.appendChild(f);
  f.onload = function () {
    var d = f.contentDocument, w = f.contentWindow;
    var t = d.querySelector('.cart-line__title');
    var parent = t.parentElement;
    NAMES.forEach(function (n) {
      t.textContent = n;
      void d.body.offsetHeight;
      var tr = t.getBoundingClientRect(), pr = parent.getBoundingClientRect();
      out.push({
        width: W, name: n, chars: n.length,
        titleW: Math.round(tr.width), titleH: Math.round(tr.height * 10) / 10,
        parentW: Math.round(pr.width),
        overflowPx: Math.round(tr.right - pr.right),
        rects: t.getClientRects().length,
        docScrollW: d.documentElement.scrollWidth,
        docClientW: d.documentElement.clientWidth,
        chain: chain(t, d)
      });
    });
    f.remove(); wi++; step();
  };
}
step();
</script>
"""

if __name__ == '__main__':
    S8 = os.path.abspath(os.path.join(HERE, '..', 'phase8', 'site'))
    html = PROBE.replace('NAMELIST', json.dumps(NAMES))
    p = os.path.join(S8, '_ovf.html')
    io.open(p, 'w', encoding='utf-8').write(html)
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8808'],
                           cwd=S8, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        outp = os.path.join(HERE, 'ovf.html')
        subprocess.call([EDGE, '--headless=new', '--disable-gpu',
                         '--user-data-dir=' + PROFILE, '--virtual-time-budget=20000',
                         '--dump-dom', 'http://127.0.0.1:8808/_ovf.html'],
                        stdout=io.open(outp, 'wb'), stderr=subprocess.DEVNULL)
        dom = io.open(outp, encoding='utf-8', errors='replace').read()
        m = re.search(r'&lt;&lt;&lt;(.*?)&gt;&gt;&gt;', dom, re.S) or \
            re.search(r'<<<(.*?)>>>', dom, re.S)
        if not m:
            raise SystemExit('  *** no payload ***')
        data = json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&'))
    finally:
        srv.terminate()
        try:
            os.remove(p)
        except OSError:
            pass

    print('=== DOES A LONG CART TITLE OVERFLOW ITS COLUMN? ===')
    print('  %-7s %-4s %-8s %-9s %-10s %-7s %s'
          % ('screen', 'len', 'title w', 'column w', 'overflow', 'lines', 'page scrolls?'))
    bad = []
    for r in data:
        scrolls = r['docScrollW'] > r['docClientW']
        flag = ''
        if r['overflowPx'] > 1:
            flag = ' ***'
            bad.append(r)
        print('  %-7d %-4d %-8d %-9d %+-10d %-7d %s%s'
              % (r['width'], r['chars'], r['titleW'], r['parentW'], r['overflowPx'],
                 r['rects'], 'YES %d>%d' % (r['docScrollW'], r['docClientW']) if scrolls else 'no',
                 flag))

    print()
    if bad:
        print('=== THE OVERFLOW, AND WHO CATCHES IT ===')
        seen = set()
        for r in bad:
            k = (r['width'], r['chars'])
            if k in seen:
                continue
            seen.add(k)
            print('  %dpx screen, %d-char name -- title runs %dpx past its column:'
                  % (r['width'], r['chars'], r['overflowPx']))
            for c in r['chain']:
                clip = 'CLIPS' if c['ox'] in ('hidden', 'auto', 'scroll') else 'lets it through'
                print('      %-26s w=%-5d overflow-x:%-8s %s%s'
                      % (c['cls'], c['w'], c['ox'], clip,
                         '  (scrollWidth %d)' % c['sw'] if c['sw'] > c['w'] else ''))
            print()
    else:
        print('No overflow at any tested width or length.')
