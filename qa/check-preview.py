# -*- coding: utf-8 -*-
"""Find every error in preview-site/ — console, assets, markup, content.

    python check-preview.py

Loads all eighteen preview pages in a real browser and reports what is wrong,
grouped by severity. This is not the theme suite: check-all.py proves the THEME
is correct, and this proves the PREVIEW BUILD of it is correct. They fail in
different ways — a preview can be broken by the link rewriting, a missing asset,
or a fixture that was never generated, none of which the theme suite can see.

WHAT IT LOOKS FOR

  BROKEN      a JavaScript error, an asset that 404s, an image that does not
              decode, a link to a page that does not exist
  WRONG       Liquid that was never rendered ({{ }} or {% %} left in the output),
              "undefined"/"NaN" leaking into visible text, a duplicate id
  SUSPECT     an empty href or src, a missing alt, a page with no h1 or no
              title, horizontal overflow

Every finding names the page and the element, because "there are errors" is not
something anyone can act on.
"""
import io
import json
import os
import re
import subprocess
import sys
import time
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
QA = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(QA)
SITE = os.path.join(PROJECT, 'preview-site')
PORT = 8177

BROWSERS = [
    os.environ.get('GS_BROWSER'),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
]

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var PAGE = 'PAGEHERE', FILES = FILELIST, out = {page: PAGE, errors: [], findings: []};
function add(sev, kind, detail) { out.findings.push({sev: sev, kind: kind, detail: detail}); }

var f = document.createElement('iframe');
f.style.cssText = 'border:0;width:1280px;height:900px';
document.body.appendChild(f);

/* Attach before navigation so early throws are caught. */
f.src = PAGE;
try {
  var w0 = f.contentWindow;
  w0.addEventListener('error', function (e) {
    out.errors.push('error: ' + (e.message || e.type) + ' @ ' + (e.filename || '?') + ':' + (e.lineno || 0));
  }, true);
  w0.addEventListener('unhandledrejection', function (e) {
    out.errors.push('unhandledrejection: ' + (e.reason && e.reason.message || e.reason));
  });
} catch (e) {}

f.onload = function () {
  var d = f.contentDocument, w = f.contentWindow;

  try {
    var oe = w.console.error, ow = w.console.warn;
    w.console.error = function () { out.errors.push('console.error: ' + [].join.call(arguments, ' ')); oe.apply(w.console, arguments); };
    w.console.warn = function () { out.errors.push('console.warn: ' + [].join.call(arguments, ' ')); ow.apply(w.console, arguments); };
  } catch (e) {}

  setTimeout(function () {
    /* ---------------------------------------------- assets that failed */
    try {
      w.performance.getEntriesByType('resource').forEach(function (r) {
        if (r.transferSize === 0 && r.decodedBodySize === 0 && r.duration === 0) {
          add('BROKEN', 'resource-failed', r.name.split('/').slice(-1)[0]);
        }
      });
    } catch (e) {}

    Array.prototype.forEach.call(d.querySelectorAll('img'), function (i) {
      var src = i.getAttribute('src') || '(no src)';
      if (!i.getAttribute('src')) { add('SUSPECT', 'img-no-src', i.className || i.tagName); return; }
      if (i.complete && i.naturalWidth === 0) add('BROKEN', 'img-broken', src);
      if (!i.hasAttribute('alt')) add('SUSPECT', 'img-no-alt', src);
    });

    /* ---------------------------------------------- unrendered Liquid */
    var html = d.documentElement.innerHTML;
    var liq = html.match(/\{\{[^}]{0,60}\}\}|\{%[^%]{0,60}%\}/g);
    if (liq) {
      var uniq = {};
      liq.forEach(function (x) { uniq[x] = 1; });
      Object.keys(uniq).slice(0, 6).forEach(function (x) {
        add('WRONG', 'liquid-not-rendered', x.replace(/\s+/g, ' ').slice(0, 60));
      });
    }

    /* ---------------------------------------------- junk in visible text */
    var body = d.body.innerText || '';
    ['undefined', 'NaN', 'null', '[object Object]', 'translation missing'].forEach(function (bad) {
      var re = new RegExp(bad.replace(/[.[\]]/g, '\\$&'), 'i');
      if (re.test(body)) {
        var m = body.match(new RegExp('.{0,30}' + bad.replace(/[.[\]]/g, '\\$&') + '.{0,30}', 'i'));
        add('WRONG', 'junk-in-text', (m ? m[0] : bad).replace(/\s+/g, ' '));
      }
    });

    /* ---------------------------------------------- duplicate ids */
    var seen = {}, dupes = {};
    Array.prototype.forEach.call(d.querySelectorAll('[id]'), function (el) {
      var id = el.id;
      if (!id) return;
      if (seen[id]) dupes[id] = 1; else seen[id] = 1;
    });
    Object.keys(dupes).slice(0, 8).forEach(function (id) { add('WRONG', 'duplicate-id', id); });

    /* ---------------------------------------------- links */
    Array.prototype.forEach.call(d.querySelectorAll('a'), function (a) {
      var h = a.getAttribute('href');
      if (h === null) { add('SUSPECT', 'anchor-no-href', (a.textContent || '').trim().slice(0, 24)); return; }
      if (h === '' ) { add('SUSPECT', 'anchor-empty-href', (a.textContent || '').trim().slice(0, 24)); return; }
      if (h.charAt(0) === '#' || /^(https?:|mailto:|tel:|data:)/.test(h)) return;
      var file = h.split('?')[0].split('#')[0];
      if (!file) return;
      if (FILES.indexOf(file) === -1 && file.indexOf('assets/') !== 0 && file.indexOf('img/') !== 0) {
        add('BROKEN', 'link-target-missing', h + '  (' + (a.textContent || '').trim().slice(0, 20) + ')');
      }
    });

    /* ---------------------------------------------- document basics */
    if (!d.querySelector('h1')) add('SUSPECT', 'no-h1', '');
    var t = (d.title || '').trim();
    if (!t) add('SUSPECT', 'no-title', '');
    else if (/harness|WAIT|untitled/i.test(t)) add('WRONG', 'placeholder-title', t);

    if (d.documentElement.scrollWidth > d.documentElement.clientWidth + 1) {
      add('BROKEN', 'horizontal-overflow',
          d.documentElement.scrollWidth + ' > ' + d.documentElement.clientWidth);
    }

    /* ---------------------------------------------- forms that go nowhere */
    Array.prototype.forEach.call(d.querySelectorAll('form'), function (fm) {
      var a = fm.getAttribute('action');
      if (a === '#' || a === '' || a === null) {
        add('SUSPECT', 'form-no-action', (fm.className || 'form').toString().split(' ')[0]);
      }
    });

    document.title = 'DONE';
    document.getElementById('o').textContent = '<<<' + JSON.stringify(out) + '>>>';
  }, 2200);
};
</script>
"""


def working_browser(url):
    for p in BROWSERS:
        if not p or not os.path.exists(p):
            continue
        prof = os.path.join(QA, '_pvprobe')
        out = os.path.join(QA, '_pvprobe.html')
        try:
            subprocess.call([p, '--headless=new', '--disable-gpu', '--no-first-run',
                             '--user-data-dir=' + prof, '--virtual-time-budget=12000',
                             '--dump-dom', url],
                            stdout=io.open(out, 'wb'), stderr=subprocess.DEVNULL, timeout=60)
            if os.path.getsize(out) > 2000:
                return p
        except Exception:
            pass
    return None


def run_page(browser, page, files):
    html = (PROBE.replace('PAGEHERE', page)
                 .replace('FILELIST', json.dumps(files)))
    probe = os.path.join(SITE, '_check.html')
    io.open(probe, 'w', encoding='utf-8').write(html)
    out = os.path.join(QA, '_pvout.html')
    try:
        subprocess.call([browser, '--headless=new', '--disable-gpu', '--no-first-run',
                         '--user-data-dir=' + os.path.join(QA, '_pvprobe'),
                         '--virtual-time-budget=20000', '--window-size=1280,900',
                         '--dump-dom', 'http://127.0.0.1:%d/_check.html' % PORT],
                        stdout=io.open(out, 'wb'), stderr=subprocess.DEVNULL, timeout=120)
        dom = io.open(out, encoding='utf-8', errors='replace').read()
        m = re.search(r'&lt;&lt;&lt;(.*?)&gt;&gt;&gt;', dom, re.S) or \
            re.search(r'<<<(.*?)>>>', dom, re.S)
        if not m:
            return None
        return json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')
                          .replace('&lt;', '<').replace('&gt;', '>'))
    finally:
        try:
            os.remove(probe)
        except OSError:
            pass


if __name__ == '__main__':
    if not os.path.isdir(SITE):
        raise SystemExit('preview-site/ does not exist. Run: python build-preview.py')

    pages = sorted(f for f in os.listdir(SITE)
                   if f.endswith('.html') and not f.startswith('_'))
    files = list(pages)
    print('=' * 74)
    print('PREVIEW-SITE CHECK — %d pages' % len(pages))
    print('=' * 74)

    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)],
                           cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    try:
        browser = working_browser('http://127.0.0.1:%d/%s' % (PORT, pages[0]))
        if not browser:
            raise SystemExit('no working browser found')
        print('browser: %s' % browser)
        print()

        by_sev = defaultdict(list)
        noread = []
        for p in pages:
            r = run_page(browser, p, files)
            if r is None:
                noread.append(p)
                print('  %-26s NO READING' % p)
                continue
            n = len(r['findings']) + len(r['errors'])
            print('  %-26s %s' % (p, 'clean' if n == 0 else '%d issue(s)' % n))
            for e in r['errors']:
                by_sev['BROKEN'].append((p, 'js-error', e[:90]))
            for f in r['findings']:
                by_sev[f['sev']].append((p, f['kind'], f['detail']))
    finally:
        srv.terminate()

    print()
    total = sum(len(v) for v in by_sev.values())
    for sev in ('BROKEN', 'WRONG', 'SUSPECT'):
        rows = by_sev.get(sev, [])
        if not rows:
            continue
        print('=' * 74)
        print('%s — %d' % (sev, len(rows)))
        print('=' * 74)
        grouped = defaultdict(list)
        for page, kind, detail in rows:
            grouped[(kind, detail)].append(page)
        for (kind, detail), pgs in sorted(grouped.items()):
            where = pgs[0] if len(pgs) == 1 else '%d pages' % len(pgs)
            print('  %-24s %-44s %s' % (kind, str(detail)[:44], where))
        print()

    print('=' * 74)
    print('%d finding(s) across %d page(s); %d page(s) unread'
          % (total, len(pages), len(noread)))
    print('=' * 74)
    raise SystemExit(1 if (by_sev.get('BROKEN') or by_sev.get('WRONG') or noread) else 0)
