# -*- coding: utf-8 -*-
"""Do the quantity steppers really render cursor:default, or did the probe lie?

review.py grouped controls by class and reported one row per group using
group[0] as the exemplar. That is fine for size but wrong for any property that
can differ between instances — and component-quantity.css:54 plainly declares
`cursor: pointer`, so the reported `default` is either a real cascade failure or
an artefact of which instance happened to be first.

This reads every instance individually instead of one exemplar, and also reports
whether it is the plus or the minus, whether it is aria-disabled, and what its
icon is — because an icon-only control with no border and no background gets its
entire affordance from the glyph, and if the glyph is missing there is nothing
to click.
"""
import io
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = os.environ.get('GS_BROWSER',
                      r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-qty')
PAGES = {8808: ['p-sizes.html', 'c-many.html', 'c-one.html'],
         8809: ['c-page-note.html']}

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var PAGES = PAGELIST, out = [], i = 0;
function step() {
  if (i >= PAGES.length) {
    document.title = 'DONE';
    document.getElementById('o').textContent = '<<<' + JSON.stringify(out) + '>>>';
    return;
  }
  var page = PAGES[i];
  var f = document.createElement('iframe');
  f.style.cssText = 'border:0;width:1440px;height:1400px';
  f.src = page;
  document.body.appendChild(f);
  f.onload = function () {
    var d = f.contentDocument, w = f.contentWindow;
    var htmlCls = d.documentElement.className;
    Array.prototype.forEach.call(d.querySelectorAll('.quantity__button'), function (el) {
      var r = el.getBoundingClientRect();
      var cs = w.getComputedStyle(el);
      var icon = el.querySelector('svg, .icon');
      out.push({
        page: page,
        htmlCls: htmlCls,
        name: el.getAttribute('name') || el.getAttribute('data-qty-step') || '-',
        cursor: cs.cursor,
        display: cs.display,
        bg: cs.backgroundColor,
        border: cs.borderTopWidth + ' ' + cs.borderTopStyle,
        w: Math.round(r.width), h: Math.round(r.height),
        rendered: el.offsetParent !== null,
        ariaDisabled: el.getAttribute('aria-disabled'),
        opacity: cs.opacity,
        hasIcon: !!icon,
        iconSize: icon ? Math.round(icon.getBoundingClientRect().width) : 0
      });
    });
    f.remove(); i++; step();
  };
  f.onerror = function () { f.remove(); i++; step(); };
}
step();
</script>
"""


def run(port, site, pages):
    avail = set(os.listdir(site))
    pages = [p for p in pages if p in avail]
    if not pages:
        return []
    html = PROBE.replace('PAGELIST', json.dumps(pages))
    p = os.path.join(site, '_qty.html')
    io.open(p, 'w', encoding='utf-8').write(html)
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port)],
                           cwd=site, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        outp = os.path.join(HERE, 'qty-%d.html' % port)
        subprocess.call([EDGE, '--headless=new', '--disable-gpu',
                         '--user-data-dir=' + PROFILE, '--virtual-time-budget=25000',
                         '--dump-dom', 'http://127.0.0.1:%d/_qty.html' % port],
                        stdout=io.open(outp, 'wb'), stderr=subprocess.DEVNULL)
        dom = io.open(outp, encoding='utf-8', errors='replace').read()
        m = re.search(r'&lt;&lt;&lt;(.*?)&gt;&gt;&gt;', dom, re.S) or \
            re.search(r'<<<(.*?)>>>', dom, re.S)
        return json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')) if m else []
    finally:
        srv.terminate()
        try:
            os.remove(p)
        except OSError:
            pass


if __name__ == '__main__':
    S9 = os.path.abspath(os.path.join(HERE, '..', 'phase9', 'site'))
    S8 = os.path.abspath(os.path.join(HERE, '..', 'phase8', 'site'))
    rows = run(8808, S8, PAGES[8808]) + run(8809, S9, PAGES[8809])

    print('=== EVERY QUANTITY STEPPER INSTANCE (%d) ===' % len(rows))
    print('  %-20s %-10s %-9s %-8s %-7s %-6s %-8s %s'
          % ('page', 'name', 'cursor', 'display', 'size', 'icon', 'opacity', 'html class'))
    for r in rows:
        print('  %-20s %-10s %-9s %-8s %-7s %-6s %-8s %s'
              % (r['page'][:20], r['name'][:10], r['cursor'], r['display'],
                 '%dx%d' % (r['w'], r['h']),
                 ('%dpx' % r['iconSize']) if r['hasIcon'] else 'NONE',
                 r['opacity'], r['htmlCls'][:22]))

    print()
    cur = Counter(r['cursor'] for r in rows)
    print('  cursors in use: %s' % dict(cur))
    noicon = [r for r in rows if not r['hasIcon']]
    print('  instances with NO icon glyph: %d' % len(noicon))
    print()
    if set(cur) == {'pointer'}:
        print('  VERDICT: every instance is cursor:pointer. review.py reported')
        print('  "default" because it used one exemplar per class group, and the')
        print('  exemplar it picked was not rendered. The finding was an artefact.')
    else:
        print('  VERDICT: cursor really is inconsistent across instances.')
