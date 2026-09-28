# -*- coding: utf-8 -*-
"""The product card's COMPUTED styles, in a browser.

catalog.py renders the card and asserts on its markup. That cannot see the
cascade: it confirmed the secondary image's rule said `opacity: 0` while a
higher-specificity sold-out rule was quietly repainting it to 0.6. Only a
browser can answer "which rule won".

The fixture that exposes it does not exist in the shipped set — a SOLD-OUT
product with two images — so it is composed here from P_MULTI, which has two,
by marking every variant unavailable. Nothing is invented: the fields are the
ones Shopify itself sets.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build  # noqa: E402
import surfaces  # noqa: E402
from miniliquid import wrap  # noqa: E402

EDGE = os.environ.get('GS_BROWSER') or r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 8809
SITE = os.path.join(HERE, 'site')
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-cascade')
FAILURES = []
CHECKS = [0]


def check(label, ok, detail=''):
    CHECKS[0] += 1
    print('  %-58s %s %s' % (label, 'OK  ' if ok else '*** FAIL ***',
                             '' if ok else str(detail)[:140]))
    if not ok:
        FAILURES.append(label)


def sold_out(product):
    """The same product, unavailable — as Shopify would report it."""
    d = dict(product)
    d['available'] = False
    d['variants'] = [wrap(dict(dict(v), available=False)) for v in product['variants']]
    first = dict(d['variants'][0])
    d['selected_or_first_available_variant'] = wrap(first)
    return wrap(d)


def build_page():
    e = surfaces.engine(template='collection')
    merged = dict(e.globals['settings'])
    merged['card_hover_secondary_image'] = True
    e.globals['settings'] = wrap(merged)

    src = open(os.path.join(build.THEME, 'snippets', 'product-card.liquid'),
               encoding='utf-8').read()
    cards = []
    for label, product in (('available', build.P_MULTI),
                           ('soldout', sold_out(build.P_MULTI))):
        html = e.render(src, {'product': product})
        cards.append('<div class="product-grid" data-case="%s">%s</div>' % (label, html))

    header = build.render_section(e, 'sections/header.liquid', 'header',
                                  dict(build.HEADER_SETTINGS))
    drawer = build.render_section(e, 'sections/cart-drawer.liquid', 'cart-drawer',
                                  dict(build.DRAWER_DEFAULTS))
    build.write('_cardcascade.html', [('cards', '\n'.join(cards))],
                header, drawer, template='collection')

    # The card's stylesheet is linked by the SECTIONS that use the card, not by
    # the snippet itself — so a page that renders the snippet bare gets no card
    # CSS at all, and every computed value read from it is a browser default.
    # The first run of this probe reported 900px stacked images, which is the
    # shape of "no stylesheet", not the shape of a cascade bug.
    p = os.path.join(build.OUT, '_cardcascade.html')
    html = open(p, encoding='utf-8').read()
    link = '<link rel="stylesheet" href="assets/component-product-card.css">'
    assert link not in html, 'the page already links the card CSS'
    open(p, 'w', encoding='utf-8').write(html.replace('</head>', link + '</head>', 1))
    return '_cardcascade.html'


PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre><script>
var res = {}, f = document.createElement('iframe');
f.style.cssText='width:1440px;height:900px;border:0;position:absolute;left:-9999px;top:0';
f.src='PAGE';
f.onload=function(){
  var d=f.contentDocument,w=f.contentWindow;
  var st=d.createElement('style');
  st.textContent='*,*::before,*::after{transition:none!important;animation:none!important}';
  d.head.appendChild(st);
  w.setTimeout(function(){
    ['available','soldout'].forEach(function(key){
      var box=d.querySelector('[data-case="'+key+'"]');
      if(!box){res[key]=null;return;}
      var primary=box.querySelector('.product-card__image:not(.product-card__image--secondary)');
      var second=box.querySelector('.product-card__image--secondary');
      res[key]={
        hasSecondary: !!second,
        primaryOpacity: primary? w.getComputedStyle(primary).opacity : null,
        secondaryOpacity: second? w.getComputedStyle(second).opacity : null,
        secondaryPosition: second? w.getComputedStyle(second).position : null,
        // Both images must occupy the same box, or the swap shifts the layout.
        primaryBox: primary? JSON.stringify(['x','y','width','height'].map(function(k){
          return Math.round(primary.getBoundingClientRect()[k]);})) : null,
        secondaryBox: second? JSON.stringify(['x','y','width','height'].map(function(k){
          return Math.round(second.getBoundingClientRect()[k]);})) : null,
        mediaHeight: Math.round(box.querySelector('.product-card__media').getBoundingClientRect().height)
      };
    });
    document.getElementById('o').textContent='<<<'+JSON.stringify(res)+'>>>';
    document.title='DONE';
  },300);
};
document.body.appendChild(f);
</script>"""


def run(page):
    open(os.path.join(SITE, '_cascade.html'), 'w', encoding='utf-8').write(
        PROBE.replace('PAGE', page))
    shutil.rmtree(PROFILE, ignore_errors=True)
    out = os.path.join(HERE, 'cascade-dom.html')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run',
                    '--no-default-browser-check', '--user-data-dir=' + PROFILE,
                    '--virtual-time-budget=40000', '--window-size=1600,1000', '--dump-dom',
                    'http://127.0.0.1:%d/_cascade.html' % PORT],
                   stdout=open(out, 'w', encoding='utf-8'), stderr=subprocess.DEVNULL)
    d = open(out, encoding='utf-8', errors='replace').read()
    m = re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>', d, re.S)
    if not m:
        return None
    return json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')
                      .replace('&lt;', '<').replace('&gt;', '>'))


if __name__ == '__main__':
    r = run(build_page())
    if not r:
        print('NO READING')
        raise SystemExit(1)

    for key, label in (('available', 'AVAILABLE product, two photos'),
                       ('soldout', 'SOLD-OUT product, two photos')):
        v = r.get(key)
        print('=== %s ===' % label)
        if not v:
            check('%s rendered' % label, False, 'no case found')
            continue
        print('    primary opacity %s, secondary opacity %s'
              % (v['primaryOpacity'], v['secondaryOpacity']))
        check('a secondary image is present', v['hasSecondary'] is True)
        check('the secondary is HIDDEN at rest (computed opacity 0)',
              v['secondaryOpacity'] == '0',
              'computed %s — a higher-specificity rule is repainting it'
              % v['secondaryOpacity'])
        check('the secondary is laid over the primary, not beside it',
              v['secondaryPosition'] == 'absolute')
        check('both images occupy exactly the same box, so nothing shifts',
              v['primaryBox'] == v['secondaryBox'],
              'primary %s vs secondary %s' % (v['primaryBox'], v['secondaryBox']))
        if key == 'soldout':
            check('the visible image still carries the sold-out dim',
                  v['primaryOpacity'] == '0.6', 'computed %s' % v['primaryOpacity'])
        else:
            check('an available product is not dimmed',
                  v['primaryOpacity'] == '1', 'computed %s' % v['primaryOpacity'])
        print()

    print('%d checks, %d passed, %d failed'
          % (CHECKS[0], CHECKS[0] - len(FAILURES), len(FAILURES)))
    print('OVERALL: %s' % ('PASS' if not FAILURES else '*** FAILURES ABOVE ***'))
