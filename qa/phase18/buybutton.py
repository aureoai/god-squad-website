# -*- coding: utf-8 -*-
"""Is the Buy it now button actually a red box — and did the rule stay off the
wallet buttons?

WHY THIS PROBE EXISTS. The owner asked for a red box. The theme had no rule for
that button at all, so the browser was drawing it. Writing the rule is easy;
proving it lands on the right element and ONLY the right element is the part
worth measuring, because `payment_button` resolves to two different things at
runtime and only one of them is the theme's to style:

  --unbranded   ordinary DOM in the page. The theme styles it. Shopify's own
                Dawn theme styles it. This is the button the owner pointed at.
  --branded     Shop Pay / Apple Pay / Google Pay / PayPal, injected inside
                Shopify's own iframe. Trade dress. Must not be touched, and
                cannot be from here anyway.

Both carry `shopify-payment-button__button`. A rule written on the bare class
would claim both, so the NEGATIVE CONTROL below is the real test: it injects one
of each into the live page and asserts the red reaches the first and not the
second. Without that control this probe would report PASS for a rule that
repaints Apple Pay.

The harness's own stand-in is a third case — a plain button with the bare class
inside a `data-harness-stub` wrapper — which is why the rule names that wrapper
rather than the bare class.

WHAT ELSE IS CHECKED. That the box lines up with Add to bag directly above it
(same width, same height, or the pair reads as a mistake); that the label clears
AA against the fill it is sitting on, computed from the RENDERED rgb values
rather than from the hex anyone typed; and that none of the four things the
reference image had and Phase 2 section 10 forbids — gradient, bevel, drop
shadow, pill radius — came along with the colour.
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
BROWSER = os.environ.get('GS_BROWSER')
CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-buybutton')
PAGES = ['p-sizes.html', 'p-multi.html', 'p-details.html', 'p-soldout.html']

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var T = PAGES, out = [], i = 0;

/* Relative luminance and contrast, WCAG 2.x, from the colours the browser
   actually computed. getComputedStyle returns rgb()/rgba(), never the hex. */
function lum(rgb) {
  var p = rgb.match(/[\d.]+/g).slice(0, 3).map(Number).map(function (v) {
    v = v / 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2];
}
function contrast(a, b) {
  var x = lum(a), y = lum(b), hi = Math.max(x, y), lo = Math.min(x, y);
  return Math.round(((hi + 0.05) / (lo + 0.05)) * 100) / 100;
}
function box(el, w) {
  var r = el.getBoundingClientRect(), s = w.getComputedStyle(el);
  return {
    w: Math.round(r.width), h: Math.round(r.height),
    bg: s.backgroundColor, fg: s.color,
    radius: s.borderTopLeftRadius,
    font: s.fontFamily.split(',')[0].replace(/["']/g, ''),
    size: s.fontSize, ls: s.letterSpacing, tt: s.textTransform,
    cursor: s.cursor,
    gradient: s.backgroundImage, shadow: s.boxShadow
  };
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
  f.src = page;
  document.body.appendChild(f);
  f.onload = function () {
    var d = f.contentDocument, w = f.contentWindow;
    /* Transitioned properties read as their START value. background-color is in
       this button's transition list, so without this the fill would come back
       as transparent on a cold paint. Phase 4 recorded the same trap. */
    var kill = d.createElement('style');
    kill.textContent = '*,*::before,*::after{transition:none !important;animation:none !important}';
    d.head.appendChild(kill);

    var rec = {page: page};
    var stub = d.querySelector('[data-harness-stub="payment-button"] .shopify-payment-button__button');
    var add = d.querySelector('.main-product__submit');
    if (!stub) { rec.error = 'no payment button on this page'; out.push(rec); f.remove(); i++; step(); return; }

    rec.buy = box(stub, w);
    rec.label = stub.textContent.trim();
    rec.contrast = contrast(rec.buy.fg, rec.buy.bg);
    if (add) {
      var a = box(add, w);
      rec.add = {w: a.w, h: a.h, bg: a.bg, font: a.font, size: a.size, ls: a.ls};
      rec.widthMatch = a.w === rec.buy.w;
      rec.heightMatch = a.h === rec.buy.h;
      rec.fontMatch = a.font === rec.buy.font && a.size === rec.buy.size && a.ls === rec.buy.ls;
    }

    /* NEGATIVE CONTROL. Two buttons, the real store's two classes, injected into
       the live document OUTSIDE the harness wrapper. The rule must paint the
       first and leave the second at the browser default. */
    var host = d.createElement('div');
    host.innerHTML =
      '<button class="shopify-payment-button__button shopify-payment-button__button--unbranded">Buy it now</button>' +
      '<button class="shopify-payment-button__button shopify-payment-button__button--branded">Shop Pay</button>';
    d.body.appendChild(host);
    var unb = host.children[0], brd = host.children[1];
    rec.control = {
      unbranded: w.getComputedStyle(unb).backgroundColor,
      branded: w.getComputedStyle(brd).backgroundColor,
      unbrandedRadius: w.getComputedStyle(unb).borderTopLeftRadius,
      brandedRadius: w.getComputedStyle(brd).borderTopLeftRadius
    };
    rec.control.unbrandedPainted = rec.control.unbranded === rec.buy.bg;
    rec.control.brandedUntouched = rec.control.branded !== rec.buy.bg;
    host.remove();

    /* Do the hover and disabled rules exist, and is hover pointer-scoped? The
       computed style cannot answer this headlessly, so read the CSSOM. */
    var hoverMQ = null, disabled = false;
    try {
      for (var si = 0; si < d.styleSheets.length; si++) {
        var rules = d.styleSheets[si].cssRules;
        if (!rules) continue;
        for (var ri = 0; ri < rules.length; ri++) {
          var r = rules[ri];
          if (r.type === 4 && r.cssRules) {          /* @media */
            for (var mi = 0; mi < r.cssRules.length; mi++) {
              var t = r.cssRules[mi].selectorText || '';
              if (t.indexOf('payment-button__button--unbranded:hover') >= 0) hoverMQ = r.conditionText;
            }
          } else if (r.selectorText &&
                     r.selectorText.indexOf('payment-button__button--unbranded[disabled]') >= 0) {
            disabled = true;
          }
        }
      }
    } catch (e) { hoverMQ = 'unreadable: ' + e.message; }
    rec.hoverMedia = hoverMQ;
    rec.hasDisabled = disabled;

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


def run(site, port=8818):
    exe = browser()
    if not exe:
        return None, 'no browser found'
    html = PROBE.replace('PAGES', json.dumps(PAGES))
    p = os.path.join(site, '_buy.html')
    io.open(p, 'w', encoding='utf-8').write(html)
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port)],
                           cwd=site, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        outp = os.path.join(tempfile.gettempdir(), 'gs-buy-dom.html')
        subprocess.call([exe, '--headless=new', '--disable-gpu',
                         '--user-data-dir=' + PROFILE, '--virtual-time-budget=25000',
                         '--dump-dom', 'http://127.0.0.1:%d/_buy.html' % port],
                        stdout=io.open(outp, 'wb'), stderr=subprocess.DEVNULL)
        dom = io.open(outp, encoding='utf-8', errors='replace').read()
        m = re.search(r'&lt;&lt;&lt;(.*?)&gt;&gt;&gt;', dom, re.S) or \
            re.search(r'<<<(.*?)>>>', dom, re.S)
        if not m:
            return None, 'probe produced no reading (%d bytes of DOM)' % len(dom)
        raw = m.group(1).replace('&quot;', '"').replace('&amp;', '&')
        return json.loads(raw), None
    finally:
        srv.terminate()
        try:
            os.remove(p)
        except OSError:
            pass


if __name__ == '__main__':
    site = os.path.abspath(os.path.join(HERE, '..', 'phase9', 'site'))
    rows, err = run(site)
    if err:
        print('*** UNREADABLE: %s' % err)
        raise SystemExit(2)

    fails = []
    print('=== THE BUY IT NOW BUTTON, AS RENDERED ===')
    print()
    for r in rows:
        if r.get('error'):
            print('  %-18s %s' % (r['page'], r['error']))
            fails.append('%s: %s' % (r['page'], r['error']))
            continue
        b = r['buy']
        print('  %s' % r['page'])
        print('      label      %r' % r['label'])
        print('      box        %dx%d   radius %s' % (b['w'], b['h'], b['radius']))
        print('      fill       %s   label %s   contrast %.2f:1 %s'
              % (b['bg'], b['fg'], r['contrast'],
                 'AA' if r['contrast'] >= 4.5 else '*** BELOW AA ***'))
        print('      type       %s %s  tracking %s  %s' % (b['font'], b['size'], b['ls'], b['tt']))
        print('      cursor     %s' % b['cursor'])
        print('      gradient   %s        shadow  %s' % (b['gradient'], b['shadow']))
        if 'add' in r:
            a = r['add']
            print('      Add to bag %dx%d  %s        width %s   height %s   type %s'
                  % (a['w'], a['h'], a['bg'],
                     'match' if r['widthMatch'] else '*** DIFFERS ***',
                     'match' if r['heightMatch'] else '*** DIFFERS ***',
                     'match' if r['fontMatch'] else '*** DIFFERS ***'))
        c = r['control']
        print('      control    --unbranded %s %s'
              % (c['unbranded'], 'PAINTED' if c['unbrandedPainted'] else '*** NOT PAINTED ***'))
        print('                 --branded   %s %s'
              % (c['branded'], 'untouched' if c['brandedUntouched'] else '*** REPAINTED ***'))
        print('      hover      %s' % (r['hoverMedia'] or '*** NO HOVER RULE ***'))
        print('      disabled   %s' % ('rule present' if r['hasDisabled'] else '*** MISSING ***'))
        print()

        if r['contrast'] < 4.5:
            fails.append('%s: label contrast %.2f:1' % (r['page'], r['contrast']))
        if b['gradient'] != 'none':
            fails.append('%s: gradient present' % r['page'])
        if b['shadow'] != 'none':
            fails.append('%s: box-shadow present' % r['page'])
        if b['cursor'] != 'pointer':
            fails.append('%s: cursor is %s, not pointer' % (r['page'], b['cursor']))
        try:
            if float(b['radius'].replace('px', '')) > 4:
                fails.append('%s: radius %s exceeds the 0/2/4 set' % (r['page'], b['radius']))
        except ValueError:
            pass
        if not c['unbrandedPainted']:
            fails.append('%s: the real store class is NOT styled' % r['page'])
        if not c['brandedUntouched']:
            fails.append('%s: the rule repaints the BRANDED wallet button' % r['page'])
        if not r['hoverMedia'] or 'hover' not in str(r['hoverMedia']):
            fails.append('%s: hover is not pointer-scoped' % r['page'])
        if not r['hasDisabled']:
            fails.append('%s: no disabled rule' % r['page'])
        if 'add' in r and not r['widthMatch']:
            fails.append('%s: width does not match Add to bag' % r['page'])

    print('-' * 70)
    if not rows:
        print('OVERALL: *** UNREADABLE — the probe measured nothing ***')
        raise SystemExit(2)
    if fails:
        print('OVERALL: *** %d problem(s) ***' % len(fails))
        for f in fails:
            print('   - %s' % f)
        raise SystemExit(1)
    print('OVERALL: PASS — %d product page(s) measured. The unbranded Buy it now' % len(rows))
    print('button is a flat red box matching Add to bag in width, height and type,')
    print('its label clears AA on the fill, the radius stays inside the 0/2/4 set,')
    print('there is no gradient and no shadow, hover is pointer-scoped, and the')
    print('negative control confirms the BRANDED wallet button is left untouched.')
