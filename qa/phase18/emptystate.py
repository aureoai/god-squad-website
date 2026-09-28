# -*- coding: utf-8 -*-
"""Phase 18 — is the empty-state line really a second copy of the page heading?

The claim: .cart-empty__title and .main-collection__empty-title carry the same
four type declarations as their own page's <h1>, and the <h1> renders
unconditionally above them — so an empty cart shows two stacked lines at
identical size, weight and case, one of which is a <p>. The search page sets its
equivalent one step down instead, so three empty states ship two treatments.

Read off the stylesheet that is three rules and a guess about what renders. This
measures what is actually on the page: every heading-ish element in document
order with its computed type, so a duplicated level is visible as two adjacent
rows with the same signature.
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
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-empty')
# (port, page, human label)
PAGES = [
    (8809, 'c-page-empty.html', 'empty cart page'),
    (8809, 's-search-none.html', 'search, no results'),
    (8809, 's-collection-empty.html', 'collection, no products'),
]

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var PAGES = PAGELIST, out = [], i = 0;
var SEL = 'h1, h2, h3, [class*="__title"], [class*="empty-title"], [class*="__heading"]';
function step() {
  if (i >= PAGES.length) {
    document.title = 'DONE';
    document.getElementById('o').textContent = '<<<' + JSON.stringify(out) + '>>>';
    return;
  }
  var t = PAGES[i];
  var f = document.createElement('iframe');
  f.style.cssText = 'border:0;width:1440px;height:1200px';
  f.src = t.page;
  document.body.appendChild(f);
  f.onload = function () {
    var d = f.contentDocument, w = f.contentWindow;
    var rec = {label: t.label, page: t.page, items: []};
    Array.prototype.forEach.call(d.querySelectorAll(SEL), function (el) {
      var r = el.getBoundingClientRect();
      if (r.width === 0 && r.height === 0) return;
      if (el.offsetParent === null) return;
      var cs = w.getComputedStyle(el);
      rec.items.push({
        tag: el.tagName.toLowerCase(),
        cls: (el.className || '').toString().split(' ')[0] || '-',
        sig: [cs.fontFamily.split(',')[0].replace(/['"]/g, ''),
              Math.round(parseFloat(cs.fontSize)) + 'px', cs.fontWeight,
              cs.textTransform].join(' | '),
        text: (el.textContent || '').trim().slice(0, 30),
        top: Math.round(r.top)
      });
    });
    rec.items.sort(function (a, b) { return a.top - b.top; });
    out.push(rec);
    f.remove(); i++; step();
  };
  f.onerror = function () { out.push({label: t.label, page: t.page, error: 'no such page'}); f.remove(); i++; step(); };
}
step();
</script>
"""


def run(port, site, pages):
    html = PROBE.replace('PAGELIST', json.dumps(pages))
    p = os.path.join(site, '_empty.html')
    io.open(p, 'w', encoding='utf-8').write(html)
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port)],
                           cwd=site, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        outp = os.path.join(HERE, 'empty-%d.html' % port)
        subprocess.call([EDGE, '--headless=new', '--disable-gpu',
                         '--user-data-dir=' + PROFILE, '--virtual-time-budget=20000',
                         '--dump-dom', 'http://127.0.0.1:%d/_empty.html' % port],
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
    avail = {8809: set(os.listdir(S9)), 8808: set(os.listdir(S8))}
    rows = []
    for port, site in ((8809, S9), (8808, S8)):
        ps = [{'page': p, 'label': l} for (pt, p, l) in PAGES
              if pt == port and p in avail[port]]
        missing = [p for (pt, p, l) in PAGES if pt == port and p not in avail[port]]
        for mp in missing:
            print('  (no fixture: %s)' % mp)
        if ps:
            rows += run(port, site, ps)

    print()
    print('=== HEADINGS IN DOCUMENT ORDER ===')
    for rec in rows:
        print()
        print('  %s  (%s)' % (rec['label'], rec['page']))
        if rec.get('error'):
            print('    %s' % rec['error'])
            continue
        seen = {}
        for it in rec['items']:
            dup = ''
            if it['sig'] in seen:
                dup = '  <-- SAME TYPE AS <%s>.%s' % (seen[it['sig']][0], seen[it['sig']][1])
            else:
                seen[it['sig']] = (it['tag'], it['cls'])
            print('    <%-3s> %-32s %-44s %s%s'
                  % (it['tag'], it['cls'][:32], it['sig'], it['text'][:22], dup))
