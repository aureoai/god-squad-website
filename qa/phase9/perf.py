import tempfile
# -*- coding: utf-8 -*-
"""What the page costs on a phone.

DOM node count, tree depth, the number of stylesheet and script requests, and
the bytes of CSS and JS the theme ships. Measured at 375 through the iframe,
the same way every other Phase 9 reading is taken.
"""
import os, re, json, shutil, subprocess, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT, SITE = 8809, os.path.join(HERE, 'site')
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-perf')
PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var PAGES = PAGELIST, res = {}, i = 0;
function step() {
  if (i >= PAGES.length) {
    document.getElementById('o').textContent = '<<<' + JSON.stringify(res) + '>>>';
    document.title = 'DONE'; return;
  }
  var p = PAGES[i++];
  var f = document.createElement('iframe');
  f.style.cssText = 'width:375px;height:812px;border:0;position:absolute;left:-9999px;top:0';
  f.src = p;
  f.onload = function () {
    var d = f.contentDocument, win = f.contentWindow;
    win.setTimeout(function () {
      var all = d.querySelectorAll('*'), depth = 0;
      all.forEach(function (e) { var n = 0, q = e; while (q) { n++; q = q.parentElement; } if (n > depth) depth = n; });
      var imgs = [].slice.call(d.querySelectorAll('img'));
      res[p] = {
        nodes: all.length,
        depth: depth,
        css: d.querySelectorAll('link[rel=stylesheet]').length,
        js: d.querySelectorAll('script[src]').length,
        imgs: imgs.length,
        lazy: imgs.filter(function (m) { return m.getAttribute('loading') === 'lazy'; }).length,
        eager: imgs.filter(function (m) { return m.getAttribute('loading') !== 'lazy'; })
                   .map(function (m) { return (m.className || m.tagName) + ':' + (m.getAttribute('fetchpriority') || '-'); }),
        noSrcset: imgs.filter(function (m) { return !m.getAttribute('srcset'); }).length,
        noDims: imgs.filter(function (m) { return !m.getAttribute('width') || !m.getAttribute('height'); }).length,
        inlineStyleTags: d.querySelectorAll('style').length
      };
      f.remove(); step();
    }, 220);
  };
  document.body.appendChild(f);
}
step();
</script>
"""

pages = ['home.html', 'p-sizes.html', 'c-page-many.html']
open(os.path.join(SITE, '_perf.html'), 'w', encoding='utf-8').write(
    PROBE.replace('PAGELIST', json.dumps(pages)))
shutil.rmtree(PROFILE, ignore_errors=True)
out = os.path.join(HERE, 'perf-dom.html')
subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run',
                '--no-default-browser-check', '--user-data-dir=' + PROFILE,
                '--virtual-time-budget=60000', '--window-size=1400,1000', '--dump-dom',
                'http://127.0.0.1:%d/_perf.html' % PORT],
               stdout=open(out, 'w', encoding='utf-8'), stderr=subprocess.DEVNULL)
d = open(out, encoding='utf-8', errors='replace').read()
m = re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>', d, re.S)
if not m:
    print('NO READING'); raise SystemExit(1)
data = json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')
                  .replace('&lt;', '<').replace('&gt;', '>'))
print('%-18s %6s %6s %4s %4s %5s %5s %7s %7s %6s' %
      ('page @375', 'nodes', 'depth', 'css', 'js', 'imgs', 'lazy', 'noSrcst', 'noDims', 'style'))
for k, r in data.items():
    print('%-18s %6d %6d %4d %4d %5d %5d %7d %7d %6d' %
          (k, r['nodes'], r['depth'], r['css'], r['js'], r['imgs'], r['lazy'],
           r['noSrcset'], r['noDims'], r['inlineStyleTags']))
    print('    not lazy: %s' % ', '.join(r['eager']))
