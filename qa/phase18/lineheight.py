# -*- coding: utf-8 -*-
"""Phase 18 — what does `line-height: normal` actually resolve to?

The coherence table reports three roles whose only difference is line-height:
17.4px on one surface and the keyword `normal` on another, with family, size,
weight, tracking and transform identical. `normal` is a computed KEYWORD, not a
number, so the table cannot say whether that is a visible difference or the same
spacing spelled two ways. This measures the USED value.

Method: for each target element, clone its exact resolved font properties onto a
scratch element in the same document, give it two lines of text at a width that
forces a wrap, and measure the height. Half that height is the used line-height
in pixels. The page under test is never modified — the scratch element is
appended, measured and removed.

Reading the CSS would not answer this. `normal` is resolved from the font's own
metrics (ascent + descent + line gap from the Jost files this theme ships), so
only a browser with the real font loaded knows the number.
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
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-lh')
# (port, page, selector, human label)
TARGETS = [
    (8809, 'home.html', '.product-card__title', 'card title (home)'),
    (8809, 's-collection.html', '.product-card__title', 'card title (collection)'),
    (8808, 'c-page-many.html', '.cart-line__title', 'cart line title (cart page)'),
    (8809, 'c-page-note.html', '.cart-line__title', 'cart line title (with note)'),
    (8809, 'home.html', '.header__nav-link', 'nav link'),
    (8809, 'home.html', '.footer__heading', 'footer heading'),
    (8809, 'home.html', '.our-story__value-title', 'value title'),
]

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var T = TARGETS, out = [], i = 0;
function step() {
  if (i >= T.length) {
    document.title = 'DONE';
    document.getElementById('o').textContent = '<<<' + JSON.stringify(out) + '>>>';
    return;
  }
  var t = T[i];
  var f = document.createElement('iframe');
  f.style.cssText = 'border:0;width:1440px;height:900px';
  f.src = t.page;
  document.body.appendChild(f);
  f.onload = function () {
    var d = null;
    try { d = f.contentDocument; } catch (e) { d = null; }
    var rec = {label: t.label, sel: t.sel, page: t.page};
    if (!d) { rec.error = 'cross-origin'; out.push(rec); f.remove(); i++; step(); return; }
    var el = d.querySelector(t.sel);
    if (!el) { rec.error = 'not present on this page'; out.push(rec); f.remove(); i++; step(); return; }
    var cs = f.contentWindow.getComputedStyle(el);
    rec.computed = cs.lineHeight;
    rec.size = cs.fontSize;
    rec.family = cs.fontFamily.split(',')[0].replace(/['"]/g, '');
    /* Clone the resolved font properties onto a scratch element in the SAME
       document, so the same @font-face files and the same fallback chain apply.
       Two lines forced by a hard break; height / 2 is the used line-height. */
    var s = d.createElement('div');
    s.style.cssText = 'position:absolute;left:-9999px;top:0;width:auto;white-space:pre;' +
      'font-family:' + cs.fontFamily + ';font-size:' + cs.fontSize +
      ';font-weight:' + cs.fontWeight + ';letter-spacing:' + cs.letterSpacing +
      ';text-transform:' + cs.textTransform + ';line-height:' + cs.lineHeight + ';' +
      'padding:0;margin:0;border:0';
    s.textContent = 'HXQ\nHXQ';
    d.body.appendChild(s);
    rec.used = s.getBoundingClientRect().height / 2;
    s.remove();
    /* Does the real element actually wrap in its real container? An element
       that never reaches two lines cannot show a line-height difference. */
    var r = el.getBoundingClientRect();
    rec.realHeight = Math.round(r.height * 10) / 10;
    rec.realWidth = Math.round(r.width);
    rec.scrollH = el.scrollHeight;
    rec.text = (el.textContent || '').trim().slice(0, 42);
    rec.lines = Math.max(1, Math.round(el.scrollHeight / rec.used));
    out.push(rec);
    f.remove(); i++; step();
  };
  f.onerror = function () { out.push({label: t.label, error: 'load failed'}); f.remove(); i++; step(); };
}
step();
</script>
"""


def run(port, targets, site):
    html = PROBE.replace('TARGETS', json.dumps(targets))
    p = os.path.join(site, '_lh.html')
    io.open(p, 'w', encoding='utf-8').write(html)
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port)],
                           cwd=site, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        out = os.path.join(HERE, 'lh-%d.html' % port)
        if os.path.exists(out):
            os.remove(out)
        subprocess.call([EDGE, '--headless=new', '--disable-gpu',
                         '--user-data-dir=' + PROFILE, '--virtual-time-budget=20000',
                         '--dump-dom', 'http://127.0.0.1:%d/_lh.html' % port],
                        stdout=io.open(out, 'wb'), stderr=subprocess.DEVNULL)
        dom = io.open(out, encoding='utf-8', errors='replace').read()
        m = re.search(r'&lt;&lt;&lt;(.*?)&gt;&gt;&gt;', dom, re.S) or \
            re.search(r'<<<(.*?)>>>', dom, re.S)
        if not m:
            print('  *** no payload from port %d ***' % port)
            return []
        return json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&'))
    finally:
        srv.terminate()
        try:
            os.remove(p)
        except OSError:
            pass


if __name__ == '__main__':
    S9 = os.path.abspath(os.path.join(HERE, '..', 'phase9', 'site'))
    S8 = os.path.abspath(os.path.join(HERE, '..', 'phase8', 'site'))
    results = []
    for port, site in ((8809, S9), (8808, S8)):
        ts = [{'page': p, 'sel': s, 'label': l}
              for (pt, p, s, l) in TARGETS if pt == port]
        if ts:
            results += run(port, ts, site)

    print('=== USED LINE-HEIGHT: what `normal` actually resolves to ===')
    print('  %-30s %-10s %-9s %-8s %-6s %s'
          % ('element', 'computed', 'used px', 'ratio', 'lines', 'text'))
    for r in results:
        if r.get('error'):
            print('  %-30s %s' % (r['label'], r['error']))
            continue
        size = float(r['size'].replace('px', ''))
        print('  %-30s %-10s %-9.1f %-8.3f %-6d %s'
              % (r['label'], r['computed'], r['used'], r['used'] / size,
                 r['lines'], r['text']))

    print()
    card = [r for r in results if 'card title' in r.get('label', '') and 'used' in r]
    cart = [r for r in results if 'cart line title' in r.get('label', '') and 'used' in r]
    if card and cart:
        cu, ru = card[0]['used'], cart[0]['used']
        print('=== THE COMPARISON THAT MATTERS ===')
        print('  A product name on a CARD:       %.1fpx per line' % cu)
        print('  The same name in the CART:      %.1fpx per line' % ru)
        print('  Difference:                     %.1fpx per line (%.1f%%)'
              % (abs(cu - ru), abs(cu - ru) * 100.0 / cu))
        if abs(cu - ru) < 0.5:
            print('  -> SAME SPACING, spelled two ways. Not a visible defect;')
            print('     the token gap is real but nothing on screen moves.')
        else:
            print('  -> VISIBLY DIFFERENT once a title wraps to two lines.')
        print()
        print('  Does the cart title actually wrap? lines=%d at width=%dpx'
              % (cart[0]['lines'], cart[0]['realWidth']))
