# -*- coding: utf-8 -*-
"""Design review against the six stated guidelines, measured rather than judged.

The guidelines:
  1. Maintain consistent spacing throughout layout elements.
  2. Restrict typography to 1-2 typefaces.
  3. Ensure proper alignment across all design components.
  4. Apply colour intentionally and purposefully.
  5. Ensure buttons clearly appear interactive and tappable.
  6. Incorporate actual content early in the process.

Five of the six are measurable from a rendered page; the sixth is a process
question about content, answered separately from the project record.

Everything here reads COMPUTED style out of a browser, because a value can
arrive from a token, a cascade, a media query or inheritance and only the
browser knows which won. Reading the stylesheets would answer a different
question.

Traps this avoids, all learned the hard way earlier in this project:
  - getClientRects() on an atomic inline returns ONE rect regardless of line
    count, so it cannot be used to count lines.
  - A transitioned property reads as its START value in the same frame, so
    transitions are killed before anything is measured.
  - Cross-origin iframes throw on contentDocument; a caught throw must be
    reported as "not measured", never as "everything matched".
"""
import io
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = os.environ.get('GS_BROWSER',
                      r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-review')
PAGES = {
    8809: ['home.html', 's-collection.html', 's-collection-filters.html',
           's-search.html', 's-search-none.html', 's-page.html', 's-404.html',
           's-collection-empty.html', 'c-page-note.html', 'c-page-empty.html'],
    8808: ['p-sizes.html', 'p-multi.html', 'p-details.html',
           'c-one.html', 'c-many.html', 'c-empty.html'],
}

# The spacing scale, in px. Anything used that is not on it is off-scale.
SCALE = {4: 1, 8: 2, 12: 3, 16: 4, 24: 5, 32: 6, 40: 7, 48: 8, 64: 9, 96: 10}

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var PAGES = PAGELIST, W = WIDTH, out = {pages: {}, errors: []}, i = 0;
function px(v) { var n = parseFloat(v); return isNaN(n) ? null : Math.round(n * 10) / 10; }
function step() {
  if (i >= PAGES.length) {
    document.title = 'DONE';
    document.getElementById('o').textContent = '<<<' + JSON.stringify(out) + '>>>';
    return;
  }
  var page = PAGES[i];
  var f = document.createElement('iframe');
  f.style.cssText = 'border:0;width:' + W + 'px;height:1200px';
  f.src = page;
  document.body.appendChild(f);
  f.onload = function () {
    var d = null;
    try { d = f.contentDocument; } catch (e) { d = null; }
    if (!d) { out.errors.push(page + ': cross-origin, NOT MEASURED'); f.remove(); i++; step(); return; }
    var w = f.contentWindow;

    /* Kill transitions: a transitioned property reads as its start value. */
    var kill = d.createElement('style');
    kill.textContent = '*,*::before,*::after{transition:none !important;animation:none !important}';
    d.head.appendChild(kill);
    void d.body.offsetHeight;

    var rec = {fonts: {}, space: {}, colors: {}, bg: {}, border: {}, buttons: [], rows: {}};
    var all = d.querySelectorAll('*');

    Array.prototype.forEach.call(all, function (el) {
      if (el.offsetParent === null && el.tagName !== 'BODY') return;
      var r = el.getBoundingClientRect();
      if (r.width === 0 && r.height === 0) return;
      var cs = w.getComputedStyle(el);

      /* --- 2. typefaces actually rendering, for elements with real text --- */
      var txt = '';
      for (var n = 0; n < el.childNodes.length; n++) {
        if (el.childNodes[n].nodeType === 3) txt += el.childNodes[n].nodeValue;
      }
      if (txt.trim().length) {
        var fam = cs.fontFamily.split(',')[0].replace(/['"]/g, '').trim();
        rec.fonts[fam] = (rec.fonts[fam] || 0) + 1;
      }

      /* --- 1. spacing values in use --- */
      ['marginTop','marginBottom','marginLeft','marginRight',
       'paddingTop','paddingBottom','paddingLeft','paddingRight',
       'rowGap','columnGap'].forEach(function (p) {
        var v = px(cs[p]);
        if (v && v > 0) rec.space[v] = (rec.space[v] || 0) + 1;
      });

      /* --- 4. colour --- */
      if (cs.color) rec.colors[cs.color] = (rec.colors[cs.color] || 0) + 1;
      if (cs.backgroundColor && cs.backgroundColor !== 'rgba(0, 0, 0, 0)') {
        rec.bg[cs.backgroundColor] = (rec.bg[cs.backgroundColor] || 0) + 1;
      }
      ['borderTopColor','borderBottomColor','borderLeftColor','borderRightColor'].forEach(function (p) {
        if (px(cs[p.replace('Color','Width')]) > 0) {
          rec.border[cs[p]] = (rec.border[cs[p]] || 0) + 1;
        }
      });

      /* --- 3. alignment: left edge of block children, per section --- */
      var sec = el.closest('section, .shopify-section, footer, header');
      if (sec && cs.display.indexOf('inline') !== 0 && r.width > 40) {
        var key = (sec.className || sec.tagName).toString().split(' ')[0];
        rec.rows[key] = rec.rows[key] || [];
        if (rec.rows[key].length < 400) {
          rec.rows[key].push(Math.round(r.left * 10) / 10);
        }
      }
    });

    /* --- 5. buttons: is it obviously pressable, and is it big enough? --- */
    var BSEL = 'button, [role=button], .button, a.button, input[type=submit]';
    Array.prototype.forEach.call(d.querySelectorAll(BSEL), function (el) {
      var r = el.getBoundingClientRect();
      if (r.width === 0 && r.height === 0) return;
      if (el.offsetParent === null) return;
      var cs = w.getComputedStyle(el);
      var hasBg = cs.backgroundColor && cs.backgroundColor !== 'rgba(0, 0, 0, 0)';
      var hasBorder = px(cs.borderTopWidth) > 0 || px(cs.borderBottomWidth) > 0;
      var hasUnderline = cs.textDecorationLine.indexOf('underline') >= 0;
      rec.buttons.push({
        cls: (el.className || el.tagName).toString().split(' ').slice(0, 2).join('.'),
        tag: el.tagName.toLowerCase(),
        w: Math.round(r.width), h: Math.round(r.height),
        cursor: cs.cursor,
        bg: hasBg, border: hasBorder, underline: hasUnderline,
        padX: px(cs.paddingLeft), padY: px(cs.paddingTop),
        radius: cs.borderRadius,
        boundary: hasBg || hasBorder || hasUnderline,
        text: (el.textContent || '').trim().slice(0, 24)
      });
    });

    out.pages[page] = rec;
    f.remove(); i++; step();
  };
  f.onerror = function () { out.errors.push(page + ': load failed'); f.remove(); i++; step(); };
}
step();
</script>
"""


def run(port, site, pages, width):
    avail = set(os.listdir(site))
    pages = [p for p in pages if p in avail]
    if not pages:
        return {'pages': {}, 'errors': []}
    html = PROBE.replace('PAGELIST', json.dumps(pages)).replace('WIDTH', str(width))
    p = os.path.join(site, '_review.html')
    io.open(p, 'w', encoding='utf-8').write(html)
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port)],
                           cwd=site, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        outp = os.path.join(HERE, 'review-%d-%d.html' % (port, width))
        subprocess.call([EDGE, '--headless=new', '--disable-gpu',
                         '--user-data-dir=' + PROFILE, '--virtual-time-budget=40000',
                         '--dump-dom', 'http://127.0.0.1:%d/_review.html' % port],
                        stdout=io.open(outp, 'wb'), stderr=subprocess.DEVNULL)
        dom = io.open(outp, encoding='utf-8', errors='replace').read()
        m = re.search(r'&lt;&lt;&lt;(.*?)&gt;&gt;&gt;', dom, re.S) or \
            re.search(r'<<<(.*?)>>>', dom, re.S)
        if not m:
            print('  *** no payload from port %d at %dpx ***' % (port, width))
            return {'pages': {}, 'errors': ['no payload']}
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
    WIDTH = int(os.environ.get('GS_WIDTH', '1440'))

    merged = {'pages': {}, 'errors': []}
    for port, site in ((8809, S9), (8808, S8)):
        r = run(port, site, PAGES[port], WIDTH)
        merged['pages'].update(r.get('pages', {}))
        merged['errors'] += r.get('errors', [])

    pages = merged['pages']
    io.open(os.path.join(HERE, 'review-%d.json' % WIDTH), 'w', encoding='utf-8').write(
        json.dumps(merged, indent=1))

    print('=' * 78)
    print('DESIGN REVIEW — %d surfaces measured at %dpx' % (len(pages), WIDTH))
    print('=' * 78)
    if merged['errors']:
        print('NOT MEASURED: %s' % '; '.join(merged['errors']))
    print()

    # ---------------------------------------------------- 2. typefaces
    fonts = Counter()
    for rec in pages.values():
        for f, n in (rec.get('fonts') or {}).items():
            fonts[f] += n
    print('--- GUIDELINE 2: RESTRICT TYPOGRAPHY TO 1-2 TYPEFACES ---')
    for f, n in fonts.most_common():
        print('  %-30s %5d rendered text element(s)' % (f, n))
    print('  => %d typeface(s) actually rendering.  %s'
          % (len(fonts), 'PASS' if len(fonts) <= 2 else '*** OVER BUDGET ***'))
    print()

    # ---------------------------------------------------- 1. spacing
    space = Counter()
    for rec in pages.values():
        for v, n in (rec.get('space') or {}).items():
            space[float(v)] += n
    on = Counter({v: n for v, n in space.items() if int(round(v)) in SCALE})
    off = Counter({v: n for v, n in space.items() if int(round(v)) not in SCALE})
    total = sum(space.values())
    print('--- GUIDELINE 1: CONSISTENT SPACING ---')
    print('  %d distinct spacing values in use, %d declarations total'
          % (len(space), total))
    print('  on the scale:  %3d value(s), %5d uses (%.1f%%)'
          % (len(on), sum(on.values()), 100.0 * sum(on.values()) / max(1, total)))
    print('  off the scale: %3d value(s), %5d uses (%.1f%%)'
          % (len(off), sum(off.values()), 100.0 * sum(off.values()) / max(1, total)))
    print()
    print('  the off-scale values, most used first:')
    for v, n in off.most_common(22):
        print('    %8.1fpx  x%-5d' % (v, n))
    print()

    # ---------------------------------------------------- 4. colour
    col, bg, bd = Counter(), Counter(), Counter()
    for rec in pages.values():
        for k, n in (rec.get('colors') or {}).items():
            col[k] += n
        for k, n in (rec.get('bg') or {}).items():
            bg[k] += n
        for k, n in (rec.get('border') or {}).items():
            bd[k] += n
    print('--- GUIDELINE 4: APPLY COLOUR INTENTIONALLY ---')
    print('  %d distinct text colours, %d backgrounds, %d border colours'
          % (len(col), len(bg), len(bd)))
    for label, c in (('text', col), ('background', bg), ('border', bd)):
        print('  %s:' % label)
        for k, n in c.most_common(12):
            print('    %-34s x%d' % (k, n))
    print()

    # ---------------------------------------------------- 3. alignment
    print('--- GUIDELINE 3: ALIGNMENT ---')
    print('  Distinct left edges per section. A section whose children start at')
    print('  many near-but-unequal x values is misaligned; a small set of edges')
    print('  is a deliberate indent structure.')
    print()
    worst = []
    for page, rec in sorted(pages.items()):
        for sec, lefts in (rec.get('rows') or {}).items():
            uniq = sorted(set(lefts))
            # near-duplicates: edges within 4px of each other but not equal
            near = 0
            for a in range(len(uniq) - 1):
                if 0 < uniq[a + 1] - uniq[a] <= 4:
                    near += 1
            worst.append((near, len(uniq), page, sec, uniq[:8]))
    worst.sort(reverse=True)
    print('  %-26s %-28s %5s %5s  %s'
          % ('page', 'section', 'edges', 'near', 'first edges'))
    for near, nuniq, page, sec, sample in worst[:16]:
        flag = '  <-- near-miss edges' if near else ''
        print('  %-26s %-28s %5d %5d  %s%s'
              % (page[:26], sec[:28], nuniq, near,
                 ', '.join('%g' % x for x in sample), flag))
    tot_near = sum(w[0] for w in worst)
    print()
    print('  total near-miss edge pairs across all sections: %d' % tot_near)
    print()

    # ---------------------------------------------------- 5. buttons
    btns = []
    for page, rec in pages.items():
        for b in (rec.get('buttons') or []):
            b['page'] = page
            btns.append(b)
    print('--- GUIDELINE 5: BUTTONS LOOK INTERACTIVE AND TAPPABLE ---')
    print('  %d button instance(s) measured' % len(btns))
    byclass = defaultdict(list)
    for b in btns:
        byclass[b['cls']].append(b)
    print()
    print('  %-34s %4s %-9s %-8s %-9s %s'
          % ('control', 'n', 'size', 'cursor', 'boundary', 'min height'))
    small, noboundary, nocursor = [], [], []
    for cls, group in sorted(byclass.items()):
        hs = [g['h'] for g in group]
        ws = [g['w'] for g in group]
        b0 = group[0]
        boundary = ('bg' if b0['bg'] else '') + ('+border' if b0['border'] else '') \
            + ('+underline' if b0['underline'] else '')
        ok_h = min(hs) >= 44
        if min(hs) < 44:
            small.append((cls, min(hs)))
        if not b0['boundary']:
            noboundary.append(cls)
        if b0['cursor'] != 'pointer':
            nocursor.append((cls, b0['cursor']))
        print('  %-34s %4d %-9s %-8s %-9s %d%s'
              % (cls[:34], len(group), '%dx%d' % (max(ws), max(hs)),
                 b0['cursor'], boundary or 'NONE', min(hs),
                 '' if ok_h else '  <-- under 44'))
    print()
    print('  controls with NO visual boundary (no bg, border or underline): %s'
          % (', '.join(noboundary) if noboundary else 'none'))
    print('  controls whose cursor is not pointer: %s'
          % (', '.join('%s(%s)' % x for x in nocursor) if nocursor else 'none'))
    print('  controls under 44px tall: %s'
          % (', '.join('%s(%dpx)' % x for x in small) if small else 'none'))
    print()
    print('=' * 78)
