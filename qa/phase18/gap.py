# -*- coding: utf-8 -*-
"""Phase 18 — measure the vertical gaps down the collection page.

The claim is that the first filter row sits flush against the collection
description — 0px — while the same page leaves 40px above its toolbar when a
merchant has no filters configured. That is a rendered-geometry claim, so it is
measured rather than read out of the stylesheet.

Runs against the filtered page and the unfiltered one, before and after the
candidate fix, so the "0 or 40 depending on a setting" contradiction is either
reproduced or dismissed on evidence.
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
SITE = os.path.abspath(os.path.join(HERE, '..', 'phase9', 'site'))
EDGE = os.environ.get('GS_BROWSER',
                      r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-gap')
PORT = 8809

PAGES = ['s-collection-filters.html', 's-collection.html']
CANDIDATE = '.main-collection__header { margin-block-end: var(--space-7); }'

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var PAGES = PAGELIST, CSS = 'CSSHERE', out = [], i = 0;
function gaps(d) {
  /* Walk the real children of the collection inner column and report the
     vertical distance between each pair, which is what a customer sees
     regardless of which element's margin produced it. */
  var inner = d.querySelector('.main-collection__inner');
  if (!inner) return null;
  var kids = Array.prototype.filter.call(inner.children, function (el) {
    var r = el.getBoundingClientRect();
    return r.height > 0 || r.width > 0;
  });
  var rows = [];
  for (var n = 0; n < kids.length; n++) {
    var r = kids[n].getBoundingClientRect();
    var name = (kids[n].className || kids[n].tagName).toString().split(' ')[0];
    var gap = null;
    if (n > 0) {
      var prev = kids[n - 1].getBoundingClientRect();
      gap = Math.round((r.top - prev.bottom) * 10) / 10;
    }
    rows.push({el: name, gap: gap, h: Math.round(r.height)});
  }
  return rows;
}
function step() {
  if (i >= PAGES.length) {
    document.title = 'DONE';
    document.getElementById('o').textContent = '<<<' + JSON.stringify(out) + '>>>';
    return;
  }
  var f = document.createElement('iframe');
  f.style.cssText = 'border:0;width:1440px;height:1400px';
  f.src = PAGES[i];
  document.body.appendChild(f);
  f.onload = function () {
    var d = f.contentDocument;
    var before = gaps(d);
    var s = d.createElement('style');
    s.textContent = CSS;
    d.head.appendChild(s);
    void d.body.offsetHeight;
    var after = gaps(d);
    out.push({page: PAGES[i], before: before, after: after});
    f.remove(); i++; step();
  };
  f.onerror = function () { out.push({page: PAGES[i], error: 'load failed'}); f.remove(); i++; step(); };
}
step();
</script>
"""

if __name__ == '__main__':
    html = (PROBE.replace('PAGELIST', json.dumps(PAGES))
                 .replace('CSSHERE', CANDIDATE.replace("'", "\\'")))
    p = os.path.join(SITE, '_gap.html')
    io.open(p, 'w', encoding='utf-8').write(html)
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)],
                           cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        outp = os.path.join(HERE, 'gap.html')
        subprocess.call([EDGE, '--headless=new', '--disable-gpu',
                         '--user-data-dir=' + PROFILE, '--virtual-time-budget=20000',
                         '--dump-dom', 'http://127.0.0.1:%d/_gap.html' % PORT],
                        stdout=io.open(outp, 'wb'), stderr=subprocess.DEVNULL)
        dom = io.open(outp, encoding='utf-8', errors='replace').read()
        m = re.search(r'&lt;&lt;&lt;(.*?)&gt;&gt;&gt;', dom, re.S) or \
            re.search(r'<<<(.*?)>>>', dom, re.S)
        if not m:
            raise SystemExit('*** no payload ***')
        data = json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&'))
    finally:
        srv.terminate()
        try:
            os.remove(p)
        except OSError:
            pass

    print('=== VERTICAL GAPS INSIDE .main-collection__inner (1440px) ===')
    print('candidate: %s' % CANDIDATE)
    for rec in data:
        print()
        print('  %s' % rec['page'])
        if rec.get('error'):
            print('    %s' % rec['error'])
            continue
        print('    %-34s %-12s %-12s' % ('element', 'gap before', 'gap after'))
        for b, a in zip(rec['before'], rec['after']):
            mark = ''
            if b['gap'] is not None and a['gap'] is not None and abs(a['gap'] - b['gap']) > 0.5:
                mark = '  <- moved'
            print('    %-34s %-12s %-12s%s'
                  % (b['el'],
                     '-' if b['gap'] is None else '%.0fpx' % b['gap'],
                     '-' if a['gap'] is None else '%.0fpx' % a['gap'], mark))
