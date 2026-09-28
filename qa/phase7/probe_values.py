import tempfile
# -*- coding: utf-8 -*-
"""How the values row wraps, at every block count that fits in the schema.

The review's claim was that a 14rem floor fits five tracks at the container
width, so the sixth permitted block lands alone on a second row. This measures
the rows rather than arguing about the arithmetic: it reads each tile's top
edge and groups the tiles that share one.

A fresh browser profile each run — the earlier probe reported five tracks after
the floor had already changed to 17rem, which was a cached stylesheet.
"""
import os, re, json, shutil, subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 8807
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-values')
PAGE = """<!doctype html><meta charset="utf-8"><title>v</title>
<style>html,body{margin:0}iframe{border:0;display:block}</style>
<iframe id="f" src="SRC" width="WIDTH" height="1600"></iframe>
<pre id="o"></pre>
<script>
document.getElementById('f').onload=function(){
  var d=this.contentDocument, w=this.contentWindow;
  var g=d.querySelector('.our-story__value-list');
  var items=[].slice.call(d.querySelectorAll('.our-story__value'));
  var rows={};
  items.forEach(function(el){
    var r=el.getBoundingClientRect();
    var k=Math.round(r.top);
    (rows[k]=rows[k]||[]).push(Math.round(r.width));
  });
  var tracks=w.getComputedStyle(g).gridTemplateColumns.split(' ').filter(Boolean);
  document.getElementById('o').textContent='<<<'+JSON.stringify({
    tracks:tracks, rows:Object.keys(rows).sort(function(a,b){return a-b;})
      .map(function(k){return rows[k];})})+'>>>';
};
</script>"""

shutil.rmtree(PROFILE, ignore_errors=True)
site = os.path.join(HERE, 'site')

print('%-22s %-6s %-34s %s' % ('page', 'width', 'tracks', 'rows (tile widths)'))
for page in ('case-values6.html', 'case-story.html'):
    for width in (1024, 1280, 1440, 1920):
        # A unique name per reading. http.server answers If-Modified-Since with
        # one-second granularity, so rewriting one filename inside the same
        # second hands the browser a 304 and the PREVIOUS page's geometry.
        name = 'probe-values-%s-%d.html' % (page.split('.')[0], width)
        open(os.path.join(site, name), 'w', encoding='utf-8').write(
            PAGE.replace('SRC', page).replace('WIDTH', str(width)))
        out = os.path.join(HERE, 'values-dom.html')
        subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run',
                        '--no-default-browser-check', '--user-data-dir=' + PROFILE,
                        '--virtual-time-budget=25000',
                        '--window-size=%d,1700' % (width + 60), '--dump-dom',
                        'http://127.0.0.1:%d/%s' % (PORT, name)],
                       stdout=open(out, 'w', encoding='utf-8'), stderr=subprocess.DEVNULL)
        d = open(out, encoding='utf-8', errors='replace').read()
        m = re.search(r'<pre id="o">&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>', d, re.S)
        if not m:
            print('%-22s %-6s NO READING' % (page, width))
            continue
        j = json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&'))
        print('%-22s %-6s %-34s %s' % (page, width, ' '.join(j['tracks']),
                                       ' | '.join(str(r) for r in j['rows'])))
