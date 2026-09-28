# -*- coding: utf-8 -*-
"""Theme Editor lifecycle: what happens when a section is re-rendered or removed.

The Theme Editor is the only place a section is replaced while the page stays
alive, so it is the only place these failures appear. Nothing in the storefront
suites can see them.

The probe installs a counting shim on EventTarget.prototype before any theme
script runs, so it can measure the NET number of listeners bound to window and
document by type. Then it drives the real Shopify editor events —
shopify:section:load and shopify:section:unload — against the real markup and
the real scripts, and asserts on observable state:

  * does a re-render leave the page scroll-locked?
  * does the focus trap stay bound to a panel that is no longer in the document?
  * does each re-render add another scroll or matchMedia listener?

Every assertion here failed before Phase 11, except where noted.
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

EDGE = os.environ.get('GS_BROWSER') or r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 8809
SITE = os.path.join(HERE, 'site')
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-editor')
SHIM = """<script>
// Installed before any theme script. Counts NET listeners per (target, type) so
// a re-render that re-binds without releasing is visible as growth.
(function () {
  var counts = {};
  function key(t, ty) {
    return (t === window ? 'window' : t === document ? 'document' : 'other') + ':' + ty;
  }
  var addFn = EventTarget.prototype.addEventListener;
  var remFn = EventTarget.prototype.removeEventListener;
  EventTarget.prototype.addEventListener = function (ty, fn, o) {
    if (this === window || this === document) {
      var k = key(this, ty); counts[k] = (counts[k] || 0) + 1;
    }
    return addFn.call(this, ty, fn, o);
  };
  EventTarget.prototype.removeEventListener = function (ty, fn, o) {
    if (this === window || this === document) {
      var k = key(this, ty); counts[k] = (counts[k] || 0) - 1;
    }
    return remFn.call(this, ty, fn, o);
  };
  window.__counts = counts;
  // matchMedia listeners do not go through EventTarget in every engine.
  var mm = window.matchMedia;
  window.__mq = 0;
  window.matchMedia = function (q) {
    var list = mm.call(window, q);
    var a = list.addEventListener, r = list.removeEventListener;
    if (a) {
      list.addEventListener = function () { window.__mq++; return a.apply(list, arguments); };
      list.removeEventListener = function () { window.__mq--; return r.apply(list, arguments); };
    }
    return list;
  };
})();
</script>"""

PROBE = r"""<!doctype html><meta charset="utf-8"><title>WAIT</title><body style="margin:0">
<pre id="o" style="display:none"></pre>
<script>
var res = {}, f = document.createElement('iframe');
f.style.cssText = 'width:390px;height:844px;border:0;position:absolute;left:-9999px;top:0';
f.src = 'PAGE';
f.onload = function () {
  var d = f.contentDocument, w = f.contentWindow;
  var st = d.createElement('style');
  st.textContent = '*,*::before,*::after{transition:none!important;animation:none!important}';
  d.head.appendChild(st);

  function section() { return d.getElementById('shopify-section-header'); }
  function fire(name, target) {
    var ev = new w.CustomEvent(name, { bubbles: true });
    Object.defineProperty(ev, 'target', { value: target, enumerable: true });
    d.dispatchEvent(ev);
  }
  function counts() {
    return { scroll: (w.__counts['window:scroll'] || 0),
             keydown: (w.__counts['document:keydown'] || 0),
             mq: (w.__mq || 0) };
  }
  function locked() { return d.documentElement.classList.contains('menu-open'); }
  function openMenu() {
    var t = d.querySelector('[data-menu-toggle]');
    if (t) t.click();
  }

  w.setTimeout(function () {
    res.baseline = counts();
    res.lockedAtStart = locked();

    // 1. Open the menu, then re-render the section as the editor does.
    openMenu();
    res.lockedWhenOpen = locked();
    var sec = section();
    fire('shopify:section:unload', sec);
    fire('shopify:section:load', sec);
    res.lockedAfterRerenderWhileOpen = locked();
    res.afterOneRerender = counts();

    // 2. Re-render four more times and watch for listener growth.
    for (var i = 0; i < 4; i++) {
      fire('shopify:section:unload', section());
      fire('shopify:section:load', section());
    }
    res.afterFiveRerenders = counts();

    // 3. Open the menu, then REMOVE the section entirely.
    openMenu();
    res.lockedBeforeRemoval = locked();
    var s2 = section();
    fire('shopify:section:unload', s2);
    if (s2 && s2.parentNode) s2.parentNode.removeChild(s2);
    res.lockedAfterRemoval = locked();
    res.afterRemoval = counts();

    document.getElementById('o').textContent = '<<<' + JSON.stringify(res) + '>>>';
    document.title = 'DONE';
  }, 350);
};
document.body.appendChild(f);
</script>
"""

FAILURES = []
CHECKS = [0]


def check(label, ok, detail=''):
    CHECKS[0] += 1
    print('  %-58s %s %s' % (label, 'OK  ' if ok else '*** FAIL ***',
                             '' if ok else str(detail)[:150]))
    if not ok:
        FAILURES.append(label)


def make_probe_page():
    """home.html with the counting shim injected ahead of every theme script."""
    src = open(os.path.join(SITE, 'home.html'), encoding='utf-8').read()
    assert '<head>' in src
    out = src.replace('<head>', '<head>' + SHIM, 1)
    name = '_editor-target.html'
    open(os.path.join(SITE, name), 'w', encoding='utf-8').write(out)
    return name


def run():
    target = make_probe_page()
    open(os.path.join(SITE, '_editor.html'), 'w', encoding='utf-8').write(
        PROBE.replace('PAGE', target))
    shutil.rmtree(PROFILE, ignore_errors=True)
    out = os.path.join(HERE, 'editor-dom.html')
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run',
                    '--no-default-browser-check', '--user-data-dir=' + PROFILE,
                    '--virtual-time-budget=40000', '--window-size=1200,900', '--dump-dom',
                    'http://127.0.0.1:%d/_editor.html' % PORT],
                   stdout=open(out, 'w', encoding='utf-8'), stderr=subprocess.DEVNULL)
    d = open(out, encoding='utf-8', errors='replace').read()
    m = re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>', d, re.S)
    if not m:
        return None
    return json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')
                      .replace('&lt;', '<').replace('&gt;', '>'))


if __name__ == '__main__':
    r = run()
    if not r:
        print('NO READING — the probe produced no output')
        raise SystemExit(1)

    print('=== THE MENU OPENS AND LOCKS AS EXPECTED ===')
    check('the page is not locked on load', r['lockedAtStart'] is False)
    check('opening the menu locks the page', r['lockedWhenOpen'] is True)

    print()
    print('=== RE-RENDER WHILE THE MENU IS OPEN ===')
    check('the scroll lock is released by the re-render',
          r['lockedAfterRerenderWhileOpen'] is False,
          'html still carries menu-open, so the page is stuck')

    print()
    print('=== LISTENERS DO NOT ACCUMULATE ===')
    base, one, five = r['baseline'], r['afterOneRerender'], r['afterFiveRerenders']
    print('    baseline        %s' % base)
    print('    after 1 reload  %s' % one)
    print('    after 5 reloads %s' % five)
    check('window scroll listeners do not grow across re-renders',
          five['scroll'] <= one['scroll'], 'grew %d -> %d' % (one['scroll'], five['scroll']))
    check('matchMedia listeners do not grow across re-renders',
          five['mq'] <= one['mq'], 'grew %d -> %d' % (one['mq'], five['mq']))
    check('document keydown listeners do not grow across re-renders',
          five['keydown'] <= one['keydown'], 'grew %d -> %d' % (one['keydown'], five['keydown']))

    print()
    print('=== SECTION REMOVED WHILE THE MENU IS OPEN ===')
    check('the menu was open before removal', r['lockedBeforeRemoval'] is True)
    check('removal releases the scroll lock', r['lockedAfterRemoval'] is False,
          'the page is left scroll-locked with no header on it')
    check('removal releases the focus trap', r['afterRemoval']['keydown'] <= base['keydown'],
          'keydown listeners left bound: %d vs baseline %d'
          % (r['afterRemoval']['keydown'], base['keydown']))
    check('removal releases the scroll listener',
          r['afterRemoval']['scroll'] <= base['scroll'],
          'scroll listeners left bound: %d vs baseline %d'
          % (r['afterRemoval']['scroll'], base['scroll']))

    print()
    print('%d checks, %d passed, %d failed'
          % (CHECKS[0], CHECKS[0] - len(FAILURES), len(FAILURES)))
    print('OVERALL: %s' % ('PASS' if not FAILURES else '*** FAILURES ABOVE ***'))
