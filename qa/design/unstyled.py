# -*- coding: utf-8 -*-
"""Which elements render with BROWSER DEFAULTS, and are they the theme or the harness?

review.py reported four typefaces where the theme declares two, plus black text
and rgb(0,0,238) — the user-agent link blue. That combination means elements are
rendering with no theme CSS applied at all.

Before any of it is written down as a design defect, it has to be established
WHOSE elements they are. The QA harness wraps real theme output in its own
scaffolding, and Phase 9 recorded the lesson: confirm the fixture renders the
element before trusting what you measured about it.

So this names every element whose first declared font family is not one of the
theme's two, or whose colour is a UA default, and prints its ancestry. If the
ancestry is harness chrome, the finding is an artifact and must be reported as
such. If it is inside a theme section, it is real.
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
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-unstyled')
PAGES = {
    8809: ['home.html', 's-collection.html', 's-search.html', 's-page.html', 's-404.html'],
    8808: ['p-sizes.html', 'c-many.html'],
}

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var PAGES = PAGELIST, out = [], i = 0;
var THEME_FAMS = ['Jost', 'Playfair Display', 'Kaushan Script'];
function chain(el) {
  var parts = [], n = el, guard = 0;
  while (n && n.tagName !== 'HTML' && guard++ < 8) {
    var c = (n.className || '').toString().split(' ')[0];
    parts.unshift(n.tagName.toLowerCase() + (c ? '.' + c : ''));
    n = n.parentElement;
  }
  return parts.join(' > ');
}
function step() {
  if (i >= PAGES.length) {
    document.title = 'DONE';
    document.getElementById('o').textContent = '<<<' + JSON.stringify(out) + '>>>';
    return;
  }
  var page = PAGES[i];
  var f = document.createElement('iframe');
  f.style.cssText = 'border:0;width:1440px;height:1200px';
  f.src = page;
  document.body.appendChild(f);
  f.onload = function () {
    var d = f.contentDocument, w = f.contentWindow;
    Array.prototype.forEach.call(d.querySelectorAll('*'), function (el) {
      if (el.offsetParent === null && el.tagName !== 'BODY') return;
      var r = el.getBoundingClientRect();
      if (r.width === 0 && r.height === 0) return;
      var txt = '';
      for (var n = 0; n < el.childNodes.length; n++) {
        if (el.childNodes[n].nodeType === 3) txt += el.childNodes[n].nodeValue;
      }
      if (!txt.trim().length) return;
      var cs = w.getComputedStyle(el);
      var fam = cs.fontFamily.split(',')[0].replace(/['"]/g, '').trim();
      var uaColor = (cs.color === 'rgb(0, 0, 0)' || cs.color === 'rgb(0, 0, 238)');
      if (THEME_FAMS.indexOf(fam) >= 0 && !uaColor) return;
      out.push({
        page: page,
        fam: fam,
        color: cs.color,
        size: cs.fontSize,
        chain: chain(el),
        text: txt.trim().slice(0, 40),
        inSection: !!el.closest('.shopify-section, section, header, footer')
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
    p = os.path.join(site, '_unstyled.html')
    io.open(p, 'w', encoding='utf-8').write(html)
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port)],
                           cwd=site, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        outp = os.path.join(HERE, 'unstyled-%d.html' % port)
        subprocess.call([EDGE, '--headless=new', '--disable-gpu',
                         '--user-data-dir=' + PROFILE, '--virtual-time-budget=30000',
                         '--dump-dom', 'http://127.0.0.1:%d/_unstyled.html' % port],
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

    print('=== ELEMENTS NOT RENDERING IN A THEME TYPEFACE / COLOUR (%d) ===' % len(rows))
    print()
    inside = [r for r in rows if r['inSection']]
    outside = [r for r in rows if not r['inSection']]
    print('  inside a theme section : %d   <-- these would be REAL defects' % len(inside))
    print('  outside any section    : %d   <-- harness scaffolding' % len(outside))
    print()

    print('--- ANCESTRY, grouped ---')
    ch = Counter((r['chain'].split(' > ')[0], r['fam'], r['inSection']) for r in rows)
    for (root, fam, ins), n in ch.most_common(20):
        print('  %-28s %-20s in-section=%-5s x%d' % (root[:28], fam, ins, n))

    if inside:
        print()
        print('--- THE ONES INSIDE A THEME SECTION (real if any) ---')
        for r in inside[:25]:
            print('  %-22s %-18s %-20s %s' % (r['page'][:22], r['fam'], r['color'], r['chain'][-60:]))
            print('       text: %s' % r['text'])

    print()
    print('--- SAMPLE OF THE HARNESS ONES ---')
    for r in outside[:8]:
        print('  %-22s %-18s %s' % (r['page'][:22], r['fam'], r['chain'][:70]))
        print('       text: %s' % r['text'])
