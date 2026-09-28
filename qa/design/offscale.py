# -*- coding: utf-8 -*-
"""Which elements use spacing that is not on the scale, and is it deliberate?

review.py found 8.9% of spacing declarations resolve to values outside the
--space-1..10 scale. A percentage is not actionable; the elements are. This
names each one so every off-scale value can be judged individually.

Expected legitimate sources, which must be recognised rather than reported as
drift:
  - --section-pad-block is clamp(40px, 6vw, 96px), so at 1440 it resolves to
    86.4px, and to 85.5px once a scrollbar takes 15px off the viewport. A fluid
    value is SUPPOSED to land between scale steps; that is the point of it.
  - .visually-hidden sets margin: -1px, so 1px appears 20+ times and is the
    screen-reader utility, not a spacing decision.
  - em- and ch-relative padding resolves against the element's own font size,
    so 6px / 11px / 15px can come from a proportional value that is correct.
  - auto margins on a centred container resolve to whatever half the leftover
    space is, which is why 284.5px and 170px appear.

What is left after those are set aside is the real answer to "is spacing
consistent".
"""
import io
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = os.environ.get('GS_BROWSER',
                      r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-offscale')
SCALE = {4, 8, 12, 16, 24, 32, 40, 48, 64, 96}

PAGES = {
    8809: ['home.html', 's-collection.html', 's-collection-filters.html', 's-search.html',
           's-page.html', 's-404.html', 'c-page-note.html'],
    8808: ['p-sizes.html', 'p-multi.html', 'c-many.html', 'c-empty.html'],
}

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var PAGES = PAGELIST, SCALE = SCALEHERE, out = [], i = 0;
var PROPS = ['marginTop','marginBottom','marginLeft','marginRight',
             'paddingTop','paddingBottom','paddingLeft','paddingRight',
             'rowGap','columnGap'];
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
    Array.prototype.forEach.call(d.querySelectorAll('*'), function (el) {
      if (el.offsetParent === null && el.tagName !== 'BODY') return;
      var r = el.getBoundingClientRect();
      if (r.width === 0 && r.height === 0) return;
      var cs = w.getComputedStyle(el);
      PROPS.forEach(function (p) {
        var v = Math.round(parseFloat(cs[p]) * 10) / 10;
        if (!v || v <= 0) return;
        if (SCALE.indexOf(Math.round(v)) >= 0) return;
        out.push({
          page: page, prop: p, value: v,
          cls: (el.className || '').toString().split(' ')[0] || el.tagName.toLowerCase(),
          tag: el.tagName.toLowerCase(),
          fontSize: cs.fontSize
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
    avail = set(os.listdir(site))
    pages = [p for p in pages if p in avail]
    if not pages:
        return []
    html = (PROBE.replace('PAGELIST', json.dumps(pages))
                 .replace('SCALEHERE', json.dumps(sorted(SCALE))))
    p = os.path.join(site, '_offscale.html')
    io.open(p, 'w', encoding='utf-8').write(html)
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port)],
                           cwd=site, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        outp = os.path.join(HERE, 'offscale-%d.html' % port)
        subprocess.call([EDGE, '--headless=new', '--disable-gpu',
                         '--user-data-dir=' + PROFILE, '--virtual-time-budget=30000',
                         '--dump-dom', 'http://127.0.0.1:%d/_offscale.html' % port],
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


def classify(v, cls, prop):
    if 80 <= v <= 100:
        return 'fluid --section-pad-block clamp(40px, 6vw, 96px)'
    if v == 1 and 'visually-hidden' in cls:
        return 'the .visually-hidden utility (margin: -1px)'
    if v > 120 and prop in ('marginLeft', 'marginRight'):
        return 'auto margin on a centred container'
    return None


if __name__ == '__main__':
    S9 = os.path.abspath(os.path.join(HERE, '..', 'phase9', 'site'))
    S8 = os.path.abspath(os.path.join(HERE, '..', 'phase8', 'site'))
    rows = run(8809, S9, PAGES[8809]) + run(8808, S8, PAGES[8808])

    explained, unexplained = defaultdict(list), defaultdict(list)
    for r in rows:
        why = classify(r['value'], r['cls'], r['prop'])
        (explained if why else unexplained)[(r['value'], r['cls'], r['prop'])].append((r, why))

    print('=== OFF-SCALE SPACING: %d declaration(s) ===' % len(rows))
    print()
    print('--- EXPLAINED (deliberate, not drift) ---')
    seen = set()
    for (v, cls, prop), items in sorted(explained.items()):
        why = items[0][1]
        if why in seen:
            continue
        seen.add(why)
        n = sum(len(i) for (vv, cc, pp), i in explained.items() if explained[(vv, cc, pp)][0][1] == why)
        print('  %-56s %d declaration(s)' % (why, n))
    print()
    print('--- NOT EXPLAINED — judge these individually ---')
    print('  %-9s %-30s %-15s %-8s %s' % ('value', 'element', 'property', 'font', 'n'))
    tot = 0
    for (v, cls, prop), items in sorted(unexplained.items(), key=lambda x: -len(x[1])):
        tot += len(items)
        fs = items[0][0]['fontSize']
        em = v / float(fs.replace('px', '')) if fs.endswith('px') else 0
        note = ''
        if abs(em - round(em * 4) / 4) < 0.02 and em > 0:
            note = '  = %.2fem of its own font size' % em
        print('  %-9s %-30s %-15s %-8s %d%s'
              % ('%gpx' % v, cls[:30], prop, fs, len(items), note))
    print()
    print('  %d explained, %d to judge' % (len(rows) - tot, tot))
