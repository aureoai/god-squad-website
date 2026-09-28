import tempfile
# -*- coding: utf-8 -*-
"""Contrast for every text role Phase 8 introduces.

Phase 7 had to sample pixels, because its copy sat over a photograph. Nothing
in Phase 8 does: the product page and the cart are flat surface tokens, so the
effective background can be composited exactly from the computed styles and the
ratio computed rather than estimated. That is stronger evidence, not weaker —
there is no sampling error in it.

Each role is reported with the size and weight it renders at, because the
threshold depends on them: WCAG 2.2 SC 1.4.3 wants 4.5:1 for normal text and
3:1 for large text, where large is 24px, or 18.66px at 700+.
"""
import os, re, json, shutil, subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = os.environ.get('GS_BROWSER') or r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 8808
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-contrast8')
SITE = os.path.join(HERE, 'site')

ROLES_PRODUCT = [
    ('product title', '.main-product__title'),
    ('vendor', '.main-product__vendor'),
    ('price, current', '.price__current'),
    ('price, compare-at', '.price__compare'),
    ('price, unit', '.price__unit'),
    ('variant option name', '.variant-picker__legend-name'),
    ('variant chosen value', '.variant-picker__legend-value'),
    ('variant chip', '.variant-picker__value-text'),
    ('variant chip, unavailable', '.variant-picker__value--unavailable .variant-picker__value-text'),
    ('quantity label', '.main-product__quantity-label'),
    ('quantity value', '.quantity__input'),
    ('add to cart label', '.main-product__submit'),
    ('description', '.main-product__description'),
    ('description list item', '.main-product__description li'),
    ('meta term', '.main-product__meta dt'),
    ('meta value', '.main-product__meta dd'),
    ('form error', '.main-product__error'),
]

ROLES_CART = [
    ('drawer title', '.cart-drawer__title'),
    ('line title', '.cart-line__title'),
    ('line variant', '.cart-line__variant'),
    ('line discount', '.cart-line__discount'),
    ('line error', '.cart-line__error'),
    ('line price', '.cart-line__price-final'),
    ('line price, original', '.cart-line__price-original'),
    ('remove', '.cart-line__remove'),
    ('quantity value', '.cart-line .quantity__input'),
    ('total label', '.cart-totals__row dt'),
    ('total value', '.cart-totals__row dd'),
    ('discount row', '.cart-totals__row--discount dt'),
    ('estimated total', '.cart-totals__row--final dd'),
    ('taxes note', '.cart-totals__note'),
    ('checkout label', '[data-cart-checkout]'),
    ('cart failure line', '[data-cart-error]'),
    ('view cart label', '.cart-drawer__actions .button--secondary'),
    # Phase 14
    ('continue shopping', '.cart-drawer__continue'),
]

# Phase 14. The order note, on both surfaces. Measured rather than reasoned
# about: every one of these reuses a pairing Phase 2 verified, and "reuses a
# verified pairing" is a claim about the cascade, which is the kind of claim
# this project has been wrong about before.
ROLES_NOTE = [
    ('note label', '.cart-note__summary-label'),
    ('note field text', '.cart-note__field'),
    ('note help', '.cart-note__help'),
]

ROLES_EMPTY = [
    ('empty title', '.cart-empty__title'),
    ('empty body', '.cart-empty__body'),
    ('empty button label', '.cart-empty .button'),
]

ROLES_CART_PAGE = [
    ('page title', '.main-cart__title'),
    ('line title', '.cart-line__title'),
    ('total label', '.cart-totals__row dt'),
    ('estimated total', '.cart-totals__row--final dd'),
    ('taxes note', '.cart-totals__note'),
    # Phase 14
    ('continue shopping', '.main-cart__continue'),
]

# Phase 14. The add confirmation, which only renders where no drawer opens.
ROLES_CONFIRM = [
    ('add confirmation', '[data-product-success] [data-product-success-text]'),
    ('confirmation link', '.main-product__success-link'),
    ('add failure line', '[data-product-error]'),
]

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var ROLES = ROLESJSON, OPEN = OPENFLAG;
var f = document.createElement('iframe');
f.style.cssText = 'width:1440px;height:2400px;border:0;position:absolute;left:-9999px;top:0';
f.src = 'SRC';
f.onload = function () {
  var d = f.contentDocument, win = f.contentWindow;
  win.setTimeout(function () {
    if (OPEN) { var b = d.querySelector('[data-cart-bubble]'); if (b) b.click(); }
    // The failure line only exists on screen when something has failed.
    [].forEach.call(d.querySelectorAll('[data-cart-error]'), function (el) {
      el.hidden = false;
      el.textContent = 'Measurement text.';
    });
    win.setTimeout(report, 200);
  }, 200);

  function parse(c) {
    var m = c.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    var p = m[1].split(',').map(function (x) { return parseFloat(x); });
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  }
  function over(fg, bg) {
    var a = fg.a;
    return { r: fg.r * a + bg.r * (1 - a), g: fg.g * a + bg.g * (1 - a),
             b: fg.b * a + bg.b * (1 - a), a: 1 };
  }
  function bgOf(el) {
    var stack = [], node = el;
    while (node && node.nodeType === 1) {
      var c = parse(win.getComputedStyle(node).backgroundColor);
      if (c && c.a > 0) stack.push(c);
      if (c && c.a === 1) break;
      node = node.parentElement;
    }
    var base = { r: 255, g: 255, b: 255, a: 1 };
    for (var i = stack.length - 1; i >= 0; i--) base = over(stack[i], base);
    return base;
  }
  function lum(c) {
    function ch(v) { v = v / 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }
    return 0.2126 * ch(c.r) + 0.7152 * ch(c.g) + 0.0722 * ch(c.b);
  }
  function ratio(a, b) {
    var l1 = lum(a), l2 = lum(b);
    return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
  }
  function hex(c) {
    function h(v) { var s = Math.round(v).toString(16); return s.length < 2 ? '0' + s : s; }
    return '#' + (h(c.r) + h(c.g) + h(c.b)).toUpperCase();
  }

  function report() {
    var out = [];
    ROLES.forEach(function (pair) {
      var el = d.querySelector(pair[1]);
      if (!el) { out.push({ role: pair[0], missing: true }); return; }
      var cs = win.getComputedStyle(el);
      var fgRaw = parse(cs.color);
      var bg = bgOf(el);
      var fg = fgRaw.a < 1 ? over(fgRaw, bg) : fgRaw;
      var size = parseFloat(cs.fontSize);
      var weight = parseInt(cs.fontWeight, 10) || 400;
      // Effective size: opacity on an ancestor dims the text too.
      var op = 1, node = el;
      while (node && node.nodeType === 1) {
        op *= parseFloat(win.getComputedStyle(node).opacity);
        node = node.parentElement;
      }
      if (op < 1) fg = over({ r: fg.r, g: fg.g, b: fg.b, a: op }, bg);
      var large = size >= 24 || (size >= 18.66 && weight >= 700);
      out.push({
        role: pair[0], fg: hex(fg), bg: hex(bg),
        size: Math.round(size * 10) / 10, weight: weight, opacity: Math.round(op * 100) / 100,
        ratio: Math.round(ratio(fg, bg) * 100) / 100,
        required: large ? 3 : 4.5
      });
    });
    document.getElementById('o').textContent = '<<<' + JSON.stringify(out) + '>>>';
    document.title = 'DONE';
  }
};
document.body.appendChild(f);
</script>
"""


def run(page, roles, open_drawer=False, tag=''):
    name = '_contrast-%s.html' % re.sub(r'[^a-z0-9]+', '-', (page + tag).lower())
    body = (PROBE.replace('SRC', page)
            .replace('ROLESJSON', json.dumps(roles))
            .replace('OPENFLAG', 'true' if open_drawer else 'false'))
    open(os.path.join(SITE, name), 'w', encoding='utf-8').write(body)
    out = os.path.join(HERE, 'contrast-dom.html')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run',
                    '--no-default-browser-check', '--user-data-dir=' + PROFILE,
                    '--virtual-time-budget=30000', '--window-size=1600,2600', '--dump-dom',
                    'http://127.0.0.1:%d/%s' % (PORT, name)],
                   stdout=open(out, 'w', encoding='utf-8'), stderr=subprocess.DEVNULL)
    d = open(out, encoding='utf-8', errors='replace').read()
    m = re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>', d, re.S)
    if not m:
        return None
    return json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')
                      .replace('&lt;', '<').replace('&gt;', '>'))


if __name__ == '__main__':
    shutil.rmtree(PROFILE, ignore_errors=True)
    passes = fails = missing = 0
    jobs = [
        ('p-details.html', ROLES_PRODUCT, False, 'product, cream'),
        ('p-ink.html', ROLES_PRODUCT, False, 'product, ink'),
        ('c-many.html', ROLES_CART, True, 'drawer, ink'),
        ('c-empty.html', ROLES_EMPTY, True, 'drawer empty, ink'),
        ('c-page-many.html', ROLES_CART_PAGE, False, 'cart page, ink'),
        ('c-noted.html', ROLES_NOTE, True, 'order note, drawer ink'),
        ('c-page-note.html', ROLES_NOTE + ROLES_CART_PAGE, False, 'order note, cart page ink'),
        ('p-nodrawer.html', ROLES_CONFIRM, False, 'add confirmation, cream'),
        ('p-rule.html', [('price, current', '.price__current'),
                         ('price, unit', '.price__unit')], False, 'unit price, cream'),
    ]
    for page, roles, open_drawer, tag in jobs:
        rows = run(page, roles, open_drawer, tag)
        print('=' * 88)
        print('%s  (%s)' % (tag.upper(), page))
        print('%-30s %-9s %-9s %6s %7s %7s %6s %s' %
              ('role', 'fg', 'bg', 'size', 'weight', 'ratio', 'needs', ''))
        if not rows:
            print('  NO READING')
            fails += 1
            continue
        for r in rows:
            if r.get('missing'):
                print('%-30s %s' % (r['role'], 'not present on this page'))
                missing += 1
                continue
            ok = r['ratio'] >= r['required']
            if ok:
                passes += 1
            else:
                fails += 1
            print('%-30s %-9s %-9s %6s %7s %7s %6s %s' %
                  (r['role'], r['fg'], r['bg'], r['size'], r['weight'],
                   r['ratio'], r['required'], 'PASS' if ok else '*** FAIL ***'))
    for f in os.listdir(SITE):
        if f.startswith('_contrast-'):
            os.remove(os.path.join(SITE, f))
    print()
    print('%d measurements, %d pass, %d fail, %d roles not on the page tested'
          % (passes + fails, passes, fails, missing))
