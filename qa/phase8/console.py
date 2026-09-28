import tempfile
# -*- coding: utf-8 -*-
"""Load every harness page in a real browser and report console errors.

The first thing this catches is a JavaScript syntax error, which no amount of
reading the file finds reliably. It also catches a Liquid-rendered attribute
that the browser rejects, and any exception thrown while the two scripts
initialise.
"""
import os, re, json, shutil, subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = os.environ.get('GS_BROWSER') or r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 8808
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-console')
SITE = os.path.join(HERE, 'site')

HARNESS = """<!doctype html><meta charset="utf-8"><title>c</title>
<body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var errors = [];
window.addEventListener('error', function (e) {
  errors.push('ERROR ' + (e.message || '') + ' @ ' + (e.filename || '') + ':' + (e.lineno || ''));
}, true);
window.addEventListener('unhandledrejection', function (e) {
  errors.push('REJECT ' + (e.reason && e.reason.message ? e.reason.message : String(e.reason)));
});
var origError = console.error, origWarn = console.warn;
console.error = function () { errors.push('console.error: ' + [].join.call(arguments, ' ')); origError.apply(console, arguments); };
console.warn = function () { errors.push('console.warn: ' + [].join.call(arguments, ' ')); origWarn.apply(console, arguments); };

var f = document.createElement('iframe');
f.style.cssText = 'width:1440px;height:1000px;border:0;position:absolute;left:-9999px';
f.src = 'PAGE';
f.onload = function () {
  var w = f.contentWindow, d = f.contentDocument;
  w.addEventListener('error', function (e) {
    errors.push('IFRAME ERROR ' + (e.message || '') + ' @ ' + (e.filename || '') + ':' + (e.lineno || ''));
  }, true);
  w.setTimeout(function () {
    var report = {
      errors: errors,
      cartJs: typeof w.GodSquad === 'object' && !!(w.GodSquad && w.GodSquad.cart),
      drawer: !!d.querySelector('[data-cart-drawer]'),
      status: !!d.getElementById('CartStatus'),
      productBound: (function () {
        var p = d.querySelector('[data-main-product]');
        return p ? p.dataset.gsProductBound === 'true' : null;
      })(),
      variantData: (function () {
        var el = d.querySelector('[data-variant-data]');
        if (!el) return null;
        try { return JSON.parse(el.textContent).length; } catch (e) { return 'INVALID JSON: ' + e.message; }
      })(),
      ldJson: (function () {
        var out = [];
        [].forEach.call(d.querySelectorAll('script[type="application/ld+json"]'), function (s) {
          try { JSON.parse(s.textContent); out.push('ok'); } catch (e) { out.push('INVALID: ' + e.message); }
        });
        return out;
      })()
    };
    document.getElementById('o').textContent = '<<<' + JSON.stringify(report) + '>>>';
    document.title = 'DONE';
  }, 900);
};
document.body.appendChild(f);
</script>
"""

shutil.rmtree(PROFILE, ignore_errors=True)
pages = sorted(f for f in os.listdir(SITE) if f.endswith('.html') and not f.startswith('_'))

print('%-22s %-6s %-5s %-6s %-7s %-9s %s' %
      ('page', 'cart', 'drwr', 'status', 'variants', 'json-ld', 'console'))
bad = 0
for i, page in enumerate(pages):
    name = '_console-%d.html' % i
    open(os.path.join(SITE, name), 'w', encoding='utf-8').write(HARNESS.replace('PAGE', page))
    out = os.path.join(HERE, 'console-dom.html')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run',
                    '--no-default-browser-check', '--user-data-dir=' + PROFILE,
                    '--virtual-time-budget=20000', '--window-size=1600,1100', '--dump-dom',
                    'http://127.0.0.1:%d/%s' % (PORT, name)],
                   stdout=open(out, 'w', encoding='utf-8'), stderr=subprocess.DEVNULL)
    d = open(out, encoding='utf-8', errors='replace').read()
    m = re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>', d, re.S)
    if not m:
        print('%-22s NO READING' % page)
        bad += 1
        continue
    r = json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')
                   .replace('&lt;', '<').replace('&gt;', '>'))
    errs = r['errors']
    if errs:
        bad += 1
    print('%-22s %-6s %-5s %-6s %-8s %-9s %s' %
          (page, r['cartJs'], r['drawer'], r['status'],
           r['variantData'], ','.join(r['ldJson']) or '-',
           ('; '.join(errs)[:90] if errs else 'clean')))

for f in os.listdir(SITE):
    if f.startswith('_console-'):
        os.remove(os.path.join(SITE, f))
print()
print('pages with console errors or no reading: %d of %d' % (bad, len(pages)))
