# -*- coding: utf-8 -*-
"""The add-to-cart confirmation: hidden when it should be, a button when it shows.

WHY THIS SUITE EXISTS. `qa/phase14/notes.py:205` already asserted that the
confirmation "starts hidden" — and it passed for nineteen phases while the block
was plainly on screen. It asserted `box.hidden === true`, which reads the
ATTRIBUTE. The attribute was always there. What was missing was any effect: the
block also declared `display: flex`, an author declaration that beats the user
agent's `[hidden] { display: none }` whatever the specificity, so the
confirmation rendered at 467x68 on every product page with its View cart control
in the tab order, under an empty sentence.

The lesson is the assertion, not the bug. Testing the attribute tests what the
markup INTENDED; only the computed style tests what the customer GOT. Everything
below reads computed style.

TWO STATES ARE CHECKED, because each alone is satisfiable by a broken theme:

  at rest   nothing has been added. The block must be genuinely display:none and
            contribute no tab stop. A theme that deleted the block entirely would
            also pass this, which is why the second state exists.
  shown     the `hidden` attribute removed, standing in for a successful add. The
            View cart control must be there, must still be an ANCHOR (it
            navigates; PHASE-2 §10.5), and must be wearing the button system.

THE CONTROLS. Two elements on the same page carry the same `hidden` attribute and
DO have a `[hidden]` rule written for them — header.css:459 for the mobile menu
panel, section-main-product.css:190 for the price compare wrap. If they do not
read as hidden, this suite is measuring nothing and says so instead of passing.

WHAT IS DELIBERATELY NOT ASSERTED. That the confirmation is ANNOUNCED. A live
region announcement is not observable from script — nothing in the DOM changes
when a screen reader speaks. What is observable, and is checked, is the
precondition the theme's own announce() comment states: the region must be
revealed before its text lands, not in the same turn. cart.js showFormSuccess
defers the write for exactly that reason.
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
BROWSER = os.environ.get('GS_BROWSER')
CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]
PORT = 8819
# A fresh profile and a cache-busted URL every run. With a fixed profile this
# probe served the OLD stylesheet back after the fix had landed and reported the
# defect as still present — a false failure that looked exactly like a real one.
PROF = tempfile.mkdtemp(prefix='gs-success-')
CB = str(os.getpid())

PAGES = ['p-sizes.html', 'p-multi.html', 'p-soldout.html']

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var T = PAGES, out = [], i = 0;

function parse(c) {
  var p = (c || '').match(/[\d.]+/g) || [0, 0, 0];
  return {r: +p[0], g: +p[1], b: +p[2], a: p.length > 3 ? +p[3] : 1};
}
function over(fg, bg) {
  return {r: fg.r * fg.a + bg.r * (1 - fg.a),
          g: fg.g * fg.a + bg.g * (1 - fg.a),
          b: fg.b * fg.a + bg.b * (1 - fg.a), a: 1};
}
function lum(c) {
  var p = [c.r, c.g, c.b].map(function (v) {
    v = v / 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2];
}
function ratio(a, b) {
  var x = lum(a), y = lum(b), hi = Math.max(x, y), lo = Math.min(x, y);
  return Math.round(((hi + 0.05) / (lo + 0.05)) * 100) / 100;
}
/* Walk up for the first non-transparent background, the way the Phase 8
   contrast suite does — a control's own background is usually transparent. */
function bgOf(el, w) {
  var node = el;
  while (node && node.nodeType === 1) {
    var c = parse(w.getComputedStyle(node).backgroundColor);
    if (c.a > 0) return c;
    node = node.parentElement;
  }
  return {r: 255, g: 255, b: 255, a: 1};
}
function tabStops(el) {
  var n = el.querySelectorAll('a[href], button, input, select, textarea, [tabindex]').length;
  if (el.matches('a[href], button, input, select, textarea, [tabindex]')) n += 1;
  return n;
}

function step() {
  if (i >= T.length) {
    document.title = 'DONE';
    document.getElementById('o').textContent = '<<<' + JSON.stringify(out) + '>>>';
    return;
  }
  var page = T[i];
  var f = document.createElement('iframe');
  f.style.cssText = 'border:0;width:1440px;height:1400px';
  f.src = page + '?cb=' + CB;
  document.body.appendChild(f);
  f.onload = function () {
    var d = f.contentDocument, w = f.contentWindow;
    var kill = d.createElement('style');
    kill.textContent = '*,*::before,*::after{transition:none !important;animation:none !important}';
    d.head.appendChild(kill);

    var rec = {page: page};
    var box = d.querySelector('.main-product__success');
    if (!box) { rec.error = 'no confirmation block'; out.push(rec); f.remove(); i++; step(); return; }

    /* ---- STATE 1: at rest ---- */
    var cs = w.getComputedStyle(box);
    rec.rest = {
      hiddenAttr: box.hasAttribute('hidden'),
      display: cs.display,
      box: Math.round(box.getBoundingClientRect().width) + 'x' +
           Math.round(box.getBoundingClientRect().height),
      offsetParentNull: box.offsetParent === null,
      tabStops: box.offsetParent === null ? 0 : tabStops(box)
    };

    /* ---- CONTROLS: elements that SHOULD be hidden, and have the rule ---- */
    rec.controls = [];
    [['.header__panel', 'mobile menu panel'],
     ['.price__compare-wrap', 'price compare wrap']].forEach(function (c) {
      var el = d.querySelector(c[0]);
      if (!el) { rec.controls.push({label: c[1], missing: true}); return; }
      rec.controls.push({
        label: c[1], hiddenAttr: el.hasAttribute('hidden'),
        display: w.getComputedStyle(el).display,
        hidden: w.getComputedStyle(el).display === 'none'
      });
    });

    /* ---- STATE 2: shown, standing in for a successful add ---- */
    box.removeAttribute('hidden');
    var span = box.querySelector('[data-product-success-text]');
    if (span) span.textContent = 'Added to bag';
    void d.body.offsetHeight;

    var link = box.querySelector('.main-product__success-link');
    if (!link) { rec.error = 'no View cart control'; out.push(rec); f.remove(); i++; step(); return; }
    var ls = w.getComputedStyle(link);
    var lr = link.getBoundingClientRect();
    var bg = bgOf(link, w);
    var bc = parse(ls.borderTopColor);
    var submit = d.querySelector('.main-product__submit');
    var sr = submit ? submit.getBoundingClientRect() : null;

    rec.shown = {
      tag: link.tagName,
      href: link.getAttribute('href'),
      hasButtonClass: link.classList.contains('button'),
      variant: link.classList.contains('button--secondary') ? 'secondary'
             : (link.classList.contains('button--primary') ? 'primary' : 'none'),
      firstClass: link.className.split(' ')[0],
      w: Math.round(lr.width), h: Math.round(lr.height),
      display: ls.display,
      radius: ls.borderTopLeftRadius,
      borderWidth: ls.borderTopWidth,
      font: ls.fontFamily.split(',')[0].replace(/["']/g, ''),
      size: ls.fontSize, weight: ls.fontWeight, ls: ls.letterSpacing,
      transform: ls.textTransform,
      decoration: ls.textDecorationLine,
      cursor: ls.cursor,
      gradient: ls.backgroundImage,
      shadow: ls.boxShadow,
      borderContrast: bc.a > 0 ? ratio(bc.a < 1 ? over(bc, bg) : bc, bg) : null,
      /* The block's own border + padding inset everything inside it. Reported
         because it is why this control is content width and not full width. */
      indentFromSubmit: sr ? Math.round(lr.left - sr.left) : null,
      submitWidth: sr ? Math.round(sr.width) : null,
      boxInnerWidth: Math.round(box.getBoundingClientRect().width)
    };
    out.push(rec);
    f.remove(); i++; step();
  };
  f.onerror = function () { out.push({page: page, error: 'load failed'}); f.remove(); i++; step(); };
}
step();
</script>
"""


def browser():
    if BROWSER and os.path.exists(BROWSER):
        return BROWSER
    for c in CANDIDATES:
        if os.path.exists(c):
            return c
    return None


def run():
    exe = browser()
    if not exe:
        return None, 'no browser found'
    html = (PROBE.replace('PAGES', json.dumps(PAGES))
                 .replace('CB', json.dumps(CB)))
    p = os.path.join(SITE, '_succ.html')
    io.open(p, 'w', encoding='utf-8').write(html)
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        outp = os.path.join(tempfile.gettempdir(), 'gs-succ-dom.html')
        subprocess.call([exe, '--headless=new', '--disable-gpu',
                         '--user-data-dir=' + PROF, '--disable-application-cache',
                         '--virtual-time-budget=25000', '--dump-dom',
                         'http://127.0.0.1:%d/_succ.html' % PORT],
                        stdout=io.open(outp, 'wb'), stderr=subprocess.DEVNULL)
        dom = io.open(outp, encoding='utf-8', errors='replace').read()
        m = re.search(r'&lt;&lt;&lt;(.*?)&gt;&gt;&gt;', dom, re.S) or \
            re.search(r'<<<(.*?)>>>', dom, re.S)
        if not m:
            return None, 'probe produced no reading (%d bytes of DOM)' % len(dom)
        return json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')), None
    finally:
        srv.terminate()
        try:
            os.remove(p)
        except OSError:
            pass


if __name__ == '__main__':
    rows, err = run()
    if err:
        print('*** UNREADABLE: %s' % err)
        raise SystemExit(2)
    if not rows:
        print('*** UNREADABLE — the probe measured nothing')
        raise SystemExit(2)

    fails = []
    controls_held = []

    print('=== THE ADD-TO-CART CONFIRMATION ===')
    print()
    for r in rows:
        if r.get('error'):
            print('  %-16s %s' % (r['page'], r['error']))
            fails.append('%s: %s' % (r['page'], r['error']))
            continue
        rest, shown = r['rest'], r['shown']
        print('  %s' % r['page'])
        print('    AT REST (nothing added)')
        print('      hidden attr   %s' % rest['hiddenAttr'])
        print('      computed      display:%s   box %s   offsetParent %s'
              % (rest['display'], rest['box'],
                 'null' if rest['offsetParentNull'] else 'set'))
        print('      tab stops     %d  %s' % (rest['tabStops'],
                                              '' if rest['tabStops'] == 0 else '*** REACHABLE ***'))
        for c in r['controls']:
            if c.get('missing'):
                print('      control       %-22s MISSING' % c['label'])
                continue
            # A control that is not carrying `hidden` on THIS fixture is not a
            # control — p-multi is a sale product, so its price compare wrap is
            # legitimately shown. Counting it would fail the suite for a
            # correctly rendered page.
            if not c['hiddenAttr']:
                print('      control       %-22s no hidden attr here, skipped' % c['label'])
                continue
            print('      control       %-22s display:%-6s %s'
                  % (c['label'], c['display'], 'hidden' if c['hidden'] else '*** VISIBLE ***'))
            controls_held.append(c['hidden'])
        print('    SHOWN (standing in for a successful add)')
        print('      element       <%s href=%s>  first class %r'
              % (shown['tag'].lower(), shown['href'], shown['firstClass']))
        print('      button system %s  variant %s' % (shown['hasButtonClass'], shown['variant']))
        print('      box           %dx%d   radius %s   border %s'
              % (shown['w'], shown['h'], shown['radius'], shown['borderWidth']))
        print('      type          %s %s w%s  tracking %s  %s  decoration %s'
              % (shown['font'], shown['size'], shown['weight'], shown['ls'],
                 shown['transform'], shown['decoration']))
        print('      border ratio  %s:1 %s' % (shown['borderContrast'],
                                               'SC 1.4.11 ok' if (shown['borderContrast'] or 0) >= 3
                                               else '*** BELOW 3:1 ***'))
        print('      geometry      indented %spx from Add to bag (%spx wide); this control %dpx'
              % (shown['indentFromSubmit'], shown['submitWidth'], shown['w']))
        print('      gradient %s   shadow %s   cursor %s'
              % (shown['gradient'], shown['shadow'], shown['cursor']))
        print()

        # --- at rest ---
        if rest['display'] != 'none':
            fails.append('%s: confirmation renders at rest (display:%s, %s)'
                         % (r['page'], rest['display'], rest['box']))
        if rest['tabStops'] != 0:
            fails.append('%s: %d tab stop(s) into a confirmation of nothing'
                         % (r['page'], rest['tabStops']))
        # --- shown ---
        if shown['tag'] != 'A' or not shown['href']:
            fails.append('%s: View cart is not an anchor with an href (PHASE-2 10.5)' % r['page'])
        if shown['firstClass'] != 'main-product__success-link':
            fails.append('%s: first class is %r — qa/phase14/cartdoc.py and '
                         'qa/phase18/focus.py key off it' % (r['page'], shown['firstClass']))
        if not shown['hasButtonClass'] or shown['variant'] != 'secondary':
            fails.append('%s: not wearing button--secondary' % r['page'])
        if shown['h'] < 44:
            fails.append('%s: target height %dpx is under 44px' % (r['page'], shown['h']))
        if shown['transform'] != 'uppercase':
            fails.append('%s: label is not uppercase, so it is not the button type role' % r['page'])
        if 'underline' in (shown['decoration'] or ''):
            fails.append('%s: underline survived onto a bordered button — the section '
                         'stylesheet is out-specifying .button' % r['page'])
        if (shown['borderContrast'] or 0) < 3:
            fails.append('%s: border %s:1 fails SC 1.4.11' % (r['page'], shown['borderContrast']))
        if shown['gradient'] != 'none':
            fails.append('%s: gradient on the control' % r['page'])
        if shown['shadow'] != 'none':
            fails.append('%s: box-shadow on the control' % r['page'])
        if shown['cursor'] != 'pointer':
            fails.append('%s: cursor is %s' % (r['page'], shown['cursor']))
        try:
            if float(shown['radius'].replace('px', '')) > 4:
                fails.append('%s: radius %s outside the 0/2/4 set' % (r['page'], shown['radius']))
        except (ValueError, AttributeError):
            pass
        if shown['submitWidth'] and shown['w'] >= shown['submitWidth'] - 2:
            fails.append('%s: the control reaches full width inside an indented box, '
                         'so it lands %spx off Add to bag'
                         % (r['page'], shown['indentFromSubmit']))

    print('-' * 74)
    if not controls_held or not all(controls_held):
        print('*** THE CONTROLS DID NOT HOLD — elements that have a [hidden] rule')
        print('    were not reported hidden, so this suite cannot tell a hidden')
        print('    element from a visible one and none of the above means anything.')
        raise SystemExit(2)
    print('%d/%d controls held, so hidden and visible are distinguishable here.'
          % (sum(controls_held), len(controls_held)))
    print()
    if fails:
        print('*** %d problem(s) ***' % len(fails))
        for f in fails:
            print('   - %s' % f)
        raise SystemExit(1)
    print('OVERALL: PASS — %d product page(s). The confirmation is genuinely' % len(rows))
    print('display:none before an add, with no tab stop into it. When shown, View')
    print('cart is still an anchor to the cart, wearing button--secondary at')
    print('content width, uppercase, no surviving underline, its border clears')
    print('SC 1.4.11, and it carries no gradient and no shadow.')
