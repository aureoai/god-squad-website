# -*- coding: utf-8 -*-
"""Phase 18 — the filter drawer's exit slide, and the class that holds it open.

Phase 18 gave the drawer an exit animation it never had: `visibility: hidden`
was not a transitioned property, so removing .is-open hid the panel in the frame
the transform started and the slide out was never rendered. PHASE-2 §21 line
1725 specifies "menu panel / drawer entry AND exit".

The fix adds .is-closing, held by assets/facets.js until transitionend and
removed by a 500ms fallback if that never arrives. A class that is added and
never removed would leave the drawer sitting over the page, so the fallback and
the reopen-mid-slide path matter more than the animation does — those are what
this tests, not the prettiness of the slide.

Negative control, run rather than assumed: removing ONLY the .is-closing CSS
rule fails exactly one assertion -- "panel still visible during the slide". The
class assertions keep passing, correctly, because facets.js still sets the
class; it is the CSS rule that makes the class mean anything. One failing
assertion is the right answer here, and knowing WHICH one is the point of
running the control instead of claiming a range.
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
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-exit')
PORT = 8809
PAGE = 's-collection-filters.html'

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var out = [], f = document.createElement('iframe');
/* Phone width: every drawer rule lives inside @media (max-width: 767px). */
f.style.cssText = 'border:0;width:375px;height:812px';
f.src = 'PAGEHERE';
document.body.appendChild(f);
function rec(name, got, want) {
  out.push({name: name, got: String(got), want: String(want), pass: String(got) === String(want)});
}
f.onload = function () {
  var d = f.contentDocument, w = f.contentWindow;
  var panel = d.querySelector('.facets');
  var toggle = d.querySelector('[data-facets-toggle]');
  if (!panel || !toggle) {
    out.push({name: 'drawer present on the page', got: 'missing', want: 'present', pass: false});
    document.title = 'DONE';
    document.getElementById('o').textContent = '<<<' + JSON.stringify(out) + '>>>';
    return;
  }
  function cls() { return panel.className; }
  function vis() { return w.getComputedStyle(panel).visibility; }

  /* 1. Opening puts it on screen. */
  toggle.click();
  rec('open adds .is-open', /\bis-open\b/.test(cls()), 'true');
  rec('open leaves no .is-closing', /\bis-closing\b/.test(cls()), 'false');
  rec('open is visible', vis(), 'visible');

  /* 2. Closing holds it visible for the slide. */
  toggle.click();
  rec('close drops .is-open', /\bis-open\b/.test(cls()), 'false');
  rec('close adds .is-closing', /\bis-closing\b/.test(cls()), 'true');
  rec('panel still visible during the slide', vis(), 'visible');

  /* 3. Reopening mid-slide must not leave the stale class behind. */
  toggle.click();
  rec('reopen mid-slide clears .is-closing', /\bis-closing\b/.test(cls()), 'false');
  rec('reopen mid-slide is open', /\bis-open\b/.test(cls()), 'true');
  toggle.click();   /* close again, leaving .is-closing set for the wait below */

  /* 4. The class must come off by itself. transitionend should do it at 250ms;
        the 500ms fallback is the guarantee. Wait past both. */
  w.setTimeout(function () {
    rec('.is-closing is released after the slide', /\bis-closing\b/.test(cls()), 'false');
    rec('panel is hidden once settled', vis(), 'hidden');
    rec('no .is-open left', /\bis-open\b/.test(cls()), 'false');
    rec('page scroll lock released',
        d.documentElement.classList.contains('facets-open'), 'false');
    document.title = 'DONE';
    document.getElementById('o').textContent = '<<<' + JSON.stringify(out) + '>>>';
  }, 900);
};
</script>
"""

if __name__ == '__main__':
    html = PROBE.replace('PAGEHERE', PAGE)
    p = os.path.join(SITE, '_exit.html')
    io.open(p, 'w', encoding='utf-8').write(html)
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)],
                           cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        outp = os.path.join(HERE, 'exit.html')
        subprocess.call([EDGE, '--headless=new', '--disable-gpu',
                         '--user-data-dir=' + PROFILE, '--virtual-time-budget=25000',
                         '--dump-dom', 'http://127.0.0.1:%d/_exit.html' % PORT],
                        stdout=io.open(outp, 'wb'), stderr=subprocess.DEVNULL)
        dom = io.open(outp, encoding='utf-8', errors='replace').read()
        m = re.search(r'&lt;&lt;&lt;(.*?)&gt;&gt;&gt;', dom, re.S) or \
            re.search(r'<<<(.*?)>>>', dom, re.S)
        if not m:
            raise SystemExit('*** no payload — the probe did not finish ***')
        rows = json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&'))
    finally:
        srv.terminate()
        try:
            os.remove(p)
        except OSError:
            pass

    bad = 0
    for r in rows:
        if not r['pass']:
            bad += 1
        print('  %-4s %-46s got %-10s want %s'
              % ('PASS' if r['pass'] else 'FAIL', r['name'], r['got'], r['want']))
    print()
    print('%d assertions, %d failed' % (len(rows), bad))
    print('OVERALL: %s' % ('PASS' if not bad else '*** REVIEW ABOVE ***'))
