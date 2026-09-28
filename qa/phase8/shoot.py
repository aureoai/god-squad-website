import tempfile
# -*- coding: utf-8 -*-
"""Capture a harness page at an exact CSS width.

Headless Edge's --screenshot never matches --window-size: below about 492px it
clamps the layout and crops the PNG, and above it the layout comes out ~24px
narrower than the window and is scaled up to fill the image. Everything is
therefore captured through an iframe of the exact target size and cropped.
Verified in Phase 5, re-confirmed in Phase 7.
"""
import os, shutil, subprocess, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 8808
SITE = os.path.join(HERE, 'site')
SHOTS = os.path.join(HERE, 'shots')
PROFILE = os.path.join(tempfile.gettempdir(), 'gs-edge-shoot')
os.makedirs(SHOTS, exist_ok=True)

FRAME = """<!doctype html><meta charset="utf-8"><title>f</title>
<style>html,body{margin:0;background:#fff}iframe{border:0;display:block}</style>
<iframe id="f" src="SRC" width="WIDTH" height="HEIGHT"></iframe>
<script>
document.getElementById('f').onload = function () {
  var d = this.contentDocument, w = this.contentWindow;
  var st = d.createElement('style');
  st.textContent = '*,*::before,*::after{transition:none!important;animation:none!important}';
  d.head.appendChild(st);
  if (OPENFLAG) { var b = d.querySelector('[data-cart-bubble]'); if (b) b.click(); }
  if (SCROLLY) { w.scrollTo(0, SCROLLY); }
};
</script>
"""


def shoot(page, width, height, out, open_drawer=False, scroll=0, tries=3):
    name = '_shoot.html'
    open(os.path.join(SITE, name), 'w', encoding='utf-8').write(
        FRAME.replace('SRC', page).replace('WIDTH', str(width))
        .replace('HEIGHT', str(height))
        .replace('OPENFLAG', 'true' if open_drawer else 'false')
        .replace('SCROLLY', str(scroll)))
    ww = width + 40 if width > 492 else 532
    for n in (1, 2, 3)[:tries]:
        subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                        '--no-first-run', '--no-default-browser-check',
                        '--force-prefers-reduced-motion',
                        '--user-data-dir=' + PROFILE,
                        '--virtual-time-budget=%d' % (18000 * n),
                        '--window-size=%d,%d' % (ww, height + 40),
                        '--screenshot=' + os.path.join(SHOTS, 'raw.png'),
                        'http://127.0.0.1:%d/%s' % (PORT, name)],
                       capture_output=True)
        subprocess.run([sys.executable, os.path.join(HERE, 'crop.py'),
                        os.path.join(SHOTS, 'raw.png'), os.path.join(SHOTS, out),
                        str(width), str(height)], capture_output=True)
        r = subprocess.run([sys.executable, os.path.join(HERE, 'hascheck.py'),
                            os.path.join(SHOTS, out), '0', str(height)],
                           capture_output=True, text=True)
        try:
            colours = int(r.stdout.strip())
        except Exception:
            colours = 0
        if colours > 400:
            print('  %-28s ok (%d colours)' % (out, colours))
            return True
    print('  %-28s THIN (%s colours)' % (out, colours))
    return False


if __name__ == '__main__':
    shutil.rmtree(PROFILE, ignore_errors=True)
    jobs = [
        ('p-sizes.html', 1440, 1150, 'pdp-1440.png', False, 0),
        ('p-sizes.html', 375, 1180, 'pdp-375.png', False, 0),
        ('p-multi.html', 1440, 1150, 'pdp-swatches-1440.png', False, 0),
        ('p-soldout.html', 1440, 1000, 'pdp-soldout-1440.png', False, 0),
        ('p-carousel.html', 1440, 1150, 'pdp-carousel-1440.png', False, 0),
        ('c-many.html', 1440, 1000, 'drawer-1440.png', True, 0),
        ('c-many.html', 375, 800, 'drawer-375.png', True, 0),
        ('c-empty.html', 1440, 900, 'drawer-empty-1440.png', True, 0),
        ('c-page-many.html', 1440, 1100, 'cart-page-1440.png', False, 0),
    ]
    for page, w, h, out, opened, scroll in jobs:
        shoot(page, w, h, out, opened, scroll)
    os.remove(os.path.join(SITE, '_shoot.html'))
    if os.path.exists(os.path.join(SHOTS, 'raw.png')):
        os.remove(os.path.join(SHOTS, 'raw.png'))
