# -*- coding: utf-8 -*-
"""Phase 16 — the filter drawer must not exist above --bp-md.

THE DEFECT, AS REPORTED BY TWO INDEPENDENT AUDITORS.

assets/facets.js reveals the Filter trigger unconditionally. Every drawer rule
in component-facets.css lives inside @media (max-width: 767px), but
`.facets-open body { overflow: hidden }` is at top level. So at >=768px, on a
collection page with filters configured, there is a visible Filter button that
locks the page scroll and opens nothing — and because `.facets__bar` is
display:none at that width, the close button cannot take focus, so the panel's
Tab guard pulls focus into an in-flow panel with Escape as the only way out.

Written as a negative control first: run before the fix, every assertion below
should fail at 1440 and pass at 375.
"""
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(HERE, '..', 'phase9', 'site'))
EDGE = os.environ.get('GS_BROWSER',
                      r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-facets')
PORT = 8809

# The page that renders filters, at a desktop width and a phone width.
VIEWPORTS = [(1440, 900), (1280, 800), (768, 1024), (375, 812)]

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
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
    setTimeout(function () {
      var d = f.contentDocument, win = f.contentWindow;
      var toggle = d.querySelector('[data-facets-toggle]');
      var panel = d.querySelector('[data-facets]');
      var out = { hasToggle: !!toggle, hasPanel: !!panel };
      if (toggle) {
        out.toggleHidden = toggle.hidden;
        out.toggleDisplay = win.getComputedStyle(toggle).display;
        out.toggleVisible = toggle.offsetParent !== null;
      }
      if (toggle && out.toggleVisible) {
        /* Press it, exactly as a customer would. */
        toggle.click();
        out.htmlClass = d.documentElement.className;
        out.bodyOverflow = win.getComputedStyle(d.body).overflow;
        out.scrollLocked = win.getComputedStyle(d.body).overflow === 'hidden';
        var bar = d.querySelector('.facets__bar');
        out.barDisplay = bar ? win.getComputedStyle(bar).display : null;
        out.activeAfterOpen = d.activeElement ? (d.activeElement.className || d.activeElement.tagName) : null;
        out.panelPosition = panel ? win.getComputedStyle(panel).position : null;
        out.panelIsDrawer = panel ? panel.classList.contains('facets--drawer') : null;
      }
      res[w + 'x' + h] = out;
      f.remove(); i++; step();
    }, 400);
  };
}
step();
</script>
"""

FAILURES = []
CHECKS = [0]


def check(label, ok, detail=''):
    CHECKS[0] += 1
    print('  %-62s %s %s' % (label, 'OK  ' if ok else '*** FAIL ***',
                             '' if ok else str(detail)[:110]))
    if not ok:
        FAILURES.append(label)


if __name__ == '__main__':
    shutil.rmtree(PROFILE, ignore_errors=True)
    page = 's-collection-filters.html'
    src = PROBE.replace('WIDTHS', json.dumps(VIEWPORTS)).replace('PAGE', page)
    io.open(os.path.join(SITE, '_facetsgate.html'), 'w', encoding='utf-8').write(src)
    out = os.path.join(HERE, 'facetsgate-dom.html')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run',
                    '--no-default-browser-check', '--user-data-dir=' + PROFILE,
                    '--virtual-time-budget=30000', '--window-size=1600,1100', '--dump-dom',
                    'http://127.0.0.1:%d/_facetsgate.html' % PORT],
                   stdout=io.open(out, 'w', encoding='utf-8'), stderr=subprocess.DEVNULL)
    d = io.open(out, encoding='utf-8', errors='replace').read()
    m = re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>', d, re.S)
    if not m:
        print('NO READING')
        print(d[-800:])
        raise SystemExit(1)
    data = json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')
                      .replace('&lt;', '<').replace('&gt;', '>'))

    print('=== THE FILTER TRIGGER, BY VIEWPORT ===')
    print('%-10s %-8s %-9s %-9s %-11s %-9s %s' %
          ('viewport', 'toggle', 'visible', 'display', 'scrollLock', 'isDrawer', 'barDisplay'))
    for k, r in data.items():
        print('%-10s %-8s %-9s %-9s %-11s %-9s %s' %
              (k, r.get('hasToggle'), r.get('toggleVisible'), r.get('toggleDisplay', '-'),
               r.get('scrollLocked', '-'), r.get('panelIsDrawer', '-'),
               r.get('barDisplay', '-')))

    print()
    print('=== ABOVE --bp-md THERE IS NO DRAWER, SO THERE IS NO TRIGGER ===')
    for k in ('1440x900', '1280x800', '768x1024'):
        r = data.get(k, {})
        check('%-10s the Filter trigger is not offered' % k,
              r.get('toggleVisible') is not True,
              'display=%s hidden=%s' % (r.get('toggleDisplay'), r.get('toggleHidden')))
        check('%-10s and the page scroll is never locked' % k,
              r.get('scrollLocked') is not True,
              'body overflow=%s' % r.get('bodyOverflow'))

    print()
    print('=== BELOW IT, THE DRAWER STILL WORKS ===')
    r = data.get('375x812', {})
    check('375x812    the trigger is offered', r.get('toggleVisible') is True)
    check('375x812    pressing it makes the panel a drawer', r.get('panelIsDrawer') is True)
    check('375x812    and locks the page behind it', r.get('scrollLocked') is True)
    check('375x812    the drawer header is visible, so close can take focus',
          r.get('barDisplay') not in (None, 'none'), r.get('barDisplay'))

    print()
    print('%d checks, %d passed, %d failed'
          % (CHECKS[0], CHECKS[0] - len(FAILURES), len(FAILURES)))
    print('OVERALL: %s' % ('PASS' if not FAILURES else '*** FAILURES ABOVE ***'))
