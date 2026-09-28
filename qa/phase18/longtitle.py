# -*- coding: utf-8 -*-
"""Phase 18 — does the cart title line-height gap ever actually show?

blastradius.py proved the fix changes nothing on the fixture, and the reason is
that the fixture's product names fit on one line. That makes the earlier
"2 lines" reading an artifact: it divided scrollHeight by the used line-height
while a 24px min-height was propping scrollHeight up.

So the honest question is not "do these two rules differ" -- they do -- but
"does a customer ever see it". That depends entirely on whether a real product
name wraps in the cart. The fixtures use short names this project invented for
testing; a merchant's catalogue will not.

This substitutes progressively longer names into a cart title and a card title,
and reports the width at which each wraps and what the row does when it happens.
No merchant data is invented as fact -- these are probe strings for a layout
measurement, not catalogue content.
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
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-long')
# Lengths a real streetwear catalogue produces. Plain probe strings.
NAMES = [
    'Utility Cap',
    'Signature Oversized Tee',
    'Heavyweight Hoodie Cream',
    'Signature Oversized Heavyweight Tee',
    'Signature Oversized Heavyweight Tee Cream',
    'Faith Over Fear Signature Oversized Heavyweight Tee',
]

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var NAMES = NAMELIST, out = [];
var f = document.createElement('iframe');
f.style.cssText = 'border:0;width:1440px;height:2000px';
f.src = 'c-page-many.html';
document.body.appendChild(f);
f.onload = function () {
  var d = f.contentDocument, w = f.contentWindow;
  var t = d.querySelector('.cart-line__title');
  var row = t.closest('.cart-line');
  var orig = t.textContent;

  function snap(tag) {
    return {
      mode: tag,
      title: Math.round(t.getBoundingClientRect().height * 10) / 10,
      rects: t.getClientRects().length,
      row: Math.round(row.getBoundingClientRect().height * 10) / 10,
      page: Math.round(d.body.getBoundingClientRect().height * 10) / 10
    };
  }

  NAMES.forEach(function (n) {
    t.textContent = n;
    void d.body.offsetHeight;
    var before = snap('normal');
    /* Now apply the candidate and re-measure the same text. */
    var s = d.createElement('style');
    s.textContent = '.cart-line__title { line-height: 1.45; }';
    d.head.appendChild(s);
    void d.body.offsetHeight;
    var after = snap('1.45');
    s.remove();
    void d.body.offsetHeight;
    out.push({name: n, chars: n.length, before: before, after: after});
  });

  t.textContent = orig;
  document.title = 'DONE';
  document.getElementById('o').textContent = '<<<' + JSON.stringify(out) + '>>>';
};
</script>
"""

if __name__ == '__main__':
    S8 = os.path.abspath(os.path.join(HERE, '..', 'phase8', 'site'))
    html = PROBE.replace('NAMELIST', json.dumps(NAMES))
    p = os.path.join(S8, '_long.html')
    io.open(p, 'w', encoding='utf-8').write(html)
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8808'],
                           cwd=S8, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        outp = os.path.join(HERE, 'long.html')
        subprocess.call([EDGE, '--headless=new', '--disable-gpu',
                         '--user-data-dir=' + PROFILE, '--virtual-time-budget=20000',
                         '--dump-dom', 'http://127.0.0.1:8808/_long.html'],
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

    print('=== WHEN DOES A CART TITLE WRAP, AND DOES THE GAP THEN SHOW? ===')
    print('  %-52s %-4s %-18s %-18s %s'
          % ('product name', 'len', 'normal (today)', 'with 1.45', 'row'))
    visible = 0
    for r in data:
        b, a = r['before'], r['after']
        diff = abs(a['title'] - b['title'])
        rowdiff = abs(a['row'] - b['row'])
        if diff > 0.5:
            visible += 1
        print('  %-52s %-4d title %-11.1f title %-11.1f %s'
              % (r['name'][:52], r['chars'], b['title'], a['title'],
                 ('row %.1f -> %.1f' % (b['row'], a['row'])) if rowdiff > 0.5
                 else 'row unchanged (%.1f)' % b['row']))

    print()
    print('=== VERDICT ===')
    wrapped = [r for r in data if r['before']['rects'] > 1 or r['before']['title'] > 26]
    print('  names that wrap in the cart today: %d of %d' % (len(wrapped), len(data)))
    print('  names where the line-height gap is VISIBLE: %d of %d' % (visible, len(data)))
    if visible:
        print()
        print('  The gap is real and reachable. It is invisible on the short names')
        print('  the fixtures use and visible on names a real catalogue produces,')
        print('  which is exactly the kind of defect that ships.')
    else:
        print()
        print('  The gap never renders differently at any tested length. It is a')
        print('  token inconsistency with no visual consequence -- worth recording,')
        print('  not worth a change during a no-redesign phase.')
