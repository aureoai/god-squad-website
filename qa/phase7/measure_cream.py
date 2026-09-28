# -*- coding: utf-8 -*-
"""The same contrast pass, on the cream scheme.

The ink band was measured first because it is the default; the cream option is
a merchant choice and must hold up too. On cream every role flips: the eyebrow
and value titles take --color-accent-strong, the body takes
--color-text-inverse-muted, and the caption rail becomes ink on a cream wash
over the photograph.
"""
import os, re, subprocess, sys, io, json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, 'site')
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 8807

HIDE = ('<style>.our-story__eyebrow,.our-story__heading,.our-story__body,'
        '.our-story__caption,.our-story__value-title,.our-story__value-body'
        '{visibility:hidden}'
        '.our-story__caption::before,.our-story__caption::after{visibility:visible}</style>')

src = open(os.path.join(SITE, 'case-cream.html'), encoding='utf-8').read()
open(os.path.join(SITE, 'case-cream-bg.html'), 'w', encoding='utf-8').write(
    src.replace('</head>', HIDE + '</head>'))

roles = open(os.path.join(SITE, 'roles.html'), encoding='utf-8').read()
open(os.path.join(SITE, 'roles-cream.html'), 'w', encoding='utf-8').write(
    roles.replace("f.src='case-story.html'", "f.src='case-cream.html'"))
print('cream backdrop and role probe written')


def shoot(page, w, h, out, min_colours=600):
    for n in (1, 2, 3):
        ww = w + 40 if w > 492 else 532
        subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                        '--no-first-run', '--no-default-browser-check',
                        '--user-data-dir=' + os.path.join(HERE, 'edge'),
                        '--virtual-time-budget=%d' % (20000 * n),
                        '--window-size=%d,%d' % (ww, h + 40),
                        '--screenshot=' + os.path.join(HERE, 'shots', 'raw.png'),
                        'http://127.0.0.1:%d/frame.html?w=%d&h=%d&src=%s' % (PORT, w, h, page)],
                       capture_output=True)
        subprocess.run([sys.executable, os.path.join(HERE, 'crop.py'),
                        os.path.join(HERE, 'shots', 'raw.png'),
                        os.path.join(HERE, 'shots', out), str(w), str(h)], capture_output=True)
        r = subprocess.run([sys.executable, os.path.join(HERE, 'hascheck.py'),
                            os.path.join(HERE, 'shots', out), '0', str(h)],
                           capture_output=True, text=True)
        try:
            c = int(r.stdout.strip())
        except Exception:
            c = 0
        if c > min_colours:
            print('  %-16s ok (%d colours)' % (out, c))
            return
    print('  %-16s THIN (%s)' % (out, c))


for w, h in [(1024, 1000), (1280, 1100), (1440, 1200), (1920, 1300)]:
    shoot('case-cream.html', w, h, 'os-w%d.png' % w)
    shoot('case-cream-bg.html', w, h, 'os-bg%d.png' % w)

subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-first-run',
                '--no-default-browser-check',
                '--user-data-dir=' + os.path.join(HERE, 'edge'),
                '--virtual-time-budget=40000', '--window-size=2200,1500', '--dump-dom',
                'http://127.0.0.1:%d/roles-cream.html' % PORT],
               stdout=open(os.path.join(HERE, 'roles-dom.html'), 'w', encoding='utf-8'),
               stderr=subprocess.DEVNULL)
d = open(os.path.join(HERE, 'roles-dom.html'), encoding='utf-8', errors='replace').read()
m = re.search(r'<pre id="o"[^>]*>&lt;&lt;&lt;(.*?)&gt;&gt;&gt;</pre>', d, re.S)
j = json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')
               .replace('&lt;', '<').replace('&gt;', '>'))
json.dump(j, open(os.path.join(HERE, 'roles.json'), 'w'), indent=1)

r = subprocess.run([sys.executable, os.path.join(HERE, 'contrast.py')],
                   capture_output=True, text=True)
print(r.stdout or r.stderr)
