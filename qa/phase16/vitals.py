# -*- coding: utf-8 -*-
"""Phase 16 — LCP element, layout shift and handler cost, measured in a browser.

HONEST SCOPE, stated up front because the brief forbids inventing metrics.

MEANINGFUL HERE:
  - which element is the LCP candidate, and whether it is lazy-loaded
  - layout shifts caused by images without a reserved box, and by scripts
  - the duration of the theme's own event handlers (an INP input, not INP)
  - long tasks during load

NOT MEANINGFUL HERE, and therefore not reported as a number anywhere:
  - LCP / FCP / TTFB TIMINGS. There is no Shopify server and no network; the
    harness serves from localhost with placeholder images.
  - CLS from FONT SWAP. The harness has no font files, so no swap happens. This
    is the one CLS source that cannot be reproduced locally and it is called out
    separately rather than silently scoring zero.
  - INP as a field metric. Handler duration is a component of it, not it.
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
EDGE = os.environ.get('GS_BROWSER',
                      r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-vitals')
# (label, port, page, interactions to time)
PAGES = [
    ('Homepage', 8809, 'home.html', ['[data-menu-toggle]', '[data-cart-bubble]']),
    ('Collection', 8809, 's-collection.html', ['[data-cart-bubble]']),
    ('Collection+filters', 8809, 's-collection-filters.html', ['[data-facets-toggle]']),
    ('Product', 8808, 'p-sizes.html', ['[data-quantity-step="1"]', '[data-cart-bubble]']),
    ('Cart page', 8808, 'c-page-many.html', ['[data-quantity-step="1"]']),
    ('Search', 8809, 's-search.html', ['[data-search-trigger]']),
]

PROBE = r"""
<script>
(function () {
  window.__vitals = { shifts: [], lcp: null, longTasks: [], handlers: [] };

  try {
    new PerformanceObserver(function (list) {
      for (const e of list.getEntries()) {
        var el = e.element;
        window.__vitals.lcp = {
          size: Math.round(e.size),
          tag: el ? el.tagName.toLowerCase() : null,
          cls: el ? (el.className && el.className.baseVal !== undefined
                      ? el.className.baseVal : String(el.className || '')).slice(0, 60) : null,
          loading: el && el.getAttribute ? el.getAttribute('loading') : null,
          fetchpriority: el && el.getAttribute ? el.getAttribute('fetchpriority') : null,
          src: el && el.currentSrc ? el.currentSrc.split('/').pop().slice(0, 40) : null
        };
      }
    }).observe({ type: 'largest-contentful-paint', buffered: true });
  } catch (e) {}

  try {
    new PerformanceObserver(function (list) {
      for (const e of list.getEntries()) {
        if (e.hadRecentInput) continue;
        var srcs = (e.sources || []).map(function (s) {
          var n = s.node;
          if (!n || !n.tagName) return '?';
          var c = n.className && n.className.baseVal !== undefined
            ? n.className.baseVal : String(n.className || '');
          return n.tagName.toLowerCase() + (c ? '.' + c.split(' ')[0] : '');
        });
        window.__vitals.shifts.push({ value: e.value, sources: srcs.slice(0, 3) });
      }
    }).observe({ type: 'layout-shift', buffered: true });
  } catch (e) {}

  try {
    new PerformanceObserver(function (list) {
      for (const e of list.getEntries()) {
        window.__vitals.longTasks.push(Math.round(e.duration));
      }
    }).observe({ type: 'longtask', buffered: true });
  } catch (e) {}
})();
</script>
"""

RUNNER = r"""
<script>
(function () {
  function wait(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }

  /* Handler cost: the synchronous time the theme's own listeners take. This is
     an INPUT to INP, not INP — it excludes input delay and presentation. */
  function timeClick(sel) {
    var el = document.querySelector(sel);
    if (!el) return { sel: sel, ms: null, note: 'not on this page' };
    var t0 = performance.now();
    el.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
    var ms = performance.now() - t0;
    return { sel: sel, ms: Math.round(ms * 100) / 100 };
  }

  function run() {
    return wait(600).then(function () {
      /* CLS IS SNAPSHOTTED BEFORE ANY INTERACTION.

         The first version summed every shift and reported the total as CLS. It
         was wrong: the synthetic clicks below open a drawer and reveal a
         confirmation line, and a shift caused by a real user's click carries
         hadRecentInput and is excluded from CLS by definition — but a shift
         caused by dispatchEvent does NOT set that flag, so those shifts were
         being counted as load instability. The product page's 0.0036 was
         mostly the cart drawer opening.

         Load CLS is what is above this line. Interaction shifts are reported
         separately, because they are worth knowing about and are not CLS. */
      var v = window.__vitals;
      v.loadShifts = v.shifts.slice();
      v.cls = v.loadShifts.reduce(function (a, s) { return a + s.value; }, 0);

      var targets = TARGETS;
      for (var i = 0; i < targets.length; i++) {
        window.__vitals.handlers.push(timeClick(targets[i]));
      }
      return wait(400);
    }).then(function () {
      var v = window.__vitals;
      var after = v.shifts.slice(v.loadShifts.length);
      v.interactionCls = after.reduce(function (a, s) { return a + s.value; }, 0);
      v.interactionSources = after.map(function (s) { return s.sources.join('+'); });
      document.title = 'DONE';
      document.getElementById('o').textContent = '<<<' + JSON.stringify(v) + '>>>';
    });
  }
  if (document.readyState === 'complete') run();
  else window.addEventListener('load', function () { setTimeout(run, 50); });
})();
</script>
<pre id="o" style="display:none"></pre>
"""


def run(port, page, targets, site_dir):
    src = io.open(os.path.join(site_dir, page), encoding='utf-8').read()
    # The observers must be installed before anything else runs.
    src = src.replace('<meta charset="utf-8">', '<meta charset="utf-8">' + PROBE, 1)
    src = src.replace('</body>', RUNNER.replace('TARGETS', json.dumps(targets)) + '</body>', 1)
    out_name = '_vitals-%s' % page
    io.open(os.path.join(site_dir, out_name), 'w', encoding='utf-8').write(src)

    dom = os.path.join(HERE, 'vitals-dom.html')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run',
                    '--no-default-browser-check', '--user-data-dir=' + PROFILE,
                    '--virtual-time-budget=25000', '--window-size=1440,900', '--dump-dom',
                    '--incognito', '--disable-http-cache', '--disk-cache-size=1',
                    'http://127.0.0.1:%d/%s' % (port, out_name)],
                   stdout=io.open(dom, 'w', encoding='utf-8'), stderr=subprocess.DEVNULL)
    d = io.open(dom, encoding='utf-8', errors='replace').read()
    m = re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>', d, re.S)
    if not m:
        return None
    return json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')
                      .replace('&lt;', '<').replace('&gt;', '>'))


if __name__ == '__main__':
    shutil.rmtree(PROFILE, ignore_errors=True)
    SITES = {8809: os.path.abspath(os.path.join(HERE, '..', 'phase9', 'site')),
             8808: os.path.abspath(os.path.join(HERE, '..', 'phase8', 'site'))}

    print('=== LCP CANDIDATE ELEMENT (identity is meaningful; timing is not) ===')
    print('%-20s %-8s %-30s %-9s %-8s %s' %
          ('surface', 'tag', 'class', 'loading', 'fetchpri', 'size'))
    data = {}
    for label, port, page, targets in PAGES:
        r = run(port, page, targets, SITES[port])
        data[label] = r
        if not r:
            print('%-20s  NO READING' % label)
            continue
        l = r.get('lcp')
        if not l:
            print('%-20s  (no LCP entry)' % label)
            continue
        print('%-20s %-8s %-30s %-9s %-8s %s' %
              (label, l['tag'], (l['cls'] or '')[:30], l['loading'] or '-',
               l['fetchpriority'] or '-', l['size']))

    print()
    print('=== LOAD CLS — shifts before any interaction ===')
    print('%-20s %10s  %s' % ('surface', 'CLS', 'sources'))
    for label, _p, _pg, _t in PAGES:
        r = data.get(label)
        if not r:
            continue
        srcs = []
        for s in r.get('loadShifts', []):
            srcs.extend(s['sources'])
        print('%-20s %10.4f  %s' % (label, r['cls'],
                                    ', '.join(dict.fromkeys(srcs)) or 'none'))
    print('  Google\'s "good" threshold is 0.1. Font-swap shift is NOT included —')
    print('  the harness has no font files, so no swap occurs. That is the one CLS')
    print('  source this environment cannot reproduce.')

    print()
    print('=== SHIFT CAUSED BY INTERACTION — not CLS, but worth knowing ===')
    for label, _p, _pg, _t in PAGES:
        r = data.get(label)
        if not r:
            continue
        print('%-20s %10.4f  %s' % (label, r.get('interactionCls', 0.0),
                                    ', '.join(dict.fromkeys(
                                        s for s in r.get('interactionSources', []) if s)) or 'none'))
    print('  A real user\'s click sets hadRecentInput and these are excluded from')
    print('  CLS. A synthetic dispatchEvent does not, which is why they are split out.')

    print()
    print('=== THEME EVENT-HANDLER COST (an input to INP, not INP) ===')
    print('%-20s %-28s %8s' % ('surface', 'control', 'ms'))
    worst = 0.0
    for label, _p, _pg, _t in PAGES:
        r = data.get(label)
        if not r:
            continue
        for h in r['handlers']:
            if h.get('ms') is None:
                print('%-20s %-28s %8s' % (label, h['sel'][:28], h.get('note', '-')))
            else:
                worst = max(worst, h['ms'])
                print('%-20s %-28s %8.2f' % (label, h['sel'][:28], h['ms']))

    print()
    print('=== LONG TASKS DURING LOAD ===')
    for label, _p, _pg, _t in PAGES:
        r = data.get(label)
        if r:
            lt = r['longTasks']
            print('  %-20s %s' % (label, ('%d tasks, longest %dms' % (len(lt), max(lt)))
                                  if lt else 'none'))

    print()
    print('  worst theme handler: %.2f ms. Google\'s INP "good" threshold is 200ms' % worst)
    print('  for the whole interaction, of which handler time is one component.')
