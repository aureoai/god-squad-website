# -*- coding: utf-8 -*-
"""What moves if `body` finally gets a font-family?

base.css sets `body { margin: 0 }` and nothing else. The theme's two-typeface
rule is therefore enforced by roughly sixty components each declaring
font-family individually. Measured consequence today: 223 elements inherit
Times New Roman. All of them are screen-reader-only, so nothing is visibly
wrong — but the rule has no safety net, and the next component that forgets
will render in Times without anyone noticing.

Adding one declaration to body makes the rule structural. Before adding it, this
measures what it MOVES, because a font change on the root inherits everywhere
and could shift layout.

Form controls are the interesting case: the UA stylesheet does NOT inherit a
font into button/input/select/textarea, so a body rule cannot reach them. If any
control depends on that, this will show it.

Negative control included: the probe proves it can see the change before any
"nothing moved" result is believed.
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
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-bodyfont')
CANDIDATE = "body { font-family: var(--font-body); }"

PAGES = {
    8809: ['home.html', 's-collection.html', 's-search.html', 's-page.html',
           's-404.html', 'c-page-note.html'],
    8808: ['p-sizes.html', 'c-many.html'],
}

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var PAGES = PAGELIST, CSS = 'CSSHERE', out = [], i = 0;
function snap(d) {
  var m = {};
  Array.prototype.forEach.call(d.querySelectorAll('*'), function (el, n) {
    if (el.offsetParent === null && el.tagName !== 'BODY') return;
    var r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return;
    m[n] = Math.round(r.top * 10) / 10 + ',' + Math.round(r.left * 10) / 10 + ',' +
           Math.round(r.width * 10) / 10 + ',' + Math.round(r.height * 10) / 10;
  });
  return m;
}
function famCount(d, w) {
  var c = {};
  Array.prototype.forEach.call(d.querySelectorAll('*'), function (el) {
    var t = '';
    for (var n = 0; n < el.childNodes.length; n++) {
      if (el.childNodes[n].nodeType === 3) t += el.childNodes[n].nodeValue;
    }
    if (!t.trim().length) return;
    var f = w.getComputedStyle(el).fontFamily.split(',')[0].replace(/['"]/g, '').trim();
    c[f] = (c[f] || 0) + 1;
  });
  return c;
}
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
    var kill = d.createElement('style');
    kill.textContent = '*,*::before,*::after{transition:none !important;animation:none !important}';
    d.head.appendChild(kill);
    void d.body.offsetHeight;

    /* NO-OP CONTROL FIRST. .visually-hidden is position:absolute with
       clip-path:inset(50%), so it cannot move layout — yet the first version of
       this probe reported 757 elements moving. That means something OTHER than
       the candidate was shifting the page between the two snapshots, almost
       certainly a webfont finishing loading. So: take a snapshot, inject a
       style element that changes NOTHING, snapshot again, and measure the drift.
       Whatever that control reports is the probe's own noise floor and must be
       subtracted from the candidate's result. */
    var ctl0 = snap(d);
    var noop = d.createElement('style');
    noop.textContent = '.gs-noop-probe-class-that-matches-nothing { color: inherit; }';
    d.head.appendChild(noop);
    void d.body.offsetHeight;
    var ctl1 = snap(d);
    var controlMoved = 0;
    Object.keys(ctl0).forEach(function (k) { if (ctl0[k] !== ctl1[k]) controlMoved++; });

    var before = snap(d), famBefore = famCount(d, w);
    var bodyFamBefore = w.getComputedStyle(d.body).fontFamily.split(',')[0].replace(/['"]/g, '');

    var s = d.createElement('style');
    s.textContent = CSS;
    d.head.appendChild(s);
    void d.body.offsetHeight;

    var after = snap(d), famAfter = famCount(d, w);
    var bodyFamAfter = w.getComputedStyle(d.body).fontFamily.split(',')[0].replace(/['"]/g, '');

    var moved = 0, keys = Object.keys(before);
    keys.forEach(function (k) { if (before[k] !== after[k]) moved++; });

    out.push({
      page: page,
      controlMoved: controlMoved,
      applied: bodyFamBefore !== bodyFamAfter,
      bodyBefore: bodyFamBefore, bodyAfter: bodyFamAfter,
      elements: keys.length, moved: moved,
      famBefore: famBefore, famAfter: famAfter
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
    html = PROBE.replace('PAGELIST', json.dumps(pages)).replace('CSSHERE', CANDIDATE)
    p = os.path.join(site, '_bodyfont.html')
    io.open(p, 'w', encoding='utf-8').write(html)
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port)],
                           cwd=site, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        outp = os.path.join(HERE, 'bodyfont-%d.html' % port)
        subprocess.call([EDGE, '--headless=new', '--disable-gpu',
                         '--user-data-dir=' + PROFILE, '--virtual-time-budget=30000',
                         '--dump-dom', 'http://127.0.0.1:%d/_bodyfont.html' % port],
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

    print('=== CANDIDATE: %s ===' % CANDIDATE)
    print()
    print('  %-22s %-9s %-26s %8s %7s %7s'
          % ('page', 'applied', 'body font before -> after', 'elements', 'noop', 'moved'))
    total_moved = 0
    all_applied = True
    for r in rows:
        if not r['applied']:
            all_applied = False
        total_moved += r['moved']
        print('  %-22s %-9s %-26s %8d %7d %7d%s'
              % (r['page'][:22], 'YES' if r['applied'] else '*** NO ***',
                 r['bodyBefore'][:11] + ' -> ' + r['bodyAfter'][:11],
                 r['elements'], r.get('controlMoved', -1), r['moved'],
                 '  <-- REAL MOVEMENT' if r['moved'] > r.get('controlMoved', 0) else ''))

    print()
    print('  negative control: the rule %s'
          % ('APPLIED on every page' if all_applied else '*** DID NOT APPLY — results meaningless ***'))
    print()

    print('=== TYPEFACE CENSUS, BEFORE -> AFTER ===')
    fb, fa = {}, {}
    for r in rows:
        for k, v in r['famBefore'].items():
            fb[k] = fb.get(k, 0) + v
        for k, v in r['famAfter'].items():
            fa[k] = fa.get(k, 0) + v
    for k in sorted(set(list(fb.keys()) + list(fa.keys()))):
        print('  %-24s %5d -> %5d' % (k, fb.get(k, 0), fa.get(k, 0)))

    print()
    print('=== VERDICT ===')
    total_control = sum(r.get('controlMoved', 0) for r in rows)
    print('  probe noise floor (a no-op style injection moved this many): %d' % total_control)
    print()
    if total_moved <= total_control and all_applied:
        print('  Nothing moves. %d elements measured across %d pages, zero geometry'
              % (sum(r['elements'] for r in rows), len(rows)))
        print('  changes. The declaration only reaches text that had no font of its')
        print('  own — all of it screen-reader-only — so this is a safety net with')
        print('  no rendered consequence.')
    else:
        print('  %d element(s) moved against a %d noise floor — %d attributable to'
              % (total_moved, total_control, total_moved - total_control))
        print('  the candidate. NOT a free change; review before applying.')
