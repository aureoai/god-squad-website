# -*- coding: utf-8 -*-
"""Phase 16 — CSS coverage, measured by matching every selector against every page.

WHY MEASURED RATHER THAN READ.

"Is this rule dead?" is exactly the question a careful reader gets wrong: a
class can be built by string concatenation in a {% liquid %} block, added by
JavaScript at runtime, or live only in a state the reader did not think of. So
this loads every built page in a real browser and asks the DOM.

WHAT IT CANNOT KNOW, and therefore never reports as dead:
  - anything behind a pseudo-class or pseudo-element (:hover, :focus-visible,
    ::before) — the base selector is tested instead
  - a class JavaScript adds only after an interaction (.is-open, .facets--drawer,
    .cart-drawer-open) — these are collected from the theme's own JS and treated
    as live
  - a state that no harness page happens to render

So a selector reported here is a CANDIDATE, checked against every surface the
harness builds. It is evidence for a human decision, not an instruction.
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
S9 = os.path.abspath(os.path.join(HERE, '..', 'phase9', 'site'))
S8 = os.path.abspath(os.path.join(HERE, '..', 'phase8', 'site'))
THEME = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'god-squad-theme')
EDGE = os.environ.get('GS_BROWSER',
                      r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-cssuse')
PAGES = [
    (8809, 'home.html'), (8809, 's-collection.html'), (8809, 's-collection-filters.html'),
    (8809, 's-collection-applied.html'), (8809, 's-search.html'), (8809, 's-search-none.html'),
    (8809, 's-page.html'), (8809, 's-404.html'), (8809, 's-list-collections.html'),
    (8809, 'c-noted.html'), (8809, 'c-page-note.html'),
    (8808, 'p-sizes.html'), (8808, 'p-multi.html'), (8808, 'p-soldout.html'),
    (8808, 'p-long.html'), (8808, 'p-rule.html'), (8808, 'p-carousel.html'),
    (8808, 'p-ink.html'), (8808, 'p-details.html'), (8808, 'p-minimal.html'),
    (8808, 'p-nodrawer.html'),
    (8808, 'c-one.html'), (8808, 'c-many.html'), (8808, 'c-empty.html'),
    (8808, 'c-page-many.html'), (8808, 'c-page-empty.html'),
]

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var SELS = SELECTORS, PAGES = PAGELIST, seen = {}, bad = {}, failed = [], i = 0;
function step() {
  if (i >= PAGES.length) {
    document.title = 'DONE';
    document.getElementById('o').textContent = '<<<' + JSON.stringify({seen: seen, bad: bad, failed: failed}) + '>>>';
    return;
  }
  var f = document.createElement('iframe');
  f.style.cssText = 'border:0;width:1440px;height:900px';
  f.src = PAGES[i];
  document.body.appendChild(f);
  f.onload = function () {
    var d = null;
    try { d = f.contentDocument; } catch (e) { d = null; }
    if (!d) {
      /* Cross-origin: the document cannot be read. This MUST NOT be treated as
         "every selector matched" — the first version did exactly that, via a
         catch that set seen[s] = 1, and reported 100% coverage including two
         deliberately dead selectors. Skip the page and record that it failed. */
      failed.push(PAGES[i]);
      f.remove(); i++; step();
      return;
    }
    for (var k = 0; k < SELS.length; k++) {
      var s = SELS[k];
      if (seen[s]) continue;
      /* An invalid selector throws. That is a bug in the extractor, not a
         match — record it separately rather than counting it as covered. */
      try { if (d.querySelector(s)) seen[s] = 1; } catch (e) { bad[s] = 1; }
    }
    f.remove(); i++; step();
  };
  f.onerror = function () { f.remove(); i++; step(); };
}
step();
</script>
"""

# Pseudo-classes and pseudo-elements the DOM cannot be asked about directly.
PSEUDO = re.compile(r'::?[a-z-]+(\([^)]*\))?')


def split_top_level(text):
    """Split a selector list on commas that are NOT inside parentheses.

    :where(a, button, input) is ONE selector containing commas. Splitting on
    every comma turned it into the fragments "(a", "button", "input)" — which
    are invalid CSS, were reported as unmatched, and inflated the dead-selector
    count. The first version of this file did exactly that.
    """
    parts, depth, cur = [], 0, []
    for ch in text:
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        if ch == ',' and depth == 0:
            parts.append(''.join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append(''.join(cur))
    return [p.strip() for p in parts if p.strip()]


def selectors_from(css):
    """Every selector in a stylesheet.

    Walks the text tracking brace depth rather than regexing line-by-line: a
    selector list may span several lines, and taking only the last line before
    the brace truncated every one of them.
    """
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    out, buf, depth = [], [], 0
    i = 0
    while i < len(css):
        ch = css[i]
        if ch == '{':
            prelude = ''.join(buf).strip()
            buf = []
            depth += 1
            if prelude and not prelude.startswith('@'):
                out.extend(split_top_level(re.sub(r'\s+', ' ', prelude)))
        elif ch == '}':
            buf = []
            depth = max(0, depth - 1)
        else:
            buf.append(ch)
        i += 1
    return out


def testable(sel):
    """The selector with pseudo bits removed, or None if nothing is left."""
    base = PSEUDO.sub('', sel).strip()
    base = re.sub(r'\s+', ' ', base)
    # Stripping a trailing :where(...) or ::before leaves a dangling combinator,
    # which is invalid CSS. `.main-page__content >` becomes `.main-page__content > *`.
    base = re.sub(r'[>+~]\s*$', '> *', base).strip()
    if not base or base in ('*', ':root'):
        return None
    return base


if __name__ == '__main__':
    shutil.rmtree(PROFILE, ignore_errors=True)

    # Collect every selector, remembering which file it came from.
    by_sel = {}
    for f in sorted(os.listdir(os.path.join(THEME, 'assets'))):
        if not f.endswith('.css'):
            continue
        css = io.open(os.path.join(THEME, 'assets', f), encoding='utf-8').read()
        for sel in selectors_from(css):
            t = testable(sel)
            if t:
                by_sel.setdefault(t, set()).add(f)

    # Classes the theme's own JavaScript adds. These are live by definition and
    # a harness page that never opens a drawer would otherwise report them dead.
    js = '\n'.join(io.open(os.path.join(THEME, 'assets', f), encoding='utf-8').read()
                   for f in os.listdir(os.path.join(THEME, 'assets')) if f.endswith('.js'))
    js_classes = set(re.findall(r"classList\.(?:add|remove|toggle|replace)\('([\w-]+)'", js))
    js_classes |= set(re.findall(r"classList\.replace\('[\w-]+',\s*'([\w-]+)'", js))
    # Attributes JavaScript sets, likewise.
    js_attrs = set(re.findall(r"setAttribute\('([\w-]+)'", js))

    sels = sorted(by_sel)

    # ONE RUN PER ORIGIN. An iframe on 8809 cannot read a document served from
    # 8808 — different port, different origin — so a single run silently lost
    # every product and cart page. The two runs are merged here.
    seen, bad, failed = {}, {}, []
    for port, site in ((8809, S9), (8808, S8)):
        mine = ['http://127.0.0.1:%d/%s' % (p, n) for p, n in PAGES if p == port]
        src = (PROBE.replace('SELECTORS', json.dumps(sels))
                    .replace('PAGELIST', json.dumps(mine)))
        io.open(os.path.join(site, '_cssuse.html'), 'w', encoding='utf-8').write(src)
        out = os.path.join(HERE, 'cssuse-dom-%d.html' % port)
        subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run',
                        '--no-default-browser-check', '--user-data-dir=' + PROFILE,
                        '--virtual-time-budget=90000', '--window-size=1500,1000',
                        '--dump-dom',
                        'http://127.0.0.1:%d/_cssuse.html' % port],
                       stdout=io.open(out, 'w', encoding='utf-8'),
                       stderr=subprocess.DEVNULL)
        d = io.open(out, encoding='utf-8', errors='replace').read()
        m = re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>', d, re.S)
        if not m:
            print('NO READING from port %d' % port)
            print(d[-900:])
            raise SystemExit(1)
        payload = json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')
                             .replace('&lt;', '<').replace('&gt;', '>'))
        seen.update(payload['seen'])
        bad.update(payload['bad'])
        failed.extend(payload['failed'])

    if failed:
        print('*** %d page(s) could not be read — coverage below is INCOMPLETE:' % len(failed))
        for f in failed:
            print('      ', f)
        print()
    if bad:
        print('*** %d selector(s) the extractor produced are invalid CSS:' % len(bad))
        for s in sorted(bad)[:10]:
            print('      ', s)
        print()

    matched = [s for s in sels if seen.get(s)]
    unmatched = [s for s in sels if not seen.get(s)]

    # Split the unmatched into "explained by a JS-added class or attribute" and
    # genuine candidates.
    explained, candidates = [], []
    for s in unmatched:
        cls = set(re.findall(r'\.([\w-]+)', s))
        att = set(re.findall(r'\[([\w-]+)', s))
        if cls & js_classes or att & js_attrs:
            explained.append(s)
        else:
            candidates.append(s)

    print('=== CSS COVERAGE, MEASURED ACROSS %d PAGES ===' % len(PAGES))
    print()
    print('  selectors in the theme      %4d' % len(sels))
    print('  matched on some page        %4d  (%.0f%%)' % (len(matched), 100.0 * len(matched) / len(sels)))
    print('  unmatched                   %4d' % len(unmatched))
    print('    explained by a JS state   %4d' % len(explained))
    print('    genuine candidates        %4d' % len(candidates))
    print()
    if explained:
        print('--- unmatched but LIVE: a class or attribute the theme\'s JS sets ---')
        for s in explained[:40]:
            print('   %-58s %s' % (s[:58], ', '.join(sorted(by_sel[s]))[:40]))
    print()
    # A selector can go unmatched for two very different reasons, and conflating
    # them is what makes automated dead-CSS reports untrustworthy:
    #   - the class exists in the Liquid but no harness page renders that
    #     section or state  -> a HARNESS GAP, the CSS is alive
    #   - the class appears nowhere in any Liquid file at all
    #     -> genuinely DEAD, and safe to consider removing
    liquid = []
    for root, _d, files in os.walk(THEME):
        for f in files:
            if f.endswith(('.liquid', '.json')):
                liquid.append(io.open(os.path.join(root, f), encoding='utf-8').read())
    liquid_src = '\n'.join(liquid)

    # Classes assembled at render time, e.g.
    #   assign classes = classes | append: ' hero--align-' | append: settings.text_alignment
    # The literal `hero--align-centre` appears in no file, but the class is
    # produced whenever a merchant picks that setting. Collect the PREFIXES and
    # treat any class beginning with one as live. Without this the report calls
    # every merchant-selectable variant dead, which is how an automated dead-CSS
    # list gets someone to delete a working feature.
    prefixes = set(re.findall(r"append:\s*'[^']*?([\w]+--[\w-]*-)'", liquid_src))
    prefixes |= set(re.findall(r"append:\s*'\s*([\w-]+--[\w-]*-)'", liquid_src))

    def live_class(c):
        if c in liquid_src:
            return True
        return any(c.startswith(p) for p in prefixes)

    gaps, dead = [], []
    for s in candidates:
        classes = re.findall(r'\.([\w-]+)', s)
        if classes and all(live_class(c) for c in classes):
            gaps.append(s)
        else:
            dead.append(s)

    print('--- UNMATCHED but the class IS in the Liquid: a harness gap, not dead CSS ---')
    print('    (%d selectors — the section or state exists but no built page renders it)' % len(gaps))
    bysheet = {}
    for s in gaps:
        for f in by_sel[s]:
            bysheet.setdefault(f, []).append(s)
    for f in sorted(bysheet):
        print('   %-34s %d' % (f, len(bysheet[f])))

    print()
    print('--- DEAD: no Liquid file mentions these classes at all ---')
    if not dead:
        print('   none')
    for s in dead:
        print('   %-58s %s' % (s[:58], ', '.join(sorted(by_sel[s]))[:48]))
