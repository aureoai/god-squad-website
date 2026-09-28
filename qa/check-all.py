# -*- coding: utf-8 -*-
"""GOD SQUAD — check the whole theme, in one command.

    python check-all.py

Runs every automated suite against the CURRENT theme and prints one verdict.
Nothing here is new testing: it is the suites Phases 4-18 already built,
collected behind a single entry point so the whole thing can be checked without
knowing which of thirty-odd scripts to run or in what order.

WHAT IT DOES FOR YOU, so the results mean something:

  1. Rebuilds both harness sites from the theme on disk. Skipping this is the
     classic way to test yesterday's code and believe it was today's.
  2. Starts the two HTTP servers the browser suites need, on 8808 and 8809, and
     stops them afterwards. Four suites do NOT start their own and silently
     report NO READING without them.
  3. Runs Theme Check through @shopify/theme-check-node.
  4. Separates a FAILURE from a NO READING. A suite that cannot get a browser
     reading has not passed and has not failed — it has not run, and saying so
     is the difference between a green board and an honest one.

WHAT IT CANNOT CHECK, and no amount of local testing will:

  - The purchase flow. Add-to-cart, cart updates, search, filtering and checkout
    are Shopify's, and there is no Shopify here.
  - Real merchant data. Every fixture is invented. Phase 18 found a live defect
    that was invisible on short fixture names and visible on realistic ones.
  - Real photography, real Section Rendering API responses, real
    content_for_header, real image CDN behaviour, live Theme Check.

    Those need the theme on a real store. GODSQUAD-THEME-REFERENCE-MANUAL.md
    section 10 is the runbook for getting it there.

FLAGS
    --fast      skip the browser suites (structure and Liquid only, ~30s)
    --list      print the suite inventory and exit
"""
import io
import json
import os
import re
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
THEME = os.environ.get('GS_THEME') or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'god-squad-theme')

# (group, script, needs_browser, one-line description)
SUITES = [
    ('Structure & Liquid', 'phase8/validate.py', False,
     'every structural rule the theme holds itself to'),
    ('Structure & Liquid', 'phase16/refs.py', False,
     'every asset, snippet, section, translation key and internal link resolves'),
    ('Structure & Liquid', 'phase15/hygiene.py', False,
     'no stale or orphaned code'),
    ('Structure & Liquid', 'phase14/cartdoc.py', False,
     'the cart contract, documented and asserted'),
    ('Structure & Liquid', 'phase15/accounts.py', False,
     'customer accounts: the new-accounts posture'),
    ('Structure & Liquid', 'phase15/negctl.py', False,
     'negative control — seeds violations and proves the guards catch them'),
    ('Structure & Liquid', 'phase16/seo.py', False,
     'metadata, structured data, canonical, headings'),
    ('Structure & Liquid', 'phase16/images.py', False,
     'image handling, sizes, alt text paths'),

    ('Analytics & safety', 'phase17/tracking.py', False,
     'confirms NO tracking ships, and nothing leaks'),
    ('Analytics & safety', 'phase17/negctl.py', False,
     'negative control for the tracking guards'),
    ('Analytics & safety', 'phase17/escaping.py', False,
     'every untrusted value is escaped (this caught a live stored-XSS)'),
    ('Analytics & safety', 'phase17/funnel.py', False,
     'the purchase path still emits what an integration would bind to'),

    ('Layout & design', 'phase9/layout.py', True, 'page frames and section geometry'),
    ('Layout & design', 'phase9/surfaces.py', True, 'the dark/light surface model'),
    ('Layout & design', 'phase9/catalog.py', True, 'collection and card layout'),
    ('Layout & design', 'phase9/cardcascade.py', True, 'the product-card cascade'),
    ('Layout & design', 'phase9/facets.py', True, 'filter UI, row and drawer'),
    ('Layout & design', 'phase9/settings.py', True, 'merchant settings drive what they claim'),
    ('Layout & design', 'phase9/editor.py', True, 'Theme Editor section lifecycle'),
    ('Layout & design', 'phase9/respond.py', True, 'every breakpoint, overflow and target size'),
    ('Layout & design', 'phase8/contrast8.py', True, 'WCAG contrast, measured per role'),

    ('Behaviour', 'phase8/interact.py', True, 'cart drawer interactions'),
    ('Behaviour', 'phase8/interact_cartpage.py', True, 'cart page interactions'),
    ('Behaviour', 'phase8/interact_product.py', True, 'product page interactions'),
    ('Behaviour', 'phase14/cartqa.py', True, 'cart failure and recovery states'),
    ('Behaviour', 'phase14/notes.py', True, 'the order note'),
    ('Behaviour', 'phase14/lifecycle.py', True, 'drawer open/close/focus lifecycle'),
    ('Behaviour', 'phase16/facetsgate.py', True, 'the desktop filter-drawer gate (a P0 once)'),
    ('Behaviour', 'phase8/console.py', True, 'no console errors on any page'),

    ('Verse feature', 'phase19/verse.py', True, 'the three Verse bands render, filter and fit a phone'),
    ('Phase 18 guards', 'phase18/successblock.py', True, 'the add-to-cart confirmation hides, and View cart is a button'),
    ('Phase 18 guards', 'phase18/buybutton.py', True, 'Buy it now is a red box, wallet buttons untouched'),
    ('Phase 18 guards', 'phase18/chevron.py', True, 'all disclosures point the same way'),
    ('Phase 18 guards', 'phase18/hovergate.py', False, 'every hover rule is pointer-scoped'),
    ('Phase 18 guards', 'phase18/drawerexit.py', True, 'the filter drawer exit animation'),
]

SERVERS = [(8808, 'phase8/site'), (8809, 'phase9/site')]

# EVERY BROWSER SUITE READS GS_BROWSER, AND THE DEFAULT STOPPED WORKING.
#
# All the probes shell out to a Chromium binary with --dump-dom and parse the
# returned HTML. On 2026-09-26 Edge began returning ZERO BYTES with exit code 0
# — it launches, builds its profile, and emits nothing. Fourteen of the suites
# here went NO READING as a result, which reads exactly like a broken theme and
# is not one.
#
# So the browser is chosen by TESTING it rather than by assuming. Each candidate
# is asked to dump a page that is known to be served; the first one that returns
# real HTML wins and is passed to every suite through GS_BROWSER.
BROWSERS = [
    (os.environ.get('GS_BROWSER'), 'GS_BROWSER (already set)'),
    (r"C:\Program Files\Google\Chrome\Application\chrome.exe", 'Chrome'),
    (r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", 'Edge'),
    (r"C:\Program Files\Microsoft\Edge\Application\msedge.exe", 'Edge (64-bit)'),
    (r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe", 'Brave'),
]


def working_browser(probe_url):
    """The first candidate whose --dump-dom actually returns HTML."""
    for path, label in BROWSERS:
        if not path or not os.path.exists(path):
            continue
        prof = os.path.join(HERE, '_browserprobe')
        subprocess.call(['cmd', '/c', 'rmdir', '/s', '/q', prof],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        out = os.path.join(HERE, '_browserprobe.html')
        try:
            subprocess.call([path, '--headless=new', '--disable-gpu', '--no-first-run',
                             '--no-default-browser-check', '--user-data-dir=' + prof,
                             '--virtual-time-budget=15000', '--dump-dom', probe_url],
                            stdout=io.open(out, 'wb'), stderr=subprocess.DEVNULL,
                            timeout=60)
            n = os.path.getsize(out)
        except Exception:
            n = 0
        if n > 2000:
            return path, label, n
    return None, None, 0
OK = re.compile(r'OVERALL:\s*(PASS|NO TRACKING PRESENT)|(\d+) assertions?, 0 failed|'
                r'0 hard problems|0 finding\(s\)|(\d+) measurements?, \3 pass|'
                r'0 errors|(\d+) of \4 caught')
NOREAD = re.compile(r'NO READING|no payload|\*\*\* no ', re.I)


def run(cmd, cwd=None, timeout=600):
    try:
        p = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=timeout)
        return p.returncode, p.stdout.decode('utf-8', 'replace')
    except subprocess.TimeoutExpired:
        return -1, '*** TIMED OUT ***'


ZERO = re.compile(r'0 assertions|0 measurements|conventions in the theme: 0|'
                  r'0 checks|0 of 0')


def verdict(out):
    """PASS / FAIL / NO READING, from the suite's own last lines."""
    tail = '\n'.join(out.strip().split('\n')[-6:])

    # EXPLICIT NUMERIC VERDICTS FIRST, AND THE ORDER MATTERS.
    #
    # console.py's summary reads "pages with console errors or no reading:
    # 0 of 22" — a clean pass whose LABEL contains the words "no reading".
    # Matching the no-read phrase before reading the number reported that pass
    # as a suite that never ran. A detector that cannot tell a result from the
    # word for a missing result is worse than no detector.
    #
    # A suite that measured ZERO of anything has not passed either: it did not
    # run. That is a NO-READ, not a green tick.
    m = re.search(r'pages with console errors[^:]*:\s*(\d+)\s+of\s+(\d+)', tail)
    if m:
        return 'NOREAD' if m.group(2) == '0' else ('PASS' if m.group(1) == '0' else 'FAIL')
    m = re.search(r'(\d+) assertions?, (\d+) failed', tail)
    if m:
        return 'NOREAD' if m.group(1) == '0' else ('PASS' if m.group(2) == '0' else 'FAIL')
    m = re.search(r'(\d+) measurements?, (\d+) pass, (\d+) fail', tail)
    if m:
        return 'NOREAD' if m.group(1) == '0' else ('PASS' if m.group(3) == '0' else 'FAIL')
    m = re.search(r'(\d+) checks?, (\d+) passed, (\d+) failed', tail)
    if m:
        return 'NOREAD' if m.group(1) == '0' else ('PASS' if m.group(3) == '0' else 'FAIL')
    m = re.search(r'hard problems[^:]*:\s*(\d+)', tail)
    if m:
        return 'PASS' if m.group(1) == '0' else 'FAIL'
    if re.search(r'(\d+) violations seeded, \1 (fully )?caught', tail):
        return 'PASS'

    # Only now the phrase-based fallbacks.
    if NOREAD.search(tail) or ZERO.search(tail):
        return 'NOREAD'
    if 'OVERALL: PASS' in tail or 'NO TRACKING PRESENT' in tail:
        return 'PASS'
    if 'OVERALL:' in tail:
        return 'FAIL'
    return 'UNKNOWN'


def headline(out):
    for line in reversed(out.strip().split('\n')):
        s = line.strip()
        if s and not s.startswith('OVERALL') and any(c.isdigit() for c in s):
            return s[:64]
    return ''


if __name__ == '__main__':
    if '--list' in sys.argv:
        g = None
        for grp, script, br, desc in SUITES:
            if grp != g:
                g = grp
                print('\n%s' % grp.upper())
            print('  %-28s %s%s' % (script, desc, '  [browser]' if br else ''))
        raise SystemExit(0)

    fast = '--fast' in sys.argv
    t0 = time.time()
    print('=' * 78)
    print('GOD SQUAD — FULL CHECK')
    print('theme: %s' % THEME)
    print('=' * 78)

    # ---------------------------------------------------------- 1. rebuild
    print()
    print('[1/4] Rebuilding the harness from the theme on disk ...')
    # phase9/build.py MUST run before phase9/home.py. It writes the collection,
    # search, product, cart and 404 fixtures; home.py writes only the homepage
    # variants on top of them. The scratchpad hid this for the whole project:
    # every phase had run build.py at some point and its output persisted, so a
    # runner that skipped it still found a full site. A fresh checkout does not,
    # and the symptom was nineteen suites quietly measuring an empty directory.
    # phase9/surfacepages.py writes the collection, search, page and 404
    # fixtures, and must run after build.py. Between the three phase9 scripts a
    # cold checkout gets 34 of the 38 pages the long-lived scratchpad had
    # accumulated; the other four are hero-variant and iframe-wrapper demos from
    # Phase 5 whose producer was never a build script, and no suite reads them.
    for b in ('phase8/build.py', 'phase9/build.py', 'phase9/surfacepages.py',
              'phase9/home.py'):
        d, f = b.split('/')
        rc, out = run([sys.executable, f], cwd=os.path.join(HERE, d), timeout=300)
        print('      %-18s %s' % (b, 'ok' if rc == 0 else '*** FAILED ***'))
        if rc != 0:
            print(out[-600:])

    # ---------------------------------------------------------- 2. servers
    procs = []
    if not fast:
        print()
        print('[2/4] Starting harness servers ...')
        for port, rel in SERVERS:
            site = os.path.join(HERE, rel.replace('/', os.sep))
            p = subprocess.Popen([sys.executable, '-m', 'http.server', str(port)],
                                 cwd=site, stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
            procs.append(p)
            print('      port %d  <- %s' % (port, rel))
        time.sleep(2.5)

        path, label, n = working_browser('http://127.0.0.1:8809/home.html')
        if path:
            os.environ['GS_BROWSER'] = path
            print('      browser: %s  (%s, dumped %d bytes)' % (label, path, n))
        else:
            print('      *** NO WORKING BROWSER. Every browser suite will report')
            print('          NO READING. Tried: %s'
                  % ', '.join(l for p, l in BROWSERS if p and os.path.exists(p)))
    else:
        print()
        print('[2/4] --fast: skipping servers and every browser suite.')

    # ---------------------------------------------------------- 3. suites
    print()
    print('[3/4] Running suites ...')
    print()
    results, group = [], None
    try:
        for grp, script, needs_browser, desc in SUITES:
            if fast and needs_browser:
                continue
            if grp != group:
                group = grp
                print('  %s' % grp.upper())
            d, f = script.split('/')
            rc, out = run([sys.executable, f], cwd=os.path.join(HERE, d))
            v = verdict(out)
            results.append((grp, script, v, headline(out), out))
            mark = {'PASS': 'PASS  ', 'FAIL': '*FAIL*', 'NOREAD': 'NO-READ',
                    'UNKNOWN': '  ?   '}[v]
            print('    %-7s %-28s %s' % (mark, f.replace('.py', ''), headline(out)))
    finally:
        for p in procs:
            p.terminate()

    # ---------------------------------------------------------- 4. theme check
    print()
    print('[4/4] Theme Check ...')
    tc = os.path.join(HERE, 'node_modules', '@shopify', 'theme-check-node')
    if os.path.isdir(tc):
        js = ("const{themeCheckRun}=require('./node_modules/@shopify/theme-check-node');"
              "themeCheckRun(String.raw`%s`).then(r=>{const o=r.offenses||[];"
              "console.log(JSON.stringify(o.map(x=>({c:x.check,m:x.message}))));});" % THEME)
        rc, out = run(['node', '-e', js], cwd=HERE, timeout=300)
        m = re.search(r'\[.*\]', out, re.S)
        offences = json.loads(m.group(0)) if m else []
        print('      %d offence(s)' % len(offences))
        for o in offences:
            print('        %s: %s' % (o['c'], o['m']))
    else:
        offences = None
        print('      *** theme-check-node not installed in %s' % HERE)

    # ---------------------------------------------------------- report
    npass = sum(1 for r in results if r[2] == 'PASS')
    nfail = sum(1 for r in results if r[2] == 'FAIL')
    nread = sum(1 for r in results if r[2] == 'NOREAD')
    nunk = sum(1 for r in results if r[2] == 'UNKNOWN')

    print()
    print('=' * 78)
    print('RESULT   %d passed   %d failed   %d could not be read   %d unclear'
          % (npass, nfail, nread, nunk))
    print('         Theme Check: %s'
          % ('not run' if offences is None else '%d offence(s)' % len(offences)))
    print('         %.0f seconds' % (time.time() - t0))
    print('=' * 78)

    if nfail:
        print()
        print('FAILURES — the output of each, last 20 lines:')
        for grp, script, v, head, out in results:
            if v == 'FAIL':
                print()
                print('--- %s ---' % script)
                print('\n'.join(out.strip().split('\n')[-20:]))

    if nread:
        print()
        print('COULD NOT BE READ (%d) — these have NOT passed:' % nread)
        for grp, script, v, head, out in results:
            if v == 'NOREAD':
                print('  %s' % script)
        print()
        print('  A browser suite reports this when its probe returns nothing.')
        print('  Usual causes, in order: the harness servers are not up (this')
        print('  script starts them, so that is unlikely here); too many stale')
        print('  msedge processes; or a corrupt edge-* profile directory. Kill')
        print('  every msedge process and delete the edge-* directories under')
        print('  this folder, then run again.')

    print()
    print('WHAT THIS RUN DID NOT CHECK, and could not:')
    print('  - the purchase flow (add to cart, checkout) — Shopify\'s, not the theme\'s')
    print('  - real products, real copy, real photography — every fixture is invented')
    print('  - Section Rendering API, content_for_header, the image CDN, live Theme Check')
    print('  See GODSQUAD-THEME-REFERENCE-MANUAL.md section 10 for the store runbook.')

    raise SystemExit(1 if (nfail or nunk) else 0)
