# -*- coding: utf-8 -*-
"""Phase 18 — do all three disclosures point the same way now?

The audit found this seven times across four dimensions, which is why it was
worth verifying rather than accepting: the verifiers also called the SIZE
difference a defect, and PHASE-2 line 1428 assigns the chevron both sizes on
purpose ("--icon-sm 16px inline; --icon-md in controls"), so size was rejected
and only direction fixed.

Computed `transform` comes back as a matrix, not as the degrees anyone wrote, so
this converts it back to an angle with atan2 and reports where the glyph
actually points. icon-chevron.svg is drawn pointing RIGHT, so 0deg is right,
90deg is down, 180deg is left and 270deg (-90) is up.

The correct pattern for a disclosure is down when closed, up when open. Anything
pointing left or right in either state is the defect this is checking for.
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
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-chev')
# (port, page, the <details>, the summary inside it, label)
TARGETS = [
    (8809, 's-collection-filters.html', '.facets__group', '.facets__summary', 'filter group'),
    (8809, 'c-page-note.html', '.cart-note', '.cart-note__summary', 'cart note'),
    (8809, 'p-details.html', '.main-product__details', '.main-product__details-summary',
     'product details'),
]

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var T = TARGETS, out = [], i = 0;
function angle(el, w) {
  var m = w.getComputedStyle(el).transform;
  if (!m || m === 'none') return 0;
  var n = m.match(/matrix\(([^)]+)\)/);
  if (!n) return null;
  var p = n[1].split(',').map(parseFloat);
  var deg = Math.round(Math.atan2(p[1], p[0]) * 180 / Math.PI);
  return ((deg % 360) + 360) % 360;
}
function pointsTo(a) {
  if (a === null) return '?';
  if (a > 315 || a <= 45) return 'RIGHT';
  if (a <= 135) return 'DOWN';
  if (a <= 225) return 'LEFT';
  return 'UP';
}
function step() {
  if (i >= T.length) {
    document.title = 'DONE';
    document.getElementById('o').textContent = '<<<' + JSON.stringify(out) + '>>>';
    return;
  }
  var t = T[i];
  var f = document.createElement('iframe');
  f.style.cssText = 'border:0;width:1440px;height:1200px';
  f.src = t.page;
  document.body.appendChild(f);
  f.onload = function () {
    var d = f.contentDocument, w = f.contentWindow;
    /* The transform is TRANSITIONED. Reading it straight after flipping [open]
       returns the start value, which is how this probe first reported the
       filter chevron as unchanged. Phase 4 recorded the same lesson: disable
       transitions before measuring anything animated. */
    var kill = d.createElement('style');
    kill.textContent = '*, *::before, *::after { transition: none !important; animation: none !important; }';
    d.head.appendChild(kill);
    var det = d.querySelector(t.det);
    var rec = {label: t.label, page: t.page};
    if (!det) { rec.error = 'no ' + t.det + ' on this page'; out.push(rec); f.remove(); i++; step(); return; }
    var sum = det.querySelector(t.sum);
    var icon = sum ? sum.querySelector('.icon, svg') : null;
    if (!icon) { rec.error = 'no icon inside ' + t.sum; out.push(rec); f.remove(); i++; step(); return; }
    det.open = false; void d.body.offsetHeight;
    rec.closedDeg = angle(icon, w); rec.closed = pointsTo(rec.closedDeg);
    rec.size = Math.round(icon.getBoundingClientRect().width);
    det.open = true; void d.body.offsetHeight;
    rec.openDeg = angle(icon, w); rec.open = pointsTo(rec.openDeg);
    rec.sweep = (rec.openDeg === null || rec.closedDeg === null) ? null
      : (rec.openDeg - rec.closedDeg + 360) % 360;
    out.push(rec);
    f.remove(); i++; step();
  };
  f.onerror = function () { out.push({label: t.label, error: 'load failed'}); f.remove(); i++; step(); };
}
step();
</script>
"""


def run(port, site, targets):
    html = PROBE.replace('TARGETS', json.dumps(targets))
    p = os.path.join(site, '_chev.html')
    io.open(p, 'w', encoding='utf-8').write(html)
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port)],
                           cwd=site, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        outp = os.path.join(HERE, 'chev-%d.html' % port)
        subprocess.call([EDGE, '--headless=new', '--disable-gpu',
                         '--user-data-dir=' + PROFILE, '--virtual-time-budget=20000',
                         '--dump-dom', 'http://127.0.0.1:%d/_chev.html' % port],
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
    rows = []
    for port, site in ((8809, S9), (8808, S8)):
        ts = [{'page': p, 'det': det, 'sum': s, 'label': l}
              for (pt, p, det, s, l) in TARGETS if pt == port]
        if ts:
            rows += run(port, site, ts)

    print('=== WHERE EACH DISCLOSURE CHEVRON POINTS ===')
    print('  %-18s %-16s %-16s %-7s %s'
          % ('disclosure', 'closed', 'open', 'sweep', 'size'))
    bad = []
    for r in rows:
        if r.get('error'):
            print('  %-18s %s' % (r['label'], r['error']))
            bad.append(r['label'])
            continue
        ok = r['closed'] == 'DOWN' and r['open'] == 'UP'
        if not ok:
            bad.append(r['label'])
        print('  %-18s %-16s %-16s %-7s %dpx  %s'
              % (r['label'],
                 '%s (%d°)' % (r['closed'], r['closedDeg']),
                 '%s (%d°)' % (r['open'], r['openDeg']),
                 '%s°' % r['sweep'], r['size'], '' if ok else '*** WRONG ***'))

    print()
    states = {(r.get('closed'), r.get('open')) for r in rows if not r.get('error')}
    print('distinct closed/open conventions in the theme: %d' % len(states))
    if len(states) == 1 and not bad:
        print('OVERALL: PASS — all three disclosures read down-when-closed,')
        print('up-when-open, each a 180° sweep, which is what PHASE-2 §18 permits.')
    else:
        print('OVERALL: *** %d disclosure(s) still wrong: %s ***' % (len(bad), ', '.join(bad)))
