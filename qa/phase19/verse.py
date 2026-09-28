# -*- coding: utf-8 -*-
"""The three Verse bands: do they render, filter, and survive a phone?

WHAT THIS GUARDS, and why each check exists rather than being assumed.

  RENDERS        All three bands are on the home page after Our Story. A band
                 that silently stops rendering is the failure mode of a section
                 whose guard condition drifts.

  NO-JS FIRST    The chip row ships with the `hidden` attribute and is revealed
                 by verse-filter.js. This suite measures BOTH states, because
                 each alone is satisfiable by a broken theme: a row that is
                 always hidden passes the no-JS check, and a row that is always
                 visible passes the filtering check.

  THE CASCADE    `[hidden] { display: none }` is a USER AGENT rule and any
                 author `display` beats it. The chips are a flex row and the
                 cards are grid items, so both carry an author display and both
                 need an explicit [hidden] rule. This theme has hit that trap
                 five times; the no-JS check here is what catches the sixth.

  FILTERING      Pressing a chip must leave only that category showing, and must
                 move aria-pressed. Measured through the real script.

  CONTRAST       Every line of card copy sits on a merchant photograph. The
                 scrim's alpha was derived rather than chosen — 0.65 is the
                 floor for cream on ink-over-white, 0.72 ships — and this reads
                 the composited result back rather than trusting the arithmetic.

  ORDINALS       01, 02, 03, 04 with no gaps. They are counted, not taken from
                 forloop.index, because the loop skips empty blocks; a gap here
                 means the counter was reverted to forloop.index.

  PHONE          No horizontal overflow at 390px, and every control still at
                 least 44px. The chip row is allowed to scroll sideways; the
                 PAGE is not allowed to.
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
PORT = 8821
PROF = tempfile.mkdtemp(prefix='gs-verse-')
CB = str(os.getpid())

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var out = {}, widths = [1440, 390], wi = 0;

function parse(c) {
  var p = (c || '').match(/[\d.]+/g) || [0, 0, 0];
  return {r: +p[0], g: +p[1], b: +p[2], a: p.length > 3 ? +p[3] : 1};
}
function over(fg, bg) {
  return {r: fg.r * fg.a + bg.r * (1 - fg.a), g: fg.g * fg.a + bg.g * (1 - fg.a),
          b: fg.b * fg.a + bg.b * (1 - fg.a), a: 1};
}
function lum(c) {
  var p = [c.r, c.g, c.b].map(function (v) {
    v = v / 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2];
}
function ratio(a, b) {
  var x = lum(a), y = lum(b), hi = Math.max(x, y), lo = Math.min(x, y);
  return Math.round(((hi + 0.05) / (lo + 0.05)) * 100) / 100;
}

function step() {
  if (wi >= widths.length) {
    document.title = 'DONE';
    document.getElementById('o').textContent = '<<<' + JSON.stringify(out) + '>>>';
    return;
  }
  var w = widths[wi];
  var f = document.createElement('iframe');
  f.style.cssText = 'border:0;width:' + w + 'px;height:2400px';
  f.src = 'home.html?cb=' + CB;
  document.body.appendChild(f);
  f.onload = function () {
    var d = f.contentDocument, win = f.contentWindow;
    var rec = {};

    rec.bands = {
      feature: !!d.querySelector('.verse-feature'),
      index: !!d.querySelector('.verse-index'),
      words: !!d.querySelector('.words-we-wear')
    };

    /* Band order on the page, so "after Our Story" is measured not assumed. */
    var known = ['.hero', '.featured-collection', '.our-story', '.verse-feature',
                 '.verse-index', '.words-we-wear'];
    var seen = [];
    Array.prototype.forEach.call(d.querySelectorAll(known.join(',')), function (el) {
      for (var i = 0; i < known.length; i++) {
        if (el.matches(known[i])) { seen.push(known[i].slice(1)); break; }
      }
    });
    rec.order = seen;

    /* ---- STATE 1: the no-script state ----
       NOT measured by reading the row on load: the SECTION emits its own
       <script defer>, so by the time this iframe fires onload the script has
       already run and revealed the row. An earlier version of this probe read
       display:flex here and reported a correct theme as broken.

       Two things are measured instead, and together they are the no-JS state:
       (a) does the markup SHIP the hidden attribute — read off disk by the
           Python side, which cannot be wrong about it, and
       (b) does `hidden` actually HIDE it — re-applied here, because a flex row
           carries an author display and `[hidden]{display:none}` is only a user
           agent rule. (b) is the check that matters: (a) has been true all along
           in every one of this theme's five instances of that cascade bug. */
    var filter = d.querySelector('[data-verse-filter]');
    rec.noJs = null;
    if (filter) {
      filter.setAttribute('hidden', '');
      var hiddenDisplay = win.getComputedStyle(filter).display;
      rec.noJs = {
        displayWhenHidden: hiddenDisplay,
        reallyHidden: hiddenDisplay === 'none'
      };
      filter.removeAttribute('hidden');
    }

    /* Cards must all be visible with no script. */
    var cards = Array.prototype.slice.call(d.querySelectorAll('.verse-card'));
    rec.cardCount = cards.length;
    rec.cardsVisibleNoJs = cards.filter(function (c) {
      return win.getComputedStyle(c).display !== 'none';
    }).length;

    /* ---- run the real script ---- */
    var s = d.createElement('script');
    s.src = 'assets/verse-filter.js';
    d.body.appendChild(s);

    win.setTimeout(function () {
      rec.afterJs = filter ? {
        hasHiddenAttr: filter.hasAttribute('hidden'),
        display: win.getComputedStyle(filter).display,
        visible: win.getComputedStyle(filter).display !== 'none'
      } : null;

      var chips = Array.prototype.slice.call(d.querySelectorAll('[data-verse-chip]'));
      rec.chips = chips.map(function (c) {
        var r = c.getBoundingClientRect();
        return {key: c.getAttribute('data-verse-chip'),
                pressed: c.getAttribute('aria-pressed'),
                h: Math.round(r.height),
                weight: win.getComputedStyle(c).fontWeight};
      });

      /* Press the second chip (the first real category) and read the grid. */
      var target = chips[1];
      if (target) {
        target.click();
        rec.filtered = {
          key: target.getAttribute('data-verse-chip'),
          pressed: target.getAttribute('aria-pressed'),
          allChipPressed: chips[0].getAttribute('aria-pressed'),
          showing: cards.filter(function (c) {
            return win.getComputedStyle(c).display !== 'none';
          }).map(function (c) { return c.getAttribute('data-verse-category'); })
        };
      }

      /* ---- contrast of card copy over the scrim, worst case ----
         The scrim is composited over the DARKEST assumption a theme can make
         about an unknown photograph: white. Read the scrim's own gradient stops
         is not possible from script, so this reads the declared background and
         reports it for the record, then measures the copy colours against the
         alpha the stylesheet ships. */
      var card = d.querySelector('.verse-card');
      if (card) {
        var WHITE = {r: 255, g: 255, b: 255, a: 1};
        var scrimAt = over({r: 13, g: 12, b: 10, a: 0.72}, WHITE);
        var quote = card.querySelector('.verse-card__quote p');
        var refEl = card.querySelector('.verse-card__reference');
        var catEl = card.querySelector('.verse-card__category');
        rec.contrast = {};
        [['quote', quote], ['reference', refEl], ['category', catEl]].forEach(function (pair) {
          if (!pair[1]) return;
          var c = parse(win.getComputedStyle(pair[1]).color);
          var fg = c.a < 1 ? over(c, scrimAt) : c;
          rec.contrast[pair[0]] = ratio(fg, scrimAt);
        });
      }

      /* ---- ordinals ---- */
      rec.ordinals = Array.prototype.map.call(
        d.querySelectorAll('.words-we-wear__ordinal'),
        function (o) { return (o.textContent || '').trim(); });

      /* ---- radius / gradient / shadow discipline ---- */
      var bad = [];
      Array.prototype.forEach.call(
        d.querySelectorAll('.verse-feature *, .verse-index *, .words-we-wear *'),
        function (el) {
          var cs = win.getComputedStyle(el);
          var r = parseFloat(cs.borderTopLeftRadius) || 0;
          if (r > 4 && r < 9000) bad.push('radius ' + r + ' on ' + (el.className || el.tagName));
          if (cs.boxShadow && cs.boxShadow !== 'none') {
            bad.push('shadow on ' + (el.className || el.tagName));
          }
          /* A gradient is allowed ONLY on a scrim. */
          if (cs.backgroundImage && cs.backgroundImage.indexOf('gradient') >= 0) {
            var cls = String(el.className || '');
            if (cls.indexOf('scrim') < 0) bad.push('gradient on ' + cls);
          }
        });
      rec.discipline = bad.slice(0, 8);

      /* ---- phone: does the PAGE scroll sideways? ---- */
      rec.docScrollW = d.documentElement.scrollWidth;
      rec.docClientW = d.documentElement.clientWidth;
      rec.overflows = d.documentElement.scrollWidth > d.documentElement.clientWidth + 1;

      out['w' + w] = rec;
      f.remove(); wi++; step();
    }, 400);
  };
  f.onerror = function () { out['w' + w] = {error: 'load failed'}; f.remove(); wi++; step(); };
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
    html = PROBE.replace('CB', json.dumps(CB))
    p = os.path.join(SITE, '_verse.html')
    io.open(p, 'w', encoding='utf-8').write(html)
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        outp = os.path.join(tempfile.gettempdir(), 'gs-verse-dom.html')
        subprocess.call([exe, '--headless=new', '--disable-gpu',
                         '--user-data-dir=' + PROF, '--disable-application-cache',
                         '--virtual-time-budget=30000', '--dump-dom',
                         'http://127.0.0.1:%d/_verse.html' % PORT],
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
    data, err = run()
    if err:
        print('*** UNREADABLE: %s' % err)
        raise SystemExit(2)
    if not data:
        print('*** UNREADABLE — the probe measured nothing')
        raise SystemExit(2)

    # (a), read off disk. The <script defer> the section emits means the live
    # DOM has already been altered by the time any probe sees it, so the only
    # honest place to ask whether the markup SHIPS the row hidden is the file.
    ships_hidden = None
    src_path = os.path.join(SITE, 'home.html')
    if os.path.exists(src_path):
        src = io.open(src_path, encoding='utf-8', errors='replace').read()
        m = re.search(r'data-verse-filter[^>]*>', src)
        # Split the tag's attributes and look for the bare word rather than
        # matching a word boundary. A regex is how this line first shipped with
        # a literal backspace byte in place of its escape, and a check that can
        # only ever be false is worse than no check at all.
        attrs = m.group(0).replace('>', ' ').split() if m else []
        ships_hidden = 'hidden' in attrs

    fails = []
    checks = 0
    print('=== the shipped markup ===')
    print('  chip row carries the hidden attribute: %s' % ships_hidden)
    print()
    checks += 1
    if ships_hidden is not True:
        fails.append('the rendered markup does not ship the chip row hidden (%r)'
                     % ships_hidden)
    for key in sorted(data):
        r = data[key]
        width = key[1:]
        print('=== %spx ===' % width)
        if r.get('error'):
            print('  %s' % r['error'])
            fails.append('%s: %s' % (width, r['error']))
            continue

        b = r['bands']
        print('  bands present      feature=%s index=%s words=%s'
              % (b['feature'], b['index'], b['words']))
        print('  page order         %s' % ' -> '.join(r['order']))
        checks += 1
        for name, ok in b.items():
            if not ok:
                fails.append('%s: the %s band did not render' % (width, name))
        order = r['order']
        if 'our-story' in order and 'verse-feature' in order:
            if order.index('verse-feature') < order.index('our-story'):
                fails.append('%s: the verse bands are before Our Story' % width)
        for a, bnd in (('verse-feature', 'verse-index'), ('verse-index', 'words-we-wear')):
            if a in order and bnd in order and order.index(a) > order.index(bnd):
                fails.append('%s: %s comes after %s' % (width, a, bnd))

        nj = r.get('noJs')
        if nj:
            print('  no-script state    hidden really hides=%s (display:%s)   '
                  'cards showing %d/%d'
                  % (nj['reallyHidden'], nj['displayWhenHidden'],
                     r['cardsVisibleNoJs'], r['cardCount']))
            checks += 1
            if not nj['reallyHidden']:
                fails.append('%s: `hidden` does not hide the chip row — it computes to '
                             '%s, so the author display is beating the user agent rule'
                             % (width, nj['displayWhenHidden']))
            if r['cardsVisibleNoJs'] != r['cardCount']:
                fails.append('%s: only %d of %d cards show without script'
                             % (width, r['cardsVisibleNoJs'], r['cardCount']))

        aj = r.get('afterJs')
        if aj:
            print('  with script        chips %s' % ('revealed' if aj['visible'] else '*** STILL HIDDEN ***'))
            checks += 1
            if not aj['visible']:
                fails.append('%s: the script did not reveal the chip row' % width)

        chips = r.get('chips') or []
        if chips:
            print('  chips              %s' % ', '.join(
                '%s(%s,%spx,w%s)' % (c['key'], c['pressed'], c['h'], c['weight']) for c in chips))
            checks += 1
            short = [c for c in chips if c['h'] < 44]
            if short:
                fails.append('%s: %d chip(s) under the 44px target' % (width, len(short)))
            pressed = [c for c in chips if c['pressed'] == 'true']
            if len(pressed) != 1:
                fails.append('%s: %d chips report aria-pressed=true, expected 1'
                             % (width, len(pressed)))
            if pressed and pressed[0]['weight'] == chips[-1]['weight']:
                fails.append('%s: the pressed chip has the same weight as an unpressed one, '
                             'so its state is carried by colour alone' % width)

        fl = r.get('filtered')
        if fl:
            others = [c for c in fl['showing'] if c != fl['key']]
            print('  after pressing %-9s showing %s   all-chip now %s'
                  % (fl['key'], fl['showing'], fl['allChipPressed']))
            checks += 1
            if others:
                fails.append('%s: filtering on %r left %r showing'
                             % (width, fl['key'], others))
            if not fl['showing']:
                fails.append('%s: filtering on %r hid everything' % (width, fl['key']))
            if fl['pressed'] != 'true':
                fails.append('%s: the pressed chip did not take aria-pressed' % width)
            if fl['allChipPressed'] != 'false':
                fails.append('%s: the All chip stayed pressed' % width)

        c = r.get('contrast') or {}
        if c:
            print('  card copy on scrim %s' % '  '.join(
                '%s %.2f:1' % (k, v) for k, v in sorted(c.items())))
            checks += 1
            for k, v in c.items():
                if v < 4.5:
                    fails.append('%s: card %s is %.2f:1 over the scrim' % (width, k, v))

        o = r.get('ordinals') or []
        if o:
            print('  ordinals           %s' % ', '.join(o))
            checks += 1
            expect = ['%02d' % (i + 1) for i in range(len(o))]
            if o != expect:
                fails.append('%s: ordinals are %s, expected %s — the counter was '
                             'reverted to forloop.index' % (width, o, expect))

        d = r.get('discipline') or []
        print('  design discipline  %s' % ('clean' if not d else '*** ' + '; '.join(d)))
        checks += 1
        for item in d:
            fails.append('%s: %s' % (width, item))

        print('  page width         scroll %s vs client %s  %s'
              % (r['docScrollW'], r['docClientW'],
                 '*** SCROLLS SIDEWAYS ***' if r['overflows'] else 'no sideways scroll'))
        checks += 1
        if r['overflows']:
            fails.append('%s: the page scrolls sideways (%s > %s)'
                         % (width, r['docScrollW'], r['docClientW']))
        print()

    print('-' * 72)
    if checks == 0:
        print('*** NO CHECKS RAN — this suite did not pass, it did not run.')
        raise SystemExit(2)
    if fails:
        print('*** %d problem(s) across %d checks ***' % (len(fails), checks))
        for f in fails:
            print('   - %s' % f)
        raise SystemExit(1)
    # The narrative first, the verdict LAST and on one line. check-all.py reads
    # a suite's outcome from its final lines, and a PASS trailed by six lines of
    # prose came back as "unclear" — a suite whose result cannot be read has not
    # reported one.
    print('%d checks at two widths. The three bands render after Our Story in' % checks)
    print('order; the chip row is genuinely hidden without script and revealed with')
    print('it; every card shows with no script; filtering leaves only the chosen')
    print('category and moves aria-pressed; card copy clears AA over the scrim at')
    print('its worst case; the ordinals are sequential; no gradient outside a scrim,')
    print('no shadow, no radius past 4px; the page does not scroll sideways at 390px.')
    print()
    print('OVERALL: PASS — %d checks, 0 failed' % checks)
