# -*- coding: utf-8 -*-
"""Phase 18 — design coherence, measured rather than judged.

"Does this look like one design team built it?" is a question about whether the
same KIND of element resolves to the same computed values wherever it appears.
That is measurable, and measuring it is more reliable than reading CSS: a value
can arrive from a token, a cascade, a media query or an inherited property, and
only the browser knows which won.

So this walks every built surface, collects the COMPUTED style of every element
matching each design role, and reports how many distinct signatures each role
resolves to. One signature per role is coherence. Two is drift, and the report
names both.

It measures the reservation, never the photography: this project has no merchant
images (Phase 3 recorded sourcing as the ceiling), so nothing here judges crops,
composition or art direction. Those are not checkable in this environment and
saying otherwise would be inventing a visual review.
"""
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
S9 = os.path.abspath(os.path.join(HERE, '..', 'phase9', 'site'))
S8 = os.path.abspath(os.path.join(HERE, '..', 'phase8', 'site'))
EDGE = os.environ.get('GS_BROWSER',
                      r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-coherence')
PAGES = {
    8809: ['home.html', 's-collection.html', 's-collection-filters.html',
           's-search.html', 's-page.html', 's-404.html', 'c-page-note.html'],
    8808: ['p-sizes.html', 'p-multi.html', 'c-one.html', 'c-many.html',
           'c-page-many.html', 'c-empty.html'],
}

# A design ROLE, and every selector that should render it identically.
ROLES = {
    'section heading (h2)': 'h2',
    'sub heading (h3)': 'h3',
    'body copy': '.our-story__body, .main-page__content > p, .cart-empty__body, '
                 '.main-404__body, .main-collection__empty-body, .hero__description',
    'eyebrow': '.hero__eyebrow, .our-story__eyebrow, .featured-collection__eyebrow',
    'label / caps': '.facets__summary-label, .cart-note__summary-label, '
                    '.main-collection__sort-label, .quantity + label',
    'caption': '.facets__count, .cart-totals__note, .product-card__vendor',
    'price': '.price__current, .product-card__price, .cart-line__price-final',
    'nav link': '.header__nav-link',
    'footer link': '.footer__link',
    'product title': '.product-card__title, .cart-line__title',
    'button primary': '.button--primary',
    'button secondary': '.button--secondary',
    'button accent': '.button--accent',
    'quiet text control': '.cart-drawer__continue, .main-cart__continue, '
                          '.facets__clear, .facets-active__clear',
    'icon': '.icon',
}

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var PAGES = PAGELIST, ROLES = ROLEMAP, out = {}, i = 0;
function sig(cs, el) {
  return [cs.fontFamily.split(',')[0].replace(/['"]/g,''), cs.fontSize, cs.fontWeight,
          cs.lineHeight, cs.letterSpacing, cs.textTransform].join(' | ');
}
function box(cs) {
  return ['r=' + cs.borderRadius, 'pad=' + cs.padding, 'minh=' + cs.minHeight,
          'border=' + cs.borderTopWidth + ' ' + cs.borderTopStyle].join(' ');
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
    var d = null;
    try { d = f.contentDocument; } catch (e) { d = null; }
    if (!d) { f.remove(); i++; step(); return; }
    var win = f.contentWindow, page = PAGES[i].split('/').pop();
    Object.keys(ROLES).forEach(function (role) {
      var els;
      try { els = d.querySelectorAll(ROLES[role]); } catch (e) { return; }
      Array.prototype.forEach.call(els, function (el) {
        var r = el.getBoundingClientRect();
        if (r.width === 0 && r.height === 0) return;   // in a hidden panel, not drift
        if (el.offsetParent === null && el.tagName !== 'svg') return;
        var cs = win.getComputedStyle(el);
        var key = role === 'icon'
          ? 'size=' + Math.round(el.getBoundingClientRect().width) + 'x' +
            Math.round(el.getBoundingClientRect().height) +
            ' stroke=' + (el.getAttribute('stroke-width') || '-')
          : (role.indexOf('button') === 0 || role === 'quiet text control')
            ? sig(cs, el) + ' || ' + box(cs)
            : sig(cs, el);
        out[role] = out[role] || {};
        out[role][key] = out[role][key] || [];
        if (out[role][key].indexOf(page) === -1) out[role][key].push(page);
      });
    });
    /* Values used anywhere, for the token-drift tables. */
    var all = d.querySelectorAll('*');
    ['radius','shadow','transition'].forEach(function (k) { out['_' + k] = out['_' + k] || {}; });
    Array.prototype.forEach.call(all, function (el) {
      if (el.offsetParent === null) return;
      var cs = win.getComputedStyle(el);
      if (cs.borderRadius && cs.borderRadius !== '0px') {
        out._radius[cs.borderRadius] = (out._radius[cs.borderRadius] || 0) + 1;
      }
      if (cs.boxShadow && cs.boxShadow !== 'none') {
        out._shadow[cs.boxShadow] = (out._shadow[cs.boxShadow] || 0) + 1;
      }
      if (cs.transitionDuration && cs.transitionDuration !== '0s') {
        var durs = cs.transitionDuration.split(',').map(function (x) { return x.trim(); });
        var ease = cs.transitionTimingFunction.split('),').map(function (x) { return x.trim(); });
        var t = Array.from(new Set(durs)).sort().join('+') + '  ' + ease[0] + (ease[0].slice(-1) === ')' ? '' : ')');
        out._transition[t] = (out._transition[t] || 0) + 1;
      }
    });
    f.remove(); i++; step();
  };
  f.onerror = function () { f.remove(); i++; step(); };
}
step();
</script>
"""


def run(port, pages):
    site = S9 if port == 8809 else S8
    src = (PROBE.replace('PAGELIST', json.dumps(pages))
                .replace('ROLEMAP', json.dumps(ROLES)))
    io.open(os.path.join(site, '_coherence.html'), 'w', encoding='utf-8').write(src)
    out = os.path.join(HERE, 'coherence-dom-%d.html' % port)
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run',
                    '--no-default-browser-check', '--user-data-dir=' + PROFILE,
                    '--virtual-time-budget=60000', '--window-size=1500,1000', '--dump-dom',
                    'http://127.0.0.1:%d/_coherence.html' % port],
                   stdout=io.open(out, 'w', encoding='utf-8'), stderr=subprocess.DEVNULL)
    d = io.open(out, encoding='utf-8', errors='replace').read()
    m = re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>', d, re.S)
    if not m:
        print('NO READING from port %d' % port)
        print(d[-700:])
        return {}
    return json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')
                      .replace('&lt;', '<').replace('&gt;', '>'))


if __name__ == '__main__':
    shutil.rmtree(PROFILE, ignore_errors=True)
    merged = defaultdict(lambda: defaultdict(list))
    for port, pages in PAGES.items():
        data = run(port, pages)
        for role, sigs in data.items():
            for sig, pgs in sigs.items():
                if role.startswith('_'):
                    merged[role][sig] = (merged[role].get(sig) or 0) + (pgs if isinstance(pgs, int) else 0)
                else:
                    merged[role][sig] = sorted(set(merged[role][sig]) | set(pgs))

    print('=== ONE ROLE, HOW MANY COMPUTED SIGNATURES? ===')
    print('   family | size | weight | line-height | tracking | transform')
    print()
    drift = []
    for role in ROLES:
        sigs = merged.get(role) or {}
        n = len(sigs)
        flag = '' if n <= 1 else '   <-- %d SIGNATURES' % n
        print('  %-22s %d%s' % (role, n, flag))
        if n > 1:
            drift.append(role)
            for sig, pgs in sorted(sigs.items()):
                print('      %-62s %s' % (sig[:62], ', '.join(p.replace('.html', '') for p in pgs)[:60]))

    print()
    print('=== TOKEN DRIFT: DISTINCT VALUES IN USE ===')
    for key, label, want in (('_radius', 'border radius', 3),
                             ('_shadow', 'box shadow', 3),
                             ('_transition', 'transition', 6)):
        vals = merged.get(key) or {}
        print()
        print('  %s — %d distinct value(s)' % (label, len(vals)))
        for v, n in sorted(vals.items(), key=lambda kv: -kv[1])[:8]:
            print('      %-70s x%d' % (str(v)[:70], n))

    print()
    print('=== SUMMARY ===')
    print('  roles measured:            %d' % len(ROLES))
    print('  roles with ONE signature:  %d' % (len(ROLES) - len(drift)))
    print('  roles with drift:          %d  %s'
          % (len(drift), ', '.join(drift) if drift else ''))
    print()
    print('  Drift is not automatically a defect — a price in a cart line and a')
    print('  price on a product page may legitimately differ in size. What this')
    print('  table gives is the list to make that decision about, deliberately,')
    print('  instead of discovering it in review.')
