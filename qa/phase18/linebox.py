# -*- coding: utf-8 -*-
"""Phase 18 — count the REAL line boxes of a cart title.

Two measurements disagree. overflow.py reports a 67-character name sitting in a
215px box that is 24px tall and does not overflow; the CSS has no clamp, no
ellipsis and no nowrap, so that string must occupy several lines and the box
must be taller than 24px. One of those readings is wrong.

getClientRects() was the wrong instrument. .cart-line__title is inline-flex,
which is an ATOMIC INLINE: it returns one rect for its border box no matter how
many lines its content takes. Counting lines that way can only ever return 1.

A Range over the TEXT NODE returns one rect per line fragment, which is the
actual number of lines the text occupies. That is the instrument this uses,
alongside scrollHeight and the parent's height, so the three have to agree
before anything is concluded.
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
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-lbox')
NAMES = [
    'Signature Oversized Tee',
    'Signature Oversized Heavyweight Tee Cream',
    'Faith Over Fear Signature Oversized Heavyweight Tee In Cream Cotton',
]

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var NAMES = NAMELIST, WIDTHS = [1440, 375], out = [], wi = 0;
function textRects(el) {
  /* One rect per LINE FRAGMENT of the text itself. */
  var d = el.ownerDocument, n = el.firstChild;
  while (n && n.nodeType !== 3) { n = n.firstChild || n.nextSibling; }
  if (!n) return null;
  var r = d.createRange();
  r.selectNodeContents(n);
  var rects = r.getClientRects();
  var tops = {}, list = [];
  for (var i = 0; i < rects.length; i++) {
    var t = Math.round(rects[i].top);
    if (!(t in tops)) { tops[t] = 1; list.push({top: t, w: Math.round(rects[i].width),
                                               h: Math.round(rects[i].height * 10) / 10}); }
  }
  return list;
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
    var row = t.closest('.cart-line');
    NAMES.forEach(function (n) {
      [false, true].forEach(function (withFix) {
        var s = null;
        if (withFix) {
          s = d.createElement('style');
          s.textContent = '.cart-line__title { line-height: 1.45; }';
          d.head.appendChild(s);
        }
        t.textContent = n;
        void d.body.offsetHeight;
        var lines = textRects(t);
        out.push({
          width: W, chars: n.length, fix: withFix,
          lines: lines ? lines.length : -1,
          lineTops: lines ? lines.map(function (x) { return x.top; }) : [],
          boxH: Math.round(t.getBoundingClientRect().height * 10) / 10,
          boxW: Math.round(t.getBoundingClientRect().width),
          scrollH: t.scrollHeight,
          rowH: Math.round(row.getBoundingClientRect().height * 10) / 10,
          pageH: Math.round(d.body.getBoundingClientRect().height * 10) / 10
        });
        if (s) s.remove();
        void d.body.offsetHeight;
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
    p = os.path.join(S8, '_lbox.html')
    io.open(p, 'w', encoding='utf-8').write(html)
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8808'],
                           cwd=S8, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        outp = os.path.join(HERE, 'lbox.html')
        subprocess.call([EDGE, '--headless=new', '--disable-gpu',
                         '--user-data-dir=' + PROFILE, '--virtual-time-budget=20000',
                         '--dump-dom', 'http://127.0.0.1:8808/_lbox.html'],
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

    print('=== REAL LINE BOXES (Range over the text node) ===')
    print('  %-7s %-5s %-7s %-6s %-7s %-8s %-8s %s'
          % ('screen', 'chars', 'lh', 'lines', 'box h', 'scroll h', 'row h', 'page h'))
    for r in data:
        print('  %-7d %-5d %-7s %-6d %-7.1f %-8d %-8.1f %.1f'
              % (r['width'], r['chars'], '1.45' if r['fix'] else 'normal',
                 r['lines'], r['boxH'], r['scrollH'], r['rowH'], r['pageH']))

    print()
    print('=== DOES THE FIX CHANGE ANYTHING A CUSTOMER SEES? ===')
    pairs = {}
    for r in data:
        pairs.setdefault((r['width'], r['chars']), {})[r['fix']] = r
    anyvis = False
    for (w, c), d2 in sorted(pairs.items()):
        if False not in d2 or True not in d2:
            continue
        b, a = d2[False], d2[True]
        dh = a['boxH'] - b['boxH']
        dr = a['rowH'] - b['rowH']
        dp = a['pageH'] - b['pageH']
        vis = abs(dh) > 0.5 or abs(dr) > 0.5
        if vis:
            anyvis = True
        print('  %dpx / %d chars: %d line(s), title %+.1fpx, row %+.1fpx, page %+.1fpx  %s'
              % (w, c, b['lines'], dh, dr, dp, '<-- VISIBLE' if vis else 'no change'))

    print()
    if anyvis:
        print('VERDICT: the missing line-height is a real visual defect on wrapped')
        print('titles. Long product names are merchant data this theme cannot')
        print('constrain, so this is reachable in production.')
    else:
        print('VERDICT: no rendered difference at any tested width or length.')
