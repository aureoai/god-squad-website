# -*- coding: utf-8 -*-
"""Phase 18 — name the elements behind the remaining h2/h3 drift.

The coherence table groups by ROLE, and it uses the bare tag as the proxy for
"section heading" and "sub heading". That is the right default — it catches
headings no class list would have thought to include — but it means a reported
drift can be two unrelated components that merely share a tag rather than one
component rendering inconsistently.

Telling those apart is the whole decision, so this prints the class of every
matching element beside its signature. Drift between .product-card__title and
.our-story__value-title is two components; drift between two instances of the
SAME class is a defect.
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
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-h3')
PAGES = {
    8809: ['home.html', 's-collection.html', 's-search.html', 's-page.html', 's-404.html'],
    8808: ['p-sizes.html', 'c-many.html'],
}

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
  var f = document.createElement('iframe');
  f.style.cssText = 'border:0;width:1440px;height:900px';
  f.src = PAGES[i];
  document.body.appendChild(f);
  f.onload = function () {
    var d = f.contentDocument, w = f.contentWindow, page = PAGES[i];
    ['h2', 'h3'].forEach(function (tag) {
      Array.prototype.forEach.call(d.querySelectorAll(tag), function (el) {
        var r = el.getBoundingClientRect();
        if (r.width === 0 && r.height === 0) return;
        if (el.offsetParent === null) return;
        var cs = w.getComputedStyle(el);
        out.push({
          page: page, tag: tag,
          cls: (el.className || '').toString().split(' ')[0] || '(no class)',
          sig: [cs.fontFamily.split(',')[0].replace(/['"]/g, ''), cs.fontSize,
                cs.fontWeight, cs.lineHeight, cs.letterSpacing,
                cs.textTransform].join(' | '),
          text: (el.textContent || '').trim().slice(0, 28)
        });
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
    html = PROBE.replace('PAGELIST', json.dumps(pages))
    p = os.path.join(site, '_h3.html')
    io.open(p, 'w', encoding='utf-8').write(html)
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port)],
                           cwd=site, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        outp = os.path.join(HERE, 'h3-%d.html' % port)
        subprocess.call([EDGE, '--headless=new', '--disable-gpu',
                         '--user-data-dir=' + PROFILE, '--virtual-time-budget=20000',
                         '--dump-dom', 'http://127.0.0.1:%d/_h3.html' % port],
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
    rows = run(8809, S9, PAGES[8809]) + run(8808, S8, PAGES[8808])

    from collections import defaultdict
    by_class = defaultdict(set)
    for r in rows:
        by_class[(r['tag'], r['cls'])].add(r['sig'])

    print('=== EVERY HEADING, BY CLASS ===')
    print('  %-5s %-34s %-4s %s' % ('tag', 'class', 'sigs', 'signature'))
    real = []
    for (tag, cls), sigs in sorted(by_class.items()):
        for n, s in enumerate(sorted(sigs)):
            print('  %-5s %-34s %-4s %s' % (tag if n == 0 else '', cls if n == 0 else '',
                                            len(sigs) if n == 0 else '', s))
        if len(sigs) > 1:
            real.append((tag, cls, sigs))

    print()
    print('=== THE DISTINCTION THAT MATTERS ===')
    if real:
        print('  ONE CLASS rendering more than one way -- these are defects:')
        for tag, cls, sigs in real:
            print('    %s.%s -> %d signatures' % (tag, cls, len(sigs)))
            for s in sorted(sigs):
                print('        %s' % s)
    else:
        print('  No class renders more than one way. Every signature difference')
        print('  reported at the ROLE level is between DIFFERENT components that')
        print('  share a heading tag, which is design, not drift.')
