# -*- coding: utf-8 -*-
"""Phase 15 — the account control's geometry, measured in a real browser.

THE HARNESS CAN ONLY EVER SEE THE UNDEFINED STATE, AND THAT IS THE POINT.

<shopify-account> is upgraded by a script Shopify serves through
content_for_header. The harness never loads it, so the element is permanently
un-upgraded here. That makes this harness useless for testing the component and
PERFECT for testing the one failure the component can cause in a theme: a custom
element has no dimensions until its script runs, so without an explicit
reservation the header's end cluster is short by one control on every first
paint and everything in it jumps sideways when the script lands.

So these measurements are of the reservation, never of the component, and the
suite says so rather than implying it tested Shopify's UI.
"""
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, '..', 'phase8', 'site'))
EDGE = os.environ.get('GS_BROWSER',
                      r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
PORT = 8808
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-geom')
# Every viewport the brief names, plus the two the header is tightest at.
VIEWPORTS = [(375, 812), (390, 844), (430, 932), (768, 1024),
             (1280, 800), (1440, 900), (1920, 1080)]

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title>
<body style="margin:0"><pre id="o" style="display:none"></pre>
<script>
var W = WIDTHS, res = {}, i = 0;
function step() {
  if (i >= W.length) {
    document.title = 'DONE';
    document.getElementById('o').textContent = '<<<' + JSON.stringify(res) + '>>>';
    return;
  }
  var w = W[i][0], h = W[i][1];
  var f = document.createElement('iframe');
  f.style.cssText = 'border:0;display:block;width:' + w + 'px;height:' + h + 'px';
  f.src = 'PAGE';
  document.body.appendChild(f);
  f.onload = function () {
    var d = f.contentDocument, win = f.contentWindow;
    var el = d.querySelector('shopify-account');
    var cluster = d.querySelector('.header__cluster--end');
    var controls = cluster ? cluster.children.length : 0;
    var cs = el ? win.getComputedStyle(el) : null;
    var r = el ? el.getBoundingClientRect() : null;
    var avatar = d.querySelector('.header__account-avatar');
    var ar = avatar ? avatar.getBoundingClientRect() : null;
    res[w + 'x' + h] = {
      defined: el ? (win.customElements && !!win.customElements.get('shopify-account')) : null,
      w: r ? Math.round(r.width) : null,
      h: r ? Math.round(r.height) : null,
      display: cs ? cs.display : null,
      cluster: cluster ? Math.round(cluster.getBoundingClientRect().width) : null,
      controls: controls,
      avatarW: ar ? Math.round(ar.width) : null,
      // Every sibling control's box, so "the same size as the others" is measured.
      siblings: Array.prototype.map.call(cluster ? cluster.children : [], function (c) {
        var b = c.getBoundingClientRect();
        return c.tagName.toLowerCase() + ':' + Math.round(b.width) + 'x' + Math.round(b.height);
      }),
      docScrollW: Math.round(d.documentElement.scrollWidth),
      viewportW: w,
      // Is it reachable by keyboard before the upgrade?
      focusable: el ? (el.tabIndex >= 0) : null
    };
    f.remove();
    i++;
    step();
  };
}
step();
</script>
"""


def run(page):
    src = PROBE.replace('WIDTHS', json.dumps(VIEWPORTS)).replace('PAGE', page)
    io.open(os.path.join(SITE, '_geom.html'), 'w', encoding='utf-8').write(src)
    out = os.path.join(HERE, 'geom-dom.html')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run',
                    '--no-default-browser-check', '--user-data-dir=' + PROFILE,
                    '--virtual-time-budget=30000', '--window-size=2100,1200', '--dump-dom',
                    'http://127.0.0.1:%d/_geom.html' % PORT],
                   stdout=io.open(out, 'w', encoding='utf-8'), stderr=subprocess.DEVNULL)
    d = io.open(out, encoding='utf-8', errors='replace').read()
    m = re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>', d, re.S)
    if not m:
        print('NO READING')
        print(d[-900:])
        return {}
    return json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')
                      .replace('&lt;', '<').replace('&gt;', '>'))


if __name__ == '__main__':
    shutil.rmtree(PROFILE, ignore_errors=True)
    data = run('c-one.html')
    fails = []

    print('=== THE UNDEFINED ELEMENT RESERVES ITS BOX ===')
    print('%-10s %-9s %-8s %-8s %-9s %s' %
          ('viewport', 'box', 'display', 'cluster', 'docScrW', 'end-cluster controls'))
    for k in data:
        r = data[k]
        box = '%sx%s' % (r['w'], r['h'])
        print('%-10s %-9s %-8s %-8s %-9s %s' %
              (k, box, r['display'], r['cluster'], r['docScrollW'], ', '.join(r['siblings'])))
        if r['defined'] is not False and r['defined'] is not None:
            fails.append('%s: the element reports as DEFINED — the harness has loaded a real component '
                         'and every reading here is about something else' % k)
        if r['w'] != 44 or r['h'] != 44:
            fails.append('%s: reserved box is %s, not 44x44' % (k, box))
        if r['docScrollW'] > r['viewportW']:
            fails.append('%s: the page scrolls sideways (%d > %d)'
                         % (k, r['docScrollW'], r['viewportW']))
        if r['controls'] != 3:
            fails.append('%s: end cluster has %d controls, expected 3' % (k, r['controls']))
        # Every control in the cluster is the same 44px box, so nothing moves
        # when one of them is replaced.
        sizes = set(s.split(':')[1] for s in r['siblings'])
        if sizes != {'44x44'}:
            fails.append('%s: the cluster is not a uniform row of 44px controls: %s' % (k, sizes))

    print()
    print('=== WHAT THIS CANNOT TELL YOU ===')
    any_row = next(iter(data.values())) if data else {}
    print('  the element is defined here: %s  (expected False — no Shopify script in the harness)'
          % any_row.get('defined'))
    print('  keyboard-focusable while undefined: %s' % any_row.get('focusable'))
    print('  -> a custom element is not focusable until its script upgrades it. Before')
    print('     that the control cannot be tabbed to or clicked. This is inherent to the')
    print('     component and is the one thing the old <a href> did better. Recorded as a')
    print('     known limitation rather than worked around, because a fallback link inside')
    print('     the slot would nest an anchor inside the upgraded button.')

    print()
    if fails:
        for f in fails:
            print('  *** %s' % f)
    print('%d viewports measured, %d problems' % (len(data), len(fails)))
    print('OVERALL: %s' % ('PASS' if not fails else '*** FAILURES ABOVE ***'))
