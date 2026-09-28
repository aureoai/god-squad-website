# -*- coding: utf-8 -*-
"""Phase 18 — what would giving .cart-line__title a line-height actually move?

The defect is confirmed: the same product name wraps to two lines on a card and
in the cart, and the two render 3.4px apart per line because the card sets a
line-height and the cart inherits `normal`. The fix is one declaration. The
question this answers is what ELSE moves when it lands.

Method: apply the candidate declaration in the page itself, then measure the
cart line, its row, the panel and the page before and after. Nothing is written
to the theme — the rule is injected into a live copy, which is the cheapest way
to find out whether a one-line fix is really a one-line fix.

The rows that matter are the CONTAINERS. A title growing 6.8px inside a 44px
minimum is invisible; a title growing a row is a layout change, and Phase 18 is
explicitly not a redesign.
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
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-blast')
CANDIDATE = '.cart-line__title { line-height: 1.45; }'

# Everything the change could plausibly reach, from the element outwards.
WATCH = [
    ('.cart-line__title', 'the title itself'),
    ('.cart-line', 'the cart row'),
    ('.cart-line__details', 'the row text column'),
    ('.cart-line__media', 'the row image'),
    ('.main-cart__lines', 'the list of rows'),
    ('.main-cart__inner', 'the cart column'),
    ('.cart-totals', 'the totals panel'),
    ('body', 'the page'),
]

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var PAGE = 'PAGEHERE', WATCH = WATCHLIST, CSS = 'CSSHERE';
var out = {before: {}, after: {}, titles: {before: [], after: []}};
function measure(d, bucket) {
  WATCH.forEach(function (w) {
    var els = d.querySelectorAll(w[0]);
    var hs = [];
    Array.prototype.forEach.call(els, function (el) {
      hs.push(Math.round(el.getBoundingClientRect().height * 10) / 10);
    });
    out[bucket][w[0]] = hs;
  });
  var ts = d.querySelectorAll('.cart-line__title');
  Array.prototype.forEach.call(ts, function (el) {
    out.titles[bucket].push({
      h: Math.round(el.getBoundingClientRect().height * 10) / 10,
      scroll: el.scrollHeight,
      text: (el.textContent || '').trim().slice(0, 30)
    });
  });
}
var f = document.createElement('iframe');
f.style.cssText = 'border:0;width:1440px;height:2000px';
f.src = PAGE;
document.body.appendChild(f);
f.onload = function () {
  var d = f.contentDocument;
  measure(d, 'before');
  /* NEGATIVE CONTROL. A probe that reports "nothing moved" is worthless until
     it has proved it can see a change at all. Read the computed line-height
     back after injecting, and record whether the rule actually won. */
  var t0 = d.querySelector('.cart-line__title');
  out.control = {before: t0 ? f.contentWindow.getComputedStyle(t0).lineHeight : 'no element'};
  var s = d.createElement('style');
  s.textContent = CSS;
  d.head.appendChild(s);
  /* Force layout before reading back. */
  void d.body.offsetHeight;
  out.control.after = t0 ? f.contentWindow.getComputedStyle(t0).lineHeight : 'no element';
  out.control.applied = out.control.before !== out.control.after;
  out.control.display = t0 ? f.contentWindow.getComputedStyle(t0).display : '-';
  out.control.minHeight = t0 ? f.contentWindow.getComputedStyle(t0).minHeight : '-';
  out.control.childRects = t0 ? t0.getClientRects().length : 0;
  measure(d, 'after');
  document.title = 'DONE';
  document.getElementById('o').textContent = '<<<' + JSON.stringify(out) + '>>>';
};
</script>
"""


def run(port, site, page):
    html = (PROBE.replace('PAGEHERE', page)
                 .replace('WATCHLIST', json.dumps([[s, d] for s, d in WATCH]))
                 .replace('CSSHERE', CANDIDATE.replace("'", "\\'")))
    p = os.path.join(site, '_blast.html')
    io.open(p, 'w', encoding='utf-8').write(html)
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port)],
                           cwd=site, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        out = os.path.join(HERE, 'blast-%d.html' % port)
        subprocess.call([EDGE, '--headless=new', '--disable-gpu',
                         '--user-data-dir=' + PROFILE, '--virtual-time-budget=20000',
                         '--dump-dom', 'http://127.0.0.1:%d/_blast.html' % port],
                        stdout=io.open(out, 'wb'), stderr=subprocess.DEVNULL)
        dom = io.open(out, encoding='utf-8', errors='replace').read()
        m = re.search(r'&lt;&lt;&lt;(.*?)&gt;&gt;&gt;', dom, re.S) or \
            re.search(r'<<<(.*?)>>>', dom, re.S)
        if not m:
            print('  *** no payload ***')
            return None
        return json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&'))
    finally:
        srv.terminate()
        try:
            os.remove(p)
        except OSError:
            pass


if __name__ == '__main__':
    S8 = os.path.abspath(os.path.join(HERE, '..', 'phase8', 'site'))
    r = run(8808, S8, 'c-page-many.html')
    if not r:
        raise SystemExit(1)

    print('=== CANDIDATE: %s ===' % CANDIDATE)
    c = r.get('control', {})
    print('  negative control: line-height %s -> %s   %s'
          % (c.get('before'), c.get('after'),
             'rule APPLIED' if c.get('applied') else '*** RULE NEVER APPLIED ***'))
    print('  element: display=%s min-height=%s client-rects=%s'
          % (c.get('display'), c.get('minHeight'), c.get('childRects')))
    if not c.get('applied'):
        print()
        print('  Everything below is meaningless until that reads APPLIED.')
    print()
    print('  %-24s %-28s %-28s %s' % ('element', 'before', 'after', 'verdict'))
    moved = []
    for sel, desc in WATCH:
        b, a = r['before'].get(sel, []), r['after'].get(sel, [])
        same = b == a
        if not same:
            moved.append((sel, desc, b, a))
        print('  %-24s %-28s %-28s %s'
              % (sel, str(b)[:27], str(a)[:27], 'unchanged' if same else '*** MOVED ***'))

    print()
    print('=== THE TITLES THEMSELVES ===')
    for i, (b, a) in enumerate(zip(r['titles']['before'], r['titles']['after'])):
        note = ''
        if b['scroll'] != a['scroll']:
            note = '  text block %d -> %dpx' % (b['scroll'], a['scroll'])
        print('  %-32s box %.1f -> %.1f%s' % (b['text'], b['h'], a['h'], note))

    print()
    if not moved:
        print('VERDICT: nothing outside the title moves. The 44px tap-target')
        print('minimum absorbs the extra leading, so this is a contained fix:')
        print('the text is spaced correctly and no row, panel or page reflows.')
    else:
        print('VERDICT: %d container(s) move. This is NOT a contained fix --' % len(moved))
        for sel, desc, b, a in moved:
            print('  %s (%s): %s -> %s' % (sel, desc, b, a))
