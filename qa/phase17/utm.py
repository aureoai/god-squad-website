# -*- coding: utf-8 -*-
"""Phase 17 — do the theme's GET forms discard campaign parameters?

THE CLAIM UNDER TEST, from the theme's own comment at
sections/main-collection.liquid:34 —

    "A GET form does not append to its action's query string. The browser
     discards whatever query the action URL carries and rebuilds it from the
     form's own fields."

Phase 13 relied on that to drop the `page` parameter deliberately. The same
mechanism would drop utm_source, utm_medium and utm_campaign. The theme has two
GET forms a customer can submit while a campaign parameter is in the URL: the
collection sort/filter form, and the header search form.

This does not read the code. It loads the page with campaign parameters in the
URL, submits the form the way a customer would, and reads the URL that results.
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
SITE = os.path.abspath(os.path.join(HERE, '..', 'phase9', 'site'))
EDGE = os.environ.get('GS_BROWSER',
                      r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-utm')
PORT = 8809

CAMPAIGN = 'utm_source=facebook&utm_medium=paid_social&utm_campaign=drop_01'

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var CASES = CASELIST, res = {}, i = 0;
function step() {
  if (i >= CASES.length) {
    document.title = 'DONE';
    document.getElementById('o').textContent = '<<<' + JSON.stringify(res) + '>>>';
    return;
  }
  var c = CASES[i];
  var f = document.createElement('iframe');
  f.style.cssText = 'border:0;width:1440px;height:900px';
  f.src = c.url;
  document.body.appendChild(f);
  var submitted = false;
  f.onload = function () {
    var d = f.contentDocument;
    if (!submitted) {
      submitted = true;
      var form = d.querySelector(c.form);
      if (!form) {
        res[c.name] = { error: 'form not found: ' + c.form };
        f.remove(); i++; step(); return;
      }
      /* What the customer does: change the control and submit. requestSubmit()
         runs validation and fires submit exactly as a real interaction does. */
      if (c.set) {
        var el = d.querySelector(c.set.sel);
        if (el) { el.value = c.set.value; }
      }
      res[c.name] = { before: f.contentWindow.location.search };
      try { form.requestSubmit ? form.requestSubmit() : form.submit(); }
      catch (e) { res[c.name].error = String(e); f.remove(); i++; step(); return; }
      setTimeout(function () {
        /* The iframe has navigated; read where it landed. */
        try { res[c.name].after = f.contentWindow.location.search; }
        catch (e) { res[c.name].after = 'unreadable: ' + e; }
        f.remove(); i++; step();
      }, 700);
    }
  };
}
step();
</script>
"""

CASES = [
    {'name': 'collection sort',
     'url': 's-collection.html?' + CAMPAIGN,
     'form': 'form[data-collection-sort]',
     'set': {'sel': 'select[name="sort_by"]', 'value': 'price-ascending'}},
    {'name': 'collection filter',
     'url': 's-collection-filters.html?' + CAMPAIGN,
     'form': 'form[data-collection-sort]',
     'set': None},
    {'name': 'header search',
     'url': 's-collection.html?' + CAMPAIGN,
     'form': 'form[role="search"]',
     'set': {'sel': 'input[name="q"]', 'value': 'tee'}},
]

FAILURES = []
CHECKS = [0]


def check(label, ok, detail=''):
    CHECKS[0] += 1
    print('  %-58s %s %s' % (label, 'OK  ' if ok else '*** LOST ***',
                             '' if ok else str(detail)[:120]))
    if not ok:
        FAILURES.append(label)


if __name__ == '__main__':
    shutil.rmtree(PROFILE, ignore_errors=True)
    src = PROBE.replace('CASELIST', json.dumps(CASES))
    io.open(os.path.join(SITE, '_utm.html'), 'w', encoding='utf-8').write(src)
    out = os.path.join(HERE, 'utm-dom.html')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run',
                    '--no-default-browser-check', '--user-data-dir=' + PROFILE,
                    '--virtual-time-budget=30000', '--window-size=1600,1100', '--dump-dom',
                    'http://127.0.0.1:%d/_utm.html' % PORT],
                   stdout=io.open(out, 'w', encoding='utf-8'), stderr=subprocess.DEVNULL)
    d = io.open(out, encoding='utf-8', errors='replace').read()
    m = re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>', d, re.S)
    if not m:
        print('NO READING')
        print(d[-900:])
        raise SystemExit(1)
    data = json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')
                      .replace('&lt;', '<').replace('&gt;', '>'))

    print('=== WHAT SUBMITTING EACH GET FORM DOES TO THE QUERY STRING ===')
    print()
    for name, r in data.items():
        print('  %s' % name)
        print('    before: %s' % (r.get('before') or '(none)'))
        print('    after : %s' % (r.get('after') or r.get('error') or '(none)'))
        print()

    for name, r in data.items():
        after = r.get('after') or ''
        check('%-18s keeps utm_source' % name, 'utm_source' in after, after[:90])
        check('%-18s keeps utm_campaign' % name, 'utm_campaign' in after, after[:90])

    print()
    print('%d checks, %d kept, %d dropped'
          % (CHECKS[0], CHECKS[0] - len(FAILURES), len(FAILURES)))
    print('OVERALL: %s' % ('CAMPAIGN PARAMETERS SURVIVE'
                           if not FAILURES else '*** CAMPAIGN PARAMETERS ARE DROPPED ***'))
