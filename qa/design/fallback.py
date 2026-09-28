# -*- coding: utf-8 -*-
"""Does any VISIBLE text render in a fallback typeface?

base.css sets `body { margin: 0 }` and no font-family. So the theme's two-
typeface rule is enforced by roughly sixty components each declaring
`font-family: var(--font-body)` or `var(--font-display)` individually, with no
inheritance to catch one that forgets. Anything missed renders Times New Roman,
and form controls render Arial, because the UA stylesheet does not inherit a
font into button/input/select/textarea.

The earlier scan found 36 such elements, but nearly all were .visually-hidden —
clipped to a 1px box and read only by a screen reader, where the typeface is
irrelevant. That is a very different finding from visible body copy in Times.

So this splits them: visible versus screen-reader-only. Only the visible ones
are a design defect today. The missing base rule is a separate, structural
finding either way, because it is why the next component to forget will render
in Times without anyone noticing.
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
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-fb')
PAGES = {
    8809: ['home.html', 's-collection.html', 's-collection-filters.html', 's-search.html',
           's-page.html', 's-404.html', 'c-page-note.html', 'c-page-empty.html'],
    8808: ['p-sizes.html', 'p-multi.html', 'p-details.html', 'c-many.html', 'c-empty.html'],
}

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var PAGES = PAGELIST, out = [], i = 0;
var THEME = ['Jost', 'Playfair Display', 'Kaushan Script'];
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
      var txt = '';
      for (var n = 0; n < el.childNodes.length; n++) {
        if (el.childNodes[n].nodeType === 3) txt += el.childNodes[n].nodeValue;
      }
      if (!txt.trim().length) return;
      var cs = w.getComputedStyle(el);
      var fam = cs.fontFamily.split(',')[0].replace(/['"]/g, '').trim();
      if (THEME.indexOf(fam) >= 0) return;
      var r = el.getBoundingClientRect();
      /* Screen-reader-only text is clipped to a ~1px box. Anything larger that
         is not display:none and not hidden is text a sighted user can read. */
      var srOnly = (r.width <= 2 && r.height <= 2) ||
                   /visually-hidden/.test((el.className || '').toString());
      var invisible = cs.display === 'none' || cs.visibility === 'hidden' ||
                      el.offsetParent === null;
      out.push({
        page: page, fam: fam, tag: el.tagName.toLowerCase(),
        cls: (el.className || '').toString().split(' ')[0] || '-',
        w: Math.round(r.width), h: Math.round(r.height),
        size: cs.fontSize,
        srOnly: srOnly, invisible: invisible,
        text: txt.trim().slice(0, 36)
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
    p = os.path.join(site, '_fb.html')
    io.open(p, 'w', encoding='utf-8').write(html)
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port)],
                           cwd=site, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        outp = os.path.join(HERE, 'fb-%d.html' % port)
        subprocess.call([EDGE, '--headless=new', '--disable-gpu',
                         '--user-data-dir=' + PROFILE, '--virtual-time-budget=30000',
                         '--dump-dom', 'http://127.0.0.1:%d/_fb.html' % port],
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

    visible = [r for r in rows if not r['srOnly'] and not r['invisible']]
    sr = [r for r in rows if r['srOnly']]
    hidden = [r for r in rows if r['invisible'] and not r['srOnly']]

    print('=== TEXT NOT IN A THEME TYPEFACE (%d elements) ===' % len(rows))
    print()
    print('  screen-reader-only (clipped, typeface irrelevant) : %d' % len(sr))
    print('  not rendered at all                               : %d' % len(hidden))
    print('  VISIBLE TO A SIGHTED USER                         : %d' % len(visible))
    print()

    if visible:
        print('--- THE VISIBLE ONES — these are real defects ---')
        for r in visible:
            print('  %-22s %-16s <%s.%s> %dx%d @%s'
                  % (r['page'][:22], r['fam'], r['tag'], r['cls'][:22], r['w'], r['h'], r['size']))
            print('       "%s"' % r['text'])
    else:
        print('--- NO VISIBLE TEXT renders in a fallback face. ---')
        print('    The two-typeface rule holds on screen. Every fallback is')
        print('    screen-reader-only text, where the typeface has no effect.')

    print()
    print('--- WHICH ELEMENTS FALL BACK, by class ---')
    for (cls, fam), n in Counter((r['cls'], r['fam']) for r in rows).most_common(15):
        print('  %-30s %-18s x%d' % (cls[:30], fam, n))
