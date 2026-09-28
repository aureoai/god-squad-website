import tempfile
# -*- coding: utf-8 -*-
"""The Phase 9 responsive measurement.

Every page, at every viewport the brief names, in an iframe of exactly that CSS
size — headless Edge's own window never gives the layout the width it is asked
for, which Phase 5 measured and every phase since has re-confirmed.

It reports what the brief asks to be checked, and it reports it as numbers:
horizontal overflow and the element causing it, every tappable control smaller
than the minimum, the rendered type sizes, the grid's actual column count and
card width, and the geometry of the three things that move most — the hero, the
drawer and the mobile menu.
"""
import os, re, json, shutil, subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = os.environ.get('GS_BROWSER') or r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 8809
SITE = os.path.join(HERE, 'site')
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-respond')
# The brief's matrix, plus the two landscape cases it asks for.
VIEWPORTS = [
    (375, 812), (390, 844), (430, 932), (480, 1040),
    # 820 is a Phase 18 addition: the spec names it explicitly and this list had
    # 834 (iPad Pro) instead, so the nine required widths were eight.
    (768, 1024), (820, 1180), (834, 1194), (1024, 1366),
    (1280, 800), (1440, 900), (1920, 1080),
    (812, 375), (932, 430),      # landscape
]

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var PAGE = 'SRC', MODE = 'MODEFLAG';
var W = WIDTHS, res = {}, i = 0;

function step() {
  if (i >= W.length) {
    document.getElementById('o').textContent = '<<<' + JSON.stringify(res) + '>>>';
    document.title = 'DONE';
    return;
  }
  var pair = W[i++], w = pair[0], h = pair[1];
  var f = document.createElement('iframe');
  f.style.cssText = 'width:' + w + 'px;height:' + h + 'px;border:0;position:absolute;left:-9999px;top:0';
  f.src = PAGE;
  f.onload = function () {
    var d = f.contentDocument, win = f.contentWindow;
    var st = d.createElement('style');
    st.textContent = '*,*::before,*::after{transition:none!important;animation:none!important}'
      + '::-webkit-scrollbar{width:0!important;height:0!important;display:none!important}'
      + 'html{scrollbar-width:none}';
    d.head.appendChild(st);
    win.setTimeout(function () {
      if (MODE === 'drawer') { var b = d.querySelector('[data-cart-bubble]'); if (b) b.click(); }
      if (MODE === 'menu') { var m = d.querySelector('[data-menu-toggle]'); if (m) m.click(); }
      win.setTimeout(function () { res[w + 'x' + h] = measure(d, win, w, h); f.remove(); step(); }, 140);
    }, 160);
  };
  document.body.appendChild(f);
}

function measure(d, win, w, h) {
  function box(s) {
    var e = d.querySelector(s); if (!e) return null;
    var r = e.getBoundingClientRect();
    return [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)];
  }
  function cs(s, p) { var e = d.querySelector(s); return e ? win.getComputedStyle(e)[p] : null; }
  function fs(s) { var e = d.querySelector(s); return e ? Math.round(parseFloat(win.getComputedStyle(e).fontSize) * 10) / 10 : null; }
  function lines(s) {
    var e = d.querySelector(s); if (!e) return null;
    var lh = parseFloat(win.getComputedStyle(e).lineHeight);
    if (isNaN(lh)) lh = parseFloat(win.getComputedStyle(e).fontSize) * 1.2;
    return Math.round(e.getBoundingClientRect().height / lh);
  }

  // --------------------------------------------------- horizontal overflow
  var over = [];
  d.querySelectorAll('body *').forEach(function (e) {
    var r = e.getBoundingClientRect();
    if (r.width <= 0) return;
    var style = win.getComputedStyle(e);
    if (style.position === 'fixed') return;
    if (r.right > w + 0.5 || r.left < -0.5) {
      var cl = (e.className && e.className.baseVal !== undefined) ? e.className.baseVal : (e.className || e.tagName);
      over.push(String(cl).trim().split(/\s+/)[0].slice(0, 36) + '|' + Math.round(r.left) + '..' + Math.round(r.right));
    }
  });

  // ------------------------------------------------------- tappable targets
  var small = [], tiny = [], count = 0;
  d.querySelectorAll('a[href],button,input:not([type=hidden]),select,textarea,summary,[tabindex="0"]').forEach(function (e) {
    if (e.disabled) return;
    var st = win.getComputedStyle(e);
    if (st.visibility === 'hidden' || st.display === 'none') return;
    if (e.classList && e.classList.contains('visually-hidden')) return;
    if (e.closest('[data-harness-stub]')) return;
    if (e.closest('[inert]')) return;
    var r = e.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return;
    count++;
    var label = e.tagName + '.' + String((e.className && e.className.baseVal !== undefined)
      ? e.className.baseVal : (e.className || '')).trim().split(/\s+/)[0].slice(0, 30);
    var dim = Math.round(r.width) + 'x' + Math.round(r.height);
    if (r.width < 24 || r.height < 24) tiny.push(label + ' ' + dim);
    else if (r.width < 44 || r.height < 44) small.push(label + ' ' + dim);
  });

  // -------------------------------------------------------- the grid itself
  var grid = d.querySelector('.product-grid');
  var gridInfo = null;
  if (grid) {
    var tracks = win.getComputedStyle(grid).gridTemplateColumns.split(' ').filter(Boolean);
    var card = d.querySelector('.product-card');
    gridInfo = {
      cols: tracks.length,
      track: tracks[0],
      gap: win.getComputedStyle(grid).columnGap,
      card: card ? Math.round(card.getBoundingClientRect().width) : null,
      title: fs('.product-card__title'),
      price: fs('.product-card__price')
    };
  }

  return {
    scrollW: d.documentElement.scrollWidth,
    hscroll: d.documentElement.scrollWidth > w + 1,
    overflow: over.slice(0, 4),
    targets: count,
    tiny: tiny.slice(0, 5),
    small: small.slice(0, 5),
    grid: gridInfo,
    // type
    h1: fs('h1'), h1lines: lines('h1'),
    h2: fs('h2'),
    body: fs('.hero__description, .our-story__body p, .main-product__description p'),
    // the three movers
    hero: box('.hero'), heroInner: box('.hero__inner'), heroCta: box('.hero__cta'),
    heroMinH: cs('.hero', 'minHeight'),
    story: box('.our-story'), storyMedia: box('.our-story__media'),
    storyCols: cs('.our-story__inner', 'gridTemplateColumns'),
    pdp: box('.main-product__inner'), pdpCols: cs('.main-product__inner', 'gridTemplateColumns'),
    panel: box('.cart-drawer__panel'),
    panelFooter: box('.cart-drawer__footer'),
    scroller: (function () {
      var e = d.querySelector('.cart-drawer__scroller');
      if (!e) return null;
      return [Math.round(e.clientHeight), Math.round(e.scrollHeight)];
    })(),
    menu: box('.header__panel'),
    headerInner: box('.header__inner'),
    bodyLocked: d.body.style.position === 'fixed'
  };
}
step();
</script>
"""


def run(page, mode='none'):
    name = '_r-%s-%s.html' % (page.replace('.html', ''), mode)
    open(os.path.join(SITE, name), 'w', encoding='utf-8').write(
        PROBE.replace('SRC', page).replace('MODEFLAG', mode)
        .replace('WIDTHS', json.dumps(VIEWPORTS)))
    out = os.path.join(HERE, 'respond-dom.html')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run',
                    '--no-default-browser-check', '--force-prefers-reduced-motion',
                    '--user-data-dir=' + PROFILE, '--virtual-time-budget=120000',
                    '--window-size=2200,2600', '--dump-dom',
                    'http://127.0.0.1:%d/%s' % (PORT, name)],
                   stdout=open(out, 'w', encoding='utf-8'), stderr=subprocess.DEVNULL)
    d = open(out, encoding='utf-8', errors='replace').read()
    m = re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>', d, re.S)
    if not m:
        return None
    return json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')
                      .replace('&lt;', '<').replace('&gt;', '>'))


def w(b):
    return b[2] if b else 0


if __name__ == '__main__':
    shutil.rmtree(PROFILE, ignore_errors=True)
    jobs = [a.split(':') for a in sys.argv[1:]] or [
        ['home.html', 'none'], ['home.html', 'menu'], ['home-cart.html', 'drawer'],
        ['p-sizes.html', 'none'], ['p-multi.html', 'none'],
        ['c-page-many.html', 'none'],
    ]
    problems = 0
    for job in jobs:
        page, mode = (job + ['none'])[:2]
        data = run(page, mode)
        tag = page + ('' if mode == 'none' else ' [%s open]' % mode)
        print('=' * 118)
        print(tag)
        if not data:
            print('  NO READING')
            problems += 1
            continue
        print('%10s %7s %4s %5s %-18s %-5s %-5s %-24s %s' %
              ('viewport', 'scrollW', 'ovf', 'tgts', 'grid c/card/gap',
               'h1', 'ln', 'panel w/foot/scroll', 'flags'))
        for k in data:
            r = data[k]
            flags = []
            if r['hscroll']:
                flags.append('OVERFLOW ' + ','.join(r['overflow'][:2]))
                problems += 1
            if r['tiny']:
                flags.append('UNDER-24 ' + ','.join(r['tiny'][:2]))
                problems += 1
            if r['small']:
                flags.append('UNDER-44 ' + ','.join(r['small'][:3]))
            g = r['grid']
            gtxt = ('%d/%s/%s' % (g['cols'], g['card'], g['gap'])) if g else '-'

            if mode == 'menu':
                panel = 'menu %s@%s' % (w(r['menu']), r['menu'][0] if r['menu'] else '-')
            elif mode == 'drawer':
                foot = r['panelFooter']
                sc = r['scroller']
                panel = '%s/%s/%s' % (
                    w(r['panel']),
                    ('%d..%d' % (foot[1], foot[1] + foot[3])) if foot else '-',
                    ('%d<%d' % (sc[0], sc[1])) if sc else '-')
            else:
                panel = r['pdpCols'] or r['storyCols'] or (r['heroMinH'] or '-')
                panel = str(panel)[:24]
            print('%10s %7s %4s %5s %-18s %-5s %-5s %-24s %s' %
                  (k, r['scrollW'], 'YES' if r['hscroll'] else '-', r['targets'],
                   gtxt, r['h1'], r['h1lines'], panel,
                   ' | '.join(flags) or 'ok'))
    print()
    print('hard problems (overflow or under-24 targets): %d' % problems)
