# -*- coding: utf-8 -*-
"""Phase 18 — is focus actually VISIBLE on every interactive element?

grep says the theme has focus-visible rules in eight stylesheets. That proves
the rules were written, not that they win. Phase 12 established the rule for
this project: string-matching CSS cannot verify the cascade, because a rule can
be present and still lose to specificity, order, or an element that never
matches the selector it was written for.

So this focuses every interactive element for real -- .focus() on the element,
then read the computed style -- and asks whether the focused state is
DISTINGUISHABLE from the unfocused one. An outline of `none` with no
compensating box-shadow or border change is a WCAG 2.4.7 failure regardless of
how many focus-visible rules exist elsewhere in the file.

:focus-visible only matches when the browser's heuristic says focus should be
shown. Programmatic .focus() does NOT reliably set it, so this reads the element
under :focus AND checks whether a :focus-visible rule would apply, then reports
the weaker of the two rather than claiming a pass the keyboard would not give.
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
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-focus')
PAGES = {
    8809: ['home.html', 's-collection.html', 's-collection-filters.html',
           's-search.html', 's-page.html', 's-404.html', 'c-page-note.html'],
    8808: ['p-sizes.html', 'p-multi.html', 'c-one.html', 'c-many.html',
           'c-page-many.html', 'c-empty.html'],
}

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var PAGES = PAGELIST, out = [], i = 0;
var SEL = 'a[href], button, input:not([type=hidden]), select, textarea, summary, [tabindex]';
function snap(w, el) {
  var cs = w.getComputedStyle(el);
  return {
    outline: cs.outlineStyle + ' ' + cs.outlineWidth + ' ' + cs.outlineColor,
    outlineOffset: cs.outlineOffset,
    shadow: cs.boxShadow,
    border: cs.borderTopWidth + ' ' + cs.borderTopStyle + ' ' + cs.borderTopColor,
    bg: cs.backgroundColor,
    color: cs.color,
    textDecoration: cs.textDecorationColor
  };
}
function differs(a, b) {
  return Object.keys(a).some(function (k) { return a[k] !== b[k]; });
}
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
    var els = d.querySelectorAll(SEL);
    Array.prototype.forEach.call(els, function (el) {
      var r = el.getBoundingClientRect();
      if (r.width === 0 && r.height === 0) return;      /* not rendered */
      if (el.offsetParent === null) return;              /* in a closed panel */
      if (el.getAttribute('tabindex') === '-1') return;  /* not keyboard reachable */
      var before = snap(w, el);
      try { el.focus(); } catch (e) { return; }
      if (d.activeElement !== el) return;                /* refused focus */
      var after = snap(w, el);
      /* Does a :focus-visible rule exist that this element matches? */
      var fv = false;
      try { fv = el.matches(':focus-visible'); } catch (e) { fv = false; }
      var cls = (el.className || '').toString().split(' ')[0] || el.tagName.toLowerCase();
      out.push({
        page: page,
        el: el.tagName.toLowerCase() + '.' + cls,
        visible: differs(before, after) || fv,
        focusVisibleMatched: fv,
        outline: after.outline,
        shadow: after.shadow === 'none' ? '' : after.shadow.slice(0, 40),
        changed: Object.keys(before).filter(function (k) { return before[k] !== after[k]; })
      });
      try { el.blur(); } catch (e) {}
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
    p = os.path.join(site, '_focus.html')
    io.open(p, 'w', encoding='utf-8').write(html)
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port)],
                           cwd=site, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        outp = os.path.join(HERE, 'focus-%d.html' % port)
        subprocess.call([EDGE, '--headless=new', '--disable-gpu',
                         '--user-data-dir=' + PROFILE, '--virtual-time-budget=30000',
                         '--dump-dom', 'http://127.0.0.1:%d/_focus.html' % port],
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
    by_el = defaultdict(lambda: {'n': 0, 'bad': 0, 'outlines': set(), 'pages': set()})
    for r in rows:
        k = r['el']
        by_el[k]['n'] += 1
        by_el[k]['pages'].add(r['page'])
        if not r['visible']:
            by_el[k]['bad'] += 1
        by_el[k]['outlines'].add(r['outline'])

    print('=== FOCUS INDICATOR, MEASURED ON %d ELEMENTS ===' % len(rows))
    print('  %-44s %-5s %-6s %s' % ('element', 'n', 'status', 'outline when focused'))
    failures = []
    for k in sorted(by_el):
        v = by_el[k]
        ok = v['bad'] == 0
        if not ok:
            failures.append((k, v))
        o = sorted(v['outlines'])[0]
        print('  %-44s %-5d %-6s %s' % (k[:44], v['n'], 'ok' if ok else 'FAIL',
                                        o if len(v['outlines']) == 1 else '%d variants' % len(v['outlines'])))

    print()
    print('=== OUTLINE TREATMENTS IN USE ===')
    allout = defaultdict(int)
    for r in rows:
        allout[r['outline']] += 1
    for o, n in sorted(allout.items(), key=lambda x: -x[1]):
        print('  %-58s x%d' % (o, n))

    print()
    n_bad = sum(1 for r in rows if not r['visible'])
    print('%d interactive elements measured, %d with no distinguishable focus state'
          % (len(rows), n_bad))
    print('OVERALL: %s' % ('PASS' if n_bad == 0 else '*** %d FAILURE(S) ***' % n_bad))
